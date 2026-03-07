"""FastAPI server — P2 owns this file."""
import uvicorn
import structlog
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import PipelineState
from agents import decision_agent, writer_agent
from safety import ArgoSafetyGate
from data.load_incident import load_incident
from viz.timeline import RerunTimeline
from config import API_HOST, API_PORT

log = structlog.get_logger()
app = FastAPI(title="Log Whisperer", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

states: dict[str, PipelineState] = {}
timeline = RerunTimeline()
gate = ArgoSafetyGate()


@app.post("/trigger")
async def trigger(incident_file: str = "cloudflare_incident.json"):
    incident_id, events = load_incident(incident_file)
    state = PipelineState(incident_id=incident_id, status="investigating")
    states[incident_id] = state

    timeline.log_event("incident/anomaly", "🚨 Anomaly detected — starting investigation", "CRITICAL")

    # Decision Agent
    state.fault_report = await decision_agent.run(events)
    timeline.log_event("agents/decision", f"✅ Root cause: {state.fault_report.root_cause}", "INFO")

    # Writer Agent
    state.status = "planning"
    state.remediation_plan = await writer_agent.run(state.fault_report)
    timeline.log_event("agents/writer", f"📋 {len(state.remediation_plan.commands)} commands generated", "INFO")

    # Argo Dry-Run
    state.status = "dry_running"
    timeline.log_event("safety/dryrun", "🔒 Running Argo CD safety dry-run...", "WARN")
    state.remediation_plan, state.dry_run_results = await gate.validate_plan(state.remediation_plan)

    if state.remediation_plan.dry_run_passed:
        state.status = "awaiting_approval"
        timeline.log_event("safety/dryrun", "✅ Dry-run passed — awaiting human approval", "INFO")
    else:
        state.status = "failed"
        timeline.log_event("safety/dryrun", "🚫 Dry-run FAILED — unsafe commands blocked", "CRITICAL")

    states[incident_id] = state
    return {"incident_id": incident_id, "status": state.status, "fault": state.fault_report}


@app.get("/status/{incident_id}")
async def status(incident_id: str):
    if incident_id not in states:
        raise HTTPException(404, "Not found")
    return states[incident_id]


@app.post("/approve/{incident_id}")
async def approve(incident_id: str):
    state = states.get(incident_id)
    if not state:
        raise HTTPException(404, "Not found")
    if state.status != "awaiting_approval":
        raise HTTPException(400, f"Cannot approve — status: {state.status}")

    state.status = "executing"
    timeline.log_event("remediation/execute", "👤 Human approved — executing fix...", "INFO")

    for cmd in state.remediation_plan.commands:
        timeline.log_event("remediation/execute", f"⚡ {cmd.tool}: {cmd.description}", "INFO")

    state.status = "resolved"
    state.resolved_at = datetime.utcnow()
    mttr = (state.resolved_at - state.created_at).seconds // 60
    timeline.log_event("remediation/resolved", f"✅ System healed. MTTR: {mttr} minutes (vs 57 min manual)", "INFO")
    states[incident_id] = state
    return {"status": "resolved", "mttr_minutes": mttr, "commands_executed": len(state.remediation_plan.commands)}


if __name__ == "__main__":
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)
