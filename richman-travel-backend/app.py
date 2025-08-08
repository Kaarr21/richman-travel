# app.py - Main application entry point
import os
from app import create_app
from app.extensions import db

# Create Flask app
app = create_app(os.getenv('FLASK_CONFIG', 'development'))

@app.cli.command()
def init_db():
    """Initialize database with tables and seed data"""
    from scripts.seed_data import seed_database
    print("Creating database tables...")
    db.create_all()
    print("Seeding database...")
    seed_database()
    print("Database initialized successfully!")

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    from scripts.seed_data import seed_database
    seed_database()
    print("Database seeded successfully!")

@app.cli.command()
def create_admin():
    """Create admin user interactively"""
    from app.models import Admin
    import getpass
    
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = getpass.getpass("Enter admin password: ")
    
    # Check if admin already exists
    if Admin.query.filter_by(username=username).first():
        print(f"Admin with username '{username}' already exists!")
        return
    
    admin = Admin(username=username, email=email)
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin user '{username}' created successfully!")

if __name__ == '__main__':
    # For development
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(
        debug=debug_mode,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )