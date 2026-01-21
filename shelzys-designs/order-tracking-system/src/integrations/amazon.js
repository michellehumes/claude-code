import fetch from 'node-fetch';
import CryptoJS from 'crypto-js';
import { config } from '../config/index.js';

/**
 * Amazon Selling Partner API (SP-API) Integration for Shelzy's Designs
 * Documentation: https://developer-docs.amazon.com/sp-api/
 */
export class AmazonClient {
  constructor() {
    this.sellerId = config.amazon.sellerId;
    this.marketplaceId = config.amazon.marketplaceId;
    this.refreshToken = config.amazon.refreshToken;
    this.clientId = config.amazon.clientId;
    this.clientSecret = config.amazon.clientSecret;
    this.region = config.amazon.region;
    this.baseUrl = config.amazon.baseUrl;
    this.accessToken = null;
    this.tokenExpiry = null;
  }

  /**
   * Get LWA (Login with Amazon) access token
   */
  async getAccessToken() {
    // Return cached token if still valid
    if (this.accessToken && this.tokenExpiry && Date.now() < this.tokenExpiry) {
      return this.accessToken;
    }

    const response = await fetch('https://api.amazon.com/auth/o2/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: this.refreshToken,
        client_id: this.clientId,
        client_secret: this.clientSecret,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to get Amazon access token: ${response.status}`);
    }

    const data = await response.json();
    this.accessToken = data.access_token;
    this.tokenExpiry = Date.now() + (data.expires_in * 1000) - 60000; // Subtract 1 minute for safety

    return this.accessToken;
  }

  /**
   * Generate AWS Signature V4 for SP-API requests
   */
  signRequest(method, path, queryParams, payload, headers, datetime) {
    const accessKey = config.amazon.accessKey;
    const secretKey = config.amazon.secretKey;
    const region = this.region;
    const service = 'execute-api';

    const date = datetime.slice(0, 8);
    const credentialScope = `${date}/${region}/${service}/aws4_request`;

    // Create canonical request
    const canonicalHeaders = Object.keys(headers)
      .sort()
      .map(key => `${key.toLowerCase()}:${headers[key]}`)
      .join('\n');

    const signedHeaders = Object.keys(headers)
      .sort()
      .map(key => key.toLowerCase())
      .join(';');

    const canonicalQueryString = queryParams
      ? Object.keys(queryParams)
          .sort()
          .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(queryParams[key])}`)
          .join('&')
      : '';

    const payloadHash = CryptoJS.SHA256(payload || '').toString(CryptoJS.enc.Hex);

    const canonicalRequest = [
      method,
      path,
      canonicalQueryString,
      canonicalHeaders + '\n',
      signedHeaders,
      payloadHash,
    ].join('\n');

    // Create string to sign
    const stringToSign = [
      'AWS4-HMAC-SHA256',
      datetime,
      credentialScope,
      CryptoJS.SHA256(canonicalRequest).toString(CryptoJS.enc.Hex),
    ].join('\n');

    // Calculate signature
    const kDate = CryptoJS.HmacSHA256(date, `AWS4${secretKey}`);
    const kRegion = CryptoJS.HmacSHA256(region, kDate);
    const kService = CryptoJS.HmacSHA256(service, kRegion);
    const kSigning = CryptoJS.HmacSHA256('aws4_request', kService);
    const signature = CryptoJS.HmacSHA256(stringToSign, kSigning).toString(CryptoJS.enc.Hex);

    return {
      authorization: `AWS4-HMAC-SHA256 Credential=${accessKey}/${credentialScope}, SignedHeaders=${signedHeaders}, Signature=${signature}`,
      signedHeaders,
    };
  }

  /**
   * Make authenticated request to Amazon SP-API
   */
  async request(method, path, queryParams = null, body = null) {
    const accessToken = await this.getAccessToken();
    const datetime = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
    const host = new URL(this.baseUrl).host;

    const headers = {
      'host': host,
      'x-amz-access-token': accessToken,
      'x-amz-date': datetime,
      'content-type': 'application/json',
    };

    const payload = body ? JSON.stringify(body) : '';
    const { authorization } = this.signRequest(method, path, queryParams, payload, headers, datetime);

    headers['Authorization'] = authorization;

    const url = queryParams
      ? `${this.baseUrl}${path}?${new URLSearchParams(queryParams)}`
      : `${this.baseUrl}${path}`;

    const response = await fetch(url, {
      method,
      headers,
      body: body ? payload : undefined,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(`Amazon SP-API Error: ${response.status} - ${JSON.stringify(error)}`);
    }

    return response.json();
  }

  /**
   * Get orders from Amazon
   * @param {Object} params - Query parameters
   * @param {string} params.CreatedAfter - ISO 8601 datetime
   * @param {string} params.CreatedBefore - ISO 8601 datetime
   * @param {string[]} params.OrderStatuses - Filter by status
   */
  async getOrders(params = {}) {
    const queryParams = {
      MarketplaceIds: this.marketplaceId,
      ...params,
    };

    return this.request('GET', '/orders/v0/orders', queryParams);
  }

  /**
   * Get a specific order by ID
   */
  async getOrder(orderId) {
    return this.request('GET', `/orders/v0/orders/${orderId}`);
  }

  /**
   * Get order items for an order
   */
  async getOrderItems(orderId) {
    return this.request('GET', `/orders/v0/orders/${orderId}/orderItems`);
  }

  /**
   * Get order address information
   */
  async getOrderAddress(orderId) {
    return this.request('GET', `/orders/v0/orders/${orderId}/address`);
  }

  /**
   * Get all orders with pagination
   */
  async getAllOrders(params = {}) {
    const allOrders = [];
    let nextToken = null;

    do {
      const queryParams = nextToken ? { NextToken: nextToken } : params;
      const response = await this.getOrders(queryParams);

      if (response.payload?.Orders) {
        allOrders.push(...response.payload.Orders);
      }

      nextToken = response.payload?.NextToken;
    } while (nextToken);

    return allOrders;
  }

  /**
   * Get shipment tracking for FBA orders
   */
  async getShipmentTracking(orderId) {
    try {
      // For FBA orders, tracking comes from fulfillment
      const order = await this.getOrder(orderId);
      if (order.payload?.FulfillmentChannel === 'AFN') {
        // Amazon Fulfilled Network - tracking is handled by Amazon
        return {
          carrier: 'Amazon',
          trackingNumber: null,
          status: order.payload?.OrderStatus,
        };
      }

      // For MFN (Merchant Fulfilled), tracking would be added by seller
      return null;
    } catch (error) {
      console.error(`Error getting tracking for order ${orderId}:`, error.message);
      return null;
    }
  }

  /**
   * Update shipment for merchant-fulfilled orders
   */
  async confirmShipment(orderId, shipmentData) {
    return this.request('POST', `/orders/v0/orders/${orderId}/shipment`, null, {
      marketplaceId: this.marketplaceId,
      packageDetail: {
        packageReferenceId: shipmentData.packageReferenceId || '1',
        carrierCode: shipmentData.carrier,
        trackingNumber: shipmentData.trackingNumber,
        shipDate: shipmentData.shipDate || new Date().toISOString(),
        orderItems: shipmentData.orderItems,
      },
    });
  }

  /**
   * Transform Amazon order to normalized order format
   */
  async normalizeOrder(order) {
    // Get additional details
    let items = [];
    let address = {};

    try {
      const itemsResponse = await this.getOrderItems(order.AmazonOrderId);
      items = itemsResponse.payload?.OrderItems || [];
    } catch (e) {
      console.warn(`Could not get items for order ${order.AmazonOrderId}`);
    }

    try {
      const addressResponse = await this.getOrderAddress(order.AmazonOrderId);
      address = addressResponse.payload?.ShippingAddress || {};
    } catch (e) {
      console.warn(`Could not get address for order ${order.AmazonOrderId}`);
    }

    return {
      platform: 'amazon',
      platformOrderId: order.AmazonOrderId,
      orderNumber: order.AmazonOrderId,
      status: this.mapAmazonStatus(order.OrderStatus),
      customerName: address.Name || order.BuyerInfo?.BuyerName || 'Unknown',
      customerEmail: order.BuyerInfo?.BuyerEmail || '',
      shippingAddress: {
        name: address.Name || '',
        street1: address.AddressLine1 || '',
        street2: address.AddressLine2 || '',
        city: address.City || '',
        state: address.StateOrRegion || '',
        postalCode: address.PostalCode || '',
        country: address.CountryCode || '',
      },
      items: items.map(item => ({
        productId: item.ASIN,
        title: item.Title,
        quantity: parseInt(item.QuantityOrdered) || 1,
        price: parseFloat(item.ItemPrice?.Amount || 0),
        sku: item.SellerSKU || '',
      })),
      subtotal: items.reduce((sum, item) => sum + parseFloat(item.ItemPrice?.Amount || 0), 0),
      shippingCost: parseFloat(order.ShippingPrice?.Amount || 0),
      tax: parseFloat(order.ItemTax?.Amount || 0),
      total: parseFloat(order.OrderTotal?.Amount || 0),
      currency: order.OrderTotal?.CurrencyCode || 'USD',
      platformFees: null, // Amazon doesn't expose fees in order API
      trackingNumber: null, // Would need to be fetched separately or added when shipping
      carrier: null,
      labelCreatedAt: null,
      shippedAt: order.OrderStatus === 'Shipped' ? new Date(order.LastUpdateDate) : null,
      deliveredAt: null,
      fulfillmentChannel: order.FulfillmentChannel, // AFN = FBA, MFN = Merchant
      isPrime: order.IsPrime || false,
      createdAt: new Date(order.PurchaseDate),
      updatedAt: new Date(order.LastUpdateDate),
      rawData: order,
    };
  }

  /**
   * Map Amazon order status to normalized status
   */
  mapAmazonStatus(amazonStatus) {
    const statusMap = {
      'Pending': 'pending',
      'Unshipped': 'paid',
      'PartiallyShipped': 'shipped',
      'Shipped': 'shipped',
      'Delivered': 'delivered',
      'Canceled': 'cancelled',
      'Unfulfillable': 'error',
    };

    return statusMap[amazonStatus] || 'unknown';
  }

  /**
   * Get new orders since a specific timestamp
   */
  async getNewOrdersSince(timestamp) {
    const orders = await this.getAllOrders({
      CreatedAfter: timestamp.toISOString(),
    });

    const normalizedOrders = [];
    for (const order of orders) {
      normalizedOrders.push(await this.normalizeOrder(order));
    }

    return normalizedOrders;
  }

  /**
   * Get orders that need shipment (MFN orders that are unshipped)
   */
  async getOrdersNeedingShipment() {
    const orders = await this.getAllOrders({
      OrderStatuses: 'Unshipped',
    });

    // Filter to MFN (Merchant Fulfilled) orders only
    const mfnOrders = orders.filter(o => o.FulfillmentChannel === 'MFN');

    const normalizedOrders = [];
    for (const order of mfnOrders) {
      normalizedOrders.push(await this.normalizeOrder(order));
    }

    return normalizedOrders;
  }
}

export default AmazonClient;
