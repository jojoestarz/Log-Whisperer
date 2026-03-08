# 🤫 Log Whisperer

> Multi-agent incident remediation. AI diagnoses. AI proposes. Human approves. System heals.

## Quick Start (One Command)

```bash
cd log-whisperer
./run_demo.sh
```

This launches an interactive menu with all options. **That's the only command you need to know.**

## What You Get

A menu with 4 options:
1. **Full Pipeline** - Complete AI-powered incident remediation
2. **Quick Demo** - Test execution without AI (no API key needed)
3. **API Server** - Run as HTTP/WebSocket service
4. **Tests** - Verify system components

Choose an option, follow the prompts. Done!

## First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key (optional for quick demo)
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### Option 1: Interactive Menu (Recommended)
```bash
./run_demo.sh
```

### Option 2: Direct Python
```bash
python3 main.py
```

### Option 3: Specific Mode
```bash
# Full pipeline
python3 main.py  # Choose option 1

# Quick demo
python3 main.py  # Choose option 2

# API server
python3 main.py  # Choose option 3
```

## Architecture
```
Loki Anomaly → Council Agent → Writer Agent → Safety Gate → Terminal Grid → Human Approve → Execute
```

## Components

- **Council Agent** - Multi-agent debate (3 specialized agents)
- **Writer Agent** - Generates remediation commands
- **Executor** - Runs commands with safety modes (dry/safe/full)
- **Terminal Grid** - Real-time infrastructure visualization
- **API Server** - HTTP/WebSocket interface

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup and installation guide
- **[DEMO_QUICK_START.md](DEMO_QUICK_START.md)** - Quick demo guide with presentation tips
- **[INTERACTIVE_DEMO_SUMMARY.md](INTERACTIVE_DEMO_SUMMARY.md)** - Technical details of the interactive demo
- **[MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md)** - Guide for integrating MCP tools
- **[EXECUTION_IMPLEMENTATION_SUMMARY.md](EXECUTION_IMPLEMENTATION_SUMMARY.md)** - Real execution system details
