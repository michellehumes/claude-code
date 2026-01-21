# Gmail Organization System

Automated Gmail organization with priority-based labels and smart filters to keep your inbox focused on what matters.

## 📋 System Overview

This system automatically organizes your emails into 7 categories, designed to:
- **Keep priority emails visible** in your inbox
- **Auto-archive low-priority emails** for later review
- **Flag emails that need responses**
- **Reduce inbox clutter** while maintaining organization

## 🎯 Label Categories

### PRIORITY (Stays in Inbox)

#### 🔴 Needs Response
**Purpose:** Emails requiring your action or reply
**Stays:** In inbox, unread
**Automatically catches:**
- Emails with subjects containing "please respond", "need your input", "waiting for", "action required", "RSVP"
- Emails you sent to yourself (reminders)
- Emails with attachments asking you to "review", "approve", or "sign"
- Excludes automated no-reply emails

**Why it matters:** These emails need your immediate attention. They stay unread and visible until you handle them.

#### ⭐ High Priority
**Purpose:** Important people and organizations
**Stays:** In inbox, unread
**Customize with:** Your important contacts and domains

**How to customize:**
```python
criteria_priority = {
    'from': 'your-boss@company.com OR important-client.com OR partner-name@company.com'
}
```

**Why it matters:** Never miss emails from VIPs. Customize this with your most important contacts.

#### 💼 Work/Business
**Purpose:** Professional emails and work-related messages
**Stays:** In inbox, unread
**Automatically catches:**
- Emails about meetings, projects, deadlines, proposals, contracts, invoices
- Emails with PDF, DOC, DOCX, or XLSX attachments
- Excludes marketing and automated notifications

**Why it matters:** Keeps work emails front and center, separate from personal communications.

---

### AUTO-ARCHIVED (Organized but out of inbox)

#### 💰 Finance
**Purpose:** Banking, credit cards, investments, payment services
**Status:** Auto-archived, kept unread
**Includes:** Chase, American Express, PNC, Fidelity, PayPal, Venmo, Stripe, and more

**Why it matters:** Financial emails are important but don't need immediate attention. They're archived but kept unread so you can review statements monthly.

#### 📦 Orders & Receipts
**Purpose:** Shopping confirmations, delivery notifications, receipts
**Status:** Auto-archived, marked as read
**Includes:** Amazon, Uber, Etsy, Shopify, Target, Walmart, FedEx, UPS, and more

**Why it matters:** You ordered it, you know it's coming. Archive for search when needed, but no need to clutter your inbox.

#### 📧 Newsletters
**Purpose:** Marketing emails, subscriptions, updates
**Status:** Auto-archived, marked as read
**Automatically catches:**
- Emails with unsubscribe links
- Mailing list messages
- Newsletters and digest emails

**Why it matters:** Read newsletters when you have time, not when they arrive. Keep inbox for actionable items.

#### 🔔 Social
**Purpose:** Social media notifications and community updates
**Status:** Auto-archived, marked as read
**Includes:** Facebook, Twitter, LinkedIn, Instagram, Reddit, Slack, Discord, Medium, and more

**Why it matters:** Social notifications are nice to know but rarely urgent. Check them on your own schedule.

## 🚀 How to Use

### Initial Setup

1. **Install dependencies:**
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

2. **Set up Google Cloud credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Gmail API
   - Download OAuth credentials as `credentials.json`
   - Place in the same directory as the script

3. **Run the script:**
   ```bash
   python gmail_labels_filters.py
   ```

4. **First-time authentication:**
   - Browser window will open
   - Sign in to your Google account
   - Grant Gmail permissions
   - Token will be saved for future use

### Automated Daily Runs

The system runs automatically daily at 6:00 AM UTC via GitHub Actions. New emails are automatically categorized as they arrive.

### Manual Runs

To manually trigger the organization:
```bash
python gmail_labels_filters.py
```

Or via GitHub Actions:
- Go to Actions tab → "Gmail Labels and Filters" → "Run workflow"

## 🎨 Customization Guide

### Adding Important Contacts (High Priority)

Edit line 108 in `gmail_labels_filters.py`:
```python
criteria_priority = {
    'from': 'boss@company.com OR client@important.com OR partner@business.com'
}
```

### Adding More Shopping Sites (Orders)

Edit line 145 in `gmail_labels_filters.py`:
```python
criteria_orders = {
    'from': 'amazon.com OR uber.com OR YOUR-STORE.com'
}
```

### Adding Financial Institutions

Edit line 135 in `gmail_labels_filters.py`:
```python
criteria_finance = {
    'from': 'chase.com OR YOUR-BANK.com OR YOUR-CREDIT-CARD.com'
}
```

### Creating Custom Labels

Add a new section in the `main()` function:
```python
# CUSTOM LABEL - Travel confirmations
print("[8/7] Creating 'Travel' label...")
travel_label = create_label(service, user_id, '✈️ Travel')
if travel_label:
    criteria_travel = {
        'from': 'airlines.com OR hotels.com OR airbnb.com OR booking.com'
    }
    create_filter(service, user_id, criteria_travel, travel_label,
                 skip_inbox=False, mark_read=False)
```

## 📊 Expected Results

### Your Inbox Will Contain:
- 🔴 **Needs Response** - Action items waiting for you
- ⭐ **High Priority** - Important people you configured
- 💼 **Work/Business** - Professional emails

### Everything Else Auto-Organized:
- 💰 **Finance** - Check monthly for statements
- 📦 **Orders & Receipts** - Search when needed
- 📧 **Newsletters** - Read when you have time
- 🔔 **Social** - Check at your convenience

### Inbox Zero Made Easy:
Your inbox now only shows emails that truly need attention. Everything else is organized and searchable but out of sight.

## 🔧 Troubleshooting

### Labels Already Exist
If you run the script multiple times, Gmail will prevent duplicate label creation. This is normal and safe.

### Filters Not Working
- Check that credentials are valid (`token.pickle` is current)
- Verify Gmail API is enabled in Google Cloud Console
- Test Gmail search queries manually in Gmail search bar

### Customization Not Working
- Ensure you save changes to `gmail_labels_filters.py`
- Re-run the script after making changes
- New filters only apply to future emails (not retroactive)

### Want to Apply to Existing Emails
Gmail filters only work on new emails. To organize existing emails:
1. Use Gmail search with the same criteria
2. Manually apply labels to search results
3. Archive if desired

Example search: `from:(amazon.com OR uber.com)`

## 🎯 Best Practices

1. **Review "Needs Response" daily** - These are action items
2. **Customize High Priority** - Add your VIP contacts
3. **Check Finance monthly** - Review statements and transactions
4. **Clean Newsletters quarterly** - Unsubscribe from unwanted lists
5. **Trust the system** - Let automation handle the organization

## 💡 Pro Tips

- **Search is powerful:** All emails are searchable even when archived
- **Starred emails:** Use Gmail stars for extra-important flagging
- **Snooze feature:** Use Gmail snooze for emails you'll need later
- **Mobile labels:** Labels sync to Gmail mobile app automatically
- **Notification settings:** Configure mobile notifications for "Needs Response" only

## 📅 Maintenance

- **Monthly:** Review Finance label for statements
- **Quarterly:** Audit and customize filter rules
- **Annually:** Remove unused labels, update important contacts

---

**Created:** 2026-01-21
**Automation:** GitHub Actions (Daily at 6:00 AM UTC)
**Script:** `gmail_labels_filters.py`
