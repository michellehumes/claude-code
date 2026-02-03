# Excel Life Tracker

A comprehensive Excel-based personal life tracking system that helps you monitor and manage all aspects of your life in one workbook.

## Overview

The Excel Life Tracker is a fully-featured, local-first tracking system built as a single `.xlsx` file. It covers daily wellness, habits, tasks, goals, finances, job search, and health/fertility tracking with automated dashboards and insights.

## Features

### 📊 **Dashboard**
- Real-time KPIs for last 7 and 30 days
- Average sleep, mood, and energy metrics
- Financial summary (income, expenses, cash flow)
- Job search pipeline status
- Task completion rates
- Habit tracking completion percentages

### 📅 **Daily Log**
Track your daily life metrics:
- Sleep hours and quality
- Steps and exercise minutes
- Water intake
- Mood, energy, and stress levels
- Daily highlights and notes

### ✅ **Habit Tracking**
- Log daily habits with completion status
- Monthly completion rate calculations
- Category-based habit organization
- Progress tracking over time

### 📝 **Tasks & Goals**
- **Tasks**: Manage to-dos with priorities, due dates, and status tracking
- **Goals**: Set long-term goals with progress tracking and target values
- Automatic overdue task highlighting
- Visual progress indicators

### 💰 **Finance Tracker**
- Track income and expenses
- Category-based spending analysis
- Monthly financial summaries
- Account-level transaction tracking
- Net cash flow calculations

### 💼 **Job Search Pipeline**
- Track job applications from target to offer
- Salary range tracking
- Application status management
- Next action reminders
- Pipeline summary statistics

### 🩺 **Health & Fertility**
- Menstrual cycle tracking
- Ovulation prediction (cycle day, DPO)
- BBT temperature logging
- LH test results
- Symptom tracking
- Fertility phase visualization

## Getting Started

### Quick Start

1. **Open the workbook**: Double-click `Life_Tracker.xlsx`
2. **Review the README sheet**: Understand how the tracker works
3. **Check the SETUP sheet**: Review and customize dropdown lists
4. **Start tracking**: Add your first entries to any module
5. **View the Dashboard**: See your insights update in real-time

### First Steps

1. **Customize Categories** (SETUP sheet):
   - Review all dropdown lists
   - Add or modify categories to fit your needs
   - Named ranges will update automatically

2. **Add Sample Data or Clear It**:
   - Sample data is pre-loaded for demonstration
   - Delete sample rows and add your own data
   - Tables will auto-expand as you add rows

3. **Daily Routine**:
   - Update DAILY_LOG with yesterday's metrics
   - Check HABIT_LOG and mark completed habits
   - Review TASKS and update status
   - Check DASHBOARD for trends

## Workbook Structure

| Sheet | Purpose |
|-------|---------|
| **README** | Usage instructions and quick reference |
| **SETUP** | Configuration and dropdown list management |
| **DASHBOARD** | High-level KPIs, charts, and insights |
| **DAILY_LOG** | Daily metrics (sleep, mood, exercise, etc.) |
| **HABIT_LOG** | Habit tracking and completion rates |
| **TASKS** | Task management with due dates and priorities |
| **GOALS** | Long-term goal tracking with progress |
| **FINANCE** | Personal finance transaction tracking |
| **JOB_SEARCH** | Job application pipeline management |
| **HEALTH_FERTILITY** | Cycle tracking and fertility monitoring |

## Key Features

### Automated Formulas
- All calculations update automatically
- Dashboard pulls from all data sheets
- No manual updates required
- Structured references for easy maintenance

### Data Validation
- Dropdown menus for consistent data entry
- All lists managed in SETUP sheet
- Easy to customize categories
- Prevents data entry errors

### Conditional Formatting
- Visual highlighting for overdue tasks
- Completed tasks shown in green
- Fertility phases color-coded
- Weekend highlighting in daily log

### Excel Tables
- Auto-expanding as you add data
- Structured references in formulas
- Easy sorting and filtering
- Professional formatting

## Technical Details

- **Format**: Excel 365 (`.xlsx`)
- **Compatibility**: Windows and Mac
- **Size**: ~28 KB (lightweight and portable)
- **Dependencies**: None (no macros, no VBA, no external data)
- **Data Storage**: Local file only (privacy-first)

## Customization

### Adding New Categories

1. Go to **SETUP** sheet
2. Find the list you want to modify
3. Add new values in the appropriate column
4. The named range updates automatically
5. New values appear in all dropdown menus

### Modifying Formulas

All formulas use structured references (e.g., `tblDaily[Mood]`), making them:
- Easy to understand
- Self-documenting
- Resistant to errors when adding rows
- Simple to modify

### Adding Charts

The Dashboard includes placeholders for charts. To add your own:
1. Select data from any sheet
2. Insert → Recommended Charts
3. Choose your preferred visualization
4. Copy/move chart to Dashboard

## Rebuilding the Workbook

If you want to regenerate the workbook or modify its structure:

```bash
cd life-tracker
python3 create_life_tracker.py
```

This will create a fresh `Life_Tracker.xlsx` with all features and sample data.

### Prerequisites

```bash
pip3 install openpyxl
```

## Tips for Best Results

1. **Be Consistent**: Enter data daily for best insights
2. **Use Standard Categories**: Stick to predefined lists for better analysis
3. **Review Dashboard Weekly**: Check trends and adjust habits
4. **Back Up Regularly**: Save copies of your tracker monthly
5. **Customize Gradually**: Start with default setup, adjust as needed

## Data Privacy

- ✅ All data stored locally in the Excel file
- ✅ No cloud sync or external connections
- ✅ No macros or scripts that run automatically
- ✅ Complete control over your personal data
- ⚠️ Remember to back up your file regularly

## Support & Maintenance

### Common Issues

**Formulas showing #N/A or #DIV/0!**
- Add more data rows to the relevant tables
- Sample data may have been deleted

**Dropdown not showing expected values**
- Check SETUP sheet for the named range
- Ensure values are entered correctly

**Table not expanding**
- Make sure you're adding data within the table
- Or add a new row using the Table Tools menu

### Future Enhancements

Consider adding:
- Pivot tables for deeper analysis
- Additional charts on Dashboard
- Custom conditional formatting rules
- More calculated metrics

## Files in This Directory

- `Life_Tracker.xlsx` - The complete Excel workbook (ready to use)
- `create_life_tracker.py` - Python script to rebuild the workbook
- `README.md` - This file
- `EXCEL_TRACKER_PROMPT.md` - Original build specifications

## Version History

- **v1.0.0** (February 2026) - Initial release
  - 10 integrated tracking modules
  - Automated dashboard with KPIs
  - Sample data included
  - Full documentation

## License

Built for personal use by Michelle (Shelzy) Humes. Feel free to modify and customize for your own needs.

---

**Questions or issues?** Check the README sheet inside the workbook for quick reference guides.
