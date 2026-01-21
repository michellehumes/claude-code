# Quick Setup Guide - Financial Dashboard

Get your financial dashboard running in 5 minutes!

## Step 1: Open Your Google Sheet
**URL:** https://docs.google.com/spreadsheets/d/1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw/edit

## Step 2: Install the Script (One-Time Setup)

1. In Google Sheets: **Extensions > Apps Script**
2. Delete any existing code
3. Copy **ALL** code from `Code.gs` in this repository
4. Paste into the Apps Script editor
5. Click **💾 Save** (name it "Financial Dashboard")
6. Click **▶️ Run** → Select `buildFinancialDashboard`
7. **Authorize** when prompted:
   - Click "Review permissions"
   - Choose your Google account
   - Click "Advanced" → "Go to Financial Dashboard Builder (unsafe)"
   - Click "Allow"
8. Wait 30-60 seconds for completion
9. You'll see: "Financial Dashboard Created!" alert

## Step 3: Import Your Transaction Data

### Option A: From Your CSV File
1. Go to **📊 Transactions** tab
2. **File > Import**
3. **Upload** your CSV: `Transactions_20260120T223550.csv`
4. Settings:
   - Import location: **Replace data at selected cell**
   - Click cell **A2** (not A1!)
   - Separator: **Comma**
5. Click **Import Data**

### Option B: Copy from Sample CSV
1. Open `Transactions_20260120T223550.csv` in a text editor
2. Copy all transaction rows (skip the header row)
3. In Google Sheets, click cell **A2** in the Transactions tab
4. Paste (Ctrl+V or Cmd+V)

## Step 4: Customize Your Budgets

1. Go to **📊 Budget Master** tab
2. Update column **B** (Budget Amount) with your target spending for each category
3. All calculations update automatically!

## Step 5: Explore Your Dashboard

1. Click **📋 Dashboard** tab (should be first tab)
2. Review key metrics:
   - Total balances
   - This month spending
   - Budget status
   - Spending trends

## That's It!

All 11 tabs are now active with your data:

### Financial Tabs (Auto-Calculated)
- 📊 Transactions
- 💳 Credit Cards
- 📊 Budget Master
- 📈 Spending by Category
- 💰 Monthly Summary
- 📊 Spending by Merchant

### Personal Productivity Tabs (Manual Entry)
- ✅ Master Tasks
- 🎁 Gift Tracker
- 🩺 Health Dashboard
- 📅 Calendar View
- 📋 Dashboard (Overview)

## Quick Tips

### Adding New Transactions
1. Go to Transactions tab
2. Add new rows at the bottom
3. All tabs auto-update!

### Updating Budgets
1. Budget Master tab → Column B
2. Change budget amounts as needed

### Viewing Trends
- Monthly Summary: 12-month overview
- Spending by Category: Current trends
- Dashboard: Executive summary

## Troubleshooting

**Problem:** Formulas show #REF!
**Solution:** Import transactions into cell A2 of Transactions tab

**Problem:** Numbers not calculating
**Solution:** Make sure Amount column has numbers (not text), dates are formatted as dates

**Problem:** Can't import CSV
**Solution:** Ensure CSV has these 9 columns: Date,Merchant,Category,Account,Original Statement,Notes,Amount,Tags,Owner

## Need More Help?

See the full **README.md** for:
- Detailed feature explanations
- Formula reference
- Advanced customization
- Custom reports

---

**🎉 You're all set! Your financial dashboard is ready to use.**
