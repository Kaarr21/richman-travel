# app/services/booking_service.py - Booking business logic
from app.extensions import db
from app.models import Booking
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BookingService:
    @staticmethod
    def create_booking(booking_data):
        """Create new booking"""
        try:
            # Create booking
            booking = Booking(**booking_data)
            booking.booking_reference = booking.generate_reference()
            
            db.session.add(booking)
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
            db.session.commit()
            
            logger.info(f"Updated booking {booking.booking_reference} status to {status}")
            return booking
            
        except Exception as e:
            logger.error(f"Error updating booking status: {e}")
            db.session.rollback()
            raise
        