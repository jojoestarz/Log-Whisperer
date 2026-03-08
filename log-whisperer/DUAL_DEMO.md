# Log Whisperer Dual Demo

Simultaneous CLI terminal grid + browser spatial visualizer.

## Quick Start

```bash
# One command to launch everything
./demo_setup.sh
```

Then open http://localhost:3000 in your browser.

## What You Get

### 1. Browser Spatializer (http://localhost:3000)
- **10x10 interactive grid** with glowing nodes
- **Real-time updates** via Server-Sent Events
- **Click nodes** to cycle states: healthy → failed → executing → recovered
- **Live stats** in top-right corner
- **Dark aesthetic** matching the vibe (#0b0f0e background, Space Mono font)

### 2. Terminal Grid (Background)
- ASCII visualization in terminal
- Updates from same `state.json`
- Runs alongside browser view

### 3. SSE Server (Port 3000)
- Watches `state.json` for changes
- Streams updates to browser clients
- Serves static UI files
- **No pipeline logic** - just a viewer

## Architecture

```
┌─────────────────┐
│   main.py       │  Run pipeline
│   or CLI        │  Updates state.json
└────────┬────────┘
         │
         ▼
    state.json ◄──────┐
         │            │
         ├────────────┤
         ▼            ▼
┌──────────────┐ ┌──────────────┐
│ Terminal     │ │ SSE Server   │
│ Grid         │ │ (Port 3000)  │
│ (ASCII)      │ │              │
└──────────────┘ └──────┬───────┘
                        │
                        ▼ SSE /events
                 ┌──────────────┐
                 │   Browser    │
                 │   (Canvas)   │
                 └──────────────┘
```

## Files Created

1. **`api/sse_server.py`** (85 lines)
   - FastAPI SSE server
   - `/events` endpoint streams state.json changes
   - Serves `ui/` static files
   - No pipeline logic

2. **`ui/index.html`** (95 lines)
   - Pure HTML/CSS/JS (no frameworks)
   - Canvas-based 10x10 grid
   - SSE client for live updates
   - Interactive node clicking

3. **`demo_setup.sh`** (60 lines)
   - One-command launcher
   - Creates initial state.json
   - Starts SSE server + terminal grid
   - Shows usage instructions

## Usage Workflow

### Option 1: Main Pipeline
```bash
./demo_setup.sh
# Open http://localhost:3000
./venv/bin/python main.py
# Select option 1 (Full Pipeline)
# Watch both visualizers update!
```

### Option 2: CLI Trigger
```bash
./demo_setup.sh
# Open http://localhost:3000
./venv/bin/python cli/main.py trigger --mode=demo
# Both visualizers update from state.json
```

### Option 3: Manual Testing
```bash
./demo_setup.sh
# Open http://localhost:3000
# Click nodes in browser to change states
# Or edit state.json manually
# Both views update automatically
```

## Color Scheme

| State | Color | Hex |
|-------|-------|-----|
| Healthy | Green | `#00e87a` |
| Failed | Red | `#ff4d6d` |
| Executing | Orange | `#f4a228` |
| Recovered | Blue | `#4d8fff` |

## Features

✅ **No existing code modified** - All new files  
✅ **Real-time sync** - Both views watch same state.json  
✅ **Interactive** - Click browser nodes to change states  
✅ **Presentation-ready** - Dark aesthetic with glowing effects  
✅ **Simple** - No React, no build step, pure HTML/JS  
✅ **Fast** - SSE polling every 500ms  

## Stopping Services

```bash
# Kill processes shown in demo_setup.sh output
kill <SSE_PID>
kill <GRID_PID>

# Or just:
pkill -f "sse_server"
pkill -f "terminal_grid"
```

## Customization

### Change Grid Size
Edit `ui/index.html`:
```javascript
const GRID = 10; // Change to 20 for 20x20
```

### Change Colors
Edit `ui/index.html`:
```javascript
const COLORS = {
    healthy: '#00e87a',    // Your color here
    failed: '#ff4d6d',     // Your color here
    // ...
};
```

### Change Poll Rate
Edit `api/sse_server.py`:
```python
await asyncio.sleep(0.5)  # Change to 0.1 for faster updates
```

## Troubleshooting

**Browser not updating?**
- Check http://localhost:3000/state returns JSON
- Check browser console for SSE errors
- Verify state.json exists and is valid JSON

**Terminal grid not showing?**
- Check if `viz/terminal_grid.py` exists
- Run manually: `./venv/bin/python viz/terminal_grid.py`

**Port 3000 already in use?**
- Edit `demo_setup.sh` and change `--port 3000` to another port
- Update browser URL accordingly

## Demo Tips

1. **Open browser FIRST** before running pipeline
2. **Use DEMO_MODE=true** for cached responses (no API calls)
3. **Click nodes** in browser to simulate failures
4. **Watch both views** update simultaneously
5. **Perfect for presentations** - dual visualization is impressive!

## Integration with Existing System

This dual demo integrates seamlessly:
- Uses existing `state.json` format
- Works with existing pipeline
- No changes to council_agent.py, pipeline.py, etc.
- Bonus visualization layer on top of existing CLI

Enjoy the dual demo! 🤫✨
