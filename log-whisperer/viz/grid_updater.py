"""
Grid state updater - helper functions to update state.json from pipeline
"""
import json
from typing import List


# Map services to grid positions (3 nodes per service)
SERVICE_POSITIONS = {
    'bgp-router-lon01': [10, 11, 12],
    'bgp-router-iad01': [20, 21, 22],
    'api-gateway': [30, 31, 32],
    'dns-resolver': [40, 41, 42],
    'cdn-edge': [50, 51, 52],
    'config-deployer': [60, 61, 62],
    'bgp-validator': [70, 71, 72],
}


def initialize_grid():
    """Initialize grid with all healthy nodes."""
    state = ['healthy'] * 100
    with open('state.json', 'w') as f:
        json.dump({'nodes': state}, f)
    return state


def load_grid_state() -> List[str]:
    """Load current grid state from state.json."""
    try:
        with open('state.json', 'r') as f:
            data = json.load(f)
            return data.get('nodes', ['healthy'] * 100)
    except FileNotFoundError:
        return initialize_grid()


def update_services(services: List[str], status: str):
    """
    Update grid state for specific services.
    
    Args:
        services: List of service names
        status: Node state ('failed', 'executing', 'recovered', 'healthy')
    """
    state = load_grid_state()
    
    for service in services:
        positions = SERVICE_POSITIONS.get(service, [])
        for pos in positions:
            if pos < 100:
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
