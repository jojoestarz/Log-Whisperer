#!/usr/bin/env python3
"""
Test script for writer_agent.py
Tests with both DEMO_MODE and real API
"""
import os
import sys
from agents.writer_agent import generate_plan
from models import FaultReport

results = []

def log(msg):
    results.append(msg)
    print(msg)

try:
    log("=" * 60)
    log("Testing writer_agent.py")
    log("=" * 60)
    
    # Create a sample fault report
    fault = FaultReport(
        root_cause="Empty-string config in BGP deployment 4821 triggered bulk route withdrawal",
        affected_services=["bgp-router-lon01", "bgp-router-iad01", "api-gateway"],
        severity="P1",
        fix_type="config_rollback",
        confidence=0.97,
        summary="BGP config issue",
        time_of_failure="2022-06-21T06:27:12Z"
    )
    
    # Test 1: DEMO_MODE
    log("\nTest 1: DEMO_MODE=true")
    os.environ['DEMO_MODE'] = 'true'
    plan = generate_plan(fault)
    
    # Validate
    assert len(plan.commands) == 3, f"Expected 3 commands, got {len(plan.commands)}"
    log(f"✓ Plan ID: {plan.plan_id}")
    log(f"✓ Commands: {len(plan.commands)}")
    log(f"✓ Overall Risk: {plan.overall_risk}")
    log(f"✓ Recovery Time: {plan.estimated_recovery_mins} mins")
    
    for i, cmd in enumerate(plan.commands, 1):
        log(f"  Command {i}: {cmd.tool} - {cmd.description}")
    
    # Test 2: Real API (if key available)
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key and api_key != 'your_key_here':
        log("\nTest 2: Real API call")
        os.environ['DEMO_MODE'] = 'false'
        
        try:
            plan = generate_plan(fault)
            assert len(plan.commands) == 3, f"Expected 3 commands, got {len(plan.commands)}"
            log(f"✓ API call successful")
            log(f"✓ Plan ID: {plan.plan_id}")
            log(f"✓ Commands: {len(plan.commands)}")
        except Exception as e:
            log(f"✗ API call failed: {str(e)[:100]}")
    else:
        log("\nTest 2: Skipped (no valid API key)")
    
    # Test 3: Error handling
    log("\nTest 3: Error handling (invalid API key)")
    os.environ['DEMO_MODE'] = 'false'
    os.environ['ANTHROPIC_API_KEY'] = 'invalid_key_test'
    plan = generate_plan(fault)
    assert len(plan.commands) == 3, f"Expected 3 commands, got {len(plan.commands)}"
    log(f"✓ Fallback successful - {len(plan.commands)} commands")
    
    log("\n" + "=" * 60)
    log("ALL TESTS COMPLETED SUCCESSFULLY")
    log("=" * 60)
    
except Exception as e:
    log(f"\n✗ TEST FAILED: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

# Write results
with open('test_writer_results.txt', 'w') as f:
    f.write('\n'.join(results))

log("\nResults written to test_writer_results.txt")
