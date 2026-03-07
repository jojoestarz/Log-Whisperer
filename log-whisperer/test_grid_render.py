#!/usr/bin/env python3
"""
Test grid rendering without live updates
"""
import json
from viz.terminal_grid import render_grid
from rich.console import Console

console = Console()

print("Testing grid rendering...")
print("=" * 60)

# Test 1: All healthy
print("\nTest 1: All healthy (100 green nodes)")
state = ['healthy'] * 100
panel = render_grid(state)
console.print(panel)

# Test 2: Mixed states
print("\nTest 2: Mixed states")
state = ['healthy'] * 100
# Set some failed nodes
for i in [10, 11, 12, 20, 21, 22, 30, 31, 32]:
    state[i] = 'failed'
# Set some executing nodes
for i in [50, 51, 52]:
    state[i] = 'executing'
# Set some recovered nodes
for i in [80, 81, 82, 90, 91]:
    state[i] = 'recovered'

panel = render_grid(state)
console.print(panel)

# Test 3: Create state.json
print("\nTest 3: Creating state.json")
with open('state.json', 'w') as f:
    json.dump({'nodes': state}, f)
print("✓ state.json created with mixed states")

# Test 4: Read from state.json
print("\nTest 4: Reading from state.json")
with open('state.json', 'r') as f:
    data = json.load(f)
    loaded_state = data.get('nodes', [])
print(f"✓ Loaded {len(loaded_state)} nodes from state.json")

# Verify counts
healthy = loaded_state.count('healthy')
failed = loaded_state.count('failed')
executing = loaded_state.count('executing')
recovered = loaded_state.count('recovered')

print(f"\nStatistics:")
print(f"  Healthy: {healthy}")
print(f"  Failed: {failed}")
print(f"  Executing: {executing}")
print(f"  Recovered: {recovered}")
print(f"  Total: {len(loaded_state)}")

assert len(loaded_state) == 100, "Should have 100 nodes"
print("\n✓ All tests passed!")
