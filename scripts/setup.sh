#!/bin/bash

# Setup script for LangChain App Boilerplate

set -e

echo "🚀 Setting up LangChain App Boilerplate..."

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✅ Prerequisites met"

# Setup backend
echo ""
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your configuration"
fi

echo "✅ Backend setup complete"

cd ..

# Setup frontend
echo ""
echo "🎨 Setting up frontend..."
cd frontend

echo "Installing Node.js dependencies..."
npm install

if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cp .env.local.example .env.local
fi

echo "✅ Frontend setup complete"

cd ..

# Check Ollama
echo ""
echo "🤖 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434 > /dev/null 2>&1; then
        echo "✅ Ollama is running"
        
        # Check if llama2 model is available
        if ollama list | grep -q "llama2"; then
            echo "✅ llama2 model is installed"
        else
            echo "⚠️  llama2 model not found. You can pull it with: ollama pull llama2"
        fi
    else
        echo "⚠️  Ollama is not running. Please start Ollama."
    fi
else
    echo "⚠️  Ollama is not installed. Please install from https://ollama.ai"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure backend/.env with your settings"
echo "2. Start Ollama and pull a model: ollama pull llama2"
echo "3. Start the backend: cd backend && source venv/bin/activate && python main.py"
echo "4. Start the frontend: cd frontend && npm run dev"
echo ""
echo "Visit http://localhost:3000 to see the application"
