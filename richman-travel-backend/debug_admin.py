# debug_admin.py - Check what's wrong with admin login
from app import create_app
from app.extensions import db
from app.models import Admin, Booking
import bcrypt

app = create_app()

with app.app_context():
    print("🔍 Debugging admin user...")
    
    # Check all admin users
    admins = Admin.query.all()
    print(f"\n📊 Found {len(admins)} admin user(s):")
    
    for admin in admins:
        print(f"\n👤 Admin ID: {admin.id}")
        print(f"   Username: '{admin.username}'")
        print(f"   Email: {admin.email}")
        print(f"   Is Active: {admin.is_active}")
        print(f"   Password Hash: {admin.password_hash}")
        print(f"   Created: {admin.created_at}")
        print(f"   Last Login: {admin.last_login}")
        
        # Test password verification
        test_password = 'admin123'
        print(f"\n🔐 Testing password '{test_password}'...")
        
        try:
            # Test the stored hash
            result = admin.check_password(test_password)
            print(f"   Password check result: {result}")
            
            # Manual verification
            manual_check = bcrypt.checkpw(
                test_password.encode('utf-8'), 
                admin.password_hash.encode('utf-8')
            )
            print(f"   Manual bcrypt check: {manual_check}")
            
        except Exception as e:
            print(f"   ❌ Password check error: {e}")
    
    # Let's also check if there are any bookings
    booking_count = Booking.query.count()
    print(f"\n📋 Total bookings in database: {booking_count}")
    
    if booking_count > 0:
        recent_booking = Booking.query.order_by(Booking.created_at.desc()).first()
        print(f"   Most recent booking: {recent_booking.name} - {recent_booking.destination}")
    
    print("\n🔧 Let's reset the admin password to be sure...")
    
    # Reset admin password
    admin = Admin.query.filter_by(username='admin').first()
    if admin:
        # Set new password
        admin.set_password('admin123')
        db.session.commit()
        
        print("✅ Admin password reset successfully!")
        
        # Test again
        test_result = admin.check_password('admin123')
        print(f"   New password test: {test_result}")
        
        if test_result:
            print("✅ Password verification working!")
        else:
            print("❌ Password verification still failing")
            
            # Let's try creating a completely new admin
            print("\n🔄 Creating fresh admin user...")
            
            # Delete old admin
            db.session.delete(admin)
            db.session.commit()
            
            # Create new admin
            new_admin = Admin(
                username='admin',
                email='admin@richmantravel.co.ke',
                is_active=True
            )
            new_admin.set_password('admin123')
            
            db.session.add(new_admin)
            db.session.commit()
            
            # Test new admin
            final_test = new_admin.check_password('admin123')
            print(f"   Fresh admin password test: {final_test}")
    
    print("\n🎯 Final verification...")
    final_admin = Admin.query.filter_by(username='admin').first()
    if final_admin and final_admin.check_password('admin123'):
        print("✅ Admin login should work now!")
        print(f"   Username: admin")
        print(f"   Password: admin123") 
        print(f"   Active: {final_admin.is_active}")
    else:
        print("❌ Still having issues with admin login")
        