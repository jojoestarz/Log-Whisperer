# 🤫 Log Whisperer

> Multi-agent incident remediation. AI diagnoses. AI proposes. Human approves. System heals.

## Overview
Log Whisperer ingests incident logs, performs root cause analysis via a Decision Agent, generates CLI remediation commands via a Writer Agent, dry-runs them through an Argo CD safety hook, visualises the full timeline in Rerun.io, and waits for human approval before executing.

## Quickstart

### Interactive Demo (Recommended)
```bash
cd log-whisperer
pip install -r requirements.txt
cp .env.example .env        # add your API keys

# Run the interactive demo
./run_demo.sh
# or
python3 demo_interactive.py
```

The interactive demo lets you choose the execution mode:
- **dry** - Preview mode (shows what would happen, no execution)
- **safe** - Safe mode (executes only low-risk commands)
- **full** - Full mode (executes all commands, real remediation)

### API Server
```bash
python api/main.py          # start the API server
# In another terminal:
python viz/timeline.py      # open Rerun viewer
# Trigger a demo incident:
curl -X POST http://localhost:8000/trigger
```

## Team
- P1 — Agent Engineer (Decision Agent, Writer Agent)
- P2 — Infrastructure Lead (MCP tools, Argo CD, API)
- P3 — Viz & Demo Lead (Rerun.io, demo flow, pitch)

## Architecture
```
Loki Anomaly → Council Agent → Writer Agent → Safety Gate → Terminal Grid → Human Approve → Execute
```

## Execution Modes

Log Whisperer supports three execution modes for safety and flexibility:

| Mode | Description | Executes Commands? | Use Case |
|------|-------------|-------------------|----------|
| **dry_run** | Preview mode | No | Testing, demos, validation |
| **safe** | Safe mode | Yes (low-risk only) | Controlled remediation |
| **full** | Full mode | Yes (all commands) | Production incidents |

Set the mode via:
- Interactive demo: Choose at runtime
- Environment: `EXECUTION_MODE=dry_run` in `.env`
- Code: `CommandExecutor(mode=ExecutionMode.FULL)`

## Features

- **Multi-Agent Debate**: Council of 3 specialized agents (Conservative SRE, Network Specialist, Chaos Engineer)
- **Real Execution**: Actual command execution with subprocess (git, kubectl, argocd)
- **Terminal Grid**: Real-time 10x10 infrastructure health visualization
- **Pretty Logging**: Rich console output with panels and syntax highlighting
- **WebSocket Streaming**: Stream execution to web UI
- **Safety Modes**: Three execution modes for different risk levels

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup and installation guide
- **[DEMO_QUICK_START.md](DEMO_QUICK_START.md)** - Quick demo guide with presentation tips
- **[INTERACTIVE_DEMO_SUMMARY.md](INTERACTIVE_DEMO_SUMMARY.md)** - Technical details of the interactive demo
- **[MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md)** - Guide for integrating MCP tools
- **[EXECUTION_IMPLEMENTATION_SUMMARY.md](EXECUTION_IMPLEMENTATION_SUMMARY.md)** - Real execution system details
