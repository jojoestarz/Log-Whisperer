# Stream Wrapper - Implementation Complete ✓

## Overview

Captures Rich console output to a buffer, streams it to WebSocket in real-time, and works with existing pipeline code unchanged through monkey-patching.

## Architecture

```
Pipeline (unchanged)
    ↓
Rich Console Output
    ↓
Monkey-Patched Console → StringIO Buffer
    ↓
Stream Wrapper → ANSI Output
    ↓
WebSocket Client
```

## Key Features

- ✓ Captures Rich console output without modifying existing code
- ✓ Temporarily monkey-patches global console objects
- ✓ Streams ANSI-formatted output to WebSocket
- ✓ Restores original console afterward
- ✓ Works with async functions
- ✓ Handles existing pipeline.py unchanged
- ✓ Preserves ANSI color codes and formatting

## Implementation

### Core Components

#### 1. ConsoleCapture Class

```python
class ConsoleCapture:
    def __init__(self):
        self.buffer = io.StringIO()
        self.console = Console(file=self.buffer, force_terminal=True)
        self.original_consoles = {}
    
    def patch_module_console(self, module, attr_name='console'):
        # Saves original and replaces with capturing console
        
    def restore_all(self):
        # Restores all patched consoles
```

#### 2. Context Manager

```python
@contextmanager
def capture_console_output():
    capture = ConsoleCapture()
    
    # Patch consoles in all modules
    from agents import council_agent
    from agents import writer_agent
    from viz import terminal_logger
    
    capture.patch_module_console(council_agent, 'console')
    capture.patch_module_console(writer_agent, 'console')
    capture.patch_module_console(terminal_logger, 'console')
    
    try:
        yield capture
    finally:
        capture.restore_all()
```

#### 3. WebSocket Streaming

```python
async def stream_to_websocket(websocket, async_func, *args, **kwargs):
    with capture_console_output() as capture:
        task = asyncio.create_task(async_func(*args, **kwargs))
        
        while not task.done():
            output = capture.get_output()
            if output:
                await websocket.send_text(output)
            await asyncio.sleep(0.1)
        
        # Get final output
        output = capture.get_output()
        if output:
            await websocket.send_text(output)
        
        return await task
```

## Usage

### 1. Basic Capture (Testing)

```python
from api.stream_wrapper import capture_output_sync

def my_function():
    console.print("[green]Hello[/green]")
    return 42

result, output = capture_output_sync(my_function)
print(f"Result: {result}")
print(f"Captured: {output}")
```

### 2. Async Capture (Testing)

```python
from api.stream_wrapper import capture_output_async

async def my_async_function():
    console.print("[green]Hello[/green]")
    return 42

result, output = await capture_output_async(my_async_function)
```

### 3. WebSocket Streaming

```python
from fastapi import WebSocket
from api.stream_wrapper import stream_pipeline_to_websocket
from data.load_incident import load_cloudflare_incident

@app.websocket("/ws/pipeline/{incident_id}")
async def pipeline_endpoint(websocket: WebSocket, incident_id: str):
    await websocket.accept()
    
    logs = load_cloudflare_incident()
    state = await stream_pipeline_to_websocket(
        websocket,
        incident_id=incident_id,
        log_events=logs
    )
    
    await websocket.send_json({
        "status": "complete",
        "severity": state.fault_report.severity
    })
```

### 4. Custom Function Streaming

```python
from api.stream_wrapper import stream_to_websocket

async def my_task():
    from viz.terminal_logger import log_event
    log_event("🚀", "START", "Task started", "green")
    # ... do work ...
    log_event("✅", "DONE", "Task completed", "green")
    return "result"

result = await stream_to_websocket(websocket, my_task)
```

## WebSocket Endpoint Example

Complete FastAPI endpoint in `api/websocket_endpoint.py`:

```python
from fastapi import FastAPI, WebSocket
from api.stream_wrapper import stream_pipeline_to_websocket

app = FastAPI()

@app.websocket("/ws/pipeline/{incident_id}")
async def pipeline_websocket(websocket: WebSocket, incident_id: str):
    await websocket.accept()
    
    # Stream pipeline execution
    state = await stream_pipeline_to_websocket(
        websocket,
        incident_id=incident_id,
        log_events=logs
    )
    
    # Send completion
    await websocket.send_json({
        "type": "complete",
        "status": state.status
    })
```

## Running the Demo

### Start WebSocket Server

```bash
cd log-whisperer
./venv/bin/python api/websocket_endpoint.py
```

### Open Browser

Navigate to: http://localhost:8000

Click "Start Pipeline" to see real-time streaming!

## How It Works

### 1. Monkey-Patching

```python
# Before patching
from viz.terminal_logger import console
console.print("Hello")  # Goes to stdout

# During capture
with capture_console_output() as capture:
    console.print("Hello")  # Goes to StringIO buffer

# After capture
console.print("Hello")  # Goes to stdout again
```

### 2. Module Patching

The wrapper patches console objects in:
- `agents.council_agent.console`
- `agents.writer_agent.console`
- `viz.terminal_logger.console`

### 3. Output Streaming

```
Rich Console → StringIO Buffer → Get Output → WebSocket
     ↓              ↓                ↓            ↓
  [green]Hi    "\\x1b[32mHi"    ANSI text   Client
```

## ANSI Output

The captured output includes ANSI escape codes:

```
\x1b[32m✓\x1b[0m Success
\x1b[31m✗\x1b[0m Error
\x1b[36m📥 INGESTING\x1b[0m
```

Clients can:
- Render ANSI codes (terminal emulators)
- Strip ANSI codes (plain text)
- Convert to HTML (ansi-to-html libraries)

## Testing

### Run Test Suite

```bash
./venv/bin/python test_stream_wrapper.py
```

Tests:
1. Basic console capture
2. Async console capture
3. Pipeline capture
4. Console restoration
5. Mock WebSocket streaming

### Manual Testing

```python
import asyncio
from api.stream_wrapper import capture_output_async

async def test():
    from viz.terminal_logger import log_event
    log_event("🎉", "TEST", "It works!", "green")
    return "done"

result, output = await capture_output_async(test)
print(output)  # Shows ANSI-formatted output
```

## Client-Side Integration

### JavaScript WebSocket Client

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/pipeline/demo-001');

ws.onmessage = (event) => {
    try {
        // JSON status messages
        const data = JSON.parse(event.data);
        console.log('Status:', data);
    } catch {
        // ANSI text output
        displayANSI(event.data);
    }
};
```

### ANSI Rendering

Use libraries like:
- `ansi-to-html` (npm)
- `xterm.js` (terminal emulator)
- `blessed-contrib` (Node.js)

## Benefits

### 1. No Code Changes Required

Existing pipeline code works unchanged:

```python
# This code doesn't need modification
from viz.terminal_logger import log_event
log_event("📥", "INGESTING", "Loading...", "cyan")
```

### 2. Real-Time Streaming

Output streams as it's generated, not after completion.

### 3. Preserves Formatting

ANSI codes preserved for rich terminal output.

### 4. Clean Restoration

Original console always restored, even on errors.

### 5. Flexible

Works with any async function that uses Rich console.

## Limitations

### 1. Grid Visualization

Terminal grid (`viz/terminal_grid.py`) doesn't work over WebSocket:
- Uses `rich.live.Live()` which requires terminal
- Set `enable_grid=False` for WebSocket

### 2. Interactive Input

Functions requiring `input()` won't work over WebSocket.

### 3. Module Import Timing

Modules must be imported before patching:
- Wrapper imports modules at capture time
- New modules after capture won't be patched

## Error Handling

### WebSocket Disconnect

```python
try:
    await websocket.send_text(output)
except Exception:
    # WebSocket closed, cancel task
    task.cancel()
    raise
```

### Console Restoration

```python
try:
    yield capture
finally:
    # Always restore, even on error
    capture.restore_all()
```

## Performance

- Minimal overhead (~0.1s polling interval)
- Buffer cleared after each read
- No memory leaks (StringIO cleared)
- Async-friendly (non-blocking)

## Validation

- ✓ No syntax errors (getDiagnostics clean)
- ✓ All imports successful
- ✓ Console capture working
- ✓ Console restoration working
- ✓ WebSocket streaming working
- ✓ Pipeline integration working
- ✓ ANSI codes preserved

## Files Created

- `api/stream_wrapper.py` - Core implementation
- `api/websocket_endpoint.py` - FastAPI WebSocket example
- `test_stream_wrapper.py` - Test suite

## Next Steps

1. Start the WebSocket server:
   ```bash
   python api/websocket_endpoint.py
   ```

2. Open http://localhost:8000

3. Click "Start Pipeline" to see streaming!

The pipeline output streams in real-time to your browser! 🚀
