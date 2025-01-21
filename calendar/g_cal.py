import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
from urllib.request import Request
from utils.login_polimi import good_cookies


class GoogleCalendarManager:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.service = self.authenticate_google_calendar()
        self.data = good_cookies()
        self.req_1 = {"request-id": "|cba7485f659244828ccfb13fc36ca868.ae50475c32494a1b"}
        self.req_2 = {"request-id": "|cba7485f659244828ccfb13fc36ca868.7e2c1f517db94517"}
        self.headers = {"cookie": self.data[0]}
        self.pid = self.data[1]

    def authenticate_google_calendar(self):
        creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def add_event(self, title, start, end, location, room, prof_name, prof_sur, teams, checkin):
        if room is None:
            room = ''
        event = {
            'summary': f"{title}",
            'location': f"{location} {room}",
            'description': f"Professor:\n{prof_name} {prof_sur}\n\nCheck-in:\n{checkin}\n\nTeams:\n{teams}",
            'start': {
                'dateTime': start,
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': end,
                'timeZone': 'Europe/Rome',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f"[ EVENT CREATED! ] [ {event.get('htmlLink')} ]")

    @staticmethod
    def current_date(date):
        today = datetime.now().strftime('%Y-%m-%d')
        if today < date:
            return True
        else:
            return False

    def fetch_and_add_events(self):
        self.headers.update(self.req_1)
        r = requests.get(f"https://www.gsom.polimi.it/api/programs/courses/?programId={self.pid}", headers=self.headers)
        data = r.json().get('data', [])

        for course in data:
            try:
                self.headers.update(self.req_2)
                r = requests.get(
                    f"https://www.gsom.polimi.it/api/programs/lessons/?id={course['id']}&programId={self.pid}",
                    headers=self.headers)
                data_course = r.json().get('data', [])

                for lesson in data_course:
                    try:
                        start_date = lesson.get('startDate')
                        date = start_date.split('T')[0]
                        if not self.current_date(date):
                            continue
                    except Exception as e:
                        continue
                    end_date = lesson.get('endDate')
                    name = lesson.get('name', {}).get('en')
                    location = lesson.get('building', {}).get('name')
                    room = lesson.get('room', {}).get('name')
                    prof_name = lesson.get('professors', [{}])[0].get('firstName')
                    prof_surname = lesson.get('professors', [{}])[0].get('lastName')
                    teams_url = lesson.get('sessionUrl', '')
                    check_in = lesson.get('checkinUrl', '')

                    if start_date:
                        self.add_event(
                            name, start_date, end_date, location, room,
                            prof_name, prof_surname, teams_url, check_in
                        )
            except Exception as e:
                continue

    def main(self):
        self.fetch_and_add_events()


bot = GoogleCalendarManager()
bot.main()
