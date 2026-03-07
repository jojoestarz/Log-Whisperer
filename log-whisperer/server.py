"""FastAPI server with SSE streaming"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

event_queue: asyncio.Queue = asyncio.Queue()

# Import new visualization modules
from viz.cost_calculator import get_calculator, reset_calculator
from viz.confidence_tracker import get_tracker, reset_tracker
from simulator.incident_simulator import get_simulator


async def emit(event: dict):
    """Emit event to SSE stream"""
    await event_queue.put(json.dumps(event))


from pipeline import set_emit
set_emit(emit)


@app.post("/trigger")
async def trigger():
    """Start the pipeline"""
    from pipeline import run_pipeline
    
    # Reset calculators for new run
    reset_calculator()
    reset_tracker()
    
    # Start cost tracking
    calc = get_calculator()
    calc.start_incident()
    
    asyncio.create_task(run_pipeline())
    return {"status": "started"}

@app.post("/simulate")
async def simulate_incident():
    """Start live incident simulation"""
    sim = get_simulator()
    
    # Reset calculators
    reset_calculator()
    reset_tracker()
    
    calc = get_calculator()
    calc.start_incident()
    
    # Inject failure
    await emit({"type": "sim_start", "message": "🔥 Injecting BGP failure..."})
    await asyncio.sleep(0.5)
    
    snapshot = await sim.inject_bgp_failure()
    
    await emit({
        "type": "sim_incident",
        "services": snapshot["services"],
        "message": f"Incident active - {sum(1 for s in snapshot['services'].values() if s['status'] in ['critical', 'down'])} services affected"
    })
    
    # Now run the pipeline with simulated logs
    from pipeline import run_pipeline_with_logs
    asyncio.create_task(run_pipeline_with_logs(sim.get_logs_json()))
    
    return {"status": "simulating", "snapshot": snapshot}

@app.get("/cost/live")
async def get_live_cost():
    """Get real-time cost data"""
    calc = get_calculator()
    return calc.get_live_ticker_data()

@app.get("/confidence/chart")
async def get_confidence_chart():
    """Get confidence progression data"""
    tracker = get_tracker()
    return tracker.get_chart_data()


@app.get("/events")
async def events():
    """SSE endpoint for streaming events"""
    async def generator():
        while True:
            try:
                data = await asyncio.wait_for(event_queue.get(), timeout=30)
                yield {"data": data}
            except asyncio.TimeoutError:
                yield {"data": json.dumps({"type": "ping"})}
    
    return EventSourceResponse(generator())


@app.post("/approve")
async def approve():
    """Human approval endpoint"""
    calc = get_calculator()
    sim = get_simulator()
    
    await emit({
        "type": "fix_executing",
        "command": "argocd app rollback byoip-cleanup --staging --dry-run",
        "target": "staging",
        "message": "Executing approved fix on staging..."
    })
    await asyncio.sleep(1.2)
    
    # If simulation is active, heal services
    if sim.incident_active:
        heal_result = await sim.heal([
            "argocd app rollback byoip-cleanup --staging --dry-run",
            "kubectl get bgproutes -n edge | grep -c ESTABLISHED",
            "argocd app rollback byoip-cleanup --staging"
        ])
        
        # Emit service recovery updates
        await emit({
            "type": "sim_healing",
            "services": heal_result["services"],
            "message": "Services recovering..."
        })
    
    # Resolve incident and calculate final costs
    calc.resolve_incident()
    current_cost = calc.get_current_cost()
    comparison = calc.compare_mttr(57.0, current_cost["duration_minutes"])
    
    await emit({
        "type": "resolved",
        "mttr_seconds": current_cost["duration_seconds"],
        "total_cost": current_cost["total_cost"],
        "savings": comparison["savings"],
        "message": f"BGP routes restored. MTTR: {current_cost['duration_minutes']:.1f}m — saved ${comparison['savings']:,}"
    })
    
    return {"status": "executing", "cost": current_cost, "comparison": comparison}


@app.get("/status")
async def status():
    """Health check endpoint"""
    return {"status": "running", "queue_size": event_queue.qsize()}
