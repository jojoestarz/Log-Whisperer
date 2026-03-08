# How to Run the Interactive Demo

## Quick Start

### Option 1: Use the launcher script (Recommended)
```bash
cd log-whisperer
./run_demo.sh
```

The script will automatically:
- Activate the virtual environment if it exists
- Install dependencies if needed
- Run the demo

### Option 2: Manual with virtual environment
```bash
cd log-whisperer
source venv/bin/activate
python3 demo_interactive.py
```

### Option 3: Install dependencies globally
```bash
cd log-whisperer
pip3 install rich pydantic structlog
python3 demo_interactive.py
```

## What to Expect

1. **Mode Selection Menu** - Type `dry`, `safe`, or `full` then press Enter
   - Don't use arrow keys or mouse
   - Just type the mode name
   - Press Enter to confirm
   - Default is `dry` if you just press Enter
2. **Scenario Setup** - Creates a test git repository
3. **Broken Config** - Shows the incident
4. **Remediation** - Executes based on your mode
5. **Verification** - Shows before/after results
6. **Cleanup** - Removes test directory

## How to Select Mode

When you see:
```
Select execution mode [dry/safe/full] (dry):
```

**Just type the mode name and press Enter:**
- Type `dry` and press Enter (or just press Enter for default)
- Type `safe` and press Enter
- Type `full` and press Enter

**Don't use arrow keys or mouse** - they won't work. Just type!

## Execution Modes

- **dry** - Preview only (safe, no execution)
- **safe** - Execute low-risk commands only
- **full** - Execute all commands (real fix)

## Troubleshooting

### "No module named 'rich'"
```bash
# Activate venv first
source venv/bin/activate
python3 demo_interactive.py
```

Or install globally:
```bash
pip3 install rich pydantic structlog
```

### "Permission denied"
```bash
chmod +x run_demo.sh
./run_demo.sh
```

### "Git not found"
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git
```

## Tips

- Start with **dry** mode to see what happens
- Try **full** mode to see real execution
- The demo creates a temporary directory and cleans up automatically
- Press Ctrl+C to exit at any time

Enjoy! 🚀
