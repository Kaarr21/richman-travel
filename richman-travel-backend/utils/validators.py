# app/utils/validators.py - Input validation functions
import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_booking_data(data):
    """Validate booking form data"""
    errors = []
    
    if not data.get('name'):
        errors.append('Name is required')
    
    if not data.get('email') or not validate_email(data['email']):
        errors.append('Valid email is required')
    
    # More validation logic
    
    return errors

def validate_destination_data(data):
    """Validate destination data"""
    # Destination validation logic
    pass