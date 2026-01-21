import Database from 'better-sqlite3';
import { config } from '../config/index.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let db = null;

/**
 * Initialize the SQLite database
 */
export function initDatabase() {
  const dbPath = config.app.databasePath.startsWith('.')
    ? join(__dirname, '../..', config.app.databasePath)
    : config.app.databasePath;

  // Ensure the data directory exists
  const dataDir = dirname(dbPath);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  db = new Database(dbPath);
  db.pragma('journal_mode = WAL');

  createTables();

  return db;
}

/**
 * Get database instance
 */
export function getDatabase() {
  if (!db) {
    return initDatabase();
  }
  return db;
}

/**
 * Create database tables
 */
function createTables() {
  // Orders table - main order information
  db.exec(`
    CREATE TABLE IF NOT EXISTS orders (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      platform TEXT NOT NULL,
      platform_order_id TEXT NOT NULL,
      order_number TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending',
      customer_name TEXT,
      customer_email TEXT,
      shipping_address TEXT,
      items TEXT,
      subtotal REAL DEFAULT 0,
      shipping_cost REAL DEFAULT 0,
      tax REAL DEFAULT 0,
      total REAL DEFAULT 0,
      currency TEXT DEFAULT 'USD',
      platform_fees REAL DEFAULT 0,
      net_revenue REAL DEFAULT 0,
      fulfillment_channel TEXT,
      is_prime INTEGER DEFAULT 0,
      created_at DATETIME,
      updated_at DATETIME,
      synced_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      raw_data TEXT,
      UNIQUE(platform, platform_order_id)
    )
  `);

  // Shipment tracking table - tracks shipment status changes
  db.exec(`
    CREATE TABLE IF NOT EXISTS shipments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      order_id INTEGER NOT NULL,
      tracking_number TEXT,
      carrier TEXT,
      carrier_code TEXT,
      service_type TEXT,
      label_created_at DATETIME,
      shipped_at DATETIME,
      out_for_delivery_at DATETIME,
      delivered_at DATETIME,
      delivery_signature TEXT,
      current_status TEXT DEFAULT 'pending',
      last_location TEXT,
      estimated_delivery DATETIME,
      actual_weight REAL,
      shipping_cost REAL,
      label_url TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (order_id) REFERENCES orders(id)
    )
  `);

  // Tracking events table - detailed tracking history
  db.exec(`
    CREATE TABLE IF NOT EXISTS tracking_events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      shipment_id INTEGER NOT NULL,
      event_type TEXT NOT NULL,
      event_status TEXT,
      event_description TEXT,
      location TEXT,
      event_timestamp DATETIME,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (shipment_id) REFERENCES shipments(id)
    )
  `);

  // Sync log table - tracks when syncs occurred
  db.exec(`
    CREATE TABLE IF NOT EXISTS sync_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      platform TEXT NOT NULL,
      sync_type TEXT NOT NULL,
      started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      completed_at DATETIME,
      orders_synced INTEGER DEFAULT 0,
      errors TEXT,
      status TEXT DEFAULT 'running'
    )
  `);

  // Notifications table - tracks sent notifications
  db.exec(`
    CREATE TABLE IF NOT EXISTS notifications (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      order_id INTEGER,
      shipment_id INTEGER,
      notification_type TEXT NOT NULL,
      channel TEXT NOT NULL,
      recipient TEXT,
      subject TEXT,
      message TEXT,
      sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      status TEXT DEFAULT 'sent',
      FOREIGN KEY (order_id) REFERENCES orders(id),
      FOREIGN KEY (shipment_id) REFERENCES shipments(id)
    )
  `);

  // Create indexes for better query performance
  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_orders_platform ON orders(platform);
    CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
    CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
    CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON shipments(order_id);
    CREATE INDEX IF NOT EXISTS idx_shipments_tracking ON shipments(tracking_number);
    CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(current_status);
    CREATE INDEX IF NOT EXISTS idx_tracking_events_shipment ON tracking_events(shipment_id);
  `);

  console.log('[Database] Tables created/verified successfully');
}

/**
 * Order model operations
 */
export const OrderModel = {
  /**
   * Create or update an order
   */
  upsert(order) {
    const db = getDatabase();
    const stmt = db.prepare(`
      INSERT INTO orders (
        platform, platform_order_id, order_number, status, customer_name,
        customer_email, shipping_address, items, subtotal, shipping_cost,
        tax, total, currency, platform_fees, net_revenue, fulfillment_channel,
        is_prime, created_at, updated_at, raw_data
      ) VALUES (
        @platform, @platformOrderId, @orderNumber, @status, @customerName,
        @customerEmail, @shippingAddress, @items, @subtotal, @shippingCost,
        @tax, @total, @currency, @platformFees, @netRevenue, @fulfillmentChannel,
        @isPrime, @createdAt, @updatedAt, @rawData
      )
      ON CONFLICT(platform, platform_order_id) DO UPDATE SET
        status = @status,
        customer_name = @customerName,
        customer_email = @customerEmail,
        shipping_address = @shippingAddress,
        items = @items,
        subtotal = @subtotal,
        shipping_cost = @shippingCost,
        tax = @tax,
        total = @total,
        platform_fees = @platformFees,
        net_revenue = @netRevenue,
        updated_at = @updatedAt,
        synced_at = CURRENT_TIMESTAMP,
        raw_data = @rawData
    `);

    const netRevenue = order.total - (order.platformFees || 0) - (order.shippingCost || 0);

    return stmt.run({
      platform: order.platform,
      platformOrderId: order.platformOrderId,
      orderNumber: order.orderNumber,
      status: order.status,
      customerName: order.customerName,
      customerEmail: order.customerEmail,
      shippingAddress: JSON.stringify(order.shippingAddress),
      items: JSON.stringify(order.items),
      subtotal: order.subtotal,
      shippingCost: order.shippingCost,
      tax: order.tax,
      total: order.total,
      currency: order.currency,
      platformFees: order.platformFees || 0,
      netRevenue: netRevenue,
      fulfillmentChannel: order.fulfillmentChannel || null,
      isPrime: order.isPrime ? 1 : 0,
      createdAt: order.createdAt?.toISOString(),
      updatedAt: order.updatedAt?.toISOString(),
      rawData: JSON.stringify(order.rawData),
    });
  },

  /**
   * Get order by ID
   */
  getById(id) {
    const db = getDatabase();
    const row = db.prepare('SELECT * FROM orders WHERE id = ?').get(id);
    return row ? this.parseOrder(row) : null;
  },

  /**
   * Get order by platform and platform order ID
   */
  getByPlatformId(platform, platformOrderId) {
    const db = getDatabase();
    const row = db.prepare('SELECT * FROM orders WHERE platform = ? AND platform_order_id = ?').get(platform, platformOrderId);
    return row ? this.parseOrder(row) : null;
  },

  /**
   * Get all orders with optional filters
   */
  getAll(filters = {}) {
    const db = getDatabase();
    let query = 'SELECT * FROM orders WHERE 1=1';
    const params = [];

    if (filters.platform) {
      query += ' AND platform = ?';
      params.push(filters.platform);
    }

    if (filters.status) {
      query += ' AND status = ?';
      params.push(filters.status);
    }

    if (filters.startDate) {
      query += ' AND created_at >= ?';
      params.push(filters.startDate);
    }

    if (filters.endDate) {
      query += ' AND created_at <= ?';
      params.push(filters.endDate);
    }

    query += ' ORDER BY created_at DESC';

    if (filters.limit) {
      query += ' LIMIT ?';
      params.push(filters.limit);
    }

    const rows = db.prepare(query).all(...params);
    return rows.map(row => this.parseOrder(row));
  },

  /**
   * Get orders needing tracking updates
   */
  getNeedingTrackingUpdate() {
    const db = getDatabase();
    const rows = db.prepare(`
      SELECT o.* FROM orders o
      LEFT JOIN shipments s ON o.id = s.order_id
      WHERE o.status IN ('paid', 'label_created', 'shipped')
      AND (s.delivered_at IS NULL OR s.id IS NULL)
      ORDER BY o.created_at ASC
    `).all();
    return rows.map(row => this.parseOrder(row));
  },

  /**
   * Update order status
   */
  updateStatus(id, status) {
    const db = getDatabase();
    return db.prepare('UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').run(status, id);
  },

  /**
   * Parse database row to order object
   */
  parseOrder(row) {
    return {
      ...row,
      shippingAddress: JSON.parse(row.shipping_address || '{}'),
      items: JSON.parse(row.items || '[]'),
      rawData: JSON.parse(row.raw_data || '{}'),
      isPrime: row.is_prime === 1,
    };
  },
};

/**
 * Shipment model operations
 */
export const ShipmentModel = {
  /**
   * Create a new shipment record
   */
  create(shipment) {
    const db = getDatabase();
    const stmt = db.prepare(`
      INSERT INTO shipments (
        order_id, tracking_number, carrier, carrier_code, service_type,
        label_created_at, current_status, shipping_cost, label_url
      ) VALUES (
        @orderId, @trackingNumber, @carrier, @carrierCode, @serviceType,
        @labelCreatedAt, @currentStatus, @shippingCost, @labelUrl
      )
    `);

    return stmt.run({
      orderId: shipment.orderId,
      trackingNumber: shipment.trackingNumber,
      carrier: shipment.carrier,
      carrierCode: shipment.carrierCode || null,
      serviceType: shipment.serviceType || null,
      labelCreatedAt: shipment.labelCreatedAt || new Date().toISOString(),
      currentStatus: shipment.currentStatus || 'label_created',
      shippingCost: shipment.shippingCost || null,
      labelUrl: shipment.labelUrl || null,
    });
  },

  /**
   * Get shipment by order ID
   */
  getByOrderId(orderId) {
    const db = getDatabase();
    return db.prepare('SELECT * FROM shipments WHERE order_id = ?').get(orderId);
  },

  /**
   * Get shipment by tracking number
   */
  getByTrackingNumber(trackingNumber) {
    const db = getDatabase();
    return db.prepare('SELECT * FROM shipments WHERE tracking_number = ?').get(trackingNumber);
  },

  /**
   * Update shipment status
   */
  updateStatus(id, updates) {
    const db = getDatabase();
    const fields = [];
    const params = [];

    if (updates.currentStatus) {
      fields.push('current_status = ?');
      params.push(updates.currentStatus);
    }
    if (updates.shippedAt) {
      fields.push('shipped_at = ?');
      params.push(updates.shippedAt);
    }
    if (updates.outForDeliveryAt) {
      fields.push('out_for_delivery_at = ?');
      params.push(updates.outForDeliveryAt);
    }
    if (updates.deliveredAt) {
      fields.push('delivered_at = ?');
      params.push(updates.deliveredAt);
    }
    if (updates.lastLocation) {
      fields.push('last_location = ?');
      params.push(updates.lastLocation);
    }
    if (updates.estimatedDelivery) {
      fields.push('estimated_delivery = ?');
      params.push(updates.estimatedDelivery);
    }
    if (updates.deliverySignature) {
      fields.push('delivery_signature = ?');
      params.push(updates.deliverySignature);
    }

    fields.push('updated_at = CURRENT_TIMESTAMP');
    params.push(id);

    const query = `UPDATE shipments SET ${fields.join(', ')} WHERE id = ?`;
    return db.prepare(query).run(...params);
  },

  /**
   * Get shipments needing tracking updates
   */
  getNeedingUpdate() {
    const db = getDatabase();
    return db.prepare(`
      SELECT s.*, o.platform, o.order_number
      FROM shipments s
      JOIN orders o ON s.order_id = o.id
      WHERE s.current_status NOT IN ('delivered', 'returned', 'exception')
      AND s.tracking_number IS NOT NULL
      ORDER BY s.created_at ASC
    `).all();
  },
};

/**
 * Tracking events model operations
 */
export const TrackingEventModel = {
  /**
   * Add a tracking event
   */
  add(event) {
    const db = getDatabase();
    const stmt = db.prepare(`
      INSERT INTO tracking_events (
        shipment_id, event_type, event_status, event_description,
        location, event_timestamp
      ) VALUES (
        @shipmentId, @eventType, @eventStatus, @eventDescription,
        @location, @eventTimestamp
      )
    `);

    return stmt.run({
      shipmentId: event.shipmentId,
      eventType: event.eventType,
      eventStatus: event.eventStatus || null,
      eventDescription: event.eventDescription || null,
      location: event.location || null,
      eventTimestamp: event.eventTimestamp || new Date().toISOString(),
    });
  },

  /**
   * Get events for a shipment
   */
  getByShipmentId(shipmentId) {
    const db = getDatabase();
    return db.prepare(`
      SELECT * FROM tracking_events
      WHERE shipment_id = ?
      ORDER BY event_timestamp DESC
    `).all(shipmentId);
  },
};

/**
 * Sync log model operations
 */
export const SyncLogModel = {
  /**
   * Start a sync log entry
   */
  start(platform, syncType) {
    const db = getDatabase();
    const result = db.prepare(`
      INSERT INTO sync_log (platform, sync_type, status)
      VALUES (?, ?, 'running')
    `).run(platform, syncType);
    return result.lastInsertRowid;
  },

  /**
   * Complete a sync log entry
   */
  complete(id, ordersSynced, errors = null) {
    const db = getDatabase();
    return db.prepare(`
      UPDATE sync_log
      SET completed_at = CURRENT_TIMESTAMP,
          orders_synced = ?,
          errors = ?,
          status = ?
      WHERE id = ?
    `).run(ordersSynced, errors, errors ? 'error' : 'completed', id);
  },

  /**
   * Get last sync for a platform
   */
  getLastSync(platform) {
    const db = getDatabase();
    return db.prepare(`
      SELECT * FROM sync_log
      WHERE platform = ? AND status = 'completed'
      ORDER BY completed_at DESC
      LIMIT 1
    `).get(platform);
  },
};

export default { initDatabase, getDatabase, OrderModel, ShipmentModel, TrackingEventModel, SyncLogModel };
