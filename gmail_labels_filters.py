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

    # Example: create "Orders & Receipts" label and filter
    label_name = 'Orders & Receipts'
    label_id = create_label(service, user_id, label_name)
    if label_id:
        criteria = {
            'from': 'amazon.com OR uber.com OR nuuly.com OR alibaba.com OR tjmaxx.com OR madisonreed.com'
        }
        create_filter(service, user_id, criteria, label_id)

    # Repeat the above block for other labels and filters
    # For example, to create a Finance filter:
    # finance_label = create_label(service, user_id, 'Finance')
    # if finance_label:
    #     criteria_finance = {
    #         'from': 'chase.com OR americanexpress.com OR pnc.com OR fidelity.com OR empower.com OR monarchmoney.com'
    #     }
    #     create_filter(service, user_id, criteria_finance, finance_label)

if __name__ == '__main__':
    main()
