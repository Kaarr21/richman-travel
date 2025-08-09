# create_admin.py - Run this to set up your database and admin user
from app import create_app
from app.extensions import db
from app.models import Admin, Destination, Booking
from datetime import datetime, date
import json

app = create_app()

with app.app_context():
    print("🔧 Setting up database...")
    
    # Create all tables
    db.create_all()
    print("✅ Database tables created")
    
    # Create admin user if it doesn't exist
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(
            username='admin',
            email='admin@richmantravel.co.ke'
        )
        admin.set_password('admin123')  # Change this password!
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   🚨 IMPORTANT: Change this password in production!")
    else:
        print("✅ Admin user already exists")
    
    # Add sample destinations if none exist
    if Destination.query.count() == 0:
        sample_destinations = [
            {
                'name': 'Maasai Mara Safari',
                'slug': 'maasai-mara-safari',
                'description': 'Experience the Great Migration and witness the Big Five in Kenya\'s most famous national reserve.',
                'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=400',
                'duration': '3 days',
                'highlights': json.dumps(['Big Five', 'Great Migration', 'Maasai Culture', 'Hot Air Balloon Safari']),
                'price_range': '$300-500 per person',
                'difficulty_level': 'easy',
                'best_time_to_visit': 'July to October',
                'is_featured': True
            },
            {
                'name': 'Mount Kenya Expedition',
                'slug': 'mount-kenya-expedition',
                'description': 'Conquer Africa\'s second-highest peak and explore pristine alpine landscapes.',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400',
                'duration': '5 days',
                'highlights': json.dumps(['Mountain Climbing', 'Alpine Lakes', 'Rare Wildlife', 'Technical Climbing']),
                'price_range': '$500-800 per person',
                'difficulty_level': 'challenging',
                'best_time_to_visit': 'January to February, August to September',
                'is_featured': True
            },
            {
                'name': 'Diani Beach Coastal Experience',
                'slug': 'diani-beach-coastal',
                'description': 'Relax on pristine white sand beaches and explore vibrant coral reefs.',
                'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400',
                'duration': '4 days',
                'highlights': json.dumps(['White Sand Beaches', 'Coral Reefs', 'Water Sports', 'Local Cuisine']),
                'price_range': '$200-400 per person',
                'difficulty_level': 'easy',
                'best_time_to_visit': 'October to April',
                'is_featured': False
            },
            {
                'name': 'Hell\'s Gate National Park',
                'slug': 'hells-gate-national-park',
                'description': 'Cycle through dramatic landscapes and explore geothermal wonders.',
                'image_url': 'https://images.unsplash.com/photo-1551718746-4c8f5be3c65f?w=400',
                'duration': '1 day',
                'highlights': json.dumps(['Cycling Safari', 'Rock Climbing', 'Geothermal Features', 'Walking Safari']),
                'price_range': '$50-100 per person',
                'difficulty_level': 'moderate',
                'best_time_to_visit': 'Year round',
                'is_featured': False
            }
        ]
        
        for dest_data in sample_destinations:
            destination = Destination(**dest_data)
            db.session.add(destination)
        
        db.session.commit()
        print("✅ Sample destinations added")
    else:
        print("✅ Destinations already exist")
    
    # Add some sample bookings if none exist (for testing)
    if Booking.query.count() == 0:
        sample_bookings = [
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+254 700 123 456',
                'destination': 'Maasai Mara Safari',
                'preferred_date': date(2025, 9, 15),
                'guests': 2,
                'message': 'Looking forward to seeing the Big Five! This is our first safari.',
                'status': 'confirmed',
                'estimated_cost': 900.0,
                'ip_address': '127.0.0.1'
            },
            {
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'phone': '+254 700 654 321',
                'destination': 'Mount Kenya Expedition',
                'preferred_date': date(2025, 10, 5),
                'guests': 4,
                'message': 'First time mountain climbing, need experienced guide.',
                'status': 'pending',
                'ip_address': '127.0.0.1'
            },
            {
                'name': 'Mike Johnson',
                'email': 'mike@example.com',
                'phone': '+254 700 987 654',
                'destination': 'Diani Beach',
                'preferred_date': date(2025, 8, 28),
                'guests': 2,
                'message': 'Honeymoon trip, looking for romantic beachfront accommodation.',
                'status': 'completed',
                'estimated_cost': 400.0,
                'ip_address': '127.0.0.1'
            }
        ]
        
        for booking_data in sample_bookings:
            booking = Booking(**booking_data)
            booking.booking_reference = Booking.generate_unique_reference()
            db.session.add(booking)
        
        db.session.commit()
        print("✅ Sample bookings added")
    else:
        print("✅ Bookings already exist")
    
    # Display summary
    print("\n📊 Database Summary:")
    print(f"   Admins: {Admin.query.count()}")
    print(f"   Destinations: {Destination.query.count()}")
    print(f"   Bookings: {Booking.query.count()}")
    
    print("\n🚀 Setup complete!")
    print("\n🔐 Admin Login Details:")
    print("   URL: http://localhost:5173 (click 'Admin' button)")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n⚠️  Remember to change the admin password in production!")
    print("\n🎯 Next steps:")
    print("   1. Start your Flask backend: python app.py")
    print("   2. Start your React frontend: npm run dev")
    print("   3. Test the admin dashboard functionality")
    