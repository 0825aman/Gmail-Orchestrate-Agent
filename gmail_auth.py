"""
gmail_auth.py
-------------
Handles Gmail OAuth2 Authorization Code flow.

Client ID : 531441136148-f4q4541c93f2f7rg6lohqo843smv9ev7.apps.googleusercontent.com
Scopes    : https://www.googleapis.com/auth/gmail.modify
            https://mail.google.com/

First run:  Opens browser for Google consent screen → saves token.json
Later runs: Loads token.json and auto-refreshes if expired

Returns an authenticated Gmail API service object ready to use.
"""

import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Both scopes registered on the OAuth consent screen:
#   - gmail.modify  : read, compose, send, and modify (but not delete permanently)
#   - mail.google.com: full access including permanent delete
# Using both ensures all four agent operations are covered.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://mail.google.com/",
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_gmail_service():
    """
    Authenticate with Gmail API using OAuth2.

    - If token.json exists and is valid, uses it directly.
    - If token.json is expired, refreshes it automatically.
    - If no token.json, opens browser for user consent and saves new token.json.

    Returns:
        googleapiclient Resource: Authenticated Gmail API service (v1).
    """
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, obtain or refresh them
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Silently refresh expired token
            creds.refresh(Request())
        else:
            # Launch browser-based OAuth2 consent flow using your credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            # port=0 lets the OS pick a free redirect port automatically
            creds = flow.run_local_server(port=0)

        # Persist the token so subsequent runs skip the browser step
        with open(TOKEN_FILE, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)
