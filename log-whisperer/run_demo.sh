#!/bin/bash
# Simple launcher for the interactive demo

cd "$(dirname "$0")"

echo "🚀 Starting Log Whisperer Interactive Demo..."
echo ""

# Check if venv exists and activate it
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if dependencies are installed
if ! python3 -c "import rich" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing now..."
    pip3 install rich pydantic structlog
    echo ""
fi

python3 demo_interactive.py
