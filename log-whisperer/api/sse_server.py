"""
SSE Server for Log Whisperer Spatial Visualizer
Streams state.json changes to browser clients
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os

app = FastAPI(title="Log Whisperer Spatial Visualizer")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static UI files
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")


@app.get("/events")
async def sse_events():
    """SSE endpoint - streams state.json changes to browser"""
    
    async def generate():
        last_mtime = 0
        
        while True:
            try:
                if os.path.exists('state.json'):
                    mtime = os.path.getmtime('state.json')
                    
                    if mtime > last_mtime:
                        with open('state.json') as f:
                            state = json.load(f)
                        
                        yield f"data: {json.dumps(state)}\n\n"
                        last_mtime = mtime
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            await asyncio.sleep(0.2)
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
