#!/usr/bin/env python3
"""
Demo: Real Execution with Log Whisperer
Shows the difference between dry-run, safe, and full execution modes.
"""
import os
import asyncio
os.environ['DEMO_MODE'] = 'true'

from api.pipeline import Pipeline
from data.load_incident import load_cloudflare_incident
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


async def demo_execution_modes():
    """Demonstrate all three execution modes."""
    
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Log Whisperer - Real Execution Demo[/bold cyan]\n"
        "Demonstrating DRY_RUN, SAFE, and FULL execution modes",
        border_style="cyan"
    ))
    
    # Load incident data
    logs = load_cloudflare_incident()
    
    # Mode 1: DRY_RUN
    console.print("\n[bold yellow]═══ Mode 1: DRY_RUN (Safest) ═══[/bold yellow]")
    console.print("[dim]Shows what would happen without executing[/dim]\n")
    
    pipeline1 = Pipeline(incident_id='demo-dry-run', enable_pretty_logs=False)
    state1 = await pipeline1.run(logs)
    
    console.print(f"[cyan]Commands generated:[/cyan] {len(state1.remediation_plan.commands)}")
    for i, cmd in enumerate(state1.remediation_plan.commands, 1):
        console.print(f"  {i}. {cmd.tool}: {cmd.description}")
    
    console.print("\n[yellow]Executing in DRY_RUN mode...[/yellow]")
    execution_logs1 = pipeline1.execute_approved_plan(execution_mode="dry_run")
    
    for i, log in enumerate(execution_logs1, 1):
        status = "✓" if log.success else "✗"
        console.print(f"  {status} Command {i}: {log.command.tool}")
        console.print(f"     Output: {log.output[:80]}...")
    
    console.print(f"\n[green]✓ DRY_RUN complete - No actual commands executed[/green]")
    
    # Mode 2: SAFE
    console.print("\n[bold yellow]═══ Mode 2: SAFE (Controlled) ═══[/bold yellow]")
    console.print("[dim]Executes only low-risk commands[/dim]\n")
    
    pipeline2 = Pipeline(incident_id='demo-safe', enable_pretty_logs=False)
    state2 = await pipeline2.run(logs)
    
    console.print("[yellow]Executing in SAFE mode...[/yellow]")
    execution_logs2 = pipeline2.execute_approved_plan(execution_mode="safe")
    
    for i, log in enumerate(execution_logs2, 1):
        status = "✓" if log.success else "✗"
        console.print(f"  {status} Command {i}: {log.command.tool}")
        if log.error:
            console.print(f"     [red]Blocked: {log.error}[/red]")
        else:
            console.print(f"     [green]Would execute (if tools installed)[/green]")
    
    console.print(f"\n[green]✓ SAFE mode complete - Only safe commands allowed[/green]")
    
    # Mode 3: FULL (explanation only)
    console.print("\n[bold yellow]═══ Mode 3: FULL (Complete) ═══[/bold yellow]")
    console.print("[dim]Executes ALL commands - use with caution![/dim]\n")
    
    console.print("[red]⚠️  FULL mode not demonstrated in this demo[/red]")
    console.print("[dim]FULL mode executes real commands and should only be used:")
    console.print("  • In production incidents")
    console.print("  • After human review and approval")
    console.print("  • With proper infrastructure access")
    console.print("  • When confident in the remediation plan[/dim]")
    
    # Summary table
    console.print("\n[bold cyan]═══ Execution Mode Comparison ═══[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Mode", style="cyan")
    table.add_column("Executes", style="yellow")
    table.add_column("Safety", style="green")
    table.add_column("Use Case", style="white")
    
    table.add_row(
        "DRY_RUN",
        "Nothing",
        "Highest",
        "Testing, demos, development"
    )
    table.add_row(
        "SAFE",
        "Low-risk only",
        "Medium",
        "Dev/staging, learning"
    )
    table.add_row(
        "FULL",
        "Everything",
        "Lowest",
        "Production incidents"
    )
    
    console.print(table)
    
    # Configuration
    console.print("\n[bold cyan]═══ Configuration ═══[/bold cyan]\n")
    console.print("Set execution mode in .env:")
    console.print("  [yellow]EXECUTION_MODE=dry_run[/yellow]   # Default, safest")
    console.print("  [yellow]EXECUTION_MODE=safe[/yellow]      # Controlled execution")
    console.print("  [yellow]EXECUTION_MODE=full[/yellow]      # Complete execution")
    
    console.print("\nOr pass explicitly:")
    console.print("  [yellow]pipeline.execute_approved_plan(execution_mode='dry_run')[/yellow]")
    
    # Real execution proof
    console.print("\n[bold cyan]═══ Real Execution Proof ═══[/bold cyan]\n")
    console.print("Run the test suite to see real git operations:")
    console.print("  [yellow]python test_real_execution.py[/yellow]")
    console.print("\nThis will:")
    console.print("  • Create a temporary git repository")
    console.print("  • Execute real git revert commands")
    console.print("  • Verify the operations worked")
    console.print("  • Clean up afterward")
    
    console.print("\n[bold green]Demo complete![/bold green]")
    console.print("[dim]Real execution is functional and ready to use.[/dim]\n")


if __name__ == '__main__':
    try:
        asyncio.run(demo_execution_modes())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted[/yellow]")
