# app/routes/admin.py - Fixed version with duplicate login removed
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db, limiter
from app.models import Booking, Destination, Admin, SiteVisit, ContactMessage
from app.utils.decorators import token_required
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

# REMOVED: Duplicate login route (now only in auth.py)

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
        cancelled_bookings = Booking.query.filter_by(status='cancelled').count()
        
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
                    'completed': completed_bookings,
                    'cancelled': cancelled_bookings
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
        
        # Log the update attempt
        logger.info(f"Admin {current_admin.username} updating booking {booking_id} with data: {data}")
        
        # Update allowed fields
        allowed_fields = ['status', 'estimated_cost']
        updated_fields = []
        
        for field in allowed_fields:
            if field in data and data[field] is not None:
                old_value = getattr(booking, field)
                new_value = data[field]
                
                # Convert estimated_cost to float if provided
                if field == 'estimated_cost' and new_value:
                    try:
                        new_value = float(new_value)
                    except (ValueError, TypeError):
                        return jsonify({
                            'success': False, 
                            'message': 'Invalid estimated cost format'
                        }), 400
                
                setattr(booking, field, new_value)
                updated_fields.append(f"{field}: {old_value} → {new_value}")
        
        booking.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Booking {booking.booking_reference} updated successfully. Changes: {', '.join(updated_fields)}")
        
        return jsonify({
            'success': True,
            'message': 'Booking updated successfully',
            'data': booking.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error updating booking {booking_id}: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
@token_required
def admin_delete_booking(current_admin, booking_id):
    """Delete a booking (soft delete by marking as cancelled)"""
    try:
        booking = Booking.query.get_or_404(booking_id)
        
        # Instead of actually deleting, mark as cancelled
        booking.status = 'cancelled'
        booking.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Admin {current_admin.username} cancelled booking {booking.booking_reference}")
        
        return jsonify({
            'success': True,
            'message': 'Booking cancelled successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting booking {booking_id}: {e}")
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
        
        # Check if slug already exists
        existing = Destination.query.filter_by(slug=slug).first()
        if existing:
            return jsonify({'success': False, 'message': 'A destination with this name already exists'}), 400
        
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
        
        logger.info(f"Admin {current_admin.username} created destination: {destination.name}")
        
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
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        messages = ContactMessage.query.order_by(
            ContactMessage.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': [msg.to_dict() for msg in messages.items],
            'pagination': {
                'page': page,
                'pages': messages.pages,
                'per_page': per_page,
                'total': messages.total
            }
        })
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@admin_bp.route('/export/bookings', methods=['GET'])
@token_required
def admin_export_bookings(current_admin):
    """Export bookings as CSV"""
    try:
        import csv
        import io
        from flask import make_response
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Booking Reference', 'Name', 'Email', 'Phone', 'Destination',
            'Date', 'Guests', 'Status', 'Estimated Cost', 'Created', 'Message'
        ])
        
        # Write bookings
        bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        for booking in bookings:
            writer.writerow([
                booking.booking_reference,
                booking.name,
                booking.email,
                booking.phone or '',
                booking.destination or '',
                booking.preferred_date.strftime('%Y-%m-%d') if booking.preferred_date else '',
                booking.guests,
                booking.status,
                booking.estimated_cost or '',
                booking.created_at.strftime('%Y-%m-%d %H:%M'),
                booking.message or ''
            ])
        
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=bookings_{datetime.now().strftime("%Y%m%d")}.csv'
        
        logger.info(f"Admin {current_admin.username} exported bookings")
        return response
        
    except Exception as e:
        logger.error(f"Error exporting bookings: {e}")
        return jsonify({'success': False, 'message': 'Export failed'}), 500