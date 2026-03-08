"""
Grid state updater - helper functions to update state.json from pipeline
"""
import json
from typing import List


# Map services to grid positions (dynamically calculated based on node count)
SERVICE_POSITIONS = {
    'bgp-router-lon01': [0, 1],
    'bgp-router-iad01': [2, 3],
    'api-gateway': [4, 5],
    'dns-resolver': [6, 7],
    'cdn-edge': [8],
    'config-deployer': [0, 1, 2],  # Fallback to first nodes
    'bgp-validator': [3, 4, 5],
}


def initialize_grid():
    """Initialize grid with all failed nodes (dynamic count from logs)."""
    # Try to preserve existing node count, otherwise default to 100
    try:
        with open('state.json', 'r') as f:
            data = json.load(f)
            node_count = len(data.get('nodes', []))
            if node_count > 0:
                state = ['failed'] * node_count
            else:
                state = ['failed'] * 100
    except FileNotFoundError:
        state = ['failed'] * 100
    
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    return state


def load_grid_state() -> List[str]:
    """Load current grid state from state.json."""
    try:
        with open('state.json', 'r') as f:
            data = json.load(f)
            nodes = data.get('nodes', [])
            if not nodes:
                return initialize_grid()
            return nodes
    except FileNotFoundError:
        return initialize_grid()


def update_services(services: List[str], status: str):
    """
    Update grid state for specific services.
    For small grids (< 20 nodes), updates all nodes to show system-wide state.
    For larger grids, updates specific service positions.
    
    Args:
        services: List of service names
        status: Node state ('failed', 'executing', 'recovered', 'healthy')
    """
    state = load_grid_state()
    max_pos = len(state)
    
    # For small grids, update all nodes to show system-wide state
    if max_pos < 20:
        state = [status] * max_pos
    else:
        # For larger grids, use specific positions
        for service in services:
            positions = SERVICE_POSITIONS.get(service, [])
            for pos in positions:
                if pos < max_pos:
                    state[pos] = status
    
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)


def mark_services_failed(services: List[str]):
    """Mark services as failed (red)."""
    update_services(services, 'failed')


def mark_services_executing(services: List[str]):
    """Mark services as executing remediation (yellow)."""
    update_services(services, 'executing')


def mark_services_recovered(services: List[str]):
    """Mark services as recovered (blue)."""
    update_services(services, 'recovered')


def mark_services_healthy(services: List[str]):
    """Mark services as healthy (green)."""
    update_services(services, 'healthy')


def reset_grid():
    """Reset all nodes to healthy."""
    initialize_grid()


if __name__ == '__main__':
    # Demo usage
    print("Grid Updater Demo")
    print("=" * 60)
    
    print("\n1. Initialize grid (all healthy)")
    initialize_grid()
    
    print("\n2. Mark some services as failed")
    mark_services_failed(['bgp-router-lon01', 'api-gateway', 'dns-resolver'])
    
    print("\n3. Mark one service as executing")
    mark_services_executing(['bgp-router-lon01'])
    
    print("\n4. Mark one service as recovered")
    mark_services_recovered(['bgp-router-lon01'])
    
    print("\n✓ Grid state updated in state.json")
    print("Run 'python viz/terminal_grid.py' to see the changes")
