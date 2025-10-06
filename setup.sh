#!/bin/bash

# IAEF Setup Script
echo "🚀 Setting up Inegben Adaptive EdTech Framework (IAEF)"

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Please install PostgreSQL."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your database credentials"
fi

# Setup database
echo "Setting up database..."
echo "Please ensure PostgreSQL is running and create a database named 'iaef_db'"
echo "You can do this by running: createdb iaef_db"

# Initialize database
echo "Initializing database with sample data..."
python scripts/init_db.py

cd ..

# Setup Frontend
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Update backend/.env with your database credentials"
echo "2. Start the backend server: cd backend && source venv/bin/activate && python run.py"
echo "3. Start the frontend server: cd frontend && npm start"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "👥 Sample users:"
echo "- alex@example.com / alex_student (Visual Learner)"
echo "- sarah@example.com / sarah_professional (Auditory Learner)"
echo "- mike@example.com / mike_learner (Kinesthetic Learner)"
echo "Password for all: password123"
