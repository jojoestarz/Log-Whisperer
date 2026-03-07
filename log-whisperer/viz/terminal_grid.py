"""
Terminal-based grid visualization using Rich.
Real-time 10x10 infrastructure health grid with live updates.
"""
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
import time
import json


def render_grid(state: list[str]) -> Panel:
    """
    Render a 10x10 grid of infrastructure nodes.
    
    Args:
        state: List of 100 node states ('healthy', 'failed', 'executing', 'recovered')
        
    Returns:
        Panel with colored grid and statistics
    """
    lines = []
    for row in range(10):
        line = ""
        for col in range(10):
            idx = row * 10 + col
            if state[idx] == 'healthy':
                line += "[green]█[/green]"
            elif state[idx] == 'failed':
                line += "[red]█[/red]"
            elif state[idx] == 'executing':
                line += "[yellow]█[/yellow]"
            elif state[idx] == 'recovered':
                line += "[blue]█[/blue]"
        lines.append(line)
    
    # Calculate statistics
    healthy = state.count('healthy')
    failed = state.count('failed')
    recovered = state.count('recovered')
    executing = state.count('executing')
    
    grid_text = "\n".join(lines)
    stats = f"\n[dim]✓ {healthy} healthy | ✗ {failed} degraded | ⚡ {executing} executing | ↻ {recovered} recovered[/]"
    
    return Panel(
        grid_text + stats,
        title="[bold green]🌐 Infrastructure Health Grid[/]",
        border_style="green"
    )


if __name__ == "__main__":
    console = Console()
    
    # Initial state: all 100 nodes healthy
    state = ['healthy'] * 100
    
    # Create initial state.json if it doesn't exist
    try:
        with open('state.json', 'r') as f:
            data = json.load(f)
            state = data.get('nodes', state)
    except FileNotFoundError:
        with open('state.json', 'w') as f:
            json.dump({'nodes': state}, f)
    
    console.print("[cyan]Starting Infrastructure Health Grid...[/cyan]")
    console.print("[dim]Reading state.json every 0.5s for updates[/dim]")
    console.print("[dim]Press Ctrl+C to exit[/dim]\n")
    
    with Live(render_grid(state), console=console, refresh_per_second=2) as live:
        while True:
            try:
                # Read state.json every 0.5s
                with open('state.json') as f:
                    data = json.load(f)
                    state = data.get('nodes', state)
                live.update(render_grid(state))
                time.sleep(0.5)
            except FileNotFoundError:
                # If file doesn't exist, keep current state
                pass
            except KeyboardInterrupt:
                console.print("\n[yellow]Grid monitoring stopped[/yellow]")
                break
            except Exception as e:
                # Continue on any other error
                pass
