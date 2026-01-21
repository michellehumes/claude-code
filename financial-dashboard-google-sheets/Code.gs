/**
 * Financial Dashboard Builder for Google Sheets
 * Creates 11 tabs with automatic calculations, formatting, and data import
 *
 * Instructions:
 * 1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw/edit
 * 2. Go to Extensions > Apps Script
 * 3. Delete any existing code and paste this entire script
 * 4. Save the script (Ctrl+S or Cmd+S)
 * 5. Run the function: buildFinancialDashboard()
 * 6. Grant necessary permissions when prompted
 * 7. After the script runs, manually import your CSV data into the Transactions tab
 */

// Main function to build the entire dashboard
function buildFinancialDashboard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Delete any existing sheets except Sheet1
  const sheets = ss.getSheets();
  for (let i = sheets.length - 1; i >= 0; i--) {
    ss.deleteSheet(sheets[i]);
  }

  // Create all tabs in reverse order (so they appear in correct order)
  Logger.log('Creating Dashboard tab...');
  createDashboardTab(ss);

  Logger.log('Creating Calendar View tab...');
  createCalendarViewTab(ss);

  Logger.log('Creating Health Dashboard tab...');
  createHealthDashboardTab(ss);

  Logger.log('Creating Gift Tracker tab...');
  createGiftTrackerTab(ss);

  Logger.log('Creating Master Tasks tab...');
  createMasterTasksTab(ss);

  Logger.log('Creating Spending by Merchant tab...');
  createSpendingByMerchantTab(ss);

  Logger.log('Creating Monthly Summary tab...');
  createMonthlySummaryTab(ss);

  Logger.log('Creating Spending by Category tab...');
  createSpendingByCategoryTab(ss);

  Logger.log('Creating Budget Master tab...');
  createBudgetMasterTab(ss);

  Logger.log('Creating Credit Cards tab...');
  createCreditCardsTab(ss);

  Logger.log('Creating Transactions tab...');
  createTransactionsTab(ss);

  // Move Dashboard to first position
  const dashboard = ss.getSheetByName('📋 Dashboard');
  ss.setActiveSheet(dashboard);
  ss.moveActiveSheet(1);

  Logger.log('Financial Dashboard build complete!');
  SpreadsheetApp.getUi().alert('Financial Dashboard Created!\\n\\nAll 11 tabs have been created.\\n\\nNext step: Import your CSV data into the "📊 Transactions" tab:\\n1. Open the Transactions tab\\n2. File > Import > Upload your CSV file\\n3. Choose "Replace data at selected cell"\\n4. Select cell A2\\n5. Click Import');
}

// Helper function to format headers
function formatHeaders(sheet, headerRow, numColumns, headerColor = '#4A90E2') {
  const headerRange = sheet.getRange(headerRow, 1, 1, numColumns);
  headerRange.setBackground(headerColor)
    .setFontColor('#FFFFFF')
    .setFontWeight('bold')
    .setHorizontalAlignment('center')
    .setVerticalAlignment('middle');
  sheet.setFrozenRows(headerRow);
}

// Helper function to apply filters
function applyFilters(sheet, headerRow, numColumns) {
  const range = sheet.getRange(headerRow, 1, 1, numColumns);
  range.createFilter();
}

// TAB 1: Transactions
function createTransactionsTab(ss) {
  const sheet = ss.insertSheet('📊 Transactions');

  // Set headers
  const headers = ['Date', 'Merchant', 'Category', 'Account', 'Original Statement', 'Notes', 'Amount', 'Tags', 'Owner'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length);

  // Apply filters
  applyFilters(sheet, 1, headers.length);

  // Set column widths
  sheet.setColumnWidth(1, 100);  // Date
  sheet.setColumnWidth(2, 200);  // Merchant
  sheet.setColumnWidth(3, 150);  // Category
  sheet.setColumnWidth(4, 200);  // Account
  sheet.setColumnWidth(5, 300);  // Original Statement
  sheet.setColumnWidth(6, 150);  // Notes
  sheet.setColumnWidth(7, 120);  // Amount
  sheet.setColumnWidth(8, 100);  // Tags
  sheet.setColumnWidth(9, 100);  // Owner

  // Format Amount column as currency
  sheet.getRange('G:G').setNumberFormat('$#,##0.00');

  // Format Date column
  sheet.getRange('A:A').setNumberFormat('yyyy-mm-dd');

  // Add instruction in cell A2
  sheet.getRange('A2').setValue('IMPORT YOUR CSV DATA HERE: File > Import > Upload > Replace data at selected cell (A2)');
  sheet.getRange('A2:I2').mergeAcross().setBackground('#FFF3CD').setFontColor('#856404').setFontWeight('bold');
}

// TAB 2: Credit Cards
function createCreditCardsTab(ss) {
  const sheet = ss.insertSheet('💳 Credit Cards');

  // Set headers
  const headers = ['Account', 'Current Balance', 'Total Spent This Month', 'Total Spent This Year', 'Last Transaction Date'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length);

  // Add sample account rows (these will be populated with formulas)
  const sampleData = [
    ['Venture (...4522)', '=SUMIF(\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!G:G)',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A2)'],
    ['Michelle\'s Sapphire Reserve (...1041)', '=SUMIF(\'📊 Transactions\'!D:D,A3,\'📊 Transactions\'!G:G)',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A3,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A3,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A3)'],
    ['Gray\'s Amex Gold Card (...2003)', '=SUMIF(\'📊 Transactions\'!D:D,A4,\'📊 Transactions\'!G:G)',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A4,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A4,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A4)'],
    ['Michelle\'s Freedom Unlimited (...9759)', '=SUMIF(\'📊 Transactions\'!D:D,A5,\'📊 Transactions\'!G:G)',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A5,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A5,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A5)'],
    ['Target Circle Card (...2828)', '=SUMIF(\'📊 Transactions\'!D:D,A6,\'📊 Transactions\'!G:G)',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A6,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A6,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A6)'],
    ['CHECKING (...4688)', '=SUMIF(\'📊 Transactions\'!D:D,A7,\'📊 Transactions\'!G:G)',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A7,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A7,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A7)'],
    ['Bugs Checking (...3045)', '=SUMIF(\'📊 Transactions\'!D:D,A8,\'📊 Transactions\'!G:G)',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A8,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A8,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A8)']
  ];

  sheet.getRange(2, 1, sampleData.length, headers.length).setValues(sampleData);

  // Format currency columns
  sheet.getRange('B:D').setNumberFormat('$#,##0.00');

  // Format date column
  sheet.getRange('E:E').setNumberFormat('yyyy-mm-dd');

  // Set column widths
  sheet.setColumnWidth(1, 300);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 180);
  sheet.setColumnWidth(4, 180);
  sheet.setColumnWidth(5, 180);

  // Add note
  sheet.getRange('A10').setValue('NOTE: Add more accounts as needed. Copy formulas from row above.');
  sheet.getRange('A10:E10').mergeAcross().setBackground('#E8F4F8').setFontStyle('italic');
}

// TAB 3: Budget Master
function createBudgetMasterTab(ss) {
  const sheet = ss.insertSheet('📊 Budget Master');

  // Set headers
  const headers = ['Category', 'Budget Amount', 'Actual Spent', 'Remaining', '% Used'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length);

  // Add categories with formulas
  const categories = [
    ['Rent', 7500, '=SUMIF(\'📊 Transactions\'!C:C,A2,\'📊 Transactions\'!G:G)', '=B2-C2', '=IF(B2=0,0,C2/B2)'],
    ['Hotel', 1000, '=SUMIF(\'📊 Transactions\'!C:C,A3,\'📊 Transactions\'!G:G)', '=B3-C3', '=IF(B3=0,0,C3/B3)'],
    ['Restaurants & Bars', 2000, '=SUMIF(\'📊 Transactions\'!C:C,A4,\'📊 Transactions\'!G:G)', '=B4-C4', '=IF(B4=0,0,C4/B4)'],
    ['Shopping', 1500, '=SUMIF(\'📊 Transactions\'!C:C,A5,\'📊 Transactions\'!G:G)', '=B5-C5', '=IF(B5=0,0,C5/B5)'],
    ['Subscriptions', 500, '=SUMIF(\'📊 Transactions\'!C:C,A6,\'📊 Transactions\'!G:G)', '=B6-C6', '=IF(B6=0,0,C6/B6)'],
    ['Music', 20, '=SUMIF(\'📊 Transactions\'!C:C,A7,\'📊 Transactions\'!G:G)', '=B7-C7', '=IF(B7=0,0,C7/B7)'],
    ['Car Insurance', 300, '=SUMIF(\'📊 Transactions\'!C:C,A8,\'📊 Transactions\'!G:G)', '=B8-C8', '=IF(B8=0,0,C8/B8)'],
    ['Car Payment', 800, '=SUMIF(\'📊 Transactions\'!C:C,A9,\'📊 Transactions\'!G:G)', '=B9-C9', '=IF(B9=0,0,C9/B9)'],
    ['Taxi & Ride Shares', 200, '=SUMIF(\'📊 Transactions\'!C:C,A10,\'📊 Transactions\'!G:G)', '=B10-C10', '=IF(B10=0,0,C10/B10)'],
    ['Transfer', 0, '=SUMIF(\'📊 Transactions\'!C:C,A11,\'📊 Transactions\'!G:G)', '=B11-C11', '=IF(B11=0,0,C11/B11)'],
    ['Delivery & Takeout', 800, '=SUMIF(\'📊 Transactions\'!C:C,A12,\'📊 Transactions\'!G:G)', '=B12-C12', '=IF(B12=0,0,C12/B12)']
  ];

  sheet.getRange(2, 1, categories.length, headers.length).setValues(categories);

  // Format currency columns
  sheet.getRange('B:D').setNumberFormat('$#,##0.00');

  // Format percentage column
  sheet.getRange('E:E').setNumberFormat('0.0%');

  // Set column widths
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 100);

  // Add conditional formatting for % Used column
  const percentRange = sheet.getRange('E2:E100');
  const rule1 = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThan(1)
    .setBackground('#F4C7C3')
    .setRanges([percentRange])
    .build();
  const rule2 = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberBetween(0.8, 1)
    .setBackground('#FCE8B2')
    .setRanges([percentRange])
    .build();
  const rule3 = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(0.8)
    .setBackground('#B7E1CD')
    .setRanges([percentRange])
    .build();

  sheet.setConditionalFormatRules([rule1, rule2, rule3]);

  // Add totals row
  const totalRow = categories.length + 2;
  sheet.getRange(totalRow, 1).setValue('TOTAL');
  sheet.getRange(totalRow, 2).setFormula('=SUM(B2:B' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 3).setFormula('=SUM(C2:C' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 4).setFormula('=SUM(D2:D' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 1, 1, 5).setBackground('#E8F4F8').setFontWeight('bold');
}

// TAB 4: Spending by Category
function createSpendingByCategoryTab(ss) {
  const sheet = ss.insertSheet('📈 Spending by Category');

  // Set headers
  const headers = ['Category', 'This Month', 'Last Month', '3-Month Avg', 'YTD Total', '% of Total'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length);

  // Add categories with formulas
  const categories = [
    ['Rent',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A2,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A2,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A2,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A2,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E2/$F$13)'],
    ['Hotel',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A3,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A3,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A3,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A3,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E3/$F$13)'],
    ['Restaurants & Bars',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A4,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A4,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A4,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A4,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E4/$F$13)'],
    ['Shopping',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A5,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A5,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A5,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A5,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E5/$F$13)'],
    ['Subscriptions',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A6,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A6,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A6,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A6,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E6/$F$13)'],
    ['Music',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A7,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A7,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A7,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A7,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E7/$F$13)'],
    ['Car Insurance',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A8,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A8,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A8,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A8,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E8/$F$13)'],
    ['Car Payment',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A9,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A9,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A9,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A9,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E9/$F$13)'],
    ['Taxi & Ride Shares',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A10,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A10,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A10,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A10,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E10/$F$13)'],
    ['Transfer',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A11,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A11,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A11,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A11,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E11/$F$13)'],
    ['Delivery & Takeout',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A12,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A12,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-2)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-1))',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A12,\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-3)+1)/3',
     '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!C:C,A12,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))',
     '=IF($F$13=0,0,E12/$F$13)']
  ];

  sheet.getRange(2, 1, categories.length, headers.length).setValues(categories);

  // Add totals row
  const totalRow = categories.length + 2;
  sheet.getRange(totalRow, 1).setValue('TOTAL');
  sheet.getRange(totalRow, 2).setFormula('=SUM(B2:B' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 3).setFormula('=SUM(C2:C' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 4).setFormula('=SUM(D2:D' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 5).setFormula('=SUM(E2:E' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 1, 1, 6).setBackground('#E8F4F8').setFontWeight('bold');

  // Format currency columns
  sheet.getRange('B:E').setNumberFormat('$#,##0.00');

  // Format percentage column
  sheet.getRange('F:F').setNumberFormat('0.0%');

  // Set column widths
  sheet.setColumnWidth(1, 200);
  for (let i = 2; i <= 6; i++) {
    sheet.setColumnWidth(i, 130);
  }
}

// TAB 5: Monthly Summary
function createMonthlySummaryTab(ss) {
  const sheet = ss.insertSheet('💰 Monthly Summary');

  // Set headers
  const headers = ['Month', 'Total Income', 'Total Expenses', 'Net', 'Savings Rate %'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length);

  // Add months (last 12 months)
  const monthsData = [];
  for (let i = 11; i >= 0; i--) {
    const row = i + 2;
    monthsData.push([
      '=TEXT(EOMONTH(TODAY(),-' + i + '),"YYYY-MM")',
      '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-' + (i + 1) + ')+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-' + i + '))',
      '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-' + (i + 1) + ')+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),-' + i + '))',
      '=B' + row + '-C' + row,
      '=IF(B' + row + '=0,0,D' + row + '/B' + row + ')'
    ]);
  }

  sheet.getRange(2, 1, monthsData.length, headers.length).setValues(monthsData);

  // Add totals row
  const totalRow = monthsData.length + 2;
  sheet.getRange(totalRow, 1).setValue('TOTAL / AVG');
  sheet.getRange(totalRow, 2).setFormula('=SUM(B2:B' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 3).setFormula('=SUM(C2:C' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 4).setFormula('=SUM(D2:D' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 5).setFormula('=AVERAGE(E2:E' + (totalRow - 1) + ')');
  sheet.getRange(totalRow, 1, 1, 5).setBackground('#E8F4F8').setFontWeight('bold');

  // Format currency columns
  sheet.getRange('B:D').setNumberFormat('$#,##0.00');

  // Format percentage column
  sheet.getRange('E:E').setNumberFormat('0.0%');

  // Set column widths
  sheet.setColumnWidth(1, 120);
  for (let i = 2; i <= 5; i++) {
    sheet.setColumnWidth(i, 150);
  }

  // Add conditional formatting for Savings Rate
  const savingsRange = sheet.getRange('E2:E' + (totalRow - 1));
  const rule1 = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThanOrEqualTo(0.2)
    .setBackground('#B7E1CD')
    .setRanges([savingsRange])
    .build();
  const rule2 = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberBetween(0.1, 0.2)
    .setBackground('#FCE8B2')
    .setRanges([savingsRange])
    .build();
  const rule3 = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(0.1)
    .setBackground('#F4C7C3')
    .setRanges([savingsRange])
    .build();

  sheet.setConditionalFormatRules([rule1, rule2, rule3]);
}

// TAB 6: Spending by Merchant
function createSpendingByMerchantTab(ss) {
  const sheet = ss.insertSheet('📊 Spending by Merchant');

  // Set headers
  const headers = ['Merchant', 'Transaction Count', 'Total Spent', 'Avg Transaction', 'Category'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length);

  // Add note about manual creation
  sheet.getRange('A2').setValue('NOTE: This tab requires manual creation using Pivot Table or QUERY function.');
  sheet.getRange('A3').setValue('Steps to create:');
  sheet.getRange('A4').setValue('1. Go to Data > Pivot Table');
  sheet.getRange('A5').setValue('2. Select data from Transactions tab');
  sheet.getRange('A6').setValue('3. Add Merchant as Row');
  sheet.getRange('A7').setValue('4. Add Amount as Value (SUM and COUNT)');
  sheet.getRange('A8').setValue('5. Sort by Total Spent descending');
  sheet.getRange('A9').setValue('6. Add Category as additional column');

  // Alternative: Add some sample merchants with formulas
  const merchants = [
    ['BILL PAY 12 Harbor', '=COUNTIF(\'📊 Transactions\'!B:B,A11)', '=-SUMIF(\'📊 Transactions\'!B:B,A11,\'📊 Transactions\'!G:G)', '=C11/B11', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A11,\'📊 Transactions\'!B:B,0))'],
    ['Lord Camden Inn', '=COUNTIF(\'📊 Transactions\'!B:B,A12)', '=-SUMIF(\'📊 Transactions\'!B:B,A12,\'📊 Transactions\'!G:G)', '=C12/B12', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A12,\'📊 Transactions\'!B:B,0))'],
    ['Woodstock Inn & Resort', '=COUNTIF(\'📊 Transactions\'!B:B,A13)', '=-SUMIF(\'📊 Transactions\'!B:B,A13,\'📊 Transactions\'!G:G)', '=C13/B13', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A13,\'📊 Transactions\'!B:B,0))'],
    ['Spotify', '=COUNTIF(\'📊 Transactions\'!B:B,A14)', '=-SUMIF(\'📊 Transactions\'!B:B,A14,\'📊 Transactions\'!G:G)', '=C14/B14', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A14,\'📊 Transactions\'!B:B,0))'],
    ['Geico', '=COUNTIF(\'📊 Transactions\'!B:B,A15)', '=-SUMIF(\'📊 Transactions\'!B:B,A15,\'📊 Transactions\'!G:G)', '=C15/B15', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A15,\'📊 Transactions\'!B:B,0))'],
    ['BMW', '=COUNTIF(\'📊 Transactions\'!B:B,A16)', '=-SUMIF(\'📊 Transactions\'!B:B,A16,\'📊 Transactions\'!G:G)', '=C16/B16', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A16,\'📊 Transactions\'!B:B,0))'],
    ['Target', '=COUNTIF(\'📊 Transactions\'!B:B,A17)', '=-SUMIF(\'📊 Transactions\'!B:B,A17,\'📊 Transactions\'!G:G)', '=C17/B17', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A17,\'📊 Transactions\'!B:B,0))'],
    ['OpenAI', '=COUNTIF(\'📊 Transactions\'!B:B,A18)', '=-SUMIF(\'📊 Transactions\'!B:B,A18,\'📊 Transactions\'!G:G)', '=C18/B18', '=INDEX(\'📊 Transactions\'!C:C,MATCH(A18,\'📊 Transactions\'!B:B,0))']
  ];

  sheet.getRange(11, 1, merchants.length, headers.length).setValues(merchants);

  // Format currency columns
  sheet.getRange('C:D').setNumberFormat('$#,##0.00');

  // Set column widths
  sheet.setColumnWidth(1, 250);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 130);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 180);

  // Add note styling
  sheet.getRange('A2:A9').setBackground('#FFF3CD').setFontStyle('italic');
}

// TAB 7: Master Tasks
function createMasterTasksTab(ss) {
  const sheet = ss.insertSheet('✅ Master Tasks');

  // Set headers
  const headers = ['✓', 'Task', 'Priority', 'Status', 'Due Date', 'Category', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length, '#6AA84F');

  // Apply filters
  applyFilters(sheet, 1, headers.length);

  // Add sample data
  const sampleTasks = [
    ['☐', 'Review monthly budget', 'High', 'Not Started', '', 'Finance', ''],
    ['☐', 'Update spending categories', 'Medium', 'Not Started', '', 'Finance', ''],
    ['☐', 'Set financial goals for Q1', 'High', 'Not Started', '', 'Finance', ''],
    ['☐', 'Review credit card rewards', 'Low', 'Not Started', '', 'Finance', '']
  ];

  sheet.getRange(2, 1, sampleTasks.length, headers.length).setValues(sampleTasks);

  // Format date column
  sheet.getRange('E:E').setNumberFormat('yyyy-mm-dd');

  // Set column widths
  sheet.setColumnWidth(1, 50);
  sheet.setColumnWidth(2, 300);
  sheet.setColumnWidth(3, 100);
  sheet.setColumnWidth(4, 120);
  sheet.setColumnWidth(5, 120);
  sheet.setColumnWidth(6, 120);
  sheet.setColumnWidth(7, 250);

  // Add data validation for Priority
  const priorityRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['High', 'Medium', 'Low'])
    .setAllowInvalid(false)
    .build();
  sheet.getRange('C2:C100').setDataValidation(priorityRule);

  // Add data validation for Status
  const statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Not Started', 'In Progress', 'Completed', 'On Hold'])
    .setAllowInvalid(false)
    .build();
  sheet.getRange('D2:D100').setDataValidation(statusRule);

  // Add conditional formatting for Status
  const statusRange = sheet.getRange('D2:D100');
  const rule1 = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Completed')
    .setBackground('#B7E1CD')
    .setRanges([statusRange])
    .build();
  const rule2 = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('In Progress')
    .setBackground('#FCE8B2')
    .setRanges([statusRange])
    .build();
  const rule3 = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('On Hold')
    .setBackground('#F4C7C3')
    .setRanges([statusRange])
    .build();

  sheet.setConditionalFormatRules([rule1, rule2, rule3]);
}

// TAB 8: Gift Tracker
function createGiftTrackerTab(ss) {
  const sheet = ss.insertSheet('🎁 Gift Tracker');

  // Set headers
  const headers = ['Person', 'Occasion', 'Date', 'Gift Idea', 'Budget', 'Actual Cost', 'Purchased?', 'Store/Link', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  formatHeaders(sheet, 1, headers.length, '#E69138');

  // Apply filters
  applyFilters(sheet, 1, headers.length);

  // Add sample data
  const sampleGifts = [
    ['', 'Birthday', '', '', 100, '', '☐', '', ''],
    ['', 'Anniversary', '', '', 150, '', '☐', '', ''],
    ['', 'Holiday', '', '', 50, '', '☐', '', '']
  ];

  sheet.getRange(2, 1, sampleGifts.length, headers.length).setValues(sampleGifts);

  // Format currency columns
  sheet.getRange('E:F').setNumberFormat('$#,##0.00');

  // Format date column
  sheet.getRange('C:C').setNumberFormat('yyyy-mm-dd');

  // Set column widths
  sheet.setColumnWidth(1, 150);
  sheet.setColumnWidth(2, 120);
  sheet.setColumnWidth(3, 100);
  sheet.setColumnWidth(4, 200);
  sheet.setColumnWidth(5, 100);
  sheet.setColumnWidth(6, 100);
  sheet.setColumnWidth(7, 100);
  sheet.setColumnWidth(8, 200);
  sheet.setColumnWidth(9, 250);
}

// TAB 9: Health Dashboard
function createHealthDashboardTab(ss) {
  const sheet = ss.insertSheet('🩺 Health Dashboard');

  // Section 1: Weight Log
  sheet.getRange('A1').setValue('WEIGHT LOG');
  sheet.getRange('A1:C1').mergeAcross().setBackground('#93C47D').setFontColor('#FFFFFF').setFontWeight('bold').setHorizontalAlignment('center');

  const weightHeaders = ['Date', 'Weight (lbs)', 'Notes'];
  sheet.getRange(2, 1, 1, weightHeaders.length).setValues([weightHeaders]);
  formatHeaders(sheet, 2, weightHeaders.length, '#6AA84F');

  // Add sample weight data
  const sampleWeight = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
  ];
  sheet.getRange(3, 1, sampleWeight.length, weightHeaders.length).setValues(sampleWeight);

  // Section 2: Workouts
  sheet.getRange('A8').setValue('WORKOUTS');
  sheet.getRange('A8:D8').mergeAcross().setBackground('#93C47D').setFontColor('#FFFFFF').setFontWeight('bold').setHorizontalAlignment('center');

  const workoutHeaders = ['Date', 'Type', 'Duration (min)', 'Notes'];
  sheet.getRange(9, 1, 1, workoutHeaders.length).setValues([workoutHeaders]);
  formatHeaders(sheet, 9, workoutHeaders.length, '#6AA84F');

  // Add sample workout data
  const sampleWorkout = [
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', '']
  ];
  sheet.getRange(10, 1, sampleWorkout.length, workoutHeaders.length).setValues(sampleWorkout);

  // Section 3: Appointments
  sheet.getRange('A15').setValue('APPOINTMENTS');
  sheet.getRange('A15:E15').mergeAcross().setBackground('#93C47D').setFontColor('#FFFFFF').setFontWeight('bold').setHorizontalAlignment('center');

  const appointmentHeaders = ['Date', 'Provider', 'Type', 'Notes', 'Follow-up'];
  sheet.getRange(16, 1, 1, appointmentHeaders.length).setValues([appointmentHeaders]);
  formatHeaders(sheet, 16, appointmentHeaders.length, '#6AA84F');

  // Add sample appointment data
  const sampleAppointments = [
    ['', '', '', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', '']
  ];
  sheet.getRange(17, 1, sampleAppointments.length, appointmentHeaders.length).setValues(sampleAppointments);

  // Format date columns
  sheet.getRange('A:A').setNumberFormat('yyyy-mm-dd');

  // Set column widths
  sheet.setColumnWidth(1, 120);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 250);
  sheet.setColumnWidth(5, 150);
}

// TAB 10: Calendar View
function createCalendarViewTab(ss) {
  const sheet = ss.insertSheet('📅 Calendar View');

  // Create title
  sheet.getRange('A1').setValue('MONTHLY SPENDING CALENDAR');
  sheet.getRange('A1:G1').mergeAcross().setBackground('#674EA7').setFontColor('#FFFFFF').setFontWeight('bold').setFontSize(14).setHorizontalAlignment('center');

  // Create month selector
  sheet.getRange('A3').setValue('Select Month:');
  sheet.getRange('B3').setValue('=TEXT(TODAY(),"MMMM YYYY")');
  sheet.getRange('A3:B3').setFontWeight('bold');

  // Create calendar headers (days of week)
  const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  sheet.getRange(5, 1, 1, 7).setValues([daysOfWeek]);
  formatHeaders(sheet, 5, 7, '#674EA7');

  // Create calendar grid (5 weeks)
  for (let week = 0; week < 5; week++) {
    for (let day = 0; day < 7; day++) {
      const row = 6 + week * 3;
      const col = day + 1;

      // Day number
      sheet.getRange(row, col).setValue((week * 7 + day + 1).toString());
      sheet.getRange(row, col).setBackground('#F3F3F3').setFontWeight('bold');

      // Daily spending (placeholder formula)
      sheet.getRange(row + 1, col).setValue('$0.00');
      sheet.getRange(row + 1, col).setNumberFormat('$#,##0.00').setFontSize(10);

      // Transaction count
      sheet.getRange(row + 2, col).setValue('0 trans');
      sheet.getRange(row + 2, col).setFontSize(8).setFontStyle('italic');

      // Set cell borders
      const cellRange = sheet.getRange(row, col, 3, 1);
      cellRange.setBorder(true, true, true, true, true, true);
    }
  }

  // Set column widths
  for (let i = 1; i <= 7; i++) {
    sheet.setColumnWidth(i, 130);
  }

  // Add instructions
  sheet.getRange('A22').setValue('NOTE: This is a template. To populate with actual data, you\'ll need to create formulas that match dates to transaction amounts.');
  sheet.getRange('A22:G22').mergeAcross().setBackground('#FFF3CD').setFontStyle('italic').setWrap(true);
}

// TAB 11: Dashboard (Executive Summary)
function createDashboardTab(ss) {
  const sheet = ss.insertSheet('📋 Dashboard');

  // Title
  sheet.getRange('A1').setValue('FINANCIAL DASHBOARD - EXECUTIVE SUMMARY');
  sheet.getRange('A1:F1').mergeAcross().setBackground('#1155CC').setFontColor('#FFFFFF').setFontWeight('bold').setFontSize(16).setHorizontalAlignment('center');

  // Last Updated
  sheet.getRange('A2').setValue('Last Updated:');
  sheet.getRange('B2').setValue('=NOW()');
  sheet.getRange('B2').setNumberFormat('yyyy-mm-dd hh:mm:ss');

  // KEY METRICS SECTION
  sheet.getRange('A4').setValue('KEY METRICS');
  sheet.getRange('A4:F4').mergeAcross().setBackground('#4A90E2').setFontColor('#FFFFFF').setFontWeight('bold').setFontSize(12).setHorizontalAlignment('center');

  const metrics = [
    ['Total Account Balance', '=SUM(\'💳 Credit Cards\'!B:B)', '', 'This Month Spending', '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))'],
    ['This Month Income', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&EOMONTH(TODAY(),-1)+1,\'📊 Transactions\'!A:A,"<="&EOMONTH(TODAY(),0))', '', 'This Month Net', '=B6-E5'],
    ['YTD Spending', '=-SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,"<0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))', '', 'YTD Income', '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!G:G,">0",\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))'],
    ['Savings Rate (This Month)', '=IF(B6=0,0,(B6-E5)/B6)', '', 'Avg Monthly Spending', '=AVERAGE(\'💰 Monthly Summary\'!C:C)']
  ];

  sheet.getRange(5, 1, metrics.length, 5).setValues(metrics);

  // Format metric values
  sheet.getRange('B5:B8').setNumberFormat('$#,##0.00').setFontSize(14).setFontWeight('bold').setBackground('#E8F4F8');
  sheet.getRange('E5:E8').setNumberFormat('$#,##0.00').setFontSize(14).setFontWeight('bold').setBackground('#E8F4F8');
  sheet.getRange('B8').setNumberFormat('0.0%');

  // Format labels
  sheet.getRange('A5:A8').setFontWeight('bold');
  sheet.getRange('D5:D8').setFontWeight('bold');

  // BUDGET STATUS SECTION
  sheet.getRange('A10').setValue('BUDGET STATUS (TOP 5 CATEGORIES)');
  sheet.getRange('A10:F10').mergeAcross().setBackground('#4A90E2').setFontColor('#FFFFFF').setFontWeight('bold').setFontSize(12).setHorizontalAlignment('center');

  const budgetHeaders = ['Category', 'Budget', 'Actual', 'Remaining', '% Used', 'Status'];
  sheet.getRange(11, 1, 1, budgetHeaders.length).setValues([budgetHeaders]);
  formatHeaders(sheet, 11, budgetHeaders.length, '#4A90E2');

  // Pull top 5 budget items
  for (let i = 0; i < 5; i++) {
    const row = 12 + i;
    sheet.getRange(row, 1).setFormula('=IFERROR(\'📊 Budget Master\'!A' + (i + 2) + ',"")');
    sheet.getRange(row, 2).setFormula('=IFERROR(\'📊 Budget Master\'!B' + (i + 2) + ',0)');
    sheet.getRange(row, 3).setFormula('=IFERROR(\'📊 Budget Master\'!C' + (i + 2) + ',0)');
    sheet.getRange(row, 4).setFormula('=IFERROR(\'📊 Budget Master\'!D' + (i + 2) + ',0)');
    sheet.getRange(row, 5).setFormula('=IFERROR(\'📊 Budget Master\'!E' + (i + 2) + ',0)');
    sheet.getRange(row, 6).setFormula('=IF(E' + row + '>1,"Over Budget",IF(E' + row + '>0.8,"Warning","On Track"))');
  }

  // Format budget columns
  sheet.getRange('B12:D16').setNumberFormat('$#,##0.00');
  sheet.getRange('E12:E16').setNumberFormat('0.0%');

  // Add conditional formatting for Status
  const statusRange = sheet.getRange('F12:F16');
  const rule1 = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Over Budget')
    .setBackground('#F4C7C3')
    .setFontColor('#CC0000')
    .setRanges([statusRange])
    .build();
  const rule2 = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Warning')
    .setBackground('#FCE8B2')
    .setFontColor('#F57C00')
    .setRanges([statusRange])
    .build();
  const rule3 = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('On Track')
    .setBackground('#B7E1CD')
    .setFontColor('#38761D')
    .setRanges([statusRange])
    .build();

  sheet.setConditionalFormatRules([rule1, rule2, rule3]);

  // SPENDING TRENDS SECTION
  sheet.getRange('A18').setValue('SPENDING TRENDS (LAST 3 MONTHS)');
  sheet.getRange('A18:F18').mergeAcross().setBackground('#4A90E2').setFontColor('#FFFFFF').setFontWeight('bold').setFontSize(12).setHorizontalAlignment('center');

  const trendHeaders = ['Month', 'Income', 'Expenses', 'Net', 'Savings Rate', 'Trend'];
  sheet.getRange(19, 1, 1, trendHeaders.length).setValues([trendHeaders]);
  formatHeaders(sheet, 19, trendHeaders.length, '#4A90E2');

  // Pull last 3 months from Monthly Summary
  for (let i = 0; i < 3; i++) {
    const row = 20 + i;
    const sourceRow = 12 - i; // Assuming Monthly Summary has 12 months
    sheet.getRange(row, 1).setFormula('=IFERROR(\'💰 Monthly Summary\'!A' + sourceRow + ',"")');
    sheet.getRange(row, 2).setFormula('=IFERROR(\'💰 Monthly Summary\'!B' + sourceRow + ',0)');
    sheet.getRange(row, 3).setFormula('=IFERROR(\'💰 Monthly Summary\'!C' + sourceRow + ',0)');
    sheet.getRange(row, 4).setFormula('=IFERROR(\'💰 Monthly Summary\'!D' + sourceRow + ',0)');
    sheet.getRange(row, 5).setFormula('=IFERROR(\'💰 Monthly Summary\'!E' + sourceRow + ',0)');

    // Trend indicator
    if (i < 2) {
      sheet.getRange(row, 6).setFormula('=IF(C' + row + '=0,"N/A",IF(C' + (row + 1) + '=0,"N/A",IF(C' + row + '<C' + (row + 1) + ',"↓ Lower","↑ Higher")))');
    } else {
      sheet.getRange(row, 6).setValue('--');
    }
  }

  // Format trend columns
  sheet.getRange('B20:D22').setNumberFormat('$#,##0.00');
  sheet.getRange('E20:E22').setNumberFormat('0.0%');

  // Set column widths
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 130);
  sheet.setColumnWidth(3, 130);
  sheet.setColumnWidth(4, 130);
  sheet.setColumnWidth(5, 130);
  sheet.setColumnWidth(6, 130);

  // Add instructions at bottom
  sheet.getRange('A24').setValue('📌 Quick Links: Navigate to other tabs using the sheet tabs at the bottom');
  sheet.getRange('A24:F24').mergeAcross().setBackground('#D9EAD3').setFontStyle('italic').setWrap(true);
}

// Helper function to show completion message
function showCompletionMessage() {
  const ui = SpreadsheetApp.getUi();
  ui.alert(
    'Financial Dashboard Complete!',
    'All 11 tabs have been created successfully.\\n\\n' +
    'Next steps:\\n' +
    '1. Import your CSV data into the "📊 Transactions" tab\\n' +
    '2. Review and adjust budget amounts in "📊 Budget Master"\\n' +
    '3. All other tabs will auto-calculate from your transactions\\n\\n' +
    'The Dashboard tab provides an executive summary of your finances.',
    ui.ButtonSet.OK
  );
}
