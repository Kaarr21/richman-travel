# app/services/booking_service.py - Booking business logic
from app.extensions import db
from app.models import Booking
from services.calendar_service import CalendarService
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
            
            # Add to Google Calendar if date is provided
            if booking.preferred_date:
                calendar_service = CalendarService()
                event_id = calendar_service.create_event(booking)
                if event_id:
                    booking.google_event_id = event_id
                    db.session.commit()
            
            logger.info(f"Created booking: {booking.booking_reference}")
            return booking
            
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def update_booking_status(booking_id, status, estimated_cost=None):
        """Update booking status and cost"""
        try:
            booking = Booking.query.get(booking_id)
            if not booking:
                return None
            
            booking.status = status
            if estimated_cost:
                booking.estimated_cost = estimated_cost
            
            booking.updated_at = datetime.utcnow()
            
            # Update calendar event
            if booking.google_event_id:
                calendar_service = CalendarService()
                calendar_service.update_event(booking.google_event_id, booking)
            
            db.session.commit()
            logger.info(f"Updated booking {booking.booking_reference} status to {status}")
            return booking
            
        except Exception as e:
            logger.error(f"Error updating booking status: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def cancel_booking(booking_id, reason=None):
        """Cancel a booking and remove from calendar"""
        try:
            booking = Booking.query.get(booking_id)
            if not booking:
                return None
            
            booking.status = 'cancelled'
            if reason:
                booking.message += f"\n\nCancellation reason: {reason}"
            
            # Remove from calendar
            if booking.google_event_id:
                calendar_service = CalendarService()
                calendar_service.delete_event(booking.google_event_id)
                booking.google_event_id = None
            
            db.session.commit()
            logger.info(f"Cancelled booking: {booking.booking_reference}")
            return booking
            
        except Exception as e:
            logger.error(f"Error cancelling booking: {e}")
            db.session.rollback()
            raise
        