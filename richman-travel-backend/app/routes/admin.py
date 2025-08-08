# app/routes/admin.py - Admin-only API endpoints
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db, limiter
from app.models import Booking, Destination, Admin, SiteVisit, ContactMessage
from app.utils.decorators import token_required
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import jwt
import json
import logging

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def admin_login():
    """Admin login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        admin = Admin.query.filter_by(username=username, is_active=True).first()
        if not admin or not admin.check_password(password):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Update last login
        admin.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'admin_id': admin.id,
            'username': admin.username,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'admin': {
                'id': admin.id,
                'username': admin.username,
                'email': admin.email,
                'last_login': admin.last_login.isoformat() if admin.last_login else None
            }
        })
        
    except Exception as e:
        logger.error(f"Error during admin login: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/dashboard/stats', methods=['GET'])
@token_required
def admin_dashboard_stats(current_admin):
    """Get dashboard statistics"""
    try:
        now = datetime.utcnow()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)
        
        # Visit statistics
        daily_visits = SiteVisit.query.filter(
            func.date(SiteVisit.timestamp) == today
        ).count()
        
        weekly_visits = SiteVisit.query.filter(
            SiteVisit.timestamp >= week_ago
        ).count()
        
        monthly_visits = SiteVisit.query.filter(
            SiteVisit.timestamp >= month_ago
        ).count()
        
        yearly_visits = SiteVisit.query.filter(
            SiteVisit.timestamp >= year_ago
        ).count()
        
        # Booking statistics
        total_bookings = Booking.query.count()
        pending_bookings = Booking.query.filter_by(status='pending').count()
        confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
        completed_bookings = Booking.query.filter_by(status='completed').count()
        
        # Top destinations
        top_destinations = db.session.query(
            Booking.destination,
            func.count(Booking.id).label('count')
        ).filter(
            Booking.destination.isnot(None),
            Booking.destination != ''
        ).group_by(Booking.destination).order_by(func.count(Booking.id).desc()).limit(5).all()
        
        return jsonify({
            'success': True,
            'data': {
                'visits': {
                    'daily': daily_visits,
                    'weekly': weekly_visits,
                    'monthly': monthly_visits,
                    'yearly': yearly_visits
                },
                'bookings': {
                    'total': total_bookings,
                    'pending': pending_bookings,
                    'confirmed': confirmed_bookings,
                    'completed': completed_bookings
                },
                'top_destinations': [{'destination': d, 'count': c} for d, c in top_destinations]
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/bookings', methods=['GET'])
@token_required
def admin_get_bookings(current_admin):
    """Get all bookings with pagination"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        status = request.args.get('status', '')
        
        query = Booking.query
        if status:
            query = query.filter_by(status=status)
        
        bookings = query.order_by(Booking.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [booking.to_dict() for booking in bookings.items],
            'pagination': {
                'page': page,
                'pages': bookings.pages,
                'per_page': per_page,
                'total': bookings.total
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching bookings: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/bookings/<int:booking_id>', methods=['PUT'])
@token_required
def admin_update_booking(current_admin, booking_id):
    """Update booking status and details"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['status', 'estimated_cost']
        for field in allowed_fields:
            if field in data:
                setattr(booking, field, data[field])
        
        booking.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Booking updated successfully',
            'data': booking.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating booking: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/destinations', methods=['GET'])
@token_required
def admin_get_destinations(current_admin):
    """Get all destinations for admin"""
    try:
        destinations = Destination.query.order_by(Destination.created_at.desc()).all()
        return jsonify({
            'success': True,
            'data': [dest.to_dict() for dest in destinations]
        })
    except Exception as e:
        logger.error(f"Error fetching destinations: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/destinations', methods=['POST'])
@token_required
def admin_create_destination(current_admin):
    """Create new destination"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        # Generate slug
        slug = data['name'].lower().replace(' ', '-').replace('&', 'and')
        
        destination = Destination(
            name=data['name'],
            slug=slug,
            description=data['description'],
            image_url=data.get('image_url', ''),
            duration=data.get('duration', ''),
            highlights=json.dumps(data.get('highlights', [])),
            price_range=data.get('price_range', ''),
            difficulty_level=data.get('difficulty_level', 'easy'),
            best_time_to_visit=data.get('best_time_to_visit', ''),
            is_featured=data.get('is_featured', False)
        )
        
        db.session.add(destination)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Destination created successfully',
            'data': destination.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating destination: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/messages', methods=['GET'])
@token_required
def admin_get_messages(current_admin):
    """Get contact messages"""
    try:
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(50).all()
        return jsonify({
            'success': True,
            'data': [msg.to_dict() for msg in messages]
        })
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
        