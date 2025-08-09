# debug_backend.py - Quick test script for your backend
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models import Booking
import json

def test_booking_validation():
    """Test booking validation with sample data"""
    app = create_app()
    
    with app.app_context():
        # Test data that should pass validation
        valid_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+254700123456',
            'destination': 'maasai-mara-safari',
            'date': '2025-08-15',
            'guests': 2,
            'message': 'Looking forward to the safari experience!'
        }
        
        # Test data that should fail validation
        invalid_data = {
            'name': '',  # Missing name
            'email': 'invalid-email',  # Invalid email
            'phone': '123',  # Too short phone
            'date': '2025-13-45',  # Invalid date
            'guests': -1,  # Invalid guests
            'message': 'x' * 2001  # Too long message
        }
        
        # Import validation function
        from app.utils.validators import validate_booking_data
        
        print("Testing valid data:")
        valid_errors = validate_booking_data(valid_data)
        print(f"Errors: {valid_errors}")
        print(f"Valid: {len(valid_errors) == 0}")
        
        print("\nTesting invalid data:")
        invalid_errors = validate_booking_data(invalid_data)
        print(f"Errors: {invalid_errors}")
        print(f"Invalid: {len(invalid_errors) > 0}")
        
        # Test database connection
        print("\nTesting database connection:")
        try:
            booking_count = Booking.query.count()
            print(f"Current bookings in database: {booking_count}")
            print("Database connection: OK")
        except Exception as e:
            print(f"Database error: {e}")
        
        # Test creating a booking
        print("\nTesting booking creation:")
        try:
            test_booking = Booking(
                name=valid_data['name'],
                email=valid_data['email'],
                phone=valid_data['phone'],
                destination=valid_data['destination'],
                guests=valid_data['guests'],
                message=valid_data['message'],
                ip_address='127.0.0.1',
                user_agent='test'
            )
            test_booking.booking_reference = test_booking.generate_reference()
            
            print(f"Generated reference: {test_booking.booking_reference}")
            print("Booking creation: OK")
            
            # Don't actually save to avoid test data in production
            # db.session.add(test_booking)
            # db.session.commit()
            
        except Exception as e:
            print(f"Booking creation error: {e}")

def test_api_endpoints():
    """Test API endpoints"""
    app = create_app()
    
    with app.test_client() as client:
        print("\nTesting API endpoints:")
        
        # Test health endpoint
        response = client.get('/api/health')
        print(f"Health endpoint: {response.status_code} - {response.get_json()}")
        
        # Test destinations endpoint
        response = client.get('/api/destinations')
        print(f"Destinations endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"Found {data.get('count', 0)} destinations")
        
        # Test booking endpoint with valid data
        booking_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+254700123456',
            'destination': 'maasai-mara-safari',
            'date': '2025-08-15',
            'guests': 2,
            'message': 'Test booking'
        }
        
        response = client.post('/api/bookings', 
                              data=json.dumps(booking_data),
                              content_type='application/json')
        print(f"Booking endpoint: {response.status_code}")
        if response.status_code != 201:
            print(f"Error: {response.get_json()}")

if __name__ == '__main__':
    print("=== Richman Travel Backend Debug ===")
    test_booking_validation()
    test_api_endpoints()
    print("\n=== Debug Complete ===")
    