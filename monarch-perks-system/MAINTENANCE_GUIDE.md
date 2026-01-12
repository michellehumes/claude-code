# Monarch Credit Card Perks Tracker - Maintenance Guide

## Routine Maintenance Tasks

### Weekly: Refresh Transaction Data

1. Export new transactions from Monarch (filter to current year)
2. Either:
   - **Paste Method**: Replace CSV content in Config tab, run ingest
   - **Drive Method**: Upload new file to Drive folder, run ingest (or let nightly trigger handle it)
3. Run **Match Perks to Transactions** to assign perks to new transactions
4. Check **Dashboard** for updated pacing

### Monthly: Review Matches and Overrides

1. Go to **Transactions_2026** tab
2. Sort by `Match Confidence` ascending to find low-confidence matches
3. Review unmatched transactions (empty `Matched Perk ID`)
4. Add manual overrides where needed (see below)

### Quarterly: Audit Perks Catalog

1. Review each perk's **Used YTD** vs **Max Value**
2. Check for perks showing "Behind" that shouldn't be
3. Add new perks from card benefit changes
4. Remove perks from closed cards

### Annually: Year-End Reset

1. Archive current year's **Transactions_2026** and **Perk Usage 2026** data
2. Clear transactions for new year (or create new tabs)
3. Update `CONFIG.TRACKING_YEAR` in Code.gs if needed
4. Review and update perk values for the new year

---

## How to Update Perks

### Adding a New Perk

1. Go to **Perks Catalog** tab
2. Add a new row with all fields:

```
Perk ID:              CARD_PERKNAME (unique, e.g., PLAT_UBER)
Card ID:              Must match a Card ID from Cards tab
Card Name:            Human-readable card name
Perk Name:            Descriptive perk name
Category:             Travel|Dining|Retail|Subscriptions|Fees|Entertainment|Grocery|Gas|Fitness|Other
Annual Value:         Dollar amount (e.g., 200)
Frequency:            monthly|quarterly|annual|every_4_years|one_time
Reset Rule:           calendar|anniversary
Merchant Keywords:    pipe-separated (e.g., uber|uber eats|lyft)
Monarch Category:     pipe-separated (e.g., rideshare|food delivery)
Amount Pattern:       Optional: =100, >50, <25, 50-100, ~50
Notes:                Any helpful notes
```

### Editing an Existing Perk

1. Find the perk in **Perks Catalog**
2. Edit any field directly
3. **Important**: Don't change the Perk ID - it's used to link transactions
4. Run **Match Perks to Transactions** to re-evaluate matches with new rules

### Deleting a Perk

1. Delete the row from **Perks Catalog**
2. Transactions previously matched to this perk will show the old Perk ID
3. Run **Match Perks to Transactions** to re-match those transactions

### Common Perk Patterns

| Perk Type | Frequency | Reset | Amount Pattern | Example |
|-----------|-----------|-------|----------------|---------|
| Monthly credit | monthly | calendar | `10` or `10-15` | Amex Gold dining $10/mo |
| Annual credit | annual | anniversary | blank | CSR $300 travel |
| TSA/Global Entry | every_4_years | anniversary | `=100` or `~100` | Once per 4 years |
| Subscription benefit | annual | calendar | blank | Free DoorDash DashPass |
| Semi-annual | annual | calendar | `50` | Saks $50 twice/year |

---

## How to Refresh CSVs

### Paste Method (Simplest)

1. Export from Monarch:
   - Balances: Account Overview → Export
   - Transactions: Transactions → Filter to 2026 → Export

2. Open **Config** tab in Google Sheet

3. For Balances:
   - Find "Paste Balances CSV below this row:"
   - Clear any old data below it
   - Paste new CSV content
   - Run **🎯 Perks Tracker → Ingest Balances CSV (from Config tab)**

4. For Transactions:
   - Find "Paste Transactions CSV below this row:"
   - Clear any old data below it
   - Paste new CSV content
   - Run **🎯 Perks Tracker → Ingest Transactions CSV (from Config tab)**

### Drive Method (For Automation)

1. Create/use a dedicated Google Drive folder

2. Set the folder ID (one-time):
   - Get folder ID from URL: `drive.google.com/drive/folders/FOLDER_ID_HERE`
   - Run **Settings → Set Drive Folder ID**
   - Paste the folder ID

3. Upload new CSVs:
   - Name Balances file: starts with `Balances` (e.g., `Balances_2026-01-15.csv`)
   - Name Transactions file: starts with `transactions` (e.g., `transactions_export.csv`)
   - The system will find the most recently modified matching file

4. Run manually or let nightly trigger handle it

### Deduplication Behavior

- Each transaction gets a **Dedupe Key** (visible in Transactions_2026)
- Format: `ID:transaction_id` if Transaction ID exists
- Otherwise: `KEY:date|merchant|amount|account|description`
- Re-importing the same CSV won't create duplicates
- True duplicates in your source CSV are automatically removed

---

## How to Override Matches

### Manual Override for a Single Transaction

1. Go to **Transactions_2026** tab
2. Find the transaction you want to override
3. In the **Notes / Override Perk ID** column (column M), enter the correct Perk ID
4. Run **Match Perks to Transactions**
5. The transaction will show:
   - Match Confidence: 100
   - Match Reason: Manual override

### Common Override Scenarios

| Scenario | Solution |
|----------|----------|
| Wrong perk matched | Enter correct Perk ID in Override column |
| Should be unmatched | Enter `NONE` or `SKIP` in Override column |
| Multiple perks apply | Choose the higher-value perk (or split manually) |
| Refund for perk purchase | Override to same perk (counts as negative usage) |

### Bulk Override with Find/Replace

1. Filter Transactions_2026 to show only target transactions
2. Select the Override column cells
3. Use **Edit → Find and replace** to set Perk IDs in bulk
4. Run **Match Perks to Transactions**

---

## Understanding Pacing Logic

### Frequency Types

| Frequency | Expected Usage Calculation |
|-----------|---------------------------|
| monthly | (months elapsed) / 12 |
| quarterly | (quarters elapsed) / 4 |
| annual | (day of year) / 365 |
| every_4_years | (day of year) / 365 × 0.25 |
| one_time | Same as annual |

### Reset Rules

| Reset Rule | Period Start |
|------------|--------------|
| calendar | January 1 of tracking year |
| anniversary | Benefit Year Start Month from Cards tab |

### Status Calculation

```
tolerance = max(10% of Max Value, $10)

If (% Used) < (Expected Pace - tolerance): "Behind"
If (% Used) > (Expected Pace + tolerance): "Ahead"
Otherwise: "On Track"
```

### Example

- Perk: $200 annual, calendar reset
- Date: March 31 (day 90 of 365)
- Expected Pace: 90/365 = 24.7%
- Expected Usage: $200 × 24.7% = $49.32
- Tolerance: max(10% × $200, $10) = $20

- If Used = $25: Status = "Behind" (below $49.32 - $20 = $29.32)
- If Used = $50: Status = "On Track"
- If Used = $75: Status = "Ahead" (above $49.32 + $20 = $69.32)

---

## Adding Merchant Aliases

### When to Add Aliases

- Merchant shows up with different variations
- You want cleaner canonical names
- Matching isn't working because merchant name doesn't match keywords

### How to Add

1. Go to **Merchant_Aliases** tab
2. Add a new row:

| Match Type | Match Pattern | Canonical Merchant | Notes |
|------------|---------------|-------------------|-------|
| contains | doordash | DoorDash | Food delivery |
| equals | UBER *EATS | Uber Eats | Exact match |
| regex | uber.*trip | Uber | Regex pattern |

### Match Types

- **contains**: Pattern found anywhere in merchant name (most common)
- **equals**: Exact match only
- **regex**: JavaScript regular expression (advanced)

### Priority

- Rules are evaluated **top to bottom**
- First matching rule wins
- Put specific patterns ABOVE general patterns

Example order:
```
contains | uber eats | Uber Eats    ← More specific, first
contains | uber      | Uber         ← More general, second
```

---

## Troubleshooting

### Transactions Not Matching to Cards

1. Check **Transactions_2026** → **Card ID** column
2. If empty, the account name didn't match any card
3. Solutions:
   - Add the card to **Cards** tab if missing
   - Check the account name matches card keywords
   - The system matches on: card name words, last 4 digits

### Perks Not Being Matched

1. Check the **Match Confidence** column - if below 60, no match assigned
2. Improve matching:
   - Add merchant to **Merchant_Aliases**
   - Add merchant keywords to the perk's **Merchant Keywords**
   - Add category to perk's **Monarch Category Match**

### Dashboard Shows Wrong Numbers

1. Run **Calculate Usage & Pacing** to refresh
2. Check **Perk Usage 2026** for detailed breakdown
3. Verify transactions are correctly matched
4. Check for duplicate transactions

### "Behind" Status Seems Wrong

1. Check the perk's **Frequency** setting
2. Check the card's **Benefit Year Start Month** (for anniversary reset)
3. Monthly perks expect steady usage throughout the year
4. Annual perks are more forgiving early in the year

### DRY_RUN Mode Stuck On

1. Go to **🎯 Perks Tracker → Settings → Toggle DRY_RUN Mode**
2. Set to OFF
3. Re-run your operations

---

## Advanced: Customizing the Code

### Changing the Tracking Year

In `Code.gs`, find:
```javascript
TRACKING_YEAR: 2026
```
Change to your desired year.

### Adjusting Match Threshold

In `Code.gs`, find:
```javascript
MATCH_THRESHOLD: 60
```
Lower = more matches (possibly false positives)
Higher = fewer matches (possibly missing valid ones)

### Adjusting Pacing Tolerance

In `Code.gs`, find:
```javascript
TOLERANCE_PERCENT: 0.10,
TOLERANCE_MIN_DOLLARS: 10
```
Increase for more forgiving "On Track" status.

### Adding Custom Scoring Rules

In the `matchPerks()` function, find the scoring section and add:
```javascript
// Custom rule example: bonus for specific card
if (perk.cardId === 'MY_SPECIAL_CARD') {
  score += 10;
  reasons.push('preferred_card');
}
```

### Modifying Neutral Merchant List

In `Code.gs`, find:
```javascript
const NEUTRAL_MERCHANTS = [
  'amazon', 'paypal', ...
];
```
Add or remove merchants as needed.

---

## Backup Recommendations

1. **Weekly**: Download a copy of the Sheet (File → Download → .xlsx)
2. **Monthly**: Make a copy in Drive (File → Make a copy)
3. **Before major changes**: Duplicate tabs you're about to modify

## Support

- Check the **Log** tab for error messages
- Review the **Match Reason** column to understand matching decisions
- Test changes with **DRY_RUN mode** enabled first
