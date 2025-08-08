# app/utils/decorators.py - Custom decorators
from functools import wraps
from flask import request, jsonify
import jwt
from app.models import Admin

def token_required(f):
    """Decorator for protecting admin routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_admin = Admin.query.get(data['admin_id'])
            if not current_admin or not current_admin.is_active:
                return jsonify({'message': 'Token is invalid'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_admin, *args, **kwargs)
    return decorated

def track_visit():
    """Track site visits for analytics"""
    try:
        visit = SiteVisit(
            ip_address=request.remote_addr,
            page=request.endpoint,
            user_agent=request.headers.get('User-Agent', ''),
            referer=request.headers.get('Referer', ''),
            session_id=request.headers.get('X-Session-ID', str(uuid.uuid4()))
        )
        db.session.add(visit)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error tracking visit: {e}")
        db.session.rollback()

def create_google_calendar_event(booking):
    """Create Google Calendar event for booking"""
    try:
        # Load credentials (you'll need to set this up)
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # This would be handled during initial setup
                logger.warning("Google Calendar credentials not available")
                return None
        
        service = build('calendar', 'v3', credentials=creds)
        
        # Create event
        event_start = datetime.combine(booking.preferred_date, datetime.min.time())
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
        
        created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return created_event.get('id')
        
    except Exception as e:
        logger.error(f"Error creating Google Calendar event: {e}")
        return None
