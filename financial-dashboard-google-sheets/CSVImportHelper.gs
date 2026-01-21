/**
 * CSV Import Helper for Financial Dashboard
 *
 * This optional script adds a custom menu to import CSV data automatically.
 *
 * To use:
 * 1. In Google Apps Script editor, create a new file: CSVImportHelper.gs
 * 2. Paste this code
 * 3. Save and refresh your Google Sheet
 * 4. You'll see a new "Financial Tools" menu
 * 5. Use "Import CSV from URL" to import directly from a public URL
 */

// Creates custom menu when sheet opens
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('💰 Financial Tools')
    .addItem('📥 Import CSV from URL', 'importCSVFromURL')
    .addItem('🔄 Refresh All Calculations', 'refreshCalculations')
    .addSeparator()
    .addItem('📊 Rebuild Dashboard', 'buildFinancialDashboard')
    .addToUi();
}

// Import CSV from a public URL
function importCSVFromURL() {
  const ui = SpreadsheetApp.getUi();

  // Prompt for URL
  const response = ui.prompt(
    'Import CSV from URL',
    'Enter the URL of your CSV file (must be publicly accessible):',
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() === ui.Button.OK) {
    const url = response.getResponseText().trim();

    if (!url) {
      ui.alert('Error', 'Please provide a valid URL.', ui.ButtonSet.OK);
      return;
    }

    try {
      // Fetch CSV data
      const csvData = UrlFetchApp.fetch(url).getContentText();

      // Parse CSV
      const rows = Utilities.parseCsv(csvData);

      if (rows.length === 0) {
        ui.alert('Error', 'CSV file is empty.', ui.ButtonSet.OK);
        return;
      }

      // Get Transactions sheet
      const ss = SpreadsheetApp.getActiveSpreadsheet();
      const sheet = ss.getSheetByName('📊 Transactions');

      if (!sheet) {
        ui.alert('Error', 'Transactions sheet not found. Please run buildFinancialDashboard first.', ui.ButtonSet.OK);
        return;
      }

      // Clear existing data (except header)
      const lastRow = sheet.getLastRow();
      if (lastRow > 1) {
        sheet.getRange(2, 1, lastRow - 1, 9).clearContent();
      }

      // Import data starting from row 2 (skip CSV header)
      const dataRows = rows.slice(1); // Skip header row from CSV

      if (dataRows.length > 0) {
        // Ensure all rows have 9 columns
        const formattedRows = dataRows.map(row => {
          while (row.length < 9) row.push('');
          return row.slice(0, 9);
        });

        sheet.getRange(2, 1, formattedRows.length, 9).setValues(formattedRows);

        // Format Amount column as currency
        sheet.getRange(2, 7, formattedRows.length, 1).setNumberFormat('$#,##0.00');

        // Format Date column
        sheet.getRange(2, 1, formattedRows.length, 1).setNumberFormat('yyyy-mm-dd');

        ui.alert(
          'Success!',
          `Imported ${formattedRows.length} transactions successfully!\\n\\nAll financial tabs will now auto-calculate.`,
          ui.ButtonSet.OK
        );
      } else {
        ui.alert('Error', 'No data rows found in CSV (only header).', ui.ButtonSet.OK);
      }

    } catch (error) {
      ui.alert('Error', `Failed to import CSV: ${error.message}\\n\\nMake sure the URL is publicly accessible.`, ui.ButtonSet.OK);
      Logger.log('CSV Import Error: ' + error);
    }
  }
}

// Import CSV from file (requires manual file selection)
function importCSVFromFile() {
  const ui = SpreadsheetApp.getUi();

  ui.alert(
    'Manual Import Required',
    'To import a CSV file from your computer:\\n\\n' +
    '1. Go to the 📊 Transactions tab\\n' +
    '2. Click File > Import\\n' +
    '3. Upload your CSV file\\n' +
    '4. Select "Replace data at selected cell"\\n' +
    '5. Click cell A2\\n' +
    '6. Click Import',
    ui.ButtonSet.OK
  );
}

// Refresh all calculations
function refreshCalculations() {
  SpreadsheetApp.flush();
  SpreadsheetApp.getActiveSpreadsheet().toast('All calculations refreshed!', 'Success ✓', 3);
}

// Parse transaction data and auto-create unique accounts in Credit Cards tab
function autoPopulateCreditCards() {
  const ui = SpreadsheetApp.getUi();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const transSheet = ss.getSheetByName('📊 Transactions');
  const ccSheet = ss.getSheetByName('💳 Credit Cards');

  if (!transSheet || !ccSheet) {
    ui.alert('Error', 'Required sheets not found.', ui.ButtonSet.OK);
    return;
  }

  try {
    // Get all accounts from Transactions (column D)
    const lastRow = transSheet.getLastRow();
    if (lastRow < 2) {
      ui.alert('Error', 'No transaction data found.', ui.ButtonSet.OK);
      return;
    }

    const accountsData = transSheet.getRange(2, 4, lastRow - 1, 1).getValues();

    // Get unique accounts
    const uniqueAccounts = [...new Set(accountsData.flat().filter(acc => acc !== ''))];

    if (uniqueAccounts.length === 0) {
      ui.alert('Error', 'No accounts found in transactions.', ui.ButtonSet.OK);
      return;
    }

    // Clear existing data in Credit Cards (keep header)
    const ccLastRow = ccSheet.getLastRow();
    if (ccLastRow > 1) {
      ccSheet.getRange(2, 1, ccLastRow - 1, 5).clearContent();
    }

    // Create rows for each unique account
    const accountRows = uniqueAccounts.map((account, index) => {
      const row = index + 2;
      return [
        account,
        `=SUMIF('📊 Transactions'!D:D,A${row},'📊 Transactions'!G:G)`,
        `=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!D:D,A${row},'📊 Transactions'!A:A,">="&EOMONTH(TODAY(),-1)+1,'📊 Transactions'!A:A,"<="&EOMONTH(TODAY(),0))`,
        `=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!D:D,A${row},'📊 Transactions'!A:A,">="&DATE(YEAR(TODAY()),1,1))`,
        `=MAXIFS('📊 Transactions'!A:A,'📊 Transactions'!D:D,A${row})`
      ];
    });

    ccSheet.getRange(2, 1, accountRows.length, 5).setValues(accountRows);

    // Format currency and date columns
    ccSheet.getRange(2, 2, accountRows.length, 3).setNumberFormat('$#,##0.00');
    ccSheet.getRange(2, 5, accountRows.length, 1).setNumberFormat('yyyy-mm-dd');

    ui.alert(
      'Success!',
      `Populated ${uniqueAccounts.length} unique accounts in Credit Cards tab.`,
      ui.ButtonSet.OK
    );

  } catch (error) {
    ui.alert('Error', `Failed to populate accounts: ${error.message}`, ui.ButtonSet.OK);
    Logger.log('Auto-populate Error: ' + error);
  }
}

// Parse transaction data and auto-create unique categories in Budget Master
function autoPopulateBudgetCategories() {
  const ui = SpreadsheetApp.getUi();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const transSheet = ss.getSheetByName('📊 Transactions');
  const budgetSheet = ss.getSheetByName('📊 Budget Master');

  if (!transSheet || !budgetSheet) {
    ui.alert('Error', 'Required sheets not found.', ui.ButtonSet.OK);
    return;
  }

  try {
    // Get all categories from Transactions (column C)
    const lastRow = transSheet.getLastRow();
    if (lastRow < 2) {
      ui.alert('Error', 'No transaction data found.', ui.ButtonSet.OK);
      return;
    }

    const categoriesData = transSheet.getRange(2, 3, lastRow - 1, 1).getValues();

    // Get unique categories and sort
    const uniqueCategories = [...new Set(categoriesData.flat().filter(cat => cat !== ''))].sort();

    if (uniqueCategories.length === 0) {
      ui.alert('Error', 'No categories found in transactions.', ui.ButtonSet.OK);
      return;
    }

    // Clear existing data in Budget Master (keep header)
    const budgetLastRow = budgetSheet.getLastRow();
    if (budgetLastRow > 1) {
      budgetSheet.getRange(2, 1, budgetLastRow - 1, 5).clearContent();
    }

    // Create rows for each unique category
    const categoryRows = uniqueCategories.map((category, index) => {
      const row = index + 2;
      return [
        category,
        0, // Budget amount - user needs to fill this in
        `=SUMIF('📊 Transactions'!C:C,A${row},'📊 Transactions'!G:G)`,
        `=B${row}-C${row}`,
        `=IF(B${row}=0,0,C${row}/B${row})`
      ];
    });

    budgetSheet.getRange(2, 1, categoryRows.length, 5).setValues(categoryRows);

    // Format currency and percentage columns
    budgetSheet.getRange(2, 2, categoryRows.length, 3).setNumberFormat('$#,##0.00');
    budgetSheet.getRange(2, 5, categoryRows.length, 1).setNumberFormat('0.0%');

    // Add total row
    const totalRow = categoryRows.length + 2;
    budgetSheet.getRange(totalRow, 1).setValue('TOTAL');
    budgetSheet.getRange(totalRow, 2).setFormula(`=SUM(B2:B${totalRow - 1})`);
    budgetSheet.getRange(totalRow, 3).setFormula(`=SUM(C2:C${totalRow - 1})`);
    budgetSheet.getRange(totalRow, 4).setFormula(`=SUM(D2:D${totalRow - 1})`);
    budgetSheet.getRange(totalRow, 1, 1, 5).setBackground('#E8F4F8').setFontWeight('bold');

    ui.alert(
      'Success!',
      `Populated ${uniqueCategories.length} unique categories in Budget Master.\\n\\nPlease update the Budget Amount column (B) with your target spending for each category.`,
      ui.ButtonSet.OK
    );

  } catch (error) {
    ui.alert('Error', `Failed to populate categories: ${error.message}`, ui.ButtonSet.OK);
    Logger.log('Auto-populate Error: ' + error);
  }
}

// Enhanced onOpen with more tools
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('💰 Financial Tools')
    .addItem('📥 Import CSV from URL', 'importCSVFromURL')
    .addSeparator()
    .addItem('🔄 Auto-populate Credit Cards', 'autoPopulateCreditCards')
    .addItem('🔄 Auto-populate Budget Categories', 'autoPopulateBudgetCategories')
    .addSeparator()
    .addItem('♻️ Refresh All Calculations', 'refreshCalculations')
    .addItem('🔧 Rebuild Entire Dashboard', 'buildFinancialDashboard')
    .addToUi();
}
