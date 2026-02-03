# Excel Life Tracker - Build Prompt

You are an expert Excel 365 template designer. Build a clean, modern, and fully functional Life Tracker workbook in Microsoft Excel (not Google Sheets). The output must be a single .xlsx file that is ready to use without any macros or external data connections.

## Goal
Create a personal life-tracking workbook that covers daily well-being, habits, tasks, goals, finances, job search, and health/fertility tracking. It should be easy to use daily, provide monthly summaries, and surface key insights on a Dashboard.

## Deliverables
- One Excel workbook (.xlsx)
- Sheets and features exactly as specified below
- Pre-loaded with 5-10 sample rows per input table to demonstrate use

## Constraints
- Excel 365 compatible (Windows and Mac)
- No VBA, no macros, no Power Query
- Use Excel Tables and structured references
- Use named ranges for dropdown lists
- Keep formatting clean and print-friendly

## Workbook Structure
1. README
2. SETUP
3. DASHBOARD
4. DAILY_LOG
5. HABIT_LOG
6. TASKS
7. GOALS
8. FINANCE
9. JOB_SEARCH
10. HEALTH_FERTILITY

---

## Sheet: README
Purpose: quick start and usage tips.

Include:
- What the tracker is for
- How to add daily entries
- How to add tasks and goals
- How to update categories in SETUP
- How to read the Dashboard

---

## Sheet: SETUP
Purpose: all lists and configuration settings.

Layout:
- Cell B2: `Start Year` (default 2026)
- Cell B3: `Start Date` (default 2026-01-01)
- Cell B4: `Owner Name` (default Michelle Humes)

Lists (create as named ranges):
- `list_mood` = 1,2,3,4,5
- `list_energy` = 1,2,3,4,5
- `list_stress` = 1,2,3,4,5
- `list_yes_no` = Yes, No
- `list_task_status` = Backlog, Today, In Progress, Completed
- `list_task_priority` = Low, Medium, High
- `list_task_category` = Health, Career, Business, Personal, Relationships
- `list_goal_status` = Active, Paused, Completed
- `list_goal_timeframe` = Short, Medium, Long
- `list_finance_type` = Income, Expense
- `list_finance_category` = Housing, Utilities, Groceries, Dining, Transportation, Health, Fitness, Subscriptions, Shopping, Travel, Education, Business, Savings, Other
- `list_job_status` = Target, Applied, Screening, Interview, Offer, Rejected, Stalled, Withdrawn
- `list_health_symptom` = Cramps, Bloating, Headache, Fatigue, Nausea, Tenderness, Other
- `list_lh_test` = Negative, Positive, Not Taken
- `list_cycle_phase` = Follicular, Fertile, Ovulation, Luteal, Implantation

---

## Sheet: DAILY_LOG
Purpose: daily life metrics and notes.

Create an Excel Table named `tblDaily` with these columns:
- Date (date)
- Day (formula)
- Week (formula)
- Month (formula)
- SleepHours
- SleepQuality (dropdown list_mood)
- Steps
- ExerciseMinutes
- WaterOz
- Mood (dropdown list_mood)
- Energy (dropdown list_energy)
- Stress (dropdown list_stress)
- Highlights (text)
- Notes (text)

Formulas:
- Day: `=TEXT([@Date],"ddd")`
- Week: `=WEEKNUM([@Date])`
- Month: `=TEXT([@Date],"yyyy-mm")`

Formatting:
- Freeze header row
- Alternate row shading
- Date column in yyyy-mm-dd format
- Conditional formatting to highlight weekends (Day = Sat or Sun)

---

## Sheet: HABIT_LOG
Purpose: simple habit logging and completion tracking.

Create an Excel Table named `tblHabits` with columns:
- Date (date)
- Habit (text)
- Category (text)
- Value (number or text)
- Done (dropdown list_yes_no)
- Notes (text)

Add a small summary area above or to the right:
- Monthly Habit Completion % by Habit (use COUNTIFS)
- Formula example: `=IFERROR(COUNTIFS(tblHabits[Habit],"Exercise",tblHabits[Done],"Yes",tblHabits[Date],">="&EOMONTH(TODAY(),-1)+1,tblHabits[Date],"<="&EOMONTH(TODAY(),0)) / COUNTIFS(tblHabits[Habit],"Exercise",tblHabits[Date],">="&EOMONTH(TODAY(),-1)+1,tblHabits[Date],"<="&EOMONTH(TODAY(),0)),0)`

---

## Sheet: TASKS
Purpose: task management with due dates and status.

Create an Excel Table named `tblTasks` with columns:
- Task
- Category (dropdown list_task_category)
- Priority (dropdown list_task_priority)
- Status (dropdown list_task_status)
- DueDate
- CompletedDate
- Notes
- IsOverdue (formula)

Formula:
- IsOverdue: `=IF(AND([@Status]<>"Completed",[@DueDate]<>"",[@DueDate]<TODAY()),"Yes","No")`

Formatting:
- Conditional formatting: red fill if IsOverdue = Yes
- Green fill if Status = Completed

---

## Sheet: GOALS
Purpose: long-term goals with progress.

Create an Excel Table named `tblGoals` with columns:
- Goal
- Category (dropdown list_task_category)
- Timeframe (dropdown list_goal_timeframe)
- Status (dropdown list_goal_status)
- StartDate
- TargetDate
- TargetValue
- CurrentValue
- ProgressPct (formula)
- Notes

Formula:
- ProgressPct: `=IF([@TargetValue]="", "", MIN(1, [@CurrentValue]/[@TargetValue]))`

Format ProgressPct as percentage and add data bars.

---

## Sheet: FINANCE
Purpose: personal finance tracking.

Create an Excel Table named `tblFinance` with columns:
- Date
- Description
- Category (dropdown list_finance_category)
- Type (dropdown list_finance_type)
- Amount
- Account
- Owner
- Notes

Rules:
- Income should be positive; Expenses should be positive but interpreted as outflows in summary

Add a monthly summary section to the right:
- Total Income (current month)
- Total Expenses (current month)
- Net Cash Flow

Formula examples:
- Income: `=SUMIFS(tblFinance[Amount],tblFinance[Type],"Income",tblFinance[Date],">="&EOMONTH(TODAY(),-1)+1,tblFinance[Date],"<="&EOMONTH(TODAY(),0))`
- Expenses: `=SUMIFS(tblFinance[Amount],tblFinance[Type],"Expense",tblFinance[Date],">="&EOMONTH(TODAY(),-1)+1,tblFinance[Date],"<="&EOMONTH(TODAY(),0))`
- Net: `=Income-Expenses`

---

## Sheet: JOB_SEARCH
Purpose: job application pipeline tracking.

Create an Excel Table named `tblJobs` with columns:
- Company
- Role
- Level
- SalaryMin
- SalaryMax
- Location
- Remote (dropdown list_yes_no)
- Status (dropdown list_job_status)
- AppliedDate
- LastContact
- NextAction
- NextActionDate
- Notes

Add a small summary area:
- Count by Status (use COUNTIF)
- Average SalaryMin and SalaryMax for active roles

---

## Sheet: HEALTH_FERTILITY
Purpose: health and fertility tracking (optional but included).

Create an Excel Table named `tblHealth` with columns:
- Date
- CycleDay
- DPO
- Phase (dropdown list_cycle_phase)
- Temperature
- LHTest (dropdown list_lh_test)
- Symptoms (dropdown list_health_symptom)
- Mood (dropdown list_mood)
- Energy (dropdown list_energy)
- SexualActivity (dropdown list_yes_no)
- Notes

Formatting:
- Conditional formatting by Phase (light color fills)

---

## Sheet: DASHBOARD
Purpose: high-level insights and trends.

Include:
- KPI cards for last 7 days and last 30 days:
  - Average SleepHours
  - Average Mood
  - Average Energy
  - Total ExerciseMinutes
  - Tasks Completed
  - Habit Completion %
  - Total Expenses
  - Net Cash Flow
- A monthly trend chart for Mood and SleepHours
- A bar chart for Expenses by Category (current month)
- A small job pipeline summary (counts by status)

Formulas:
- Use AVERAGEIFS and SUMIFS tied to tblDaily and tblFinance
- Example for Avg Mood (last 7 days):
  - `=AVERAGEIFS(tblDaily[Mood],tblDaily[Date],">="&TODAY()-6,tblDaily[Date],"<="&TODAY())`

Design:
- Clean, neutral palette
- Use light gray backgrounds for headers
- Keep charts minimal, with clear labels

---

## General Formatting Rules
- Use consistent fonts (Calibri or Arial)
- Header rows bold with light gray fill (#f5f5f5)
- Alternate row shading for tables
- Freeze top row on data-entry sheets
- Apply data validation to all list-based columns

---

## Final Checks
- All formulas should work with sample data
- No #N/A or #DIV/0! in the Dashboard
- Tables expand automatically when new rows are added
- All named ranges correctly referenced in dropdowns

Build the workbook exactly as specified. Use sample data that looks realistic and aligns with the life tracker theme.
