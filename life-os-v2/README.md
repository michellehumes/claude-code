# Life OS v2 - Accounts Master 💰

An automated Google Sheets creator for comprehensive financial account tracking and management.

## What This Creates

A professional-grade Google Sheet with:

- **💰 Accounts Master Tab**: Track all your financial accounts in one place
  - Checking, savings, credit cards, loans, investments, crypto, and more
  - 21 comprehensive fields for each account
  - Automatic ID numbering and date tracking
  - Smart dropdown menus for data consistency

- **🎨 Color-Coded Alerts**: Visual warnings for:
  - Password age (6mo/1yr/2yr thresholds)
  - Account status (active/closed/frozen/past due)
  - Accounts needing review

- **📊 Live Dashboard**: Real-time summary showing:
  - Total and active account counts
  - Breakdown by account type
  - Security alerts (old passwords, missing 2FA)
  - Review reminders

- **🔒 Security Tracking**:
  - Password last updated dates
  - 2FA method tracking
  - Automatic aging alerts

## Quick Start

1. **Install dependencies**:
   ```bash
   cd life-os-v2
   pip3 install -r requirements.txt
   ```

2. **Set up Google API credentials** (see [SETUP.md](SETUP.md) for detailed instructions)

3. **Run the script**:
   ```bash
   python3 create_accounts_master.py
   ```

4. **Open your new spreadsheet** and start adding accounts!

## Features

✅ **Professional account tracking system**
✅ **Automatic ID numbering**
✅ **Dropdown menus for consistency**
✅ **Color-coded status alerts**
✅ **Password security tracking**
✅ **Live summary dashboard**
✅ **Frozen headers for easy scrolling**
✅ **Protected formulas**
✅ **Automatic date tracking**

## Account Types Supported

- Checking & Savings (Primary, Secondary, Emergency Fund, Goal-Based, High-Yield, Money Market)
- Credit Cards (Personal, Business)
- Loans (Mortgage, Auto, Personal, Student, Line of Credit)
- Investments (401k, IRA, Brokerage, HSA, FSA, 529 College Savings)
- Alternative (Crypto, PayPal, Venmo)

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide with Google API configuration
- **[create_accounts_master.py](create_accounts_master.py)** - Main script with inline documentation

## Security

This script:
- Only requests access to create/edit Google Sheets
- Stores credentials locally (never transmitted except to Google)
- Uses OAuth 2.0 for secure authentication
- Runs entirely on your local machine

**Important**: Never commit `credentials.json` or `token.pickle` to version control!

## What Gets Tracked

Each account includes:

1. Basic Info: ID, Type, Institution, Name, Account Number
2. Status: Active/Inactive/Closed tracking
3. Holders: Primary and joint account holders
4. Financial: Current balance, available credit, interest rate, fees
5. Dates: Opening date, maturity date
6. Automation: Auto-pay linking
7. Security: Login username, password update date, 2FA method
8. Support: Customer service number, notes
9. Management: Last reviewed date (auto-updates)

## Next Steps After Creation

1. Open your new spreadsheet
2. Fill in Row 2 with your first account (use the dropdowns!)
3. Continue adding all your accounts
4. Review the summary dashboard
5. Set reminders to update passwords for accounts with yellow/orange/red alerts
6. Review accounts monthly (those not reviewed in 90+ days show in alerts)

## License

MIT License - Feel free to use and modify for your personal financial management!

## Support

See [SETUP.md](SETUP.md) for troubleshooting and detailed setup instructions.

---

Built with ❤️ for better financial organization
