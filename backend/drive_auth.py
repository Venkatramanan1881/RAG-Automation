from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = None
    if os.path.exists('auth/token.pickle'):
        with open('auth/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no valid creds, let user login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'auth/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials
        with open('auth/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # Build the service
    service = build('drive', 'v3', credentials=creds)
    return service
