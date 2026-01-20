# Life OS Google Sheets Automation

Deploy Google Apps Script automations from the terminal using `clasp`.

## Prerequisites

- Node.js installed
- A Google account with the "LIFE_OS_MASTER (LIVE)" spreadsheet

## Setup Instructions

### 1. Install clasp globally

```bash
npm install -g @google/clasp
```

### 2. Enable the Google Apps Script API

Visit: https://script.google.com/home/usersettings

Toggle **"Google Apps Script API"** to **ON**.

### 3. Login to Google

```bash
clasp login
```

This opens a browser for Google OAuth. Authorize the access.

### 4. Create a new Apps Script project bound to your spreadsheet

First, get your spreadsheet ID from the URL:
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
```

Then create the project:
```bash
cd google-sheets-automation
clasp create --title "Life OS Automation" --parentId "YOUR_SPREADSHEET_ID"
```

### 5. Push the code

```bash
clasp push
```

When prompted about overwriting the manifest, type `y`.

### 6. Open in browser and set up triggers

```bash
clasp open
```

In the Apps Script editor:
1. Select `setupTriggers` from the function dropdown
2. Click **Run**
3. Authorize the permissions when prompted

This will automatically create all three triggers:
- **Weekly** (Monday 8am): Executive summary + stalled alerts
- **Daily** (9am): Stalled interview alerts
- **Daily** (7am): Job feed ingestion

## Alternative: Manual Trigger Setup

If you prefer, go to **Triggers** (clock icon) in the Apps Script editor and manually add triggers for:
- `weeklyLifeOS` → Weekly, Monday, 8-9am
- `stalledInterviewAlerts` → Daily, 9-10am
- `ingestJobFeed` → Daily, 7-8am

## Commands Reference

| Command | Description |
|---------|-------------|
| `clasp push` | Upload local changes to Google |
| `clasp pull` | Download changes from Google |
| `clasp open` | Open project in browser |
| `clasp logs` | View execution logs |
| `clasp run functionName` | Run a function (requires extra setup) |

## File Structure

```
google-sheets-automation/
├── Code.js           # Main automation script
├── appsscript.json   # Manifest (permissions, timezone)
├── .clasp.json       # Project config (created by clasp)
└── README.md         # This file
```

## Troubleshooting

**"Script not bound to spreadsheet"**: Make sure you used `--parentId` when creating the project.

**"Authorization required"**: Run `setupTriggers` manually once to grant permissions.

**"API not enabled"**: Visit https://script.google.com/home/usersettings and enable the API.
