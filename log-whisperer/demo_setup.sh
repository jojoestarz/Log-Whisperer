#!/bin/bash
set -e

echo "🎬 Starting Log Whisperer Dual Demo..."
echo ""

# Dynamically read log count and set initial state to FAILED (red)
./venv/bin/python -c "
import json
try:
    logs = json.load(open('data/cloudflare_incident.json'))
    count = len(logs)
    print(f'📊 Detected {count} log events')
except:
    count = 9
    print('⚠️  Using default 9 nodes')

json.dump({'nodes': ['failed'] * count}, open('state.json', 'w'))
print('✅ Initial state: ALL NODES FAILED (red)')
"

echo ""
echo "🚀 Starting services..."

# Start SSE server
./venv/bin/uvicorn api.sse_server:app --port 3000 --host 0.0.0.0 > /dev/null 2>&1 &
SSE_PID=$!
echo "✅ SSE server running (PID: $SSE_PID)"

# Start terminal grid if available
if [ -f "viz/terminal_grid.py" ]; then
    ./venv/bin/python viz/terminal_grid.py > /dev/null 2>&1 &
    GRID_PID=$!
    echo "✅ Terminal grid running (PID: $GRID_PID)"
fi

sleep 2

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🎯 LOG WHISPERER - DUAL DEMO READY"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📍 Access Points:"
echo "   🌐 Browser:  http://localhost:3000"
echo "   🖥️  Terminal: Running in background"
echo ""
echo "🎮 Usage:"
echo "   1. Open browser: http://localhost:3000"
echo "   2. Run demo: ./venv/bin/python cli/main.py trigger --mode=demo"
echo "   3. Watch nodes heal from RED → GREEN!"
echo ""
echo "💡 Nodes start FAILED (red) and heal as pipeline processes"
echo ""
echo "🛑 To stop:"
echo "   kill $SSE_PID"
if [ ! -z "$GRID_PID" ]; then
    echo "   kill $GRID_PID"
fi
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait
