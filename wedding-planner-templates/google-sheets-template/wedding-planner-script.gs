/**
 * Michelle & Gray Wedding Planner - Auto Setup Script
 *
 * HOW TO USE:
 * 1. Open a new Google Sheet
 * 2. Go to Extensions → Apps Script
 * 3. Delete any existing code and paste this entire script
 * 4. Click Save (disk icon)
 * 5. Click Run → select "createWeddingPlanner"
 * 6. Authorize when prompted (click "Advanced" → "Go to Wedding Planner")
 * 7. Wait ~30 seconds for it to build everything!
 */

function createWeddingPlanner() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Create all tabs
  createDashboardTab(ss);
  createBudgetTab(ss);
  createGuestsTab(ss);
  createVendorsTab(ss);
  createChecklistTab(ss);
  createTimelineTab(ss);

  // Delete default Sheet1 if it exists
  const defaultSheet = ss.getSheetByName('Sheet1');
  if (defaultSheet) {
    ss.deleteSheet(defaultSheet);
  }

  // Set Dashboard as active
  ss.setActiveSheet(ss.getSheetByName('Dashboard'));

  SpreadsheetApp.getUi().alert('🎉 Wedding Planner Created!\n\nYour planner is ready for Michelle & Gray.\n\nReplace the sample data with your real info!');
}

function createDashboardTab(ss) {
  let sheet = ss.getSheetByName('Dashboard');
  if (!sheet) {
    sheet = ss.insertSheet('Dashboard', 0);
  }

  // Header
  sheet.getRange('A1').setValue('Michelle & Gray Wedding Planner').setFontSize(24).setFontWeight('bold');
  sheet.getRange('A2').setValue('September 14, 2025 • Rosewood Gardens').setFontSize(12).setFontColor('#666666');

  // Quick Stats Headers
  sheet.getRange('A4:D4').setValues([['Days to Go', 'Tasks Done', 'Guests Attending', 'Budget Spent']]);
  sheet.getRange('A4:D4').setFontWeight('bold').setBackground('#f3f3f3');

  // Quick Stats Formulas
  sheet.getRange('A5').setFormula('=MAX(0,DATE(2025,9,14)-TODAY())');
  sheet.getRange('B5').setFormula('=IFERROR(ROUND(COUNTIF(Checklist!C:C,TRUE)/COUNTA(Checklist!B2:B100)*100,0)&"%","0%")');
  sheet.getRange('C5').setFormula('=COUNTIF(Guests!D:D,"Attending")');
  sheet.getRange('D5').setFormula('=TEXT(SUM(Budget!E:E),"$#,##0")');
  sheet.getRange('A5:D5').setFontSize(18).setFontWeight('bold');

  // Budget Summary
  sheet.getRange('A7').setValue('BUDGET BY CATEGORY').setFontSize(14).setFontWeight('bold');
  sheet.getRange('A8:D8').setValues([['Category', 'Spent', 'Budgeted', 'Remaining']]);
  sheet.getRange('A8:D8').setFontWeight('bold').setBackground('#f3f3f3');

  const categories = ['Venue & Catering', 'Photography', 'Florals & Decor', 'Attire & Beauty', 'Music & Entertainment', 'Stationery', 'Other'];
  for (let i = 0; i < categories.length; i++) {
    const row = 9 + i;
    sheet.getRange('A' + row).setValue(categories[i]);
    sheet.getRange('B' + row).setFormula('=SUMIF(Budget!$B:$B,A' + row + ',Budget!$E:$E)');
    sheet.getRange('C' + row).setFormula('=SUMIF(Budget!$B:$B,A' + row + ',Budget!$D:$D)');
    sheet.getRange('D' + row).setFormula('=C' + row + '-B' + row);
  }

  // Budget Totals
  const totalRow = 9 + categories.length;
  sheet.getRange('A' + totalRow).setValue('TOTAL').setFontWeight('bold');
  sheet.getRange('B' + totalRow).setFormula('=SUM(B9:B' + (totalRow - 1) + ')').setFontWeight('bold');
  sheet.getRange('C' + totalRow).setFormula('=SUM(C9:C' + (totalRow - 1) + ')').setFontWeight('bold');
  sheet.getRange('D' + totalRow).setFormula('=C' + totalRow + '-B' + totalRow).setFontWeight('bold');
  sheet.getRange('A' + totalRow + ':D' + totalRow).setBackground('#e8f5e9');

  // RSVP Summary
  const rsvpStart = totalRow + 2;
  sheet.getRange('A' + rsvpStart).setValue('RSVP STATUS').setFontSize(14).setFontWeight('bold');
  sheet.getRange('A' + (rsvpStart + 1) + ':B' + (rsvpStart + 1)).setValues([['Status', 'Count']]).setFontWeight('bold').setBackground('#f3f3f3');
  sheet.getRange('A' + (rsvpStart + 2)).setValue('Attending');
  sheet.getRange('B' + (rsvpStart + 2)).setFormula('=COUNTIF(Guests!D:D,"Attending")');
  sheet.getRange('A' + (rsvpStart + 3)).setValue('Declined');
  sheet.getRange('B' + (rsvpStart + 3)).setFormula('=COUNTIF(Guests!D:D,"Declined")');
  sheet.getRange('A' + (rsvpStart + 4)).setValue('Pending');
  sheet.getRange('B' + (rsvpStart + 4)).setFormula('=COUNTIF(Guests!D:D,"Pending")+COUNTIF(Guests!D:D,"No Response")');
  sheet.getRange('A' + (rsvpStart + 5)).setValue('Total').setFontWeight('bold');
  sheet.getRange('B' + (rsvpStart + 5)).setFormula('=SUM(B' + (rsvpStart + 2) + ':B' + (rsvpStart + 4) + ')').setFontWeight('bold');

  // Meal Counts
  const mealStart = rsvpStart + 7;
  sheet.getRange('A' + mealStart).setValue('MEAL COUNTS').setFontSize(14).setFontWeight('bold');
  sheet.getRange('A' + (mealStart + 1)).setValue('Beef');
  sheet.getRange('B' + (mealStart + 1)).setFormula('=COUNTIF(Guests!E:E,"Beef")');
  sheet.getRange('A' + (mealStart + 2)).setValue('Chicken');
  sheet.getRange('B' + (mealStart + 2)).setFormula('=COUNTIF(Guests!E:E,"Chicken")');
  sheet.getRange('A' + (mealStart + 3)).setValue('Fish');
  sheet.getRange('B' + (mealStart + 3)).setFormula('=COUNTIF(Guests!E:E,"Fish")');
  sheet.getRange('A' + (mealStart + 4)).setValue('Vegetarian');
  sheet.getRange('B' + (mealStart + 4)).setFormula('=COUNTIF(Guests!E:E,"Vegetarian")');
  sheet.getRange('A' + (mealStart + 5)).setValue('Vegan');
  sheet.getRange('B' + (mealStart + 5)).setFormula('=COUNTIF(Guests!E:E,"Vegan")');
  sheet.getRange('A' + (mealStart + 6)).setValue('Kids Meal');
  sheet.getRange('B' + (mealStart + 6)).setFormula('=COUNTIF(Guests!E:E,"Kids Meal")');

  // Column widths
  sheet.setColumnWidth(1, 180);
  sheet.setColumnWidth(2, 120);
  sheet.setColumnWidth(3, 120);
  sheet.setColumnWidth(4, 120);

  // Freeze header
  sheet.setFrozenRows(1);
}

function createBudgetTab(ss) {
  let sheet = ss.getSheetByName('Budget');
  if (!sheet) {
    sheet = ss.insertSheet('Budget');
  }

  // Headers
  const headers = ['Item', 'Category', 'Vendor', 'Estimated', 'Actual', 'Paid', 'Balance'];
  sheet.getRange('A1:G1').setValues([headers]).setFontWeight('bold').setBackground('#f3f3f3');

  // Sample data
  const data = [
    ['Venue rental', 'Venue & Catering', 'Rosewood Gardens', 5000, 5000, 5000, '=E2-F2'],
    ['Catering (per head x 142)', 'Venue & Catering', 'Rosewood Catering', 4000, 3500, 2000, '=E3-F3'],
    ['Photographer', 'Photography', 'Jane Smith Photo', 4000, 3500, 1750, '=E4-F4'],
    ['Videographer', 'Photography', '', 2000, 0, 0, '=E5-F5'],
    ['Bridal bouquet', 'Florals & Decor', 'Bloom Studio', 300, 350, 0, '=E6-F6'],
    ['Bridesmaids bouquets', 'Florals & Decor', 'Bloom Studio', 400, 400, 0, '=E7-F7'],
    ['Centerpieces', 'Florals & Decor', 'Bloom Studio', 1200, 1000, 500, '=E8-F8'],
    ['Ceremony flowers', 'Florals & Decor', 'Bloom Studio', 600, 500, 0, '=E9-F9'],
    ['Wedding dress', 'Attire & Beauty', 'Bridal Boutique', 2000, 1800, 1800, '=E10-F10'],
    ['Alterations', 'Attire & Beauty', '', 400, 400, 0, '=E11-F11'],
    ['Groom suit', 'Attire & Beauty', '', 500, 450, 450, '=E12-F12'],
    ['Hair & makeup', 'Attire & Beauty', '', 600, 600, 0, '=E13-F13'],
    ['DJ', 'Music & Entertainment', 'DJ Mike', 1500, 1500, 500, '=E14-F14'],
    ['Ceremony music', 'Music & Entertainment', '', 300, 0, 0, '=E15-F15'],
    ['Invitations', 'Stationery', 'Minted', 600, 550, 550, '=E16-F16'],
    ['Save the dates', 'Stationery', 'Minted', 200, 250, 250, '=E17-F17'],
    ['Programs & menus', 'Stationery', '', 300, 0, 0, '=E18-F18'],
    ['Guest transportation', 'Other', '', 500, 0, 0, '=E19-F19'],
    ['Wedding favors', 'Other', '', 400, 0, 0, '=E20-F20'],
    ['Wedding party gifts', 'Other', '', 600, 0, 0, '=E21-F21'],
    ['Tips & gratuities', 'Other', '', 500, 0, 0, '=E22-F22'],
    ['Emergency fund', 'Other', '', 1000, 0, 0, '=E23-F23'],
    ['Marriage license', 'Other', '', 100, 100, 100, '=E24-F24']
  ];

  sheet.getRange(2, 1, data.length, 7).setValues(data);

  // Totals row
  const totalRow = data.length + 2;
  sheet.getRange('A' + totalRow).setValue('TOTALS').setFontWeight('bold');
  sheet.getRange('D' + totalRow).setFormula('=SUM(D2:D' + (totalRow - 1) + ')').setFontWeight('bold');
  sheet.getRange('E' + totalRow).setFormula('=SUM(E2:E' + (totalRow - 1) + ')').setFontWeight('bold');
  sheet.getRange('F' + totalRow).setFormula('=SUM(F2:F' + (totalRow - 1) + ')').setFontWeight('bold');
  sheet.getRange('G' + totalRow).setFormula('=SUM(G2:G' + (totalRow - 1) + ')').setFontWeight('bold');
  sheet.getRange('A' + totalRow + ':G' + totalRow).setBackground('#e8f5e9');

  // Category dropdown
  const categoryRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Venue & Catering', 'Photography', 'Florals & Decor', 'Attire & Beauty', 'Music & Entertainment', 'Stationery', 'Transportation', 'Gifts & Favors', 'Other'])
    .build();
  sheet.getRange('B2:B100').setDataValidation(categoryRule);

  // Format currency columns
  sheet.getRange('D:G').setNumberFormat('$#,##0');

  // Conditional formatting for Balance
  const balanceRange = sheet.getRange('G2:G100');
  const zeroRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberEqualTo(0)
    .setBackground('#c8e6c9')
    .setRanges([balanceRange])
    .build();
  const positiveRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThan(0)
    .setBackground('#ffcdd2')
    .setRanges([balanceRange])
    .build();
  sheet.setConditionalFormatRules([zeroRule, positiveRule]);

  // Column widths
  sheet.setColumnWidth(1, 200);
  sheet.setColumnWidth(2, 150);
  sheet.setColumnWidth(3, 150);

  // Freeze header
  sheet.setFrozenRows(1);
}

function createGuestsTab(ss) {
  let sheet = ss.getSheetByName('Guests');
  if (!sheet) {
    sheet = ss.insertSheet('Guests');
  }

  // Headers
  const headers = ['Name', 'Email', 'Phone', 'RSVP', 'Meal', 'Table', 'Plus One', 'Notes'];
  sheet.getRange('A1:H1').setValues([headers]).setFontWeight('bold').setBackground('#f3f3f3');

  // Sample data
  const data = [
    ['John Smith', 'john@email.com', '555-1234', 'Attending', 'Beef', '1', 'Jane Smith', 'Best man'],
    ['Jane Smith', 'jane@email.com', '555-1235', 'Attending', 'Chicken', '1', '', "Best man's wife"],
    ['Sarah Johnson', 'sarah@email.com', '555-5678', 'Attending', 'Vegetarian', '2', '', 'Aunt'],
    ['Mike Brown', 'mike@email.com', '555-9012', 'Declined', '', '', '', 'College friend'],
    ['Emily Davis', 'emily@email.com', '555-3456', 'Pending', '', '', 'Tom Davis', 'Cousin'],
    ['Tom Davis', '', '', 'Pending', '', '', '', "Emily's plus one"],
    ['Robert Wilson', 'robert@email.com', '555-7890', 'Attending', 'Beef', '3', 'Lisa Wilson', 'Uncle'],
    ['Lisa Wilson', '', '', 'Attending', 'Fish', '3', '', 'Aunt'],
    ['Jennifer Lee', 'jennifer@email.com', '555-2345', 'No Response', '', '', '', 'Work friend'],
    ['David Martinez', 'david@email.com', '555-6789', 'Attending', 'Chicken', '4', 'Maria Martinez', 'Neighbor'],
    ['Maria Martinez', '', '', 'Attending', 'Vegetarian', '4', '', '']
  ];

  sheet.getRange(2, 1, data.length, 8).setValues(data);

  // RSVP dropdown
  const rsvpRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Attending', 'Declined', 'Pending', 'No Response'])
    .build();
  sheet.getRange('D2:D200').setDataValidation(rsvpRule);

  // Meal dropdown
  const mealRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Beef', 'Chicken', 'Fish', 'Vegetarian', 'Vegan', 'Kids Meal'])
    .build();
  sheet.getRange('E2:E200').setDataValidation(mealRule);

  // Conditional formatting for RSVP
  const rsvpRange = sheet.getRange('D2:D200');
  const attendingRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Attending')
    .setBackground('#c8e6c9')
    .setRanges([rsvpRange])
    .build();
  const declinedRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Declined')
    .setBackground('#ffcdd2')
    .setRanges([rsvpRange])
    .build();
  const pendingRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Pending')
    .setBackground('#fff9c4')
    .setRanges([rsvpRange])
    .build();
  const noResponseRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('No Response')
    .setBackground('#fff9c4')
    .setRanges([rsvpRange])
    .build();
  sheet.setConditionalFormatRules([attendingRule, declinedRule, pendingRule, noResponseRule]);

  // Column widths
  sheet.setColumnWidth(1, 150);
  sheet.setColumnWidth(2, 180);
  sheet.setColumnWidth(7, 150);
  sheet.setColumnWidth(8, 200);

  // Freeze header
  sheet.setFrozenRows(1);
}

function createVendorsTab(ss) {
  let sheet = ss.getSheetByName('Vendors');
  if (!sheet) {
    sheet = ss.insertSheet('Vendors');
  }

  // Headers
  const headers = ['Vendor', 'Service', 'Contact', 'Phone', 'Email', 'Total Cost', 'Deposit Paid', 'Status'];
  sheet.getRange('A1:H1').setValues([headers]).setFontWeight('bold').setBackground('#f3f3f3');

  // Sample data
  const data = [
    ['Rosewood Gardens', 'Venue', 'Amanda Lee', '555-1111', 'events@rosewood.com', 5000, 2500, 'Booked'],
    ['Jane Smith Photography', 'Photographer', 'Jane Smith', '555-2222', 'jane@janesmithphoto.com', 3500, 1750, 'Booked'],
    ['Bloom Studio', 'Florist', 'Maria Garcia', '555-3333', 'maria@bloomstudio.com', 2400, 500, 'Booked'],
    ['DJ Mike Entertainment', 'DJ', 'Mike Johnson', '555-4444', 'mike@djmike.com', 1500, 500, 'Booked'],
    ['Bella Catering', 'Catering', 'Chef Roberto', '555-5555', 'info@bellacatering.com', 3500, 0, 'Meeting Scheduled'],
    ['Sweet Dreams Bakery', 'Cake', 'Susan Baker', '555-6666', 'orders@sweetdreams.com', 800, 0, 'Researching'],
    ['Glamour Hair & Makeup', 'Hair & Makeup', 'Ashley Taylor', '555-7777', 'ashley@glamourhmu.com', 600, 0, 'Contacted'],
    ['Premier Limo', 'Transportation', '', '555-8888', 'info@premierlimo.com', 500, 0, 'Researching'],
    ['Rev. Thomas', 'Officiant', 'Rev. Thomas', '555-9999', 'rev.thomas@email.com', 300, 0, 'Contacted']
  ];

  sheet.getRange(2, 1, data.length, 8).setValues(data);

  // Status dropdown
  const statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Researching', 'Contacted', 'Meeting Scheduled', 'Booked', 'Deposit Paid', 'Paid in Full'])
    .build();
  sheet.getRange('H2:H50').setDataValidation(statusRule);

  // Format currency columns
  sheet.getRange('F:G').setNumberFormat('$#,##0');

  // Conditional formatting for Status
  const statusRange = sheet.getRange('H2:H50');
  const bookedRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextContains('Booked')
    .setBackground('#c8e6c9')
    .setRanges([statusRange])
    .build();
  const paidRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextContains('Paid')
    .setBackground('#c8e6c9')
    .setRanges([statusRange])
    .build();
  const researchRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextContains('Researching')
    .setBackground('#fff9c4')
    .setRanges([statusRange])
    .build();
  const contactedRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextContains('Contacted')
    .setBackground('#fff9c4')
    .setRanges([statusRange])
    .build();
  sheet.setConditionalFormatRules([bookedRule, paidRule, researchRule, contactedRule]);

  // Column widths
  sheet.setColumnWidth(1, 180);
  sheet.setColumnWidth(5, 200);

  // Freeze header
  sheet.setFrozenRows(1);
}

function createChecklistTab(ss) {
  let sheet = ss.getSheetByName('Checklist');
  if (!sheet) {
    sheet = ss.insertSheet('Checklist');
  }

  // Headers
  const headers = ['Phase', 'Task', 'Done', 'Due Date', 'Notes'];
  sheet.getRange('A1:E1').setValues([headers]).setFontWeight('bold').setBackground('#f3f3f3');

  // Sample data
  const data = [
    ['12+ Months', 'Announce engagement', true, '', ''],
    ['12+ Months', 'Set wedding date', true, '', 'September 14, 2025'],
    ['12+ Months', 'Determine overall budget', true, '', '$24,500 total'],
    ['12+ Months', 'Create guest list estimate', true, '', '~150 guests'],
    ['12+ Months', 'Research venues', true, '', ''],
    ['12+ Months', 'Book venue', true, '', 'Rosewood Gardens'],
    ['12+ Months', 'Hire wedding planner', false, '', 'Optional'],
    ['12+ Months', 'Book photographer', true, '', 'Jane Smith Photo'],
    ['9-6 Months', 'Book caterer', true, '', ''],
    ['9-6 Months', 'Hire florist', true, '', 'Bloom Studio'],
    ['9-6 Months', 'Book DJ or band', true, '', 'DJ Mike'],
    ['9-6 Months', 'Hire officiant', false, '', ''],
    ['9-6 Months', 'Book hair & makeup', false, '1/20/2025', ''],
    ['9-6 Months', 'Begin dress shopping', true, '', ''],
    ['9-6 Months', 'Order wedding dress', true, '', 'Allow 4-6 months'],
    ['9-6 Months', 'Start wedding registry', false, '', ''],
    ['9-6 Months', 'Reserve hotel room blocks', false, '', ''],
    ['9-6 Months', 'Book rehearsal dinner venue', false, '', ''],
    ['9-6 Months', 'Plan honeymoon', false, '', ''],
    ['6-3 Months', 'Send save-the-dates', true, '', ''],
    ['6-3 Months', 'Order invitations', true, '', 'Minted'],
    ['6-3 Months', 'Finalize guest list', false, '', ''],
    ['6-3 Months', 'Schedule cake tasting', false, '1/25/2025', ''],
    ['6-3 Months', 'Order wedding cake', false, '', ''],
    ['6-3 Months', 'Purchase wedding bands', false, '', ''],
    ['6-3 Months', 'Book transportation', false, '', ''],
    ['6-3 Months', 'Plan wedding favors', false, '', ''],
    ['6-3 Months', 'Schedule dress fittings', false, '', ''],
    ['90 Days', 'Mail invitations', false, '6/14/2025', '8-10 weeks before'],
    ['90 Days', 'Set up RSVP tracking', false, '', ''],
    ['90 Days', 'Schedule hair/makeup trial', false, '', ''],
    ['90 Days', 'Finalize wedding party attire', false, '', ''],
    ['90 Days', 'Order groom attire', false, '', ''],
    ['90 Days', 'Apply for marriage license', false, '', ''],
    ['90 Days', 'Confirm honeymoon reservations', false, '', ''],
    ['30 Days', 'Follow up on RSVPs', false, '8/14/2025', ''],
    ['30 Days', 'Submit final guest count', false, '', ''],
    ['30 Days', 'Confirm all vendor times', false, '', ''],
    ['30 Days', 'Finalize seating chart', false, '', ''],
    ['30 Days', 'Final dress fitting', false, '', ''],
    ['30 Days', 'Create day-of timeline', false, '', ''],
    ['30 Days', 'Create playlist for DJ', false, '', ''],
    ['30 Days', 'Prepare toasts', false, '', ''],
    ['30 Days', 'Prepare vendor tip envelopes', false, '', ''],
    ['30 Days', 'Arrange wedding party gifts', false, '', ''],
    ['Week Of', 'Confirm vendor deliveries', false, '9/10/2025', ''],
    ['Week Of', 'Share timeline with wedding party', false, '', ''],
    ['Week Of', 'Pack honeymoon bags', false, '', ''],
    ['Week Of', 'Rehearsal dinner', false, '9/12/2025', ''],
    ['Week Of', 'Give wedding party gifts', false, '', ''],
    ['Week Of', 'Lay out wedding day items', false, '9/13/2025', ''],
    ['Week Of', 'Get a good night\'s rest', false, '9/13/2025', '']
  ];

  sheet.getRange(2, 1, data.length, 5).setValues(data);

  // Add checkboxes to Done column
  sheet.getRange('C2:C' + (data.length + 1)).insertCheckboxes();

  // Phase dropdown
  const phaseRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['12+ Months', '9-6 Months', '6-3 Months', '90 Days', '30 Days', 'Week Of', 'Wedding Day'])
    .build();
  sheet.getRange('A2:A100').setDataValidation(phaseRule);

  // Conditional formatting - strikethrough completed tasks
  const dataRange = sheet.getRange('A2:E100');
  const completedRule = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=$C2=TRUE')
    .setStrikethrough(true)
    .setFontColor('#999999')
    .setRanges([dataRange])
    .build();
  sheet.setConditionalFormatRules([completedRule]);

  // Column widths
  sheet.setColumnWidth(1, 100);
  sheet.setColumnWidth(2, 250);
  sheet.setColumnWidth(3, 60);
  sheet.setColumnWidth(4, 100);
  sheet.setColumnWidth(5, 200);

  // Freeze header
  sheet.setFrozenRows(1);
}

function createTimelineTab(ss) {
  let sheet = ss.getSheetByName('Timeline');
  if (!sheet) {
    sheet = ss.insertSheet('Timeline');
  }

  // Headers
  const headers = ['Time', 'Event', 'Location', 'Who', 'Notes'];
  sheet.getRange('A1:E1').setValues([headers]).setFontWeight('bold').setBackground('#f3f3f3');

  // Sample data
  const data = [
    ['8:00 AM', 'Hair & Makeup team arrives', 'Bridal Suite', 'Glam team', 'Set up stations'],
    ['9:00 AM', 'Bride hair begins', 'Bridal Suite', 'Bride + stylist', ''],
    ['9:30 AM', 'Bridesmaids arrive', 'Bridal Suite', 'Bridesmaids', ''],
    ['10:00 AM', 'Bridesmaids hair begins', 'Bridal Suite', 'Bridesmaids', ''],
    ['10:30 AM', 'Groom & groomsmen getting ready', 'Groom\'s Suite', 'Groom + groomsmen', ''],
    ['11:00 AM', 'Photographer arrives', 'Bridal Suite', 'Photographer', 'Detail shots - dress, rings, shoes'],
    ['11:30 AM', 'Bride makeup begins', 'Bridal Suite', 'Bride', ''],
    ['12:00 PM', 'Lunch delivered', 'Both suites', 'Everyone', 'Light lunch - no red sauce!'],
    ['12:30 PM', 'Videographer arrives', 'Bridal Suite', 'Videographer', ''],
    ['1:00 PM', 'Bride gets into dress', 'Bridal Suite', 'Bride + MOH', 'Photo moment'],
    ['1:30 PM', 'Groom gets dressed', 'Groom\'s Suite', 'Groom + best man', ''],
    ['2:00 PM', 'First look', 'Garden Gazebo', 'Bride + Groom', 'Private moment'],
    ['2:30 PM', 'Couple photos', 'Garden', 'Bride + Groom + Photographers', ''],
    ['3:00 PM', 'Wedding party photos', 'Garden', 'Full wedding party', ''],
    ['3:30 PM', 'Family photos', 'Garden', 'Immediate family', 'List prepared'],
    ['4:00 PM', 'Guests begin arriving', 'Ceremony Lawn', 'Guests', 'Ushers seat guests'],
    ['4:15 PM', 'Bride & bridesmaids hidden', 'Bridal Suite', 'Bridal party', 'Final touch-ups'],
    ['4:25 PM', 'Groom takes position', 'Ceremony Altar', 'Groom + officiant', ''],
    ['4:30 PM', 'Ceremony begins', 'Ceremony Lawn', 'Everyone', 'Processional music cue'],
    ['5:00 PM', 'Ceremony ends', 'Ceremony Lawn', 'Everyone', 'Recessional'],
    ['5:05 PM', 'Receiving line OR couple photos', 'Terrace/Garden', 'Couple', 'Choose one'],
    ['5:15 PM', 'Cocktail hour begins', 'Terrace', 'Guests', 'Passed apps + signature drinks'],
    ['5:15 PM', 'More couple/family photos', 'Garden', 'Couple + family', 'Any missed shots'],
    ['6:00 PM', 'Guests seated for reception', 'Ballroom', 'Guests', 'DJ announces'],
    ['6:10 PM', 'Wedding party entrance', 'Ballroom', 'Wedding party', 'Intro music'],
    ['6:15 PM', 'Couple grand entrance', 'Ballroom', 'Bride + Groom', 'Special song'],
    ['6:20 PM', 'First dance', 'Ballroom', 'Bride + Groom', 'Song: TBD'],
    ['6:30 PM', 'Welcome & toasts begin', 'Ballroom', 'Best man + MOH', ''],
    ['6:45 PM', 'Dinner service begins', 'Ballroom', 'Everyone', ''],
    ['7:30 PM', 'Parent dances', 'Ballroom', 'Parents', 'Father-daughter then mother-son'],
    ['7:45 PM', 'Open dancing begins', 'Ballroom', 'Everyone', ''],
    ['8:30 PM', 'Cake cutting', 'Ballroom', 'Bride + Groom', 'Photo op'],
    ['8:45 PM', 'Bouquet toss', 'Ballroom', 'Single ladies', 'Optional'],
    ['9:00 PM', 'Dancing continues', 'Ballroom', 'Everyone', ''],
    ['10:30 PM', 'Last call announced', 'Ballroom', 'DJ', ''],
    ['10:45 PM', 'Last dance', 'Ballroom', 'Everyone', ''],
    ['11:00 PM', 'Sparkler send-off', 'Front entrance', 'Everyone', 'Coordinator distributes sparklers']
  ];

  sheet.getRange(2, 1, data.length, 5).setValues(data);

  // Column widths
  sheet.setColumnWidth(1, 90);
  sheet.setColumnWidth(2, 250);
  sheet.setColumnWidth(3, 120);
  sheet.setColumnWidth(4, 180);
  sheet.setColumnWidth(5, 250);

  // Alternate row colors for readability
  const evenRowRule = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=ISEVEN(ROW())')
    .setBackground('#f8f9fa')
    .setRanges([sheet.getRange('A2:E100')])
    .build();
  sheet.setConditionalFormatRules([evenRowRule]);

  // Freeze header
  sheet.setFrozenRows(1);
}
