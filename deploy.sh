#!/bin/bash

# Flask Authentication System Deployment Script

echo "🚀 Flask Authentication System Deployment"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create database tables
echo "🗄️ Setting up database..."
python -c "
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    
    # Create default admin user if it doesn't exist
    if not User.get_by_username('admin'):
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Created default admin user (username: admin, password: admin123)')
    else:
        print('ℹ️ Admin user already exists')
"

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 To start the application:"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "📱 The application will be available at: http://localhost:5000"
echo ""
echo "👤 Default login credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🧪 To run tests:"
echo "   python test_auth.py"