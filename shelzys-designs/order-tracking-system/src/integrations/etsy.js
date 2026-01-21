import fetch from 'node-fetch';
import { config, validateConfig } from '../config/index.js';

/**
 * Etsy API v3 Integration for Shelzy's Designs
 * Documentation: https://developers.etsy.com/documentation/
 */
export class EtsyClient {
  constructor() {
    this.baseUrl = config.etsy.baseUrl;
    this.apiKey = config.etsy.apiKey;
    this.shopId = config.etsy.shopId;
    this.accessToken = config.etsy.accessToken;
    this.refreshToken = config.etsy.refreshToken;
  }

  /**
   * Make authenticated request to Etsy API
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    const headers = {
      'x-api-key': this.apiKey,
      'Authorization': `Bearer ${this.accessToken}`,
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      // Token expired, try to refresh
      await this.refreshAccessToken();
      headers['Authorization'] = `Bearer ${this.accessToken}`;
      return fetch(url, { ...options, headers });
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`Etsy API Error: ${response.status} - ${error.error || response.statusText}`);
    }

    return response.json();
  }

  /**
   * Refresh OAuth access token
   */
  async refreshAccessToken() {
    const response = await fetch('https://api.etsy.com/v3/public/oauth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        client_id: this.apiKey,
        refresh_token: this.refreshToken,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to refresh Etsy access token');
    }

    const data = await response.json();
    this.accessToken = data.access_token;
    this.refreshToken = data.refresh_token;

    // Note: In production, you'd want to save these new tokens to your .env or database
    console.log('[Etsy] Access token refreshed successfully');
    return data;
  }

  /**
   * Get shop information
   */
  async getShop() {
    return this.request(`/application/shops/${this.shopId}`);
  }

  /**
   * Get all receipts (orders) for the shop
   * @param {Object} params - Query parameters
   * @param {number} params.limit - Number of results (max 100)
   * @param {number} params.offset - Pagination offset
   * @param {string} params.min_created - Minimum creation timestamp
   * @param {string} params.max_created - Maximum creation timestamp
   * @param {boolean} params.was_shipped - Filter by shipped status
   * @param {boolean} params.was_paid - Filter by paid status
   */
  async getReceipts(params = {}) {
    const queryParams = new URLSearchParams({
      limit: params.limit || 25,
      offset: params.offset || 0,
      ...params,
    });

    return this.request(`/application/shops/${this.shopId}/receipts?${queryParams}`);
  }

  /**
   * Get a specific receipt by ID
   */
  async getReceipt(receiptId) {
    return this.request(`/application/shops/${this.shopId}/receipts/${receiptId}`);
  }

  /**
   * Get all receipts with pagination
   */
  async getAllReceipts(params = {}) {
    const allReceipts = [];
    let offset = 0;
    const limit = 100;
    let hasMore = true;

    while (hasMore) {
      const response = await this.getReceipts({ ...params, limit, offset });
      allReceipts.push(...response.results);

      hasMore = response.results.length === limit;
      offset += limit;
    }

    return allReceipts;
  }

  /**
   * Get transactions (line items) for a receipt
   */
  async getReceiptTransactions(receiptId) {
    return this.request(`/application/shops/${this.shopId}/receipts/${receiptId}/transactions`);
  }

  /**
   * Get shipment information for a receipt
   */
  async getReceiptShipments(receiptId) {
    return this.request(`/application/shops/${this.shopId}/receipts/${receiptId}/shipments`);
  }

  /**
   * Create a shipment for a receipt
   */
  async createShipment(receiptId, shipmentData) {
    return this.request(`/application/shops/${this.shopId}/receipts/${receiptId}/shipments`, {
      method: 'POST',
      body: JSON.stringify(shipmentData),
    });
  }

  /**
   * Transform Etsy receipt to normalized order format
   */
  normalizeOrder(receipt) {
    return {
      platform: 'etsy',
      platformOrderId: String(receipt.receipt_id),
      orderNumber: String(receipt.receipt_id),
      status: this.mapEtsyStatus(receipt),
      customerName: receipt.name || 'Unknown',
      customerEmail: receipt.buyer_email || '',
      shippingAddress: {
        name: receipt.name,
        street1: receipt.first_line,
        street2: receipt.second_line || '',
        city: receipt.city,
        state: receipt.state,
        postalCode: receipt.zip,
        country: receipt.country_iso,
      },
      items: (receipt.transactions || []).map(t => ({
        productId: String(t.listing_id),
        title: t.title,
        quantity: t.quantity,
        price: parseFloat(t.price?.amount || 0) / parseFloat(t.price?.divisor || 100),
        sku: t.product_data?.sku || '',
      })),
      subtotal: parseFloat(receipt.subtotal?.amount || 0) / parseFloat(receipt.subtotal?.divisor || 100),
      shippingCost: parseFloat(receipt.total_shipping_cost?.amount || 0) / parseFloat(receipt.total_shipping_cost?.divisor || 100),
      tax: parseFloat(receipt.total_tax_cost?.amount || 0) / parseFloat(receipt.total_tax_cost?.divisor || 100),
      total: parseFloat(receipt.grandtotal?.amount || 0) / parseFloat(receipt.grandtotal?.divisor || 100),
      currency: receipt.grandtotal?.currency_code || 'USD',
      platformFees: parseFloat(receipt.total_fees?.amount || 0) / parseFloat(receipt.total_fees?.divisor || 100),
      trackingNumber: receipt.shipments?.[0]?.tracking_code || null,
      carrier: receipt.shipments?.[0]?.carrier_name || null,
      labelCreatedAt: receipt.shipments?.[0]?.mail_class ? receipt.create_timestamp * 1000 : null,
      shippedAt: receipt.shipments?.[0]?.shipped_date ? receipt.shipments[0].shipped_date * 1000 : null,
      deliveredAt: null, // Etsy doesn't provide delivery confirmation directly
      createdAt: new Date(receipt.create_timestamp * 1000),
      updatedAt: new Date(receipt.update_timestamp * 1000),
      rawData: receipt,
    };
  }

  /**
   * Map Etsy receipt status to normalized status
   */
  mapEtsyStatus(receipt) {
    if (receipt.is_delivered) return 'delivered';
    if (receipt.is_shipped) return 'shipped';
    if (receipt.shipments?.length > 0) return 'label_created';
    if (receipt.is_paid) return 'paid';
    return 'pending';
  }

  /**
   * Get new orders since a specific timestamp
   */
  async getNewOrdersSince(timestamp) {
    const minCreated = Math.floor(timestamp.getTime() / 1000);
    const receipts = await this.getAllReceipts({ min_created: minCreated });
    return receipts.map(r => this.normalizeOrder(r));
  }

  /**
   * Get orders that need shipment tracking updates
   */
  async getOrdersNeedingTrackingUpdate() {
    const receipts = await this.getAllReceipts({ was_shipped: false, was_paid: true });
    return receipts.map(r => this.normalizeOrder(r));
  }
}

export default EtsyClient;
