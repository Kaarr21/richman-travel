# app/routes/auth.py - Authentication endpoints
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db, limiter
from app.models import Admin
from app.utils.decorators import token_required
import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
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

@auth_bp.route('/logout', methods=['POST'])
@token_required
def admin_logout(current_admin):
    """Admin logout"""
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify_token(current_admin):
    """Verify JWT token"""
    return jsonify({
        'success': True,
        'admin': {
            'id': current_admin.id,
            'username': current_admin.username,
            'email': current_admin.email
        }
    })
    