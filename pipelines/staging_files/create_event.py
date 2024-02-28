import os
from google_auth_oauthlib. flow import InstalledAppFlow #Module for handling OAuth 2.0 authentication flow
from googleapiclient.discovery import build # Module for building API service objects
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request



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
            creds.refresh(Request())  # Corrected this line
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

def create_event (service):
    try:
        # Define the details of the event
        event = {"summary": "My Python Event", "location": "Somewhere online", "description": "This is a description", "colorId": 6, 'start': {'dateTime':
        '2023-11-20T09:00:00+05:30', 'timeZone': 'Asia/Kolkata'}, 'end': {'dateTime': '2023-11-20T17:00:00+05:30', 'timeZone': 'Asia/Kolkata'},
        "recurrence": ["RRULE:FREQ=DAILY"], 'attendees': [{'email': 'lpage@example.com'}, {'email': 'sbrin@example.com'}]}
        # Insert the event into the Google Calendar and execute the request
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        # Print the link to view the created event
        print (f"Event created: {created_event.get('htmlLink')}")
    # Handle HTTP errors
    except HttpError as error:
        print (f"An error occurred: {error}")
# Main function
def main():
    #Get Google Calendar API credentials
    creds = get_credentials()
    # Build the Google Calendar API service
    service = build("calendar", "v3", credentials=creds)
    # Create a Google Calendar event
    create_event (service)

# Execute the main function if the script is run as the main program
if __name__ ==  "__main__":
    main()