# Life OS Google Sheets Automation Setup

## Prerequisites
- The Excel file `LIFE_Master_Tracker_AUTOMATION_READY.xlsx`
- A Google account with access to Google Drive and Sheets

---

## Step 1: Upload & Convert to Google Sheets

1. Go to [Google Drive](https://drive.google.com)
2. Click **+ New** → **File upload**
3. Select `LIFE_Master_Tracker_AUTOMATION_READY.xlsx` and upload it
4. Once uploaded, right-click the file → **Open with** → **Google Sheets**
5. This creates a native Google Sheet copy

---

## Step 2: Rename the Sheet

1. In the newly opened Google Sheet, click the title at the top left
2. Rename it to: `LIFE_OS_MASTER (LIVE)`
3. Press Enter to save

---

## Step 3: Set Up Apps Script

1. In your Google Sheet, go to **Extensions** → **Apps Script**
2. Delete any starter code in the editor
3. Copy the entire contents of `Code.gs` from this folder
4. Paste it into the Apps Script editor
5. Press **Ctrl+S** (or Cmd+S on Mac) to save
6. Name the project "Life OS Automation" when prompted

---

## Step 4: Authorize Permissions

1. Click the **Run** button (▶️) or select `testWeeklySummary` from the dropdown
2. Click **Review permissions** when prompted
3. Select your Google account
4. Click **Advanced** → **Go to Life OS Automation (unsafe)**
5. Click **Allow** to grant permissions

---

## Step 5: Create Time-Driven Triggers

1. In Apps Script, click the **Triggers** icon (clock) in the left sidebar
2. Click **+ Add Trigger** in the bottom right

### Trigger 1: Weekly Life OS Summary (Monday mornings)
| Setting | Value |
|---------|-------|
| Function | `weeklyLifeOS` |
| Deployment | Head |
| Event source | Time-driven |
| Type | Week timer |
| Day | Monday |
| Time | 8am to 9am |

### Trigger 2: Daily Stalled Alerts
| Setting | Value |
|---------|-------|
| Function | `stalledInterviewAlerts` |
| Deployment | Head |
| Event source | Time-driven |
| Type | Day timer |
| Time | 9am to 10am |

### Trigger 3: Daily Job Feed (Optional)
| Setting | Value |
|---------|-------|
| Function | `ingestJobFeed` |
| Deployment | Head |
| Event source | Time-driven |
| Type | Day timer |
| Time | 6am to 7am |

---

## Required Sheet Tabs

Ensure your spreadsheet has these tabs (with exact names including emojis):

- `🧾 Weekly Exec Summary` - Data in A3:B20 for the executive summary
- `📈 Job Pipeline` - Columns: Company, Role, [skip], [skip], [skip], Last Touch Date, [skip], Status
- `🔎 Job Feed (Auto)` - For auto-ingested job listings (columns: Source, Company, Title, Notes, Link, Date)

---

## Testing

Before relying on automated triggers, test each function manually:

1. In Apps Script, select `testWeeklySummary` from the function dropdown
2. Click **Run** (▶️)
3. Check your email for the summary
4. Repeat for `testStalledAlerts` and `testJobFeed`

---

## Troubleshooting

**"Sheet not found" error:**
- Verify tab names match exactly (including emojis)

**No email received:**
- Check spam folder
- Verify Gmail permissions were granted

**Job feed not populating:**
- Indeed RSS feeds may require different URL formats
- Check execution logs: View → Logs

---

## What Gets Automated

| Function | Frequency | What It Does |
|----------|-----------|--------------|
| `weeklyLifeOS` | Weekly (Mon) | Sends executive summary + stalled alerts |
| `stalledInterviewAlerts` | Daily | Emails if any job hasn't been touched in 14+ days |
| `ingestJobFeed` | Daily | Adds new VP/Director job listings from Indeed RSS |
