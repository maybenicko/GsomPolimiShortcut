from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
import os


class GoogleCalendarManager:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.service = self.authenticate_google_calendar()

    def authenticate_google_calendar(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        token_path = os.path.join(current_folder, "token.json")
        creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                cred_path = os.path.join(current_folder, "credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(cred_path, self.SCOPES)
                creds = flow.run_local_server(port=0)

        return build('calendar', 'v3', credentials=creds)

    def get_all_events(self):
        events = []
        page_token = None
        while True:
            events_result = self.service.events().list(
                calendarId='primary', pageToken=page_token).execute()
            events.extend(events_result.get('items', []))
            page_token = events_result.get('nextPageToken')
            if not page_token:
                break
        return events

    def remove_duplicates(self):
        events = self.get_all_events()
        unique_events = {}

        for event in events:
            title = event.get('summary')
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            location = event.get('location')
            event_key = (title, start_time, location)

            if event_key in unique_events:
                print(f"Duplicate found: {event['summary']} at {start_time} - Removing...")
                self.service.events().delete(calendarId='primary', eventId=event['id']).execute()
            else:
                unique_events[event_key] = event

        print("Duplicates removed.")


bot = GoogleCalendarManager()
bot.remove_duplicates()
