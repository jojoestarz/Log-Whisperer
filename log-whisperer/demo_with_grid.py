#!/usr/bin/env python3
"""
Full pipeline demo with grid visualization
Run viz/terminal_grid.py in another terminal to watch real-time updates
"""
import os
import asyncio
import time
os.environ['DEMO_MODE'] = 'true'

from api.pipeline import Pipeline
from data.load_incident import load_cloudflare_incident
from rich.console import Console

console = Console()

async def run_demo():
    console.print("\n[bold cyan]Log Whisperer - Full Pipeline Demo with Grid[/bold cyan]")
    console.print("[dim]Make sure to run 'python viz/terminal_grid.py' in another terminal![/dim]\n")
    
    # Initialize pipeline with grid enabled
    pipeline = Pipeline(incident_id='demo-001', enable_grid=True)
    
    # Load incident data
    console.print("[yellow]Loading incident data...[/yellow]")
    log_events = load_cloudflare_incident()
    time.sleep(1)
    
    # Run pipeline
    console.print("[yellow]Running pipeline...[/yellow]")
    console.print("[dim]Watch the grid for real-time updates![/dim]\n")
    
    state = await pipeline.run(log_events)
    
    console.print(f"\n[green]✓[/green] Pipeline Status: {state.status}")
    console.print(f"[green]✓[/green] Fault Report: {state.fault_report.severity}")
    console.print(f"[green]✓[/green] Remediation Plan: {len(state.remediation_plan.commands)} commands")
    console.print(f"[green]✓[/green] Affected Services: {len(state.fault_report.affected_services)}")
    
    console.print("\n[yellow]Grid should now show failed services (red nodes)[/yellow]")
    console.print("[dim]Press Enter to execute remediation...[/dim]")
    input()
    
    # Execute remediation
    console.print("\n[yellow]Executing remediation...[/yellow]")
    execution_logs = pipeline.execute_approved_plan()
    
    console.print(f"\n[green]✓[/green] Remediation complete!")
    console.print(f"[green]✓[/green] Executed {len(execution_logs)} commands")
    console.print(f"[green]✓[/green] Status: {pipeline.state.status}")
    
    console.print("\n[yellow]Grid should now show recovered services (blue nodes)[/yellow]")
    console.print("\n[bold green]Demo complete![/bold green]")

if __name__ == '__main__':
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted[/yellow]")
