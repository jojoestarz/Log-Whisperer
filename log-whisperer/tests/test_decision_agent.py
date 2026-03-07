import asyncio, os
os.environ["DEMO_MODE"] = "true"
os.environ["ANTHROPIC_API_KEY"] = "test"
from agents import decision_agent
from data.load_incident import load_incident

def test_decision_agent():
    _, events = load_incident()
    report = asyncio.run(decision_agent.run(events))
    assert report.severity == "P1"
    assert report.confidence > 0.5
    print(f"\n✅ {report.root_cause}")
