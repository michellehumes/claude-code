/**
 * Financial Dashboard Builder
 * This script creates a comprehensive 11-tab financial dashboard in Google Sheets
 *
 * Instructions:
 * 1. Open your Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Delete any existing code and paste this entire script
 * 4. Click the disk icon to save
 * 5. Run the 'setupFinancialDashboard' function
 * 6. Grant necessary permissions when prompted
 * 7. Import your CSV data into the Transactions tab
 */

function setupFinancialDashboard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Delete existing sheets except the first one
  const sheets = ss.getSheets();
  for (let i = sheets.length - 1; i > 0; i--) {
    ss.deleteSheet(sheets[i]);
  }

  // Create all tabs in order
  Logger.log('Creating tabs...');
  createTransactionsTab(ss);
  createCreditCardsTab(ss);
  createBudgetMasterTab(ss);
  createSpendingByCategoryTab(ss);
  createMonthlySummaryTab(ss);
  createSpendingByMerchantTab(ss);
  createMasterTasksTab(ss);
  createGiftTrackerTab(ss);
  createHealthDashboardTab(ss);
  createCalendarViewTab(ss);
  createDashboardTab(ss);

  // Reorder sheets so Dashboard is first
  const dashboard = ss.getSheetByName('📋 Dashboard');
  ss.setActiveSheet(dashboard);
  ss.moveActiveSheet(1);

  Logger.log('Financial Dashboard setup complete!');
  SpreadsheetApp.getUi().alert('Success!', 'Financial Dashboard has been created successfully. Now import your CSV data into the "📊 Transactions" tab.', SpreadsheetApp.getUi().ButtonSet.OK);
}

function createTransactionsTab(ss) {
  let sheet = ss.getSheets()[0];
  sheet.setName('📊 Transactions');
  sheet.clear();

  // Headers
  const headers = ['Date', 'Merchant', 'Category', 'Account', 'Original Statement', 'Notes', 'Amount', 'Tags', 'Owner'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  // Freeze header row
  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 100); // Date
  sheet.setColumnWidth(2, 200); // Merchant
  sheet.setColumnWidth(3, 150); // Category
  sheet.setColumnWidth(4, 180); // Account
  sheet.setColumnWidth(5, 250); // Original Statement
  sheet.setColumnWidth(6, 200); // Notes
  sheet.setColumnWidth(7, 100); // Amount
  sheet.setColumnWidth(8, 100); // Tags
  sheet.setColumnWidth(9, 100); // Owner

  // Add filters
  sheet.getRange(1, 1, 1, headers.length).createFilter();

  // Format Amount column as currency (will apply to all rows)
  sheet.getRange('G:G').setNumberFormat('$#,##0.00');

  // Format Date column
  sheet.getRange('A:A').setNumberFormat('yyyy-mm-dd');

  Logger.log('Transactions tab created');
}

function createCreditCardsTab(ss) {
  const sheet = ss.insertSheet('💳 Credit Cards');

  // Headers
  const headers = ['Account Name', 'Current Balance', 'Total Spent This Month', 'Total Spent This Year', 'Last Transaction Date'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 250);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 180);
  sheet.setColumnWidth(4, 180);
  sheet.setColumnWidth(5, 150);

  // Sample formula structure (row 2) - user will need to add accounts
  // Note: These formulas will need to be adjusted based on actual account names
  const row2Formulas = [
    '', // Account Name - manual entry
    '=SUMIF(\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!G:G)', // Current Balance
    '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1))', // This Month
    '=SUMIFS(\'📊 Transactions\'!G:G,\'📊 Transactions\'!D:D,A2,\'📊 Transactions\'!A:A,">="&DATE(YEAR(TODAY()),1,1))', // This Year
    '=MAXIFS(\'📊 Transactions\'!A:A,\'📊 Transactions\'!D:D,A2)' // Last Transaction
  ];

  sheet.getRange(2, 1, 1, headers.length).setValues([row2Formulas]);

  // Format currency columns
  sheet.getRange('B:D').setNumberFormat('$#,##0.00');
  sheet.getRange('E:E').setNumberFormat('yyyy-mm-dd');

  // Add note about manual entry
  sheet.getRange('A2').setNote('Enter your account names here. The formulas will auto-calculate based on the Transactions tab. Copy row 2 down for additional accounts.');

  Logger.log('Credit Cards tab created');
}

function createBudgetMasterTab(ss) {
  const sheet = ss.insertSheet('📊 Budget Master');

  // Headers
  const headers = ['Category', 'Budget Amount', 'Actual Spent', 'Remaining', '% Used'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 120);

  // Sample formulas for row 2
  const row2Formulas = [
    '', // Category - manual entry
    '', // Budget Amount - manual entry
    '=SUMIF(\'📊 Transactions\'!C:C,A2,\'📊 Transactions\'!G:G)*-1', // Actual Spent (convert negative to positive)
    '=B2-C2', // Remaining
    '=IF(B2=0,0,C2/B2)' // % Used
  ];

  sheet.getRange(2, 1, 1, headers.length).setValues([row2Formulas]);

  // Format currency columns
  sheet.getRange('B:D').setNumberFormat('$#,##0.00');
  sheet.getRange('E:E').setNumberFormat('0.0%');

  // Add conditional formatting for % Used
  const percentRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThan(0.9)
    .setBackground('#F4CCCC')
    .setRanges([sheet.getRange('E2:E1000')])
    .build();

  const rules = sheet.getConditionalFormatRules();
  rules.push(percentRule);
  sheet.setConditionalFormatRules(rules);

  // Add note
  sheet.getRange('A2').setNote('Enter categories from your Transactions tab. Copy row 2 down for additional categories.');

  Logger.log('Budget Master tab created');
}

function createSpendingByCategoryTab(ss) {
  const sheet = ss.insertSheet('📈 Spending by Category');

  // Headers
  const headers = ['Category', 'This Month', 'Last Month', '3-Month Avg', 'YTD Total', '% of Total'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 130);
  sheet.setColumnWidth(3, 130);
  sheet.setColumnWidth(4, 130);
  sheet.setColumnWidth(5, 130);
  sheet.setColumnWidth(6, 120);

  // Sample formulas for row 2
  const thisMonthStart = 'DATE(YEAR(TODAY()),MONTH(TODAY()),1)';
  const lastMonthStart = 'DATE(YEAR(TODAY()),MONTH(TODAY())-1,1)';
  const lastMonthEnd = 'DATE(YEAR(TODAY()),MONTH(TODAY()),1)-1';
  const threeMonthsAgo = 'DATE(YEAR(TODAY()),MONTH(TODAY())-3,1)';
  const yearStart = 'DATE(YEAR(TODAY()),1,1)';

  const row2Formulas = [
    '', // Category - manual entry
    `=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!C:C,A2,'📊 Transactions'!A:A,">="&${thisMonthStart})*-1`,
    `=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!C:C,A2,'📊 Transactions'!A:A,">="&${lastMonthStart},'📊 Transactions'!A:A,"<="&${lastMonthEnd})*-1`,
    `=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!C:C,A2,'📊 Transactions'!A:A,">="&${threeMonthsAgo})*-1/3`,
    `=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!C:C,A2,'📊 Transactions'!A:A,">="&${yearStart})*-1`,
    `=IF(F2=0,0,E2/F2)`
  ];

  sheet.getRange(2, 1, 1, headers.length).setValues([row2Formulas]);

  // Add total row formula in F2 (will calculate total of all expenses)
  sheet.getRange('F2').setFormula(`=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!G:G,"<0",'📊 Transactions'!A:A,">="&${yearStart})*-1`);

  // Format currency columns
  sheet.getRange('B:E').setNumberFormat('$#,##0.00');
  sheet.getRange('F:F').setNumberFormat('0.0%');

  // Add note
  sheet.getRange('A2').setNote('Enter categories from your Transactions tab. Copy row 2 down for additional categories.');

  Logger.log('Spending by Category tab created');
}

function createMonthlySummaryTab(ss) {
  const sheet = ss.insertSheet('💰 Monthly Summary');

  // Headers
  const headers = ['Month', 'Total Income', 'Total Expenses', 'Net', 'Savings Rate %'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 120);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 130);

  // Add sample months and formulas
  const currentYear = new Date().getFullYear();
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  for (let i = 0; i < 12; i++) {
    const row = i + 2;
    const monthNum = i + 1;
    const monthLabel = `${months[i]} ${currentYear}`;
    const monthStart = `DATE(${currentYear},${monthNum},1)`;
    const monthEnd = `DATE(${currentYear},${monthNum}+1,1)-1`;

    sheet.getRange(row, 1).setValue(monthLabel);
    sheet.getRange(row, 2).setFormula(`=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!G:G,">0",'📊 Transactions'!A:A,">="&${monthStart},'📊 Transactions'!A:A,"<="&${monthEnd})`);
    sheet.getRange(row, 3).setFormula(`=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!G:G,"<0",'📊 Transactions'!A:A,">="&${monthStart},'📊 Transactions'!A:A,"<="&${monthEnd})*-1`);
    sheet.getRange(row, 4).setFormula(`=B${row}-C${row}`);
    sheet.getRange(row, 5).setFormula(`=IF(B${row}=0,0,D${row}/B${row})`);
  }

  // Format currency columns
  sheet.getRange('B:D').setNumberFormat('$#,##0.00');
  sheet.getRange('E:E').setNumberFormat('0.0%');

  Logger.log('Monthly Summary tab created');
}

function createSpendingByMerchantTab(ss) {
  const sheet = ss.insertSheet('📊 Spending by Merchant');

  // Headers
  const headers = ['Merchant', 'Transaction Count', 'Total Spent', 'Avg Transaction', 'Category'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 300);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 150);
  sheet.setColumnWidth(5, 150);

  // Sample formulas for row 2
  const row2Formulas = [
    '', // Merchant - manual entry
    '=COUNTIF(\'📊 Transactions\'!B:B,A2)', // Transaction Count
    '=SUMIF(\'📊 Transactions\'!B:B,A2,\'📊 Transactions\'!G:G)*-1', // Total Spent
    '=IF(B2=0,0,C2/B2)', // Avg Transaction
    '=INDEX(\'📊 Transactions\'!C:C,MATCH(A2,\'📊 Transactions\'!B:B,0))' // Category
  ];

  sheet.getRange(2, 1, 1, headers.length).setValues([row2Formulas]);

  // Format currency columns
  sheet.getRange('C:D').setNumberFormat('$#,##0.00');

  // Add note
  sheet.getRange('A2').setNote('Enter merchant names from your Transactions tab. Copy row 2 down for up to 100 merchants. Sort by Total Spent to see top merchants.');

  Logger.log('Spending by Merchant tab created');
}

function createMasterTasksTab(ss) {
  const sheet = ss.insertSheet('✅ Master Tasks');

  // Headers
  const headers = ['✓', 'Task', 'Priority', 'Status', 'Due Date', 'Category', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 50);
  sheet.setColumnWidth(2, 300);
  sheet.setColumnWidth(3, 100);
  sheet.setColumnWidth(4, 120);
  sheet.setColumnWidth(5, 120);
  sheet.setColumnWidth(6, 150);
  sheet.setColumnWidth(7, 250);

  // Add data validation for checkbox column
  const checkboxRange = sheet.getRange('A2:A100');
  const checkboxRule = SpreadsheetApp.newDataValidation()
    .requireCheckbox()
    .build();
  checkboxRange.setDataValidation(checkboxRule);

  // Add data validation for Priority
  const priorityRange = sheet.getRange('C2:C100');
  const priorityRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['High', 'Medium', 'Low'], true)
    .build();
  priorityRange.setDataValidation(priorityRule);

  // Add data validation for Status
  const statusRange = sheet.getRange('D2:D100');
  const statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Not Started', 'In Progress', 'Completed', 'Blocked'], true)
    .build();
  statusRange.setDataValidation(statusRule);

  // Format date column
  sheet.getRange('E:E').setNumberFormat('yyyy-mm-dd');

  // Add sample task
  sheet.getRange(2, 1, 1, 7).setValues([[false, 'Sample Task', 'Medium', 'Not Started', '', 'Personal', 'This is a sample task']]);

  Logger.log('Master Tasks tab created');
}

function createGiftTrackerTab(ss) {
  const sheet = ss.insertSheet('🎁 Gift Tracker');

  // Headers
  const headers = ['Person', 'Occasion', 'Date', 'Gift Idea', 'Budget', 'Actual Cost', 'Purchased?', 'Store/Link', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4A86E8')
            .setFontColor('#FFFFFF')
            .setFontWeight('bold')
            .setHorizontalAlignment('center');

  sheet.setFrozenRows(1);

  // Set column widths
  sheet.setColumnWidth(1, 150);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 120);
  sheet.setColumnWidth(4, 200);
  sheet.setColumnWidth(5, 100);
  sheet.setColumnWidth(6, 100);
  sheet.setColumnWidth(7, 100);
  sheet.setColumnWidth(8, 200);
  sheet.setColumnWidth(9, 250);

  // Add data validation for checkbox column
  const checkboxRange = sheet.getRange('G2:G100');
  const checkboxRule = SpreadsheetApp.newDataValidation()
    .requireCheckbox()
    .build();
  checkboxRange.setDataValidation(checkboxRule);

  // Format currency columns
  sheet.getRange('E:F').setNumberFormat('$#,##0.00');

  // Format date column
  sheet.getRange('C:C').setNumberFormat('yyyy-mm-dd');

  Logger.log('Gift Tracker tab created');
}

function createHealthDashboardTab(ss) {
  const sheet = ss.insertSheet('🩺 Health Dashboard');

  // Section 1: Weight Log
  sheet.getRange('A1').setValue('WEIGHT LOG').setFontWeight('bold').setFontSize(12).setBackground('#4A86E8').setFontColor('#FFFFFF');
  sheet.getRange('A2:C2').setValues([['Date', 'Weight (lbs)', 'Notes']]);
  sheet.getRange('A2:C2').setBackground('#4A86E8').setFontColor('#FFFFFF').setFontWeight('bold');

  // Section 2: Workouts
  sheet.getRange('E1').setValue('WORKOUTS').setFontWeight('bold').setFontSize(12).setBackground('#4A86E8').setFontColor('#FFFFFF');
  sheet.getRange('E2:G2').setValues([['Date', 'Type', 'Duration (min)']]);
  sheet.getRange('E2:G2').setBackground('#4A86E8').setFontColor('#FFFFFF').setFontWeight('bold');

  // Section 3: Appointments
  sheet.getRange('I1').setValue('APPOINTMENTS').setFontWeight('bold').setFontSize(12).setBackground('#4A86E8').setFontColor('#FFFFFF');
  sheet.getRange('I2:L2').setValues([['Date', 'Provider', 'Type', 'Notes']]);
  sheet.getRange('I2:L2').setBackground('#4A86E8').setFontColor('#FFFFFF').setFontWeight('bold');

  // Set column widths
  sheet.setColumnWidth(1, 120); // Date
  sheet.setColumnWidth(2, 120); // Weight
  sheet.setColumnWidth(3, 200); // Notes
  sheet.setColumnWidth(4, 30);  // Spacer
  sheet.setColumnWidth(5, 120); // Date
  sheet.setColumnWidth(6, 150); // Type
  sheet.setColumnWidth(7, 120); // Duration
  sheet.setColumnWidth(8, 30);  // Spacer
  sheet.setColumnWidth(9, 120); // Date
  sheet.setColumnWidth(10, 150); // Provider
  sheet.setColumnWidth(11, 150); // Type
  sheet.setColumnWidth(12, 200); // Notes

  // Format date columns
  sheet.getRange('A:A').setNumberFormat('yyyy-mm-dd');
  sheet.getRange('E:E').setNumberFormat('yyyy-mm-dd');
  sheet.getRange('I:I').setNumberFormat('yyyy-mm-dd');

  // Freeze header rows
  sheet.setFrozenRows(2);

  Logger.log('Health Dashboard tab created');
}

function createCalendarViewTab(ss) {
  const sheet = ss.insertSheet('📅 Calendar View');

  // Create a monthly calendar view with daily spending totals
  const currentYear = new Date().getFullYear();
  const currentMonth = new Date().getMonth() + 1;

  // Title
  sheet.getRange('A1').setValue(`${getMonthName(currentMonth)} ${currentYear} - Daily Spending`)
    .setFontWeight('bold')
    .setFontSize(14)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF');

  // Days of week header
  const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  sheet.getRange(2, 1, 1, 7).setValues([daysOfWeek]);
  sheet.getRange(2, 1, 1, 7)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF')
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  // Set column widths
  for (let i = 1; i <= 7; i++) {
    sheet.setColumnWidth(i, 120);
  }

  // Create calendar grid (5 rows for weeks)
  const firstDay = new Date(currentYear, currentMonth - 1, 1).getDay();
  const daysInMonth = new Date(currentYear, currentMonth, 0).getDate();

  let day = 1;
  for (let week = 0; week < 6; week++) {
    for (let dayOfWeek = 0; dayOfWeek < 7; dayOfWeek++) {
      const row = week + 3;
      const col = dayOfWeek + 1;

      if ((week === 0 && dayOfWeek < firstDay) || day > daysInMonth) {
        sheet.getRange(row, col).setValue('').setBackground('#F3F3F3');
      } else {
        const dateFormula = `DATE(${currentYear},${currentMonth},${day})`;
        const spendingFormula = `=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!A:A,${dateFormula},'📊 Transactions'!G:G,"<0")*-1`;

        sheet.getRange(row, col).setValue(day).setFontWeight('bold');
        sheet.getRange(row, col).setNote(`Spending: ${spendingFormula}`);
        day++;
      }

      // Add border
      sheet.getRange(row, col).setBorder(true, true, true, true, true, true);
    }

    if (day > daysInMonth) break;
  }

  // Add instructions
  sheet.getRange('A10').setValue('Note: Hover over dates to see daily spending totals')
    .setFontStyle('italic')
    .setFontColor('#666666');

  Logger.log('Calendar View tab created');
}

function createDashboardTab(ss) {
  const sheet = ss.insertSheet('📋 Dashboard');

  // Title
  sheet.getRange('A1:F1').merge()
    .setValue('FINANCIAL DASHBOARD - EXECUTIVE SUMMARY')
    .setFontWeight('bold')
    .setFontSize(16)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF')
    .setHorizontalAlignment('center');

  // Current date
  sheet.getRange('A2:F2').merge()
    .setFormula('=TEXT(TODAY(),"mmmm dd, yyyy")')
    .setHorizontalAlignment('center')
    .setFontSize(12)
    .setBackground('#E8F0FE');

  // Section 1: Account Balances
  sheet.getRange('A4').setValue('ACCOUNT BALANCES')
    .setFontWeight('bold')
    .setFontSize(12)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF');

  sheet.getRange('A5').setValue('Total Balance:');
  sheet.getRange('B5').setFormula('=SUM(\'💳 Credit Cards\'!B:B)')
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold')
    .setFontSize(14);

  // Section 2: This Month
  sheet.getRange('A7').setValue('THIS MONTH')
    .setFontWeight('bold')
    .setFontSize(12)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF');

  const currentMonthIndex = new Date().getMonth() + 2; // +2 because row 2 is first month

  sheet.getRange('A8').setValue('Total Spending:');
  sheet.getRange('B8').setFormula(`=\'💰 Monthly Summary\'!C${currentMonthIndex}`)
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold');

  sheet.getRange('A9').setValue('Total Income:');
  sheet.getRange('B9').setFormula(`=\'💰 Monthly Summary\'!B${currentMonthIndex}`)
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold');

  sheet.getRange('A10').setValue('Net:');
  sheet.getRange('B10').setFormula(`=\'💰 Monthly Summary\'!D${currentMonthIndex}`)
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold')
    .setFontSize(14);

  sheet.getRange('A11').setValue('Savings Rate:');
  sheet.getRange('B11').setFormula(`=\'💰 Monthly Summary\'!E${currentMonthIndex}`)
    .setNumberFormat('0.0%')
    .setFontWeight('bold');

  // Section 3: Year to Date
  sheet.getRange('A13').setValue('YEAR TO DATE')
    .setFontWeight('bold')
    .setFontSize(12)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF');

  sheet.getRange('A14').setValue('Total Spending:');
  sheet.getRange('B14').setFormula('=SUM(\'💰 Monthly Summary\'!C:C)')
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold');

  sheet.getRange('A15').setValue('Total Income:');
  sheet.getRange('B15').setFormula('=SUM(\'💰 Monthly Summary\'!B:B)')
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold');

  sheet.getRange('A16').setValue('YTD Net:');
  sheet.getRange('B16').setFormula('=B15-B14')
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold')
    .setFontSize(14);

  // Section 4: Budget Status
  sheet.getRange('D4').setValue('BUDGET STATUS')
    .setFontWeight('bold')
    .setFontSize(12)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF');

  sheet.getRange('D5').setValue('Total Budget:');
  sheet.getRange('E5').setFormula('=SUM(\'📊 Budget Master\'!B:B)')
    .setNumberFormat('$#,##0.00');

  sheet.getRange('D6').setValue('Total Spent:');
  sheet.getRange('E6').setFormula('=SUM(\'📊 Budget Master\'!C:C)')
    .setNumberFormat('$#,##0.00');

  sheet.getRange('D7').setValue('Remaining:');
  sheet.getRange('E7').setFormula('=E5-E6')
    .setNumberFormat('$#,##0.00')
    .setFontWeight('bold');

  sheet.getRange('D8').setValue('Budget Used:');
  sheet.getRange('E8').setFormula('=IF(E5=0,0,E6/E5)')
    .setNumberFormat('0.0%')
    .setFontWeight('bold');

  // Section 5: Quick Stats
  sheet.getRange('D10').setValue('QUICK STATS')
    .setFontWeight('bold')
    .setFontSize(12)
    .setBackground('#4A86E8')
    .setFontColor('#FFFFFF');

  sheet.getRange('D11').setValue('Total Transactions:');
  sheet.getRange('E11').setFormula('=COUNTA(\'📊 Transactions\'!A:A)-1')
    .setNumberFormat('#,##0');

  sheet.getRange('D12').setValue('Active Accounts:');
  sheet.getRange('E12').setFormula('=COUNTA(\'💳 Credit Cards\'!A:A)-1')
    .setNumberFormat('#,##0');

  sheet.getRange('D13').setValue('Active Tasks:');
  sheet.getRange('E13').setFormula('=COUNTIF(\'✅ Master Tasks\'!A:A,FALSE)')
    .setNumberFormat('#,##0');

  // Set column widths
  sheet.setColumnWidth(1, 180);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 30); // Spacer
  sheet.setColumnWidth(4, 180);
  sheet.setColumnWidth(5, 150);

  // Add conditional formatting for net income
  const netRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(0)
    .setBackground('#F4CCCC')
    .setRanges([sheet.getRange('B10'), sheet.getRange('B16')])
    .build();

  const positiveRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThan(0)
    .setBackground('#D9EAD3')
    .setRanges([sheet.getRange('B10'), sheet.getRange('B16')])
    .build();

  const rules = sheet.getConditionalFormatRules();
  rules.push(netRule);
  rules.push(positiveRule);
  sheet.setConditionalFormatRules(rules);

  Logger.log('Dashboard tab created');
}

// Helper function to get month name
function getMonthName(monthNum) {
  const months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'];
  return months[monthNum - 1];
}

/**
 * Custom menu to run functions
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Financial Dashboard')
    .addItem('Setup Dashboard', 'setupFinancialDashboard')
    .addItem('Import CSV Data', 'showImportDialog')
    .addToUi();
}

/**
 * Show dialog for CSV import instructions
 */
function showImportDialog() {
  const html = `
    <div style="font-family: Arial, sans-serif; padding: 20px;">
      <h2>Import CSV Data</h2>
      <p>To import your transaction data:</p>
      <ol>
        <li>Go to the <strong>📊 Transactions</strong> tab</li>
        <li>Click <strong>File > Import</strong></li>
        <li>Upload your CSV file</li>
        <li>Select <strong>Append rows to current sheet</strong></li>
        <li>Make sure the data starts at row 2 (below headers)</li>
      </ol>
      <p><strong>CSV Format Required:</strong><br>
      Date, Merchant, Category, Account, Original Statement, Notes, Amount, Tags, Owner</p>
      <p>After importing, all formulas in other tabs will automatically calculate!</p>
    </div>
  `;

  const htmlOutput = HtmlService.createHtmlOutput(html)
    .setWidth(500)
    .setHeight(350);

  SpreadsheetApp.getUi().showModalDialog(htmlOutput, 'Import CSV Instructions');
}
