#!/usr/bin/env node

/**
 * Order Sync Script for Shelzy's Designs
 * Run with: npm run sync
 *
 * Options:
 *   --etsy     Sync only Etsy orders
 *   --amazon   Sync only Amazon orders
 *   --full     Full sync (last 90 days instead of incremental)
 */

import { OrderSyncService } from '../src/services/order-sync.js';
import { initDatabase } from '../src/models/database.js';

// Parse arguments
const args = process.argv.slice(2);
const etsyOnly = args.includes('--etsy');
const amazonOnly = args.includes('--amazon');
const fullSync = args.includes('--full');

console.log('═'.repeat(50));
console.log('  Shelzy\'s Designs - Order Sync');
console.log('═'.repeat(50));
console.log();

// Initialize
initDatabase();
const syncService = new OrderSyncService();

async function main() {
  try {
    await syncService.initialize();

    const startTime = Date.now();

    if (etsyOnly) {
      console.log('Syncing Etsy orders...');
      const result = await syncService.syncEtsyOrders({ fullSync });
      console.log(`✓ Etsy: ${result.synced} orders synced`);
      if (result.errors.length > 0) {
        console.log(`  Errors: ${result.errors.length}`);
      }
    } else if (amazonOnly) {
      console.log('Syncing Amazon orders...');
      const result = await syncService.syncAmazonOrders({ fullSync });
      console.log(`✓ Amazon: ${result.synced} orders synced`);
      if (result.errors.length > 0) {
        console.log(`  Errors: ${result.errors.length}`);
      }
    } else {
      console.log('Syncing all platforms...\n');
      const results = await syncService.syncAll();

      console.log('\n--- Results ---');
      console.log(`Etsy: ${results.etsy.synced} orders synced`);
      if (results.etsy.errors.length > 0) {
        console.log(`  Errors: ${results.etsy.errors.length}`);
      }
      console.log(`Amazon: ${results.amazon.synced} orders synced`);
      if (results.amazon.errors.length > 0) {
        console.log(`  Errors: ${results.amazon.errors.length}`);
      }
    }

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log(`\n✓ Sync completed in ${elapsed}s`);

    // Show summary
    const summary = syncService.getOrdersSummary();
    console.log('\n--- Summary ---');
    console.log(`Total orders: ${summary.total}`);
    console.log(`Total revenue: $${summary.revenue.total.toFixed(2)}`);

    if (Object.keys(summary.byPlatform).length > 0) {
      console.log('\nBy Platform:');
      for (const [platform, count] of Object.entries(summary.byPlatform)) {
        const revenue = summary.revenue.byPlatform[platform] || 0;
        console.log(`  ${platform.toUpperCase()}: ${count} orders ($${revenue.toFixed(2)})`);
      }
    }

    if (Object.keys(summary.byStatus).length > 0) {
      console.log('\nBy Status:');
      for (const [status, count] of Object.entries(summary.byStatus)) {
        console.log(`  ${status}: ${count}`);
      }
    }

  } catch (error) {
    console.error('\n✗ Sync failed:', error.message);
    process.exit(1);
  }
}

main();
