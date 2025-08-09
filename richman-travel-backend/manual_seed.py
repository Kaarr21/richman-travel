# manual_seed.py - Manually seed database with debugging
from app import create_app
from app.extensions import db
from app.models import Admin, Destination
import json

app = create_app()
with app.app_context():
    print("🌱 Manual Database Seeding")
    print("=" * 50)
    
    # Clear existing data first (optional)
    print("🗑️ Clearing existing destinations...")
    Destination.query.delete()
    db.session.commit()
    print("✅ Cleared existing destinations")
    
    # Create destinations manually
    destinations_data = [
        {
            'name': 'Maasai Mara Safari',
            'slug': 'maasai-mara-safari',
            'description': 'Experience the Great Migration and witness the Big Five in Kenya\'s most famous game reserve. The Maasai Mara offers unparalleled wildlife viewing opportunities.',
            'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800',
            'duration': '3 days',
            'highlights': ['Big Five', 'Great Migration', 'Maasai Culture', 'Hot Air Balloon Safari'],
            'price_range': '$800 - $1200',
            'difficulty_level': 'easy',
            'best_time_to_visit': 'July - October',
            'is_featured': True,
            'is_active': True
        },
        {
            'name': 'Mount Kenya Expedition',
            'slug': 'mount-kenya-expedition',
            'description': 'Conquer Africa\'s second-highest peak with breathtaking alpine scenery and unique wildlife. Perfect for adventure seekers.',
            'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
            'duration': '5 days',
            'highlights': ['Mountain Climbing', 'Alpine Lakes', 'Rare Wildlife', 'Photography'],
            'price_range': '$600 - $900',
            'difficulty_level': 'challenging',
            'best_time_to_visit': 'December - March, June - October',
            'is_featured': True,
            'is_active': True
        },
        {
            'name': 'Coastal Paradise - Diani Beach',
            'slug': 'diani-beach-coastal',
            'description': 'Relax on pristine white sand beaches with crystal-clear waters of the Indian Ocean. Perfect for beach lovers.',
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
            'duration': '2 days',
            'highlights': ['White Sand Beaches', 'Water Sports', 'Coral Reefs', 'Seafood'],
            'price_range': '$300 - $500',
            'difficulty_level': 'easy',
            'best_time_to_visit': 'October - April',
            'is_featured': True,
            'is_active': True
        },
        {
            'name': 'Hell\'s Gate National Park',
            'slug': 'hells-gate-national-park',
            'description': 'Cycle through dramatic landscapes and geothermal features in this unique park. Great for adventure activities.',
            'image_url': 'https://images.unsplash.com/photo-1571771019784-3ff35f4f4277?w=800',
            'duration': '1 day',
            'highlights': ['Cycling Safari', 'Rock Climbing', 'Geothermal Springs', 'Scenic Cliffs'],
            'price_range': '$150 - $250',
            'difficulty_level': 'moderate',
            'best_time_to_visit': 'Year Round',
            'is_featured': False,
            'is_active': True
        }
    ]
    
    print(f"🏗️ Creating {len(destinations_data)} destinations...")
    
    for i, dest_data in enumerate(destinations_data, 1):
        print(f"Creating destination {i}: {dest_data['name']}")
        
        # Convert highlights list to JSON string
        dest_data['highlights'] = json.dumps(dest_data['highlights'])
        
        try:
            destination = Destination(**dest_data)
            db.session.add(destination)
            print(f"  ✅ Added {destination.name}")
        except Exception as e:
            print(f"  ❌ Error adding {dest_data['name']}: {e}")
    
    # Commit all destinations
    try:
        db.session.commit()
        print("✅ All destinations committed to database")
    except Exception as e:
        print(f"❌ Commit failed: {e}")
        db.session.rollback()
        exit(1)
    
    # Verify the destinations were created
    print("\n🔍 Verifying created destinations:")
    all_destinations = Destination.query.all()
    print(f"Total destinations: {len(all_destinations)}")
    
    active_destinations = Destination.query.filter_by(is_active=True).all()
    print(f"Active destinations: {len(active_destinations)}")
    
    for dest in active_destinations:
        print(f"  - {dest.name} (Active: {dest.is_active}, Featured: {dest.is_featured})")
    
    # Test serialization
    if active_destinations:
        print("\n🧪 Testing serialization of first destination:")
        try:
            first_dest = active_destinations[0]
            dest_dict = first_dest.to_dict()
            print("✅ Serialization successful!")
            print(f"Sample: {dest_dict['name']} - {dest_dict['duration']}")
        except Exception as e:
            print(f"❌ Serialization failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎉 Manual seeding complete!")
    