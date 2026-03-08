#!/usr/bin/env python3
"""
Grid simulator - updates state.json to test the terminal grid
Run this in one terminal, and viz/terminal_grid.py in another
"""
import json
import time
import random

def simulate_incident():
    """Simulate an infrastructure incident with state changes."""
    
    # Initial: all healthy
    state = ['healthy'] * 100
    
    print("Simulating infrastructure incident...")
    print("Run 'python viz/terminal_grid.py' in another terminal to watch")
    print()
    
    # Phase 1: Initial state (all healthy)
    print("Phase 1: All systems healthy")
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    time.sleep(2)
    
    # Phase 2: Incident starts - some nodes fail
    print("Phase 2: Incident detected - nodes failing")
    failed_nodes = random.sample(range(100), 15)  # 15 random nodes fail
    for idx in failed_nodes:
        state[idx] = 'failed'
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    time.sleep(3)
    
    # Phase 3: More cascading failures
    print("Phase 3: Cascading failures")
    additional_failures = random.sample([i for i in range(100) if state[i] == 'healthy'], 10)
    for idx in additional_failures:
        state[idx] = 'failed'
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    time.sleep(3)
    
    # Phase 4: Remediation executing
    print("Phase 4: Executing remediation commands")
    executing_nodes = [i for i in range(100) if state[i] == 'failed'][:10]
    for idx in executing_nodes:
        state[idx] = 'executing'
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    time.sleep(3)
    
    # Phase 5: Recovery in progress
    print("Phase 5: Nodes recovering")
    for idx in executing_nodes:
        state[idx] = 'recovered'
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    time.sleep(2)
    
    # Phase 6: More nodes recovering
    print("Phase 6: Full recovery")
    remaining_failed = [i for i in range(100) if state[i] == 'failed']
    for idx in remaining_failed:
        state[idx] = 'recovered'
        with open('state.json', 'w') as f:
            json.dump({'nodes': state}, f)
        time.sleep(0.3)
    
    # Phase 7: Back to healthy
    print("Phase 7: All systems restored")
    time.sleep(2)
    state = ['healthy'] * 100
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    
    print("\nSimulation complete!")
    print("Grid should show all nodes healthy again")

if __name__ == '__main__':
    try:
        simulate_incident()
    except KeyboardInterrupt:
        print("\nSimulation stopped")
