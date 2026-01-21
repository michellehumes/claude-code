#!/usr/bin/env node

/**
 * Shipment Tracking Script for Shelzy's Designs
 * Run with: npm run track
 *
 * Updates tracking information for all active shipments
 */

import { ShipmentTrackingService } from '../src/services/shipment-tracking.js';
import { NotificationService } from '../src/services/notifications.js';
import { ShipmentModel, OrderModel, initDatabase } from '../src/models/database.js';

console.log('═'.repeat(50));
console.log('  Shelzy\'s Designs - Shipment Tracking Update');
console.log('═'.repeat(50));
console.log();

// Initialize
initDatabase();
const trackingService = new ShipmentTrackingService();
const notificationService = new NotificationService();

async function main() {
  try {
    const startTime = Date.now();

    // Get shipments needing update
    const shipments = ShipmentModel.getNeedingUpdate();
    console.log(`Found ${shipments.length} shipments to update\n`);

    if (shipments.length === 0) {
      console.log('No shipments need tracking updates.');
      showStatusSummary();
      return;
    }

    let updated = 0;
    let delivered = 0;
    let errors = 0;

    for (const shipment of shipments) {
      try {
        console.log(`Checking: ${shipment.tracking_number} (${shipment.carrier || 'Unknown'})...`);

        const previousStatus = shipment.current_status;
        const result = await trackingService.updateTrackingStatus(shipment);

        if (result) {
          updated++;

          // Check if status changed to delivered
          if (result.currentStatus === 'delivered' && previousStatus !== 'delivered') {
            delivered++;
            console.log(`  ✓ DELIVERED!`);

            // Send delivery notification
            const order = OrderModel.getById(shipment.order_id);
            if (order) {
              await notificationService.notifyDelivered(order, result);
            }
          } else {
            console.log(`  → ${result.currentStatus || 'updated'}`);
          }
        }

        // Small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 500));

      } catch (error) {
        console.log(`  ✗ Error: ${error.message}`);
        errors++;
      }
    }

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);

    console.log('\n--- Results ---');
    console.log(`Updated: ${updated}`);
    console.log(`Delivered: ${delivered}`);
    console.log(`Errors: ${errors}`);
    console.log(`Time: ${elapsed}s`);

    showStatusSummary();

  } catch (error) {
    console.error('\n✗ Tracking update failed:', error.message);
    process.exit(1);
  }
}

function showStatusSummary() {
  const summary = trackingService.getStatusSummary();

  console.log('\n--- Current Status Summary ---');
  console.log(`Pending: ${summary.pending}`);
  console.log(`Awaiting Shipment: ${summary.paid}`);
  console.log(`Label Created: ${summary.labelCreated}`);
  console.log(`Shipped/In Transit: ${summary.shipped}`);
  console.log(`Delivered: ${summary.delivered}`);
  console.log(`Total: ${summary.total}`);
}

main();
