# app/services/booking_service.py - Booking business logic
from app.extensions import db
from app.models import Booking
from app.services.calendar_service import CalendarService
import logging

logger = logging.getLogger(__name__)

class BookingService:
    @staticmethod
    def create_booking(booking_data):
        """Create new booking with calendar integration"""
        try:
            # Create booking
            booking = Booking(**booking_data)
            booking.booking_reference = booking.generate_reference()
            
            db.session.add(booking)
            db.session.commit()
            
            # Add to Google Calendar
            if booking.preferred_date:
                calendar_service = CalendarService()
                event_id = calendar_service.create_event(booking)
                if event_id:
                    booking.google_event_id = event_id
                    db.session.commit()
            
            return booking
            
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def update_booking_status(booking_id, status, estimated_cost=None):
        """Update booking status and cost"""
        # Update booking logic
        pass