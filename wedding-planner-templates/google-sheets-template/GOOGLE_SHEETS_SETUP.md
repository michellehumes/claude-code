# Wedding Command Center - Google Sheets Template

**For: Michelle & Gray | September 14, 2025**

Follow this guide to create your complete wedding planner in Google Sheets.

---

## Quick Start

1. Create a new Google Sheet
2. Rename it: "Michelle & Gray Wedding Planner"
3. Create these tabs (in order):
   - Dashboard
   - Budget
   - Guests
   - Vendors
   - Timeline
   - Checklist
   - Config

---

## Tab 1: Config (Set this up first!)

This tab stores your wedding details that other tabs reference.

| Row | A | B |
|-----|---|---|
| 1 | **Setting** | **Value** |
| 2 | Couple Names | Michelle & Gray |
| 3 | Wedding Date | 9/14/2025 |
| 4 | Venue | Rosewood Gardens |
| 5 | Total Budget | 24500 |
| 6 | Guest Estimate | 150 |

**Name these cells** (Select cell B3, go to Data > Named ranges):
- B2 → `CoupleNames`
- B3 → `WeddingDate`
- B4 → `Venue`
- B5 → `TotalBudget`
- B6 → `GuestEstimate`

---

## Tab 2: Dashboard

### Row 1-2: Header
| A | B | C | D |
|---|---|---|---|
| **Michelle & Gray** | | | |
| September 14, 2025 • Rosewood Gardens | | | |

**Formulas:**
- A1: `=Config!B2`
- A2: `=TEXT(Config!B3,"mmmm d, yyyy") & " • " & Config!B4`

### Row 4-5: Quick Stats
| A | B | C | D |
|---|---|---|---|
| **Days to Go** | **Tasks Done** | **Guests** | **Budget Spent** |
| 243 | 85% | 142 | $20,000 |

**Formulas:**
- A5: `=MAX(0, Config!B3 - TODAY())`
- B5: `=ROUND(COUNTIF(Checklist!C:C, TRUE) / COUNTA(Checklist!B:B) * 100, 0) & "%"`
- C5: `=COUNTIF(Guests!D:D, "Attending")`
- D5: `=TEXT(SUMIF(Budget!E:E, ">0", Budget!E:E), "$#,##0")`

### Row 7-15: Budget Summary
| A | B | C |
|---|---|---|
| **Category** | **Spent** | **Budget** |
| Venue & Catering | $8,500 | $9,000 |
| Photography | $3,500 | $4,000 |
| Florals & Decor | $1,800 | $2,500 |
| Attire & Beauty | $2,200 | $2,500 |
| Music & Entertainment | $1,500 | $2,000 |
| Stationery | $800 | $1,000 |
| Other | $1,700 | $3,500 |
| **TOTAL** | **$20,000** | **$24,500** |

**Formulas:**
- B8: `=SUMIF(Budget!$B:$B, A8, Budget!$E:$E)`
- C8: `=SUMIF(Budget!$B:$B, A8, Budget!$D:$D)`
- (Copy down for each category)
- B15: `=SUM(B8:B14)`
- C15: `=Config!B5`

### Row 17-22: Upcoming Tasks (This Week)
| A | B |
|---|---|
| **This Week's Tasks** | **Due** |
| Book hair & makeup trial | Jan 20 |
| Confirm photographer timeline | Jan 22 |
| Order wedding favors | Jan 25 |

**Formula:**
- Pull from Checklist where due date is within 7 days:
- A18: `=FILTER(Checklist!B:B, Checklist!D:D <= TODAY()+7, Checklist!C:C = FALSE)`

---

## Tab 3: Budget

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| **Item** | **Category** | **Vendor** | **Estimated** | **Actual** | **Paid** | **Balance** |
| Venue rental | Venue & Catering | Rosewood Gardens | 5000 | 5000 | 5000 | 0 |
| Catering (per head) | Venue & Catering | Rosewood Catering | 4000 | 3500 | 2000 | 1500 |
| Photographer | Photography | Jane Smith Photo | 4000 | 3500 | 1750 | 1750 |
| Videographer | Photography | Film Co | 0 | 0 | 0 | 0 |
| Bridal bouquet | Florals & Decor | Bloom Studio | 300 | 350 | 0 | 350 |
| Centerpieces | Florals & Decor | Bloom Studio | 1200 | 1000 | 500 | 500 |
| Wedding dress | Attire & Beauty | Bridal Boutique | 2000 | 1800 | 1800 | 0 |
| Alterations | Attire & Beauty | | 400 | 400 | 0 | 400 |
| DJ | Music & Entertainment | DJ Mike | 1500 | 1500 | 500 | 1000 |
| Invitations | Stationery | Minted | 600 | 550 | 550 | 0 |
| Save the dates | Stationery | Minted | 200 | 250 | 250 | 0 |

**Formulas:**
- G2: `=E2-F2` (Balance = Actual - Paid)
- Copy formula down for all rows

**Data Validation for Column B (Category):**
1. Select column B
2. Data > Data validation
3. Criteria: List of items
4. Enter: `Venue & Catering, Photography, Florals & Decor, Attire & Beauty, Music & Entertainment, Stationery, Transportation, Gifts & Favors, Other`

### Summary Row (at bottom):
| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| **TOTALS** | | | =SUM(D:D) | =SUM(E:E) | =SUM(F:F) | =SUM(G:G) |

---

## Tab 4: Guests

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| **Name** | **Email** | **Phone** | **RSVP** | **Meal** | **Table** | **Plus One** | **Notes** |
| John Smith | john@email.com | 555-1234 | Attending | Beef | 1 | Jane Smith | Best man |
| Sarah Johnson | sarah@email.com | 555-5678 | Attending | Vegetarian | 2 | | Aunt |
| Mike Brown | mike@email.com | 555-9012 | Declined | | | | College friend |
| Emily Davis | emily@email.com | 555-3456 | Pending | | | Tom Davis | Cousin |

**Data Validation for Column D (RSVP):**
- List: `Pending, Attending, Declined, No Response`

**Data Validation for Column E (Meal):**
- List: `Beef, Chicken, Fish, Vegetarian, Vegan, Kids Meal`

### Guest Summary (add at top or on Dashboard):
| | Formula |
|---|---|
| Total Invited | `=COUNTA(A:A)-1` |
| Attending | `=COUNTIF(D:D, "Attending")` |
| Declined | `=COUNTIF(D:D, "Declined")` |
| Pending | `=COUNTIF(D:D, "Pending") + COUNTIF(D:D, "No Response")` |
| Beef | `=COUNTIF(E:E, "Beef")` |
| Vegetarian | `=COUNTIF(E:E, "Vegetarian")` |

---

## Tab 5: Vendors

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| **Vendor** | **Service** | **Contact** | **Phone** | **Email** | **Total Cost** | **Deposit Paid** | **Status** |
| Rosewood Gardens | Venue | Amanda Lee | 555-1111 | events@rosewood.com | 5000 | 2500 | Booked |
| Jane Smith Photo | Photography | Jane Smith | 555-2222 | jane@photo.com | 3500 | 1750 | Booked |
| Bloom Studio | Florals | Maria Garcia | 555-3333 | maria@bloom.com | 1350 | 500 | Booked |
| DJ Mike | Entertainment | Mike Johnson | 555-4444 | mike@djmike.com | 1500 | 500 | Booked |
| Bella Catering | Catering | | 555-5555 | info@bella.com | 3500 | 0 | Pending |

**Data Validation for Column H (Status):**
- List: `Researching, Contacted, Meeting Scheduled, Booked, Deposit Paid, Paid in Full`

---

## Tab 6: Timeline (Day-of Schedule)

| A | B | C | D |
|---|---|---|---|
| **Time** | **Event** | **Location** | **Notes** |
| 8:00 AM | Hair & Makeup arrives | Bridal Suite | |
| 9:00 AM | Bride hair begins | Bridal Suite | |
| 10:00 AM | Bridesmaids hair begins | Bridal Suite | |
| 11:00 AM | Photographer arrives | Bridal Suite | Detail shots |
| 12:00 PM | Lunch for bridal party | Bridal Suite | |
| 1:00 PM | Bride gets dressed | Bridal Suite | |
| 2:00 PM | First look | Garden | |
| 2:30 PM | Wedding party photos | Garden | |
| 3:30 PM | Family photos | Garden | |
| 4:00 PM | Guests arrive | Ceremony lawn | |
| 4:30 PM | Ceremony begins | Ceremony lawn | |
| 5:00 PM | Cocktail hour | Terrace | |
| 6:00 PM | Reception begins | Ballroom | |
| 6:30 PM | First dance | Ballroom | |
| 6:45 PM | Toasts | Ballroom | |
| 7:00 PM | Dinner served | Ballroom | |
| 8:30 PM | Cake cutting | Ballroom | |
| 9:00 PM | Dancing | Ballroom | |
| 11:00 PM | Last dance & send off | Ballroom | |

---

## Tab 7: Checklist

| A | B | C | D | E |
|---|---|---|---|---|
| **Phase** | **Task** | **Done** | **Due Date** | **Notes** |
| 12+ Months | Set wedding date | TRUE | | |
| 12+ Months | Determine budget | TRUE | | |
| 12+ Months | Book venue | TRUE | | |
| 12+ Months | Hire photographer | TRUE | | |
| 9-6 Months | Book caterer | TRUE | | |
| 9-6 Months | Hire florist | TRUE | | |
| 9-6 Months | Book DJ/band | TRUE | | |
| 9-6 Months | Order wedding dress | TRUE | | |
| 6-3 Months | Send save-the-dates | TRUE | | |
| 6-3 Months | Order invitations | TRUE | | |
| 6-3 Months | Book hair & makeup | FALSE | 1/20/2025 | |
| 6-3 Months | Schedule cake tasting | FALSE | 1/25/2025 | |
| 90 Days | Mail invitations | FALSE | 6/14/2025 | |
| 90 Days | Finalize guest count | FALSE | 7/14/2025 | |
| 30 Days | Final dress fitting | FALSE | 8/14/2025 | |
| 30 Days | Confirm all vendors | FALSE | 8/14/2025 | |
| Week Of | Rehearsal dinner | FALSE | 9/12/2025 | |
| Week Of | Pack honeymoon bags | FALSE | 9/13/2025 | |

**Column C Setup:**
1. Select column C
2. Insert > Checkbox

**Data Validation for Column A (Phase):**
- List: `12+ Months, 9-6 Months, 6-3 Months, 90 Days, 30 Days, Week Of, Wedding Day`

---

## Formatting Tips

### Colors (match the HTML dashboard):
| Element | Hex Code |
|---------|----------|
| Background | #F8F6F2 |
| Headers | #2C2C2C |
| Accent (gold) | #B8860B |
| Success (sage) | #9CAF88 |
| Pending (blush) | #E8B4B8 |
| Borders | #CFC6BC |

### Conditional Formatting:

**For RSVP Status (Guests tab, column D):**
1. Select column D
2. Format > Conditional formatting
3. Add rules:
   - "Attending" → Green background (#9CAF88)
   - "Declined" → Red background (#E8B4B8)
   - "Pending" → Yellow background (#F5E6A3)

**For Budget Balance (Budget tab, column G):**
1. Select column G
2. Format > Conditional formatting
3. Add rules:
   - Greater than 0 → Red text
   - Equal to 0 → Green text

**For Checklist Done (Checklist tab, column C):**
1. Select entire rows
2. Custom formula: `=$C2=TRUE`
3. Format: Strikethrough + gray text

---

## Useful Formulas Reference

```
Days until wedding:
=MAX(0, Config!B3 - TODAY())

Percentage complete:
=ROUND(COUNTIF(Checklist!C:C, TRUE) / COUNTA(Checklist!B:B) * 100, 0) & "%"

Total guests attending:
=COUNTIF(Guests!D:D, "Attending")

Budget remaining:
=Config!B5 - SUM(Budget!E:E)

Overdue tasks:
=COUNTIFS(Checklist!C:C, FALSE, Checklist!D:D, "<" & TODAY())

Tasks due this week:
=FILTER(Checklist!B:B, Checklist!D:D <= TODAY()+7, Checklist!C:C = FALSE)
```

---

## Next Steps

1. Copy this structure into your Google Sheet
2. Customize the sample data with your actual vendors, guests, etc.
3. Share with your partner and wedding party (View or Edit access)
4. Bookmark it for easy access!

**Pro tip:** Use Google Sheets mobile app to update RSVPs and tasks on the go!
