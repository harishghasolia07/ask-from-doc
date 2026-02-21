#!/bin/bash

echo "🔄 Restarting servers with updated configuration..."
echo ""

# Kill existing servers
echo "⏹️  Stopping existing servers..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# Start backend
echo "🐍 Starting Python backend..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Test backend
echo "🧪 Testing backend..."
curl -s http://localhost:8000/health | python3 -m json.tool | head -5

# Start frontend
echo ""
echo "⚛️  Starting React frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
cd ..

echo ""
echo "✅ Servers started!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3001"
echo ""
echo "To stop servers:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
