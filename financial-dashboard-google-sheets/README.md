# Financial Dashboard for Google Sheets

A comprehensive, automated financial tracking system with 11 specialized tabs including transaction tracking, budget management, spending analytics, and personal productivity tools.

## Features

### Financial Tabs (Auto-calculated from transaction data)
1. **📊 Transactions** - Main transaction import with filters and formatting
2. **💳 Credit Cards** - Account summaries with automatic balance calculations
3. **📊 Budget Master** - Category budgets with actual vs. planned tracking
4. **📈 Spending by Category** - Monthly and YTD spending trends
5. **💰 Monthly Summary** - Income, expenses, and savings rate over time
6. **📊 Spending by Merchant** - Top merchants and transaction patterns

### Personal Productivity Tabs (Manual entry templates)
7. **✅ Master Tasks** - Task management with priorities and due dates
8. **🎁 Gift Tracker** - Gift planning and budget tracking
9. **🩺 Health Dashboard** - Weight log, workouts, and medical appointments
10. **📅 Calendar View** - Monthly spending calendar visualization
11. **📋 Dashboard** - Executive summary with key metrics and trends

## Quick Start

### Step 1: Open Your Google Sheet
Open your Google Sheet at:
https://docs.google.com/spreadsheets/d/1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw/edit

### Step 2: Add the Google Apps Script

1. In your Google Sheet, go to **Extensions > Apps Script**
2. Delete any existing code in the editor
3. Copy the entire contents of `Code.gs` from this repository
4. Paste it into the Apps Script editor
5. Click **Save** (Ctrl+S or Cmd+S)
6. Name the project "Financial Dashboard Builder"

### Step 3: Run the Script

1. In the Apps Script editor, select the function **buildFinancialDashboard** from the dropdown
2. Click **Run** (▶️ button)
3. You'll be prompted to authorize the script:
   - Click **Review permissions**
   - Choose your Google account
   - Click **Advanced** → **Go to Financial Dashboard Builder (unsafe)**
   - Click **Allow**
4. Wait for the script to complete (30-60 seconds)
5. You'll see a success message when done

### Step 4: Import Your Transaction Data

1. Navigate to the **📊 Transactions** tab in your Google Sheet
2. Click **File > Import**
3. Choose **Upload** and select your CSV file: `Transactions_20260120T223550.csv`
4. In the import settings:
   - **Import location**: Select "Replace data at selected cell"
   - Click on cell **A2** (important: not A1, to preserve headers)
   - **Separator type**: Comma
   - **Convert text to numbers**: Yes
5. Click **Import Data**
6. Your transactions will appear, and all other financial tabs will automatically calculate

### Step 5: Customize Your Dashboard

After importing transactions:

1. **📊 Budget Master**: Update the "Budget Amount" column (Column B) with your target spending for each category
2. **💳 Credit Cards**: Add or remove account rows as needed, copy formulas from existing rows
3. **📋 Dashboard**: All metrics will auto-populate from your data
4. **Personal Tabs**: Start adding tasks, gifts, health data as needed

## Understanding the Financial Tabs

### 📊 Transactions
- **Purpose**: Central repository for all financial transactions
- **Columns**: Date, Merchant, Category, Account, Original Statement, Notes, Amount, Tags, Owner
- **Features**: Auto-filters, frozen headers, currency formatting
- **Usage**: Import CSV data here, all other tabs reference this data

### 💳 Credit Cards
- **Purpose**: Track balances and spending across all accounts
- **Auto-calculates**:
  - Current balance (sum of all transactions)
  - This month's spending
  - Year-to-date spending
  - Last transaction date
- **Usage**: Add rows for each account, formulas will auto-calculate from Transactions tab

### 📊 Budget Master
- **Purpose**: Set budgets and track actual spending
- **Features**:
  - Set budget amounts for each category
  - Actual spending auto-calculates from Transactions
  - Remaining budget shows what's left
  - % Used column with color coding (green = under 80%, yellow = 80-100%, red = over 100%)
- **Usage**: Enter your budget amounts in column B, everything else calculates automatically

### 📈 Spending by Category
- **Purpose**: Analyze spending trends across different time periods
- **Shows**:
  - This month vs. last month spending
  - 3-month average
  - Year-to-date totals
  - Percentage of total spending
- **Usage**: All data auto-calculates, use for monthly reviews

### 💰 Monthly Summary
- **Purpose**: Track income, expenses, and savings over time
- **Shows**: Last 12 months with:
  - Total income (positive transactions)
  - Total expenses (negative transactions, shown as positive)
  - Net (income - expenses)
  - Savings rate percentage
- **Features**: Color-coded savings rate (green = 20%+, yellow = 10-20%, red = under 10%)
- **Usage**: Review monthly to track financial progress

### 📊 Spending by Merchant
- **Purpose**: Identify where money is going
- **Shows**:
  - Transaction count per merchant
  - Total spent per merchant
  - Average transaction amount
  - Category
- **Usage**: Use to identify spending patterns and opportunities to cut costs

## Understanding the Personal Tabs

### ✅ Master Tasks
- **Purpose**: Track to-do items and projects
- **Columns**: Checkbox, Task, Priority (High/Medium/Low), Status, Due Date, Category, Notes
- **Features**: Drop-down menus for Priority and Status, color-coded status
- **Usage**: Add tasks, update status, track completion

### 🎁 Gift Tracker
- **Purpose**: Plan and budget for gifts
- **Columns**: Person, Occasion, Date, Gift Idea, Budget, Actual Cost, Purchased?, Store/Link, Notes
- **Usage**: Track gift ideas, budgets, and purchases throughout the year

### 🩺 Health Dashboard
- **Purpose**: Track health and wellness
- **Sections**:
  - Weight Log: Date, Weight, Notes
  - Workouts: Date, Type, Duration, Notes
  - Appointments: Date, Provider, Type, Notes, Follow-up
- **Usage**: Record health data for tracking progress

### 📅 Calendar View
- **Purpose**: Visualize daily spending patterns
- **Features**: Monthly calendar showing daily spending totals
- **Usage**: Currently a template, can be enhanced with formulas to pull from Transactions

### 📋 Dashboard
- **Purpose**: Executive summary and overview
- **Shows**:
  - Key metrics (balances, monthly spending, income, savings rate)
  - Budget status for top 5 categories
  - 3-month spending trends
- **Features**: All data auto-calculates from other tabs
- **Usage**: Your go-to view for quick financial overview

## CSV Data Format

Your transaction CSV should have these 9 columns:

```
Date,Merchant,Category,Account,Original Statement,Notes,Amount,Tags,Owner
```

- **Date**: YYYY-MM-DD format (e.g., 2026-01-15)
- **Merchant**: Name of merchant/business
- **Category**: Spending category (Rent, Shopping, Food, etc.)
- **Account**: Account name (e.g., "Venture (...4522)")
- **Original Statement**: Original transaction description
- **Notes**: Optional notes
- **Amount**: Transaction amount (negative for expenses, positive for income)
- **Tags**: Optional tags
- **Owner**: Transaction owner (Shared, Personal, etc.)

## Formulas Reference

### Key Formula Patterns

**This Month Spending:**
```
=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!A:A,">="&EOMONTH(TODAY(),-1)+1,'📊 Transactions'!A:A,"<="&EOMONTH(TODAY(),0))
```

**Year-to-Date Spending:**
```
=SUMIFS('📊 Transactions'!G:G,'📊 Transactions'!A:A,">="&DATE(YEAR(TODAY()),1,1))
```

**Category Total:**
```
=SUMIF('📊 Transactions'!C:C,A2,'📊 Transactions'!G:G)
```

**Savings Rate:**
```
=IF(Income=0,0,(Income-Expenses)/Income)
```

## Customization Tips

### Adding New Categories
1. Go to **📊 Budget Master** tab
2. Add a new row with the category name
3. Copy formulas from the row above
4. Update cell references in the formulas

### Adding New Accounts
1. Go to **💳 Credit Cards** tab
2. Add a new row with the account name
3. Copy formulas from the row above
4. Update cell references (A2 → A9, etc.)

### Modifying Date Ranges
- Current formulas use `TODAY()` function for dynamic date calculations
- Modify `EOMONTH(TODAY(),-1)` to change month offsets
  - `-1` = last month
  - `-2` = 2 months ago
  - `0` = current month

### Creating Custom Views
1. Use Google Sheets **Pivot Tables** for custom analysis
2. Reference the Transactions tab as your data source
3. Group by Category, Merchant, or Date as needed

## Troubleshooting

### "Import data" not working
- Ensure you're clicking cell A2 (not A1) before importing
- Check that your CSV is comma-separated
- Verify date format is YYYY-MM-DD

### Formulas showing #REF! errors
- Make sure Transactions tab has data imported
- Check that tab names haven't been changed (formulas reference tab names)
- Verify cell references are correct

### Numbers not calculating
- Ensure Amount column in Transactions has numbers, not text
- Check that dates are formatted as dates, not text
- Remove any extra spaces in category/merchant names

### Conditional formatting not showing colors
- Rerun the Apps Script to reapply formatting
- Or manually apply conditional formatting:
  - Select range → Format → Conditional formatting
  - Set rules based on cell values

## Advanced Features

### Auto-refresh with Macros
Create a custom menu to refresh data:

```javascript
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Financial Dashboard')
    .addItem('Refresh All Calculations', 'refreshCalculations')
    .addToUi();
}

function refreshCalculations() {
  SpreadsheetApp.flush();
  SpreadsheetApp.getActiveSpreadsheet().toast('Calculations refreshed!', 'Success');
}
```

### Export Reports
Use File > Download to export individual tabs:
- Dashboard → PDF for monthly reports
- Budget Master → CSV for backup
- Monthly Summary → Excel for analysis

### Sharing Settings
- **View only**: Share for read-only access
- **Comment**: Allow feedback without editing
- **Edit**: Full collaboration (be careful with formulas)

## File Structure

```
financial-dashboard-google-sheets/
├── Code.gs                          # Google Apps Script (paste into Extensions > Apps Script)
├── Transactions_20260120T223550.csv # Sample transaction data
└── README.md                        # This file
```

## Support & Customization

This dashboard is fully customizable. Common customizations:

1. **Add new metrics to Dashboard**: Reference any tab with `='Tab Name'!CellRange`
2. **Create new spending categories**: Add to Budget Master and formulas will work
3. **Track multiple users**: Use Owner column in Transactions, filter by user
4. **Add charts**: Insert > Chart, use any tab as data source

## Version History

- **v1.0** (2026-01-20): Initial release with 11 tabs and full automation

## License

Free to use and customize for personal financial tracking.

---

**Questions or Issues?**
Review the code comments in `Code.gs` for detailed explanations of each function and formula.
