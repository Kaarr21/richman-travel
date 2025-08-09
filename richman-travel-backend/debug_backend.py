# debug_backend.py - Debug script to identify backend issues
import os
import sys
sys.path.append('.')

def test_imports():
    """Test all imports"""
    print("🔍 Testing imports...")
    try:
        from app import create_app
        print("✅ app.create_app imported")
        
        from app.extensions import db, cors, limiter
        print("✅ extensions imported")
        
        from app.models import Destination, Booking, Admin
        print("✅ models imported")
        
        from app.routes import public_bp, admin_bp, auth_bp
        print("✅ routes imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test app creation"""
    print("\n🔍 Testing app creation...")
    try:
        from app import create_app
        app = create_app('development')
        print("✅ App created successfully")
        return app
    except Exception as e:
        print(f"❌ App creation error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_database():
    """Test database connection"""
    print("\n🔍 Testing database...")
    try:
        from app import create_app
        from app.extensions import db
        from app.models import Destination
        
        app = create_app('development')
        with app.app_context():
            # Try to create tables
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Try to query destinations
            destinations = Destination.query.all()
            print(f"✅ Found {len(destinations)} destinations in database")
            
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_routes():
    """Test route registration"""
    print("\n🔍 Testing routes...")
    try:
        from app import create_app
        app = create_app('development')
        
        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.endpoint}: {rule.rule} [{rule.methods}]")
        
        return True
    except Exception as e:
        print(f"❌ Route error: {e}")
        return False

def test_destinations_endpoint():
    """Test the destinations endpoint logic"""
    print("\n🔍 Testing destinations endpoint logic...")
    try:
        from app import create_app
        from app.models import Destination
        app = create_app('development')
        
        with app.app_context():
            destinations = Destination.query.filter_by(is_active=True).all()
            print(f"✅ Query successful: {len(destinations)} active destinations")
            
            # Test serialization
            if destinations:
                dest_dict = destinations[0].to_dict()
                print(f"✅ Serialization successful: {dest_dict}")
            
            return True
    except Exception as e:
        print(f"❌ Destinations endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Backend Debug Script")
    print("=" * 50)
    
    # Load environment
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    else:
        print("⚠️  No .env file found")
    
    # Run tests
    tests = [
        test_imports,
        test_app_creation, 
        test_database,
        test_routes,
        test_destinations_endpoint
    ]
    
    for test in tests:
        if not test():
            print(f"\n❌ Test failed: {test.__name__}")
            break
        print("")
    
    print("🔚 Debug complete")

if __name__ == "__main__":
    main()
    