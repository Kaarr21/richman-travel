# app/routes/public.py - Fixed booking route
from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.models import Destination, Booking, ContactMessage, SiteVisit
from app.utils.validators import validate_booking_data, validate_contact_data, sanitize_input
from app.utils.helpers import send_booking_confirmation_email, send_admin_booking_notification
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

public_bp = Blueprint('public', __name__)

@public_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@public_bp.route('/destinations', methods=['GET'])
@limiter.limit("30 per minute")
def get_destinations():
    """Get all active destinations"""
    try:
        featured_only = request.args.get('featured', 'false').lower() == 'true'
        
        query = Destination.query.filter_by(is_active=True)
        if featured_only:
            query = query.filter_by(is_featured=True)
        
        destinations = query.order_by(Destination.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'data': [dest.to_dict() for dest in destinations],
            'count': len(destinations)
        })
    except Exception as e:
        logger.error(f"Error fetching destinations: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@public_bp.route('/destinations/<slug>', methods=['GET'])
@limiter.limit("30 per minute")
def get_destination_by_slug(slug):
    """Get destination by slug and increment view count"""
    try:
        destination = Destination.query.filter_by(slug=slug, is_active=True).first()
        if not destination:
            return jsonify({'success': False, 'message': 'Destination not found'}), 404
        
        # Increment view count
        destination.view_count += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': destination.to_dict()
        })
    except Exception as e:
        logger.error(f"Error fetching destination: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@public_bp.route('/bookings', methods=['POST'])
@limiter.limit("5 per hour")
def create_booking():
    """Create new booking with improved validation"""
    try:
        # Get and validate JSON data
        if not request.is_json:
            return jsonify({
                'success': False, 
                'message': 'Request must be JSON',
                'errors': ['Content-Type must be application/json']
            }), 400
            
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False, 
                'message': 'No data provided',
                'errors': ['Request body is empty']
            }), 400

        # Log received data for debugging
        logger.info(f"Received booking data: {data}")
        
        # Sanitize inputs
        sanitized_data = {}
        for field in ['name', 'email', 'phone', 'destination', 'message']:
            if field in data and data[field] is not None:
                sanitized_data[field] = sanitize_input(str(data[field]))
            else:
                sanitized_data[field] = data.get(field, '')
        
        # Copy other fields as-is
        for field in ['date', 'guests']:
            sanitized_data[field] = data.get(field)
        
        # Validate data
        validation_errors = validate_booking_data(sanitized_data)
        if validation_errors:
            logger.warning(f"Validation failed for booking: {validation_errors}")
            return jsonify({
                'success': False, 
                'message': 'Validation failed',
                'errors': validation_errors
            }), 400
        
        # Parse date if provided
        booking_date = None
        if sanitized_data.get('date'):
            try:
                booking_date = datetime.strptime(sanitized_data['date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Invalid date format',
                    'errors': ['Date must be in YYYY-MM-DD format']
                }), 400
        
        # Parse guests
        try:
            guests_count = int(sanitized_data.get('guests', 1))
        except (ValueError, TypeError):
            guests_count = 1
        
        # Create booking
        booking = Booking(
            name=sanitized_data['name'],
            email=sanitized_data['email'],
            phone=sanitized_data.get('phone', ''),
            destination=sanitized_data.get('destination', ''),
            preferred_date=booking_date,
            guests=guests_count,
            message=sanitized_data.get('message', ''),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:255]  # Limit length
        )
        
        booking.booking_reference = booking.generate_reference()
        
        db.session.add(booking)
        db.session.commit()
        
        logger.info(f"Created booking: {booking.booking_reference}")
        
        # Send notifications (non-blocking)
        try:
            send_booking_confirmation_email(booking)
            send_admin_booking_notification(booking)
        except Exception as e:
            logger.warning(f"Failed to send email notifications: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Booking request submitted successfully! We will contact you within 24 hours.',
            'data': {
                'booking_reference': booking.booking_reference,
                'status': booking.status,
                'name': booking.name,
                'email': booking.email
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': 'Internal server error. Please try again later.'
        }), 500

@public_bp.route('/contact', methods=['POST'])
@limiter.limit("3 per hour")
def contact_message():
    """Handle contact form submissions with validation"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False, 
                'message': 'Request must be JSON'
            }), 400
            
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False, 
                'message': 'No data provided'
            }), 400
        
        # Sanitize inputs
        sanitized_data = {}
        for field in ['name', 'email', 'subject', 'message']:
            if field in data and data[field] is not None:
                sanitized_data[field] = sanitize_input(str(data[field]))
            else:
                sanitized_data[field] = data.get(field, '')
        
        # Validate data
        validation_errors = validate_contact_data(sanitized_data)
        if validation_errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': validation_errors
            }), 400
        
        message = ContactMessage(
            name=sanitized_data['name'],
            email=sanitized_data['email'],
            subject=sanitized_data.get('subject', ''),
            message=sanitized_data['message'],
            ip_address=request.remote_addr
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully! We will get back to you soon.'
        }), 201
        
    except Exception as e:
        logger.error(f"Error saving contact message: {e}")
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': 'Internal server error. Please try again later.'
        }), 500
        