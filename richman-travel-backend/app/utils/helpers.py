# app/utils/helpers.py - General helper functions
from flask import jsonify
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import uuid

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
        return jsonify({
            'success': False, 
            'message': 'Rate limit exceeded. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

def generate_booking_reference():
    """Generate unique booking reference"""
    timestamp = datetime.now().strftime('%Y%m')
    unique_id = str(uuid.uuid4())[:6].upper()
    return f"RT{timestamp}{unique_id}"

def send_notification_email(to_email, subject, body, is_html=False):
    """Send notification email using SMTP"""
    try:
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')
        
        if not smtp_username or not smtp_password:
            logger.warning("SMTP credentials not configured")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def send_booking_confirmation_email(booking):
    """Send booking confirmation email to client"""
    subject = f"Booking Confirmation - {booking.booking_reference}"
    
    body = f"""
    Dear {booking.name},
    
    Thank you for your booking with Richman Travel & Tours!
    
    Booking Details:
    - Reference: {booking.booking_reference}
    - Destination: {booking.destination}
    - Preferred Date: {booking.preferred_date.strftime('%B %d, %Y') if booking.preferred_date else 'TBD'}
    - Number of Guests: {booking.guests}
    - Status: {booking.status.title()}
    
    {f"Special Requests: {booking.message}" if booking.message else ""}
    
    Richard will contact you shortly with detailed itinerary and pricing information.
    
    For any questions, please don't hesitate to contact us.
    
    Best regards,
    Richard
    Richman Travel & Tours
    Phone: +254 700 123 456
    Email: richard@richmantravel.co.ke
    """
    
    return send_notification_email(booking.email, subject, body.strip())

def send_admin_booking_notification(booking):
    """Send new booking notification to admin"""
    admin_email = os.environ.get('ADMIN_EMAIL', 'richard@richmantravel.co.ke')
    subject = f"New Booking Request - {booking.booking_reference}"
    
    body = f"""
    New booking request received:
    
    Client Details:
    - Name: {booking.name}
    - Email: {booking.email}
    - Phone: {booking.phone or 'Not provided'}
    
    Booking Details:
    - Reference: {booking.booking_reference}
    - Destination: {booking.destination}
    - Preferred Date: {booking.preferred_date.strftime('%B %d, %Y') if booking.preferred_date else 'Not specified'}
    - Number of Guests: {booking.guests}
    - Status: {booking.status.title()}
    
    {f"Message from client: {booking.message}" if booking.message else ""}
    
    IP Address: {booking.ip_address}
    Created: {booking.created_at.strftime('%B %d, %Y at %I:%M %p')}
    
    Please review and respond to this booking request.
    """
    
    return send_notification_email(admin_email, subject, body.strip())

def format_currency(amount, currency='USD'):
    """Format currency amount"""
    if not amount:
        return 'N/A'
    return f"{currency} {amount:,.2f}"

def get_client_ip(request):
    """Get client IP address from request"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def log_user_activity(user_type, action, details=None):
    """Log user activity for audit trail"""
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_type': user_type,
        'action': action,
        'details': details
    }
    logger.info(f"Activity: {log_data}")
    