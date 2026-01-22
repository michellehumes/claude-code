# Life OS v2 - Complete 54-Tab Life Management System

**Created for:** Michelle & Gray Perkins
**Location:** East Hampton, NY
**Version:** 2.0

## Overview

Life OS v2 is a comprehensive 54-tab Google Sheets system integrating:
- **Financial Tracking** (Monarch Money data - 18,507 transactions)
- **Job Search Pipeline** (Applications, interviews, offers)
- **Goals Management** (Michelle, Gray, and shared goals)
- **Household Management** (Tasks, load balancing)
- **Shelzy's Designs Business** (E-commerce analytics)
- **Fertility & Health Tracking** (Cycle tracking, appointments)
- **Oura Ring Health Data** (Sleep, activity, readiness, cycle phases)
- **Executive Dashboards** (Weekly summaries, status reports)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Google Sheets API and Google Drive API
4. Create a Service Account and download the credentials JSON
5. Place the credentials file at `config/credentials.json`
6. Share your target spreadsheet with the service account email

### 3. Prepare Your Data

Place your data files in the `data/` directory:
- `data/transactions.csv` - Monarch Money export
- `data/oura/` - Oura Ring data exports (from Settings > Export)

### 4. Run the Generator

```bash
# Create a new spreadsheet
python src/main.py --create "Life OS v2"

# Or update an existing spreadsheet
python src/main.py --spreadsheet-id YOUR_SPREADSHEET_ID
```

## Project Structure

```
life-os-v2/
├── src/
│   ├── main.py                 # Main entry point
│   ├── spreadsheet_builder.py  # Core spreadsheet generation
│   ├── tabs/                   # Tab builders (54 tabs)
│   │   ├── __init__.py
│   │   ├── financial.py        # Tabs 1-11
│   │   ├── job_search.py       # Tabs 12-18
│   │   ├── goals.py            # Tabs 19-22
│   │   ├── household.py        # Tabs 23-25
│   │   ├── shelzys.py          # Tabs 26-34
│   │   ├── fertility.py        # Tabs 35-40
│   │   ├── executive.py        # Tabs 41-46
│   │   └── oura.py             # Tabs 47-54
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── formatting.py       # Styling utilities
│   │   ├── formulas.py         # Formula generators
│   │   └── validation.py       # Data validation
│   └── data_processors/
│       ├── __init__.py
│       ├── transactions.py     # Monarch Money processor
│       └── oura.py             # Oura Ring processor
├── data/
│   ├── sample/                 # Sample data files
│   └── oura/                   # Oura Ring exports
├── config/
│   ├── settings.py             # Configuration
│   └── credentials.json        # Google API credentials
└── docs/
    └── specification.md        # Full system specification
```

## Tab Structure (54 Tabs)

### Financial Dashboard (1-11)
1. Dashboard (HOME)
2. Transactions (MASTER DATA)
3. Credit Cards
4. Budget Master
5. Spending by Category
6. Monthly Summary
7. Spending by Merchant
8. Master Tasks
9. Gift Tracker
10. Health Dashboard
11. Calendar View

### Job Search System (12-18)
12. Job Pipeline
13. Applications Tracker
14. Recruiter CRM
15. Interview Tracker
16. Follow-Ups
17. Offer Comparison
18. Job Search Dashboard

### Goals System (19-22)
19. Michelle's Goals
20. Gray's Goals
21. Shared Goals
22. Goal Dashboard

### Household System (23-25)
23. Recurring Tasks
24. One-Time Projects
25. Load Dashboard

### Shelzy's Designs Business (26-34)
26. Shelzy's Transactions
27. Shelzy's Revenue Tracker
28. Shelzy's Product Catalog
29. Shelzy's Expenses
30. Shelzy's Monthly P&L
31. Shelzy's Customer Metrics
32. Shelzy's Inventory
33. Shelzy's Marketing
34. Shelzy's Dashboard

### Fertility & Health (35-40)
35. Cycle Tracking
36. Daily Log
37. DPO Tracker
38. Appointments
39. Supplements
40. Monthly Summary

### Executive Dashboards (41-46)
41. Weekly Life Summary
42. Job Search Status
43. Financial Health
44. Goal Progress
45. Household Load
46. Business Performance

### Oura Ring Integration (47-54)
47. Oura Sleep Tracker
48. Oura Activity Tracker
49. Oura Readiness Tracker
50. Oura Cycle Integration
51. Oura Temperature
52. Oura Heart Rate
53. Oura Stress Tracker
54. Oura Health Dashboard

## Data Sources

### Monarch Money Transactions
Export your transactions from Monarch Money:
1. Go to Monarch Money > Transactions
2. Click Export > Download CSV
3. Place file at `data/transactions.csv`

**Required Columns:** Date, Merchant, Category, Account, Original Statement, Notes, Amount, Tags, Owner

### Oura Ring Data
Export from Oura App or web:
1. Go to Oura > Settings > Data Export
2. Download all available data
3. Extract to `data/oura/` directory

**Expected Files:**
- dailysleep.csv
- dailyactivity.csv
- dailyreadiness.csv
- dailycyclephases.csv
- temperature.csv
- heartrate.csv
- dailystress.csv
- workout.csv

## Account Tagging

Before importing transactions, ensure accounts are tagged in the CSV:
- **"Michelle Personal"** - Michelle's individual accounts
- **"Gray Personal"** - Gray's individual accounts
- **"Joint"** - Shared household accounts
- **"Shelzys"** - Shelzy's Designs business accounts

## Formatting Standards

### Colors
- Header: RGB(66, 133, 244) - Blue
- Positive/Income: #0F9D58 - Green
- Negative/Expenses: #DB4437 - Red
- Warning: #FDAB3D - Orange
- Completed: #9AA0A6 - Gray

### Number Formats
- Currency: `$#,##0.00`
- Percentage: `0.0%`
- Dates: `MM/DD/YYYY`
- Whole numbers: `#,##0`

## License

Private use only - Created for Michelle & Gray Perkins
