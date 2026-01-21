"""
Gmail Labels and Filters API Script

This script uses the Gmail API (via google-api-python-client) to programmatically
create labels and filters for organizing emails. It requires:
- A Google Cloud project with the Gmail API enabled
- OAuth credentials downloaded as 'credentials.json'
- User authentication via OAuth 2.0

Replace label names and criteria values with specifics for each filter you want to add.
"""

from __future__ import print_function
import os
import pickle

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Authenticate and return a Gmail API service."""
    creds = None
    # token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials, let user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def create_label(service, user_id, label_name):
    """Create a new label."""
    label_body = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    try:
        label = service.users().labels().create(userId=user_id,
                                                body=label_body).execute()
        return label['id']
    except HttpError as error:
        print(f'An error occurred creating label {label_name}: {error}')
        return None

def create_filter(service, user_id, criteria, label_id, skip_inbox=True, mark_read=True):
    """Create a Gmail filter."""
    filter_action = {}
    if skip_inbox:
        filter_action['removeLabelIds'] = ['INBOX']
    if mark_read:
        filter_action.setdefault('removeLabelIds', []).append('UNREAD')
    # Apply label
    filter_action['addLabelIds'] = [label_id]

    filter_body = {
        'criteria': criteria,
        'action': filter_action
    }
    try:
        service.users().settings().filters().create(
            userId=user_id, body=filter_body).execute()
    except HttpError as error:
        print(f'An error occurred creating filter: {error}')

def main():
    service = get_gmail_service()
    user_id = 'me'  # use "me" for authenticated user

    print("Setting up comprehensive Gmail organization system...")

    # ==========================================================================
    # PRIORITY SYSTEM - These emails stay visible and require attention
    # ==========================================================================

    # 1. NEEDS RESPONSE - Emails requiring action (stays in inbox, unread)
    print("\n[1/7] Creating 'Needs Response' label...")
    needs_response_label = create_label(service, user_id, '🔴 Needs Response')
    if needs_response_label:
        # Direct questions or requests that need replies
        criteria_response = {
            'query': '(subject:(please respond OR need your input OR waiting for OR action required OR RSVP) OR (from:me to:me) OR has:attachment subject:(review OR approve OR sign)) -from:(noreply OR no-reply OR donotreply OR notification)'
        }
        # Keep in inbox, keep unread to maintain visibility
        create_filter(service, user_id, criteria_response, needs_response_label,
                     skip_inbox=False, mark_read=False)

    # 2. HIGH PRIORITY - Important senders (stays in inbox)
    print("[2/7] Creating 'High Priority' label...")
    high_priority_label = create_label(service, user_id, '⭐ High Priority')
    if high_priority_label:
        # Important domains and people - customize these
        criteria_priority = {
            'from': 'important-client.com OR partner.com OR boss@company.com'
        }
        # Keep in inbox but mark as read so you can review later
        create_filter(service, user_id, criteria_priority, high_priority_label,
                     skip_inbox=False, mark_read=False)

    # 3. WORK/BUSINESS - Professional emails (stays in inbox for now)
    print("[3/7] Creating 'Work/Business' label...")
    work_label = create_label(service, user_id, '💼 Work/Business')
    if work_label:
        # Work-related domains and keywords
        criteria_work = {
            'query': '(subject:(meeting OR project OR deadline OR proposal OR contract OR invoice) OR has:attachment (subject:(pdf OR doc OR docx OR xlsx))) -from:(noreply OR notification OR marketing)'
        }
        # Keep in inbox for visibility
        create_filter(service, user_id, criteria_work, work_label,
                     skip_inbox=False, mark_read=False)

    # ==========================================================================
    # AUTO-ARCHIVE CATEGORIES - These are organized but removed from inbox
    # ==========================================================================

    # 4. FINANCE - Banking, investments, financial services
    print("[4/7] Creating 'Finance' label...")
    finance_label = create_label(service, user_id, '💰 Finance')
    if finance_label:
        criteria_finance = {
            'from': 'chase.com OR americanexpress.com OR pnc.com OR fidelity.com OR empower.com OR monarchmoney.com OR paypal.com OR venmo.com OR stripe.com OR square.com OR bankofamerica.com OR wellsfargo.com OR discover.com OR citi.com'
        }
        # Auto-archive but keep unread so you can review statements
        create_filter(service, user_id, criteria_finance, finance_label,
                     skip_inbox=True, mark_read=False)

    # 5. ORDERS & RECEIPTS - Shopping and delivery confirmations
    print("[5/7] Creating 'Orders & Receipts' label...")
    orders_label = create_label(service, user_id, '📦 Orders & Receipts')
    if orders_label:
        criteria_orders = {
            'from': 'amazon.com OR uber.com OR ubereats.com OR doordash.com OR grubhub.com OR nuuly.com OR alibaba.com OR tjmaxx.com OR madisonreed.com OR shopify.com OR etsy.com OR ebay.com OR target.com OR walmart.com OR fedex.com OR ups.com OR usps.com'
        }
        # Auto-archive and mark read - you can search when needed
        create_filter(service, user_id, criteria_orders, orders_label,
                     skip_inbox=True, mark_read=True)

    # 6. NEWSLETTERS - Marketing emails, updates, subscriptions
    print("[6/7] Creating 'Newsletters' label...")
    newsletter_label = create_label(service, user_id, '📧 Newsletters')
    if newsletter_label:
        criteria_newsletters = {
            'query': 'list:(-) OR unsubscribe OR (subject:(newsletter OR weekly update OR monthly digest)) -from:(chase.com OR americanexpress.com OR pnc.com)'
        }
        # Auto-archive and mark read - read when you have time
        create_filter(service, user_id, criteria_newsletters, newsletter_label,
                     skip_inbox=True, mark_read=True)

    # 7. SOCIAL NOTIFICATIONS - Social media, forums, communities
    print("[7/7] Creating 'Social Notifications' label...")
    social_label = create_label(service, user_id, '🔔 Social')
    if social_label:
        criteria_social = {
            'from': 'facebookmail.com OR twitter.com OR linkedin.com OR instagram.com OR tiktok.com OR pinterest.com OR reddit.com OR notifications@slack.com OR discord.com OR medium.com OR substack.com'
        }
        # Auto-archive and mark read - check when convenient
        create_filter(service, user_id, criteria_social, social_label,
                     skip_inbox=True, mark_read=True)

    print("\n✅ Gmail organization complete!")
    print("\n📋 SUMMARY:")
    print("   STAYS IN INBOX (requires attention):")
    print("   - 🔴 Needs Response: Action items and requests")
    print("   - ⭐ High Priority: Important senders")
    print("   - 💼 Work/Business: Professional emails")
    print("\n   AUTO-ARCHIVED (organized, searchable):")
    print("   - 💰 Finance: Banking & financial services")
    print("   - 📦 Orders & Receipts: Shopping & deliveries")
    print("   - 📧 Newsletters: Marketing & subscriptions")
    print("   - 🔔 Social: Social media notifications")
    print("\n💡 TIP: Customize the 'High Priority' filter with your important contacts!")

if __name__ == '__main__':
    main()
