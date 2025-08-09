from app import create_app
from app.models import Booking, Admin
from app.extensions import db

app = create_app()
with app.app_context():
    print("Testing database connection...")
    
    # Test admin exists
    admin_count = Admin.query.count()
    print(f"Admin users: {admin_count}")
    
    # Test bookings
    booking_count = Booking.query.count()
    print(f"Bookings: {booking_count}")
    
    # Show recent booking
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    print("\nRecent bookings:")
    for booking in recent_bookings:
        print(f"- {booking.name}: {booking.destination} ({booking.status})")
        