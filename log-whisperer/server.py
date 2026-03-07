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


async def emit(event: dict):
    """Emit event to SSE stream"""
    await event_queue.put(json.dumps(event))


from pipeline import set_emit
set_emit(emit)


@app.post("/trigger")
async def trigger():
    """Start the pipeline"""
    from pipeline import run_pipeline
    asyncio.create_task(run_pipeline())
    return {"status": "started"}


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
    await emit({
        "type": "fix_executing",
        "command": "argocd app rollback byoip-cleanup --staging",
        "target": "staging",
        "message": "Executing approved fix on staging..."
    })
    await asyncio.sleep(1.5)
    
    await emit({
        "type": "resolved",
        "mttr_seconds": 252,
        "message": "BGP routes restored. MTTR: 4m 12s — baseline was 57:00"
    })
    
    return {"status": "executing"}


@app.get("/status")
async def status():
    """Health check endpoint"""
    return {"status": "running", "queue_size": event_queue.qsize()}
