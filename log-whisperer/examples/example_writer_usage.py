#!/usr/bin/env python3
"""
Example usage of writer_agent.py
Shows how to generate remediation plans from fault reports
"""
import os
from agents.writer_agent import generate_plan
from models import FaultReport

# Set DEMO_MODE
os.environ['DEMO_MODE'] = 'true'

# Create a fault report (typically from decision_agent)
fault = FaultReport(
    root_cause="Empty-string config in BGP deployment 4821 triggered bulk route withdrawal",
    affected_services=["bgp-router-lon01", "bgp-router-iad01", "api-gateway", "dns-resolver", "cdn-edge"],
    severity="P1",
    fix_type="config_rollback",
    confidence=0.97,
    summary="BGP config 4821 with empty prefix list caused cascading route withdrawal",
    time_of_failure="2022-06-21T06:27:12Z"
)

print("Generating remediation plan...")
print("-" * 60)

# Generate plan
plan = generate_plan(fault)

print(f"\nGenerated plan with {len(plan.commands)} commands")
print(f"Plan ID: {plan.plan_id}")
print(f"Risk: {plan.overall_risk}")
print(f"Estimated recovery: {plan.estimated_recovery_mins} minutes")

# Show the actual bash commands that would be generated
print("\nCommands to execute:")
for i, cmd in enumerate(plan.commands, 1):
    print(f"{i}. {cmd.tool}: {cmd.description}")
