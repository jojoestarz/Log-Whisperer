#!/bin/bash
# Test SSE event stream

echo "Testing SSE event stream..."
echo "Connecting to http://localhost:8000/events"
echo ""

# Start listening to events in background
curl -N -H "Accept: text/event-stream" http://localhost:8000/events &
SSE_PID=$!

sleep 2

# Trigger the simulation
echo ""
echo "Triggering simulation..."
curl -X POST http://localhost:8000/simulate
echo ""

# Wait for events
sleep 5

# Kill the SSE connection
kill $SSE_PID 2>/dev/null

echo ""
echo "Test complete"
