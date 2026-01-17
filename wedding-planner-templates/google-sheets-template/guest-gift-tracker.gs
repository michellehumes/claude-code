/**
 * Wedding Guest Gift Tracker - Auto Setup Script
 *
 * HOW TO USE:
 * 1. Open a new Google Sheet
 * 2. Go to Extensions → Apps Script
 * 3. Delete any existing code and paste this entire script
 * 4. Click Save (disk icon)
 * 5. Click Run → select "createGuestGiftTracker"
 * 6. Authorize when prompted (click "Advanced" → "Go to Guest Gift Tracker")
 * 7. Wait ~15 seconds for it to build everything!
 */

function createGuestGiftTracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Create all tabs
  createDashboard(ss);
  createGiftListTab(ss);
  createByStatusTab(ss);

  // Delete default Sheet1 if it exists
  const defaultSheet = ss.getSheetByName('Sheet1');
  if (defaultSheet) {
    ss.deleteSheet(defaultSheet);
  }

  // Set Dashboard as active
  ss.setActiveSheet(ss.getSheetByName('Dashboard'));

  SpreadsheetApp.getUi().alert('🎁 Guest Gift Tracker Created!\n\nYour tracker is ready with all your guest data.\n\nUse the Dashboard for quick stats!');
}

function createDashboard(ss) {
  let sheet = ss.getSheetByName('Dashboard');
  if (!sheet) {
    sheet = ss.insertSheet('Dashboard', 0);
  }
  sheet.clear();

  // Colors
  const headerBg = '#1a73e8';
  const headerText = '#ffffff';
  const accentBg = '#e8f0fe';
  const successBg = '#e6f4ea';
  const warningBg = '#fef7e0';
  const cardBg = '#f8f9fa';

  // Title Section
  sheet.getRange('A1:F1').merge().setValue('💍 Wedding Gift Tracker').setFontSize(28).setFontWeight('bold').setFontColor('#1a73e8').setHorizontalAlignment('center');
  sheet.getRange('A2:F2').merge().setValue('Thank You Note Progress Dashboard').setFontSize(12).setFontColor('#5f6368').setHorizontalAlignment('center');
  sheet.setRowHeight(1, 50);
  sheet.setRowHeight(2, 30);

  // Spacer
  sheet.setRowHeight(3, 20);

  // Quick Stats Cards Row
  sheet.getRange('A4:B4').merge().setValue('📊 TOTAL GIFTS').setFontSize(11).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText).setHorizontalAlignment('center');
  sheet.getRange('C4:D4').merge().setValue('💰 TOTAL VALUE').setFontSize(11).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText).setHorizontalAlignment('center');
  sheet.getRange('E4:F4').merge().setValue('✅ NOTES SENT').setFontSize(11).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText).setHorizontalAlignment('center');

  sheet.getRange('A5:B5').merge().setFormula('=COUNTA(\'Gift List\'!A2:A100)').setFontSize(32).setFontWeight('bold').setBackground(cardBg).setHorizontalAlignment('center');
  sheet.getRange('C5:D5').merge().setFormula('=TEXT(SUM(\'Gift List\'!F2:F100),"$#,##0.00")').setFontSize(32).setFontWeight('bold').setBackground(cardBg).setHorizontalAlignment('center');
  sheet.getRange('E5:F5').merge().setFormula('=COUNTIF(\'Gift List\'!C2:C100,"Sent")').setFontSize(32).setFontWeight('bold').setBackground(successBg).setHorizontalAlignment('center');
  sheet.setRowHeight(5, 70);

  // Spacer
  sheet.setRowHeight(6, 20);

  // Thank You Status Summary
  sheet.getRange('A7:C7').merge().setValue('📝 THANK YOU NOTE STATUS').setFontSize(12).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText);
  sheet.getRange('A8:B8').setValues([['Status', 'Count']]).setFontWeight('bold').setBackground(accentBg);
  sheet.getRange('C8').setValue('Progress').setFontWeight('bold').setBackground(accentBg);

  const statuses = ['Sent', 'Written', 'Envelope Ready', 'Note Pending'];
  for (let i = 0; i < statuses.length; i++) {
    const row = 9 + i;
    sheet.getRange('A' + row).setValue(statuses[i]);
    sheet.getRange('B' + row).setFormula('=COUNTIF(\'Gift List\'!C:C,"' + statuses[i] + '")');
  }
  sheet.getRange('A13:B13').setValues([['TOTAL', '']]).setFontWeight('bold').setBackground(accentBg);
  sheet.getRange('B13').setFormula('=SUM(B9:B12)');

  // Progress bar formula
  sheet.getRange('C9').setFormula('=REPT("█",ROUND(B9/B$13*20))&REPT("░",20-ROUND(B9/B$13*20))');
  sheet.getRange('C10').setFormula('=REPT("█",ROUND(B10/B$13*20))&REPT("░",20-ROUND(B10/B$13*20))');
  sheet.getRange('C11').setFormula('=REPT("█",ROUND(B11/B$13*20))&REPT("░",20-ROUND(B11/B$13*20))');
  sheet.getRange('C12').setFormula('=REPT("█",ROUND(B12/B$13*20))&REPT("░",20-ROUND(B12/B$13*20))');
  sheet.getRange('C9:C12').setFontFamily('Courier New').setFontColor('#1a73e8');

  // Spacer
  sheet.setRowHeight(14, 20);

  // By Side Summary
  sheet.getRange('A15:C15').merge().setValue('👰🤵 GIFTS BY SIDE').setFontSize(12).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText);
  sheet.getRange('A16:C16').setValues([['Side', 'Count', 'Total Value']]).setFontWeight('bold').setBackground(accentBg);
  sheet.getRange('A17').setValue('Bride');
  sheet.getRange('B17').setFormula('=COUNTIF(\'Gift List\'!B:B,"Bride")');
  sheet.getRange('C17').setFormula('=SUMIF(\'Gift List\'!B:B,"Bride",\'Gift List\'!F:F)').setNumberFormat('$#,##0.00');
  sheet.getRange('A18').setValue('Groom');
  sheet.getRange('B18').setFormula('=COUNTIF(\'Gift List\'!B:B,"Groom")');
  sheet.getRange('C18').setFormula('=SUMIF(\'Gift List\'!B:B,"Groom",\'Gift List\'!F:F)').setNumberFormat('$#,##0.00');
  sheet.getRange('A19:C19').setValues([['TOTAL', '', '']]).setFontWeight('bold').setBackground(accentBg);
  sheet.getRange('B19').setFormula('=SUM(B17:B18)');
  sheet.getRange('C19').setFormula('=SUM(C17:C18)').setNumberFormat('$#,##0.00');

  // Spacer
  sheet.setRowHeight(20, 20);

  // Top Gifts
  sheet.getRange('A21:C21').merge().setValue('🎁 TOP 5 GIFTS BY VALUE').setFontSize(12).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText);
  sheet.getRange('A22:C22').setValues([['Guest', 'Gift', 'Amount']]).setFontWeight('bold').setBackground(accentBg);
  for (let i = 0; i < 5; i++) {
    const row = 23 + i;
    sheet.getRange('A' + row).setFormula('=IFERROR(INDEX(\'Gift List\'!A:A,MATCH(LARGE(\'Gift List\'!F:F,' + (i+1) + '),\'Gift List\'!F:F,0)),"")');
    sheet.getRange('B' + row).setFormula('=IFERROR(INDEX(\'Gift List\'!E:E,MATCH(LARGE(\'Gift List\'!F:F,' + (i+1) + '),\'Gift List\'!F:F,0)),"")');
    sheet.getRange('C' + row).setFormula('=IFERROR(LARGE(\'Gift List\'!F:F,' + (i+1) + '),"")').setNumberFormat('$#,##0.00');
  }

  // Column widths
  sheet.setColumnWidth(1, 160);
  sheet.setColumnWidth(2, 80);
  sheet.setColumnWidth(3, 200);
  sheet.setColumnWidth(4, 80);
  sheet.setColumnWidth(5, 100);
  sheet.setColumnWidth(6, 100);

  // Borders for cards
  sheet.getRange('A4:F5').setBorder(true, true, true, true, false, false, '#dadce0', SpreadsheetApp.BorderStyle.SOLID);
  sheet.getRange('A7:C13').setBorder(true, true, true, true, false, false, '#dadce0', SpreadsheetApp.BorderStyle.SOLID);
  sheet.getRange('A15:C19').setBorder(true, true, true, true, false, false, '#dadce0', SpreadsheetApp.BorderStyle.SOLID);
  sheet.getRange('A21:C27').setBorder(true, true, true, true, false, false, '#dadce0', SpreadsheetApp.BorderStyle.SOLID);

  sheet.setFrozenRows(0);
}

function createGiftListTab(ss) {
  let sheet = ss.getSheetByName('Gift List');
  if (!sheet) {
    sheet = ss.insertSheet('Gift List');
  }
  sheet.clear();

  // Colors
  const headerBg = '#1a73e8';
  const headerText = '#ffffff';

  // Headers
  const headers = ['Guest Name', 'Side', 'Thank You Status', 'Address', 'Gift Description', 'Gift Amount', 'Timing'];
  sheet.getRange('A1:G1').setValues([headers]).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText).setHorizontalAlignment('center');
  sheet.setRowHeight(1, 35);

  // Guest data
  const data = [
    ['Meg & Anthony', 'Groom', 'Note Pending', '130 W Beardsley Ave, Beach Haven, NJ 08008', 'Cash Fund – Honeymoon Resort', 300, 'Xmas'],
    ['Alec & Kelsey Demet', 'Groom', 'Envelope Ready', '8562 E Pierce St, Scottsdale, AZ 85257', 'Cash Fund – Honeymoon Resort', 300, 'Xmas'],
    ['Alex Tirey', 'Bride', '', '', '', '', 'Xmas'],
    ['Amy & Dan McCauley', 'Bride', 'Envelope Ready', '1006 Weatherburn Dr., Valencia, PA 16059', 'Cash Fund – Honeymoon Resort; Kaloh Melamine Outdoor Serveware; Kaloh Melamine Tray', 321.20, 'Xmas'],
    ['Andy & Susan Alisberg', 'Groom', 'Note Pending', '5 Pine Lane West, Boynton Beach, FL 33436', 'Jeanne Fitz Salad Bowl & Servers; Monos Check-In Large; All-Clad Stainless-Steel Utensils', 804.94, 'Xmas'],
    ['Anne Munnelly', 'Bride', 'Sent', '9000 236th Court, 33A, Salem, WI 54168', 'Cash Fund – Honeymoon Resort', 300, 'Xmas'],
    ['Baxter & Sam Male', 'Groom', '', '', '', '', 'Xmas'],
    ['Bea Van Dam', 'Bride', '', '', '', '', 'Xmas'],
    ['Beverly Johnson', 'Groom', 'Note Pending', '18 Sawmill Lane, Greenwich, CT 06830', 'Kaloh Dinnerware Set (16pc); Kaloh Mixing Bowls (Set of 3)', 287.60, 'Xmas'],
    ['Brendan Salvadore', 'Groom', 'Envelope Ready', '630 Metropolitan Ave, 2A, Brooklyn, NY 11211', 'Cash Fund – Honeymoon Resort', 250, 'Xmas'],
    ['Bridgette & Joel Pepmeyer', 'Bride', 'Note Pending', '316 3RD ST, Aspinwall, PA 15215', 'Arles Gravy Boat; Kanto Serving Platter; Caraway Nonstick Sauce Pan', 203.50, 'Xmas'],
    ['Charlie & Libby King', 'Groom', 'Envelope Ready', '11 Oakwood Lane, Greenwich, CT 06830', 'Estelle Colored Glass Set of 6 Stem Coupes; Speckled Fruit Stand', 455, 'Xmas'],
    ['Chloe McCann', 'Bride', 'Sent', '1 John Street, 9C, Brooklyn, NY 11201', 'Napkin Holders (Pottery Barn) – Shower', 79, 'Xmas'],
    ['Connie Giovanini', 'Bride', 'Note Pending', '4045 Werthers Ct, Fairfax, VA 22030', 'Camille Long Stem Wine Glasses', 139.80, 'Xmas'],
    ['Dan & Jenny Hubner', 'Bride', 'Note Pending', '89 Voorhis Ave, Rockville Centre, NY 11570', 'Tall Ramekins (Set of 4); Monique Lhuillier Arles Footed Bowl', 92.80, 'Xmas'],
    ['David & Jennifer Evans', 'Groom', 'Envelope Ready', '35 Sawmill Lane, Greenwich, CT 06830', 'Camille Long Stem Wine Glasses (Set)', 419.40, 'Xmas'],
    ['Don & Eileen Foster', 'Bride', 'Sent', '15512 Monterosso Lane, Unit 102, Naples, FL 34108', 'Le Creuset Classic Heritage Covered Casserole Dish; Check', 269.98, 'Xmas'],
    ['Edouard & Kelley Moueix', 'Groom', 'Written', '', 'Cash Fund – Honeymoon Resort', 300, 'Xmas'],
    ['Emily Africk', 'Bride', 'Note Pending', '56 Seventh Ave, 3B, New York, NY 10011', 'Estelle Colored Glass Stemmed Wine Glass (Set of 6); Throw; Wine Glasses; Balloons (Engagement)', 185, 'Xmas'],
    ['Gary & Jacqueline Meek', 'Bride', 'Sent', '106 Easton Dr, Mooresville, NC 28117', 'Cash Fund – Honeymoon Resort', 100, 'Xmas'],
    ['Gordy & Linda Opitz', 'Bride', 'Sent', '540 Salem Heights Dr, Gibsonia, PA 15044', 'Caraway 4-Piece Cutting Board Set; Check; Shower Gift', 990, 'Xmas'],
    ['Henry Bassett', 'Groom', 'Envelope Ready', '1208 E Rock Springs Rd NE, Atlanta, GA 30306', 'High-Glass Pedestal Candleholders; Avanti G2 Touchscreen Nugget Ice Dispenser', 478.65, 'Xmas'],
    ['Howdy Howard & Robin Perkins', 'Groom', 'Sent', '103 West Lyon Farm Dr., Greenwich, CT 06831', 'Caraway Squareware Set; Caraway Roasting Pan', 760, 'Xmas'],
    ['Jane Van Dam', 'Bride', 'Sent', '', 'Check', 300, 'Xmas'],
    ['Joann Sirera', 'Bride', 'Envelope Ready', '4801 Wexford Run Road, Wexford, PA 15090', 'Cash Fund – Honeymoon Resort', 700, 'Xmas'],
    ['Jean Marie Woodard & Kenneth Munnelly', 'Bride', 'Sent', '', 'Cuisinart Precision Stand Mixer; Check', 1319.95, 'Xmas'],
    ['Kristen Munnelly', 'Bride', 'Note Pending', '105 Steeplewood Dr, Exton, PA 19341', 'Wüsthof 16-Piece Knife Block Set; Check', 1495, 'Xmas'],
    ['Lauren Beck', 'Bride', 'Note Pending', '870 Pacific Street, Apt 1F, Brooklyn, NY 11238', 'Estelle Colored Glass Champagne Flutes (Set of 6)', 205, 'Xmas'],
    ['Tami & Kelly Salvadore', 'Groom', 'Note Pending', '', 'Check', 1000, 'Xmas'],
    ['Zara Lopez', 'Bride', 'Sent', '6401 Rialto Blvd., 238, Austin, TX 78735', 'Marble Wine Cooler; Capri Blue Volcano Candle', 77.95, 'Xmas'],
    ['Zelda & Matt Moss', 'Groom', 'Note Pending', '', 'Cash & Soap', 200, 'Xmas']
  ];

  sheet.getRange(2, 1, data.length, 7).setValues(data);

  // Side dropdown
  const sideRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Bride', 'Groom'])
    .build();
  sheet.getRange('B2:B200').setDataValidation(sideRule);

  // Status dropdown
  const statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Note Pending', 'Written', 'Envelope Ready', 'Sent'])
    .build();
  sheet.getRange('C2:C200').setDataValidation(statusRule);

  // Format currency column
  sheet.getRange('F:F').setNumberFormat('$#,##0.00');

  // Conditional formatting for Status
  const statusRange = sheet.getRange('C2:C200');

  const sentRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Sent')
    .setBackground('#c8e6c9')
    .setFontColor('#1b5e20')
    .setRanges([statusRange])
    .build();

  const writtenRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Written')
    .setBackground('#b3e5fc')
    .setFontColor('#01579b')
    .setRanges([statusRange])
    .build();

  const envelopeRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Envelope Ready')
    .setBackground('#fff9c4')
    .setFontColor('#f57f17')
    .setRanges([statusRange])
    .build();

  const pendingRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Note Pending')
    .setBackground('#ffcdd2')
    .setFontColor('#b71c1c')
    .setRanges([statusRange])
    .build();

  // Conditional formatting for Side
  const sideRange = sheet.getRange('B2:B200');

  const brideRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Bride')
    .setBackground('#f3e5f5')
    .setFontColor('#7b1fa2')
    .setRanges([sideRange])
    .build();

  const groomRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Groom')
    .setBackground('#e3f2fd')
    .setFontColor('#1565c0')
    .setRanges([sideRange])
    .build();

  // Alternating row colors
  const dataRange = sheet.getRange('A2:G200');
  const evenRowRule = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=ISEVEN(ROW())')
    .setBackground('#f8f9fa')
    .setRanges([dataRange])
    .build();

  sheet.setConditionalFormatRules([sentRule, writtenRule, envelopeRule, pendingRule, brideRule, groomRule, evenRowRule]);

  // Column widths
  sheet.setColumnWidth(1, 250);  // Guest Name
  sheet.setColumnWidth(2, 80);   // Side
  sheet.setColumnWidth(3, 130);  // Status
  sheet.setColumnWidth(4, 300);  // Address
  sheet.setColumnWidth(5, 350);  // Gift Description
  sheet.setColumnWidth(6, 100);  // Gift Amount
  sheet.setColumnWidth(7, 80);   // Timing

  // Freeze header
  sheet.setFrozenRows(1);

  // Add filter
  sheet.getRange('A1:G' + (data.length + 1)).createFilter();

  // Center align some columns
  sheet.getRange('B:B').setHorizontalAlignment('center');
  sheet.getRange('C:C').setHorizontalAlignment('center');
  sheet.getRange('F:F').setHorizontalAlignment('right');
  sheet.getRange('G:G').setHorizontalAlignment('center');
}

function createByStatusTab(ss) {
  let sheet = ss.getSheetByName('Action Items');
  if (!sheet) {
    sheet = ss.insertSheet('Action Items');
  }
  sheet.clear();

  // Colors
  const headerBg = '#1a73e8';
  const headerText = '#ffffff';
  const urgentBg = '#ffcdd2';

  // Title
  sheet.getRange('A1:D1').merge().setValue('📋 Action Items - Notes Still Needed').setFontSize(16).setFontWeight('bold').setFontColor('#1a73e8');
  sheet.setRowHeight(1, 40);

  // Headers
  sheet.getRange('A3:D3').setValues([['Guest Name', 'Status', 'Address', 'Gift']]).setFontWeight('bold').setBackground(headerBg).setFontColor(headerText);

  // Formula to pull guests with pending notes
  sheet.getRange('A4').setFormula('=IFERROR(FILTER(\'Gift List\'!A2:A,\'Gift List\'!C2:C="Note Pending"),"All done!")');
  sheet.getRange('B4').setFormula('=IFERROR(FILTER(\'Gift List\'!C2:C,\'Gift List\'!C2:C="Note Pending"),"")');
  sheet.getRange('C4').setFormula('=IFERROR(FILTER(\'Gift List\'!D2:D,\'Gift List\'!C2:C="Note Pending"),"")');
  sheet.getRange('D4').setFormula('=IFERROR(FILTER(\'Gift List\'!E2:E,\'Gift List\'!C2:C="Note Pending"),"")');

  // Highlight urgent items
  const urgentRange = sheet.getRange('A4:D50');
  const urgentRule = SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=$B4="Note Pending"')
    .setBackground(urgentBg)
    .setRanges([urgentRange])
    .build();
  sheet.setConditionalFormatRules([urgentRule]);

  // Column widths
  sheet.setColumnWidth(1, 250);
  sheet.setColumnWidth(2, 120);
  sheet.setColumnWidth(3, 300);
  sheet.setColumnWidth(4, 350);

  // Freeze header
  sheet.setFrozenRows(3);
}
