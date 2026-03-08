# Log Whisperer Spatial Visualizer

Dynamic incident visualization that adapts to your log data.

## Features

✨ **Dynamic Node Count** - Automatically detects log count from `data/cloudflare_incident.json`  
🔴 **Incident State** - Nodes start RED (failed) and heal to GREEN (healthy)  
🌊 **Organic Layout** - Subtle randomized jitter creates loose, natural feel  
⚡ **Real-time Updates** - SSE streams state changes instantly  
🕸️ **Connected Web** - Subtle lines to center create spatial awareness  
🎨 **Dark Aesthetic** - #0b0f0e background, Space Mono font, glowing nodes

## Quick Start

```bash
cd log-whisperer
./demo_setup.sh
```

Then open http://localhost:3000 in your browser.

## Architecture

```
demo_setup.sh
    ↓
Reads data/cloudflare_incident.json
    ↓
Creates state.json with N failed nodes
    ↓
Starts SSE server (port 3000)
    ↓
Browser connects via /events
    ↓
Pipeline updates state.json
    ↓
Browser auto-updates (RED → GREEN)
```

## Files

### 1. `demo_setup.sh` (Launcher)
- Dynamically counts logs from `data/cloudflare_incident.json`
- Creates `state.json` with all nodes in `failed` state (RED)
- Starts SSE server on port 3000
- Starts terminal grid (if available)
- Provides usage instructions

### 2. `api/sse_server.py` (Backend)
- FastAPI SSE server
- Watches `state.json` for changes
- Streams updates to browser via `/events` endpoint
- Serves static UI from `ui/` directory
- Polls every 200ms for changes

### 3. `ui/index.html` (Frontend)
- Pure HTML/CSS/JS (no frameworks)
- Dynamic grid layout based on node count
- Smaller nodes (15% of cell size) with randomized jitter
- Subtle connection lines to center
- Color-coded states:
  - `failed`: #ff4d6d (RED)
  - `healthy`: #00e87a (GREEN)
  - `executing`: #f4a228 (ORANGE)
  - `recovered`: #4d8fff (BLUE)
- Live stats in top-right corner
- Click to cycle node states (for testing)

## Usage Workflow

### 1. Start Services
```bash
./demo_setup.sh
```

### 2. Open Browser
Navigate to http://localhost:3000

You'll see all nodes in RED (failed state).

### 3. Run Pipeline
```bash
./venv/bin/python cli/main.py trigger --mode=demo
```

Watch nodes heal from RED → GREEN as the pipeline processes!

### 4. Manual Testing
Click anywhere on the canvas to randomly cycle a node through states.

## Node States

| State | Color | Hex | Meaning |
|-------|-------|-----|---------|
| failed | Red | `#ff4d6d` | Active incident |
| executing | Orange | `#f4a228` | Remediation in progress |
| recovered | Blue | `#4d8fff` | Incident resolved |
| healthy | Green | `#00e87a` | Normal operation |

## Visual Design

### Organic Layout
- Nodes positioned in grid with randomized jitter (±60px)
- Creates loose, natural feel vs rigid grid
- Jitter is fixed per session (not animated)

### Smaller Nodes
- Node size: 15% of cell size (vs 30% in previous version)
- More breathing room
- Better for larger node counts

### Connection Web
- Subtle lines from each node to center
- Creates spatial awareness
- Very low opacity (3%) for subtlety

### Glow Effect
- Each node has colored shadow blur
- Intensity: 15px
- Matches node state color

## Dynamic Node Count

The visualizer automatically adapts to your log data:

```python
# demo_setup.sh reads actual log count
logs = json.load(open('data/cloudflare_incident.json'))
count = len(logs)  # e.g., 47 logs = 47 nodes

# Creates initial state
json.dump({'nodes': ['failed'] * count}, open('state.json', 'w'))
```

Grid layout calculates optimal rows/columns:
```javascript
const cols = Math.ceil(Math.sqrt(nodes.length));
const rows = Math.ceil(nodes.length / cols);
```

## Integration with Pipeline

The visualizer integrates seamlessly with the existing pipeline:

1. Pipeline processes logs
2. Updates `state.json` with new node states
3. SSE server detects file change
4. Streams update to browser
5. Browser redraws with new states

No changes to existing pipeline code required!

## Stopping Services

Press `Ctrl+C` in the terminal running `demo_setup.sh`, or:

```bash
pkill -f "sse_server"
pkill -f "terminal_grid"
```

## Customization

### Change Node Size
Edit `ui/index.html`:
```javascript
const size = Math.min(cellW, cellH) * 0.15; // Change 0.15 to 0.2 for larger
```

### Change Jitter Amount
Edit `ui/index.html`:
```javascript
x: (Math.random() - 0.5) * 60, // Change 60 to 100 for more jitter
```

### Change Colors
Edit `ui/index.html`:
```javascript
const colors = {
    'healthy': '#00e87a',  // Your color here
    'failed': '#ff4d6d',   // Your color here
    // ...
};
```

### Change Poll Rate
Edit `api/sse_server.py`:
```python
await asyncio.sleep(0.2)  # Change to 0.1 for faster updates
```

## Troubleshooting

**No nodes showing?**
- Check if `state.json` exists and has valid JSON
- Verify `data/cloudflare_incident.json` exists
- Check browser console for errors

**Nodes not updating?**
- Verify SSE connection in browser Network tab
- Check if `state.json` is being modified
- Ensure port 3000 is not blocked

**Wrong node count?**
- Verify `data/cloudflare_incident.json` has correct format
- Check `state.json` for actual node count
- Re-run `demo_setup.sh` to regenerate

## Demo Tips

1. **Open browser FIRST** before running pipeline
2. **Use DEMO_MODE=true** for cached responses (no API calls)
3. **Watch the healing** - nodes transition RED → ORANGE → BLUE → GREEN
4. **Click to test** - cycle individual nodes through states
5. **Perfect for presentations** - dynamic, organic, visually striking

## Comparison to Previous Version

| Feature | Previous | New |
|---------|----------|-----|
| Node count | Fixed 100 | Dynamic from logs |
| Initial state | Healthy (green) | Failed (red) |
| Node size | 30% of cell | 15% of cell |
| Layout | Rigid grid | Organic jitter |
| Connection lines | None | Subtle web to center |
| Visual feel | Structured | Loose, natural |

Enjoy the spatial visualizer! 🤫✨
