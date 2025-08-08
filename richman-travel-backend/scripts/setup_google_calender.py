# scripts/setup_google_calendar.py - Google Calendar OAuth setup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def setup_google_calendar_auth():
    """Run this once to get the token.json file"""
    # Google Calendar setup logic from earlier
    pass

if __name__ == '__main__':
    setup_google_calendar_auth()