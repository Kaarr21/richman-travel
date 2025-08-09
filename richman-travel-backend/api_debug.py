# api_debug.py - Debug the API route directly
from app import create_app
from app.extensions import db
from app.models import Destination
from flask import request

app = create_app()

def test_destinations_route():
    with app.app_context():
        print("🔍 API Route Debug")
        print("=" * 50)
        
        # Simulate the exact API logic
        print("1. Testing basic query:")
        destinations = Destination.query.filter_by(is_active=True).all()
        print(f"   Found {len(destinations)} active destinations")
        
        print("\n2. Testing with order by:")
        destinations = Destination.query.filter_by(is_active=True).order_by(Destination.created_at.desc()).all()
        print(f"   Found {len(destinations)} destinations with order by")
        
        print("\n3. Testing serialization:")
        result = []
        for dest in destinations:
            try:
                dest_dict = dest.to_dict()
                result.append(dest_dict)
                print(f"   ✅ Serialized: {dest.name}")
            except Exception as e:
                print(f"   ❌ Failed to serialize {dest.name}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n4. Final result: {len(result)} destinations serialized")
        
        if result:
            print("\n5. Sample serialized destination:")
            print(f"   Name: {result[0]['name']}")
            print(f"   Slug: {result[0]['slug']}")
            print(f"   Active: {result[0].get('is_active', 'NOT_FOUND')}")
        
        # Test the exact response format
        print("\n6. Testing response format:")
        response_data = {
            'success': True,
            'data': result,
            'count': len(result)
        }
        print(f"   Response: {response_data}")
        return response_data

if __name__ == "__main__":
    result = test_destinations_route()
    
    # Also test with Flask test client
    print("\n" + "=" * 50)
    print("🧪 Testing with Flask test client:")
    
    with app.test_client() as client:
        response = client.get('/api/destinations')
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response.get_json()}")
        
        if response.status_code == 500:
            print("❌ 500 Error - checking logs")
            # The error should be printed in the console when running
            