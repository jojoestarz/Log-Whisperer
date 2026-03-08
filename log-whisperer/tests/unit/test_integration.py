#!/usr/bin/env python3
"""
Integration test: Decision Agent → Writer Agent
Shows the full pipeline flow
"""
import os
os.environ['DEMO_MODE'] = 'true'

from agents.decision_agent import analyze_logs
from agents.writer_agent import generate_plan

print("=" * 70)
print("INTEGRATION TEST: Decision Agent → Writer Agent")
print("=" * 70)

# Step 1: Decision Agent analyzes logs
print("\n[STEP 1] Decision Agent analyzing incident logs...")
print("-" * 70)
fault_report = analyze_logs('data/cloudflare_incident.json')

print(f"\n✓ Fault Report Generated:")
print(f"  - Root Cause: {fault_report.root_cause[:60]}...")
print(f"  - Severity: {fault_report.severity}")
print(f"  - Confidence: {fault_report.confidence:.0%}")
print(f"  - Affected Services: {len(fault_report.affected_services)}")

# Step 2: Writer Agent generates remediation plan
print("\n[STEP 2] Writer Agent generating remediation plan...")
print("-" * 70)
remediation_plan = generate_plan(fault_report)

print(f"\n✓ Remediation Plan Generated:")
print(f"  - Plan ID: {remediation_plan.plan_id}")
print(f"  - Commands: {len(remediation_plan.commands)}")
print(f"  - Overall Risk: {remediation_plan.overall_risk}")
print(f"  - Recovery Time: {remediation_plan.estimated_recovery_mins} mins")

# Validate
assert len(remediation_plan.commands) == 3, "Must have exactly 3 commands"

print("\n" + "=" * 70)
print("✓ INTEGRATION TEST PASSED")
print("=" * 70)

# Write summary
with open('integration_test_results.txt', 'w') as f:
    f.write("Integration Test Results\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Fault Report:\n")
    f.write(f"  Root Cause: {fault_report.root_cause}\n")
    f.write(f"  Severity: {fault_report.severity}\n")
    f.write(f"  Confidence: {fault_report.confidence:.0%}\n\n")
    f.write(f"Remediation Plan:\n")
    f.write(f"  Plan ID: {remediation_plan.plan_id}\n")
    f.write(f"  Commands: {len(remediation_plan.commands)}\n")
    f.write(f"  Risk: {remediation_plan.overall_risk}\n")
    f.write(f"  Recovery: {remediation_plan.estimated_recovery_mins} mins\n\n")
    f.write("Commands:\n")
    for i, cmd in enumerate(remediation_plan.commands, 1):
        f.write(f"  {i}. {cmd.tool}: {cmd.description}\n")
    f.write("\n✓ All tests passed\n")

print("\nResults written to integration_test_results.txt")
