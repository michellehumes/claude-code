import nodemailer from 'nodemailer';
import { config } from '../config/index.js';
import { initDatabase, getDatabase } from '../models/database.js';

/**
 * Notification Service for Shelzy's Designs Order Tracking
 * Sends email notifications for order status changes
 */
export class NotificationService {
  constructor() {
    initDatabase();
    this.transporter = null;
    this.initialize();
  }

  /**
   * Initialize email transporter
   */
  initialize() {
    if (config.email.user && config.email.password) {
      this.transporter = nodemailer.createTransport({
        host: config.email.host,
        port: config.email.port,
        secure: config.email.port === 465,
        auth: {
          user: config.email.user,
          pass: config.email.password,
        },
      });
      console.log('[Notifications] Email service initialized');
    } else {
      console.warn('[Notifications] Email not configured - notifications will be logged only');
    }
  }

  /**
   * Send an email notification
   */
  async sendEmail(to, subject, html, text) {
    if (!this.transporter) {
      console.log(`[Notifications] Would send email to ${to}: ${subject}`);
      return { messageId: 'not-sent', logged: true };
    }

    try {
      const result = await this.transporter.sendMail({
        from: `"Shelzy's Designs Order Tracker" <${config.email.user}>`,
        to,
        subject,
        html,
        text,
      });

      this.logNotification({
        notificationType: 'email',
        channel: 'email',
        recipient: to,
        subject,
        message: text || html,
        status: 'sent',
      });

      console.log(`[Notifications] Email sent: ${result.messageId}`);
      return result;
    } catch (e) {
      console.error('[Notifications] Failed to send email:', e.message);
      this.logNotification({
        notificationType: 'email',
        channel: 'email',
        recipient: to,
        subject,
        message: text || html,
        status: 'failed',
      });
      throw e;
    }
  }

  /**
   * Log notification to database
   */
  logNotification(notification) {
    const db = getDatabase();
    db.prepare(`
      INSERT INTO notifications (
        order_id, shipment_id, notification_type, channel,
        recipient, subject, message, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      notification.orderId || null,
      notification.shipmentId || null,
      notification.notificationType,
      notification.channel,
      notification.recipient,
      notification.subject,
      notification.message,
      notification.status
    );
  }

  /**
   * Send new order notification
   */
  async notifyNewOrder(order) {
    const subject = `New Order: ${order.orderNumber} from ${order.platform.toUpperCase()}`;
    const html = `
      <h2>New Order Received!</h2>
      <p><strong>Order #:</strong> ${order.orderNumber}</p>
      <p><strong>Platform:</strong> ${order.platform.toUpperCase()}</p>
      <p><strong>Customer:</strong> ${order.customerName}</p>
      <p><strong>Total:</strong> $${order.total?.toFixed(2)} ${order.currency}</p>
      <h3>Items:</h3>
      <ul>
        ${order.items?.map(item => `
          <li>${item.title} x ${item.quantity} - $${item.price?.toFixed(2)}</li>
        `).join('') || '<li>No items</li>'}
      </ul>
      <h3>Shipping Address:</h3>
      <p>
        ${order.shippingAddress?.name || ''}<br>
        ${order.shippingAddress?.street1 || ''}<br>
        ${order.shippingAddress?.street2 ? order.shippingAddress.street2 + '<br>' : ''}
        ${order.shippingAddress?.city || ''}, ${order.shippingAddress?.state || ''} ${order.shippingAddress?.postalCode || ''}<br>
        ${order.shippingAddress?.country || ''}
      </p>
    `;

    const text = `New Order: ${order.orderNumber} from ${order.platform}. Customer: ${order.customerName}. Total: $${order.total?.toFixed(2)}`;

    return this.sendEmail(config.email.notificationEmail, subject, html, text);
  }

  /**
   * Send label created notification
   */
  async notifyLabelCreated(order, shipment) {
    const subject = `Label Created: Order ${order.orderNumber}`;
    const html = `
      <h2>Shipping Label Created</h2>
      <p><strong>Order #:</strong> ${order.orderNumber}</p>
      <p><strong>Tracking #:</strong> ${shipment.tracking_number || shipment.trackingNumber}</p>
      <p><strong>Carrier:</strong> ${shipment.carrier}</p>
      <p><strong>Customer:</strong> ${order.customerName}</p>
      <p>The shipping label has been created. Don't forget to ship the package!</p>
    `;

    const text = `Label created for order ${order.orderNumber}. Tracking: ${shipment.tracking_number || shipment.trackingNumber}`;

    return this.sendEmail(config.email.notificationEmail, subject, html, text);
  }

  /**
   * Send shipped notification
   */
  async notifyShipped(order, shipment) {
    const subject = `Shipped: Order ${order.orderNumber}`;
    const html = `
      <h2>Order Shipped!</h2>
      <p><strong>Order #:</strong> ${order.orderNumber}</p>
      <p><strong>Tracking #:</strong> ${shipment.tracking_number || shipment.trackingNumber}</p>
      <p><strong>Carrier:</strong> ${shipment.carrier}</p>
      <p><strong>Customer:</strong> ${order.customerName}</p>
      <p>Package is now in transit to the customer.</p>
    `;

    const text = `Order ${order.orderNumber} shipped. Tracking: ${shipment.tracking_number || shipment.trackingNumber}`;

    return this.sendEmail(config.email.notificationEmail, subject, html, text);
  }

  /**
   * Send delivery notification
   */
  async notifyDelivered(order, shipment) {
    const subject = `Delivered: Order ${order.orderNumber}`;
    const html = `
      <h2>Order Delivered!</h2>
      <p><strong>Order #:</strong> ${order.orderNumber}</p>
      <p><strong>Tracking #:</strong> ${shipment.tracking_number || shipment.trackingNumber}</p>
      <p><strong>Customer:</strong> ${order.customerName}</p>
      <p><strong>Delivered:</strong> ${shipment.delivered_at || shipment.deliveredAt}</p>
      ${shipment.delivery_signature ? `<p><strong>Signature:</strong> ${shipment.delivery_signature}</p>` : ''}
      <p>The package has been delivered successfully!</p>
    `;

    const text = `Order ${order.orderNumber} delivered to ${order.customerName}`;

    return this.sendEmail(config.email.notificationEmail, subject, html, text);
  }

  /**
   * Send daily summary email
   */
  async sendDailySummary(summary) {
    const subject = `Daily Order Summary - Shelzy's Designs`;
    const html = `
      <h2>Daily Order Summary</h2>
      <p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>

      <h3>Order Status Overview</h3>
      <table border="1" cellpadding="8" cellspacing="0">
        <tr><th>Status</th><th>Count</th></tr>
        <tr><td>Pending</td><td>${summary.pending || 0}</td></tr>
        <tr><td>Awaiting Shipment</td><td>${summary.paid || 0}</td></tr>
        <tr><td>Label Created</td><td>${summary.labelCreated || 0}</td></tr>
        <tr><td>Shipped</td><td>${summary.shipped || 0}</td></tr>
        <tr><td>Delivered</td><td>${summary.delivered || 0}</td></tr>
        <tr><td><strong>Total</strong></td><td><strong>${summary.total || 0}</strong></td></tr>
      </table>

      <h3>Revenue Summary</h3>
      <p><strong>Total Revenue:</strong> $${summary.revenue?.total?.toFixed(2) || '0.00'}</p>
      ${Object.entries(summary.revenue?.byPlatform || {}).map(([platform, amount]) =>
        `<p><strong>${platform.toUpperCase()}:</strong> $${amount.toFixed(2)}</p>`
      ).join('')}

      <h3>Action Required</h3>
      <ul>
        <li>${summary.paid || 0} orders need shipping</li>
        <li>${summary.needsTracking || 0} shipments need tracking updates</li>
      </ul>
    `;

    const text = `Daily Summary: ${summary.total} orders, $${summary.revenue?.total?.toFixed(2)} revenue`;

    return this.sendEmail(config.email.notificationEmail, subject, html, text);
  }
}

export default NotificationService;
