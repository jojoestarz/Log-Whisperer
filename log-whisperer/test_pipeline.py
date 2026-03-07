#!/usr/bin/env python3
"""Quick test script for the full pipeline"""
import asyncio
from agents.decision_agent import analyse, CACHED
from agents.writer_agent import generate_plan, CACHED_PLAN
from safety.argo_hook import run_argo_mock
from safety.sandbox_executor import run_sandbox

async def test():
    print("🔊 Log Whisperer Pipeline Test\n")
    
    # Load logs
    print("1. Loading incident logs...")
    logs = open("data/cloudflare_incident.json").read()
    print(f"   ✓ Loaded {len(logs)} bytes\n")
    
    # Decision Agent
    print("2. Running Decision Agent...")
    fault = analyse(logs)
    print(f"   ✓ Root cause: {fault.root_cause[:80]}...")
    print(f"   ✓ Confidence: {fault.confidence*100:.0f}%")
    print(f"   ✓ Affected services: {len(fault.affected_services)}\n")
    
    # Writer Agent
    print("3. Running Writer Agent...")
    plan = generate_plan(fault)
    print(f"   ✓ Generated {len(plan.commands)} commands:")
    for i, cmd in enumerate(plan.commands, 1):
        print(f"      {i}. {cmd}")
    print()
    
    # Safety layer
    print("4. Running safety checks...")
    plan = run_argo_mock(plan)
    print(f"   ✓ Argo mock - risk_score: {plan.risk_score}")
    print(f"   ✓ Dry-run passed: {plan.dry_run_passed}\n")
    
    violations = run_sandbox(plan)
    print(f"   ✓ Sandbox executor - {len(violations)} events generated")
    for v in violations:
        if v['type'] == 'sandbox_violation':
            print(f"      🔴 BLOCKED: {v['blocked']}")
        elif v['type'] == 'fix_executing':
            print(f"      🟢 ALLOWED: {v['target']}")
    
    print("\n✅ Pipeline test complete!")

if __name__ == "__main__":
    asyncio.run(test())
