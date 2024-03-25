import os
from google_auth_oauthlib. flow import InstalledAppFlow #Module for handling OAuth 2.0 authentication flow
from googleapiclient.discovery import build # Module for building API service objects
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

import requests # Module for handling Google API HTTP errors
# Define the access scope for the Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]
# Function to get Google Calendar API credentials
def get_credentials():
    creds = None # Initialize credentials as None
    # Check if the file 'CREDENTIALS\token.json' exists
    if os.path.exists(r"CREDENTIALS/token.json"):
        # Load credentials from the file if it exists
        creds = Credentials.from_authorized_user_file(r"CREDENTIALS/token.json")
    # Check if credentials do not exist or are invalid
    if not creds or not creds.valid:
    # Check if credentials exist, are expired, and can be refreshed
        if creds and creds.expired and creds.refresh_token:
        # Refresh expired credentials
            creds.refresh(Request())
        else:
            # Create a flow for handling OAuth 2.0 authentication
            flow = InstalledAppFlow.from_client_secrets_file(r"CREDENTIALS/credentials.json", SCOPES)
            # Run the OAuth 2.0 authentication flow locally
            creds = flow.run_local_server (port=0)
        # Save the refreshed or newly obtained credentials to 'CREDENTIALS\token.json'
        with open(r"CREDENTIALS/token.json", "w") as token:
            token.write(creds.to_json())
        # Return the obtained credentials
    return creds

def create_event (service,patient_email,org_email,therapist_name,date_time):
    try:
        # Define the details of the event
        event=event = {
    "summary": "Mental Health Presentation",
    "location": "Somewhere online",
    "description": f"Appointment with {therapist_name}",
    "colorId": 6,
    'start': {
        'dateTime': date_time,  # Adjusted time for EST
        'timeZone': 'America/New_York'  # Changed to Eastern Time zone
    },
    'end': {
        'dateTime': date_time+timedelta(hours=1),  # Adjusted time for EST
        'timeZone': 'America/New_York'  # Changed to Eastern Time zone
    },
    "recurrence": [
        "RRULE:FREQ=DAILY;COUNT=3"
    ],
    'attendees': [
        {'email': patient_email},
        {'email': org_email}
    ]
}
        # Insert the event into the Google Calendar and execute the request
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        # Print the link to view the created event
        print (f"Event created: {created_event.get('htmlLink')}")
    # Handle HTTP errors
    except HttpError as error:
        print (f"An error occurred: {error}")
# Main function
        """
def main():
    #Get Google Calendar API credentials
    creds = get_credentials()
    # Build the Google Calendar API service
    service = build("calendar", "v3", credentials=creds)
    # Create a Google Calendar event
    create_event (service,patient_email,org_email,therapist_name)
"""