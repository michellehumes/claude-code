#!/usr/bin/env node

/**
 * Database Setup Script for Shelzy's Designs Order Tracking
 * Run with: npm run setup
 *
 * Creates the SQLite database and all required tables
 */

import { initDatabase, getDatabase } from '../src/models/database.js';
import { config } from '../src/config/index.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('═'.repeat(50));
console.log('  Shelzy\'s Designs - Database Setup');
console.log('═'.repeat(50));
console.log();

// Check for .env file
const envPath = path.join(__dirname, '../.env');
const envExamplePath = path.join(__dirname, '../.env.example');

if (!fs.existsSync(envPath)) {
  console.log('⚠ No .env file found.');
  console.log('  Creating from .env.example...');

  if (fs.existsSync(envExamplePath)) {
    fs.copyFileSync(envExamplePath, envPath);
    console.log('  ✓ .env file created');
    console.log('  → Please edit .env with your API credentials\n');
  } else {
    console.log('  ✗ .env.example not found');
    console.log('  → Please create .env file manually\n');
  }
}

// Initialize database
console.log('Setting up database...');
console.log(`  Location: ${config.app.databasePath}\n`);

try {
  initDatabase();
  const db = getDatabase();

  // Verify tables exist
  const tables = db.prepare(`
    SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name
  `).all();

  console.log('✓ Database initialized successfully!\n');
  console.log('Tables created:');
  for (const table of tables) {
    if (!table.name.startsWith('sqlite_')) {
      const count = db.prepare(`SELECT COUNT(*) as count FROM ${table.name}`).get();
      console.log(`  • ${table.name} (${count.count} rows)`);
    }
  }

  console.log('\n--- Configuration Status ---');

  // Check Etsy configuration
  console.log('\nEtsy:');
  if (config.etsy.apiKey && config.etsy.shopId) {
    console.log('  ✓ API Key configured');
    console.log('  ✓ Shop ID configured');
    if (config.etsy.accessToken) {
      console.log('  ✓ Access token configured');
    } else {
      console.log('  ⚠ Access token not configured');
    }
  } else {
    console.log('  ⚠ Not configured - add ETSY_* variables to .env');
  }

  // Check Amazon configuration
  console.log('\nAmazon Seller:');
  if (config.amazon.sellerId && config.amazon.clientId) {
    console.log('  ✓ Seller ID configured');
    console.log('  ✓ Client ID configured');
    if (config.amazon.refreshToken) {
      console.log('  ✓ Refresh token configured');
    } else {
      console.log('  ⚠ Refresh token not configured');
    }
  } else {
    console.log('  ⚠ Not configured - add AMAZON_* variables to .env');
  }

  // Check carrier configuration
  console.log('\nCarrier Tracking:');
  if (config.carriers?.usps?.userId) {
    console.log('  ✓ USPS configured');
  } else {
    console.log('  ○ USPS not configured (optional)');
  }
  if (config.carriers?.ups?.accessKey) {
    console.log('  ✓ UPS configured');
  } else {
    console.log('  ○ UPS not configured (optional)');
  }
  if (config.carriers?.fedex?.apiKey) {
    console.log('  ✓ FedEx configured');
  } else {
    console.log('  ○ FedEx not configured (optional)');
  }

  // Check email configuration
  console.log('\nEmail Notifications:');
  if (config.email.user && config.email.password) {
    console.log('  ✓ Email configured');
    console.log(`    Notifications will be sent to: ${config.email.notificationEmail || config.email.user}`);
  } else {
    console.log('  ○ Not configured (optional)');
  }

  console.log('\n═'.repeat(50));
  console.log('  Setup Complete!');
  console.log('═'.repeat(50));
  console.log('\nNext steps:');
  console.log('  1. Edit .env with your API credentials');
  console.log('  2. Run: npm run sync    - to sync orders');
  console.log('  3. Run: npm run dashboard status  - to view status');
  console.log('  4. Run: npm start       - to run the daemon');
  console.log();

} catch (error) {
  console.error('✗ Database setup failed:', error.message);
  process.exit(1);
}
