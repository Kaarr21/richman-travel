# app.py - Keep this minimal, just the entry point
from app import create_app
from app.extensions import db
import os

app = create_app(os.getenv('FLASK_CONFIG', 'development'))

@app.cli.command()
def init_db():
    """Initialize database with tables and seed data"""
    from scripts.seed_data import seed_database
    db.create_all()
    seed_database()
    print("Database initialized successfully!")

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')