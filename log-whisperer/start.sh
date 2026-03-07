#!/bin/bash
# Quick start script for Log Whisperer

echo "🔊 Starting Log Whisperer..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "   Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
fi

# Check dependencies
echo "Checking dependencies..."
python3 -c "import anthropic" 2>/dev/null || {
    echo "⚠️  Installing Python dependencies..."
    pip install -r requirements.txt
}

# Start backend
echo "Starting backend on http://localhost:8000..."
python3 -m uvicorn server:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend
sleep 3

# Start frontend
echo "Starting frontend on http://localhost:5173..."
cd ui
npm install --silent 2>/dev/null
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Log Whisperer is running!"
echo ""
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
