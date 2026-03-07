"""End-to-end pipeline test."""
import asyncio, os
os.environ["DEMO_MODE"] = "true"
os.environ["ANTHROPIC_API_KEY"] = "test"

from agents import decision_agent, writer_agent
from safety import ArgoSafetyGate
from data.load_incident import load_incident

def test_full_pipeline():
    incident_id, events = load_incident()
    fault   = asyncio.run(decision_agent.run(events))
    plan    = asyncio.run(writer_agent.run(fault))
    gate    = ArgoSafetyGate()
    validated, results = asyncio.run(gate.validate_plan(plan))

    assert fault.severity == "P1"
    assert len(plan.commands) > 0
    assert validated.dry_run_passed
    print(f"\n✅ Pipeline passed | MTTR est: {plan.estimated_recovery_mins}min")
