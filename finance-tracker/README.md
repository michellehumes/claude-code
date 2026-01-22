# Personal Finance Tracker

A web-based personal finance tracker that helps you analyze and visualize your spending patterns.

## Features

- **CSV Import**: Upload transaction data from your bank or financial app (Monarch, Mint, etc.)
- **Financial Summary**: View total income, expenses, and net cash flow at a glance
- **Spending Analysis**: Interactive charts showing spending by category and over time
- **Category Breakdown**: Detailed table showing spending per category with percentage bars
- **Account Summary**: Track activity across all your accounts
- **Transaction Filtering**: Filter by date range, category, account, or search by merchant
- **Sortable Tables**: Click column headers to sort transactions
- **Pagination**: Handle large datasets with paginated transaction views

## How to Use

### Option 1: Open Directly in Browser
Simply open `index.html` in your web browser.

### Option 2: Run with Local Server
For the best experience (needed if loading sample data from file):

```bash
cd finance-tracker
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Loading Your Data

1. **Upload CSV**: Click "Upload CSV File" and select your transactions CSV
2. **Sample Data**: Click "Load Sample Data" to see the tracker in action

### Supported CSV Format

Your CSV should have these columns:
- `Date` - Transaction date (YYYY-MM-DD format)
- `Merchant` - Merchant/payee name
- `Category` - Transaction category
- `Account` - Account name
- `Amount` - Transaction amount (negative for expenses, positive for income)
- `Owner` - (Optional) Who made the transaction

Example:
```csv
Date,Merchant,Category,Account,Original Statement,Notes,Amount,Tags,Owner
2026-01-15,Amazon,Shopping,Chase Checking,AMAZON MKTPL,,-45.99,,Shared
2026-01-07,Payroll,Paychecks,Chase Checking,EMPLOYER PAYROLL,,2500.00,,John
```

## Screenshots

The tracker displays:
- Summary cards with income/expenses/net flow
- Doughnut chart of spending by category
- Bar chart showing income vs expenses over time
- Detailed category breakdown with progress bars
- Account-by-account summary
- Filterable and sortable transaction list

## Exporting from Monarch

If you use Monarch Money:
1. Go to your Monarch dashboard
2. Navigate to Transactions
3. Click Export to download your CSV
4. Upload the file to this tracker

## Tech Stack

- Pure HTML/CSS/JavaScript (no build required)
- Chart.js for data visualization
- Responsive design for mobile and desktop
