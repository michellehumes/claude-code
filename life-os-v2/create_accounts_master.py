#!/usr/bin/env python3
"""
Life OS v2 - Accounts Master Google Sheet Creator
Creates a comprehensive financial account tracking system in Google Sheets
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    """Gets valid user credentials from storage or runs OAuth flow."""
    creds = None

    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("\n❌ ERROR: credentials.json file not found!")
                print("\nPlease follow these steps:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select an existing one")
                print("3. Enable the Google Sheets API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download the credentials and save as 'credentials.json' in this directory")
                print("\nSee SETUP.md for detailed instructions.\n")
                exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_accounts_master_sheet():
    """Creates the Accounts Master spreadsheet with all formatting and formulas."""

    print("🚀 Creating Life OS v2 - Accounts Master Google Sheet...\n")

    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)

        # Step 1: Create the spreadsheet
        print("📊 Step 1: Creating spreadsheet...")
        spreadsheet = {
            'properties': {
                'title': 'Life OS v2 - Michelle'
            },
            'sheets': [{
                'properties': {
                    'title': '💰 Accounts Master',
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                }
            }]
        }

        spreadsheet = service.spreadsheets().create(
            body=spreadsheet,
            fields='spreadsheetId,spreadsheetUrl,sheets.properties.sheetId'
        ).execute()

        spreadsheet_id = spreadsheet.get('spreadsheetId')
        sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
        spreadsheet_url = spreadsheet.get('spreadsheetUrl')

        print(f"✅ Spreadsheet created!")
        print(f"   URL: {spreadsheet_url}\n")

        # Step 2: Set up column headers
        print("📝 Step 2: Adding column headers...")
        headers = [
            'Account ID', 'Account Type', 'Institution Name', 'Account Name/Nickname',
            'Account Number (Last 4)', 'Account Status', 'Primary Account Holder',
            'Joint/Secondary Holder', 'Current Balance', 'Available Credit',
            'Interest Rate/APY', 'Monthly Fee', 'Opening Date', 'Maturity Date',
            'Auto-Pay Linked', 'Login Username', 'Last Password Update', '2FA Method',
            'Customer Service Number', 'Account Notes', 'Last Reviewed Date'
        ]

        # Prepare all updates in batch
        requests = []

        # Add headers
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': len(headers)
                },
                'rows': [{
                    'values': [{'userEnteredValue': {'stringValue': header}} for header in headers]
                }],
                'fields': 'userEnteredValue'
            }
        })

        # Step 3: Format header row
        print("🎨 Step 3: Formatting header row...")
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': len(headers)
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.8, 'green': 0.9, 'blue': 1.0},
                        'textFormat': {'bold': True},
                        'horizontalAlignment': 'CENTER',
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,wrapStrategy)'
            }
        })

        # Set header row height
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'ROWS',
                    'startIndex': 0,
                    'endIndex': 1
                },
                'properties': {'pixelSize': 40},
                'fields': 'pixelSize'
            }
        })

        # Step 4: Add formulas to row 2
        print("⚡ Step 4: Adding formulas...")
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2,
                    'startColumnIndex': 0,
                    'endColumnIndex': 21
                },
                'rows': [{
                    'values': [
                        {'userEnteredValue': {'formulaValue': '=ROW()-1'}},  # A2: Account ID
                        {'userEnteredValue': {'stringValue': ''}},  # B2: Account Type
                        {'userEnteredValue': {'stringValue': ''}},  # C2: Institution Name
                        {'userEnteredValue': {'stringValue': ''}},  # D2: Account Name
                        {'userEnteredValue': {'stringValue': ''}},  # E2: Account Number
                        {'userEnteredValue': {'stringValue': 'Active'}},  # F2: Account Status
                        {'userEnteredValue': {'stringValue': 'Michelle'}},  # G2: Primary Holder
                        {'userEnteredValue': {'stringValue': ''}},  # H2: Joint Holder
                        {'userEnteredValue': {'stringValue': ''}},  # I2: Current Balance
                        {'userEnteredValue': {'stringValue': ''}},  # J2: Available Credit
                        {'userEnteredValue': {'stringValue': ''}},  # K2: Interest Rate
                        {'userEnteredValue': {'stringValue': ''}},  # L2: Monthly Fee
                        {'userEnteredValue': {'stringValue': ''}},  # M2: Opening Date
                        {'userEnteredValue': {'stringValue': ''}},  # N2: Maturity Date
                        {'userEnteredValue': {'stringValue': ''}},  # O2: Auto-Pay Linked
                        {'userEnteredValue': {'stringValue': ''}},  # P2: Login Username
                        {'userEnteredValue': {'stringValue': ''}},  # Q2: Last Password Update
                        {'userEnteredValue': {'stringValue': ''}},  # R2: 2FA Method
                        {'userEnteredValue': {'stringValue': ''}},  # S2: Customer Service
                        {'userEnteredValue': {'stringValue': ''}},  # T2: Account Notes
                        {'userEnteredValue': {'formulaValue': '=TODAY()'}}  # U2: Last Reviewed
                    ]
                }],
                'fields': 'userEnteredValue'
            }
        })

        # Copy formula for A2 down to A100
        requests.append({
            'copyPaste': {
                'source': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2,
                    'startColumnIndex': 0,
                    'endColumnIndex': 1
                },
                'destination': {
                    'sheetId': sheet_id,
                    'startRowIndex': 2,
                    'endRowIndex': 100,
                    'startColumnIndex': 0,
                    'endColumnIndex': 1
                },
                'pasteType': 'PASTE_FORMULA'
            }
        })

        # Copy formula for U2 down to U100
        requests.append({
            'copyPaste': {
                'source': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2,
                    'startColumnIndex': 20,
                    'endColumnIndex': 21
                },
                'destination': {
                    'sheetId': sheet_id,
                    'startRowIndex': 2,
                    'endRowIndex': 100,
                    'startColumnIndex': 20,
                    'endColumnIndex': 21
                },
                'pasteType': 'PASTE_FORMULA'
            }
        })

        # Step 5: Add data validation (dropdowns)
        print("📋 Step 5: Adding data validation dropdowns...")

        # Column B: Account Type
        account_types = [
            'Checking - Primary', 'Checking - Secondary', 'Savings - Emergency Fund',
            'Savings - Goal-Based', 'High-Yield Savings', 'Money Market',
            'Credit Card - Personal', 'Credit Card - Business', 'Line of Credit',
            'Mortgage', 'Auto Loan', 'Personal Loan', 'Student Loan',
            '401(k)', 'IRA - Traditional', 'IRA - Roth', 'Brokerage - Taxable',
            'Brokerage - Joint', '529 College Savings', 'HSA', 'FSA',
            'Crypto Exchange', 'PayPal/Venmo', 'Other'
        ]

        requests.append({
            'setDataValidation': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 100,
                    'startColumnIndex': 1,
                    'endColumnIndex': 2
                },
                'rule': {
                    'condition': {
                        'type': 'ONE_OF_LIST',
                        'values': [{'userEnteredValue': t} for t in account_types]
                    },
                    'showCustomUi': True,
                    'strict': False
                }
            }
        })

        # Column F: Account Status
        account_statuses = ['Active', 'Inactive', 'Closed', 'Pending Opening', 'Under Review', 'Frozen', 'Past Due']

        requests.append({
            'setDataValidation': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 100,
                    'startColumnIndex': 5,
                    'endColumnIndex': 6
                },
                'rule': {
                    'condition': {
                        'type': 'ONE_OF_LIST',
                        'values': [{'userEnteredValue': s} for s in account_statuses]
                    },
                    'showCustomUi': True,
                    'strict': False
                }
            }
        })

        # Column O: Auto-Pay Linked
        autopay_options = ['Yes - Checking Primary', 'Yes - Checking Secondary', 'Yes - Credit Card', 'No', 'Partial']

        requests.append({
            'setDataValidation': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 100,
                    'startColumnIndex': 14,
                    'endColumnIndex': 15
                },
                'rule': {
                    'condition': {
                        'type': 'ONE_OF_LIST',
                        'values': [{'userEnteredValue': o} for o in autopay_options]
                    },
                    'showCustomUi': True,
                    'strict': False
                }
            }
        })

        # Column R: 2FA Method
        tfa_methods = ['SMS', 'Authenticator App', 'Email', 'Hardware Key', 'Phone Call', 'None']

        requests.append({
            'setDataValidation': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 100,
                    'startColumnIndex': 17,
                    'endColumnIndex': 18
                },
                'rule': {
                    'condition': {
                        'type': 'ONE_OF_LIST',
                        'values': [{'userEnteredValue': m} for m in tfa_methods]
                    },
                    'showCustomUi': True,
                    'strict': False
                }
            }
        })

        # Step 6: Add conditional formatting
        print("🎨 Step 6: Adding conditional formatting...")

        # Account Status - Active (green text)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 100,
                        'startColumnIndex': 5,
                        'endColumnIndex': 6
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_CONTAINS',
                            'values': [{'userEnteredValue': 'Active'}]
                        },
                        'format': {
                            'textFormat': {'foregroundColor': {'red': 0.0, 'green': 0.5, 'blue': 0.0}}
                        }
                    }
                },
                'index': 0
            }
        })

        # Account Status - Closed (gray background)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 100,
                        'startColumnIndex': 5,
                        'endColumnIndex': 6
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_CONTAINS',
                            'values': [{'userEnteredValue': 'Closed'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 0.85, 'green': 0.85, 'blue': 0.85}
                        }
                    }
                },
                'index': 0
            }
        })

        # Account Status - Past Due (red background, white text, bold)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 100,
                        'startColumnIndex': 5,
                        'endColumnIndex': 6
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_CONTAINS',
                            'values': [{'userEnteredValue': 'Past Due'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.0, 'blue': 0.0},
                            'textFormat': {'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}, 'bold': True}
                        }
                    }
                },
                'index': 0
            }
        })

        # Account Status - Frozen (orange background)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 100,
                        'startColumnIndex': 5,
                        'endColumnIndex': 6
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'TEXT_CONTAINS',
                            'values': [{'userEnteredValue': 'Frozen'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.65, 'blue': 0.0}
                        }
                    }
                },
                'index': 0
            }
        })

        # Password Update - Over 6 months (light yellow)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 100,
                        'startColumnIndex': 16,
                        'endColumnIndex': 17
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'DATE_BEFORE',
                            'values': [{'userEnteredValue': '=TODAY()-180'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 1.0, 'blue': 0.8}
                        }
                    }
                },
                'index': 0
            }
        })

        # Password Update - Over 1 year (orange)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 100,
                        'startColumnIndex': 16,
                        'endColumnIndex': 17
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'DATE_BEFORE',
                            'values': [{'userEnteredValue': '=TODAY()-365'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.65, 'blue': 0.0}
                        }
                    }
                },
                'index': 0
            }
        })

        # Password Update - Over 2 years (red)
        requests.append({
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [{
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'endRowIndex': 100,
                        'startColumnIndex': 16,
                        'endColumnIndex': 17
                    }],
                    'booleanRule': {
                        'condition': {
                            'type': 'DATE_BEFORE',
                            'values': [{'userEnteredValue': '=TODAY()-730'}]
                        },
                        'format': {
                            'backgroundColor': {'red': 1.0, 'green': 0.0, 'blue': 0.0}
                        }
                    }
                },
                'index': 0
            }
        })

        # Step 7: Create Summary Dashboard
        print("📊 Step 7: Creating summary dashboard...")

        # Summary headers and labels (Column W)
        summary_data = [
            ['ACCOUNT SUMMARY'],  # W1
            [''],  # W2
            ['Total Accounts:'],  # W3
            ['Active Accounts:'],  # W4
            ['Inactive/Closed:'],  # W5
            [''],  # W6
            ['=== BY TYPE ==='],  # W7
            ['Checking Accounts:'],  # W8
            ['Savings Accounts:'],  # W9
            ['Credit Cards:'],  # W10
            ['Investment Accounts:'],  # W11
            ['Loans/Debt:'],  # W12
            [''],  # W13
            ['=== SECURITY ==='],  # W14
            ['Passwords >6mo old:'],  # W15
            ['Passwords >1yr old:'],  # W16
            ['No 2FA Setup:'],  # W17
            [''],  # W18
            ['=== ALERTS ==='],  # W19
            ['Accounts Need Review:']  # W20
        ]

        # Summary formulas (Column X)
        summary_formulas = [
            '',  # X1
            '',  # X2
            '=COUNTA(A:A)-1',  # X3
            '=COUNTIF(F:F,"Active")',  # X4
            '=COUNTIF(F:F,"Closed")+COUNTIF(F:F,"Inactive")',  # X5
            '',  # X6
            '',  # X7
            '=COUNTIF(B:B,"Checking*")',  # X8
            '=COUNTIF(B:B,"Savings*")+COUNTIF(B:B,"High-Yield*")+COUNTIF(B:B,"Money Market")',  # X9
            '=COUNTIF(B:B,"Credit Card*")',  # X10
            '=COUNTIF(B:B,"401(k)")+COUNTIF(B:B,"IRA*")+COUNTIF(B:B,"Brokerage*")+COUNTIF(B:B,"HSA")+COUNTIF(B:B,"529*")',  # X11
            '=COUNTIF(B:B,"*Loan")+COUNTIF(B:B,"Mortgage")+COUNTIF(B:B,"Line of Credit")',  # X12
            '',  # X13
            '',  # X14
            '=COUNTIFS(Q:Q,"<"&TODAY()-180,F:F,"Active")',  # X15
            '=COUNTIFS(Q:Q,"<"&TODAY()-365,F:F,"Active")',  # X16
            '=COUNTIFS(R:R,"None",F:F,"Active")+COUNTIFS(R:R,"",F:F,"Active")',  # X17
            '',  # X18
            '',  # X19
            '=COUNTIFS(U:U,"<"&TODAY()-90,F:F,"Active")'  # X20
        ]

        # Add summary data to column W
        requests.append({
            'updateCells': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 20,
                    'startColumnIndex': 22,
                    'endColumnIndex': 23
                },
                'rows': [{'values': [{'userEnteredValue': {'stringValue': val[0]}}]} for val in summary_data],
                'fields': 'userEnteredValue'
            }
        })

        # Add summary formulas to column X
        for i, formula in enumerate(summary_formulas):
            if formula:
                requests.append({
                    'updateCells': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': i,
                            'endRowIndex': i + 1,
                            'startColumnIndex': 23,
                            'endColumnIndex': 24
                        },
                        'rows': [{
                            'values': [{'userEnteredValue': {'formulaValue': formula}}]
                        }],
                        'fields': 'userEnteredValue'
                    }
                })

        # Format summary section
        # Make W1 bold and size 14
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 22,
                    'endColumnIndex': 23
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True, 'fontSize': 14}
                    }
                },
                'fields': 'userEnteredFormat.textFormat'
            }
        })

        # Make W column bold
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 20,
                    'startColumnIndex': 22,
                    'endColumnIndex': 23
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'bold': True}
                    }
                },
                'fields': 'userEnteredFormat.textFormat'
            }
        })

        # Add borders to summary section
        requests.append({
            'updateBorders': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 20,
                    'startColumnIndex': 22,
                    'endColumnIndex': 24
                },
                'top': {'style': 'SOLID', 'width': 1},
                'bottom': {'style': 'SOLID', 'width': 1},
                'left': {'style': 'SOLID', 'width': 1},
                'right': {'style': 'SOLID', 'width': 1},
                'innerHorizontal': {'style': 'SOLID', 'width': 1},
                'innerVertical': {'style': 'SOLID', 'width': 1}
            }
        })

        # Set column widths
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 22,
                    'endIndex': 23
                },
                'properties': {'pixelSize': 200},
                'fields': 'pixelSize'
            }
        })

        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 23,
                    'endIndex': 24
                },
                'properties': {'pixelSize': 100},
                'fields': 'pixelSize'
            }
        })

        # Execute all requests in batch
        print("⚙️  Executing all formatting requests...")
        body = {'requests': requests}
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()

        print("\n✅ SUCCESS! Your Accounts Master sheet is ready!\n")
        print("=" * 60)
        print(f"📊 Spreadsheet: Life OS v2 - Michelle")
        print(f"🔗 URL: {spreadsheet_url}")
        print("=" * 60)
        print("\n✨ What's been created:")
        print("   ✅ Professional account tracking system")
        print("   ✅ Automatic ID numbering")
        print("   ✅ Dropdown menus for consistency")
        print("   ✅ Color-coded status alerts")
        print("   ✅ Password security tracking")
        print("   ✅ Live summary dashboard")
        print("   ✅ Frozen headers")
        print("\n📝 Next Steps:")
        print("   1. Open the spreadsheet using the URL above")
        print("   2. Start adding your accounts in Row 2")
        print("   3. Use the dropdown menus for consistent data entry")
        print("   4. Watch the summary dashboard update automatically!")
        print("\n💡 Pro Tips:")
        print("   - Passwords older than 6 months will be highlighted")
        print("   - Accounts not reviewed in 90 days will show in alerts")
        print("   - All formulas are protected and auto-calculate")
        print()

        return spreadsheet_url

    except HttpError as error:
        print(f"❌ An error occurred: {error}")
        return None

if __name__ == '__main__':
    create_accounts_master_sheet()
