#!/bin/bash
# scripts/deploy.sh - Deployment script

set -e

echo "🚀 Starting deployment process..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Database migrations
echo "🗄️ Running database migrations..."
flask db upgrade

# Seed database (only if needed)
echo "🌱 Seeding database..."
python -c "
from app import create_app
from app.extensions import db
from scripts.seed_data import seed_database

app = create_app()
with app.app_context():
    # Only seed if no data exists
    from app.models import Admin
    if not Admin.query.first():
        seed_database()
        print('Database seeded successfully!')
    else:
        print('Database already contains data, skipping seed.')
"

echo "✅ Deployment completed successfully!"
