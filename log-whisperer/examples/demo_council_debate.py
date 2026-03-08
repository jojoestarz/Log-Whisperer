#!/usr/bin/env python3
"""
Council Debate Demo - Shows multi-agent debate in action
"""
import os
import asyncio
os.environ['DEMO_MODE'] = 'true'

from api.pipeline import Pipeline
from data.load_incident import load_cloudflare_incident
from rich.console import Console
from rich.panel import Panel

console = Console()

async def run_demo():
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Log Whisperer - Council Debate Demo[/bold cyan]\n"
        "Multi-agent root cause analysis system",
        border_style="cyan"
    ))
    
    console.print("\n[dim]This demo shows 3 AI agents debating the root cause:[/dim]")
    console.print("  [cyan]• Agent A (Conservative SRE)[/cyan] - Focuses on config changes")
    console.print("  [yellow]• Agent B (Network Specialist)[/yellow] - Analyzes BGP/routing")
    console.print("  [magenta]• Agent C (Chaos Engineer)[/magenta] - Looks for cascading failures")
    console.print()
    
    input("[dim]Press Enter to start the council debate...[/dim]")
    
    # Initialize pipeline
    pipeline = Pipeline(
        incident_id='council-demo-001',
        enable_grid=False,
        enable_pretty_logs=False  # Disable to see council debate clearly
    )
    
    # Load incident data
    log_events = load_cloudflare_incident()
    
    # Run pipeline - this will trigger the council debate
    console.print("\n[bold yellow]Starting incident analysis...[/bold yellow]\n")
    state = await pipeline.run(log_events)
    
    # Show debate summary
    console.print("\n" + "=" * 60)
    console.print("[bold cyan]Debate Summary[/bold cyan]")
    console.print("=" * 60)
    
    if state.fault_report and state.fault_report.debate_summary:
        for debate in state.fault_report.debate_summary:
            console.print(f"\n[bold]{debate.agent_name}[/bold]")
            console.print(f"  Hypothesis: {debate.hypothesis}")
            console.print(f"  Confidence: {debate.confidence:.0%}")
            console.print(f"  Reasoning: {debate.reasoning}")
    
    # Show final consensus
    console.print("\n" + "=" * 60)
    console.print("[bold green]Final Consensus[/bold green]")
    console.print("=" * 60)
    console.print(f"\n[bold]Root Cause:[/bold] {state.fault_report.root_cause}")
    console.print(f"[bold]Severity:[/bold] {state.fault_report.severity}")
    console.print(f"[bold]Confidence:[/bold] {state.fault_report.confidence:.0%}")
    console.print(f"[bold]Affected Services:[/bold] {len(state.fault_report.affected_services)}")
    
    # Continue with remediation
    console.print("\n[dim]The council has reached consensus. Generating remediation plan...[/dim]")
    console.print(f"\n[green]✓[/green] Remediation plan ready: {len(state.remediation_plan.commands)} commands")
    console.print(f"[green]✓[/green] Overall risk: {state.remediation_plan.overall_risk}")
    console.print(f"[green]✓[/green] Estimated recovery: {state.remediation_plan.estimated_recovery_mins} minutes")
    
    console.print("\n[bold cyan]Demo complete![/bold cyan]")
    console.print("[dim]The council debate provides diverse perspectives for better root cause analysis.[/dim]\n")

if __name__ == '__main__':
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted[/yellow]")
