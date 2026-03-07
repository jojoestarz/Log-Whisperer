"""
Decision Agent — P1 owns this file.
Ingests log events, calls Claude, returns a structured FaultReport.
"""
import json
import structlog
from anthropic import Anthropic
from models import FaultReport, LogEvent
from config import ANTHROPIC_API_KEY, DEMO_MODE, MODEL

log = structlog.get_logger()
client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """
You are an expert SRE with 15 years of experience diagnosing infrastructure incidents.
Analyse the logs and respond ONLY with a valid JSON object:
{
  "root_cause": "one sentence describing the exact cause",
  "affected_services": ["service1", "service2"],
  "severity": "P1" | "P2" | "P3",
  "fix_type": "config_rollback" | "service_restart" | "route_fix" | "cert_renewal" | "scale_up",
  "confidence": 0.0-1.0,
  "summary": "2-3 sentence human-readable summary",
  "time_of_failure": "ISO timestamp of the root cause event"
}
"""

CACHED_FAULT_REPORT = FaultReport(
    root_cause="BGP config push #4821 contained an empty-string prefix list, causing all edge routers to withdraw their routes",
    affected_services=["bgp-router-lon01","bgp-router-iad01","api-gateway","dns-resolver","cdn-edge"],
    severity="P1",
    fix_type="config_rollback",
    confidence=0.97,
    summary="A misconfigured BGP update (#4821) with an empty prefix list was deployed at 06:27 UTC. This caused cascading route withdrawal across all PoPs. A config rollback to commit #4820 will restore all routes.",
    time_of_failure="2022-06-21T06:27:12Z"
)


async def run(events: list[LogEvent]) -> FaultReport:
    if DEMO_MODE:
        log.info("decision_agent.demo_mode")
        return CACHED_FAULT_REPORT

    log.info("decision_agent.start", event_count=len(events))
    events_text = "\n".join([f"[{e.timestamp}] [{e.level}] {e.service}: {e.msg}" for e in events])

    response = client.messages.create(
        model=MODEL, max_tokens=1000, system=SYSTEM_PROMPT,
        messages=[{"role":"user","content":f"Analyse these incident logs:\n\n{events_text}"}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    report = FaultReport(**json.loads(raw))
    log.info("decision_agent.complete", severity=report.severity, confidence=report.confidence)
    return report
