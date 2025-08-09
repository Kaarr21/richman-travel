# database_debug.py - Debug database content
from app import create_app
from app.extensions import db
from app.models import Destination, Admin, Booking

app = create_app()
with app.app_context():
    print("🔍 Database Debug Information")
    print("=" * 50)
    
    # Check all destinations (including inactive ones)
    all_destinations = Destination.query.all()
    print(f"📊 Total destinations in database: {len(all_destinations)}")
    
    # Check active destinations specifically
    active_destinations = Destination.query.filter_by(is_active=True).all()
    print(f"📊 Active destinations: {len(active_destinations)}")
    
    # Check inactive destinations
    inactive_destinations = Destination.query.filter_by(is_active=False).all()
    print(f"📊 Inactive destinations: {len(inactive_destinations)}")
    
    print("\n🏷️ All destinations details:")
    for i, dest in enumerate(all_destinations, 1):
        print(f"{i}. {dest.name}")
        print(f"   ID: {dest.id}")
        print(f"   Slug: {dest.slug}")
        print(f"   Active: {dest.is_active}")
        print(f"   Featured: {dest.is_featured}")
        print(f"   Created: {dest.created_at}")
        print("")
    
    # Check admins
    admins = Admin.query.all()
    print(f"👤 Admins in database: {len(admins)}")
    for admin in admins:
        print(f"   - {admin.username} ({admin.email})")
    
    # Check bookings
    bookings = Booking.query.all()
    print(f"📅 Bookings in database: {len(bookings)}")
    
    # Test the exact query used in the API
    print("\n🔍 Testing API query:")
    try:
        query = Destination.query.filter_by(is_active=True)
        destinations = query.order_by(Destination.created_at.desc()).all()
        print(f"API query result: {len(destinations)} destinations")
        
        if destinations:
            print("First destination to_dict():")
            try:
                first_dict = destinations[0].to_dict()
                print(first_dict)
            except Exception as e:
                print(f"❌ Serialization error: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Query error: {e}")
        import traceback
        traceback.print_exc()
        