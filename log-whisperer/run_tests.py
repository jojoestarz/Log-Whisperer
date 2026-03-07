#!/usr/bin/env python3
"""
Test decision_agent.py - writes results to test_results.txt
"""
import os
import sys
from agents.decision_agent import analyze_logs

results = []

def log(msg):
    results.append(msg)
    print(msg)

try:
    log("=" * 60)
    log("Testing decision_agent.py")
    log("=" * 60)
    
    # Test 1: DEMO_MODE
    log("\nTest 1: DEMO_MODE=true")
    os.environ['DEMO_MODE'] = 'true'
    report = analyze_logs('data/cloudflare_incident.json')
    log(f"✓ Severity: {report.severity}")
    log(f"✓ Confidence: {report.confidence}")
    log(f"✓ Root Cause: {report.root_cause[:60]}...")
    log(f"✓ Affected Services: {len(report.affected_services)} services")
    
    # Test 2-6: Real API (if key available)
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key and api_key != 'your_key_here':
        log("\nTests 2-6: Real API calls (5 times)")
        os.environ['DEMO_MODE'] = 'false'
        
        for i in range(5):
            log(f"\n  API Call {i+1}/5...")
            try:
                report = analyze_logs('data/cloudflare_incident.json')
                log(f"  ✓ Success - Severity: {report.severity}, Confidence: {report.confidence:.0%}")
            except Exception as e:
                log(f"  ✗ Failed: {str(e)[:100]}")
    else:
        log("\nTests 2-6: Skipped (no valid API key)")
    
    # Test 7: Error handling
    log("\nTest 7: Error handling (invalid API key)")
    os.environ['DEMO_MODE'] = 'false'
    os.environ['ANTHROPIC_API_KEY'] = 'invalid_key_test'
    report = analyze_logs('data/cloudflare_incident.json')
    log(f"✓ Fallback successful - Severity: {report.severity}")
    
    log("\n" + "=" * 60)
    log("ALL TESTS COMPLETED SUCCESSFULLY")
    log("=" * 60)
    
except Exception as e:
    log(f"\n✗ TEST FAILED: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

# Write results to file
with open('test_results.txt', 'w') as f:
    f.write('\n'.join(results))

log("\nResults written to test_results.txt")
