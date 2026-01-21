import fetch from 'node-fetch';
import { ShipmentModel, TrackingEventModel, OrderModel, initDatabase } from '../models/database.js';
import { config } from '../config/index.js';

/**
 * Shipment Tracking Service for Shelzy's Designs
 * Tracks shipments through label creation, in-transit, and delivery
 */
export class ShipmentTrackingService {
  constructor() {
    initDatabase();
    this.carrierAPIs = {
      usps: new USPSTracker(),
      ups: new UPSTracker(),
      fedex: new FedExTracker(),
    };
  }

  /**
   * Record when a shipping label is created
   */
  async recordLabelCreated(orderId, labelData) {
    const order = OrderModel.getById(orderId);
    if (!order) {
      throw new Error(`Order ${orderId} not found`);
    }

    // Check if shipment already exists
    let shipment = ShipmentModel.getByOrderId(orderId);

    if (!shipment) {
      // Create new shipment record
      const result = ShipmentModel.create({
        orderId: orderId,
        trackingNumber: labelData.trackingNumber,
        carrier: labelData.carrier,
        carrierCode: this.normalizeCarrierCode(labelData.carrier),
        serviceType: labelData.serviceType,
        labelCreatedAt: new Date().toISOString(),
        currentStatus: 'label_created',
        shippingCost: labelData.shippingCost,
        labelUrl: labelData.labelUrl,
      });

      shipment = ShipmentModel.getByOrderId(orderId);
    }

    // Add tracking event
    TrackingEventModel.add({
      shipmentId: shipment.id,
      eventType: 'label_created',
      eventStatus: 'Label Created',
      eventDescription: `Shipping label created with ${labelData.carrier}`,
      eventTimestamp: new Date().toISOString(),
    });

    // Update order status
    OrderModel.updateStatus(orderId, 'label_created');

    console.log(`[Tracking] Label created for order ${orderId}, tracking: ${labelData.trackingNumber}`);
    return shipment;
  }

  /**
   * Record when a package is shipped (handed to carrier)
   */
  async recordShipped(shipmentId, shippedData = {}) {
    const shipment = ShipmentModel.getByOrderId(shipmentId) ||
                     { id: shipmentId }; // Allow direct shipment ID

    ShipmentModel.updateStatus(shipment.id, {
      currentStatus: 'in_transit',
      shippedAt: shippedData.shippedAt || new Date().toISOString(),
      lastLocation: shippedData.location || 'Origin facility',
    });

    // Add tracking event
    TrackingEventModel.add({
      shipmentId: shipment.id,
      eventType: 'shipped',
      eventStatus: 'Shipped',
      eventDescription: 'Package accepted by carrier',
      location: shippedData.location || 'Origin facility',
      eventTimestamp: shippedData.shippedAt || new Date().toISOString(),
    });

    // Update order status
    if (shipment.order_id) {
      OrderModel.updateStatus(shipment.order_id, 'shipped');
    }

    console.log(`[Tracking] Package shipped, shipment ID: ${shipment.id}`);
    return shipment;
  }

  /**
   * Record when a package is delivered
   */
  async recordDelivered(shipmentId, deliveryData = {}) {
    const shipment = ShipmentModel.getByOrderId(shipmentId) ||
                     { id: shipmentId };

    ShipmentModel.updateStatus(shipment.id, {
      currentStatus: 'delivered',
      deliveredAt: deliveryData.deliveredAt || new Date().toISOString(),
      lastLocation: deliveryData.location || 'Delivered',
      deliverySignature: deliveryData.signature || null,
    });

    // Add tracking event
    TrackingEventModel.add({
      shipmentId: shipment.id,
      eventType: 'delivered',
      eventStatus: 'Delivered',
      eventDescription: deliveryData.description || 'Package delivered',
      location: deliveryData.location,
      eventTimestamp: deliveryData.deliveredAt || new Date().toISOString(),
    });

    // Update order status
    if (shipment.order_id) {
      OrderModel.updateStatus(shipment.order_id, 'delivered');
    }

    console.log(`[Tracking] Package delivered, shipment ID: ${shipment.id}`);
    return shipment;
  }

  /**
   * Update tracking status from carrier APIs
   */
  async updateTrackingStatus(shipmentId) {
    const shipment = typeof shipmentId === 'object' ? shipmentId : ShipmentModel.getByOrderId(shipmentId);

    if (!shipment || !shipment.tracking_number) {
      console.warn(`[Tracking] No tracking number for shipment ${shipmentId}`);
      return null;
    }

    const carrierCode = shipment.carrier_code || this.normalizeCarrierCode(shipment.carrier);
    const tracker = this.carrierAPIs[carrierCode];

    if (!tracker) {
      console.warn(`[Tracking] No tracker available for carrier: ${shipment.carrier}`);
      return null;
    }

    try {
      const trackingInfo = await tracker.track(shipment.tracking_number);

      if (trackingInfo) {
        // Update shipment status based on tracking
        const updates = {
          lastLocation: trackingInfo.lastLocation,
          estimatedDelivery: trackingInfo.estimatedDelivery,
        };

        // Determine status from tracking events
        const latestStatus = this.determineStatus(trackingInfo);
        updates.currentStatus = latestStatus;

        // Update timestamps based on status
        if (latestStatus === 'in_transit' && !shipment.shipped_at) {
          updates.shippedAt = trackingInfo.shippedAt || new Date().toISOString();
        }
        if (latestStatus === 'out_for_delivery' && !shipment.out_for_delivery_at) {
          updates.outForDeliveryAt = new Date().toISOString();
        }
        if (latestStatus === 'delivered' && !shipment.delivered_at) {
          updates.deliveredAt = trackingInfo.deliveredAt || new Date().toISOString();
          updates.deliverySignature = trackingInfo.signature;
        }

        ShipmentModel.updateStatus(shipment.id, updates);

        // Add new tracking events
        for (const event of trackingInfo.events || []) {
          // Check if event already exists (by timestamp)
          const existingEvents = TrackingEventModel.getByShipmentId(shipment.id);
          const eventExists = existingEvents.some(e =>
            e.event_timestamp === event.timestamp && e.event_description === event.description
          );

          if (!eventExists) {
            TrackingEventModel.add({
              shipmentId: shipment.id,
              eventType: event.type,
              eventStatus: event.status,
              eventDescription: event.description,
              location: event.location,
              eventTimestamp: event.timestamp,
            });
          }
        }

        // Update order status if needed
        if (shipment.order_id && ['shipped', 'delivered'].includes(latestStatus)) {
          OrderModel.updateStatus(shipment.order_id, latestStatus);
        }

        console.log(`[Tracking] Updated tracking for ${shipment.tracking_number}: ${latestStatus}`);
        return { ...shipment, ...updates, trackingInfo };
      }
    } catch (e) {
      console.error(`[Tracking] Error updating tracking for ${shipment.tracking_number}:`, e.message);
    }

    return shipment;
  }

  /**
   * Update all shipments needing tracking updates
   */
  async updateAllTracking() {
    const shipments = ShipmentModel.getNeedingUpdate();
    console.log(`[Tracking] Updating ${shipments.length} shipments...`);

    const results = {
      updated: 0,
      errors: [],
    };

    for (const shipment of shipments) {
      try {
        await this.updateTrackingStatus(shipment);
        results.updated++;

        // Small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (e) {
        results.errors.push({ tracking: shipment.tracking_number, error: e.message });
      }
    }

    console.log(`[Tracking] Bulk update completed: ${results.updated} updated, ${results.errors.length} errors`);
    return results;
  }

  /**
   * Get shipment status summary
   */
  getStatusSummary() {
    const allOrders = OrderModel.getAll({});

    return {
      total: allOrders.length,
      pending: allOrders.filter(o => o.status === 'pending').length,
      paid: allOrders.filter(o => o.status === 'paid').length,
      labelCreated: allOrders.filter(o => o.status === 'label_created').length,
      shipped: allOrders.filter(o => o.status === 'shipped').length,
      delivered: allOrders.filter(o => o.status === 'delivered').length,
    };
  }

  /**
   * Get tracking timeline for an order
   */
  getTrackingTimeline(orderId) {
    const order = OrderModel.getById(orderId);
    if (!order) return null;

    const shipment = ShipmentModel.getByOrderId(orderId);
    if (!shipment) return { order, shipment: null, events: [] };

    const events = TrackingEventModel.getByShipmentId(shipment.id);

    return {
      order,
      shipment,
      events,
      timeline: [
        { status: 'ordered', date: order.created_at, completed: true },
        { status: 'label_created', date: shipment.label_created_at, completed: !!shipment.label_created_at },
        { status: 'shipped', date: shipment.shipped_at, completed: !!shipment.shipped_at },
        { status: 'in_transit', date: null, completed: ['in_transit', 'out_for_delivery', 'delivered'].includes(shipment.current_status) },
        { status: 'out_for_delivery', date: shipment.out_for_delivery_at, completed: ['out_for_delivery', 'delivered'].includes(shipment.current_status) },
        { status: 'delivered', date: shipment.delivered_at, completed: shipment.current_status === 'delivered' },
      ],
    };
  }

  /**
   * Normalize carrier name to carrier code
   */
  normalizeCarrierCode(carrier) {
    if (!carrier) return null;

    const normalized = carrier.toLowerCase().trim();

    if (normalized.includes('usps') || normalized.includes('postal')) return 'usps';
    if (normalized.includes('ups')) return 'ups';
    if (normalized.includes('fedex') || normalized.includes('fed ex')) return 'fedex';
    if (normalized.includes('dhl')) return 'dhl';

    return normalized;
  }

  /**
   * Determine status from tracking info
   */
  determineStatus(trackingInfo) {
    if (trackingInfo.delivered) return 'delivered';
    if (trackingInfo.outForDelivery) return 'out_for_delivery';
    if (trackingInfo.inTransit) return 'in_transit';
    if (trackingInfo.shipped) return 'shipped';
    return 'label_created';
  }
}

/**
 * USPS Tracking API Client
 * Documentation: https://www.usps.com/business/web-tools-apis/track-and-confirm-api.htm
 */
class USPSTracker {
  constructor() {
    this.userId = config.carriers?.usps?.userId;
    this.baseUrl = 'https://secure.shippingapis.com/ShippingAPI.dll';
  }

  async track(trackingNumber) {
    if (!this.userId) {
      console.warn('[USPS] Tracker not configured - using simulated tracking');
      return this.simulateTracking(trackingNumber);
    }

    try {
      const xml = `
        <TrackFieldRequest USERID="${this.userId}">
          <TrackID ID="${trackingNumber}"></TrackID>
        </TrackFieldRequest>
      `;

      const response = await fetch(`${this.baseUrl}?API=TrackV2&XML=${encodeURIComponent(xml)}`);
      const text = await response.text();

      // Parse XML response (simplified - in production use proper XML parser)
      return this.parseResponse(text);
    } catch (e) {
      console.error('[USPS] Tracking error:', e.message);
      return this.simulateTracking(trackingNumber);
    }
  }

  parseResponse(xml) {
    // Simplified XML parsing - in production use proper XML parser like xml2js
    const events = [];
    const delivered = xml.includes('Delivered') || xml.includes('DELIVERED');
    const inTransit = xml.includes('In Transit') || xml.includes('transit');

    return {
      delivered,
      inTransit: inTransit && !delivered,
      lastLocation: this.extractLocation(xml),
      events,
    };
  }

  extractLocation(xml) {
    const match = xml.match(/<EventCity>([^<]+)<\/EventCity>/);
    return match ? match[1] : null;
  }

  simulateTracking(trackingNumber) {
    // Simulated tracking for development/demo
    return {
      delivered: false,
      inTransit: true,
      shipped: true,
      lastLocation: 'In Transit',
      estimatedDelivery: null,
      events: [
        {
          type: 'in_transit',
          status: 'In Transit',
          description: 'Package in transit to destination',
          timestamp: new Date().toISOString(),
        },
      ],
    };
  }
}

/**
 * UPS Tracking API Client
 */
class UPSTracker {
  constructor() {
    this.accessKey = config.carriers?.ups?.accessKey;
    this.userId = config.carriers?.ups?.userId;
    this.password = config.carriers?.ups?.password;
  }

  async track(trackingNumber) {
    if (!this.accessKey) {
      console.warn('[UPS] Tracker not configured - using simulated tracking');
      return this.simulateTracking(trackingNumber);
    }

    // UPS API implementation would go here
    // For now, return simulated data
    return this.simulateTracking(trackingNumber);
  }

  simulateTracking(trackingNumber) {
    return {
      delivered: false,
      inTransit: true,
      shipped: true,
      lastLocation: 'UPS Facility',
      estimatedDelivery: null,
      events: [
        {
          type: 'in_transit',
          status: 'In Transit',
          description: 'Package in transit',
          timestamp: new Date().toISOString(),
        },
      ],
    };
  }
}

/**
 * FedEx Tracking API Client
 */
class FedExTracker {
  constructor() {
    this.apiKey = config.carriers?.fedex?.apiKey;
    this.secretKey = config.carriers?.fedex?.secretKey;
  }

  async track(trackingNumber) {
    if (!this.apiKey) {
      console.warn('[FedEx] Tracker not configured - using simulated tracking');
      return this.simulateTracking(trackingNumber);
    }

    // FedEx API implementation would go here
    // For now, return simulated data
    return this.simulateTracking(trackingNumber);
  }

  simulateTracking(trackingNumber) {
    return {
      delivered: false,
      inTransit: true,
      shipped: true,
      lastLocation: 'FedEx Facility',
      estimatedDelivery: null,
      events: [
        {
          type: 'in_transit',
          status: 'In Transit',
          description: 'Package in transit',
          timestamp: new Date().toISOString(),
        },
      ],
    };
  }
}

export default ShipmentTrackingService;
