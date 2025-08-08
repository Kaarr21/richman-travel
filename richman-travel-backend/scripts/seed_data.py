# scripts/seed_data.py - Database seeding
from app.extensions import db
from app.models import Admin, Destination
import json

def seed_database():
    """Seed database with initial data"""
    
    # Create default admin
    if not Admin.query.first():
        admin = Admin(
            username='admin',
            email='richard@richmantravel.co.ke'
        )
        admin.set_password('changeme123')
        db.session.add(admin)
        print("Created default admin user")
    
    # Seed destinations
    if not Destination.query.first():
        destinations = [
            {
                'name': 'Maasai Mara Safari',
                'slug': 'maasai-mara-safari',
                'description': 'Experience the Great Migration and witness the Big Five in Kenya\'s most famous game reserve. The Maasai Mara offers unparalleled wildlife viewing opportunities.',
                'image_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800',
                'duration': '3 days',
                'highlights': json.dumps(['Big Five', 'Great Migration', 'Maasai Culture', 'Hot Air Balloon Safari']),
                'price_range': '$800 - $1200',
                'difficulty_level': 'easy',
                'best_time_to_visit': 'July - October',
                'is_featured': True
            },
            {
                'name': 'Mount Kenya Expedition',
                'slug': 'mount-kenya-expedition',
                'description': 'Conquer Africa\'s second-highest peak with breathtaking alpine scenery and unique wildlife. Perfect for adventure seekers.',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
                'duration': '5 days',
                'highlights': json.dumps(['Mountain Climbing', 'Alpine Lakes', 'Rare Wildlife', 'Photography']),
                'price_range': '$600 - $900',
                'difficulty_level': 'challenging',
                'best_time_to_visit': 'December - March, June - October',
                'is_featured': True
            },
            {
                'name': 'Coastal Paradise - Diani Beach',
                'slug': 'diani-beach-coastal',
                'description': 'Relax on pristine white sand beaches with crystal-clear waters of the Indian Ocean. Perfect for beach lovers.',
                'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
                'duration': '2 days',
                'highlights': json.dumps(['White Sand Beaches', 'Water Sports', 'Coral Reefs', 'Seafood']),
                'price_range': '$300 - $500',
                'difficulty_level': 'easy',
                'best_time_to_visit': 'October - April',
                'is_featured': True
            },
            {
                'name': 'Hell\'s Gate National Park',
                'slug': 'hells-gate-national-park',
                'description': 'Cycle through dramatic landscapes and geothermal features in this unique park. Great for adventure activities.',
                'image_url': 'https://images.unsplash.com/photo-1571771019784-3ff35f4f4277?w=800',
                'duration': '1 day',
                'highlights': json.dumps(['Cycling Safari', 'Rock Climbing', 'Geothermal Springs', 'Scenic Cliffs']),
                'price_range': '$150 - $250',
                'difficulty_level': 'moderate',
                'best_time_to_visit': 'Year Round',
                'is_featured': False
            }
        ]
        
        for dest_data in destinations:
            destination = Destination(**dest_data)
            db.session.add(destination)
        
        print("Created sample destinations")
    
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()
        