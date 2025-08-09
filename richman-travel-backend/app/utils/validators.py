# app/utils/validators.py
import re
from datetime import datetime, date

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return True  # Phone is optional
    # Allow various phone formats
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    return re.match(pattern, re.sub(r'[\s\-\(\)]', '', phone)) is not None

def validate_booking_data(data):
    """Validate booking form data"""
    errors = []
    
    # Required fields
    if not data.get('name') or len(data['name'].strip()) < 2:
        errors.append('Name must be at least 2 characters long')
    
    if not data.get('email') or not validate_email(data['email']):
        errors.append('Valid email address is required')
    
    # Optional phone validation
    if data.get('phone') and not validate_phone(data['phone']):
        errors.append('Invalid phone number format')
    
    # Date validation
    if data.get('date'):
        try:
            booking_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if booking_date < date.today():
                errors.append('Booking date cannot be in the past')
        except ValueError:
            errors.append('Invalid date format (YYYY-MM-DD expected)')
    
    # Guests validation
    try:
        guests = int(data.get('guests', 1))
        if guests < 1 or guests > 50:
            errors.append('Number of guests must be between 1 and 50')
    except ValueError:
        errors.append('Invalid number of guests')
    
    # Message length
    if data.get('message') and len(data['message']) > 1000:
        errors.append('Message cannot exceed 1000 characters')
    
    return errors

def validate_destination_data(data):
    """Validate destination data"""
    errors = []
    
    # Required fields
    if not data.get('name') or len(data['name'].strip()) < 3:
        errors.append('Destination name must be at least 3 characters long')
    
    if not data.get('description') or len(data['description'].strip()) < 20:
        errors.append('Description must be at least 20 characters long')
    
    # Optional field validations
    if data.get('image_url') and not is_valid_url(data['image_url']):
        errors.append('Invalid image URL')
    
    if data.get('difficulty_level') and data['difficulty_level'] not in ['easy', 'moderate', 'challenging']:
        errors.append('Difficulty level must be easy, moderate, or challenging')
    
    return errors

def validate_contact_data(data):
    """Validate contact form data"""
    errors = []
    
    if not data.get('name') or len(data['name'].strip()) < 2:
        errors.append('Name must be at least 2 characters long')
    
    if not data.get('email') or not validate_email(data['email']):
        errors.append('Valid email address is required')
    
    if not data.get('message') or len(data['message'].strip()) < 10:
        errors.append('Message must be at least 10 characters long')
    
    if data.get('message') and len(data['message']) > 2000:
        errors.append('Message cannot exceed 2000 characters')
    
    return errors

def is_valid_url(url):
    """Validate URL format"""
    if not url:
        return True  # URL is optional
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, url) is not None

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return text
    # Remove potential HTML tags and script content
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    return text.strip()
    