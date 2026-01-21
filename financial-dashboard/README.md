# 📊 Comprehensive Financial Dashboard

A complete financial tracking and management system built for Google Sheets with 11 integrated tabs for tracking transactions, budgets, spending, tasks, gifts, health, and more.

## 🎯 Overview

This financial dashboard automatically calculates and visualizes your financial data from a single transactions CSV file. It includes both financial tracking (auto-calculated from your transaction data) and lifestyle management tabs (manual entry templates).

### Dashboard Features

**Financial Tabs (Auto-Calculated):**
1. **📊 Transactions** - Central data repository with all transaction data
2. **💳 Credit Cards** - Account balances and spending summaries
3. **📊 Budget Master** - Budget vs. actual spending with progress tracking
4. **📈 Spending by Category** - Monthly, quarterly, and YTD spending analysis
5. **💰 Monthly Summary** - Income, expenses, net, and savings rate by month
6. **📊 Spending by Merchant** - Top merchant analysis

**Lifestyle Tabs (Manual Entry Templates):**
7. **✅ Master Tasks** - Task management with priorities and due dates
8. **🎁 Gift Tracker** - Gift planning and budget tracking
9. **🩺 Health Dashboard** - Weight, workouts, and appointments tracking
10. **📅 Calendar View** - Monthly calendar with daily spending totals
11. **📋 Dashboard** - Executive summary with key financial metrics

## 📋 Prerequisites

### Required CSV Format

Your transaction CSV file must have these 9 columns in this exact order:

```
Date, Merchant, Category, Account, Original Statement, Notes, Amount, Tags, Owner
```

**Example:**
```csv
Date,Merchant,Category,Account,Original Statement,Notes,Amount,Tags,Owner
2026-01-09,Spotify,Music,Venture (...4522),Spotify USA,,-11.99,,Shared
2026-01-09,Target,Shopping,Target Circle Card (...2828),TARGET 1818,,-130.36,,Shared
```

**Important Notes:**
- **Date**: Format as YYYY-MM-DD
- **Amount**: Negative for expenses, positive for income
- **Category**: Keep categories consistent for accurate budget tracking
- **Account**: Use consistent account names for credit card tracking

## 🚀 Setup Instructions

### Option 1: Manual Setup (Recommended for Most Users)

#### Step 1: Setup the Google Sheet

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw/edit

2. Click **Extensions > Apps Script**

3. Delete any existing code in the script editor

4. Copy the entire contents of `FinancialDashboard.gs` and paste it into the script editor

5. Click the **Save** icon (disk icon) or press `Ctrl+S` (Windows) / `Cmd+S` (Mac)

6. Name your project "Financial Dashboard" when prompted

#### Step 2: Run the Setup

1. In the Apps Script editor, select the function `setupFinancialDashboard` from the dropdown menu at the top

2. Click the **Run** button (play icon)

3. The first time you run it, you'll need to authorize the script:
   - Click **Review Permissions**
   - Choose your Google account
   - Click **Advanced** (if you see a warning)
   - Click **Go to Financial Dashboard (unsafe)**
   - Click **Allow**

4. Wait for the script to complete (you'll see "Execution completed" in the log)

5. Return to your Google Sheet - you should now see all 11 tabs!

#### Step 3: Import Your Transaction Data

**Method A: Manual Import (Simple)**

1. Go to the **📊 Transactions** tab in your Google Sheet

2. Click **File > Import**

3. Upload your CSV file

4. In the import dialog:
   - Import location: **Append rows to current sheet**
   - Separator type: **Comma**
   - Convert text: **Yes**

5. Click **Import data**

6. Your data will appear starting at row 2 (below the headers)

**Method B: Python Script (For Large Files)**

If you have a large CSV file (10,000+ rows), use the Python script for faster import:

1. Install required Python packages:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas
   ```

2. Set up Google Cloud credentials:
   - Go to https://console.cloud.google.com/
   - Create a new project or select an existing one
   - Enable the Google Sheets API
   - Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
   - Choose **Desktop app**
   - Download the JSON file and save it as `credentials.json` in the same folder as the Python script

3. Run the import script:
   ```bash
   python import_csv_to_sheets.py /path/to/your/Transactions.csv 1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw
   ```

4. The first time you run it, a browser window will open asking you to authorize the application

5. The script will clear any existing transaction data and import your CSV

#### Step 4: Configure Financial Tabs

After importing your data, you need to add your specific accounts, categories, and merchants:

**1. Credit Cards Tab (💳)**
- In cell A2, enter your first credit card account name (exactly as it appears in the Transactions tab)
- Copy row 2 down for each additional account
- All formulas will auto-calculate based on the account name

**2. Budget Master Tab (📊)**
- In column A, enter each spending category from your Transactions tab
- In column B, enter your monthly budget for each category
- Columns C-E will auto-calculate actual spending, remaining budget, and % used

**3. Spending by Category Tab (📈)**
- In column A, list all your spending categories
- Copy row 2 down for each category
- All spending metrics will auto-calculate

**4. Spending by Merchant Tab (📊)**
- In column A, list your top merchants (you can find these by sorting the Transactions tab)
- Copy row 2 down for up to 100 merchants
- Transaction counts and spending totals will auto-calculate

#### Step 5: Use Non-Financial Tabs

The remaining tabs are templates for manual data entry:

- **✅ Master Tasks**: Track to-dos with priorities and due dates
- **🎁 Gift Tracker**: Plan gifts and track spending
- **🩺 Health Dashboard**: Log weight, workouts, and appointments
- **📅 Calendar View**: View daily spending in a calendar format
- **📋 Dashboard**: Your executive summary (auto-updates from other tabs)

### Option 2: Quick Menu Access

After the initial setup, a custom menu will appear:

1. Click **Financial Dashboard** in the menu bar

2. Choose:
   - **Setup Dashboard**: Re-run the full setup (will delete and recreate all tabs)
   - **Import CSV Data**: View import instructions

## 📊 Using the Dashboard

### Dashboard Tab (📋)

This is your command center with real-time metrics:

- **Account Balances**: Total across all accounts
- **This Month**: Spending, income, net, and savings rate
- **Year to Date**: Cumulative totals
- **Budget Status**: Overall budget performance
- **Quick Stats**: Transaction count, active accounts, pending tasks

All data on this tab automatically updates as you modify data in other tabs.

### Understanding the Formulas

All financial calculations reference the **📊 Transactions** tab:

- **SUMIF**: Calculates totals for a specific account or category
- **SUMIFS**: Calculates totals with multiple conditions (e.g., specific month AND category)
- **TODAY()**: Used for current month calculations
- **DATE()**: Creates date ranges for historical analysis

### Monthly Summary Calculations

The **💰 Monthly Summary** tab uses these calculations:

- **Total Income**: Sum of all positive amounts in a month
- **Total Expenses**: Sum of all negative amounts (converted to positive for display)
- **Net**: Income minus Expenses
- **Savings Rate**: Net divided by Income (as a percentage)

### Budget Tracking

The **📊 Budget Master** tab helps you stay on track:

- **Budget Amount**: Your monthly budget for each category (manual entry)
- **Actual Spent**: Auto-calculated from transactions (expenses only)
- **Remaining**: Budget minus Actual
- **% Used**: Visual indicator of budget consumption
- Cells turn red when you've used >90% of a category budget

## 🎨 Customization

### Changing Colors

All headers use the color scheme:
- **Background**: #4A86E8 (blue)
- **Text**: #FFFFFF (white)

To change colors:
1. Open Apps Script editor
2. Find and replace color codes (e.g., `#4A86E8` → your preferred color)
3. Re-run `setupFinancialDashboard`

### Adding Custom Categories

To add a custom spending category:

1. Add transactions with the new category in the **📊 Transactions** tab
2. Add the category name to relevant tracking tabs:
   - **📊 Budget Master** (with budget amount)
   - **📈 Spending by Category**
3. Formulas will automatically calculate for the new category

### Modifying Date Ranges

To change the year in **💰 Monthly Summary**:

1. Open Apps Script editor
2. Find `createMonthlySummaryTab` function
3. Change `const currentYear = new Date().getFullYear();` to a specific year
4. Re-run the setup

## 🔧 Troubleshooting

### "Reference Does Not Exist" Errors

**Problem**: Formulas show #REF! errors

**Solution**:
- Make sure the **📊 Transactions** tab exists and has data
- Check that tab names match exactly (including emojis)
- Re-run the `setupFinancialDashboard` function

### Formulas Not Calculating

**Problem**: Cells show formulas as text instead of calculating

**Solution**:
- Make sure cells aren't formatted as "Plain text"
- Select the cells → Format → Number → Automatic
- Check that data types match (dates as dates, numbers as numbers)

### Import Fails

**Problem**: CSV import doesn't work

**Solution**:
- Check CSV format matches exactly: Date, Merchant, Category, Account, Original Statement, Notes, Amount, Tags, Owner
- Make sure dates are in YYYY-MM-DD format
- Ensure amounts are numbers (negative for expenses)
- Remove any special characters from headers

### Slow Performance

**Problem**: Sheet is slow with large datasets

**Solution**:
- Google Sheets works best with <50,000 rows
- If you have more data, consider splitting by year
- Remove unnecessary formulas from unused rows
- Use filters instead of creating multiple sheets

### Python Script Authorization Issues

**Problem**: "credentials.json not found" or authorization fails

**Solution**:
1. Make sure you've downloaded credentials from Google Cloud Console
2. File must be named exactly `credentials.json`
3. Must be in the same directory as the Python script
4. Delete `token.pickle` and re-authorize if you see permission errors

## 📁 File Structure

```
financial-dashboard/
├── FinancialDashboard.gs      # Main Apps Script for Google Sheets
├── import_csv_to_sheets.py    # Python script for CSV import
├── README.md                   # This file
└── credentials.json            # Your Google Cloud credentials (you create this)
```

## 🔒 Privacy & Security

- All data stays in your Google Sheet - nothing is sent to external servers
- The Apps Script only accesses your specific spreadsheet
- Python script requires explicit authorization via OAuth 2.0
- You can revoke access anytime in your Google Account settings

## 📝 Tips & Best Practices

### For Accurate Tracking

1. **Consistent Naming**: Use the same name for accounts and categories every time
2. **Regular Updates**: Import transactions weekly or monthly
3. **Category Standardization**: Create a list of standard categories and stick to it
4. **Account Abbreviations**: Use last 4 digits in parentheses: "Card (...1234)"

### For Better Insights

1. **Review Monthly**: Check the **💰 Monthly Summary** at month-end
2. **Budget Adjustments**: Update budgets in **📊 Budget Master** quarterly
3. **Top Merchants**: Use **📊 Spending by Merchant** to identify spending patterns
4. **Category Trends**: Watch **📈 Spending by Category** for unusual spikes

### For Performance

1. **Archive Old Data**: Move transactions older than 2 years to a separate sheet
2. **Delete Unused Formulas**: Remove formula rows you're not using
3. **Freeze Panes**: Keep headers frozen for easy navigation
4. **Use Filters**: Instead of creating multiple views, use filters on existing tabs

## 🆘 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review the Apps Script execution log: **View > Logs**
3. Make sure you're using the latest version of the scripts
4. Try re-running the `setupFinancialDashboard` function

## 📜 License

This financial dashboard is provided as-is for personal use. Feel free to modify and customize for your needs.

## 🙏 Acknowledgments

Built with:
- Google Apps Script
- Google Sheets API
- Python + Google Client Libraries

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Compatible With**: Google Sheets (Web)

## 🚀 Quick Start Checklist

- [ ] Copy `FinancialDashboard.gs` to Apps Script editor
- [ ] Run `setupFinancialDashboard` function
- [ ] Authorize the script
- [ ] Import CSV data to **📊 Transactions** tab
- [ ] Add account names to **💳 Credit Cards** tab
- [ ] Add categories and budgets to **📊 Budget Master** tab
- [ ] Add categories to **📈 Spending by Category** tab
- [ ] Add top merchants to **📊 Spending by Merchant** tab
- [ ] Review **📋 Dashboard** for your financial summary
- [ ] Start using lifestyle tabs (Tasks, Gifts, Health)

**That's it! Your comprehensive financial dashboard is ready to use! 🎉**
