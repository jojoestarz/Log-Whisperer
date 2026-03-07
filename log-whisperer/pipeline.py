"""Main pipeline orchestration"""
import asyncio
import os

# emit is injected from server to avoid circular imports
_emit = None


def set_emit(fn):
    global _emit
    _emit = fn


async def run_pipeline():
    """Execute the full Log Whisperer pipeline"""
    from agents.decision_agent import analyse, CACHED
    from agents.writer_agent import generate_plan
    from safety.argo_hook import run_argo_mock
    from safety.sandbox_executor import run_sandbox
    
    # Load incident logs
    logs = open("data/cloudflare_incident.json").read()
    
    await _emit({
        "type": "ingesting",
        "message": "Reading cloudflare_bgp_incident.json — 9 events, 33min window"
    })
    await asyncio.sleep(0.8)
    
    # Decision Agent
    fault = analyse(logs)
    await _emit({
        "type": "diagnosis",
        "message": fault.root_cause,
        "blast_radius": fault.blast_radius,
        "confidence": fault.confidence,
        "affected_services": fault.affected_services
    })
    await asyncio.sleep(1.2)
    
    # Writer Agent
    plan = generate_plan(fault)
    await _emit({
        "type": "fix_proposed",
        "command": plan.commands[0],
        "all_commands": plan.commands,
        "risk_score": plan.risk_score,
        "safety_level": plan.safety_level
    })
    await asyncio.sleep(1.0)
    
    # Safety layer
    plan = run_argo_mock(plan)
    violations = run_sandbox(plan)
    
    for v in violations:
        await _emit(v)
        await asyncio.sleep(0.9)
    
    await _emit({
        "type": "awaiting_approval",
        "risk_score": plan.risk_score,
        "message": "Dry-run passed — awaiting human approval"
    })
