# 🤫 Log Whisperer

> Multi-agent incident remediation. AI diagnoses. AI proposes. Human approves. System heals.

## Overview
Log Whisperer ingests incident logs, performs root cause analysis via a Decision Agent, generates CLI remediation commands via a Writer Agent, dry-runs them through an Argo CD safety hook, visualises the full timeline in Rerun.io, and waits for human approval before executing.

## Quickstart
```bash
pip install -r requirements.txt
cp .env.example .env        # add your API keys
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
Loki Anomaly → Decision Agent → Writer Agent → Argo Dry-Run → Rerun Timeline → Human Approve → Execute
```
