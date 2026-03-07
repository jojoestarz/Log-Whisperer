#!/usr/bin/env python3
import os
os.environ['DEMO_MODE'] = 'true'

from agents.decision_agent import analyze_logs

print("Testing decision_agent.py...")
report = analyze_logs('data/cloudflare_incident.json')
print(f"Success! Severity: {report.severity}, Confidence: {report.confidence}")
