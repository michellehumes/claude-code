#!/usr/bin/env node

import { program } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import { OrderModel, ShipmentModel, initDatabase } from './models/database.js';
import { OrderSyncService } from './services/order-sync.js';
import { ShipmentTrackingService } from './services/shipment-tracking.js';
import { NotificationService } from './services/notifications.js';

// Initialize database
initDatabase();

/**
 * CLI Dashboard for Shelzy's Designs Order Tracking System
 */

program
  .name('shelzy-orders')
  .description('Order tracking dashboard for Shelzy\'s Designs')
  .version('1.0.0');

// Status command - show order status summary
program
  .command('status')
  .description('Show order status summary')
  .action(async () => {
    console.log(chalk.bold.blue('\n📦 Shelzy\'s Designs - Order Status Dashboard\n'));

    const trackingService = new ShipmentTrackingService();
    const summary = trackingService.getStatusSummary();

    const table = new Table({
      head: [chalk.cyan('Status'), chalk.cyan('Count')],
      colWidths: [25, 15],
    });

    table.push(
      ['Pending', summary.pending],
      ['Awaiting Shipment', summary.paid],
      ['Label Created', summary.labelCreated],
      ['Shipped (In Transit)', summary.shipped],
      ['Delivered', summary.delivered],
      [chalk.bold('Total Orders'), chalk.bold(summary.total)],
    );

    console.log(table.toString());
    console.log();
  });

// List orders command
program
  .command('list')
  .description('List orders')
  .option('-p, --platform <platform>', 'Filter by platform (etsy, amazon)')
  .option('-s, --status <status>', 'Filter by status')
  .option('-l, --limit <number>', 'Limit results', '20')
  .action(async (options) => {
    console.log(chalk.bold.blue('\n📋 Orders List\n'));

    const orders = OrderModel.getAll({
      platform: options.platform,
      status: options.status,
      limit: parseInt(options.limit),
    });

    if (orders.length === 0) {
      console.log(chalk.yellow('No orders found.\n'));
      return;
    }

    const table = new Table({
      head: [
        chalk.cyan('Order #'),
        chalk.cyan('Platform'),
        chalk.cyan('Customer'),
        chalk.cyan('Total'),
        chalk.cyan('Status'),
        chalk.cyan('Date'),
      ],
      colWidths: [20, 10, 20, 12, 15, 12],
    });

    for (const order of orders) {
      const statusColor = getStatusColor(order.status);
      table.push([
        order.order_number,
        order.platform.toUpperCase(),
        truncate(order.customer_name, 18),
        `$${order.total?.toFixed(2) || '0.00'}`,
        statusColor(order.status),
        new Date(order.created_at).toLocaleDateString(),
      ]);
    }

    console.log(table.toString());
    console.log(chalk.gray(`\nShowing ${orders.length} orders\n`));
  });

// Order detail command
program
  .command('order <orderNumber>')
  .description('Show order details')
  .action(async (orderNumber) => {
    const orders = OrderModel.getAll({});
    const order = orders.find(o => o.order_number === orderNumber || o.platform_order_id === orderNumber);

    if (!order) {
      console.log(chalk.red(`\nOrder ${orderNumber} not found.\n`));
      return;
    }

    console.log(chalk.bold.blue(`\n📦 Order Details: ${order.order_number}\n`));

    const table = new Table();
    table.push(
      { 'Order Number': order.order_number },
      { 'Platform': order.platform.toUpperCase() },
      { 'Status': getStatusColor(order.status)(order.status) },
      { 'Customer': order.customer_name },
      { 'Email': order.customer_email || 'N/A' },
      { 'Total': `$${order.total?.toFixed(2)} ${order.currency}` },
      { 'Subtotal': `$${order.subtotal?.toFixed(2)}` },
      { 'Shipping': `$${order.shipping_cost?.toFixed(2)}` },
      { 'Tax': `$${order.tax?.toFixed(2)}` },
      { 'Platform Fees': `$${order.platform_fees?.toFixed(2)}` },
      { 'Net Revenue': `$${order.net_revenue?.toFixed(2)}` },
      { 'Order Date': new Date(order.created_at).toLocaleString() },
    );

    console.log(table.toString());

    // Show shipping address
    const address = order.shippingAddress || {};
    console.log(chalk.bold('\n📬 Shipping Address:'));
    console.log(`   ${address.name || 'N/A'}`);
    console.log(`   ${address.street1 || ''}`);
    if (address.street2) console.log(`   ${address.street2}`);
    console.log(`   ${address.city || ''}, ${address.state || ''} ${address.postalCode || ''}`);
    console.log(`   ${address.country || ''}`);

    // Show items
    const items = order.items || [];
    if (items.length > 0) {
      console.log(chalk.bold('\n🛒 Items:'));
      const itemsTable = new Table({
        head: [chalk.cyan('Product'), chalk.cyan('SKU'), chalk.cyan('Qty'), chalk.cyan('Price')],
      });
      for (const item of items) {
        itemsTable.push([
          truncate(item.title, 40),
          item.sku || 'N/A',
          item.quantity,
          `$${item.price?.toFixed(2)}`,
        ]);
      }
      console.log(itemsTable.toString());
    }

    // Show shipment info
    const shipment = ShipmentModel.getByOrderId(order.id);
    if (shipment) {
      console.log(chalk.bold('\n🚚 Shipment Information:'));
      const shipTable = new Table();
      shipTable.push(
        { 'Tracking #': shipment.tracking_number || 'N/A' },
        { 'Carrier': shipment.carrier || 'N/A' },
        { 'Status': getStatusColor(shipment.current_status)(shipment.current_status) },
        { 'Label Created': shipment.label_created_at ? new Date(shipment.label_created_at).toLocaleString() : 'N/A' },
        { 'Shipped': shipment.shipped_at ? new Date(shipment.shipped_at).toLocaleString() : 'N/A' },
        { 'Delivered': shipment.delivered_at ? new Date(shipment.delivered_at).toLocaleString() : 'N/A' },
      );
      console.log(shipTable.toString());
    }

    console.log();
  });

// Sync command
program
  .command('sync')
  .description('Sync orders from Etsy and Amazon')
  .option('--etsy', 'Sync only Etsy orders')
  .option('--amazon', 'Sync only Amazon orders')
  .option('--full', 'Full sync (last 90 days)')
  .action(async (options) => {
    console.log(chalk.bold.blue('\n🔄 Syncing Orders...\n'));

    const syncService = new OrderSyncService();
    await syncService.initialize();

    if (options.etsy) {
      console.log(chalk.cyan('Syncing Etsy orders...'));
      const result = await syncService.syncEtsyOrders({ fullSync: options.full });
      console.log(chalk.green(`✓ Etsy: ${result.synced} orders synced`));
      if (result.errors.length > 0) {
        console.log(chalk.red(`  ${result.errors.length} errors`));
      }
    } else if (options.amazon) {
      console.log(chalk.cyan('Syncing Amazon orders...'));
      const result = await syncService.syncAmazonOrders({ fullSync: options.full });
      console.log(chalk.green(`✓ Amazon: ${result.synced} orders synced`));
      if (result.errors.length > 0) {
        console.log(chalk.red(`  ${result.errors.length} errors`));
      }
    } else {
      const results = await syncService.syncAll();
      console.log(chalk.green(`✓ Etsy: ${results.etsy.synced} orders synced`));
      console.log(chalk.green(`✓ Amazon: ${results.amazon.synced} orders synced`));
    }

    console.log(chalk.green('\n✓ Sync complete!\n'));
  });

// Track command - update tracking for all shipments
program
  .command('track')
  .description('Update tracking status for all shipments')
  .action(async () => {
    console.log(chalk.bold.blue('\n📍 Updating Tracking Information...\n'));

    const trackingService = new ShipmentTrackingService();
    const result = await trackingService.updateAllTracking();

    console.log(chalk.green(`✓ Updated ${result.updated} shipments`));
    if (result.errors.length > 0) {
      console.log(chalk.red(`✗ ${result.errors.length} errors`));
    }
    console.log();
  });

// Record label created
program
  .command('label <orderId>')
  .description('Record that a shipping label was created')
  .requiredOption('-t, --tracking <tracking>', 'Tracking number')
  .requiredOption('-c, --carrier <carrier>', 'Carrier name (USPS, UPS, FedEx)')
  .option('--service <service>', 'Service type (e.g., Priority Mail)')
  .action(async (orderId, options) => {
    const trackingService = new ShipmentTrackingService();

    // Find order by ID or order number
    const orders = OrderModel.getAll({});
    const order = orders.find(o =>
      o.id === parseInt(orderId) ||
      o.order_number === orderId ||
      o.platform_order_id === orderId
    );

    if (!order) {
      console.log(chalk.red(`\nOrder ${orderId} not found.\n`));
      return;
    }

    await trackingService.recordLabelCreated(order.id, {
      trackingNumber: options.tracking,
      carrier: options.carrier,
      serviceType: options.service,
    });

    console.log(chalk.green(`\n✓ Label recorded for order ${order.order_number}`));
    console.log(chalk.gray(`  Tracking: ${options.tracking}`));
    console.log(chalk.gray(`  Carrier: ${options.carrier}\n`));
  });

// Mark as shipped
program
  .command('ship <orderId>')
  .description('Mark an order as shipped')
  .action(async (orderId) => {
    const trackingService = new ShipmentTrackingService();

    const orders = OrderModel.getAll({});
    const order = orders.find(o =>
      o.id === parseInt(orderId) ||
      o.order_number === orderId ||
      o.platform_order_id === orderId
    );

    if (!order) {
      console.log(chalk.red(`\nOrder ${orderId} not found.\n`));
      return;
    }

    const shipment = ShipmentModel.getByOrderId(order.id);
    if (!shipment) {
      console.log(chalk.red(`\nNo shipment record found. Create a label first.\n`));
      return;
    }

    await trackingService.recordShipped(shipment.id);

    console.log(chalk.green(`\n✓ Order ${order.order_number} marked as shipped\n`));
  });

// Mark as delivered
program
  .command('deliver <orderId>')
  .description('Mark an order as delivered')
  .action(async (orderId) => {
    const trackingService = new ShipmentTrackingService();

    const orders = OrderModel.getAll({});
    const order = orders.find(o =>
      o.id === parseInt(orderId) ||
      o.order_number === orderId ||
      o.platform_order_id === orderId
    );

    if (!order) {
      console.log(chalk.red(`\nOrder ${orderId} not found.\n`));
      return;
    }

    const shipment = ShipmentModel.getByOrderId(order.id);
    if (!shipment) {
      console.log(chalk.red(`\nNo shipment record found.\n`));
      return;
    }

    await trackingService.recordDelivered(shipment.id);

    console.log(chalk.green(`\n✓ Order ${order.order_number} marked as delivered\n`));
  });

// Revenue report
program
  .command('revenue')
  .description('Show revenue report')
  .option('--days <days>', 'Number of days to report', '30')
  .action(async (options) => {
    console.log(chalk.bold.blue(`\n💰 Revenue Report (Last ${options.days} days)\n`));

    const startDate = new Date();
    startDate.setDate(startDate.getDate() - parseInt(options.days));

    const orders = OrderModel.getAll({
      startDate: startDate.toISOString(),
    });

    const revenue = {
      total: 0,
      etsy: 0,
      amazon: 0,
      fees: 0,
      net: 0,
    };

    for (const order of orders) {
      revenue.total += order.total || 0;
      revenue.fees += order.platform_fees || 0;
      revenue.net += order.net_revenue || 0;

      if (order.platform === 'etsy') revenue.etsy += order.total || 0;
      if (order.platform === 'amazon') revenue.amazon += order.total || 0;
    }

    const table = new Table();
    table.push(
      { 'Total Revenue': chalk.green(`$${revenue.total.toFixed(2)}`) },
      { 'Etsy Revenue': `$${revenue.etsy.toFixed(2)}` },
      { 'Amazon Revenue': `$${revenue.amazon.toFixed(2)}` },
      { 'Platform Fees': chalk.red(`-$${revenue.fees.toFixed(2)}`) },
      { 'Net Revenue': chalk.bold.green(`$${revenue.net.toFixed(2)}`) },
      { 'Orders': orders.length },
      { 'Avg Order Value': `$${orders.length > 0 ? (revenue.total / orders.length).toFixed(2) : '0.00'}` },
    );

    console.log(table.toString());
    console.log();
  });

// Needs action report
program
  .command('action')
  .description('Show orders needing action')
  .action(async () => {
    console.log(chalk.bold.blue('\n⚠️  Orders Needing Action\n'));

    const syncService = new OrderSyncService();
    const actions = syncService.getOrdersNeedingAction();

    if (actions.paid.length > 0) {
      console.log(chalk.yellow(`\n📦 Need Shipping (${actions.paid.length}):`));
      const table = new Table({
        head: [chalk.cyan('Order #'), chalk.cyan('Platform'), chalk.cyan('Customer'), chalk.cyan('Date')],
      });
      for (const order of actions.paid.slice(0, 10)) {
        table.push([
          order.order_number,
          order.platform.toUpperCase(),
          truncate(order.customer_name, 20),
          new Date(order.created_at).toLocaleDateString(),
        ]);
      }
      console.log(table.toString());
    }

    if (actions.needsTracking.length > 0) {
      console.log(chalk.yellow(`\n📍 Need Tracking Update (${actions.needsTracking.length}):`));
      const table = new Table({
        head: [chalk.cyan('Order #'), chalk.cyan('Platform'), chalk.cyan('Status'), chalk.cyan('Days Old')],
      });
      for (const order of actions.needsTracking.slice(0, 10)) {
        const daysOld = Math.floor((Date.now() - new Date(order.created_at).getTime()) / (1000 * 60 * 60 * 24));
        table.push([
          order.order_number,
          order.platform.toUpperCase(),
          order.status,
          daysOld,
        ]);
      }
      console.log(table.toString());
    }

    if (actions.paid.length === 0 && actions.needsTracking.length === 0) {
      console.log(chalk.green('✓ No orders need immediate action!\n'));
    }

    console.log();
  });

// Helper functions
function getStatusColor(status) {
  const colors = {
    pending: chalk.gray,
    paid: chalk.yellow,
    label_created: chalk.blue,
    shipped: chalk.cyan,
    in_transit: chalk.cyan,
    out_for_delivery: chalk.magenta,
    delivered: chalk.green,
    cancelled: chalk.red,
  };
  return colors[status] || chalk.white;
}

function truncate(str, len) {
  if (!str) return '';
  return str.length > len ? str.substring(0, len - 3) + '...' : str;
}

// Parse and run
program.parse();
