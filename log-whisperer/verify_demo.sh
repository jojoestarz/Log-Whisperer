#!/bin/bash
# Verify the interactive demo is ready to run

echo "🔍 Verifying Log Whisperer Interactive Demo..."
echo ""

# Check if demo file exists
if [ ! -f "demo_interactive.py" ]; then
    echo "❌ demo_interactive.py not found"
    exit 1
fi
echo "✓ demo_interactive.py exists"

# Check if it's executable
if [ -x "demo_interactive.py" ]; then
    echo "✓ demo_interactive.py is executable"
else
    echo "⚠ demo_interactive.py not executable (will use python3 directly)"
fi

# Check Python syntax
if python3 -m py_compile demo_interactive.py 2>/dev/null; then
    echo "✓ Python syntax is valid"
else
    echo "❌ Python syntax error"
    exit 1
fi

# Check if run_demo.sh exists
if [ -f "run_demo.sh" ]; then
    echo "✓ run_demo.sh exists"
    if [ -x "run_demo.sh" ]; then
        echo "✓ run_demo.sh is executable"
    fi
fi

# Check for required modules
echo ""
echo "Checking dependencies..."

check_module() {
    if python3 -c "import $1" 2>/dev/null; then
        echo "✓ $1"
        return 0
    else
        echo "❌ $1 (run: pip install $2)"
        return 1
    fi
}

all_good=true
check_module "rich" "rich" || all_good=false
check_module "pydantic" "pydantic" || all_good=false
check_module "structlog" "structlog" || all_good=false

echo ""
if [ "$all_good" = true ]; then
    echo "✅ All checks passed! Demo is ready to run."
    echo ""
    echo "Run the demo with:"
    echo "  ./run_demo.sh"
    echo "  or"
    echo "  python3 demo_interactive.py"
else
    echo "⚠ Some dependencies missing. Install with:"
    echo "  pip install -r requirements.txt"
    exit 1
fi
