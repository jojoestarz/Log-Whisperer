"""
WebSocket endpoint example for streaming pipeline output.
Integrates stream_wrapper with FastAPI WebSocket.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

from api.stream_wrapper import stream_pipeline_to_websocket
from data.load_incident import load_cloudflare_incident

app = FastAPI(title="Log Whisperer WebSocket API")


@app.websocket("/ws/pipeline/{incident_id}")
async def pipeline_websocket(websocket: WebSocket, incident_id: str):
    """
    WebSocket endpoint for streaming pipeline execution.
    
    Streams Rich console output in real-time as ANSI text.
    
    Usage:
        ws = new WebSocket("ws://localhost:8000/ws/pipeline/incident-001");
        ws.onmessage = (event) => {
            // event.data contains ANSI-formatted text
            console.log(event.data);
        };
    """
    await websocket.accept()
    
    try:
        # Send initial message
        await websocket.send_json({
            "type": "status",
            "message": "Pipeline starting...",
            "incident_id": incident_id
        })
        
        # Load incident data (in production, load based on incident_id)
        log_events = load_cloudflare_incident()
        
        # Stream the pipeline execution
        # All Rich console output will be streamed to the WebSocket
        state = await stream_pipeline_to_websocket(
            websocket,
            incident_id=incident_id,
            log_events=log_events,
            enable_grid=False,  # Grid doesn't work over WebSocket
            enable_pretty_logs=True  # Enable pretty logging for rich output
        )
        
        # Send completion message
        await websocket.send_json({
            "type": "complete",
            "incident_id": state.incident_id,
            "status": state.status,
            "severity": state.fault_report.severity if state.fault_report else None,
            "confidence": state.fault_report.confidence if state.fault_report else None,
            "commands": len(state.remediation_plan.commands) if state.remediation_plan else 0
        })
        
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for incident {incident_id}")
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        raise


@app.get("/")
async def get_demo_page():
    """Demo HTML page with WebSocket client."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Log Whisperer - WebSocket Demo</title>
        <style>
            body {
                font-family: 'Courier New', monospace;
                background: #1e1e1e;
                color: #d4d4d4;
                padding: 20px;
            }
            #output {
                background: #000;
                padding: 20px;
                border-radius: 5px;
                min-height: 400px;
                white-space: pre-wrap;
                font-size: 14px;
                line-height: 1.5;
            }
            button {
                background: #007acc;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 0;
            }
            button:hover {
                background: #005a9e;
            }
            .status {
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                background: #2d2d30;
            }
        </style>
    </head>
    <body>
        <h1>🤫 Log Whisperer - WebSocket Stream</h1>
        <div class="status" id="status">Status: Ready</div>
        <button onclick="startPipeline()">Start Pipeline</button>
        <button onclick="clearOutput()">Clear Output</button>
        <div id="output"></div>
        
        <script>
            let ws = null;
            
            function startPipeline() {
                const output = document.getElementById('output');
                const status = document.getElementById('status');
                
                output.textContent = '';
                status.textContent = 'Status: Connecting...';
                
                // Connect to WebSocket
                ws = new WebSocket('ws://localhost:8000/ws/pipeline/demo-001');
                
                ws.onopen = () => {
                    status.textContent = 'Status: Connected - Pipeline running...';
                };
                
                ws.onmessage = (event) => {
                    try {
                        // Try to parse as JSON (status messages)
                        const data = JSON.parse(event.data);
                        if (data.type === 'complete') {
                            status.textContent = `Status: Complete - ${data.status} (${data.severity})`;
                        } else if (data.type === 'error') {
                            status.textContent = `Status: Error - ${data.message}`;
                        }
                    } catch {
                        // Not JSON, it's ANSI text output
                        output.textContent += event.data;
                        output.scrollTop = output.scrollHeight;
                    }
                };
                
                ws.onerror = (error) => {
                    status.textContent = 'Status: Error - Connection failed';
                    console.error('WebSocket error:', error);
                };
                
                ws.onclose = () => {
                    status.textContent = 'Status: Disconnected';
                };
            }
            
            function clearOutput() {
                document.getElementById('output').textContent = '';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    print("Starting WebSocket server...")
    print("Open http://localhost:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
