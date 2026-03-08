# Log Whisperer - Setup Guide

## Quick Setup

### 1. Install Dependencies

```bash
cd log-whisperer
pip install -r requirements.txt
```

Or if you prefer using a virtual environment:

```bash
cd log-whisperer
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the Interactive Demo

```bash
./run_demo.sh
```

Or directly:

```bash
python3 demo_interactive.py
```

## What the Demo Does

The interactive demo:

1. **Asks you to choose an execution mode**:
   - `dry` - Preview mode (no execution)
   - `safe` - Safe mode (low-risk commands only)
   - `full` - Full mode (all commands)

2. **Creates a real git repository** with a broken config

3. **Simulates an incident**: BGP config deployment breaks production

4. **Generates remediation**: Creates a `git revert` command

5. **Executes based on your mode**:
   - Dry: Shows preview only
   - Safe/Full: Actually executes the command

6. **Shows verification**: Before/after comparison, git history

7. **Cleans up**: Removes the demo directory

## Execution Modes

| Mode | Executes? | Use Case |
|------|-----------|----------|
| `dry` | No | Testing, validation, safe demos |
| `safe` | Yes (low-risk) | Controlled remediation |
| `full` | Yes (all) | Production incidents |

## Requirements

- Python 3.10+
- Git (for demo execution)
- Dependencies from requirements.txt:
  - `rich` - Terminal UI
  - `pydantic` - Data models
  - `structlog` - Logging
  - `anthropic` - AI agents (for full pipeline)

## Troubleshooting

### "Module not found" errors

```bash
pip install -r requirements.txt
```

### "Git not found" errors

Install git:
```bash
# Ubuntu/Debian
sudo apt-get install git

# macOS
brew install git

# Windows
# Download from https://git-scm.com/
```

### Permission denied

```bash
chmod +x run_demo.sh
chmod +x demo_interactive.py
```

### Virtual environment issues

```bash
# Deactivate current venv
deactivate

# Create fresh venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Other Demos

After setup, try these other demos:

```bash
# Council agent debate
python3 demo_council_debate.py

# Full pipeline with visualization
python3 demo_pretty_pipeline.py

# Real execution comparison
python3 demo_real_execution.py
```

## Running Tests

```bash
# Test the executor
python3 test_real_execution.py

# Test council agent
python3 test_council_agent.py

# Test writer agent
python3 test_writer_agent.py
```

## API Server

To run the full API server:

```bash
python3 api/main.py
```

Then in another terminal:

```bash
# Trigger an incident
curl -X POST http://localhost:8000/trigger
```

## Next Steps

- Read `DEMO_QUICK_START.md` for presentation tips
- Read `MCP_INTEGRATION_GUIDE.md` for MCP tools
- Read `README.md` for architecture overview
