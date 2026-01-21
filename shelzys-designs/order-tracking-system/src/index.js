#!/usr/bin/env node

import { CronJob } from 'cron';
import { OrderSyncService } from './services/order-sync.js';
import { ShipmentTrackingService } from './services/shipment-tracking.js';
import { NotificationService } from './services/notifications.js';
import { initDatabase } from './models/database.js';
import { config } from './config/index.js';

/**
 * Shelzy's Designs Order Tracking System
 * Main entry point - runs the sync and tracking services
 */

console.log(`
╔══════════════════════════════════════════════════════════════╗
║          Shelzy's Designs Order Tracking System              ║
║                                                              ║
║  Integrates: Etsy + Amazon Seller Central                    ║
║  Tracks: Label Created → Shipped → Delivered                 ║
╚══════════════════════════════════════════════════════════════╝
`);

// Initialize database
initDatabase();

// Initialize services
const syncService = new OrderSyncService();
const trackingService = new ShipmentTrackingService();
const notificationService = new NotificationService();

async function runSync() {
  console.log(`\n[${new Date().toISOString()}] Starting order sync...`);

  try {
    await syncService.initialize();
    const results = await syncService.syncAll();

    console.log(`[Sync] Etsy: ${results.etsy.synced} orders`);
    console.log(`[Sync] Amazon: ${results.amazon.synced} orders`);

    // Check for new orders that need notifications
    const summary = syncService.getOrdersSummary();
    console.log(`[Summary] Total orders: ${summary.total}, Revenue: $${summary.revenue.total.toFixed(2)}`);

  } catch (error) {
    console.error('[Sync] Error:', error.message);
  }
}

async function runTrackingUpdate() {
  console.log(`\n[${new Date().toISOString()}] Updating shipment tracking...`);

  try {
    const results = await trackingService.updateAllTracking();
    console.log(`[Tracking] Updated: ${results.updated}, Errors: ${results.errors.length}`);
  } catch (error) {
    console.error('[Tracking] Error:', error.message);
  }
}

async function sendDailySummary() {
  console.log(`\n[${new Date().toISOString()}] Sending daily summary...`);

  try {
    const statusSummary = trackingService.getStatusSummary();
    const ordersSummary = syncService.getOrdersSummary();

    await notificationService.sendDailySummary({
      ...statusSummary,
      revenue: ordersSummary.revenue,
      needsTracking: ordersSummary.byStatus?.label_created || 0,
    });

    console.log('[Summary] Daily summary sent');
  } catch (error) {
    console.error('[Summary] Error:', error.message);
  }
}

// Check if running in daemon mode
const args = process.argv.slice(2);
const isDaemon = args.includes('--daemon') || args.includes('-d');

if (isDaemon) {
  console.log('Starting in daemon mode...');
  console.log(`Order sync interval: ${config.app.syncIntervalMinutes} minutes`);
  console.log(`Tracking update interval: ${config.app.trackingCheckIntervalHours} hours`);

  // Run initial sync
  runSync().then(() => {
    runTrackingUpdate();
  });

  // Schedule order sync (every N minutes)
  const syncCron = `*/${config.app.syncIntervalMinutes} * * * *`;
  new CronJob(syncCron, runSync, null, true);

  // Schedule tracking updates (every N hours)
  const trackingCron = `0 */${config.app.trackingCheckIntervalHours} * * *`;
  new CronJob(trackingCron, runTrackingUpdate, null, true);

  // Schedule daily summary at 8 AM
  new CronJob('0 8 * * *', sendDailySummary, null, true);

  console.log('\nDaemon started. Press Ctrl+C to stop.\n');

  // Keep process running
  process.on('SIGINT', () => {
    console.log('\nShutting down...');
    process.exit(0);
  });

} else {
  // Run once and exit
  console.log('Running one-time sync...\n');

  (async () => {
    await runSync();
    await runTrackingUpdate();

    const summary = trackingService.getStatusSummary();
    console.log('\n--- Status Summary ---');
    console.log(`Pending: ${summary.pending}`);
    console.log(`Awaiting Shipment: ${summary.paid}`);
    console.log(`Label Created: ${summary.labelCreated}`);
    console.log(`Shipped: ${summary.shipped}`);
    console.log(`Delivered: ${summary.delivered}`);
    console.log(`Total: ${summary.total}`);
    console.log('\nDone!');
  })();
}
