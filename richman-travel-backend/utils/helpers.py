# app/utils/helpers.py - General helper functions
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register error handlers for the app"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'success': False, 'message': 'Method not allowed'}), 405
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({'success': False, 'message': 'Rate limit exceeded'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

def generate_booking_reference():
    """Generate unique booking reference"""
    # Reference generation logic
    pass

def send_notification_email(to_email, subject, body):
    """Send notification email"""
    # Email sending logic
    pass