# scripts/init_db.py - Database initialization script

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from scripts.seed_data import seed_database

def init_database():
    """Initialize database with tables and seed data"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        print("Seeding database with initial data...")
        seed_database()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
