# Product 11 — Spreadsheet Build Spec

## Tab Structure

### Tab 1: DASHBOARD
- Total revenue (MTD, YTD)
- Total expenses (MTD, YTD)
- Net profit (MTD, YTD)
- Profit margin %
- Bar chart: monthly revenue vs expenses (12 months)
- Donut chart: expense breakdown by category
- Top 5 products by revenue

### Tab 2: MONTHLY LOG
Columns: Date | Order # | Product Name | Sale Price | Etsy Transaction Fee (6.5%) | Etsy Payment Processing (3% + $0.25) | Listing Fee ($0.20) | Shipping Label Cost | COGS | Other Fees | Net Profit
- Auto-calculated: all fee columns use formulas based on sale price
- Auto-calculated: Net Profit = Sale Price - all fees - COGS

### Tab 3: COGS TRACKER
Columns: Product Name | Materials Cost | Labor Hours | Hourly Rate | Total COGS | Selling Price | Gross Margin %

### Tab 4: QUARTERLY TAXES
- Q1/Q2/Q3/Q4 gross income totals (pulled from Monthly Log)
- SE tax estimate (15.3% of net profit)
- Federal income tax estimate (user enters tax bracket)
- Quarterly payment due dates
- "Set aside this amount" callout box

### Tab 5: ANNUAL SUMMARY
- 12-month totals by category
- Schedule C prep: Line 1 (gross receipts), Line 17 (taxes), Line 22 (supplies), Line 27a (other)
- YoY comparison (if second year)

### Tab 6: SETUP GUIDE
- Step-by-step instructions (plain English)
- How to make a copy in Google Drive
- How to customize categories
- FAQ

## Design Notes
- Color palette: sage green + white + gold accents
- Font: Google Sans or similar clean sans-serif
- Freeze row 1 on all data tabs
- Conditional formatting: profit cells green if positive, red if negative
- Protect formula cells (allow editing data cells only)
