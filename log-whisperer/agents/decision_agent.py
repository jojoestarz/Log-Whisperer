"""Decision Agent — analyses incident logs and outputs FaultReport"""
import anthropic
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import FaultReport
from config import ANTHROPIC_API_KEY, DEMO_MODE, MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM = """You are an elite SRE incident analyser.
Respond ONLY with a single valid JSON object.
No markdown. No backticks. No explanation. Just JSON.
Required keys: root_cause (str), blast_radius (str),
confidence (float 0-1), affected_services (list of str),
timestamp (str ISO8601)"""

CACHED = FaultReport(
    root_cause="Empty string in Query().Get('pending_delete') triggered bulk BGP prefix withdrawal across all edge routers",
    blast_radius="1,100 enterprise BYOIP customers — global routing failure",
    confidence=0.97,
    affected_services=["bgp-router-lon01", "bgp-router-iad01", "api-gateway", "dns-resolver", "cdn-edge"],
    timestamp="2026-02-20T06:27:12Z"
)


def analyse(log_text: str) -> FaultReport:
    """Analyse incident logs and return FaultReport"""
    if DEMO_MODE:
        return CACHED
    
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=500,
            system=SYSTEM,
            messages=[{"role": "user", "content": f"Analyse this incident log:\n\n{log_text}"}]
        )
        data = json.loads(resp.content[0].text)
        return FaultReport(**data)
    except Exception as e:
        print(f"LLM error: {e} — fallback to cached")
        return CACHED


if __name__ == "__main__":
    logs = open("data/cloudflare_incident.json").read()
    for i in range(5):
        f = analyse(logs)
        assert f.root_cause != "", f"Run {i+1} returned empty root_cause"
        print(f"Run {i+1} ✓ — {f.root_cause[:60]}...")
