# 🚀 Quick Start Guide - Financial Dashboard

## 5-Minute Setup

### Step 1: Open Your Google Sheet
Go to: https://docs.google.com/spreadsheets/d/1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw/edit

### Step 2: Add the Script
1. Click **Extensions > Apps Script**
2. Delete existing code
3. Copy all code from `FinancialDashboard.gs`
4. Paste into the editor
5. Click Save (💾)

### Step 3: Run Setup
1. Select `setupFinancialDashboard` from dropdown
2. Click Run (▶️)
3. Authorize when prompted (click "Advanced" → "Go to Financial Dashboard")
4. Wait for completion

### Step 4: Import Your Data
1. Go to **📊 Transactions** tab
2. Click **File > Import**
3. Upload your CSV file
4. Select **Append rows to current sheet**
5. Click **Import data**

### Step 5: Configure
Add your data to these tabs:

**💳 Credit Cards** (Column A)
- Enter each account name exactly as it appears in transactions
- Example: `Chase Sapphire (...1234)`

**📊 Budget Master** (Columns A & B)
- Column A: Category names from your transactions
- Column B: Your monthly budget for each category

**📈 Spending by Category** (Column A)
- List all your spending categories

**📊 Spending by Merchant** (Column A)
- List your top merchants

### Done! 🎉

Check the **📋 Dashboard** tab to see your financial summary.

---

## Your CSV Must Have These Columns:

```
Date, Merchant, Category, Account, Original Statement, Notes, Amount, Tags, Owner
```

**Example:**
```csv
2026-01-20,Starbucks,Coffee & Cafes,Chase (...1234),STARBUCKS STORE,-5.75,,Personal
```

- **Amount**: Negative for expenses, positive for income
- **Date**: Format as YYYY-MM-DD

---

## Need Help?

See the full `README.md` for detailed instructions and troubleshooting.

## What You Get:

✅ 11 Tabs:
- 📋 Dashboard (Executive Summary)
- 📊 Transactions (Your Data)
- 💳 Credit Cards (Account Tracking)
- 📊 Budget Master (Budget vs Actual)
- 📈 Spending by Category (Trend Analysis)
- 💰 Monthly Summary (Income/Expenses by Month)
- 📊 Spending by Merchant (Top Merchants)
- ✅ Master Tasks (To-Do List)
- 🎁 Gift Tracker (Gift Planning)
- 🩺 Health Dashboard (Health Tracking)
- 📅 Calendar View (Daily Spending Calendar)

✅ Auto-Calculated:
- Current balances
- Monthly spending by category
- Budget progress
- Savings rate
- YTD totals

✅ Beautiful Formatting:
- Color-coded headers
- Currency formatting
- Percentage displays
- Conditional formatting for budgets
