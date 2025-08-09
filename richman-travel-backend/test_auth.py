# test_auth.py - Test the authentication route directly
from app import create_app
from app.models import Admin
import json

app = create_app()

with app.app_context():
    print("🧪 Testing authentication route...")
    
    # Create test client
    client = app.test_client()
    
    # Test data
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    print(f"📤 Sending login request with data: {login_data}")
    
    # Make request to auth route
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"📥 Response status: {response.status_code}")
    print(f"📥 Response data: {response.get_json()}")
    
    # Also test the admin route (if it exists)
    print("\n🔄 Testing admin login route too...")
    
    try:
        admin_response = client.post(
            '/api/admin/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        print(f"📥 Admin route status: {admin_response.status_code}")
        print(f"📥 Admin route data: {admin_response.get_json()}")
    except Exception as e:
        print(f"❌ Admin route error: {e}")
    
    # Let's also check what routes are registered
    print("\n🗺️  Registered routes:")
    for rule in app.url_map.iter_rules():
        if 'login' in rule.rule or 'auth' in rule.rule:
            print(f"   {rule.methods} {rule.rule} -> {rule.endpoint}")
            