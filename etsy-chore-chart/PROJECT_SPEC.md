# Kids Chore Chart System — Complete Project Specification

## Product Overview
A structured, parent-friendly Excel workbook system for tracking kids' chores, progress, and rewards. Designed to feel like a premium parenting tool — not a basic printable.

**Target Price:** $19–$39
**Format:** .xlsx (Excel compatible)
**Listing:** Etsy digital download

---

## PART 1 — Template Structure

### Workbook Tabs (4 sheets)

| Tab | Color Code | Purpose |
|-----|-----------|---------|
| Chore Chart | Blue | Main daily + weekly chore tracking |
| Weekly Summary | Amber | Day-by-day completion analysis |
| Reward Tracker | Green | Points + reward goal management |
| Instructions | Gray | Complete usage guide |

### Sheet 1: Chore Chart
- **10 daily chores** — customizable names, 1 point per completion
- **5 weekly chores** — customizable names, 2 points per completion
- **Mon–Sun columns** with dropdown checkmark (✓) validation
- **Auto-calculated DONE count** per chore row
- **Auto-calculated POINTS** per row
- **Summary section:**
  - Total Completed (all check-marks)
  - Total Points (weighted: daily=1, weekly=2)
  - Progress percentage toward goal
  - Reward Status ("REWARD EARNED!" / "Keep Going!")
  - Visual data bar progress indicator
- **Input fields:** Child's Name, Week Of, Points Goal
- **Notes section** for reward description
- **Frozen panes** below column headers

### Sheet 2: Weekly Summary
- Day-by-day breakdown (Mon–Sun)
- Per-day: daily done, weekly done, total done, % complete, status
- Status labels: "Great!" (≥80%), "Good" (≥50%), "Needs Work" (<50%)
- Conditional formatting with data bars on % column
- Color-coded status cells (green/red)
- Overall stats: total check-marks, completion rate, points vs goal
- Bar chart visualization of daily completion

### Sheet 3: Reward Tracker
- Current week status (linked to Chore Chart)
- Points earned vs goal display
- Progress percentage + visual progress bar
- 8-week Reward Bank for multi-week tracking
- Per-week: points earned, goal, % achieved, reward earned?, reward given, notes
- Cumulative stats: total points, total rewards, average completion

### Sheet 4: Instructions
- Getting Started guide
- Daily chore tracking instructions
- Weekly chore tracking instructions
- Summary interpretation
- Weekly Summary tab usage
- Reward Tracker tab usage
- Tips for success
- Editable vs locked cells explanation

---

## PART 2 — Color System

### Final HEX Codes

| Role | HEX | Usage |
|------|-----|-------|
| **Primary** | `#4A90D9` | Headers, main accents, progress |
| **Primary Light** | `#D6E4F0` | Alternating rows, subtle backgrounds |
| **Secondary** | `#F5A623` | Reward/points highlights, amber accents |
| **Secondary Light** | `#FFF3D6` | Reward zone backgrounds |
| **Success** | `#27AE60` | Completed, reward earned, checkmarks |
| **Success Light** | `#D5F5E3` | Success backgrounds |
| **Incomplete** | `#E0E0E0` | Not-done indicators |
| **Danger** | `#E74C3C` | Missed/alert indicators |
| **Header BG** | `#2C3E50` | Main title bars |
| **Sub Header** | `#34495E` | Column headers |
| **Body BG** | `#FAFBFC` | Off-white page background |
| **Input BG** | `#FFFFF0` | Editable cells (ivory) |
| **Border** | `#BDC3C7` | Soft cell borders |
| **Dark Text** | `#2C3E50` | Primary text color |

### Design Principles
- No harsh neon colors
- No rainbow overload
- Playful but controlled palette
- Light background with high readability
- Reward earned state visually stands out (green glow)
- Completion is visually satisfying (green checkmarks)

---

## PART 3 — Formula Upgrades

### Chore Chart Formulas
```
DONE count:     =COUNTIF(C{row}:I{row},"✓")
Daily points:   =J{row}             (1 per check)
Weekly points:  =J{row}*2           (2 per check)
Total completed: =SUM(J9:J18,J22:J26)
Total points:   =SUM(K9:K18,K22:K26)
Progress %:     =IF(J5=0,0,SUM(K9:K18,K22:K26)/J5)
Reward status:  =IF(SUM(K9:K18,K22:K26)>=J5,"REWARD EARNED!","Keep Going!")
```

### Weekly Summary Formulas
```
Daily done:     =COUNTIF('Chore Chart'!{col}9:{col}18,"✓")
Weekly done:    =COUNTIF('Chore Chart'!{col}22:{col}26,"✓")
All done:       =C{row}+E{row}
% complete:     =IF(H{row}=0,0,G{row}/H{row})
Status:         =IF(I{row}>=0.8,"Great!",IF(I{row}>=0.5,"Good","Needs Work"))
```

### Reward Tracker Formulas
```
Points earned:  ='Chore Chart'!I29
Points goal:    ='Chore Chart'!J5
Progress %:     =IF('Chore Chart'!J5=0,0,'Chore Chart'!I29/'Chore Chart'!J5)
Reward earned:  =IF(C{row}>=D{row},"YES","NO")
Bank %:         =IF(D{row}="","",(IF(D{row}=0,0,C{row}/D{row})))
Total rewards:  =COUNTIF(F11:F18,"YES")
Avg completion: =IF(COUNTA(E11:E18)=0,0,AVERAGE(E11:E18))
```

---

## PART 4 — UX Upgrades

1. **Gridlines removed** — clean, modern look
2. **Frozen panes** — headers always visible while scrolling
3. **Data validation** — dropdown checkmarks prevent input errors
4. **Conditional formatting:**
   - Data bars on progress percentages
   - Green highlight on "REWARD EARNED!" and "Great!" statuses
   - Red highlight on "Needs Work" and "NO" statuses
5. **Alternating row shading** — improved readability
6. **Input cell coloring** — ivory background marks editable cells
7. **Section headers** — clear visual separation between areas
8. **Tab color coding** — blue/amber/green/gray for quick navigation
9. **Font hierarchy:**
   - 20pt bold: Main title
   - 13pt bold: Section headers
   - 11pt: Body text
   - 10pt: Column headers, row numbers
10. **Clear spacing** — spacer rows between sections

---

## PART 5 — Etsy Listing Images

### Specifications (all 7 images)
- **Dimensions:** 2700 x 2025 px
- **Ratio:** 4:3
- **DPI:** 300
- **Color mode:** RGB
- **Safe margin:** 150 px
- **Background:** Light (#FAFBFC)
- **Font:** DejaVu Sans (system fallback)

### Image Inventory

| # | File | Focus |
|---|------|-------|
| 1 | `01_hero.png` | Full system overview with grid, progress, rewards |
| 2 | `02_how_it_works.png` | 3-step process: Assign → Track → Earn |
| 3 | `03_progress_tracking.png` | Completion %, bars, daily breakdown |
| 4 | `04_reward_system.png` | Points tracking, threshold, earned indicator |
| 5 | `05_parent_controls.png` | Editable zones, protected formulas, input guide |
| 6 | `06_everything_included.png` | 4-sheet preview grid with feature lists |
| 7 | `07_outcome.png` | Dashboard overview, outcome statements |

---

## File Structure

```
etsy-chore-chart/
├── product/
│   ├── create_workbook.py          # Excel generator script
│   └── Kids_Chore_Chart_System.xlsx # Final product file
├── images/
│   ├── create_images.py            # Image generator script
│   ├── 01_hero.png
│   ├── 02_how_it_works.png
│   ├── 03_progress_tracking.png
│   ├── 04_reward_system.png
│   ├── 05_parent_controls.png
│   ├── 06_everything_included.png
│   └── 07_outcome.png
└── PROJECT_SPEC.md                 # This file
```
