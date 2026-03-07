#!/usr/bin/env python3
"""
Example usage of decision_agent.py
Demonstrates both DEMO_MODE and real API usage
"""
import os
from agents.decision_agent import analyze_logs

# Example 1: Using DEMO_MODE (cached response)
print("Example 1: DEMO_MODE")
print("-" * 60)
os.environ['DEMO_MODE'] = 'true'
report = analyze_logs('data/cloudflare_incident.json')
print(f"\nReturned: {report.severity} incident with {report.confidence:.0%} confidence\n")

# Example 2: Using real API (requires valid ANTHROPIC_API_KEY)
print("\nExample 2: Real API")
print("-" * 60)
os.environ['DEMO_MODE'] = 'false'
# Uncomment below and add your API key to test:
# os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-...'
# report = analyze_logs('data/cloudflare_incident.json')
print("Set ANTHROPIC_API_KEY in .env and set DEMO_MODE=false to test\n")
