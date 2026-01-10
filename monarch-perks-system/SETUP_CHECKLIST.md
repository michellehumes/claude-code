# Monarch Credit Card Perks Tracker - Setup Checklist

## Your Cards (Pre-configured)

The system has been pre-configured with your 11 credit cards from Monarch:

| Card ID | Card Name | Issuer | Last4 | Annual Fee |
|---------|-----------|--------|-------|------------|
| MSR_1041 | Michelle's Sapphire Reserve | Chase | 1041 | $550 |
| GAPP_1007 | Gray's Amex Platinum Card® | Amex | 1007 | $695 |
| GAGC_2003 | Gray's Amex Gold Card | Amex | 2003 | $250 |
| MPC_7008 | Michelle's Platinum Card® | Amex | 7008 | $695 |
| MMBB_5005 | Michelle's Marriott Bonvoy Brilliant® | Amex | 5005 | $650 |
| MFU_9759 | Michelle's Freedom Unlimited | Chase | 9759 | $0 |
| MSC_0443 | Michelle's Slate Card | Chase | 0443 | $0 |
| VEN_4522 | Venture | Capital One | 4522 | $95 |
| APC_5990 | Amazon Prime Card | Chase | 5990 | $0 |
| TCC_2828 | Target Circle Card | Target | 2828 | $0 |
| USAA_9385 | USAA Rate Advantage Platinum Visa | USAA | 9385 | $0 |

**Total Annual Fees: ~$2,935**

---

## Quick Start (5 minutes)

### Step 1: Create Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com)
2. Click **+ Blank** to create a new spreadsheet
3. Name it: `Credit Card Perks Tracker 2026`

### Step 2: Add the Code
1. Go to **Extensions → Apps Script**
2. Delete the default code in `Code.gs`
3. Copy the ENTIRE contents of `Code.gs` from this repository
4. Paste into the editor
5. Press **Ctrl+S** to save
6. Name the project: `MonarchPerksTracker`

### Step 3: Run Quick Setup
1. Select `quickSetupWithMyData` from the function dropdown
2. Click **Run** (▶️)
3. Click **Review Permissions** → **Advanced** → **Go to MonarchPerksTracker** → **Allow**
4. Wait for setup to complete

This creates all tabs AND pre-populates your 11 cards and 25 perks.

### Step 4: Import Your Transactions
1. Go back to your Google Sheet
2. Open the **Config** tab
3. Find the row "Paste Transactions CSV below this row:"
4. Paste your Monarch transactions CSV content below that row
5. Go to **🎯 Perks Tracker → Import Data → Ingest Transactions CSV (from Config tab)**

### Step 5: Run the Pipeline
1. Go to **🎯 Perks Tracker → Run Full Pipeline**
2. Wait for completion
3. Check the **Dashboard** tab!

---

## Your Pre-Configured Perks (25 total)

### Michelle's Sapphire Reserve (MSR_1041) - 4 perks
- $300 Travel Credit (annual)
- Global Entry/TSA PreCheck (every 4 years)
- DoorDash DashPass (annual)
- Lyft Pink (annual)

### Gray's Amex Platinum (GAPP_1007) - 8 perks
- $200 Uber Credit ($15-35/mo)
- $200 Airline Fee Credit (annual)
- $100 Saks Credit ($50 twice/year)
- $200 Hotel Credit (annual)
- $189 CLEAR Credit (annual)
- $240 Digital Entertainment ($20/mo)
- $155 Walmart+ Credit (annual)
- $300 Equinox Credit ($25/mo)

### Michelle's Platinum (MPC_7008) - 7 perks
- $200 Uber Credit ($15-35/mo)
- $200 Airline Fee Credit (annual)
- $100 Saks Credit ($50 twice/year)
- $200 Hotel Credit (annual)
- $155 Walmart+ Credit (annual)
- $240 Digital Entertainment ($20/mo)
- $189 CLEAR Credit (annual)

### Gray's Amex Gold (GAGC_2003) - 3 perks
- $120 Dining Credit ($10/mo)
- $120 Uber Cash ($10/mo)
- $84 Dunkin' Credit ($7/mo)

### Marriott Bonvoy Brilliant (MMBB_5005) - 3 perks
- $300 Dining Credit (annual)
- $300 Hotel Credit (annual)
- Free Night Award (~$500 value)

### Capital One Venture (VEN_4522) - 2 perks
- $100 Travel Credit (annual)
- Anniversary Miles (~$100 value)

**Total Annual Perk Value: ~$4,500+**

---

## Tabs Created

| Tab | Purpose |
|-----|---------|
| **Cards** | Your 11 credit cards with IDs and fees |
| **Perks Catalog** | 25 perks with matching rules |
| **Merchant_Aliases** | 45+ merchant name mappings |
| **Monarch Categories Map** | Category translations |
| **Transactions_2026** | Your imported transactions |
| **Perk Usage 2026** | Usage tracking and pacing |
| **Dashboard** | Summary and action items |
| **Config** | CSV paste area |
| **Log** | Execution history |

---

## Menu Reference

| Menu Item | What It Does |
|-----------|--------------|
| **⚡ Quick Setup** | Creates tabs + adds your cards + adds your perks |
| **📋 Setup Sheet Only** | Creates tabs only (no data) |
| **Import Data → Ingest Transactions CSV** | Imports pasted CSV |
| **Seed Data → Add My Cards** | Adds your 11 specific cards |
| **Seed Data → Add My Perks** | Adds your 25 specific perks |
| **▶️ Run Full Pipeline** | Normalize → Match → Calculate → Dashboard |
| **⏰ Install Nightly Trigger** | Auto-run at 2 AM daily |

---

## Sample Transactions Detected

From your Monarch data, I detected these perk-eligible transactions:

| Transaction | Card | Potential Perk |
|-------------|------|----------------|
| Lord Camden Inn ($1,470.57) | MSR_1041 | $300 Travel Credit |
| Woodstock Inn ($867.91) | VEN_4522 | Travel/Hotel |
| Lyft ($216.66 + refunds) | MSR_1041 | Travel Credit |
| Uber Eats ($33.03) | GAPP_1007 | Uber Credit |
| Breeze Airways ($1,504.34 + $175) | GAPP_1007 | Airline Fee Credit |
| American Airlines ($630.96) | GAPP_1007 | Airline Fee Credit |
| Walmart+ ($14.10) | MPC_7008 | Walmart+ Credit |
| Hulu ($12.99) | MMBB_5005 | Digital Entertainment |
| YouTube TV ($82.99) | GAPP_1007 | Digital Entertainment |
| Spotify ($11.99) | VEN_4522 | - |

---

## Troubleshooting

### "No perks found to match"
- Run **Seed Data → Add My Perks** first
- Check the **Perks Catalog** tab has data

### Transactions not matching cards
- Check **Cards** tab has your cards
- Verify the account names match (last 4 digits are key)

### Pacing seems off
- Check **Benefit Year Start Month** in Cards tab
- Verify **Frequency** in Perks Catalog (monthly vs annual)

### Need to re-run from scratch
1. Delete all data rows (keep headers) in each tab
2. Run **Quick Setup** again
3. Re-import transactions

---

## Next Steps After Setup

1. **Review Perks Catalog** - Adjust values for your specific card versions
2. **Add missing perks** - Some cards may have perks not pre-configured
3. **Check Dashboard** - See which perks you're behind on
4. **Set up nightly trigger** - For automatic daily updates
5. **Export new transactions monthly** - Re-import to keep data fresh
