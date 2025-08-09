# app/services/calendar_service.py - Google Calendar integration
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

class CalendarService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID', 'primary')
        self.credentials = None
    
    def _get_credentials(self):
        """Get Google Calendar credentials"""
        creds = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Error refreshing credentials: {e}")
                    return None
            else:
                if os.path.exists('credentials.json'):
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', self.SCOPES)
                        creds = flow.run_local_server(port=0)
                    except Exception as e:
                        logger.error(f"Error getting new credentials: {e}")
                        return None
                else:
                    logger.warning("credentials.json not found")
                    return None
            
            # Save the credentials for the next run
            if creds:
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
        
        return creds
    
    def create_event(self, booking):
        """Create Google Calendar event for booking"""
        try:
            creds = self._get_credentials()
            if not creds:
                logger.warning("No valid credentials for Google Calendar")
                return None
            
            service = build('calendar', 'v3', credentials=creds)
            
            # Create event details
            event_start = datetime.combine(booking.preferred_date, datetime.min.time().replace(hour=8))
            event_end = event_start + timedelta(hours=8)  # Default 8-hour tour
            
            event = {
                'summary': f'Tour Booking - {booking.name} ({booking.destination})',
                'description': f"""
                Booking Reference: {booking.booking_reference}
                Client: {booking.name}
                Email: {booking.email}
                Phone: {booking.phone}
                Destination: {booking.destination}
                Guests: {booking.guests}
                Message: {booking.message}
                """.strip(),
                'start': {
                    'dateTime': event_start.isoformat(),
                    'timeZone': 'Africa/Nairobi',
                },
                'end': {
                    'dateTime': event_end.isoformat(),
                    'timeZone': 'Africa/Nairobi',
                },
                'attendees': [
                    {'email': booking.email, 'displayName': booking.name}
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 60},
                    ],
                },
            }
            
            created_event = service.events().insert(calendarId=self.CALENDAR_ID, body=event).execute()
            logger.info(f"Created calendar event: {created_event.get('id')}")
            return created_event.get('id')
            
        except Exception as e:
            logger.error(f"Error creating Google Calendar event: {e}")
            return None
    
    def update_event(self, event_id, booking):
        """Update existing calendar event"""
        try:
            creds = self._get_credentials()
            if not creds:
                return None
            
            service = build('calendar', 'v3', credentials=creds)
            
            # Get existing event
            event = service.events().get(calendarId=self.CALENDAR_ID, eventId=event_id).execute()
            
            # Update event details
            event['summary'] = f'Tour Booking - {booking.name} ({booking.destination})'
            event['description'] = f"""
            Booking Reference: {booking.booking_reference}
            Client: {booking.name}
            Email: {booking.email}
            Phone: {booking.phone}
            Destination: {booking.destination}
            Guests: {booking.guests}
            Status: {booking.status}
            Message: {booking.message}
            """.strip()
            
            updated_event = service.events().update(
                calendarId=self.CALENDAR_ID, 
                eventId=event_id, 
                body=event
            ).execute()
            
            return updated_event.get('id')
            
        except Exception as e:
            logger.error(f"Error updating Google Calendar event: {e}")
            return None
    
    def delete_event(self, event_id):
        """Delete calendar event"""
        try:
            creds = self._get_credentials()
            if not creds:
                return False
            
            service = build('calendar', 'v3', credentials=creds)
            service.events().delete(calendarId=self.CALENDAR_ID, eventId=event_id).execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting Google Calendar event: {e}")
            return False
            