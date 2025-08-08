# app/routes/public.py - All public-facing API endpoints
from flask import Blueprint, request, jsonify
from app.extensions import db, limiter
from app.models import Destination, Booking, ContactMessage, SiteVisit
from app.services.booking_service import BookingService
from app.utils.validators import validate_booking_data

public_bp = Blueprint('public', __name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/destinations', methods=['GET'])
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

@app.route('/api/destinations/<slug>', methods=['GET'])
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

@app.route('/api/bookings', methods=['POST'])
@limiter.limit("5 per hour")
def create_booking():
    """Create new booking"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Create booking
        booking = Booking(
            booking_reference=Booking().generate_reference(),
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            destination=data.get('destination', ''),
            preferred_date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else None,
            guests=int(data.get('guests', 1)),
            message=data.get('message', ''),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        # Create Google Calendar event
        if booking.preferred_date:
            event_id = create_google_calendar_event(booking)
            if event_id:
                booking.google_event_id = event_id
                db.session.commit()
        
        logger.info(f"New booking created: {booking.booking_reference}")
        
        return jsonify({
            'success': True,
            'message': 'Booking request submitted successfully',
            'data': {
                'booking_reference': booking.booking_reference,
                'status': booking.status
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid date format'}), 400
    except Exception as e:
        logger.error(f"Error creating booking: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@app.route('/api/contact', methods=['POST'])
@limiter.limit("3 per hour")
def contact_message():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        message = ContactMessage(
            name=data['name'],
            email=data['email'],
            subject=data.get('subject', ''),
            message=data['message'],
            ip_address=request.remote_addr
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error saving contact message: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
