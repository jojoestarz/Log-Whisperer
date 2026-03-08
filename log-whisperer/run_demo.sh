#!/bin/bash
# Log Whisperer - Main Launcher

cd "$(dirname "$0")"

echo "🤫 Log Whisperer"
echo ""

# Check if venv exists and activate it
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if dependencies are installed
if ! python3 -c "import rich" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -q rich pydantic structlog anthropic fastapi uvicorn
    echo ""
fi

# Run main application
python3 main.py
