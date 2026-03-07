#!/usr/bin/env python3
"""
Full pipeline demo with pretty event logging
Shows all event templates in action
"""
import os
import asyncio
os.environ['DEMO_MODE'] = 'true'

from api.pipeline import Pipeline
from data.load_incident import load_cloudflare_incident
from rich.console import Console

console = Console()

async def run_demo():
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]        Log Whisperer - Pretty Event Logging Demo         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]\n")
    
    # Initialize pipeline with pretty logging enabled
    pipeline = Pipeline(
        incident_id='demo-001',
        enable_grid=False,  # Disable grid for cleaner demo
        enable_pretty_logs=True
    )
    
    # Load incident data
    log_events = load_cloudflare_incident()
    
    # Run pipeline - this will show all the pretty event logs
    console.print("[dim]Running pipeline with pretty event logging...[/dim]\n")
    state = await pipeline.run(log_events)
    
    # Simulate human approval
    console.print("\n[dim]Simulating human approval...[/dim]")
    input()  # Wait for Enter key
    
    # Execute remediation
    execution_logs = pipeline.execute_approved_plan()
    
    # Final summary
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold green]                    Demo Complete!                         [/bold green]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
    
    console.print(f"\n[cyan]Pipeline Summary:[/cyan]")
    console.print(f"  • Incident ID: {state.incident_id}")
    console.print(f"  • Status: {state.status}")
    console.print(f"  • Severity: {state.fault_report.severity}")
    console.print(f"  • Commands Executed: {len(execution_logs)}")
    console.print(f"  • Overall Risk: {state.remediation_plan.overall_risk}")
    console.print()

if __name__ == '__main__':
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted[/yellow]")
