# Life OS v2 - Accounts Master Setup Guide

This guide will help you set up and run the script to create your Accounts Master Google Sheet.

## Prerequisites

- Python 3.7 or higher
- A Google account
- Internet connection

## Step 1: Install Python Dependencies

Navigate to the `life-os-v2` directory and install the required packages:

```bash
cd life-os-v2
pip install -r requirements.txt
```

Or if you're using Python 3 specifically:

```bash
pip3 install -r requirements.txt
```

## Step 2: Set Up Google Cloud Project & Get API Credentials

### 2.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name: `Life OS v2` (or any name you prefer)
5. Click "Create"
6. Wait for the project to be created, then select it from the project dropdown

### 2.2 Enable Google Sheets API

1. In the Google Cloud Console, make sure your project is selected
2. Click on the hamburger menu (☰) → "APIs & Services" → "Library"
3. In the search bar, type "Google Sheets API"
4. Click on "Google Sheets API" from the results
5. Click the "Enable" button
6. Wait for it to enable (this may take a few seconds)

### 2.3 Create OAuth 2.0 Credentials

1. In the Google Cloud Console, go to "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" at the top
3. Select "OAuth client ID"

**IMPORTANT:** If you see a message saying you need to configure the OAuth consent screen first:

#### Configure OAuth Consent Screen

1. Click "CONFIGURE CONSENT SCREEN"
2. Select "External" user type
3. Click "Create"
4. Fill in the required information:
   - **App name**: `Life OS v2`
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
5. Click "Save and Continue"
6. On the "Scopes" page, click "Save and Continue" (no need to add scopes manually)
7. On the "Test users" page, click "+ ADD USERS"
8. Enter your email address
9. Click "Add"
10. Click "Save and Continue"
11. Review the summary and click "Back to Dashboard"

#### Create OAuth Client ID

1. Go back to "Credentials" → "+ CREATE CREDENTIALS" → "OAuth client ID"
2. For "Application type", select **"Desktop app"**
3. Enter a name: `Life OS Desktop Client`
4. Click "Create"
5. You'll see a dialog with your client ID and secret - click "OK"
6. You'll now see your OAuth 2.0 Client ID in the list

### 2.4 Download Credentials

1. In the "OAuth 2.0 Client IDs" section, find your newly created client
2. Click the download icon (⬇️) on the right side of your client ID
3. This will download a JSON file with a long name like `client_secret_XXXXX.json`
4. Rename this file to `credentials.json`
5. Move `credentials.json` to the `life-os-v2` directory (same directory as `create_accounts_master.py`)

## Step 3: Run the Script

Once you have `credentials.json` in the `life-os-v2` directory, run:

```bash
python3 create_accounts_master.py
```

### What happens next:

1. A browser window will open asking you to sign in to your Google account
2. You'll be asked to grant permissions to the app
3. Click "Allow" to grant access
4. The script will create your spreadsheet
5. You'll see a success message with the URL to your new sheet

### First-time OAuth Flow

When you run the script for the first time:

1. **Browser will open automatically** - You'll see a Google sign-in page
2. **Sign in** - Use the same Google account you added as a test user
3. **Warning screen** - You might see "Google hasn't verified this app"
   - Click "Advanced"
   - Click "Go to Life OS v2 (unsafe)"
   - This is normal for personal projects
4. **Grant permissions** - Click "Allow" to grant access to Google Sheets
5. **Done!** - The browser will show "The authentication flow has completed"

The script will save your authentication in a `token.pickle` file, so you won't need to authenticate again.

## Step 4: Access Your New Spreadsheet

After the script completes, you'll see output like:

```
✅ SUCCESS! Your Accounts Master sheet is ready!

============================================================
📊 Spreadsheet: Life OS v2 - Michelle
🔗 URL: https://docs.google.com/spreadsheets/d/XXXXX
============================================================
```

Click the URL or copy it into your browser to open your new Accounts Master sheet!

## Troubleshooting

### "credentials.json file not found"

- Make sure you've downloaded the credentials file from Google Cloud Console
- Make sure you've renamed it to exactly `credentials.json`
- Make sure it's in the same directory as `create_accounts_master.py`

### "Access blocked: Life OS v2 hasn't verified this app"

This is normal for personal projects. To proceed:

1. Click "Advanced" at the bottom of the page
2. Click "Go to Life OS v2 (unsafe)"
3. Grant the requested permissions

Your data is safe - you're just authorizing your own script to access your own Google Sheets.

### "Permission denied" or "Invalid credentials"

1. Delete the `token.pickle` file if it exists
2. Run the script again
3. Make sure you're signing in with the same Google account you added as a test user

### Import errors

If you see errors like `ModuleNotFoundError: No module named 'google'`:

```bash
pip3 install -r requirements.txt
```

Make sure you're using Python 3:

```bash
python3 --version
```

## What Gets Created

The script creates a comprehensive Accounts Master spreadsheet with:

✅ **21 columns** for tracking all account details
✅ **Automatic formulas** for ID numbering and last review dates
✅ **Dropdown menus** for:
   - Account types (checking, savings, credit cards, investments, etc.)
   - Account status (active, inactive, closed, etc.)
   - Auto-pay settings
   - 2FA methods

✅ **Color-coded alerts** for:
   - Active accounts (green)
   - Closed accounts (gray)
   - Past due accounts (red)
   - Frozen accounts (orange)
   - Password age warnings (yellow/orange/red)

✅ **Live summary dashboard** showing:
   - Total and active account counts
   - Breakdown by account type
   - Security alerts (old passwords, missing 2FA)
   - Accounts needing review

✅ **Professional formatting**:
   - Frozen header row
   - Wrapped text
   - Proper column widths
   - Borders and styling

## Next Steps

1. Open your new spreadsheet
2. Start filling in Row 2 with your first account
3. Use the dropdown menus for consistency
4. Add all your accounts (checking, savings, credit cards, loans, investments)
5. Watch the summary dashboard update automatically!

## Security Notes

- The `credentials.json` file contains your OAuth client ID and secret
- The `token.pickle` file contains your personal access token
- **IMPORTANT**: Add both files to `.gitignore` if you're using version control
- Never share these files publicly
- These files only grant access to create/edit Google Sheets in YOUR account

## Need Help?

If you encounter any issues:

1. Check the Troubleshooting section above
2. Make sure all prerequisites are installed
3. Verify your credentials.json is in the right location
4. Try deleting token.pickle and re-authenticating

Enjoy your new financial tracking system! 💰✨
