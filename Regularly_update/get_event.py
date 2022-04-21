from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_event_from_calendarIDs(calendar_ids):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API

    dt = datetime.datetime.now()

    # timefrom = '2022/3/10'
    # timeto = '2022/3/11'
     
    timefrom_datetime = dt - datetime.timedelta(hours=9)
    timeto_datetime = timefrom_datetime + datetime.timedelta(days=1)

    timefrom = timefrom_datetime.isoformat()+'Z'
    timeto = timeto_datetime.isoformat()+'Z'

    today_events_from_calendarids = []

    for calendar_id in calendar_ids:
        if calendar_id is not None :
            events_result = service.events().list(calendarId=calendar_id,
                                                timeMin=timefrom,
                                                timeMax=timeto,
                                                singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            today_event = ""

            if not events:
                print('No upcoming events found.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                if len(start) == 25 :
                    start_time = datetime.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
                    today_event += start_time.strftime('%H:%M') + "～ " + event['summary'] + "　"
                elif len(start) == 10 :
                    today_event += event['summary'] + "　"
                else :
                    print("Datetime format error.")

            print(today_event)
            today_events_from_calendarids.append(today_event)
        else :
            today_events_from_calendarids.append("")
            
    print(today_events_from_calendarids)
    return today_events_from_calendarids

if __name__ == '__main__':
    get_event_from_calendarID()