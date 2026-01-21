#!/usr/bin/env python3
"""
CSV to Google Sheets Importer
This script imports a CSV file into the Transactions tab of your Financial Dashboard

Prerequisites:
1. Install required packages: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas
2. Set up Google Cloud Project and enable Sheets API
3. Download OAuth credentials JSON file

Usage:
    python import_csv_to_sheets.py <csv_file_path> <spreadsheet_id>

Example:
    python import_csv_to_sheets.py Transactions_20260120T223550.csv 1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw
"""

import sys
import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    """Get valid user credentials from storage or run auth flow."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found!")
                print("\nTo get credentials.json:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select existing")
                print("3. Enable Google Sheets API")
                print("4. Go to 'Credentials' and create OAuth 2.0 Client ID")
                print("5. Download the JSON and save as 'credentials.json'")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def read_csv_file(csv_path):
    """Read CSV file and return as list of lists."""
    try:
        df = pd.read_csv(csv_path)
        print(f"✓ Read CSV file: {len(df)} rows, {len(df.columns)} columns")
        print(f"  Columns: {', '.join(df.columns.tolist())}")

        # Convert DataFrame to list of lists
        data = df.values.tolist()
        return data
    except Exception as e:
        print(f"ERROR reading CSV: {e}")
        sys.exit(1)

def import_to_sheets(spreadsheet_id, csv_path):
    """Import CSV data to Google Sheets."""
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)

        # Read CSV data
        print(f"\nReading CSV file: {csv_path}")
        data = read_csv_file(csv_path)

        # Prepare the data
        sheet_name = '📊 Transactions'
        range_name = f'{sheet_name}!A2'  # Start at row 2 (below headers)

        body = {
            'values': data
        }

        print(f"\nImporting {len(data)} rows to '{sheet_name}' tab...")

        # Clear existing data (except headers)
        clear_range = f'{sheet_name}!A2:Z'
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=clear_range
        ).execute()

        print("✓ Cleared existing data")

        # Append new data
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()

        print(f"✓ Successfully imported {result.get('updatedCells')} cells")
        print(f"✓ Import complete!")

        # Create a summary
        print("\n" + "="*60)
        print("IMPORT SUMMARY")
        print("="*60)
        print(f"Spreadsheet ID: {spreadsheet_id}")
        print(f"Sheet: {sheet_name}")
        print(f"Rows imported: {len(data)}")
        print(f"Cells updated: {result.get('updatedCells')}")
        print(f"\nView your dashboard at:")
        print(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
        print("="*60)

    except HttpError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

def main():
    """Main function."""
    if len(sys.argv) != 3:
        print("Usage: python import_csv_to_sheets.py <csv_file_path> <spreadsheet_id>")
        print("\nExample:")
        print("  python import_csv_to_sheets.py Transactions.csv 1nUATgIQEXXrHhLlfC9j8WQbHyjvWoBmpDzIzCfjmwVw")
        print("\nNote: The spreadsheet_id is the long string in your Google Sheets URL")
        sys.exit(1)

    csv_path = sys.argv[1]
    spreadsheet_id = sys.argv[2]

    # Validate CSV file exists
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found: {csv_path}")
        sys.exit(1)

    print("="*60)
    print("FINANCIAL DASHBOARD - CSV IMPORTER")
    print("="*60)

    import_to_sheets(spreadsheet_id, csv_path)

if __name__ == '__main__':
    main()
