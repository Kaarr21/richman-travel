# app/utils/validators.py - Fixed validation logic
import re
from datetime import datetime, date

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format - made more lenient"""
    if not phone:
        return True  # Phone is optional
    # Remove all non-digit characters for validation
    cleaned_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
    # Allow 7-15 digits (more flexible)
    return len(cleaned_phone) >= 7 and cleaned_phone.isdigit()

def validate_booking_data(data):
    """Validate booking form data with improved logic"""
    errors = []
    
    # Required fields validation
    name = data.get('name', '').strip()
    if not name or len(name) < 2:
        errors.append('Name must be at least 2 characters long')
    
    email = data.get('email', '').strip()
    if not email:
        errors.append('Email address is required')
    elif not validate_email(email):
        errors.append('Please enter a valid email address')
    
    # Optional phone validation - more lenient
    phone = data.get('phone', '').strip()
    if phone and not validate_phone(phone):
        errors.append('Please enter a valid phone number (7-15 digits)')
    
    # Date validation - allow empty dates
    booking_date = data.get('date', '').strip()
    if booking_date:
        try:
            parsed_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
            # Allow dates from today onwards (more lenient)
            if parsed_date < date.today():
                errors.append('Booking date should be today or in the future')
        except ValueError:
            errors.append('Please enter date in YYYY-MM-DD format')
    
    # Guests validation - more lenient range
    try:
        guests = int(data.get('guests', 1))
        if guests < 1:
            errors.append('Number of guests must be at least 1')
        elif guests > 100:  # More reasonable upper limit
            errors.append('Number of guests cannot exceed 100')
    except (ValueError, TypeError):
        errors.append('Please enter a valid number of guests')
    
    # Destination validation - optional
    destination = data.get('destination', '').strip()
    # No validation required since destination is optional
    
    # Message validation - optional with reasonable length limit
    message = data.get('message', '').strip()
    if message and len(message) > 2000:  # Increased limit
        errors.append('Message cannot exceed 2000 characters')
    
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
    
    name = data.get('name', '').strip()
    if not name or len(name) < 2:
        errors.append('Name must be at least 2 characters long')
    
    email = data.get('email', '').strip()
    if not email:
        errors.append('Email address is required')
    elif not validate_email(email):
        errors.append('Please enter a valid email address')
    
    message = data.get('message', '').strip()
    if not message or len(message) < 10:
        errors.append('Message must be at least 10 characters long')
    
    if message and len(message) > 2000:
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
    text = re.sub(r'<[^>]*>', '', str(text))
    text = re.sub(r'javascript:', '', str(text), flags=re.IGNORECASE)
    return text.strip()
    