#!/usr/bin/env python3
"""
Interactive setup guide for Life OS v2 Google Sheets
Helps users through the credential setup process
"""

import os
import sys
import webbrowser

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(step_num, text):
    """Print a formatted step"""
    print(f"\n{'🔹' * 30}")
    print(f"STEP {step_num}: {text}")
    print(f"{'🔹' * 30}\n")

def wait_for_user():
    """Wait for user to press Enter"""
    input("\n✅ Press ENTER when you've completed this step...")

def check_credentials():
    """Check if credentials.json exists"""
    return os.path.exists('credentials.json')

def main():
    print_header("🚀 Life OS v2 - Google Sheets Setup Guide")

    print("This guide will help you set up Google API credentials")
    print("so you can create your Accounts Master spreadsheet.")
    print("\nThe process takes about 5-10 minutes for first-time setup.")

    # Check if credentials already exist
    if check_credentials():
        print("\n✅ Great! credentials.json already exists!")
        print("\nYou're ready to create your spreadsheet.")
        print("\nRun this command:")
        print("    python3 create_accounts_master.py")
        return

    print("\n❌ credentials.json not found - let's set it up!\n")

    # Step 1: Create Google Cloud Project
    print_step(1, "Create Google Cloud Project")
    print("1. We'll open Google Cloud Console in your browser")
    print("2. Click 'Select a project' dropdown at the top")
    print("3. Click 'NEW PROJECT'")
    print("4. Name it: 'Life OS v2' (or any name you prefer)")
    print("5. Click 'CREATE'")
    print("6. Wait for project creation (~30 seconds)")
    print("7. Select your new project from the dropdown")

    open_browser = input("\n🌐 Open Google Cloud Console? (y/n): ").lower()
    if open_browser == 'y':
        webbrowser.open('https://console.cloud.google.com/')

    wait_for_user()

    # Step 2: Enable Google Sheets API
    print_step(2, "Enable Google Sheets API")
    print("1. Make sure your project is selected (check top of page)")
    print("2. We'll open the API Library")
    print("3. In the search box, type: 'Google Sheets API'")
    print("4. Click on 'Google Sheets API' from results")
    print("5. Click the blue 'ENABLE' button")
    print("6. Wait for it to enable (~10 seconds)")

    open_api = input("\n🌐 Open API Library? (y/n): ").lower()
    if open_api == 'y':
        webbrowser.open('https://console.cloud.google.com/apis/library')

    wait_for_user()

    # Step 3: Configure OAuth Consent Screen
    print_step(3, "Configure OAuth Consent Screen")
    print("1. We'll open the Credentials page")
    print("2. You may see a message about configuring consent screen")
    print("3. If prompted, click 'CONFIGURE CONSENT SCREEN'")
    print("4. Select 'External' user type")
    print("5. Click 'CREATE'")
    print("\nFill in required fields:")
    print("   - App name: Life OS v2")
    print("   - User support email: (your email)")
    print("   - Developer contact: (your email)")
    print("\n6. Click 'SAVE AND CONTINUE'")
    print("7. On Scopes page: Click 'SAVE AND CONTINUE' (skip adding scopes)")
    print("8. On Test users page:")
    print("   - Click '+ ADD USERS'")
    print("   - Enter your email address")
    print("   - Click 'ADD'")
    print("9. Click 'SAVE AND CONTINUE'")
    print("10. Review summary and click 'BACK TO DASHBOARD'")

    open_creds = input("\n🌐 Open Credentials page? (y/n): ").lower()
    if open_creds == 'y':
        webbrowser.open('https://console.cloud.google.com/apis/credentials')

    wait_for_user()

    # Step 4: Create OAuth Credentials
    print_step(4, "Create OAuth 2.0 Credentials")
    print("1. On the Credentials page, click '+ CREATE CREDENTIALS' at top")
    print("2. Select 'OAuth client ID'")
    print("3. For Application type, select: 'Desktop app'")
    print("4. Name: 'Life OS Desktop Client' (or any name)")
    print("5. Click 'CREATE'")
    print("6. You'll see a popup with Client ID and Secret - click 'OK'")

    wait_for_user()

    # Step 5: Download Credentials
    print_step(5, "Download Credentials File")
    print("1. You should now see your OAuth 2.0 Client ID in the list")
    print("2. On the right side of your client, click the Download icon (⬇️)")
    print("3. This downloads a JSON file with a long name")
    print("4. Find the downloaded file (usually in ~/Downloads/)")
    print("5. Rename it to: credentials.json")
    print("6. Move it to THIS directory:")
    print(f"   {os.getcwd()}")
    print("\n💡 You can drag and drop it here or use:")
    print(f"   mv ~/Downloads/client_secret_*.json {os.getcwd()}/credentials.json")

    wait_for_user()

    # Step 6: Verify
    print_step(6, "Verify Setup")

    if check_credentials():
        print("✅ SUCCESS! credentials.json found!")
        print("\n🎉 You're all set! Now run:")
        print("    python3 create_accounts_master.py")
        print("\nThis will:")
        print("  1. Open your browser for one-time authorization")
        print("  2. Create your Accounts Master spreadsheet")
        print("  3. Give you the URL to access it")
    else:
        print("❌ credentials.json not found yet")
        print("\nMake sure you:")
        print("  1. Downloaded the credentials file")
        print("  2. Renamed it to 'credentials.json'")
        print("  3. Moved it to this directory:")
        print(f"     {os.getcwd()}")
        print("\nThen run this setup guide again:")
        print("    python3 setup_guide.py")

    print("\n" + "=" * 70)
    print("\n📚 For detailed instructions with more context, see SETUP.md\n")

if __name__ == '__main__':
    main()
