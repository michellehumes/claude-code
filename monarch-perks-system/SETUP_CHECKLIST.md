# Monarch Credit Card Perks Tracker - Setup Checklist

## Prerequisites
- [ ] Google account with access to Google Sheets and Google Drive
- [ ] Monarch Finance account with ability to export CSVs
- [ ] Your Balances CSV export (Date, Balance, Account columns)
- [ ] Your Transactions CSV export (2026 transactions)

---

## Step 1: Create Google Sheet

1. [ ] Go to [sheets.google.com](https://sheets.google.com)
2. [ ] Click **+ Blank** to create a new spreadsheet
3. [ ] Name it: `Credit Card Perks Tracker 2026`
4. [ ] Note the URL - you'll see something like: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`

---

## Step 2: Open Apps Script Editor

1. [ ] In your new Google Sheet, go to **Extensions** → **Apps Script**
2. [ ] This opens the Apps Script editor in a new tab
3. [ ] You'll see a default `Code.gs` file with an empty `myFunction()`

---

## Step 3: Install the Code

1. [ ] Delete all existing code in `Code.gs`
2. [ ] Open the `Code.gs` file from this repository
3. [ ] Copy the ENTIRE contents (Ctrl+A, Ctrl+C)
4. [ ] Paste into the Apps Script editor (Ctrl+V)
5. [ ] Click the **Save** icon (💾) or press Ctrl+S
6. [ ] Name the project: `MonarchPerksTracker`

---

## Step 4: Run Initial Setup

1. [ ] In the Apps Script editor, select `setupSheet_IfNeeded` from the function dropdown
2. [ ] Click **Run** (▶️)
3. [ ] When prompted, click **Review Permissions**
4. [ ] Click **Advanced** → **Go to MonarchPerksTracker (unsafe)**
5. [ ] Click **Allow** to grant permissions
6. [ ] Wait for the setup to complete (~10-30 seconds)
7. [ ] Return to your Google Sheet - you should see all tabs created

### Tabs Created:
- ✅ Cards
- ✅ Perks Catalog
- ✅ Merchant_Aliases (pre-seeded with 40+ aliases)
- ✅ Monarch Categories Map (pre-seeded)
- ✅ Transactions_2026
- ✅ Perk Usage 2026
- ✅ Dashboard
- ✅ Config
- ✅ Log

---

## Step 5: Configure CSV Ingestion (Choose ONE method)

### Option A: Paste Method (Recommended for first-time setup)

1. [ ] Export Balances CSV from Monarch
2. [ ] Open the **Config** tab in your Google Sheet
3. [ ] Find the row "Paste Balances CSV below this row:"
4. [ ] Paste your CSV content directly below that row
5. [ ] Go to **🎯 Perks Tracker** menu → **Ingest Balances CSV (from Config tab)**

6. [ ] Export Transactions CSV from Monarch
7. [ ] Find the row "Paste Transactions CSV below this row:"
8. [ ] Paste your CSV content directly below that row
9. [ ] Go to **🎯 Perks Tracker** menu → **Ingest Transactions CSV (from Config tab)**

### Option B: Google Drive Method (For recurring updates)

1. [ ] Create a folder in Google Drive for your Monarch exports
2. [ ] Upload your `Balances_*.csv` file to that folder
3. [ ] Upload your `transactions-*.csv` file to that folder
4. [ ] Copy the folder ID from the URL: `https://drive.google.com/drive/folders/YOUR_FOLDER_ID`
5. [ ] In the Sheet, go to **🎯 Perks Tracker** → **Settings** → **Set Drive Folder ID**
6. [ ] Paste the folder ID and click OK
7. [ ] Go to **🎯 Perks Tracker** → **Ingest Balances CSV (from Drive)**
8. [ ] Go to **🎯 Perks Tracker** → **Ingest Transactions CSV (from Drive)**

---

## Step 6: Review and Normalize Cards

1. [ ] Go to the **Cards** tab
2. [ ] Review the extracted credit cards
3. [ ] **Delete** any non-credit-card accounts that slipped through
4. [ ] **Fill in** the Annual Fee column for each card
5. [ ] **Adjust** Benefit Year Start Month if different from January (1)
   - e.g., if your card anniversary is in March, enter `3`
6. [ ] Go to **🎯 Perks Tracker** → **Normalize Cards** to regenerate IDs if needed

---

## Step 7: Set Up Your Perks Catalog

### Option A: Use Sample Perks as Starting Point

1. [ ] In Apps Script, run the function `seedSamplePerks`
2. [ ] Return to the **Perks Catalog** tab
3. [ ] Edit the **Card ID** column to match YOUR actual Card IDs from the Cards tab
4. [ ] Delete perks for cards you don't have
5. [ ] Adjust Annual Values to match your specific card version

### Option B: Build from Scratch

Add a row for each perk with:

| Column | Description | Example |
|--------|-------------|---------|
| Perk ID | Unique identifier | `CSR_TRAVEL` |
| Card ID | Must match Cards tab | `CSR_1234` |
| Card Name | Human-readable | `Chase Sapphire Reserve` |
| Perk Name | Perk description | `$300 Travel Credit` |
| Category | Travel/Dining/Retail/etc | `Travel` |
| Annual Value | Dollar amount | `300` |
| Frequency | monthly/quarterly/annual/every_4_years | `annual` |
| Reset Rule | calendar/anniversary | `anniversary` |
| Merchant Keywords | Pipe-separated | `airline\|hotel\|lyft\|uber` |
| Monarch Category Match | Pipe-separated | `travel\|flights\|hotels` |
| Amount Pattern | Optional | `=100` or `15-35` or `~50` |
| Notes | Any notes | `Airline incidentals only` |

---

## Step 8: Run the Full Pipeline

1. [ ] Go to **🎯 Perks Tracker** → **Run Full Pipeline**
2. [ ] Wait for completion (~30-60 seconds depending on data volume)
3. [ ] Check the **Dashboard** tab for your results!

---

## Step 9: Install Nightly Trigger (Optional)

1. [ ] Go to **🎯 Perks Tracker** → **Install Nightly Trigger**
2. [ ] This will automatically run the pipeline at 2 AM daily
3. [ ] If using Drive method, new CSVs will be auto-ingested

---

## Step 10: Verify Everything Works

- [ ] **Cards tab**: Shows all your credit cards with IDs
- [ ] **Transactions_2026 tab**: Shows your transactions with Matched Perk IDs
- [ ] **Perk Usage 2026 tab**: Shows usage, remaining value, and pacing status
- [ ] **Dashboard tab**: Shows summary metrics and "behind" perks
- [ ] **Log tab**: Shows execution history

---

## Troubleshooting

### "No new cards to add"
- Your accounts may not contain credit card keywords
- Manually add cards to the Cards tab

### Transactions not matching to perks
1. Check the **Merchant_Aliases** tab - add missing aliases
2. Check the **Perks Catalog** - ensure Merchant Keywords are correct
3. Check the **Transactions_2026** Card ID column - ensure cards are matched

### "Behind" perks seem wrong
- Check the card's **Benefit Year Start Month** in Cards tab
- Check the perk's **Frequency** and **Reset Rule** in Perks Catalog

### Duplicates appearing
- The dedupe key is: Transaction ID (if present) OR Date+Merchant+Amount+Account+Description
- If duplicates have different Transaction IDs, they'll both appear
- Manually delete true duplicates if needed

---

## Quick Reference: Menu Options

| Menu Item | What It Does |
|-----------|--------------|
| Setup Sheet (if needed) | Creates all tabs and seed data |
| Ingest Balances CSV (from Config tab) | Parses pasted CSV, adds new cards |
| Ingest Transactions CSV (from Config tab) | Parses pasted CSV, adds new transactions |
| Ingest Balances CSV (from Drive) | Reads CSV from configured Drive folder |
| Ingest Transactions CSV (from Drive) | Reads CSV from configured Drive folder |
| Normalize Cards | Re-parses cards, generates missing IDs |
| Match Perks to Transactions | Scores and assigns perks to transactions |
| Calculate Usage & Pacing | Computes YTD usage and status |
| Update Dashboard | Refreshes dashboard metrics and tables |
| Run Full Pipeline | Runs normalize → match → calculate → dashboard |
| Install Nightly Trigger | Sets up 2 AM daily automation |
| Remove All Triggers | Removes all automated runs |

---

## Next Steps

1. Review the [MAINTENANCE_GUIDE.md](./MAINTENANCE_GUIDE.md) for ongoing usage
2. Customize Merchant_Aliases for your specific merchants
3. Add all your card perks to the Perks Catalog
4. Set up monthly export routine from Monarch
