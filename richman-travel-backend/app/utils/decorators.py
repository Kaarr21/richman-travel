# app/utils/decorators.py - Custom decorators
from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models import Admin, SiteVisit
from app.extensions import db
import uuid
import logging

logger = logging.getLogger(__name__)

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
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
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
        