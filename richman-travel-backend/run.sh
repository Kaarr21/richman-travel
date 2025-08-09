# Create richman-travel-backend/run.sh
cat > richman-travel-backend/run.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Starting Richman Travel Backend..."

# Load environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=true

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️ Setting up database..."
flask db init || echo "Database already initialized"
flask db migrate -m "Initial migration" || echo "Migration failed or not needed"
flask db upgrade || echo "Upgrade failed or not needed"

# Create tables and seed data
python -c "
from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    print('Creating database tables...')
    db.create_all()
    print('Database setup complete!')
"

# Start the application
echo "🌐 Starting Flask server on port 5000..."
flask run --host=0.0.0.0 --port=5000
EOF

chmod +x richman-travel-backend/run.sh
