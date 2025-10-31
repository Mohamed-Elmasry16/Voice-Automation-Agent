from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import datetime, os

# ----------------------------------
# Google Calendar API setup
# ----------------------------------
SCOPES = ['https://www.googleapis.com/auth/calendar']


# ----------------------------------
# Get or create user credentials
# ----------------------------------
def get_credentials():
    """Get or create OAuth2 credentials for accessing Google Calendar."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


# ----------------------------------
# Fetch upcoming calendar events
# ----------------------------------
def get_upcoming_events(limit=100, days_ahead=30):
    """
    Fetch upcoming events from the user's primary calendar.
    Returns a plain text summary suitable for text-to-speech output.
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=days_ahead)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=time_max,
        maxResults=limit,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        return "You have no upcoming events."

    message = "Here are your upcoming events: "
    for e in events:
        summary = e.get('summary', 'Untitled event')
        start = e['start'].get('dateTime', e['start'].get('date'))
        try:
            dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
            message += f"{summary} on {dt.strftime('%A, %B %d at %H:%M')}. "
        except Exception:
            message += f"{summary} on {start}. "
    
    return message


# ----------------------------------
# Add a new calendar event
# ----------------------------------
def add_event(summary, start_time, end_time, timezone='Africa/Cairo'):
    """
    Add a new event to the user's primary calendar.
    Returns a success message string.
    """
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': timezone},
        'end': {'dateTime': end_time, 'timeZone': timezone},
    }
    
    new_event = service.events().insert(calendarId='primary', body=event).execute()
    return f"Event created successfully: {new_event.get('summary')}"


# ----------------------------------
# Delete event
# ----------------------------------
def delete_event(summary):
    """Delete the first event that matches the summary."""
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    events_result = service.events().list(
        calendarId="primary",
        q=summary
    ).execute()

    events = events_result.get("items", [])
    if not events:
        return f"No event found with title {summary}"

    event_id = events[0]["id"]
    service.events().delete(calendarId="primary", eventId=event_id).execute()
    return f"Deleted event {summary}"
