import asyncio, os
os.environ["DEMO_MODE"] = "true"
os.environ["ANTHROPIC_API_KEY"] = "test"
from agents import decision_agent, writer_agent
from safety import ArgoSafetyGate
from data.load_incident import load_incident

def test_safety_gate():
    _, events = load_incident()
    fault = asyncio.run(decision_agent.run(events))
    plan  = asyncio.run(writer_agent.run(fault))
    gate  = ArgoSafetyGate()
    validated, results = asyncio.run(gate.validate_plan(plan))
    assert all(r.risk_score < 0.6 for r in results)
    print(f"\n✅ {len(results)} commands dry-run passed")
