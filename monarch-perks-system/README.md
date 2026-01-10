# Monarch Credit Card Perks Tracking System

A complete Google Sheets + Apps Script system that ingests Monarch CSV exports, builds a credit card perks catalog, matches transactions to perks, and tracks pacing/unused perks.

## Features

- **Automatic Card Detection**: Parses account names to identify credit cards, extract last-4 digits, and infer issuers
- **Deduplication**: Prevents duplicate transaction imports using Transaction ID or composite keys
- **Merchant Normalization**: Maps raw merchant names to canonical forms using configurable alias rules
- **Intelligent Perk Matching**: Scores transactions against perks using merchant keywords, categories, and amount patterns
- **Pacing Calculations**: Tracks usage vs expected pace with support for monthly, quarterly, annual, and every-4-year perks
- **Dashboard**: Summary metrics, "Perks I'm Behind On", and "Biggest Unused Perks" views
- **Automation**: Nightly trigger support for hands-off operation

## Quick Start

1. Create a new Google Sheet
2. Open **Extensions → Apps Script**
3. Paste the contents of `Code.gs`
4. Run `setupSheet_IfNeeded` (grant permissions when prompted)
5. Use the **🎯 Perks Tracker** menu to ingest data and run the pipeline

See [SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md) for detailed instructions.

## Sheet Structure

| Tab | Purpose |
|-----|---------|
| **Cards** | Your credit card inventory with IDs, issuers, and annual fees |
| **Perks Catalog** | All perks with matching rules and values |
| **Merchant_Aliases** | Maps raw merchants to canonical names |
| **Monarch Categories Map** | Maps Monarch categories to perk categories |
| **Transactions_2026** | Imported transactions with perk matches |
| **Perk Usage 2026** | Aggregated usage, remaining value, and pacing status |
| **Dashboard** | Summary metrics and actionable tables |
| **Config** | CSV paste area for manual ingestion |
| **Log** | Execution history and debug info |

## Matching Algorithm

For each transaction, the system scores potential perk matches:

| Rule | Points |
|------|--------|
| Merchant keyword match | +60 |
| Category match | +25 |
| Amount pattern match | +15 |
| Neutral merchant (no keyword match) | -30 |

Perks scoring ≥60 are matched. Manual overrides always take precedence.

## Pacing Logic

- **monthly**: Expected = months elapsed / 12
- **quarterly**: Expected = quarters elapsed / 4
- **annual**: Expected = day of year / 365
- **every_4_years**: Expected = (day of year / 365) × 25%

Status is calculated with a 10% tolerance (minimum $10):
- **Behind**: Used < Expected - Tolerance
- **On Track**: Within tolerance
- **Ahead**: Used > Expected + Tolerance

## Files

- `Code.gs` - Complete Apps Script implementation
- `SETUP_CHECKLIST.md` - Step-by-step setup guide
- `MAINTENANCE_GUIDE.md` - Ongoing usage and troubleshooting

## Configuration

Settings are stored in Script Properties:

| Property | Purpose |
|----------|---------|
| `DRIVE_FOLDER_ID` | Google Drive folder for CSV auto-import |
| `DRY_RUN` | When true, no data is written (test mode) |

Access via **🎯 Perks Tracker → Settings** menu.

## CSV Requirements

### Balances CSV
Required columns: `Account` (or `Account Name`)

### Transactions CSV
Required columns: `Date`, `Merchant` (or `Description`/`Name`), `Amount`
Optional columns: `Category`, `Account`, `Transaction ID`, `Original Statement`

## Sample Perks

Run `seedSamplePerks()` to populate the Perks Catalog with common credit card perks:
- Chase Sapphire Reserve (Travel Credit, Global Entry, DoorDash, Lyft)
- Amex Platinum (Uber, Airline, Saks, Hotel, CLEAR, Equinox, Entertainment, Walmart+)
- Amex Gold (Dining, Uber Cash, Dunkin')
- Capital One Venture X (Travel Credit, Global Entry)
- Hilton Aspire (Resort Credit, Airline, Free Night)

Edit Card IDs to match your actual cards.

## License

MIT
