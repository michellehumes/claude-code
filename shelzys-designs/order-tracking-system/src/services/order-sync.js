import { EtsyClient } from '../integrations/etsy.js';
import { AmazonClient } from '../integrations/amazon.js';
import { OrderModel, ShipmentModel, SyncLogModel, initDatabase } from '../models/database.js';
import { config, validateConfig } from '../config/index.js';

/**
 * Order Sync Service for Shelzy's Designs
 * Synchronizes orders from Etsy and Amazon to local database
 */
export class OrderSyncService {
  constructor() {
    this.etsyClient = null;
    this.amazonClient = null;
    initDatabase();
  }

  /**
   * Initialize platform clients
   */
  async initialize() {
    // Initialize Etsy client if configured
    try {
      validateConfig('etsy');
      this.etsyClient = new EtsyClient();
      console.log('[Sync] Etsy client initialized');
    } catch (e) {
      console.warn('[Sync] Etsy not configured:', e.message);
    }

    // Initialize Amazon client if configured
    try {
      validateConfig('amazon');
      this.amazonClient = new AmazonClient();
      console.log('[Sync] Amazon client initialized');
    } catch (e) {
      console.warn('[Sync] Amazon not configured:', e.message);
    }
  }

  /**
   * Sync all orders from all configured platforms
   */
  async syncAll() {
    console.log('[Sync] Starting full sync...');
    const results = {
      etsy: { synced: 0, errors: [] },
      amazon: { synced: 0, errors: [] },
    };

    if (this.etsyClient) {
      results.etsy = await this.syncEtsyOrders();
    }

    if (this.amazonClient) {
      results.amazon = await this.syncAmazonOrders();
    }

    console.log('[Sync] Full sync completed:', results);
    return results;
  }

  /**
   * Sync orders from Etsy
   */
  async syncEtsyOrders(options = {}) {
    if (!this.etsyClient) {
      throw new Error('Etsy client not initialized');
    }

    const syncLogId = SyncLogModel.start('etsy', 'orders');
    const errors = [];
    let synced = 0;

    try {
      console.log('[Etsy] Fetching orders...');

      // Determine start date for sync
      let startDate;
      if (options.fullSync) {
        // Full sync - get orders from last 90 days
        startDate = new Date();
        startDate.setDate(startDate.getDate() - 90);
      } else {
        // Incremental sync - get last sync time or default to 7 days
        const lastSync = SyncLogModel.getLastSync('etsy');
        if (lastSync?.completed_at) {
          startDate = new Date(lastSync.completed_at);
        } else {
          startDate = new Date();
          startDate.setDate(startDate.getDate() - 7);
        }
      }

      console.log(`[Etsy] Fetching orders since ${startDate.toISOString()}`);

      // Fetch orders from Etsy
      const orders = await this.etsyClient.getNewOrdersSince(startDate);
      console.log(`[Etsy] Found ${orders.length} orders`);

      // Process each order
      for (const order of orders) {
        try {
          // Upsert order to database
          const result = OrderModel.upsert(order);
          const orderId = result.lastInsertRowid || OrderModel.getByPlatformId('etsy', order.platformOrderId)?.id;

          // Create/update shipment if tracking info exists
          if (order.trackingNumber) {
            const existingShipment = ShipmentModel.getByOrderId(orderId);
            if (!existingShipment) {
              ShipmentModel.create({
                orderId: orderId,
                trackingNumber: order.trackingNumber,
                carrier: order.carrier,
                labelCreatedAt: order.labelCreatedAt ? new Date(order.labelCreatedAt).toISOString() : null,
                currentStatus: order.status === 'shipped' ? 'in_transit' : 'label_created',
              });
            }
          }

          synced++;
        } catch (e) {
          console.error(`[Etsy] Error processing order ${order.platformOrderId}:`, e.message);
          errors.push({ orderId: order.platformOrderId, error: e.message });
        }
      }

      SyncLogModel.complete(syncLogId, synced, errors.length > 0 ? JSON.stringify(errors) : null);
      console.log(`[Etsy] Sync completed: ${synced} orders synced`);

    } catch (e) {
      console.error('[Etsy] Sync failed:', e.message);
      SyncLogModel.complete(syncLogId, synced, e.message);
      errors.push({ error: e.message });
    }

    return { synced, errors };
  }

  /**
   * Sync orders from Amazon
   */
  async syncAmazonOrders(options = {}) {
    if (!this.amazonClient) {
      throw new Error('Amazon client not initialized');
    }

    const syncLogId = SyncLogModel.start('amazon', 'orders');
    const errors = [];
    let synced = 0;

    try {
      console.log('[Amazon] Fetching orders...');

      // Determine start date for sync
      let startDate;
      if (options.fullSync) {
        // Full sync - get orders from last 90 days (Amazon limit)
        startDate = new Date();
        startDate.setDate(startDate.getDate() - 90);
      } else {
        // Incremental sync - get last sync time or default to 7 days
        const lastSync = SyncLogModel.getLastSync('amazon');
        if (lastSync?.completed_at) {
          startDate = new Date(lastSync.completed_at);
        } else {
          startDate = new Date();
          startDate.setDate(startDate.getDate() - 7);
        }
      }

      console.log(`[Amazon] Fetching orders since ${startDate.toISOString()}`);

      // Fetch orders from Amazon
      const orders = await this.amazonClient.getNewOrdersSince(startDate);
      console.log(`[Amazon] Found ${orders.length} orders`);

      // Process each order
      for (const order of orders) {
        try {
          // Upsert order to database
          const result = OrderModel.upsert(order);
          const orderId = result.lastInsertRowid || OrderModel.getByPlatformId('amazon', order.platformOrderId)?.id;

          // Create shipment record if it has tracking
          if (order.trackingNumber) {
            const existingShipment = ShipmentModel.getByOrderId(orderId);
            if (!existingShipment) {
              ShipmentModel.create({
                orderId: orderId,
                trackingNumber: order.trackingNumber,
                carrier: order.carrier,
                currentStatus: order.status === 'shipped' ? 'in_transit' : 'label_created',
              });
            }
          }

          synced++;
        } catch (e) {
          console.error(`[Amazon] Error processing order ${order.platformOrderId}:`, e.message);
          errors.push({ orderId: order.platformOrderId, error: e.message });
        }
      }

      SyncLogModel.complete(syncLogId, synced, errors.length > 0 ? JSON.stringify(errors) : null);
      console.log(`[Amazon] Sync completed: ${synced} orders synced`);

    } catch (e) {
      console.error('[Amazon] Sync failed:', e.message);
      SyncLogModel.complete(syncLogId, synced, e.message);
      errors.push({ error: e.message });
    }

    return { synced, errors };
  }

  /**
   * Get orders summary statistics
   */
  getOrdersSummary() {
    const allOrders = OrderModel.getAll({});

    const summary = {
      total: allOrders.length,
      byPlatform: {},
      byStatus: {},
      revenue: {
        total: 0,
        byPlatform: {},
      },
      recentOrders: allOrders.slice(0, 10),
    };

    for (const order of allOrders) {
      // By platform
      summary.byPlatform[order.platform] = (summary.byPlatform[order.platform] || 0) + 1;

      // By status
      summary.byStatus[order.status] = (summary.byStatus[order.status] || 0) + 1;

      // Revenue
      summary.revenue.total += order.total || 0;
      summary.revenue.byPlatform[order.platform] = (summary.revenue.byPlatform[order.platform] || 0) + (order.total || 0);
    }

    return summary;
  }

  /**
   * Get orders needing action (unshipped, pending, etc.)
   */
  getOrdersNeedingAction() {
    return {
      pending: OrderModel.getAll({ status: 'pending' }),
      paid: OrderModel.getAll({ status: 'paid' }),
      needsTracking: OrderModel.getNeedingTrackingUpdate(),
    };
  }
}

export default OrderSyncService;
