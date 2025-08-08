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
    
    # Seed destinations
    if not Destination.query.first():
        destinations = [
            {
                'name': 'Maasai Mara Safari',
                'slug': 'maasai-mara-safari',
                'description': 'Experience the Great Migration...',
                # ... rest of destination data
            }
            # ... more destinations
        ]
        
        for dest_data in destinations:
            destination = Destination(**dest_data)
            db.session.add(destination)
    
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()