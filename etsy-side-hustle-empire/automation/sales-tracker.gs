/**
 * ============================================================
 * 📊 ETSY SALES TRACKER & AUTOMATION HUB
 * ============================================================
 *
 * Automatically track your Etsy sales and trigger automations.
 * Works with Zapier, email notifications, and Google Sheets.
 *
 * SETUP:
 * 1. Create a new Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Paste this code
 * 4. Run setupSalesTracker()
 * 5. Set up triggers (see bottom of file)
 *
 * ============================================================
 */

// ============================================================
// CONFIGURATION - Update these values
// ============================================================

const CONFIG = {
  // Your email for notifications
  notificationEmail: 'your-email@example.com',

  // Enable/disable features
  enableEmailNotifications: true,
  enableSlackNotifications: false,
  enableReviewReminders: true,

  // Slack webhook URL (if using Slack)
  slackWebhookUrl: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',

  // Review reminder settings
  reviewReminderDays: 7,

  // Sheet names
  salesSheetName: 'Sales',
  dashboardSheetName: 'Dashboard',
  customersSheetName: 'Customers',

  // Colors
  colors: {
    header: '#2E7D32',
    success: '#4CAF50',
    warning: '#FFC107',
    danger: '#F44336'
  }
};

// ============================================================
// MAIN SETUP FUNCTION
// ============================================================

function setupSalesTracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ui = SpreadsheetApp.getUi();

  ui.alert('🚀 Setting up Sales Tracker',
           'This will create your sales tracking sheets. Click OK to continue.',
           ui.ButtonSet.OK);

  // Create all sheets
  createSalesSheet(ss);
  createCustomersSheet(ss);
  createDashboardSheet(ss);
  createReviewTrackerSheet(ss);

  // Set up menu
  createMenu();

  // Set up triggers
  setupTriggers();

  ui.alert('✅ Setup Complete!',
           'Your sales tracker is ready!\n\n' +
           '• Use "Add Sale" to log new orders\n' +
           '• Dashboard updates automatically\n' +
           '• Review reminders will send after ' + CONFIG.reviewReminderDays + ' days',
           ui.ButtonSet.OK);
}

// ============================================================
// SALES SHEET
// ============================================================

function createSalesSheet(ss) {
  let sheet = ss.getSheetByName(CONFIG.salesSheetName);
  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.salesSheetName);
  }

  sheet.clear();

  // Set column widths
  const widths = [100, 120, 200, 100, 80, 80, 150, 100, 150];
  widths.forEach((w, i) => sheet.setColumnWidth(i + 1, w));

  // Headers
  const headers = ['Date', 'Order ID', 'Product', 'Revenue', 'Fees', 'Net', 'Customer Email', 'Review?', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length)
    .setValues([headers])
    .setBackground(CONFIG.colors.header)
    .setFontColor('#FFFFFF')
    .setFontWeight('bold');

  // Format columns
  sheet.getRange('A2:A1000').setNumberFormat('MM/DD/YYYY');
  sheet.getRange('D2:F1000').setNumberFormat('$#,##0.00');

  // Data validation for Review column
  const reviewRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['⏳ Pending', '✅ Received', '📧 Requested', '❌ None'], true)
    .build();
  sheet.getRange('H2:H1000').setDataValidation(reviewRule);

  // Set default values
  for (let i = 2; i <= 10; i++) {
    sheet.getRange(i, 8).setValue('⏳ Pending');
  }

  // Freeze header
  sheet.setFrozenRows(1);

  // Sample data
  const today = new Date();
  const sampleData = [
    [today, 'ETY-' + Math.floor(Math.random() * 1000000), 'Side Hustle Empire Tracker', 27.99, 4.20, '=D2-E2', 'customer@example.com', '⏳ Pending', 'First sale!']
  ];
  sheet.getRange(2, 1, 1, 9).setValues(sampleData);
}

// ============================================================
// CUSTOMERS SHEET
// ============================================================

function createCustomersSheet(ss) {
  let sheet = ss.getSheetByName(CONFIG.customersSheetName);
  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.customersSheetName);
  }

  sheet.clear();

  // Headers
  const headers = ['Email', 'First Purchase', 'Total Orders', 'Total Spent', 'Last Order', 'Review Given', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length)
    .setValues([headers])
    .setBackground(CONFIG.colors.header)
    .setFontColor('#FFFFFF')
    .setFontWeight('bold');

  // Column widths
  const widths = [200, 100, 100, 100, 100, 100, 200];
  widths.forEach((w, i) => sheet.setColumnWidth(i + 1, w));

  sheet.setFrozenRows(1);
}

// ============================================================
// DASHBOARD SHEET
// ============================================================

function createDashboardSheet(ss) {
  let sheet = ss.getSheetByName(CONFIG.dashboardSheetName);
  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.dashboardSheetName);
  }
  ss.setActiveSheet(sheet);
  ss.moveActiveSheet(1);

  sheet.clear();
  sheet.setColumnWidths(1, 6, 150);

  // Header
  sheet.getRange('A1:F1').merge()
    .setValue('📊 ETSY SALES DASHBOARD')
    .setBackground(CONFIG.colors.header)
    .setFontColor('#FFFFFF')
    .setFontSize(20)
    .setFontWeight('bold')
    .setHorizontalAlignment('center');
  sheet.setRowHeight(1, 50);

  // KPI Section
  const kpis = [
    ['💰 TOTAL REVENUE', `=SUM('${CONFIG.salesSheetName}'!D:D)`, '$#,##0.00'],
    ['📦 TOTAL ORDERS', `=COUNTA('${CONFIG.salesSheetName}'!A:A)-1`, '0'],
    ['💵 AVERAGE ORDER', `=IFERROR(AVERAGE('${CONFIG.salesSheetName}'!D:D),0)`, '$#,##0.00'],
    ['📈 THIS MONTH', `=SUMIF('${CONFIG.salesSheetName}'!A:A,">="&EOMONTH(TODAY(),-1)+1,'${CONFIG.salesSheetName}'!D:D)`, '$#,##0.00'],
    ['⭐ REVIEWS RECEIVED', `=COUNTIF('${CONFIG.salesSheetName}'!H:H,"✅ Received")`, '0'],
    ['📊 REVIEW RATE', `=IFERROR(COUNTIF('${CONFIG.salesSheetName}'!H:H,"✅ Received")/(COUNTA('${CONFIG.salesSheetName}'!A:A)-1),0)`, '0.0%']
  ];

  let row = 3;
  kpis.forEach((kpi, index) => {
    sheet.getRange(row + index, 1).setValue(kpi[0])
      .setFontWeight('bold')
      .setBackground('#E8F5E9');
    sheet.getRange(row + index, 2).setFormula(kpi[1])
      .setNumberFormat(kpi[2])
      .setFontSize(14)
      .setFontWeight('bold');
  });

  // Monthly breakdown section
  const monthlyRow = 11;
  sheet.getRange(monthlyRow, 1, 1, 6).merge()
    .setValue('📅 MONTHLY BREAKDOWN')
    .setBackground('#1565C0')
    .setFontColor('#FFFFFF')
    .setFontWeight('bold')
    .setHorizontalAlignment('center');

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  months.forEach((month, index) => {
    const col = (index % 6) + 1;
    const r = monthlyRow + 1 + Math.floor(index / 6) * 2;

    sheet.getRange(r, col).setValue(month).setFontWeight('bold').setBackground('#E3F2FD');
    sheet.getRange(r + 1, col).setFormula(
      `=SUMPRODUCT(('${CONFIG.salesSheetName}'!A:A>=DATE(YEAR(TODAY()),${index + 1},1))*('${CONFIG.salesSheetName}'!A:A<DATE(YEAR(TODAY()),${index + 2},1))*'${CONFIG.salesSheetName}'!D:D)`
    ).setNumberFormat('$#,##0');
  });

  // Quick actions section
  const actionsRow = 17;
  sheet.getRange(actionsRow, 1, 1, 6).merge()
    .setValue('⚡ Quick Actions: Use the "Sales Tools" menu above for common tasks')
    .setBackground('#FFF3E0')
    .setFontStyle('italic')
    .setHorizontalAlignment('center');
}

// ============================================================
// REVIEW TRACKER SHEET
// ============================================================

function createReviewTrackerSheet(ss) {
  let sheet = ss.getSheetByName('Review Tracker');
  if (!sheet) {
    sheet = ss.insertSheet('Review Tracker');
  }

  sheet.clear();

  // Headers
  const headers = ['Order Date', 'Order ID', 'Customer Email', 'Reminder Sent', 'Reminder Date', 'Review Status', 'Notes'];
  sheet.getRange(1, 1, 1, headers.length)
    .setValues([headers])
    .setBackground('#F57C00')
    .setFontColor('#FFFFFF')
    .setFontWeight('bold');

  sheet.setFrozenRows(1);
}

// ============================================================
// ADD SALE FUNCTION
// ============================================================

function addSale() {
  const ui = SpreadsheetApp.getUi();

  // Prompt for sale details
  const orderIdResponse = ui.prompt('Add New Sale', 'Enter Order ID (e.g., ETY-123456):', ui.ButtonSet.OK_CANCEL);
  if (orderIdResponse.getSelectedButton() !== ui.Button.OK) return;

  const revenueResponse = ui.prompt('Add New Sale', 'Enter sale amount (e.g., 27.99):', ui.ButtonSet.OK_CANCEL);
  if (revenueResponse.getSelectedButton() !== ui.Button.OK) return;

  const feesResponse = ui.prompt('Add New Sale', 'Enter Etsy fees (e.g., 4.20):', ui.ButtonSet.OK_CANCEL);
  if (feesResponse.getSelectedButton() !== ui.Button.OK) return;

  const emailResponse = ui.prompt('Add New Sale', 'Enter customer email:', ui.ButtonSet.OK_CANCEL);
  if (emailResponse.getSelectedButton() !== ui.Button.OK) return;

  // Add to sales sheet
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.salesSheetName);

  const lastRow = sheet.getLastRow() + 1;
  const revenue = parseFloat(revenueResponse.getResponseText());
  const fees = parseFloat(feesResponse.getResponseText());

  sheet.getRange(lastRow, 1).setValue(new Date());
  sheet.getRange(lastRow, 2).setValue(orderIdResponse.getResponseText());
  sheet.getRange(lastRow, 3).setValue('Side Hustle Empire Tracker');
  sheet.getRange(lastRow, 4).setValue(revenue);
  sheet.getRange(lastRow, 5).setValue(fees);
  sheet.getRange(lastRow, 6).setFormula(`=D${lastRow}-E${lastRow}`);
  sheet.getRange(lastRow, 7).setValue(emailResponse.getResponseText());
  sheet.getRange(lastRow, 8).setValue('⏳ Pending');

  // Send notification
  if (CONFIG.enableEmailNotifications) {
    sendSaleNotification(orderIdResponse.getResponseText(), revenue);
  }

  ui.alert('✅ Sale Added!', `Order ${orderIdResponse.getResponseText()} has been logged.`, ui.ButtonSet.OK);
}

// ============================================================
// NOTIFICATION FUNCTIONS
// ============================================================

function sendSaleNotification(orderId, amount) {
  const subject = `🎉 New Etsy Sale: $${amount.toFixed(2)}`;
  const body = `
    New sale recorded!

    Order ID: ${orderId}
    Amount: $${amount.toFixed(2)}
    Time: ${new Date().toLocaleString()}

    View your dashboard: ${SpreadsheetApp.getActiveSpreadsheet().getUrl()}
  `;

  GmailApp.sendEmail(CONFIG.notificationEmail, subject, body);
}

function sendSlackNotification(message) {
  if (!CONFIG.enableSlackNotifications) return;

  const payload = JSON.stringify({ text: message });

  UrlFetchApp.fetch(CONFIG.slackWebhookUrl, {
    method: 'post',
    contentType: 'application/json',
    payload: payload
  });
}

// ============================================================
// REVIEW REMINDER SYSTEM
// ============================================================

function checkReviewReminders() {
  if (!CONFIG.enableReviewReminders) return;

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const salesSheet = ss.getSheetByName(CONFIG.salesSheetName);
  const data = salesSheet.getDataRange().getValues();

  const today = new Date();
  const reminderThreshold = CONFIG.reviewReminderDays * 24 * 60 * 60 * 1000; // Days in ms

  // Skip header row
  for (let i = 1; i < data.length; i++) {
    const orderDate = new Date(data[i][0]);
    const email = data[i][6];
    const reviewStatus = data[i][7];

    // Check if reminder should be sent
    if (reviewStatus === '⏳ Pending' && email && (today - orderDate) >= reminderThreshold) {
      // Mark as reminder requested (you'd integrate with actual email system)
      salesSheet.getRange(i + 1, 8).setValue('📧 Requested');

      // Log the reminder
      Logger.log(`Review reminder due for: ${email} (Order date: ${orderDate})`);

      // You could send actual email here:
      // sendReviewRequestEmail(email, data[i][1]);
    }
  }
}

function sendReviewRequestEmail(email, orderId) {
  const subject = 'How\'s your Side Hustle Tracker working? ⭐';
  const body = `
Hi there!

I hope you're enjoying your Side Hustle Empire Tracker!

It's been about a week since your purchase, and I'd love to hear how it's working for you.

If you have a moment, a quick review would mean the world to me! Your feedback helps other side hustlers find this tool.

⭐ Leave a Review: [Your Etsy review link]

Is there anything I can help you with?

Thanks so much!
  `;

  // Uncomment to actually send
  // GmailApp.sendEmail(email, subject, body);
  Logger.log(`Review request would be sent to: ${email}`);
}

// ============================================================
// REPORTING FUNCTIONS
// ============================================================

function generateWeeklyReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const salesSheet = ss.getSheetByName(CONFIG.salesSheetName);
  const data = salesSheet.getDataRange().getValues();

  const today = new Date();
  const weekAgo = new Date(today - 7 * 24 * 60 * 60 * 1000);

  let weeklyRevenue = 0;
  let weeklySales = 0;
  let weeklyFees = 0;

  for (let i = 1; i < data.length; i++) {
    const orderDate = new Date(data[i][0]);
    if (orderDate >= weekAgo) {
      weeklySales++;
      weeklyRevenue += parseFloat(data[i][3]) || 0;
      weeklyFees += parseFloat(data[i][4]) || 0;
    }
  }

  const report = `
📊 WEEKLY SALES REPORT
${weekAgo.toLocaleDateString()} - ${today.toLocaleDateString()}

━━━━━━━━━━━━━━━━━━━━━━

📦 Total Sales: ${weeklySales}
💰 Gross Revenue: $${weeklyRevenue.toFixed(2)}
💸 Fees Paid: $${weeklyFees.toFixed(2)}
📈 Net Revenue: $${(weeklyRevenue - weeklyFees).toFixed(2)}

━━━━━━━━━━━━━━━━━━━━━━

View full dashboard: ${ss.getUrl()}
  `;

  if (CONFIG.enableEmailNotifications) {
    GmailApp.sendEmail(CONFIG.notificationEmail, '📊 Weekly Sales Report', report);
  }

  return report;
}

// ============================================================
// MENU CREATION
// ============================================================

function createMenu() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('📊 Sales Tools')
    .addItem('➕ Add New Sale', 'addSale')
    .addSeparator()
    .addItem('📧 Check Review Reminders', 'checkReviewReminders')
    .addItem('📊 Generate Weekly Report', 'generateWeeklyReport')
    .addSeparator()
    .addItem('🔄 Refresh Dashboard', 'refreshDashboard')
    .addItem('⚙️ Settings', 'showSettings')
    .addToUi();
}

function onOpen() {
  createMenu();
}

function refreshDashboard() {
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.dashboardSheetName).activate();
  SpreadsheetApp.flush();
  SpreadsheetApp.getUi().alert('Dashboard refreshed! 📊');
}

function showSettings() {
  const ui = SpreadsheetApp.getUi();
  ui.alert('⚙️ Settings',
    `Current Configuration:\n\n` +
    `• Notification Email: ${CONFIG.notificationEmail}\n` +
    `• Email Notifications: ${CONFIG.enableEmailNotifications}\n` +
    `• Review Reminders: ${CONFIG.enableReviewReminders}\n` +
    `• Reminder Days: ${CONFIG.reviewReminderDays}\n\n` +
    `To change settings, edit the CONFIG object in the script.`,
    ui.ButtonSet.OK);
}

// ============================================================
// TRIGGERS SETUP
// ============================================================

function setupTriggers() {
  // Remove existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  // Daily review reminder check
  ScriptApp.newTrigger('checkReviewReminders')
    .timeBased()
    .everyDays(1)
    .atHour(10)
    .create();

  // Weekly report
  ScriptApp.newTrigger('generateWeeklyReport')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(9)
    .create();

  // On open trigger for menu
  ScriptApp.newTrigger('onOpen')
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onOpen()
    .create();

  Logger.log('Triggers set up successfully!');
}
