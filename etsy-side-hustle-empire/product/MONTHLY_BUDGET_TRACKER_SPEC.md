# Monthly Budget Tracker (Google Sheets Template)

## Purpose
A premium, minimalist monthly budget tracker designed for Etsy customers. This spec describes the exact sheet structure, formulas, and data flow so the template can be built in Google Sheets without ambiguity. The template is print-friendly, uses neutral colors, separates editable inputs from formulas, and is optimized for month-to-month duplication.

---

## Design System (Applies to All Sheets)
- **Palette:** white (#FFFFFF), light beige (#F7F3EE), soft gray (#E6E6E6), charcoal text (#2F2F2F).
- **Typography:** clean sans-serif (e.g., Arial/Inter), consistent title and header sizing.
- **Layout:** generous spacing, no decorative elements, print-friendly margins.
- **Edit-Here Areas:** light beige fill with the label **“EDIT HERE”** in column A (where applicable).
- **Formula Areas:** soft gray fill or locked ranges (protected in final template).
- **Number Formats:** currency with 2 decimals for money, date for dates.

---

## Sheet 1: `Dashboard`

### Purpose
High-level monthly overview with clean summary tiles.

### Layout
- **A1:H1:** Title row: “Monthly Budget Dashboard” (merged A1:H1).
- **A3:H3:** Month selector row.
  - **A3:** “Month (Editable)”
  - **B3:** **EDIT HERE** month value (e.g., `Jan 2025`).
- **A5:H10:** Summary tiles (each tile is a merged block):
  - **A5:B7:** Total Income
  - **C5:D7:** Total Expenses
  - **E5:F7:** Remaining Budget
  - **G5:H7:** Savings Rate (optional but premium value)

### Formulas
- **Total Income (B6):** `=IFERROR(SUM('Monthly Budget'!H5:H),0)`
- **Total Expenses (D6):** `=IFERROR(SUM('Monthly Budget'!I5:I),0)`
- **Remaining Budget (F6):** `=B6-D6`
- **Savings Rate (H6):** `=IFERROR((B6-D6)/B6,0)` (format as %)

### Notes
- The dashboard only pulls totals; no direct editing except the Month cell.

---

## Sheet 2: `Monthly Budget`

### Purpose
Planned vs. Actual budget by category with automatic roll-ups.

### Layout
- **A1:H1:** Title row: “Monthly Budget” (merged A1:H1).
- **A3:H3:** Month row.
  - **A3:** “Month”
  - **B3:** **EDIT HERE** (use data validation list of months or typed month).
- **A4:** “EDIT HERE → Categories & Planned Values” label.

### Table (starting row 5)
| Column | Header | Type |
|---|---|---|
| A | Category | **Edit Here** (text) |
| B | Planned | **Edit Here** (currency) |
| C | Actual | Formula |
| D | Remaining | Formula |
| E | % Used | Formula |
| F | Notes | **Edit Here** (text) |
| G | Subtotal: Income/Expense | Formula (helper) |
| H | Income | Formula |
| I | Expenses | Formula |

### Table Logic
- Users list all categories once. Income categories should be labeled clearly (e.g., “Salary”, “Side Income”) and tagged in column G.
- Expense categories are all other lines.

### Formulas (row 5; copy down)
- **C5 (Actual):** `=IFERROR(SUMIF('Expense Log'!B:B,A5,'Expense Log'!E:E),0)`
- **D5 (Remaining):** `=IFERROR(B5-C5,0)`
- **E5 (% Used):** `=IFERROR(C5/B5,0)`
- **G5 (Type Helper):** `=IF(REGEXMATCH(LOWER(A5),"income|salary|paycheck"),"Income","Expense")`
- **H5 (Income):** `=IF(G5="Income",C5,0)`
- **I5 (Expenses):** `=IF(G5="Expense",C5,0)`

### Totals (bottom row)
- **A (Total row label):** “TOTAL”
- **B (Planned Total):** `=SUM(B5:B)`
- **C (Actual Total):** `=SUM(C5:C)`
- **D (Remaining Total):** `=SUM(D5:D)`
- **H (Total Income):** `=SUM(H5:H)`
- **I (Total Expenses):** `=SUM(I5:I)`

### Notes
- Column G is a helper and should be hidden or gray-filled.
- Column A (Category) and B (Planned) are the primary user inputs.

---

## Sheet 3: `Expense Log`

### Purpose
Transaction-level entries that roll up into the Monthly Budget.

### Layout
- **A1:F1:** Title row: “Expense Log” (merged A1:F1).
- **A3:** “EDIT HERE → Add transactions below.”

### Table (starting row 5)
| Column | Header | Type |
|---|---|---|
| A | Date | **Edit Here** (date) |
| B | Category | **Edit Here** (dropdown) |
| C | Description | **Edit Here** (text) |
| D | Amount | **Edit Here** (currency) |
| E | Amount (Signed) | Formula |
| F | Month Tag | Formula |

### Data Validation
- **Column B (Category dropdown):** `=FILTER('Monthly Budget'!A5:A,'Monthly Budget'!A5:A<>"")`

### Formulas (row 5; copy down)
- **E5 (Amount Signed):** `=IFERROR(D5,0)`
- **F5 (Month Tag):** `=TEXT(A5,"MMM YYYY")`

### Notes
- If you want income logging, add income rows with positive amounts and match to income categories.

---

## Sheet 4: `Category Summary`

### Purpose
Planned vs. Actual comparison per category (clean, print-friendly table).

### Layout
- **A1:F1:** Title row: “Category Summary” (merged A1:F1).
- **A3:F3:** Header row.

### Table (starting row 4)
| Column | Header | Source |
|---|---|---|
| A | Category | Pull from Monthly Budget |
| B | Planned | Pull from Monthly Budget |
| C | Actual | Pull from Monthly Budget |
| D | Remaining | Pull from Monthly Budget |
| E | % Used | Pull from Monthly Budget |
| F | Status | Formula |

### Formulas
- **A4:** `=FILTER('Monthly Budget'!A5:A,'Monthly Budget'!A5:A<>"")`
- **B4:** `=ARRAYFORMULA(IF(A4:A="",,VLOOKUP(A4:A,'Monthly Budget'!A5:D,2,FALSE)))`
- **C4:** `=ARRAYFORMULA(IF(A4:A="",,VLOOKUP(A4:A,'Monthly Budget'!A5:D,3,FALSE)))`
- **D4:** `=ARRAYFORMULA(IF(A4:A="",,VLOOKUP(A4:A,'Monthly Budget'!A5:D,4,FALSE)))`
- **E4:** `=ARRAYFORMULA(IF(A4:A="",,VLOOKUP(A4:A,'Monthly Budget'!A5:E,5,FALSE)))`
- **F4 (Status):** `=ARRAYFORMULA(IF(A4:A="",,IF(E4:E>1,"Over Budget","On Track")))`

### Notes
- Status uses neutral text; no bright color indicators (optional soft gray highlight for Over Budget in print-friendly tone).

---

## Data Flow Summary
1. **Expense Log → Monthly Budget**
   - Actual spend per category is calculated in `Monthly Budget!C:C` using `SUMIF` against `Expense Log` entries.
2. **Monthly Budget → Dashboard**
   - Income and expenses are summed from helper columns `H:I`.
3. **Monthly Budget → Category Summary**
   - Category Summary mirrors planned vs. actual values with lookup formulas.
4. **Month Tag (Expense Log) → Filtering**
   - Month Tag can be used to filter transactions when duplicating sheets per month.

---

## Duplication & Monthly Workflow
- Duplicate all four sheets as a monthly set.
- Update **Dashboard!B3** and **Monthly Budget!B3** to the new month.
- Clear `Expense Log` rows for the new month (keep headers + formulas).
- Categories persist while actuals reset via cleared log.

---

## Protection & Usability Notes
- Protect formula columns (C-E, G-I in Monthly Budget; E-F in Expense Log; B-F in Category Summary).
- Leave `EDIT HERE` areas unprotected and beige-filled.
- Keep row heights and column widths consistent for print-friendly PDF export.
