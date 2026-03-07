# Terminal Grid Usage Guide

## Overview

The terminal grid provides real-time visualization of infrastructure health using a 10x10 grid (100 nodes).

## Node States

- 🟢 **Healthy** (green █) - Node operating normally
- 🔴 **Failed** (red █) - Node experiencing issues
- 🟡 **Executing** (yellow █) - Remediation in progress
- 🔵 **Recovered** (blue █) - Node restored after incident

## Running the Grid

### Terminal 1: Start the Grid Monitor
```bash
cd log-whisperer
./venv/bin/python viz/terminal_grid.py
```

The grid will:
- Display a 10x10 grid of infrastructure nodes
- Read `state.json` every 0.5 seconds
- Update in real-time with 2 refreshes per second
- Show statistics: healthy, degraded, executing, recovered counts

### Terminal 2: Simulate an Incident
```bash
cd log-whisperer
./venv/bin/python test_grid_simulator.py
```

This will simulate a full incident lifecycle:
1. All systems healthy (100 green)
2. Incident detected (nodes turn red)
3. Cascading failures (more red nodes)
4. Remediation executing (yellow nodes)
5. Recovery in progress (blue nodes)
6. Full restoration (back to green)

## State File Format

`state.json`:
```json
{
  "nodes": [
    "healthy", "healthy", "failed", "executing", ...
  ]
}
```

- Must contain exactly 100 node states
- Valid states: "healthy", "failed", "executing", "recovered"

## Integration with Pipeline

The pipeline can update `state.json` to reflect:
- Affected services (failed nodes)
- Remediation execution (executing nodes)
- Recovery progress (recovered nodes)

Example integration in `api/pipeline.py`:
```python
import json

def update_grid_state(affected_services: list[str], status: str):
    """Update grid to show affected services."""
    state = ['healthy'] * 100
    
    # Map services to grid positions
    service_positions = {
        'bgp-router-lon01': [10, 11, 12],
        'bgp-router-iad01': [20, 21, 22],
        'api-gateway': [30, 31, 32],
        # ... more mappings
    }
    
    for service in affected_services:
        positions = service_positions.get(service, [])
        for pos in positions:
            state[pos] = status  # 'failed', 'executing', 'recovered'
    
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
```

## Testing

### Quick Test
```bash
./venv/bin/python test_grid_render.py
```

Shows static grid renders with different states.

### Live Test
1. Terminal 1: `./venv/bin/python viz/terminal_grid.py`
2. Terminal 2: `./venv/bin/python test_grid_simulator.py`
3. Watch the grid update in real-time!

## Keyboard Controls

- `Ctrl+C` - Stop the grid monitor

## Tips

- Run in a terminal with good color support
- Recommended terminal size: 80x30 or larger
- The grid updates every 0.5s, so changes appear quickly
- Statistics at the bottom show node counts by state
