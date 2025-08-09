#!/bin/bash
# setup_richman_travel.sh - Complete setup script

set -e

echo "🚀 Setting up Richman Travel & Tours application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "richman-travel-backend/app.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Backend Setup
echo "📦 Setting up backend..."
cd richman-travel-backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install flask flask-sqlalchemy flask-migrate flask-cors flask-limiter
pip install bcrypt pyjwt python-dotenv
pip install psycopg2-binary  # For PostgreSQL

# Set environment variables
print_status "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << EOL
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production-123456789
DATABASE_URL=sqlite:///richman_travel.db
JWT_SECRET_KEY=jwt-secret-key-change-in-production-987654321
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
ADMIN_EMAIL=richard@richmantravel.co.ke
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
EOL
    print_status "Created .env file"
else
    print_warning ".env file already exists"
fi

# Initialize database
print_status "Initializing database..."
export FLASK_APP=app.py
flask db init 2>/dev/null || print_warning "Database already initialized"
flask db migrate -m "Initial migration" 2>/dev/null || print_warning "Migration already exists"
flask db upgrade

# Seed database
print_status "Seeding database..."
python -c "
import sys
sys.path.append('.')
from app import create_app
from app.extensions import db
from scripts.seed_data import seed_database

app = create_app()
with app.app_context():
    seed_database()
    print('Database seeded successfully!')
" || print_warning "Database seeding failed or already seeded"

# Test the backend
print_status "Testing backend..."
python -c "
from app import create_app
app = create_app()
with app.test_client() as client:
    response = client.get('/api/health')
    if response.status_code == 200:
        print('Backend test: PASSED')
    else:
        print('Backend test: FAILED')
        exit(1)
"

cd ..

# Frontend Setup
echo "🎨 Setting up frontend..."
cd richman-travel-frontend

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install || yarn install

# Create or update Vite config for CORS
print_status "Configuring Vite..."
cat > vite.config.js << EOL
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    cors: true
  }
})
EOL

cd ..

# Create startup scripts
print_status "Creating startup scripts..."

# Backend startup script
cat > start_backend.sh << EOL
#!/bin/bash
cd richman-travel-backend
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=true
echo "🚀 Starting Richman Travel Backend on http://localhost:5000"
python app.py
EOL

# Frontend startup script
cat > start_frontend.sh << EOL
#!/bin/bash
cd richman-travel-frontend
echo "🎨 Starting Richman Travel Frontend on http://localhost:5173"
npm run dev
EOL

# Combined startup script
cat > start_all.sh << EOL
#!/bin/bash
echo "🚀 Starting Richman Travel & Tours application..."

# Function to handle cleanup
cleanup() {
    echo "Stopping servers..."
    kill \$(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Start backend in background
echo "Starting backend..."
cd richman-travel-backend
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
export FLASK_APP=app.py
export FLASK_ENV=development
python app.py &
BACKEND_PID=\$!

cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend..."
cd richman-travel-frontend
npm run dev &
FRONTEND_PID=\$!

cd ..

echo "✅ Both servers are running!"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:5000/api"
echo "Press Ctrl+C to stop both servers"

# Wait for background processes
wait
EOL

# Make scripts executable
chmod +x start_backend.sh start_frontend.sh start_all.sh

# Create requirements.txt for backend
cat > richman-travel-backend/requirements.txt << EOL
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
bcrypt==4.0.1
PyJWT==2.8.0
python-dotenv==1.0.0
psycopg2-binary==2.9.7
EOL

print_status "Setup complete!"

echo ""
echo "🎉 Richman Travel & Tours setup completed successfully!"
echo ""
echo "To start the application:"
echo "  • Backend only:  ./start_backend.sh"
echo "  • Frontend only: ./start_frontend.sh"
echo "  • Both servers:  ./start_all.sh"
echo ""
echo "URLs:"
echo "  • Frontend: http://localhost:5173"
echo "  • Backend API: http://localhost:5000/api"
echo "  • Health check: http://localhost:5000/api/health"
echo ""
echo "Default admin credentials:"
echo "  • Username: admin"
echo "  • Password: changeme123"
echo ""
print_warning "Remember to change the admin password and secret keys for production!"
