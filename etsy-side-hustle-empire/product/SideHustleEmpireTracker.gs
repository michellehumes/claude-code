/**
 * ============================================================
 * 🚀 ULTIMATE SIDE HUSTLE EMPIRE TRACKER
 * ============================================================
 *
 * A comprehensive Google Sheets template for tracking multiple
 * income streams, expenses, and preparing for tax season.
 *
 * HOW TO USE:
 * 1. Open a new Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Paste this entire code
 * 4. Run the 'createSideHustleEmpireTracker' function
 * 5. Your tracker will be automatically created!
 *
 * ============================================================
 */

// ============================================================
// CONFIGURATION
// ============================================================

const CONFIG = {
  colors: {
    primary: '#2E7D32',      // Forest Green
    secondary: '#1565C0',    // Royal Blue
    accent: '#F57C00',       // Orange
    success: '#4CAF50',      // Light Green
    warning: '#FFC107',      // Yellow
    danger: '#F44336',       // Red
    light: '#F5F5F5',        // Light Gray
    dark: '#212121',         // Dark Gray
    white: '#FFFFFF',
    headerBg: '#E8F5E9',     // Light Green Background
    rowAlt: '#FAFAFA'        // Alternating Row Color
  },
  fonts: {
    title: 'Montserrat',
    body: 'Roboto',
    mono: 'Roboto Mono'
  },
  year: new Date().getFullYear()
};

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];

const PLATFORMS = [
  { name: 'Etsy', icon: '🛍️', color: '#F56400' },
  { name: 'eBay', icon: '📦', color: '#E53238' },
  { name: 'Poshmark', icon: '👗', color: '#7B2D26' },
  { name: 'Depop', icon: '🛒', color: '#FF2300' },
  { name: 'Amazon FBA', icon: '📦', color: '#FF9900' },
  { name: 'Mercari', icon: '🏪', color: '#4DC3FA' },
  { name: 'Facebook Marketplace', icon: '📘', color: '#1877F2' },
  { name: 'Freelance', icon: '💼', color: '#6366F1' },
  { name: 'Uber/Lyft', icon: '🚗', color: '#000000' },
  { name: 'DoorDash/Delivery', icon: '🍔', color: '#FF3008' },
  { name: 'Content Creation', icon: '📹', color: '#FF0000' },
  { name: 'Consulting', icon: '🎯', color: '#9C27B0' },
  { name: 'Rental Income', icon: '🏠', color: '#795548' },
  { name: 'Investments/Dividends', icon: '📈', color: '#00BCD4' },
  { name: 'Other', icon: '💰', color: '#607D8B' }
];

const EXPENSE_CATEGORIES = [
  { name: 'Supplies & Materials', scheduleC: 'Line 22', deductible: true },
  { name: 'Shipping & Postage', scheduleC: 'Line 27a', deductible: true },
  { name: 'Packaging', scheduleC: 'Line 22', deductible: true },
  { name: 'Platform Fees', scheduleC: 'Line 10', deductible: true },
  { name: 'Payment Processing Fees', scheduleC: 'Line 10', deductible: true },
  { name: 'Advertising & Marketing', scheduleC: 'Line 8', deductible: true },
  { name: 'Software & Subscriptions', scheduleC: 'Line 27a', deductible: true },
  { name: 'Equipment & Tools', scheduleC: 'Line 13', deductible: true },
  { name: 'Office Supplies', scheduleC: 'Line 18', deductible: true },
  { name: 'Vehicle/Mileage', scheduleC: 'Line 9', deductible: true },
  { name: 'Home Office', scheduleC: 'Line 30', deductible: true },
  { name: 'Professional Services', scheduleC: 'Line 17', deductible: true },
  { name: 'Insurance', scheduleC: 'Line 15', deductible: true },
  { name: 'Education & Training', scheduleC: 'Line 27a', deductible: true },
  { name: 'Travel', scheduleC: 'Line 24a', deductible: true },
  { name: 'Meals (50%)', scheduleC: 'Line 24b', deductible: true },
  { name: 'Inventory/COGS', scheduleC: 'Part III', deductible: true },
  { name: 'Other Deductible', scheduleC: 'Line 27a', deductible: true },
  { name: 'Personal/Non-Deductible', scheduleC: 'N/A', deductible: false }
];

// ============================================================
// MAIN FUNCTION - Creates the entire tracker
// ============================================================

function createSideHustleEmpireTracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Show progress
  const ui = SpreadsheetApp.getUi();
  ui.alert('🚀 Creating Your Side Hustle Empire Tracker',
           'This will take about 30 seconds. Click OK to begin!',
           ui.ButtonSet.OK);

  // Delete default sheet if it exists
  try {
    const defaultSheet = ss.getSheetByName('Sheet1');
    if (defaultSheet) {
      ss.deleteSheet(defaultSheet);
    }
  } catch (e) {}

  // Create all sheets
  createDashboardSheet(ss);
  createIncomeTrackerSheet(ss);
  createExpenseTrackerSheet(ss);
  createTaxCenterSheet(ss);
  createGoalsSheet(ss);
  createMileageTrackerSheet(ss);
  createInventorySheet(ss);
  createSettingsSheet(ss);
  createInstructionsSheet(ss);

  // Set Dashboard as active
  ss.setActiveSheet(ss.getSheetByName('📊 Dashboard'));

  // Create custom menu
  createCustomMenu();

  ui.alert('✅ Success!',
           'Your Side Hustle Empire Tracker is ready!\n\n' +
           '📖 Start with the "📋 Instructions" tab for a quick tour.\n' +
           '⚙️ Customize your settings in the "⚙️ Settings" tab.\n' +
           '💰 Begin tracking income in the "💵 Income Tracker" tab.\n\n' +
           'Happy hustling! 🚀',
           ui.ButtonSet.OK);
}

// ============================================================
// DASHBOARD SHEET
// ============================================================

function createDashboardSheet(ss) {
  let sheet = ss.getSheetByName('📊 Dashboard');
  if (!sheet) {
    sheet = ss.insertSheet('📊 Dashboard');
  }
  ss.setActiveSheet(sheet);
  ss.moveActiveSheet(1);

  sheet.clear();
  sheet.setColumnWidths(1, 12, 120);

  // Header
  sheet.getRange('A1:L1').merge()
    .setValue('🚀 SIDE HUSTLE EMPIRE TRACKER')
    .setBackground(CONFIG.colors.primary)
    .setFontColor(CONFIG.colors.white)
    .setFontSize(24)
    .setFontWeight('bold')
    .setHorizontalAlignment('center')
    .setVerticalAlignment('middle');
  sheet.setRowHeight(1, 60);

  // Subtitle
  sheet.getRange('A2:L2').merge()
    .setValue(`📅 ${CONFIG.year} Financial Dashboard | Track • Analyze • Grow`)
    .setBackground(CONFIG.colors.headerBg)
    .setFontSize(12)
    .setHorizontalAlignment('center');

  // KPI Cards Row
  const kpiRow = 4;
  const kpis = [
    { title: '💰 TOTAL INCOME', formula: `='💵 Income Tracker'!G2`, color: CONFIG.colors.success },
    { title: '💸 TOTAL EXPENSES', formula: `='💳 Expenses'!F2`, color: CONFIG.colors.danger },
    { title: '📈 NET PROFIT', formula: `='💵 Income Tracker'!G2-'💳 Expenses'!F2`, color: CONFIG.colors.primary },
    { title: '🎯 GOAL PROGRESS', formula: `=IFERROR('🎯 Goals'!C3/'🎯 Goals'!B3,0)`, color: CONFIG.colors.secondary }
  ];

  let col = 1;
  kpis.forEach((kpi, index) => {
    // KPI Card
    sheet.getRange(kpiRow, col, 1, 3).merge()
      .setValue(kpi.title)
      .setBackground(kpi.color)
      .setFontColor(CONFIG.colors.white)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');

    sheet.getRange(kpiRow + 1, col, 1, 3).merge()
      .setFormula(kpi.formula)
      .setNumberFormat(index === 3 ? '0.0%' : '$#,##0.00')
      .setFontSize(20)
      .setFontWeight('bold')
      .setHorizontalAlignment('center')
      .setBackground(CONFIG.colors.light);

    col += 3;
  });

  // Monthly Summary Section
  const monthlyRow = 8;
  sheet.getRange(monthlyRow, 1, 1, 12).merge()
    .setValue('📅 MONTHLY INCOME SUMMARY')
    .setBackground(CONFIG.colors.secondary)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  // Month headers
  MONTHS.forEach((month, index) => {
    sheet.getRange(monthlyRow + 1, index + 1)
      .setValue(month.substring(0, 3))
      .setBackground(CONFIG.colors.headerBg)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');

    // Monthly income formula
    sheet.getRange(monthlyRow + 2, index + 1)
      .setFormula(`=SUMIF('💵 Income Tracker'!$B:$B,">="&DATE(${CONFIG.year},${index + 1},1),'💵 Income Tracker'!$E:$E)-SUMIF('💵 Income Tracker'!$B:$B,">="&DATE(${CONFIG.year},${index + 2},1),'💵 Income Tracker'!$E:$E)`)
      .setNumberFormat('$#,##0')
      .setHorizontalAlignment('center');
  });

  // Platform Performance Section
  const platformRow = 12;
  sheet.getRange(platformRow, 1, 1, 6).merge()
    .setValue('🏆 TOP PLATFORMS BY REVENUE')
    .setBackground(CONFIG.colors.accent)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  sheet.getRange(platformRow + 1, 1).setValue('Platform').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(platformRow + 1, 2).setValue('Revenue').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(platformRow + 1, 3).setValue('Transactions').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(platformRow + 1, 4).setValue('Avg Sale').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(platformRow + 1, 5).setValue('% of Total').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  // Platform data rows
  for (let i = 0; i < 5; i++) {
    const row = platformRow + 2 + i;
    sheet.getRange(row, 1).setFormula(`=IFERROR(INDEX(SORT(UNIQUE('💵 Income Tracker'!C:C),SUMIF('💵 Income Tracker'!C:C,UNIQUE('💵 Income Tracker'!C:C),'💵 Income Tracker'!E:E),FALSE),${i + 1},1),"")`);
    sheet.getRange(row, 2).setFormula(`=IFERROR(SUMIF('💵 Income Tracker'!C:C,A${row},'💵 Income Tracker'!E:E),0)`).setNumberFormat('$#,##0.00');
    sheet.getRange(row, 3).setFormula(`=IFERROR(COUNTIF('💵 Income Tracker'!C:C,A${row}),0)`);
    sheet.getRange(row, 4).setFormula(`=IFERROR(B${row}/C${row},0)`).setNumberFormat('$#,##0.00');
    sheet.getRange(row, 5).setFormula(`=IFERROR(B${row}/$B$5,0)`).setNumberFormat('0.0%');
  }

  // Expense Breakdown Section
  const expenseRow = 12;
  sheet.getRange(expenseRow, 7, 1, 6).merge()
    .setValue('💳 EXPENSE BREAKDOWN')
    .setBackground(CONFIG.colors.danger)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  sheet.getRange(expenseRow + 1, 7).setValue('Category').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(expenseRow + 1, 8).setValue('Amount').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(expenseRow + 1, 9).setValue('% of Total').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(expenseRow + 1, 10).setValue('Deductible').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  // Expense data rows
  for (let i = 0; i < 5; i++) {
    const row = expenseRow + 2 + i;
    sheet.getRange(row, 7).setFormula(`=IFERROR(INDEX(SORT(UNIQUE('💳 Expenses'!C:C),SUMIF('💳 Expenses'!C:C,UNIQUE('💳 Expenses'!C:C),'💳 Expenses'!D:D),FALSE),${i + 1},1),"")`);
    sheet.getRange(row, 8).setFormula(`=IFERROR(SUMIF('💳 Expenses'!C:C,G${row},'💳 Expenses'!D:D),0)`).setNumberFormat('$#,##0.00');
    sheet.getRange(row, 9).setFormula(`=IFERROR(H${row}/$H$5,0)`).setNumberFormat('0.0%');
    sheet.getRange(row, 10).setValue('✅').setHorizontalAlignment('center');
  }

  // Quick Stats Section
  const statsRow = 20;
  sheet.getRange(statsRow, 1, 1, 12).merge()
    .setValue('📊 QUICK STATS')
    .setBackground(CONFIG.colors.dark)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  const stats = [
    { label: 'Total Transactions', formula: `=COUNTA('💵 Income Tracker'!A:A)-1` },
    { label: 'Average Sale', formula: `=IFERROR(AVERAGE('💵 Income Tracker'!E:E),0)` },
    { label: 'Best Month', formula: `=INDEX($A$9:$L$9,1,MATCH(MAX($A$10:$L$10),$A$10:$L$10,0))` },
    { label: 'Best Day Revenue', formula: `=MAX('💵 Income Tracker'!E:E)` },
    { label: 'Active Platforms', formula: `=COUNTA(UNIQUE('💵 Income Tracker'!C:C))-1` },
    { label: 'Tax Liability Est.', formula: `=('💵 Income Tracker'!G2-'💳 Expenses'!F2)*0.25` }
  ];

  stats.forEach((stat, index) => {
    const col = (index * 2) + 1;
    sheet.getRange(statsRow + 1, col, 1, 2).merge()
      .setValue(stat.label)
      .setBackground(CONFIG.colors.light)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
    sheet.getRange(statsRow + 2, col, 1, 2).merge()
      .setFormula(stat.formula)
      .setNumberFormat(index === 1 || index === 3 || index === 5 ? '$#,##0.00' : '0')
      .setFontSize(14)
      .setHorizontalAlignment('center');
  });

  // Footer
  sheet.getRange(24, 1, 1, 12).merge()
    .setValue('💡 Tip: Update your income and expenses regularly for accurate tracking. Check the Tax Center quarterly!')
    .setFontStyle('italic')
    .setFontColor(CONFIG.colors.dark)
    .setBackground(CONFIG.colors.headerBg)
    .setHorizontalAlignment('center');

  // Freeze header row
  sheet.setFrozenRows(2);
}

// ============================================================
// INCOME TRACKER SHEET
// ============================================================

function createIncomeTrackerSheet(ss) {
  let sheet = ss.getSheetByName('💵 Income Tracker');
  if (!sheet) {
    sheet = ss.insertSheet('💵 Income Tracker');
  }

  sheet.clear();

  // Set column widths
  sheet.setColumnWidth(1, 40);   // #
  sheet.setColumnWidth(2, 100);  // Date
  sheet.setColumnWidth(3, 150);  // Platform
  sheet.setColumnWidth(4, 250);  // Description
  sheet.setColumnWidth(5, 100);  // Gross Amount
  sheet.setColumnWidth(6, 100);  // Fees
  sheet.setColumnWidth(7, 100);  // Net Amount
  sheet.setColumnWidth(8, 150);  // Notes

  // Total row at top
  sheet.getRange('F1').setValue('TOTAL:').setFontWeight('bold').setHorizontalAlignment('right');
  sheet.getRange('G1').setValue('$0.00').setFontWeight('bold').setBackground(CONFIG.colors.success).setFontColor(CONFIG.colors.white);
  sheet.getRange('G2').setFormula('=SUM(G4:G1000)').setNumberFormat('$#,##0.00').setFontWeight('bold').setFontSize(14);

  // Header row
  const headers = ['#', 'Date', 'Platform', 'Description', 'Gross $', 'Fees $', 'Net $', 'Notes'];
  headers.forEach((header, index) => {
    sheet.getRange(3, index + 1)
      .setValue(header)
      .setBackground(CONFIG.colors.primary)
      .setFontColor(CONFIG.colors.white)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
  });

  // Data validation for Platform column
  const platformNames = PLATFORMS.map(p => `${p.icon} ${p.name}`);
  const platformRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(platformNames, true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('C4:C1000').setDataValidation(platformRule);

  // Date validation
  const dateRule = SpreadsheetApp.newDataValidation()
    .requireDate()
    .setAllowInvalid(false)
    .build();
  sheet.getRange('B4:B1000').setDataValidation(dateRule);

  // Auto-numbering formula
  for (let i = 4; i <= 100; i++) {
    sheet.getRange(i, 1).setFormula(`=IF(B${i}="","",ROW()-3)`);
  }

  // Net amount formula (Gross - Fees)
  for (let i = 4; i <= 100; i++) {
    sheet.getRange(i, 7).setFormula(`=IF(E${i}="","",E${i}-F${i})`);
  }

  // Number formatting
  sheet.getRange('E4:G1000').setNumberFormat('$#,##0.00');
  sheet.getRange('B4:B1000').setNumberFormat('MM/DD/YYYY');

  // Sample data
  const sampleData = [
    [new Date(), '🛍️ Etsy', 'Printable Wall Art - Mountain Scene', 15.99, 2.40],
    [new Date(Date.now() - 86400000), '📦 eBay', 'Vintage Camera Lens', 45.00, 5.85],
    [new Date(Date.now() - 172800000), '👗 Poshmark', 'Designer Handbag', 89.00, 17.80],
    [new Date(Date.now() - 259200000), '💼 Freelance', 'Logo Design Project', 250.00, 0]
  ];

  sampleData.forEach((row, index) => {
    sheet.getRange(4 + index, 2).setValue(row[0]);
    sheet.getRange(4 + index, 3).setValue(row[1]);
    sheet.getRange(4 + index, 4).setValue(row[2]);
    sheet.getRange(4 + index, 5).setValue(row[3]);
    sheet.getRange(4 + index, 6).setValue(row[4]);
  });

  // Alternating row colors
  const rowColors = sheet.getRange('A4:H100');
  for (let i = 0; i < 97; i++) {
    if (i % 2 === 0) {
      sheet.getRange(4 + i, 1, 1, 8).setBackground(CONFIG.colors.rowAlt);
    }
  }

  // Freeze header
  sheet.setFrozenRows(3);

  // Add conditional formatting for high-value sales
  const highValueRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThan(100)
    .setBackground('#C8E6C9')
    .setRanges([sheet.getRange('E4:E1000')])
    .build();
  sheet.setConditionalFormatRules([highValueRule]);
}

// ============================================================
// EXPENSE TRACKER SHEET
// ============================================================

function createExpenseTrackerSheet(ss) {
  let sheet = ss.getSheetByName('💳 Expenses');
  if (!sheet) {
    sheet = ss.insertSheet('💳 Expenses');
  }

  sheet.clear();

  // Set column widths
  sheet.setColumnWidth(1, 40);   // #
  sheet.setColumnWidth(2, 100);  // Date
  sheet.setColumnWidth(3, 180);  // Category
  sheet.setColumnWidth(4, 100);  // Amount
  sheet.setColumnWidth(5, 250);  // Description
  sheet.setColumnWidth(6, 100);  // Schedule C Line
  sheet.setColumnWidth(7, 80);   // Deductible
  sheet.setColumnWidth(8, 150);  // Receipt/Reference

  // Total row at top
  sheet.getRange('E1').setValue('TOTAL EXPENSES:').setFontWeight('bold').setHorizontalAlignment('right');
  sheet.getRange('F2').setFormula('=SUM(D4:D1000)').setNumberFormat('$#,##0.00').setFontWeight('bold').setFontSize(14).setBackground(CONFIG.colors.danger).setFontColor(CONFIG.colors.white);

  sheet.getRange('G1').setValue('TAX DEDUCTIBLE:').setFontWeight('bold').setHorizontalAlignment('right');
  sheet.getRange('H2').setFormula('=SUMIF(G4:G1000,"✅",D4:D1000)').setNumberFormat('$#,##0.00').setFontWeight('bold').setFontSize(14).setBackground(CONFIG.colors.success).setFontColor(CONFIG.colors.white);

  // Header row
  const headers = ['#', 'Date', 'Category', 'Amount', 'Description', 'Schedule C', 'Deduct?', 'Receipt Ref'];
  headers.forEach((header, index) => {
    sheet.getRange(3, index + 1)
      .setValue(header)
      .setBackground(CONFIG.colors.danger)
      .setFontColor(CONFIG.colors.white)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
  });

  // Data validation for Category column
  const categoryNames = EXPENSE_CATEGORIES.map(c => c.name);
  const categoryRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(categoryNames, true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('C4:C1000').setDataValidation(categoryRule);

  // Auto-populate Schedule C line and Deductible based on Category
  for (let i = 4; i <= 100; i++) {
    // Schedule C line lookup
    const lookupFormula = `=IF(C${i}="","",VLOOKUP(C${i},{'⚙️ Settings'!A16:A34,'⚙️ Settings'!B16:B34},2,FALSE))`;
    sheet.getRange(i, 6).setFormula(lookupFormula);

    // Deductible lookup
    const deductFormula = `=IF(C${i}="","",IF(VLOOKUP(C${i},{'⚙️ Settings'!A16:A34,'⚙️ Settings'!C16:C34},2,FALSE),"✅","❌"))`;
    sheet.getRange(i, 7).setFormula(deductFormula);

    // Auto-number
    sheet.getRange(i, 1).setFormula(`=IF(B${i}="","",ROW()-3)`);
  }

  // Number formatting
  sheet.getRange('D4:D1000').setNumberFormat('$#,##0.00');
  sheet.getRange('B4:B1000').setNumberFormat('MM/DD/YYYY');

  // Sample data
  const sampleExpenses = [
    [new Date(), 'Supplies & Materials', 45.99, 'Craft supplies from Michaels'],
    [new Date(Date.now() - 86400000), 'Shipping & Postage', 23.50, 'USPS Priority Mail supplies'],
    [new Date(Date.now() - 172800000), 'Platform Fees', 15.00, 'Etsy listing fees - January'],
    [new Date(Date.now() - 259200000), 'Software & Subscriptions', 12.99, 'Canva Pro monthly']
  ];

  sampleExpenses.forEach((row, index) => {
    sheet.getRange(4 + index, 2).setValue(row[0]);
    sheet.getRange(4 + index, 3).setValue(row[1]);
    sheet.getRange(4 + index, 4).setValue(row[2]);
    sheet.getRange(4 + index, 5).setValue(row[3]);
  });

  // Freeze header
  sheet.setFrozenRows(3);
}

// ============================================================
// TAX CENTER SHEET
// ============================================================

function createTaxCenterSheet(ss) {
  let sheet = ss.getSheetByName('🧾 Tax Center');
  if (!sheet) {
    sheet = ss.insertSheet('🧾 Tax Center');
  }

  sheet.clear();
  sheet.setColumnWidths(1, 8, 150);

  // Header
  sheet.getRange('A1:H1').merge()
    .setValue('🧾 TAX CENTER - Schedule C Preparation')
    .setBackground(CONFIG.colors.secondary)
    .setFontColor(CONFIG.colors.white)
    .setFontSize(20)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');
  sheet.setRowHeight(1, 50);

  // Tax Year Selection
  sheet.getRange('A3').setValue('Tax Year:').setFontWeight('bold');
  sheet.getRange('B3').setValue(CONFIG.year);

  // Summary Section
  sheet.getRange('A5:D5').merge()
    .setValue('📊 INCOME & PROFIT SUMMARY')
    .setBackground(CONFIG.colors.primary)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  const summaryData = [
    ['Gross Income (Line 1)', `='💵 Income Tracker'!G2`, '$#,##0.00'],
    ['Total Expenses', `='💳 Expenses'!F2`, '$#,##0.00'],
    ['Tentative Profit (Line 29)', `=B6-B7`, '$#,##0.00'],
    ['Home Office Deduction (Line 30)', `=0`, '$#,##0.00'],
    ['Net Profit (Line 31)', `=B8-B9`, '$#,##0.00']
  ];

  summaryData.forEach((row, index) => {
    sheet.getRange(6 + index, 1).setValue(row[0]).setBackground(CONFIG.colors.light);
    sheet.getRange(6 + index, 2).setFormula(row[1]).setNumberFormat(row[2]).setFontWeight('bold');
  });

  // Quarterly Tax Estimates
  sheet.getRange('A13:D13').merge()
    .setValue('📅 QUARTERLY ESTIMATED TAX PAYMENTS')
    .setBackground(CONFIG.colors.accent)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  sheet.getRange('A14').setValue('Quarter').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('B14').setValue('Due Date').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('C14').setValue('Est. Tax Due').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('D14').setValue('Paid?').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  const quarters = [
    ['Q1 (Jan-Mar)', 'April 15', `=B10*0.25*'⚙️ Settings'!B6`],
    ['Q2 (Apr-May)', 'June 15', `=B10*0.25*'⚙️ Settings'!B6`],
    ['Q3 (Jun-Aug)', 'September 15', `=B10*0.25*'⚙️ Settings'!B6`],
    ['Q4 (Sep-Dec)', 'January 15', `=B10*0.25*'⚙️ Settings'!B6`]
  ];

  quarters.forEach((q, index) => {
    sheet.getRange(15 + index, 1).setValue(q[0]);
    sheet.getRange(15 + index, 2).setValue(q[1]);
    sheet.getRange(15 + index, 3).setFormula(q[2]).setNumberFormat('$#,##0.00');

    const checkbox = SpreadsheetApp.newDataValidation()
      .requireCheckbox()
      .build();
    sheet.getRange(15 + index, 4).setDataValidation(checkbox);
  });

  // Schedule C Expense Breakdown
  sheet.getRange('F5:H5').merge()
    .setValue('📋 SCHEDULE C EXPENSE BREAKDOWN')
    .setBackground(CONFIG.colors.danger)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  sheet.getRange('F6').setValue('Line').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('G6').setValue('Description').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('H6').setValue('Amount').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  const scheduleC = [
    ['Line 8', 'Advertising', `=SUMIF('💳 Expenses'!C:C,"Advertising & Marketing",'💳 Expenses'!D:D)`],
    ['Line 9', 'Car & Truck Expenses', `=SUMIF('💳 Expenses'!C:C,"Vehicle/Mileage",'💳 Expenses'!D:D)+'🚗 Mileage'!E2`],
    ['Line 10', 'Commissions & Fees', `=SUMIF('💳 Expenses'!C:C,"Platform Fees",'💳 Expenses'!D:D)+SUMIF('💳 Expenses'!C:C,"Payment Processing Fees",'💳 Expenses'!D:D)`],
    ['Line 13', 'Depreciation', `=SUMIF('💳 Expenses'!C:C,"Equipment & Tools",'💳 Expenses'!D:D)`],
    ['Line 15', 'Insurance', `=SUMIF('💳 Expenses'!C:C,"Insurance",'💳 Expenses'!D:D)`],
    ['Line 17', 'Legal & Professional', `=SUMIF('💳 Expenses'!C:C,"Professional Services",'💳 Expenses'!D:D)`],
    ['Line 18', 'Office Expense', `=SUMIF('💳 Expenses'!C:C,"Office Supplies",'💳 Expenses'!D:D)`],
    ['Line 22', 'Supplies', `=SUMIF('💳 Expenses'!C:C,"Supplies & Materials",'💳 Expenses'!D:D)+SUMIF('💳 Expenses'!C:C,"Packaging",'💳 Expenses'!D:D)`],
    ['Line 24a', 'Travel', `=SUMIF('💳 Expenses'!C:C,"Travel",'💳 Expenses'!D:D)`],
    ['Line 24b', 'Meals (50%)', `=SUMIF('💳 Expenses'!C:C,"Meals (50%)",'💳 Expenses'!D:D)*0.5`],
    ['Line 27a', 'Other Expenses', `=SUMIF('💳 Expenses'!C:C,"Software & Subscriptions",'💳 Expenses'!D:D)+SUMIF('💳 Expenses'!C:C,"Shipping & Postage",'💳 Expenses'!D:D)+SUMIF('💳 Expenses'!C:C,"Education & Training",'💳 Expenses'!D:D)`]
  ];

  scheduleC.forEach((line, index) => {
    sheet.getRange(7 + index, 6).setValue(line[0]).setBackground(index % 2 === 0 ? CONFIG.colors.light : CONFIG.colors.white);
    sheet.getRange(7 + index, 7).setValue(line[1]).setBackground(index % 2 === 0 ? CONFIG.colors.light : CONFIG.colors.white);
    sheet.getRange(7 + index, 8).setFormula(line[2]).setNumberFormat('$#,##0.00').setBackground(index % 2 === 0 ? CONFIG.colors.light : CONFIG.colors.white);
  });

  // Total line
  sheet.getRange(18, 6, 1, 2).merge().setValue('TOTAL EXPENSES').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(18, 8).setFormula('=SUM(H7:H17)').setNumberFormat('$#,##0.00').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  // Tax Tips Section
  sheet.getRange('A21:H21').merge()
    .setValue('💡 TAX TIPS & REMINDERS')
    .setBackground(CONFIG.colors.dark)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  const tips = [
    '✓ Keep all receipts for expenses over $75 (IRS requirement)',
    '✓ Track mileage with date, destination, purpose, and miles',
    '✓ Self-employment tax is 15.3% on net profit (Social Security + Medicare)',
    '✓ You may need to pay quarterly estimated taxes if you owe >$1,000',
    '✓ Consider a home office deduction if you use space regularly and exclusively for business',
    '✓ Consult a tax professional for personalized advice'
  ];

  tips.forEach((tip, index) => {
    sheet.getRange(22 + index, 1, 1, 8).merge().setValue(tip).setFontStyle('italic');
  });
}

// ============================================================
// GOALS SHEET
// ============================================================

function createGoalsSheet(ss) {
  let sheet = ss.getSheetByName('🎯 Goals');
  if (!sheet) {
    sheet = ss.insertSheet('🎯 Goals');
  }

  sheet.clear();
  sheet.setColumnWidths(1, 6, 150);

  // Header
  sheet.getRange('A1:F1').merge()
    .setValue('🎯 GOALS & PROGRESS TRACKER')
    .setBackground(CONFIG.colors.accent)
    .setFontColor(CONFIG.colors.white)
    .setFontSize(20)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');
  sheet.setRowHeight(1, 50);

  // Annual Goal Section
  sheet.getRange('A3:C3').merge()
    .setValue('🏆 ANNUAL INCOME GOAL')
    .setBackground(CONFIG.colors.primary)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  sheet.getRange('A4').setValue('Goal').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('B4').setValue('Current').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('C4').setValue('Progress').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  sheet.getRange('A5').setValue('Annual Goal:').setBackground(CONFIG.colors.light);
  sheet.getRange('B3').setValue(10000).setNumberFormat('$#,##0'); // Default goal
  sheet.getRange('C3').setFormula(`='💵 Income Tracker'!G2`).setNumberFormat('$#,##0');
  sheet.getRange('A6').setValue('Progress:').setBackground(CONFIG.colors.light);
  sheet.getRange('B6').setFormula('=IFERROR(C3/B3,0)').setNumberFormat('0.0%').setFontSize(16).setFontWeight('bold');

  // Monthly Goals
  sheet.getRange('A8:F8').merge()
    .setValue('📅 MONTHLY GOALS & TRACKING')
    .setBackground(CONFIG.colors.secondary)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  const goalHeaders = ['Month', 'Goal', 'Actual', 'Difference', 'Status', 'Notes'];
  goalHeaders.forEach((header, index) => {
    sheet.getRange(9, index + 1)
      .setValue(header)
      .setBackground(CONFIG.colors.headerBg)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
  });

  MONTHS.forEach((month, index) => {
    const row = 10 + index;
    sheet.getRange(row, 1).setValue(month);
    sheet.getRange(row, 2).setValue(833.33).setNumberFormat('$#,##0'); // $10k/12 months
    sheet.getRange(row, 3).setFormula(`=SUMIF('💵 Income Tracker'!B:B,">="&DATE(${CONFIG.year},${index + 1},1),'💵 Income Tracker'!G:G)-SUMIF('💵 Income Tracker'!B:B,">="&DATE(${CONFIG.year},${index + 2},1),'💵 Income Tracker'!G:G)`).setNumberFormat('$#,##0');
    sheet.getRange(row, 4).setFormula(`=C${row}-B${row}`).setNumberFormat('$#,##0');
    sheet.getRange(row, 5).setFormula(`=IF(C${row}>=B${row},"🎉 CRUSHED IT!",IF(C${row}>=B${row}*0.8,"👍 Almost There!",IF(C${row}>0,"📈 Keep Going!","⏳ Not Started")))`);

    // Alternating row colors
    if (index % 2 === 0) {
      sheet.getRange(row, 1, 1, 6).setBackground(CONFIG.colors.rowAlt);
    }
  });

  // Totals row
  sheet.getRange(22, 1).setValue('TOTAL').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(22, 2).setFormula('=SUM(B10:B21)').setNumberFormat('$#,##0').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(22, 3).setFormula('=SUM(C10:C21)').setNumberFormat('$#,##0').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange(22, 4).setFormula('=SUM(D10:D21)').setNumberFormat('$#,##0').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  // Milestones Section
  sheet.getRange('A25:F25').merge()
    .setValue('🏅 MILESTONE ACHIEVEMENTS')
    .setBackground(CONFIG.colors.success)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  const milestones = [
    ['$100', 'First $100!', `=IF('💵 Income Tracker'!G2>=100,"🏆","⬜")`],
    ['$500', 'Halfway to $1K!', `=IF('💵 Income Tracker'!G2>=500,"🏆","⬜")`],
    ['$1,000', 'Four Figure Hustler!', `=IF('💵 Income Tracker'!G2>=1000,"🏆","⬜")`],
    ['$2,500', 'Serious Side Income!', `=IF('💵 Income Tracker'!G2>=2500,"🏆","⬜")`],
    ['$5,000', 'Half Year Salary!', `=IF('💵 Income Tracker'!G2>=5000,"🏆","⬜")`],
    ['$10,000', 'Side Hustle Master!', `=IF('💵 Income Tracker'!G2>=10000,"🏆","⬜")`],
    ['$25,000', 'Empire Builder!', `=IF('💵 Income Tracker'!G2>=25000,"🏆","⬜")`],
    ['$50,000', 'LEGENDARY STATUS!', `=IF('💵 Income Tracker'!G2>=50000,"🏆","⬜")`]
  ];

  milestones.forEach((m, index) => {
    const row = 26 + Math.floor(index / 4);
    const col = ((index % 4) * 2) + 1;
    sheet.getRange(row, col).setValue(`${m[0]} - ${m[1]}`).setFontSize(10);
    sheet.getRange(row, col + 1).setFormula(m[2]).setFontSize(14).setHorizontalAlignment('center');
  });
}

// ============================================================
// MILEAGE TRACKER SHEET
// ============================================================

function createMileageTrackerSheet(ss) {
  let sheet = ss.getSheetByName('🚗 Mileage');
  if (!sheet) {
    sheet = ss.insertSheet('🚗 Mileage');
  }

  sheet.clear();

  // Set column widths
  sheet.setColumnWidth(1, 40);
  sheet.setColumnWidth(2, 100);
  sheet.setColumnWidth(3, 200);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 80);
  sheet.setColumnWidth(6, 100);
  sheet.setColumnWidth(7, 150);

  // Header
  sheet.getRange('A1:G1').merge()
    .setValue('🚗 BUSINESS MILEAGE TRACKER')
    .setBackground('#424242')
    .setFontColor(CONFIG.colors.white)
    .setFontSize(18)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');
  sheet.setRowHeight(1, 45);

  // IRS Rate and Total
  sheet.getRange('A2').setValue('IRS Rate (2025):').setFontWeight('bold');
  sheet.getRange('B2').setValue(0.67).setNumberFormat('$0.000').setBackground(CONFIG.colors.light);
  sheet.getRange('C2').setValue('Total Miles:').setFontWeight('bold');
  sheet.getRange('D2').setFormula('=SUM(E5:E1000)').setFontWeight('bold').setBackground(CONFIG.colors.light);
  sheet.getRange('E2').setFormula('=D2*B2').setNumberFormat('$#,##0.00').setFontWeight('bold').setFontSize(14).setBackground(CONFIG.colors.success).setFontColor(CONFIG.colors.white);
  sheet.getRange('F2').setValue('← Tax Deduction').setFontStyle('italic');

  // Column headers
  const headers = ['#', 'Date', 'Purpose/Destination', 'Business Reason', 'Miles', 'Value', 'Notes'];
  headers.forEach((header, index) => {
    sheet.getRange(4, index + 1)
      .setValue(header)
      .setBackground('#424242')
      .setFontColor(CONFIG.colors.white)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
  });

  // Auto formulas
  for (let i = 5; i <= 100; i++) {
    sheet.getRange(i, 1).setFormula(`=IF(B${i}="","",ROW()-4)`);
    sheet.getRange(i, 6).setFormula(`=IF(E${i}="","",E${i}*$B$2)`);
  }

  // Number formatting
  sheet.getRange('B5:B1000').setNumberFormat('MM/DD/YYYY');
  sheet.getRange('E5:E1000').setNumberFormat('0.0');
  sheet.getRange('F5:F1000').setNumberFormat('$#,##0.00');

  // Sample data
  const sampleMileage = [
    [new Date(), 'Post Office - Ship Orders', 'Shipping customer orders', 8.5],
    [new Date(Date.now() - 86400000), 'Michaels - Supplies', 'Purchase craft supplies', 12.3],
    [new Date(Date.now() - 172800000), 'Bank - Business Deposit', 'Deposit business income', 5.2]
  ];

  sampleMileage.forEach((row, index) => {
    sheet.getRange(5 + index, 2).setValue(row[0]);
    sheet.getRange(5 + index, 3).setValue(row[1]);
    sheet.getRange(5 + index, 4).setValue(row[2]);
    sheet.getRange(5 + index, 5).setValue(row[3]);
  });

  // Freeze header
  sheet.setFrozenRows(4);

  // Tip
  sheet.getRange('A100:G100').merge()
    .setValue('💡 IRS requires: Date, Destination, Business Purpose, Miles for each trip. Keep this log accurate!')
    .setFontStyle('italic')
    .setBackground(CONFIG.colors.light);
}

// ============================================================
// INVENTORY SHEET
// ============================================================

function createInventorySheet(ss) {
  let sheet = ss.getSheetByName('📦 Inventory');
  if (!sheet) {
    sheet = ss.insertSheet('📦 Inventory');
  }

  sheet.clear();

  // Set column widths
  const widths = [40, 150, 100, 80, 80, 80, 100, 80, 150];
  widths.forEach((w, i) => sheet.setColumnWidth(i + 1, w));

  // Header
  sheet.getRange('A1:I1').merge()
    .setValue('📦 INVENTORY TRACKER')
    .setBackground('#8E24AA')
    .setFontColor(CONFIG.colors.white)
    .setFontSize(18)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');
  sheet.setRowHeight(1, 45);

  // Summary row
  sheet.getRange('A2').setValue('Total Items:').setFontWeight('bold');
  sheet.getRange('B2').setFormula('=COUNTA(B5:B1000)').setFontWeight('bold');
  sheet.getRange('C2').setValue('Total Value:').setFontWeight('bold');
  sheet.getRange('D2').setFormula('=SUMPRODUCT(D5:D1000,E5:E1000)').setNumberFormat('$#,##0.00').setFontWeight('bold').setBackground(CONFIG.colors.success).setFontColor(CONFIG.colors.white);
  sheet.getRange('F2').setValue('Potential Revenue:').setFontWeight('bold');
  sheet.getRange('G2').setFormula('=SUMPRODUCT(F5:F1000,E5:E1000)').setNumberFormat('$#,##0.00').setFontWeight('bold').setBackground(CONFIG.colors.accent).setFontColor(CONFIG.colors.white);

  // Column headers
  const headers = ['#', 'Item Name', 'Platform', 'Cost', 'Qty', 'List Price', 'Status', 'Days Listed', 'Notes'];
  headers.forEach((header, index) => {
    sheet.getRange(4, index + 1)
      .setValue(header)
      .setBackground('#8E24AA')
      .setFontColor(CONFIG.colors.white)
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
  });

  // Data validations
  const platformNames = PLATFORMS.map(p => `${p.icon} ${p.name}`);
  const platformRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(platformNames, true)
    .build();
  sheet.getRange('C5:C1000').setDataValidation(platformRule);

  const statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['📋 Draft', '✅ Listed', '⏸️ Paused', '💰 Sold', '↩️ Returned'], true)
    .build();
  sheet.getRange('G5:G1000').setDataValidation(statusRule);

  // Auto-number
  for (let i = 5; i <= 100; i++) {
    sheet.getRange(i, 1).setFormula(`=IF(B${i}="","",ROW()-4)`);
  }

  // Number formatting
  sheet.getRange('D5:D1000').setNumberFormat('$#,##0.00');
  sheet.getRange('F5:F1000').setNumberFormat('$#,##0.00');

  // Freeze header
  sheet.setFrozenRows(4);
}

// ============================================================
// SETTINGS SHEET
// ============================================================

function createSettingsSheet(ss) {
  let sheet = ss.getSheetByName('⚙️ Settings');
  if (!sheet) {
    sheet = ss.insertSheet('⚙️ Settings');
  }

  sheet.clear();
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 100);

  // Header
  sheet.getRange('A1:C1').merge()
    .setValue('⚙️ SETTINGS & CONFIGURATION')
    .setBackground(CONFIG.colors.dark)
    .setFontColor(CONFIG.colors.white)
    .setFontSize(18)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');
  sheet.setRowHeight(1, 45);

  // User Settings Section
  sheet.getRange('A3:C3').merge()
    .setValue('👤 USER SETTINGS')
    .setBackground(CONFIG.colors.secondary)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold');

  const userSettings = [
    ['Business Name', 'My Side Hustle Empire'],
    ['Tax Year', CONFIG.year],
    ['Estimated Tax Rate (%)', 0.25],
    ['Annual Income Goal', 10000],
    ['IRS Mileage Rate', 0.67]
  ];

  userSettings.forEach((setting, index) => {
    sheet.getRange(4 + index, 1).setValue(setting[0]).setBackground(CONFIG.colors.light);
    sheet.getRange(4 + index, 2).setValue(setting[1]);
    if (index === 2) sheet.getRange(4 + index, 2).setNumberFormat('0%');
    if (index === 3) sheet.getRange(4 + index, 2).setNumberFormat('$#,##0');
    if (index === 4) sheet.getRange(4 + index, 2).setNumberFormat('$0.000');
  });

  // Platform Settings
  sheet.getRange('A11:C11').merge()
    .setValue('🛍️ PLATFORM SETTINGS')
    .setBackground(CONFIG.colors.accent)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold');

  sheet.getRange('A12').setValue('Platform').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('B12').setValue('Avg Fee %').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('C12').setValue('Active?').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  const platformFees = [
    ['Etsy', 0.15, true],
    ['eBay', 0.13, true],
    ['Poshmark', 0.20, true],
    ['Depop', 0.10, false],
    ['Amazon FBA', 0.15, false]
  ];

  platformFees.forEach((p, index) => {
    sheet.getRange(13 + index, 1).setValue(p[0]);
    sheet.getRange(13 + index, 2).setValue(p[1]).setNumberFormat('0%');
    const checkbox = SpreadsheetApp.newDataValidation().requireCheckbox().build();
    sheet.getRange(13 + index, 3).setDataValidation(checkbox).setValue(p[2]);
  });

  // Expense Categories Reference
  sheet.getRange('A20:C20').merge()
    .setValue('📋 EXPENSE CATEGORY REFERENCE')
    .setBackground(CONFIG.colors.danger)
    .setFontColor(CONFIG.colors.white)
    .setFontWeight('bold');

  sheet.getRange('A21').setValue('Category').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('B21').setValue('Schedule C').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('C21').setValue('Deductible').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  // Start expense categories at row 16 for formula lookups
  sheet.getRange('A15').setValue('Category').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('B15').setValue('Schedule C').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);
  sheet.getRange('C15').setValue('Deductible').setFontWeight('bold').setBackground(CONFIG.colors.headerBg);

  EXPENSE_CATEGORIES.forEach((cat, index) => {
    sheet.getRange(16 + index, 1).setValue(cat.name);
    sheet.getRange(16 + index, 2).setValue(cat.scheduleC);
    sheet.getRange(16 + index, 3).setValue(cat.deductible);
  });
}

// ============================================================
// INSTRUCTIONS SHEET
// ============================================================

function createInstructionsSheet(ss) {
  let sheet = ss.getSheetByName('📋 Instructions');
  if (!sheet) {
    sheet = ss.insertSheet('📋 Instructions');
  }

  sheet.clear();
  sheet.setColumnWidth(1, 800);

  const instructions = `
🚀 WELCOME TO YOUR SIDE HUSTLE EMPIRE TRACKER!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 QUICK START GUIDE

1️⃣ CONFIGURE SETTINGS (⚙️ Settings tab)
   • Enter your business name
   • Set your tax rate (typically 25-30% for self-employed)
   • Set your annual income goal
   • Check which platforms you use

2️⃣ TRACK YOUR INCOME (💵 Income Tracker tab)
   • Enter each sale with date, platform, description, and amount
   • Fees are automatically calculated for net profit
   • Use the dropdown to select your selling platform

3️⃣ LOG YOUR EXPENSES (💳 Expenses tab)
   • Record every business expense with date and category
   • Schedule C line and deductibility auto-populate
   • Keep receipts for amounts over $75

4️⃣ TRACK MILEAGE (🚗 Mileage tab)
   • Log every business-related trip
   • IRS requires: date, destination, purpose, miles
   • Deduction calculated automatically at current IRS rate

5️⃣ MONITOR YOUR DASHBOARD (📊 Dashboard tab)
   • See your total income, expenses, and profit at a glance
   • Track monthly trends and platform performance
   • Celebrate your progress!

6️⃣ PREPARE FOR TAXES (🧾 Tax Center tab)
   • Quarterly estimated tax amounts calculated
   • Schedule C expense breakdown ready for filing
   • Tips for maximizing deductions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 PRO TIPS

✓ Update your tracker weekly for best results
✓ Take photos of receipts and store in Google Drive
✓ Review quarterly tax estimates every 3 months
✓ Back up your spreadsheet regularly (File > Download)
✓ Use filters to analyze specific date ranges or platforms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT DISCLAIMERS

• This tracker is for organizational purposes only
• Consult a tax professional for tax advice
• Keep original receipts for all business expenses
• Tax laws vary by location - verify local requirements

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 NEED HELP?

Thank you for purchasing the Side Hustle Empire Tracker!
For support, please contact: [Your Support Email]

Happy hustling! 🎉
  `;

  sheet.getRange('A1').setValue(instructions)
    .setFontFamily('Roboto')
    .setFontSize(11)
    .setVerticalAlignment('top')
    .setWrap(true);

  sheet.setRowHeight(1, 1200);
}

// ============================================================
// CUSTOM MENU
// ============================================================

function createCustomMenu() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🚀 Side Hustle Tools')
    .addItem('📊 Refresh Dashboard', 'refreshDashboard')
    .addItem('📅 Add New Month Goals', 'addNewMonthGoals')
    .addSeparator()
    .addItem('🧾 Generate Tax Report', 'generateTaxReport')
    .addItem('📈 Export Year Summary', 'exportYearSummary')
    .addSeparator()
    .addItem('❓ Help & Instructions', 'showHelp')
    .addToUi();
}

function onOpen() {
  createCustomMenu();
}

function refreshDashboard() {
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName('📊 Dashboard').activate();
  SpreadsheetApp.flush();
  SpreadsheetApp.getUi().alert('Dashboard refreshed! 📊');
}

function addNewMonthGoals() {
  SpreadsheetApp.getUi().alert('Navigate to the Goals tab to update your monthly targets! 🎯');
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName('🎯 Goals').activate();
}

function generateTaxReport() {
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName('🧾 Tax Center').activate();
  SpreadsheetApp.getUi().alert('Your Tax Center is ready! Review the Schedule C breakdown. 🧾');
}

function exportYearSummary() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const income = ss.getSheetByName('💵 Income Tracker').getRange('G2').getValue();
  const expenses = ss.getSheetByName('💳 Expenses').getRange('F2').getValue();
  const profit = income - expenses;

  SpreadsheetApp.getUi().alert(
    '📈 Year Summary\n\n' +
    `Total Income: $${income.toFixed(2)}\n` +
    `Total Expenses: $${expenses.toFixed(2)}\n` +
    `Net Profit: $${profit.toFixed(2)}\n\n` +
    'For a detailed PDF export, use File > Download > PDF'
  );
}

function showHelp() {
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName('📋 Instructions').activate();
}
