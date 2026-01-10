/**
 * Monarch Credit Card Perks Tracking System
 * Google Apps Script - Complete Implementation
 *
 * This system ingests Monarch CSV exports, builds a credit card perks catalog,
 * matches transactions to perks, and tracks pacing/unused perks.
 *
 * Author: Claude Code
 * Version: 1.0.0
 */

// ============================================================================
// CONFIGURATION & CONSTANTS
// ============================================================================

const CONFIG = {
  // Sheet tab names
  TABS: {
    CARDS: 'Cards',
    PERKS_CATALOG: 'Perks Catalog',
    MERCHANT_ALIASES: 'Merchant_Aliases',
    CATEGORY_MAP: 'Monarch Categories Map',
    TRANSACTIONS: 'Transactions_2026',
    PERK_USAGE: 'Perk Usage 2026',
    DASHBOARD: 'Dashboard',
    CONFIG: 'Config',
    LOG: 'Log'
  },

  // Matching thresholds
  MATCH_THRESHOLD: 60,
  TOLERANCE_PERCENT: 0.10,
  TOLERANCE_MIN_DOLLARS: 10,

  // Property keys
  PROPS: {
    DRIVE_FOLDER_ID: 'DRIVE_FOLDER_ID',
    DRY_RUN: 'DRY_RUN',
    LAST_INGEST_DATE: 'LAST_INGEST_DATE'
  },

  // Current year for tracking
  TRACKING_YEAR: 2026
};

// Neutral/Ignore merchants - these get -30 penalty unless explicitly matched
const NEUTRAL_MERCHANTS = [
  'amazon', 'paypal', 'coinbase', 'robinhood', 'kaplan', 'nuuly',
  'zelle', 'venmo', 'bmw', 'chase', 'costco', 'citarella'
];

// Credit card inclusion keywords (case-insensitive)
const CARD_INCLUDE_KEYWORDS = [
  'card', 'visa', 'mastercard', 'amex', 'platinum', 'gold', 'reserve',
  'freedom', 'venture', 'bonvoy', 'hilton', 'delta', 'prime', 'target',
  'nordstrom', 'sapphire', 'preferred', 'explorer', 'world of hyatt',
  'marriott', 'ink', 'unlimited', 'flex', 'quicksilver', 'savor'
];

// Account exclusion keywords
const CARD_EXCLUDE_KEYWORDS = [
  'checking', 'savings', 'brokerage', 'robinhood', 'coinbase', 'ira',
  '401', 'mortgage', 'loan', 'investment', 'money market', 'cd ',
  'certificate', 'hsa', 'fsa'
];

// Issuer inference patterns
const ISSUER_PATTERNS = [
  { pattern: /chase/i, issuer: 'Chase' },
  { pattern: /amex|american express/i, issuer: 'Amex' },
  { pattern: /capital one|capitalone/i, issuer: 'Capital One' },
  { pattern: /wells fargo/i, issuer: 'Wells Fargo' },
  { pattern: /usaa/i, issuer: 'USAA' },
  { pattern: /target/i, issuer: 'Target' },
  { pattern: /nordstrom/i, issuer: 'Nordstrom' },
  { pattern: /citi/i, issuer: 'Citi' },
  { pattern: /discover/i, issuer: 'Discover' },
  { pattern: /bank of america|bofa/i, issuer: 'Bank of America' },
  { pattern: /barclays/i, issuer: 'Barclays' },
  { pattern: /synchrony/i, issuer: 'Synchrony' },
  { pattern: /u\.?s\.? bank/i, issuer: 'US Bank' }
];

// ============================================================================
// MAIN ENTRY POINTS
// ============================================================================

/**
 * Creates the menu when the spreadsheet opens
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎯 Perks Tracker')
    .addItem('⚡ Quick Setup (Cards + Perks)', 'quickSetupWithMyData')
    .addItem('📋 Setup Sheet Only', 'setupSheet_IfNeeded')
    .addSeparator()
    .addSubMenu(ui.createMenu('📥 Import Data')
      .addItem('Ingest Transactions CSV (from Config tab)', 'ingestTransactionsFromConfigTab')
      .addItem('Ingest Balances CSV (from Config tab)', 'ingestBalancesFromConfigTab')
      .addItem('Ingest Transactions CSV (from Drive)', 'ingestTransactionsCSV')
      .addItem('Ingest Balances CSV (from Drive)', 'ingestBalancesCSV'))
    .addSubMenu(ui.createMenu('🃏 Seed Data')
      .addItem('Add My Cards (11 cards)', 'seedMyCards')
      .addItem('Add My Perks (25 perks)', 'seedMyPerks')
      .addItem('Add Generic Sample Perks', 'seedSamplePerks'))
    .addSeparator()
    .addItem('🔄 Normalize Cards', 'normalizeCards')
    .addItem('🔗 Match Perks to Transactions', 'matchPerks')
    .addItem('📊 Calculate Usage & Pacing', 'calculateUsage')
    .addItem('📈 Update Dashboard', 'updateDashboard')
    .addSeparator()
    .addItem('▶️ Run Full Pipeline', 'runFullPipeline')
    .addItem('⏰ Install Nightly Trigger', 'installNightlyTrigger')
    .addItem('🗑️ Remove All Triggers', 'removeAllTriggers')
    .addSeparator()
    .addSubMenu(ui.createMenu('⚙️ Settings')
      .addItem('Set Drive Folder ID', 'promptForFolderId')
      .addItem('Toggle DRY_RUN Mode', 'toggleDryRun')
      .addItem('View Current Settings', 'viewSettings'))
    .addToUi();
}

/**
 * Runs the full pipeline: normalize, match, calculate, dashboard
 */
function runFullPipeline() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  logMessage('INFO', '========== STARTING FULL PIPELINE ==========');

  try {
    normalizeCards();
    matchPerks();
    calculateUsage();
    updateDashboard();
    logMessage('INFO', '========== PIPELINE COMPLETE ==========');
    SpreadsheetApp.getUi().alert('✅ Full pipeline completed successfully!');
  } catch (e) {
    logMessage('ERROR', 'Pipeline failed: ' + e.message);
    SpreadsheetApp.getUi().alert('❌ Pipeline failed: ' + e.message);
  }
}

// ============================================================================
// SETUP FUNCTIONS
// ============================================================================

/**
 * Creates all required tabs with headers, formatting, and seed data
 * Idempotent: only creates tabs/headers if they don't exist
 */
function setupSheet_IfNeeded() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  logMessage('INFO', 'Starting sheet setup...');

  // Create Cards tab
  createTabIfNeeded(ss, CONFIG.TABS.CARDS, [
    'Card ID', 'Issuer', 'Card Name', 'Last4', 'Open/Closed',
    'Annual Fee', 'Benefit Year Start Month', 'Notes'
  ]);

  // Create Perks Catalog tab
  createTabIfNeeded(ss, CONFIG.TABS.PERKS_CATALOG, [
    'Perk ID', 'Card ID', 'Card Name', 'Perk Name', 'Category',
    'Annual Value', 'Frequency', 'Reset Rule', 'Merchant Keywords',
    'Monarch Category Match', 'Amount Pattern', 'Notes'
  ]);

  // Create Merchant_Aliases tab and seed data
  const aliasesCreated = createTabIfNeeded(ss, CONFIG.TABS.MERCHANT_ALIASES, [
    'Match Type', 'Match Pattern', 'Canonical Merchant', 'Notes'
  ]);
  if (aliasesCreated) {
    seedMerchantAliases(ss);
  }

  // Create Monarch Categories Map tab
  const catMapCreated = createTabIfNeeded(ss, CONFIG.TABS.CATEGORY_MAP, [
    'Monarch Category', 'Perk Category', 'Priority'
  ]);
  if (catMapCreated) {
    seedCategoryMap(ss);
  }

  // Create Transactions_2026 tab
  createTabIfNeeded(ss, CONFIG.TABS.TRANSACTIONS, [
    'Date', 'Merchant (raw)', 'Merchant Normalized', 'Amount', 'Category',
    'Account (raw)', 'Card ID', 'Transaction ID', 'Dedupe Key',
    'Matched Perk ID', 'Match Confidence', 'Match Reason', 'Notes / Override Perk ID'
  ]);

  // Create Perk Usage 2026 tab
  createTabIfNeeded(ss, CONFIG.TABS.PERK_USAGE, [
    'Perk ID', 'Card', 'Perk', 'Max Value', 'Used YTD', 'Remaining',
    '% Used', 'Expected Pace %', 'Pace Delta', 'Status', 'Last Used Date'
  ]);

  // Create Dashboard tab
  createTabIfNeeded(ss, CONFIG.TABS.DASHBOARD, []);
  setupDashboardStructure(ss);

  // Create Config tab for CSV paste
  const configCreated = createTabIfNeeded(ss, CONFIG.TABS.CONFIG, [
    'Setting', 'Value'
  ]);
  if (configCreated) {
    setupConfigTab(ss);
  }

  // Create Log tab
  createTabIfNeeded(ss, CONFIG.TABS.LOG, [
    'Timestamp', 'Level', 'Message'
  ]);

  // Apply formatting to all tabs
  applyFormatting(ss);

  // Set up data validation
  setupDataValidation(ss);

  logMessage('INFO', 'Sheet setup complete!');
  SpreadsheetApp.getUi().alert('✅ Sheet setup complete! All tabs created with headers and seed data.');
}

/**
 * Creates a tab if it doesn't exist, returns true if created
 */
function createTabIfNeeded(ss, tabName, headers) {
  let sheet = ss.getSheetByName(tabName);
  if (!sheet) {
    sheet = ss.insertSheet(tabName);
    if (headers.length > 0) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.getRange(1, 1, 1, headers.length)
        .setFontWeight('bold')
        .setBackground('#4285f4')
        .setFontColor('white');
      sheet.setFrozenRows(1);
    }
    logMessage('INFO', `Created tab: ${tabName}`);
    return true;
  }
  return false;
}

/**
 * Seeds the Merchant_Aliases tab with initial data
 */
function seedMerchantAliases(ss) {
  const sheet = ss.getSheetByName(CONFIG.TABS.MERCHANT_ALIASES);
  const seedData = [
    // Specific patterns first (higher priority by order)
    ['contains', 'uber eats', 'Uber Eats', 'Food delivery'],
    ['contains', 'uber', 'Uber', 'Rideshare'],
    ['contains', 'walmart+', 'Walmart+', 'Subscription'],
    ['contains', 'walmart plus', 'Walmart+', 'Subscription'],
    ['contains', 'breeze', 'Breeze Airways', 'Airline'],
    ['contains', 'american airlines', 'American Airlines', 'Airline'],
    ['contains', 'airport parking', 'Airport Parking', 'Travel'],
    ['contains', 'lyft', 'Lyft', 'Rideshare'],
    ['contains', 'lord camden inn', 'Lord Camden Inn', 'Hotel'],
    ['contains', 'woodstock inn', 'Woodstock Inn & Resort', 'Hotel'],
    // Common perk partners
    ['contains', 'doordash', 'DoorDash', 'Food delivery'],
    ['contains', 'stubhub', 'StubHub', 'Entertainment'],
    ['contains', 'viagogo', 'Viagogo', 'Entertainment'],
    ['contains', 'peloton', 'Peloton', 'Fitness'],
    ['contains', 'saks', 'Saks Fifth Avenue', 'Retail'],
    ['contains', 'grubhub', 'Grubhub', 'Food delivery'],
    ['contains', 'seamless', 'Seamless', 'Food delivery'],
    ['contains', 'dunkin', "Dunkin'", 'Food & Drink'],
    ['contains', 'resy', 'Resy', 'Dining'],
    // Airlines
    ['contains', 'delta', 'Delta Air Lines', 'Airline'],
    ['contains', 'united', 'United Airlines', 'Airline'],
    ['contains', 'southwest', 'Southwest Airlines', 'Airline'],
    ['contains', 'jetblue', 'JetBlue', 'Airline'],
    // Hotels
    ['contains', 'marriott', 'Marriott', 'Hotel'],
    ['contains', 'hilton', 'Hilton', 'Hotel'],
    ['contains', 'hyatt', 'Hyatt', 'Hotel'],
    // Streaming
    ['contains', 'netflix', 'Netflix', 'Streaming'],
    ['contains', 'spotify', 'Spotify', 'Streaming'],
    ['contains', 'disney+', 'Disney+', 'Streaming'],
    ['contains', 'hulu', 'Hulu', 'Streaming'],
    ['contains', 'hbo max', 'HBO Max', 'Streaming'],
    ['contains', 'max.com', 'HBO Max', 'Streaming'],
    ['contains', 'peacock', 'Peacock', 'Streaming'],
    ['contains', 'paramount+', 'Paramount+', 'Streaming'],
    ['contains', 'nyt', 'NY Times', 'Subscription'],
    ['contains', 'new york times', 'NY Times', 'Subscription'],
    ['contains', 'audible', 'Audible', 'Subscription'],
    // TSA/Travel
    ['contains', 'global entry', 'Global Entry', 'Travel Credit'],
    ['contains', 'tsa precheck', 'TSA PreCheck', 'Travel Credit'],
    ['contains', 'clear', 'CLEAR', 'Travel Credit'],
    ['contains', 'priority pass', 'Priority Pass', 'Lounge'],
    // Other common
    ['contains', 'starbucks', 'Starbucks', 'Coffee'],
    ['contains', 'whole foods', 'Whole Foods', 'Grocery'],
    ['contains', 'instacart', 'Instacart', 'Grocery delivery'],
    ['contains', 'gopuff', 'Gopuff', 'Delivery'],
    ['contains', 'equinox', 'Equinox', 'Fitness'],
    ['contains', 'soulcycle', 'SoulCycle', 'Fitness']
  ];

  if (seedData.length > 0) {
    sheet.getRange(2, 1, seedData.length, 4).setValues(seedData);
    logMessage('INFO', `Seeded ${seedData.length} merchant aliases`);
  }
}

/**
 * Seeds the Category Map tab
 */
function seedCategoryMap(ss) {
  const sheet = ss.getSheetByName(CONFIG.TABS.CATEGORY_MAP);
  const seedData = [
    ['Travel', 'Travel', 1],
    ['Flights', 'Travel', 1],
    ['Hotels & Lodging', 'Travel', 1],
    ['Car Rental', 'Travel', 2],
    ['Rideshare', 'Travel', 2],
    ['Public Transit', 'Travel', 3],
    ['Restaurants', 'Dining', 1],
    ['Fast Food', 'Dining', 2],
    ['Coffee Shops', 'Dining', 2],
    ['Food & Drink', 'Dining', 2],
    ['Groceries', 'Grocery', 1],
    ['Entertainment', 'Entertainment', 1],
    ['Movies & DVDs', 'Entertainment', 2],
    ['Music', 'Entertainment', 2],
    ['Shopping', 'Retail', 1],
    ['Clothing', 'Retail', 2],
    ['Electronics', 'Retail', 2],
    ['Subscriptions', 'Subscriptions', 1],
    ['Streaming Services', 'Subscriptions', 1],
    ['Internet', 'Subscriptions', 2],
    ['Phone', 'Subscriptions', 2],
    ['Gas & Fuel', 'Gas', 1],
    ['Auto & Transport', 'Auto', 1],
    ['Gym', 'Fitness', 1],
    ['Sports', 'Fitness', 2],
    ['Fees & Charges', 'Fees', 1],
    ['Finance Charge', 'Fees', 1]
  ];

  if (seedData.length > 0) {
    sheet.getRange(2, 1, seedData.length, 3).setValues(seedData);
    logMessage('INFO', `Seeded ${seedData.length} category mappings`);
  }
}

/**
 * Sets up the Config tab for CSV paste method
 */
function setupConfigTab(ss) {
  const sheet = ss.getSheetByName(CONFIG.TABS.CONFIG);

  // Add configuration instructions
  const configData = [
    ['Setting', 'Value'],
    ['---', '--- INSTRUCTIONS ---'],
    ['To ingest CSVs:', 'Paste CSV content below the designated headers'],
    ['', ''],
    ['---', '--- BALANCES CSV ---'],
    ['Paste Balances CSV below this row:', ''],
    ['', ''],
    ['', ''],
    ['', ''],
    ['---', '--- TRANSACTIONS CSV ---'],
    ['Paste Transactions CSV below this row:', ''],
  ];

  sheet.getRange(1, 1, configData.length, 2).setValues(configData);
  sheet.getRange(1, 1, 1, 2).setFontWeight('bold').setBackground('#4285f4').setFontColor('white');
  sheet.getRange('A2:B5').setBackground('#f3f3f3');
  sheet.getRange('A6:B6').setBackground('#e8f5e9').setFontWeight('bold');
  sheet.getRange('A11:B11').setBackground('#e3f2fd').setFontWeight('bold');
  sheet.setColumnWidth(1, 250);
  sheet.setColumnWidth(2, 500);
}

/**
 * Sets up the Dashboard structure
 */
function setupDashboardStructure(ss) {
  const sheet = ss.getSheetByName(CONFIG.TABS.DASHBOARD);

  // Clear and set up structure
  sheet.clear();

  // Title
  sheet.getRange('A1').setValue('🎯 Credit Card Perks Dashboard - 2026');
  sheet.getRange('A1').setFontSize(18).setFontWeight('bold');

  // Summary metrics section
  sheet.getRange('A3').setValue('📊 Summary Metrics');
  sheet.getRange('A3').setFontSize(14).setFontWeight('bold').setBackground('#e8f5e9');

  const summaryLabels = [
    ['Total Annual Perk Value:', '$0.00'],
    ['Value Used YTD:', '$0.00'],
    ['Value Remaining:', '$0.00'],
    ['# Perks Behind:', '0'],
    ['# Perks Unused:', '0'],
    ['Last Updated:', '']
  ];
  sheet.getRange('A4:B9').setValues(summaryLabels);
  sheet.getRange('A4:A9').setFontWeight('bold');

  // Behind perks section
  sheet.getRange('A11').setValue('⚠️ Perks I\'m Behind On');
  sheet.getRange('A11').setFontSize(14).setFontWeight('bold').setBackground('#ffebee');

  sheet.getRange('A12:G12').setValues([['Perk', 'Card', 'Max Value', 'Used YTD', 'Expected', 'Pace Delta', 'Status']]);
  sheet.getRange('A12:G12').setFontWeight('bold').setBackground('#ffcdd2');

  // Unused perks section
  sheet.getRange('A25').setValue('💰 Biggest Unused Perks');
  sheet.getRange('A25').setFontSize(14).setFontWeight('bold').setBackground('#fff3e0');

  sheet.getRange('A26:E26').setValues([['Perk', 'Card', 'Max Value', 'Remaining', 'Frequency']]);
  sheet.getRange('A26:E26').setFontWeight('bold').setBackground('#ffe0b2');

  // Set column widths
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 180);
  sheet.setColumnWidth(3, 100);
  sheet.setColumnWidth(4, 100);
  sheet.setColumnWidth(5, 100);
  sheet.setColumnWidth(6, 100);
  sheet.setColumnWidth(7, 100);
}

/**
 * Applies consistent formatting across all tabs
 */
function applyFormatting(ss) {
  const tabsWithCurrency = [
    { name: CONFIG.TABS.CARDS, cols: [6] }, // Annual Fee
    { name: CONFIG.TABS.PERKS_CATALOG, cols: [6] }, // Annual Value
    { name: CONFIG.TABS.TRANSACTIONS, cols: [4] }, // Amount
    { name: CONFIG.TABS.PERK_USAGE, cols: [4, 5, 6] } // Max Value, Used YTD, Remaining
  ];

  tabsWithCurrency.forEach(tab => {
    const sheet = ss.getSheetByName(tab.name);
    if (sheet) {
      tab.cols.forEach(col => {
        const range = sheet.getRange(2, col, sheet.getMaxRows() - 1, 1);
        range.setNumberFormat('$#,##0.00');
      });
    }
  });

  // Date formatting
  const tabsWithDates = [
    { name: CONFIG.TABS.TRANSACTIONS, cols: [1] },
    { name: CONFIG.TABS.PERK_USAGE, cols: [11] }
  ];

  tabsWithDates.forEach(tab => {
    const sheet = ss.getSheetByName(tab.name);
    if (sheet) {
      tab.cols.forEach(col => {
        const range = sheet.getRange(2, col, sheet.getMaxRows() - 1, 1);
        range.setNumberFormat('yyyy-mm-dd');
      });
    }
  });

  // Percentage formatting
  const sheet = ss.getSheetByName(CONFIG.TABS.PERK_USAGE);
  if (sheet) {
    sheet.getRange(2, 7, sheet.getMaxRows() - 1, 1).setNumberFormat('0%'); // % Used
    sheet.getRange(2, 8, sheet.getMaxRows() - 1, 1).setNumberFormat('0%'); // Expected Pace %
    sheet.getRange(2, 9, sheet.getMaxRows() - 1, 1).setNumberFormat('+0%;-0%;0%'); // Pace Delta
  }
}

/**
 * Sets up data validation dropdowns
 */
function setupDataValidation(ss) {
  // Cards - Open/Closed validation
  const cardsSheet = ss.getSheetByName(CONFIG.TABS.CARDS);
  if (cardsSheet) {
    const openClosedRule = SpreadsheetApp.newDataValidation()
      .requireValueInList(['Open', 'Closed'], true)
      .setAllowInvalid(false)
      .build();
    cardsSheet.getRange(2, 5, 500, 1).setDataValidation(openClosedRule);

    // Benefit Year Start Month
    const monthRule = SpreadsheetApp.newDataValidation()
      .requireValueInList(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], true)
      .setAllowInvalid(true)
      .build();
    cardsSheet.getRange(2, 7, 500, 1).setDataValidation(monthRule);
  }

  // Perks Catalog validations
  const perksSheet = ss.getSheetByName(CONFIG.TABS.PERKS_CATALOG);
  if (perksSheet) {
    const categoryRule = SpreadsheetApp.newDataValidation()
      .requireValueInList(['Travel', 'Dining', 'Retail', 'Subscriptions', 'Fees', 'Entertainment', 'Grocery', 'Gas', 'Fitness', 'Other'], true)
      .setAllowInvalid(true)
      .build();
    perksSheet.getRange(2, 5, 500, 1).setDataValidation(categoryRule);

    const frequencyRule = SpreadsheetApp.newDataValidation()
      .requireValueInList(['monthly', 'quarterly', 'annual', 'every_4_years', 'one_time'], true)
      .setAllowInvalid(false)
      .build();
    perksSheet.getRange(2, 7, 500, 1).setDataValidation(frequencyRule);

    const resetRule = SpreadsheetApp.newDataValidation()
      .requireValueInList(['calendar', 'anniversary'], true)
      .setAllowInvalid(false)
      .build();
    perksSheet.getRange(2, 8, 500, 1).setDataValidation(resetRule);
  }

  // Merchant Aliases - Match Type
  const aliasSheet = ss.getSheetByName(CONFIG.TABS.MERCHANT_ALIASES);
  if (aliasSheet) {
    const matchTypeRule = SpreadsheetApp.newDataValidation()
      .requireValueInList(['contains', 'equals', 'regex'], true)
      .setAllowInvalid(false)
      .build();
    aliasSheet.getRange(2, 1, 500, 1).setDataValidation(matchTypeRule);
  }
}

// ============================================================================
// CSV INGESTION FUNCTIONS
// ============================================================================

/**
 * Ingests Balances CSV from Google Drive
 */
function ingestBalancesCSV() {
  const folderId = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRIVE_FOLDER_ID);

  if (!folderId) {
    SpreadsheetApp.getUi().alert('❌ Drive folder ID not set. Use Settings > Set Drive Folder ID');
    return;
  }

  try {
    const folder = DriveApp.getFolderById(folderId);
    const files = folder.getFilesByName('Balances'); // Will find files starting with "Balances"

    let balancesFile = null;
    let latestDate = new Date(0);

    // Find the most recent Balances file
    while (files.hasNext()) {
      const file = files.next();
      if (file.getName().includes('Balances') && file.getMimeType() === 'text/csv') {
        if (file.getLastUpdated() > latestDate) {
          balancesFile = file;
          latestDate = file.getLastUpdated();
        }
      }
    }

    // Also search with pattern
    const allFiles = folder.getFiles();
    while (allFiles.hasNext()) {
      const file = allFiles.next();
      const name = file.getName().toLowerCase();
      if (name.startsWith('balances') && (name.endsWith('.csv') || file.getMimeType() === 'text/csv')) {
        if (file.getLastUpdated() > latestDate) {
          balancesFile = file;
          latestDate = file.getLastUpdated();
        }
      }
    }

    if (!balancesFile) {
      SpreadsheetApp.getUi().alert('❌ No Balances CSV found in the specified folder.');
      return;
    }

    const csvContent = balancesFile.getBlob().getDataAsString();
    processBalancesCSV(csvContent);
    logMessage('INFO', `Ingested Balances CSV from Drive: ${balancesFile.getName()}`);

  } catch (e) {
    logMessage('ERROR', `Failed to ingest Balances from Drive: ${e.message}`);
    SpreadsheetApp.getUi().alert('❌ Error: ' + e.message);
  }
}

/**
 * Ingests Balances CSV from Config tab (paste method)
 */
function ingestBalancesFromConfigTab() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const configSheet = ss.getSheetByName(CONFIG.TABS.CONFIG);

  if (!configSheet) {
    SpreadsheetApp.getUi().alert('❌ Config tab not found. Run Setup first.');
    return;
  }

  // Find the Balances CSV section (row 6 onwards, looking for data)
  const data = configSheet.getDataRange().getValues();
  let csvStartRow = -1;
  let csvEndRow = -1;

  for (let i = 0; i < data.length; i++) {
    if (data[i][0] && data[i][0].toString().includes('Paste Balances CSV')) {
      csvStartRow = i + 1;
    }
    if (csvStartRow > 0 && data[i][0] && data[i][0].toString().includes('TRANSACTIONS CSV')) {
      csvEndRow = i - 1;
      break;
    }
  }

  if (csvStartRow < 0) {
    SpreadsheetApp.getUi().alert('❌ Could not find Balances CSV section in Config tab.');
    return;
  }

  if (csvEndRow < 0) csvEndRow = data.length - 1;

  // Extract CSV lines
  const csvLines = [];
  for (let i = csvStartRow; i <= csvEndRow; i++) {
    const row = data[i];
    // Join non-empty cells or use first cell as CSV line
    const line = row.filter(cell => cell !== '').join(',');
    if (line.trim()) {
      csvLines.push(line);
    }
  }

  if (csvLines.length === 0) {
    SpreadsheetApp.getUi().alert('❌ No CSV data found. Paste your Balances CSV content in the Config tab.');
    return;
  }

  const csvContent = csvLines.join('\n');
  processBalancesCSV(csvContent);
  logMessage('INFO', 'Ingested Balances CSV from Config tab');
}

/**
 * Processes Balances CSV content and populates Cards tab
 */
function processBalancesCSV(csvContent) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const isDryRun = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRY_RUN) === 'true';

  logMessage('INFO', `Processing Balances CSV (DRY_RUN: ${isDryRun})`);

  const lines = csvContent.split(/\r?\n/).filter(line => line.trim());
  if (lines.length < 2) {
    logMessage('WARN', 'Balances CSV has no data rows');
    return;
  }

  // Parse header
  const header = parseCSVLine(lines[0]);
  const colIndex = {};
  header.forEach((col, i) => {
    colIndex[col.toLowerCase().trim()] = i;
  });

  // Find the Account column (required)
  const accountColIdx = colIndex['account'] ?? colIndex['account name'] ?? colIndex['name'];
  if (accountColIdx === undefined) {
    logMessage('ERROR', 'Could not find Account column in Balances CSV');
    SpreadsheetApp.getUi().alert('❌ Could not find Account column. Expected: "Account" or "Account Name"');
    return;
  }

  // Extract unique accounts
  const accounts = new Set();
  for (let i = 1; i < lines.length; i++) {
    const row = parseCSVLine(lines[i]);
    if (row[accountColIdx]) {
      accounts.add(row[accountColIdx].trim());
    }
  }

  // Filter to credit cards and extract info
  const creditCards = [];
  accounts.forEach(account => {
    const cardInfo = parseAccountToCard(account);
    if (cardInfo) {
      creditCards.push(cardInfo);
    }
  });

  logMessage('INFO', `Found ${creditCards.length} credit cards from ${accounts.size} total accounts`);

  if (isDryRun) {
    logMessage('INFO', 'DRY_RUN: Would add cards: ' + JSON.stringify(creditCards.map(c => c.cardName)));
    SpreadsheetApp.getUi().alert(`DRY_RUN: Would add ${creditCards.length} credit cards:\n${creditCards.map(c => c.cardName).join('\n')}`);
    return;
  }

  // Get existing cards to avoid duplicates
  const cardsSheet = ss.getSheetByName(CONFIG.TABS.CARDS);
  const existingData = cardsSheet.getDataRange().getValues();
  const existingCardNames = new Set();
  for (let i = 1; i < existingData.length; i++) {
    if (existingData[i][2]) { // Card Name column
      existingCardNames.add(existingData[i][2].toLowerCase());
    }
  }

  // Add new cards
  const newCards = creditCards.filter(c => !existingCardNames.has(c.cardName.toLowerCase()));

  if (newCards.length === 0) {
    logMessage('INFO', 'No new cards to add');
    SpreadsheetApp.getUi().alert('✅ No new cards to add. All accounts already exist.');
    return;
  }

  const rowsToAdd = newCards.map(card => [
    card.cardId,
    card.issuer,
    card.cardName,
    card.last4,
    card.status,
    '', // Annual Fee (manual)
    1,  // Benefit Year Start Month default
    ''  // Notes
  ]);

  const lastRow = cardsSheet.getLastRow();
  cardsSheet.getRange(lastRow + 1, 1, rowsToAdd.length, 8).setValues(rowsToAdd);

  logMessage('INFO', `Added ${newCards.length} new credit cards`);
  SpreadsheetApp.getUi().alert(`✅ Added ${newCards.length} new credit cards!`);
}

/**
 * Parses an account string and returns card info if it's a credit card
 */
function parseAccountToCard(accountString) {
  const lower = accountString.toLowerCase();

  // Check exclusions first
  for (const exclude of CARD_EXCLUDE_KEYWORDS) {
    if (lower.includes(exclude)) {
      return null;
    }
  }

  // Check if it matches credit card patterns
  let isCard = false;
  for (const include of CARD_INCLUDE_KEYWORDS) {
    if (lower.includes(include)) {
      isCard = true;
      break;
    }
  }

  if (!isCard) return null;

  // Extract Last4 (look for patterns like "...1234" or "-1234" or "x1234")
  let last4 = '';
  const last4Match = accountString.match(/[\.x\-](\d{4})(?:\s|$|\))/i) ||
                     accountString.match(/(\d{4})$/);
  if (last4Match) {
    last4 = last4Match[1];
  }

  // Infer issuer
  let issuer = 'Unknown';
  for (const pattern of ISSUER_PATTERNS) {
    if (pattern.pattern.test(accountString)) {
      issuer = pattern.issuer;
      break;
    }
  }

  // Determine open/closed status
  const status = lower.includes('closed') ? 'Closed' : 'Open';

  // Clean up card name
  let cardName = accountString
    .replace(/\s*\(closed\)/i, '')
    .replace(/[\.x\-]\d{4}$/i, '')
    .replace(/\s+/g, ' ')
    .trim();

  // Generate stable Card ID
  const cardId = generateCardId(issuer, cardName, last4);

  return {
    cardId,
    issuer,
    cardName,
    last4,
    status
  };
}

/**
 * Generates a stable Card ID
 */
function generateCardId(issuer, cardName, last4) {
  // Create abbreviation from card name
  const words = cardName.split(/\s+/);
  let abbrev = '';

  // Take first letter of significant words
  for (const word of words) {
    if (word.length > 2 && !['the', 'and', 'of'].includes(word.toLowerCase())) {
      abbrev += word[0].toUpperCase();
    }
  }

  if (abbrev.length < 2) {
    abbrev = cardName.substring(0, 3).toUpperCase();
  }

  const suffix = last4 || Math.random().toString(36).substring(2, 6).toUpperCase();

  return `${abbrev}_${suffix}`;
}

/**
 * Ingests Transactions CSV from Google Drive
 */
function ingestTransactionsCSV() {
  const folderId = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRIVE_FOLDER_ID);

  if (!folderId) {
    SpreadsheetApp.getUi().alert('❌ Drive folder ID not set. Use Settings > Set Drive Folder ID');
    return;
  }

  try {
    const folder = DriveApp.getFolderById(folderId);
    const allFiles = folder.getFiles();

    let txFile = null;
    let latestDate = new Date(0);

    while (allFiles.hasNext()) {
      const file = allFiles.next();
      const name = file.getName().toLowerCase();
      if (name.startsWith('transaction') && (name.endsWith('.csv') || file.getMimeType() === 'text/csv')) {
        if (file.getLastUpdated() > latestDate) {
          txFile = file;
          latestDate = file.getLastUpdated();
        }
      }
    }

    if (!txFile) {
      SpreadsheetApp.getUi().alert('❌ No Transactions CSV found in the specified folder.');
      return;
    }

    const csvContent = txFile.getBlob().getDataAsString();
    processTransactionsCSV(csvContent);
    logMessage('INFO', `Ingested Transactions CSV from Drive: ${txFile.getName()}`);

  } catch (e) {
    logMessage('ERROR', `Failed to ingest Transactions from Drive: ${e.message}`);
    SpreadsheetApp.getUi().alert('❌ Error: ' + e.message);
  }
}

/**
 * Ingests Transactions CSV from Config tab (paste method)
 */
function ingestTransactionsFromConfigTab() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const configSheet = ss.getSheetByName(CONFIG.TABS.CONFIG);

  if (!configSheet) {
    SpreadsheetApp.getUi().alert('❌ Config tab not found. Run Setup first.');
    return;
  }

  const data = configSheet.getDataRange().getValues();
  let csvStartRow = -1;

  for (let i = 0; i < data.length; i++) {
    if (data[i][0] && data[i][0].toString().includes('Paste Transactions CSV')) {
      csvStartRow = i + 1;
      break;
    }
  }

  if (csvStartRow < 0) {
    SpreadsheetApp.getUi().alert('❌ Could not find Transactions CSV section in Config tab.');
    return;
  }

  // Extract CSV lines
  const csvLines = [];
  for (let i = csvStartRow; i < data.length; i++) {
    const row = data[i];
    const line = row.filter(cell => cell !== '').join(',');
    if (line.trim()) {
      csvLines.push(line);
    }
  }

  if (csvLines.length === 0) {
    SpreadsheetApp.getUi().alert('❌ No CSV data found. Paste your Transactions CSV content in the Config tab.');
    return;
  }

  const csvContent = csvLines.join('\n');
  processTransactionsCSV(csvContent);
  logMessage('INFO', 'Ingested Transactions CSV from Config tab');
}

/**
 * Processes Transactions CSV content
 */
function processTransactionsCSV(csvContent) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const isDryRun = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRY_RUN) === 'true';

  logMessage('INFO', `Processing Transactions CSV (DRY_RUN: ${isDryRun})`);

  const lines = csvContent.split(/\r?\n/).filter(line => line.trim());
  if (lines.length < 2) {
    logMessage('WARN', 'Transactions CSV has no data rows');
    return;
  }

  // Parse header
  const header = parseCSVLine(lines[0]);
  const colIndex = {};
  header.forEach((col, i) => {
    colIndex[col.toLowerCase().trim()] = i;
  });

  // Map columns (flexible matching)
  const dateCol = colIndex['date'] ?? colIndex['transaction date'];
  const merchantCol = colIndex['merchant'] ?? colIndex['description'] ?? colIndex['name'] ?? colIndex['payee'];
  const amountCol = colIndex['amount'];
  const categoryCol = colIndex['category'];
  const accountCol = colIndex['account'] ?? colIndex['account name'];
  const txIdCol = colIndex['transaction id'] ?? colIndex['id'] ?? colIndex['transaction_id'];
  const descCol = colIndex['original statement'] ?? colIndex['original description'] ?? colIndex['memo'];

  if (dateCol === undefined || merchantCol === undefined || amountCol === undefined) {
    logMessage('ERROR', 'Missing required columns in Transactions CSV');
    SpreadsheetApp.getUi().alert('❌ Missing required columns. Need: Date, Merchant/Description, Amount');
    return;
  }

  // Load existing dedupe keys
  const txSheet = ss.getSheetByName(CONFIG.TABS.TRANSACTIONS);
  const existingData = txSheet.getDataRange().getValues();
  const existingDedupeKeys = new Set();
  for (let i = 1; i < existingData.length; i++) {
    if (existingData[i][8]) { // Dedupe Key column
      existingDedupeKeys.add(existingData[i][8]);
    }
  }

  // Load card mappings
  const cardMap = buildCardMap(ss);

  // Process transactions
  const newTransactions = [];
  const duplicateCount = { byId: 0, byKey: 0 };

  for (let i = 1; i < lines.length; i++) {
    const row = parseCSVLine(lines[i]);

    const date = row[dateCol];
    const merchant = row[merchantCol] || '';
    const amount = parseFloat((row[amountCol] || '0').replace(/[$,]/g, ''));
    const category = categoryCol !== undefined ? row[categoryCol] : '';
    const account = accountCol !== undefined ? row[accountCol] : '';
    const txId = txIdCol !== undefined ? row[txIdCol] : '';
    const desc = descCol !== undefined ? row[descCol] : '';

    // Skip if no date (probably empty row)
    if (!date) continue;

    // Filter to tracking year
    const txDate = new Date(date);
    if (txDate.getFullYear() !== CONFIG.TRACKING_YEAR) continue;

    // Build dedupe key
    const dedupeKey = buildDedupeKey({
      txId,
      date,
      merchant,
      amount,
      account,
      description: desc || category
    });

    // Check for duplicates
    if (existingDedupeKeys.has(dedupeKey)) {
      duplicateCount.byKey++;
      continue;
    }

    // Mark as seen to catch duplicates within the same import
    existingDedupeKeys.add(dedupeKey);

    // Normalize merchant
    const merchantNormalized = normalizeMerchant(merchant, ss);

    // Match to card
    const cardId = matchAccountToCard(account, cardMap);

    newTransactions.push([
      date,
      merchant,
      merchantNormalized,
      amount,
      category,
      account,
      cardId,
      txId,
      dedupeKey,
      '', // Matched Perk ID (filled by matchPerks)
      '', // Match Confidence
      '', // Match Reason
      ''  // Notes / Override
    ]);
  }

  logMessage('INFO', `Parsed ${lines.length - 1} rows, ${newTransactions.length} new transactions, ${duplicateCount.byKey} duplicates skipped`);

  if (isDryRun) {
    logMessage('INFO', `DRY_RUN: Would add ${newTransactions.length} transactions`);
    SpreadsheetApp.getUi().alert(`DRY_RUN: Would add ${newTransactions.length} transactions\nDuplicates skipped: ${duplicateCount.byKey}`);
    return;
  }

  if (newTransactions.length === 0) {
    SpreadsheetApp.getUi().alert('✅ No new transactions to add.');
    return;
  }

  // Add new transactions
  const lastRow = txSheet.getLastRow();
  txSheet.getRange(lastRow + 1, 1, newTransactions.length, 13).setValues(newTransactions);

  // Sort by date descending
  if (txSheet.getLastRow() > 1) {
    txSheet.getRange(2, 1, txSheet.getLastRow() - 1, 13).sort({ column: 1, ascending: false });
  }

  logMessage('INFO', `Added ${newTransactions.length} new transactions`);
  SpreadsheetApp.getUi().alert(`✅ Added ${newTransactions.length} new transactions!\nDuplicates skipped: ${duplicateCount.byKey}`);
}

/**
 * Builds a dedupe key for a transaction
 */
function buildDedupeKey(tx) {
  // Prefer Transaction ID if present
  if (tx.txId && tx.txId.trim()) {
    return `ID:${tx.txId.trim()}`;
  }

  // Otherwise build composite key
  const parts = [
    tx.date,
    tx.merchant.toLowerCase().trim(),
    tx.amount.toFixed(2),
    tx.account.toLowerCase().trim(),
    (tx.description || '').toLowerCase().trim()
  ];

  return `KEY:${parts.join('|')}`;
}

/**
 * Parses a CSV line handling quoted fields
 */
function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }

  result.push(current.trim());
  return result;
}

// ============================================================================
// NORMALIZATION FUNCTIONS
// ============================================================================

/**
 * Normalizes cards: re-parses, assigns IDs, updates card info
 */
function normalizeCards() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.TABS.CARDS);

  if (!sheet || sheet.getLastRow() < 2) {
    logMessage('INFO', 'No cards to normalize');
    return;
  }

  const data = sheet.getDataRange().getValues();
  let updated = 0;

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    let cardId = row[0];
    let issuer = row[1];
    const cardName = row[2];
    let last4 = row[3];

    if (!cardName) continue;

    // Generate ID if missing
    if (!cardId) {
      // Try to extract last4 from card name if missing
      if (!last4) {
        const match = cardName.match(/(\d{4})$/);
        if (match) last4 = match[1];
      }

      // Infer issuer if missing
      if (!issuer) {
        for (const pattern of ISSUER_PATTERNS) {
          if (pattern.pattern.test(cardName)) {
            issuer = pattern.issuer;
            break;
          }
        }
        if (!issuer) issuer = 'Unknown';
      }

      cardId = generateCardId(issuer, cardName, last4);
      data[i][0] = cardId;
      data[i][1] = issuer;
      data[i][3] = last4;
      updated++;
    }
  }

  if (updated > 0) {
    sheet.getRange(1, 1, data.length, data[0].length).setValues(data);
    logMessage('INFO', `Normalized ${updated} cards`);
  }
}

/**
 * Normalizes a merchant name using alias rules
 */
function normalizeMerchant(rawMerchant, ss) {
  if (!rawMerchant) return '';

  const cleaned = rawMerchant
    .replace(/\s+/g, ' ')
    .replace(/[#*]/g, '')
    .trim();

  // Load alias rules (cached in script properties for performance)
  const aliasSheet = ss ? ss.getSheetByName(CONFIG.TABS.MERCHANT_ALIASES) :
                          SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.TABS.MERCHANT_ALIASES);

  if (!aliasSheet || aliasSheet.getLastRow() < 2) {
    return cleaned;
  }

  const rules = aliasSheet.getRange(2, 1, aliasSheet.getLastRow() - 1, 3).getValues();
  const lowerCleaned = cleaned.toLowerCase();

  // Apply rules in order (first match wins)
  for (const rule of rules) {
    const [matchType, pattern, canonical] = rule;
    if (!pattern || !canonical) continue;

    const lowerPattern = pattern.toLowerCase();

    switch (matchType) {
      case 'equals':
        if (lowerCleaned === lowerPattern) {
          return canonical;
        }
        break;
      case 'contains':
        if (lowerCleaned.includes(lowerPattern)) {
          return canonical;
        }
        break;
      case 'regex':
        try {
          const regex = new RegExp(pattern, 'i');
          if (regex.test(cleaned)) {
            return canonical;
          }
        } catch (e) {
          // Invalid regex, skip
        }
        break;
    }
  }

  return cleaned;
}

/**
 * Builds a map of account strings to Card IDs
 */
function buildCardMap(ss) {
  const sheet = ss.getSheetByName(CONFIG.TABS.CARDS);
  const cardMap = {};

  if (!sheet || sheet.getLastRow() < 2) return cardMap;

  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 4).getValues();

  for (const row of data) {
    const [cardId, issuer, cardName, last4] = row;
    if (!cardId || !cardName) continue;

    // Create multiple match keys
    const lowerName = cardName.toLowerCase();
    cardMap[lowerName] = cardId;

    if (last4) {
      cardMap[last4] = cardId;
      cardMap[`*${last4}`] = cardId;
      cardMap[`.${last4}`] = cardId;
    }

    // Also match on significant words
    const words = lowerName.split(/\s+/).filter(w => w.length > 3);
    for (const word of words) {
      if (!cardMap[word]) {
        cardMap[word] = cardId;
      }
    }
  }

  return cardMap;
}

/**
 * Matches an account string to a Card ID
 */
function matchAccountToCard(account, cardMap) {
  if (!account) return '';

  const lowerAccount = account.toLowerCase();

  // Direct match
  if (cardMap[lowerAccount]) {
    return cardMap[lowerAccount];
  }

  // Try last4 extraction
  const last4Match = account.match(/(\d{4})$/);
  if (last4Match && cardMap[last4Match[1]]) {
    return cardMap[last4Match[1]];
  }

  // Fuzzy match on words
  for (const [key, cardId] of Object.entries(cardMap)) {
    if (key.length > 3 && lowerAccount.includes(key)) {
      return cardId;
    }
  }

  return '';
}

// ============================================================================
// PERK MATCHING ENGINE
// ============================================================================

/**
 * Matches transactions to perks using scoring algorithm
 */
function matchPerks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const isDryRun = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRY_RUN) === 'true';

  logMessage('INFO', `Starting perk matching (DRY_RUN: ${isDryRun})`);

  const txSheet = ss.getSheetByName(CONFIG.TABS.TRANSACTIONS);
  const perksSheet = ss.getSheetByName(CONFIG.TABS.PERKS_CATALOG);

  if (!txSheet || txSheet.getLastRow() < 2) {
    logMessage('INFO', 'No transactions to match');
    return;
  }

  if (!perksSheet || perksSheet.getLastRow() < 2) {
    logMessage('WARN', 'No perks defined in catalog');
    SpreadsheetApp.getUi().alert('⚠️ No perks defined. Add perks to the Perks Catalog tab first.');
    return;
  }

  // Load perks
  const perksData = perksSheet.getRange(2, 1, perksSheet.getLastRow() - 1, 11).getValues();
  const perks = perksData.map(row => ({
    perkId: row[0],
    cardId: row[1],
    cardName: row[2],
    perkName: row[3],
    category: row[4],
    annualValue: parseFloat(row[5]) || 0,
    frequency: row[6],
    resetRule: row[7],
    merchantKeywords: (row[8] || '').toLowerCase().split('|').filter(k => k.trim()),
    monarchCategoryMatch: (row[9] || '').toLowerCase().split('|').filter(c => c.trim()),
    amountPattern: row[10] || ''
  })).filter(p => p.perkId);

  // Load category map
  const categoryMap = loadCategoryMap(ss);

  // Load transactions
  const txData = txSheet.getDataRange().getValues();
  const headers = txData[0];

  let matchedCount = 0;
  let updatedCount = 0;

  for (let i = 1; i < txData.length; i++) {
    const row = txData[i];
    const overridePerkId = (row[12] || '').trim(); // Notes/Override column
    const existingPerkId = row[9]; // Matched Perk ID

    // Skip if already has a match (unless override changes)
    if (existingPerkId && !overridePerkId) {
      continue;
    }

    const tx = {
      date: row[0],
      merchantRaw: row[1],
      merchantNormalized: (row[2] || '').toLowerCase(),
      amount: Math.abs(parseFloat(row[3]) || 0),
      category: (row[4] || '').toLowerCase(),
      cardId: row[6]
    };

    // If override is set, use it
    if (overridePerkId) {
      const overridePerk = perks.find(p => p.perkId === overridePerkId);
      if (overridePerk) {
        txData[i][9] = overridePerkId;
        txData[i][10] = 100;
        txData[i][11] = 'Manual override';
        updatedCount++;
        matchedCount++;
        continue;
      }
    }

    // Score each perk
    let bestMatch = null;
    let bestScore = 0;
    let bestReason = [];

    for (const perk of perks) {
      let score = 0;
      const reasons = [];

      // Must match card if perk has a card specified
      if (perk.cardId && tx.cardId && perk.cardId !== tx.cardId) {
        continue;
      }

      // Merchant keyword match (+60)
      const merchantMatched = perk.merchantKeywords.some(keyword =>
        tx.merchantNormalized.includes(keyword) ||
        (tx.merchantRaw || '').toLowerCase().includes(keyword)
      );
      if (merchantMatched) {
        score += 60;
        reasons.push('merchant_keyword');
      }

      // Category match (+25)
      const perkCategory = categoryMap[tx.category] || tx.category;
      const categoryMatched = perk.monarchCategoryMatch.some(cat =>
        tx.category.includes(cat) || perkCategory.toLowerCase().includes(cat)
      );
      if (categoryMatched) {
        score += 25;
        reasons.push('category');
      }

      // Amount pattern match (+15)
      if (perk.amountPattern && matchAmountPattern(tx.amount, perk.amountPattern)) {
        score += 15;
        reasons.push('amount');
      }

      // Neutral merchant penalty (-30) unless merchant explicitly matched
      if (!merchantMatched && isNeutralMerchant(tx.merchantNormalized)) {
        score -= 30;
        reasons.push('neutral_penalty');
      }

      if (score > bestScore && score >= CONFIG.MATCH_THRESHOLD) {
        bestScore = score;
        bestMatch = perk;
        bestReason = reasons;
      }
    }

    if (bestMatch) {
      txData[i][9] = bestMatch.perkId;
      txData[i][10] = bestScore;
      txData[i][11] = bestReason.join(', ');
      matchedCount++;
    }

    updatedCount++;
  }

  if (!isDryRun && updatedCount > 0) {
    txSheet.getRange(1, 1, txData.length, txData[0].length).setValues(txData);
  }

  logMessage('INFO', `Matched ${matchedCount} transactions (${updatedCount} processed)`);
  SpreadsheetApp.getUi().alert(`✅ Perk matching complete!\nMatched: ${matchedCount}\nProcessed: ${updatedCount}`);
}

/**
 * Checks if a merchant is in the neutral/ignore list
 */
function isNeutralMerchant(merchant) {
  const lower = merchant.toLowerCase();
  return NEUTRAL_MERCHANTS.some(n => lower.includes(n));
}

/**
 * Matches an amount against a pattern
 * Patterns: "=100", ">50", "<25", "50-100", "~50" (within 10%)
 */
function matchAmountPattern(amount, pattern) {
  if (!pattern) return false;

  pattern = pattern.trim();

  // Exact match
  if (pattern.startsWith('=')) {
    const target = parseFloat(pattern.substring(1));
    return Math.abs(amount - target) < 0.01;
  }

  // Greater than
  if (pattern.startsWith('>')) {
    const target = parseFloat(pattern.substring(1));
    return amount > target;
  }

  // Less than
  if (pattern.startsWith('<')) {
    const target = parseFloat(pattern.substring(1));
    return amount < target;
  }

  // Range
  if (pattern.includes('-')) {
    const [min, max] = pattern.split('-').map(parseFloat);
    return amount >= min && amount <= max;
  }

  // Approximate (within 10%)
  if (pattern.startsWith('~')) {
    const target = parseFloat(pattern.substring(1));
    return Math.abs(amount - target) / target <= 0.10;
  }

  // Direct number comparison
  const target = parseFloat(pattern);
  if (!isNaN(target)) {
    return Math.abs(amount - target) < 0.01;
  }

  return false;
}

/**
 * Loads the category map from sheet
 */
function loadCategoryMap(ss) {
  const sheet = ss.getSheetByName(CONFIG.TABS.CATEGORY_MAP);
  const map = {};

  if (!sheet || sheet.getLastRow() < 2) return map;

  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 2).getValues();

  for (const row of data) {
    const [monarchCat, perkCat] = row;
    if (monarchCat && perkCat) {
      map[monarchCat.toLowerCase()] = perkCat;
    }
  }

  return map;
}

// ============================================================================
// USAGE & PACING CALCULATION
// ============================================================================

/**
 * Calculates perk usage and pacing for the year
 */
function calculateUsage() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const isDryRun = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRY_RUN) === 'true';

  logMessage('INFO', `Calculating usage and pacing (DRY_RUN: ${isDryRun})`);

  const perksSheet = ss.getSheetByName(CONFIG.TABS.PERKS_CATALOG);
  const txSheet = ss.getSheetByName(CONFIG.TABS.TRANSACTIONS);
  const cardsSheet = ss.getSheetByName(CONFIG.TABS.CARDS);
  const usageSheet = ss.getSheetByName(CONFIG.TABS.PERK_USAGE);

  if (!perksSheet || perksSheet.getLastRow() < 2) {
    logMessage('WARN', 'No perks defined');
    return;
  }

  // Load perks
  const perksData = perksSheet.getRange(2, 1, perksSheet.getLastRow() - 1, 12).getValues();
  const perks = perksData.map(row => ({
    perkId: row[0],
    cardId: row[1],
    cardName: row[2],
    perkName: row[3],
    category: row[4],
    annualValue: parseFloat(row[5]) || 0,
    frequency: row[6],
    resetRule: row[7]
  })).filter(p => p.perkId);

  // Load card info for anniversary dates
  const cardAnniversaries = {};
  if (cardsSheet && cardsSheet.getLastRow() > 1) {
    const cardsData = cardsSheet.getRange(2, 1, cardsSheet.getLastRow() - 1, 7).getValues();
    for (const row of cardsData) {
      const cardId = row[0];
      const benefitMonth = parseInt(row[6]) || 1;
      cardAnniversaries[cardId] = benefitMonth;
    }
  }

  // Load transactions and aggregate by perk
  const perkUsage = {};
  const perkLastUsed = {};

  if (txSheet && txSheet.getLastRow() > 1) {
    const txData = txSheet.getRange(2, 1, txSheet.getLastRow() - 1, 13).getValues();

    for (const row of txData) {
      const txDate = row[0];
      const amount = Math.abs(parseFloat(row[3]) || 0);
      const matchedPerkId = row[9];

      if (!matchedPerkId) continue;

      if (!perkUsage[matchedPerkId]) {
        perkUsage[matchedPerkId] = 0;
      }
      perkUsage[matchedPerkId] += amount;

      // Track last used date
      if (!perkLastUsed[matchedPerkId] || new Date(txDate) > new Date(perkLastUsed[matchedPerkId])) {
        perkLastUsed[matchedPerkId] = txDate;
      }
    }
  }

  // Calculate pacing for each perk
  const now = new Date();
  const usageRows = [];

  for (const perk of perks) {
    const used = Math.min(perkUsage[perk.perkId] || 0, perk.annualValue);
    const remaining = Math.max(perk.annualValue - used, 0);
    const percentUsed = perk.annualValue > 0 ? used / perk.annualValue : 0;

    // Calculate expected pace
    const anniversaryMonth = cardAnniversaries[perk.cardId] || 1;
    const expectedPace = calculateExpectedPace(perk.frequency, perk.resetRule, anniversaryMonth, now);

    // Calculate pace delta and status
    const paceDelta = percentUsed - expectedPace;
    const tolerance = Math.max(CONFIG.TOLERANCE_PERCENT, CONFIG.TOLERANCE_MIN_DOLLARS / perk.annualValue);

    let status = 'On Track';
    if (percentUsed < expectedPace - tolerance) {
      status = 'Behind';
    } else if (percentUsed > expectedPace + tolerance) {
      status = 'Ahead';
    }

    usageRows.push([
      perk.perkId,
      perk.cardName,
      perk.perkName,
      perk.annualValue,
      used,
      remaining,
      percentUsed,
      expectedPace,
      paceDelta,
      status,
      perkLastUsed[perk.perkId] || ''
    ]);
  }

  if (!isDryRun) {
    // Clear existing data and write new
    if (usageSheet.getLastRow() > 1) {
      usageSheet.getRange(2, 1, usageSheet.getLastRow() - 1, 11).clear();
    }

    if (usageRows.length > 0) {
      usageSheet.getRange(2, 1, usageRows.length, 11).setValues(usageRows);
    }
  }

  const behindCount = usageRows.filter(r => r[9] === 'Behind').length;
  const unusedCount = usageRows.filter(r => r[4] === 0).length;

  logMessage('INFO', `Calculated usage for ${usageRows.length} perks. Behind: ${behindCount}, Unused: ${unusedCount}`);
  SpreadsheetApp.getUi().alert(`✅ Usage calculated!\nPerks: ${usageRows.length}\nBehind: ${behindCount}\nUnused: ${unusedCount}`);
}

/**
 * Calculates expected pace percentage based on frequency and reset rule
 */
function calculateExpectedPace(frequency, resetRule, anniversaryMonth, now) {
  const year = CONFIG.TRACKING_YEAR;
  let periodStart, periodEnd, current;

  if (resetRule === 'anniversary') {
    // Anniversary-based reset
    periodStart = new Date(year, anniversaryMonth - 1, 1);
    if (now < periodStart) {
      // We're before the anniversary this year, use last year's period
      periodStart = new Date(year - 1, anniversaryMonth - 1, 1);
    }
    periodEnd = new Date(periodStart.getFullYear() + 1, anniversaryMonth - 1, 1);
    current = now;
  } else {
    // Calendar year reset
    periodStart = new Date(year, 0, 1);
    periodEnd = new Date(year + 1, 0, 1);
    current = now;
  }

  // Clamp current to period
  if (current < periodStart) current = periodStart;
  if (current > periodEnd) current = periodEnd;

  const totalDays = (periodEnd - periodStart) / (1000 * 60 * 60 * 24);
  const elapsedDays = (current - periodStart) / (1000 * 60 * 60 * 24);

  switch (frequency) {
    case 'monthly':
      // Expected usage = months elapsed / 12
      const monthsElapsed = (current.getFullYear() - periodStart.getFullYear()) * 12 +
                           (current.getMonth() - periodStart.getMonth()) +
                           (current.getDate() / 30); // Partial month
      return Math.min(monthsElapsed / 12, 1);

    case 'quarterly':
      // Expected usage = quarters elapsed / 4
      const quartersElapsed = monthsElapsed / 3;
      return Math.min(quartersElapsed / 4, 1);

    case 'annual':
    case 'one_time':
      // Linear progression through the year
      return elapsedDays / totalDays;

    case 'every_4_years':
      // Treat as annual but cap at 25% per year
      const yearlyPace = elapsedDays / totalDays;
      return Math.min(yearlyPace * 0.25, 0.25); // Max 25% expected per year

    default:
      return elapsedDays / totalDays;
  }
}

// ============================================================================
// DASHBOARD UPDATE
// ============================================================================

/**
 * Updates the dashboard with summary and tables
 */
function updateDashboard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const isDryRun = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRY_RUN) === 'true';

  logMessage('INFO', `Updating dashboard (DRY_RUN: ${isDryRun})`);

  const usageSheet = ss.getSheetByName(CONFIG.TABS.PERK_USAGE);
  const dashSheet = ss.getSheetByName(CONFIG.TABS.DASHBOARD);

  if (!usageSheet || usageSheet.getLastRow() < 2) {
    logMessage('WARN', 'No usage data to display');
    return;
  }

  // Load usage data
  const usageData = usageSheet.getRange(2, 1, usageSheet.getLastRow() - 1, 11).getValues();

  // Calculate summary metrics
  let totalValue = 0;
  let usedYTD = 0;
  let remaining = 0;
  let behindCount = 0;
  let unusedCount = 0;

  const behindPerks = [];
  const unusedPerks = [];

  for (const row of usageData) {
    const [perkId, card, perk, maxValue, used, rem, percentUsed, expectedPace, paceDelta, status, lastUsed] = row;

    totalValue += maxValue || 0;
    usedYTD += used || 0;
    remaining += rem || 0;

    if (status === 'Behind') {
      behindCount++;
      behindPerks.push({
        perk,
        card,
        maxValue,
        used,
        expected: (expectedPace || 0) * (maxValue || 0),
        paceDelta,
        status
      });
    }

    if ((used || 0) === 0 && (maxValue || 0) > 0) {
      unusedCount++;
      unusedPerks.push({
        perk,
        card,
        maxValue,
        remaining: rem,
        frequency: '' // Would need to join with perks catalog
      });
    }
  }

  // Sort behind perks by pace delta (worst first)
  behindPerks.sort((a, b) => (a.paceDelta || 0) - (b.paceDelta || 0));

  // Sort unused perks by remaining value (highest first)
  unusedPerks.sort((a, b) => (b.remaining || 0) - (a.remaining || 0));

  if (isDryRun) {
    logMessage('INFO', `DRY_RUN: Dashboard would show: Total=$${totalValue}, Used=$${usedYTD}, Behind=${behindCount}`);
    return;
  }

  // Update summary section
  dashSheet.getRange('B4').setValue(totalValue).setNumberFormat('$#,##0.00');
  dashSheet.getRange('B5').setValue(usedYTD).setNumberFormat('$#,##0.00');
  dashSheet.getRange('B6').setValue(remaining).setNumberFormat('$#,##0.00');
  dashSheet.getRange('B7').setValue(behindCount);
  dashSheet.getRange('B8').setValue(unusedCount);
  dashSheet.getRange('B9').setValue(new Date()).setNumberFormat('yyyy-mm-dd hh:mm');

  // Update "Perks I'm Behind On" table
  // Clear old data
  const behindStartRow = 13;
  const behindMaxRows = 10;
  dashSheet.getRange(behindStartRow, 1, behindMaxRows, 7).clear();

  if (behindPerks.length > 0) {
    const behindRows = behindPerks.slice(0, behindMaxRows).map(p => [
      p.perk,
      p.card,
      p.maxValue,
      p.used,
      p.expected,
      p.paceDelta,
      p.status
    ]);
    dashSheet.getRange(behindStartRow, 1, behindRows.length, 7).setValues(behindRows);

    // Format
    dashSheet.getRange(behindStartRow, 3, behindRows.length, 3).setNumberFormat('$#,##0.00');
    dashSheet.getRange(behindStartRow, 6, behindRows.length, 1).setNumberFormat('+0%;-0%;0%');
  }

  // Update "Biggest Unused Perks" table
  const unusedStartRow = 27;
  const unusedMaxRows = 10;
  dashSheet.getRange(unusedStartRow, 1, unusedMaxRows, 5).clear();

  if (unusedPerks.length > 0) {
    const unusedRows = unusedPerks.slice(0, unusedMaxRows).map(p => [
      p.perk,
      p.card,
      p.maxValue,
      p.remaining,
      p.frequency
    ]);
    dashSheet.getRange(unusedStartRow, 1, unusedRows.length, 5).setValues(unusedRows);

    // Format
    dashSheet.getRange(unusedStartRow, 3, unusedRows.length, 2).setNumberFormat('$#,##0.00');
  }

  logMessage('INFO', `Dashboard updated. Total value: $${totalValue.toFixed(2)}, Behind: ${behindCount}`);
}

// ============================================================================
// TRIGGER MANAGEMENT
// ============================================================================

/**
 * Installs a nightly trigger (idempotent)
 */
function installNightlyTrigger() {
  // Remove existing triggers first
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    if (trigger.getHandlerFunction() === 'nightlyPipeline') {
      ScriptApp.deleteTrigger(trigger);
    }
  }

  // Create new trigger at 2 AM
  ScriptApp.newTrigger('nightlyPipeline')
    .timeBased()
    .atHour(2)
    .everyDays(1)
    .create();

  logMessage('INFO', 'Installed nightly trigger for 2 AM');
  SpreadsheetApp.getUi().alert('✅ Nightly trigger installed! Will run at 2 AM daily.');
}

/**
 * Removes all triggers
 */
function removeAllTriggers() {
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    ScriptApp.deleteTrigger(trigger);
  }

  logMessage('INFO', `Removed ${triggers.length} triggers`);
  SpreadsheetApp.getUi().alert(`✅ Removed ${triggers.length} trigger(s).`);
}

/**
 * Nightly pipeline function called by trigger
 */
function nightlyPipeline() {
  logMessage('INFO', '========== NIGHTLY PIPELINE START ==========');

  try {
    // Try to ingest from Drive (skip if folder not configured)
    const folderId = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRIVE_FOLDER_ID);
    if (folderId) {
      try {
        ingestBalancesCSV();
        ingestTransactionsCSV();
      } catch (e) {
        logMessage('WARN', `Drive ingestion skipped: ${e.message}`);
      }
    }

    // Run pipeline
    normalizeCards();
    matchPerks();
    calculateUsage();
    updateDashboard();

    logMessage('INFO', '========== NIGHTLY PIPELINE COMPLETE ==========');
  } catch (e) {
    logMessage('ERROR', `Nightly pipeline failed: ${e.message}`);
  }
}

// ============================================================================
// SETTINGS FUNCTIONS
// ============================================================================

/**
 * Prompts for Drive folder ID
 */
function promptForFolderId() {
  const ui = SpreadsheetApp.getUi();
  const current = PropertiesService.getScriptProperties().getProperty(CONFIG.PROPS.DRIVE_FOLDER_ID) || '(not set)';

  const result = ui.prompt(
    'Set Drive Folder ID',
    `Current folder ID: ${current}\n\nEnter the Google Drive folder ID where your CSV files are stored:`,
    ui.ButtonSet.OK_CANCEL
  );

  if (result.getSelectedButton() === ui.Button.OK) {
    const folderId = result.getResponseText().trim();
    if (folderId) {
      PropertiesService.getScriptProperties().setProperty(CONFIG.PROPS.DRIVE_FOLDER_ID, folderId);
      logMessage('INFO', `Drive folder ID set to: ${folderId}`);
      ui.alert(`✅ Folder ID saved: ${folderId}`);
    }
  }
}

/**
 * Toggles DRY_RUN mode
 */
function toggleDryRun() {
  const props = PropertiesService.getScriptProperties();
  const current = props.getProperty(CONFIG.PROPS.DRY_RUN) === 'true';
  const newValue = !current;

  props.setProperty(CONFIG.PROPS.DRY_RUN, newValue.toString());
  logMessage('INFO', `DRY_RUN mode set to: ${newValue}`);

  SpreadsheetApp.getUi().alert(`DRY_RUN mode is now: ${newValue ? 'ON' : 'OFF'}\n\nWhen ON, no data will be written.`);
}

/**
 * Displays current settings
 */
function viewSettings() {
  const props = PropertiesService.getScriptProperties();

  const settings = [
    `Drive Folder ID: ${props.getProperty(CONFIG.PROPS.DRIVE_FOLDER_ID) || '(not set)'}`,
    `DRY_RUN Mode: ${props.getProperty(CONFIG.PROPS.DRY_RUN) || 'false'}`,
    `Last Ingest: ${props.getProperty(CONFIG.PROPS.LAST_INGEST_DATE) || '(never)'}`,
    `Tracking Year: ${CONFIG.TRACKING_YEAR}`,
    `Match Threshold: ${CONFIG.MATCH_THRESHOLD}`,
    `Tolerance: ${CONFIG.TOLERANCE_PERCENT * 100}% or $${CONFIG.TOLERANCE_MIN_DOLLARS} min`
  ];

  SpreadsheetApp.getUi().alert('Current Settings:\n\n' + settings.join('\n'));
}

// ============================================================================
// LOGGING
// ============================================================================

/**
 * Logs a message to the Log tab
 */
function logMessage(level, message) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let logSheet = ss.getSheetByName(CONFIG.TABS.LOG);

    if (!logSheet) {
      logSheet = ss.insertSheet(CONFIG.TABS.LOG);
      logSheet.getRange(1, 1, 1, 3).setValues([['Timestamp', 'Level', 'Message']]);
      logSheet.getRange(1, 1, 1, 3).setFontWeight('bold').setBackground('#4285f4').setFontColor('white');
      logSheet.setFrozenRows(1);
    }

    const timestamp = new Date();
    logSheet.appendRow([timestamp, level, message]);

    // Keep only last 1000 rows
    if (logSheet.getLastRow() > 1001) {
      logSheet.deleteRows(2, logSheet.getLastRow() - 1001);
    }

    // Also log to console
    console.log(`[${level}] ${message}`);
  } catch (e) {
    console.log(`[${level}] ${message} (logging to sheet failed: ${e.message})`);
  }
}

// ============================================================================
// YOUR SPECIFIC CARDS - PRE-POPULATED FROM MONARCH DATA
// ============================================================================

/**
 * Seeds YOUR specific credit cards extracted from Monarch transactions
 * Run this to pre-populate your Cards tab with your actual cards
 */
function seedMyCards() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.TABS.CARDS);

  if (!sheet) {
    SpreadsheetApp.getUi().alert('Run Setup first!');
    return;
  }

  // Your actual cards from Monarch data
  const myCards = [
    // Card ID, Issuer, Card Name, Last4, Open/Closed, Annual Fee, Benefit Year Start Month, Notes
    ['MSR_1041', 'Chase', "Michelle's Sapphire Reserve (...1041)", '1041', 'Open', 550, 1, 'Chase Sapphire Reserve - Travel benefits'],
    ['GAPP_1007', 'Amex', "Gray's Amex Platinum Card® (...1007)", '1007', 'Open', 695, 1, 'Amex Platinum - Premium travel card'],
    ['GAGC_2003', 'Amex', "Gray's Amex Gold Card (...2003)", '2003', 'Open', 250, 1, 'Amex Gold - Dining & groceries'],
    ['MPC_7008', 'Amex', "Michelle's Platinum Card® (...7008)", '7008', 'Open', 695, 1, 'Amex Platinum'],
    ['MMBB_5005', 'Amex', "Michelle's Marriott Bonvoy Brilliant® (...5005)", '5005', 'Open', 650, 1, 'Marriott Bonvoy Brilliant'],
    ['MFU_9759', 'Chase', "Michelle's Freedom Unlimited (...9759)", '9759', 'Open', 0, 1, 'Chase Freedom Unlimited - No AF'],
    ['MSC_0443', 'Chase', "Michelle's Slate Card (...0443)", '0443', 'Open', 0, 1, 'Chase Slate - Balance transfer'],
    ['VEN_4522', 'Capital One', 'Venture (...4522)', '4522', 'Open', 95, 1, 'Capital One Venture'],
    ['APC_5990', 'Chase', 'Amazon Prime Card (...5990)', '5990', 'Open', 0, 1, 'Amazon Prime Visa - 5% Amazon'],
    ['TCC_2828', 'Target', 'Target Circle Card (...2828)', '2828', 'Open', 0, 1, 'Target Circle Card - 5% Target'],
    ['USAA_9385', 'USAA', 'USAA Rate Advantage Platinum Visa (...9385)', '9385', 'Open', 0, 1, 'USAA Rate Advantage']
  ];

  // Check if cards already exist
  if (sheet.getLastRow() > 1) {
    const confirm = SpreadsheetApp.getUi().alert(
      'Cards tab already has data. Overwrite?',
      SpreadsheetApp.getUi().ButtonSet.YES_NO
    );
    if (confirm !== SpreadsheetApp.getUi().Button.YES) return;
    sheet.getRange(2, 1, sheet.getLastRow() - 1, 8).clear();
  }

  if (myCards.length > 0) {
    sheet.getRange(2, 1, myCards.length, 8).setValues(myCards);
  }

  logMessage('INFO', `Seeded ${myCards.length} cards from your Monarch data`);
  SpreadsheetApp.getUi().alert(`✅ Added ${myCards.length} credit cards from your Monarch data!`);
}

/**
 * Seeds YOUR specific perks for your actual cards
 * These are customized for your card portfolio
 */
function seedMyPerks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.TABS.PERKS_CATALOG);

  if (!sheet) {
    SpreadsheetApp.getUi().alert('Run Setup first!');
    return;
  }

  // Only seed if empty
  if (sheet.getLastRow() > 1) {
    const confirm = SpreadsheetApp.getUi().alert(
      'Perks catalog already has data. Overwrite?',
      SpreadsheetApp.getUi().ButtonSet.YES_NO
    );
    if (confirm !== SpreadsheetApp.getUi().Button.YES) return;
    sheet.getRange(2, 1, sheet.getLastRow() - 1, 12).clear();
  }

  // Perks matched to YOUR specific cards (Card IDs match seedMyCards)
  const myPerks = [
    // ========== Michelle's Sapphire Reserve (MSR_1041) ==========
    ['MSR_TRAVEL', 'MSR_1041', "Michelle's Sapphire Reserve", '$300 Travel Credit', 'Travel', 300, 'annual', 'anniversary', 'airline|hotel|airbnb|lyft|uber|lord camden|woodstock inn|breeze|american airlines', 'travel|hotel|airline|taxi & ride shares', '', '$300 annual travel credit'],
    ['MSR_GE', 'MSR_1041', "Michelle's Sapphire Reserve", 'Global Entry/TSA PreCheck', 'Fees', 100, 'every_4_years', 'anniversary', 'global entry|tsa precheck|clear', '', '=100', 'Every 4 years'],
    ['MSR_DOORDASH', 'MSR_1041', "Michelle's Sapphire Reserve", 'DoorDash DashPass', 'Subscriptions', 60, 'annual', 'calendar', 'doordash', 'delivery & takeout', '', 'Free DashPass ($5/mo credit value)'],
    ['MSR_LYFT', 'MSR_1041', "Michelle's Sapphire Reserve", 'Lyft Pink', 'Travel', 0, 'annual', 'calendar', 'lyft', 'taxi & ride shares', '', 'Free Lyft Pink membership'],

    // ========== Gray's Amex Platinum (GAPP_1007) ==========
    ['GAPP_UBER', 'GAPP_1007', "Gray's Amex Platinum Card®", 'Uber Credit', 'Travel', 200, 'monthly', 'calendar', 'uber|uber eats', 'taxi & ride shares|delivery & takeout', '15-35', '$15/mo ($35 Dec)'],
    ['GAPP_AIRLINE', 'GAPP_1007', "Gray's Amex Platinum Card®", 'Airline Fee Credit', 'Travel', 200, 'annual', 'calendar', 'breeze|american airlines|delta|united|airline', 'airline', '', 'Select one airline - incidentals'],
    ['GAPP_SAKS', 'GAPP_1007', "Gray's Amex Platinum Card®", 'Saks Credit', 'Retail', 100, 'annual', 'calendar', 'saks|saks fifth avenue', 'shopping|clothing', '', '$50 Jan-Jun, $50 Jul-Dec'],
    ['GAPP_HOTEL', 'GAPP_1007', "Gray's Amex Platinum Card®", 'Hotel Credit', 'Travel', 200, 'annual', 'calendar', 'hotel collection|fine hotels|lord camden|woodstock', 'hotel', '', 'FHR/THC bookings'],
    ['GAPP_CLEAR', 'GAPP_1007', "Gray's Amex Platinum Card®", 'CLEAR Credit', 'Fees', 189, 'annual', 'calendar', 'clear', '', '~189', 'CLEAR membership'],
    ['GAPP_DIGITAL', 'GAPP_1007', "Gray's Amex Platinum Card®", 'Digital Entertainment', 'Entertainment', 240, 'monthly', 'calendar', 'disney+|hulu|espn+|peacock|nyt|audible|youtube tv', 'streaming|subscriptions|youtube tv', '~20', '$20/month'],
    ['GAPP_WALMART', 'GAPP_1007', "Gray's Amex Platinum Card®", 'Walmart+ Credit', 'Subscriptions', 155, 'annual', 'calendar', 'walmart+|walmart plus|wmt plus', 'shopping', '~13', 'Annual Walmart+ membership'],
    ['GAPP_EQUINOX', 'GAPP_1007', "Gray's Amex Platinum Card®", 'Equinox Credit', 'Fitness', 300, 'annual', 'calendar', 'equinox|soulcycle', 'gym|fitness', '', '$25/month'],

    // ========== Michelle's Amex Platinum (MPC_7008) ==========
    ['MPC_UBER', 'MPC_7008', "Michelle's Platinum Card®", 'Uber Credit', 'Travel', 200, 'monthly', 'calendar', 'uber|uber eats', 'taxi & ride shares|delivery & takeout', '15-35', '$15/mo ($35 Dec)'],
    ['MPC_AIRLINE', 'MPC_7008', "Michelle's Platinum Card®", 'Airline Fee Credit', 'Travel', 200, 'annual', 'calendar', 'breeze|american airlines|delta|united|airline', 'airline', '', 'Select one airline'],
    ['MPC_SAKS', 'MPC_7008', "Michelle's Platinum Card®", 'Saks Credit', 'Retail', 100, 'annual', 'calendar', 'saks|saks fifth avenue', 'shopping|clothing', '', '$50 Jan-Jun, $50 Jul-Dec'],
    ['MPC_HOTEL', 'MPC_7008', "Michelle's Platinum Card®", 'Hotel Credit', 'Travel', 200, 'annual', 'calendar', 'hotel collection|fine hotels', 'hotel', '', 'FHR/THC bookings'],
    ['MPC_WALMART', 'MPC_7008', "Michelle's Platinum Card®", 'Walmart+ Credit', 'Subscriptions', 155, 'annual', 'calendar', 'walmart+|walmart plus|wmt plus', 'shopping', '~13', 'Annual Walmart+ membership'],
    ['MPC_DIGITAL', 'MPC_7008', "Michelle's Platinum Card®", 'Digital Entertainment', 'Entertainment', 240, 'monthly', 'calendar', 'disney+|hulu|espn+|peacock|nyt|audible', 'streaming|subscriptions', '~20', '$20/month'],
    ['MPC_CLEAR', 'MPC_7008', "Michelle's Platinum Card®", 'CLEAR Credit', 'Fees', 189, 'annual', 'calendar', 'clear', '', '~189', 'CLEAR membership'],

    // ========== Gray's Amex Gold (GAGC_2003) ==========
    ['GAGC_DINING', 'GAGC_2003', "Gray's Amex Gold Card", 'Dining Credit', 'Dining', 120, 'monthly', 'calendar', 'grubhub|seamless|cheesecake factory|goldbelly|wine.com|milk bar', 'restaurants & bars|delivery & takeout', '10', '$10/month at partners'],
    ['GAGC_UBER', 'GAGC_2003', "Gray's Amex Gold Card", 'Uber Cash', 'Travel', 120, 'monthly', 'calendar', 'uber|uber eats', 'taxi & ride shares|delivery & takeout', '10', '$10/month Uber Cash'],
    ['GAGC_DUNKIN', 'GAGC_2003', "Gray's Amex Gold Card", "Dunkin' Credit", 'Dining', 84, 'monthly', 'calendar', 'dunkin', 'delivery & takeout|coffee', '7', '$7/month'],

    // ========== Marriott Bonvoy Brilliant (MMBB_5005) ==========
    ['MMBB_DINING', 'MMBB_5005', "Michelle's Marriott Bonvoy Brilliant®", 'Dining Credit', 'Dining', 300, 'annual', 'calendar', 'marriott|restaurant|dining', 'restaurants & bars', '', '$25/month at Marriott restaurants'],
    ['MMBB_HOTEL', 'MMBB_5005', "Michelle's Marriott Bonvoy Brilliant®", 'Hotel Credit', 'Travel', 300, 'annual', 'anniversary', 'marriott|ritz|westin|sheraton|w hotel', 'hotel', '', '$300 Marriott Bonvoy credit'],
    ['MMBB_FNC', 'MMBB_5005', "Michelle's Marriott Bonvoy Brilliant®", 'Free Night Award', 'Travel', 500, 'annual', 'anniversary', '', '', '', '85K points free night (est. $500 value)'],

    // ========== Capital One Venture (VEN_4522) ==========
    ['VEN_TRAVEL', 'VEN_4522', 'Venture', 'Travel Credit', 'Travel', 100, 'annual', 'anniversary', 'capital one travel', 'travel', '', '$100 Global Entry/TSA credit'],
    ['VEN_ANNIVERSARY', 'VEN_4522', 'Venture', 'Anniversary Miles', 'Travel', 100, 'annual', 'anniversary', '', '', '', '10K miles annually (est. $100)'],
  ];

  if (myPerks.length > 0) {
    sheet.getRange(2, 1, myPerks.length, 12).setValues(myPerks);
  }

  logMessage('INFO', `Seeded ${myPerks.length} perks for your cards`);
  SpreadsheetApp.getUi().alert(`✅ Added ${myPerks.length} perks for your credit cards!\n\nReview and adjust values in Perks Catalog as needed.`);
}

/**
 * Quick setup: runs full setup + seeds your cards + seeds your perks
 */
function quickSetupWithMyData() {
  setupSheet_IfNeeded();
  seedMyCards();
  seedMyPerks();
  SpreadsheetApp.getUi().alert('✅ Quick setup complete!\n\nYour cards and perks have been added.\n\nNext steps:\n1. Paste your Transactions CSV in Config tab\n2. Run "Ingest Transactions CSV"\n3. Run "Run Full Pipeline"');
}

// ============================================================================
// SAMPLE PERKS CATALOG SEEDER (Generic - for reference)
// ============================================================================

/**
 * Seeds generic sample perks for common credit cards
 * Use seedMyPerks() instead for your specific cards
 */
function seedSamplePerks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.TABS.PERKS_CATALOG);

  if (!sheet) {
    SpreadsheetApp.getUi().alert('Run Setup first!');
    return;
  }

  // Only seed if empty
  if (sheet.getLastRow() > 1) {
    const confirm = SpreadsheetApp.getUi().alert(
      'Perks catalog already has data. Overwrite?',
      SpreadsheetApp.getUi().ButtonSet.YES_NO
    );
    if (confirm !== SpreadsheetApp.getUi().Button.YES) return;
    sheet.getRange(2, 1, sheet.getLastRow() - 1, 12).clear();
  }

  const samplePerks = [
    // Chase Sapphire Reserve
    ['CSR_TRAVEL', '', 'Chase Sapphire Reserve', '$300 Travel Credit', 'Travel', 300, 'annual', 'anniversary', 'airline|hotel|airbnb|lyft|uber', 'travel|flights|hotels', '', 'Annual travel credit'],
    ['CSR_GE', '', 'Chase Sapphire Reserve', 'Global Entry/TSA Credit', 'Fees', 100, 'every_4_years', 'anniversary', 'global entry|tsa precheck|clear', '', '=100', 'Every 4 years'],
    ['CSR_DOORDASH', '', 'Chase Sapphire Reserve', 'DoorDash DashPass', 'Subscriptions', 0, 'annual', 'calendar', 'doordash', 'food & drink', '', 'Free DashPass membership'],
    ['CSR_LYFT', '', 'Chase Sapphire Reserve', 'Lyft Pink', 'Subscriptions', 0, 'annual', 'calendar', 'lyft', 'rideshare', '', 'Free Lyft Pink membership'],

    // Amex Platinum
    ['PLAT_UBER', '', 'Amex Platinum', 'Uber Credit', 'Travel', 200, 'monthly', 'calendar', 'uber|uber eats', 'rideshare|food delivery', '15-35', '$15/mo ($35 Dec)'],
    ['PLAT_AIRLINE', '', 'Amex Platinum', 'Airline Fee Credit', 'Travel', 200, 'annual', 'calendar', 'airline|delta|united|american', 'flights', '', 'Select one airline'],
    ['PLAT_SAKS', '', 'Amex Platinum', 'Saks Credit', 'Retail', 100, 'annual', 'calendar', 'saks|saks fifth avenue', 'shopping|clothing', '', '$50 Jan-Jun, $50 Jul-Dec'],
    ['PLAT_HOTEL', '', 'Amex Platinum', 'Hotel Credit', 'Travel', 200, 'annual', 'calendar', 'hotel collection|fine hotels', 'hotels', '', 'FHR/THC bookings'],
    ['PLAT_CLEAR', '', 'Amex Platinum', 'CLEAR Credit', 'Fees', 189, 'annual', 'calendar', 'clear', '', '~189', 'CLEAR membership'],
    ['PLAT_EQUINOX', '', 'Amex Platinum', 'Equinox Credit', 'Fitness', 300, 'annual', 'calendar', 'equinox|soulcycle', 'gym|fitness', '', '$25/month'],
    ['PLAT_ENTERTAINMENT', '', 'Amex Platinum', 'Entertainment Credit', 'Entertainment', 240, 'monthly', 'calendar', 'disney+|hulu|espn+|peacock|nyt|audible', 'streaming|subscriptions', '', '$20/month'],
    ['PLAT_WALMART', '', 'Amex Platinum', 'Walmart+ Credit', 'Subscriptions', 155, 'annual', 'calendar', 'walmart+|walmart plus', 'subscriptions', '~155', 'Annual membership'],

    // Amex Gold
    ['GOLD_DINING', '', 'Amex Gold', 'Dining Credit', 'Dining', 120, 'monthly', 'calendar', 'grubhub|seamless|cheesecake factory|goldbelly|wine.com|milk bar', 'restaurants|food delivery', '10', '$10/month at partners'],
    ['GOLD_UBER', '', 'Amex Gold', 'Uber Cash', 'Travel', 120, 'monthly', 'calendar', 'uber|uber eats', 'rideshare|food delivery', '10', '$10/month Uber Cash'],
    ['GOLD_DUNKIN', '', 'Amex Gold', "Dunkin' Credit", 'Dining', 84, 'monthly', 'calendar', 'dunkin', 'coffee|food & drink', '7', '$7/month'],

    // Capital One Venture X
    ['VENX_TRAVEL', '', 'Capital One Venture X', 'Travel Credit', 'Travel', 300, 'annual', 'anniversary', 'capital one travel', 'travel', '', 'Via Capital One Travel portal'],
    ['VENX_GE', '', 'Capital One Venture X', 'Global Entry Credit', 'Fees', 100, 'every_4_years', 'anniversary', 'global entry|tsa precheck', '', '=100', 'Every 4 years'],

    // Hilton Aspire
    ['ASPIRE_RESORT', '', 'Hilton Aspire', 'Resort Credit', 'Travel', 400, 'annual', 'anniversary', 'hilton|waldorf|conrad|lxr', 'hotels', '', 'At Hilton resorts'],
    ['ASPIRE_AIRLINE', '', 'Hilton Aspire', 'Airline Credit', 'Travel', 250, 'annual', 'calendar', 'airline', 'flights', '', 'Select one airline'],
    ['ASPIRE_FNC', '', 'Hilton Aspire', 'Free Night Cert', 'Travel', 500, 'annual', 'anniversary', '', '', '', 'Estimated value'],
  ];

  if (samplePerks.length > 0) {
    sheet.getRange(2, 1, samplePerks.length, 12).setValues(samplePerks);
  }

  logMessage('INFO', `Seeded ${samplePerks.length} sample perks`);
  SpreadsheetApp.getUi().alert(`✅ Seeded ${samplePerks.length} sample perks!\n\nEdit the Card ID column to match your actual cards.`);
}
