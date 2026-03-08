#!/usr/bin/env python3
"""
Log Whisperer - Main Entry Point

Single source of truth for running the application.
"""
import os
import sys
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def show_main_menu():
    """Display production-level startup prompt."""
    console.clear()
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]🤫 LOG WHISPERER[/bold green]\n"
        "[dim green]Multi-agent incident remediation system[/dim green]",
        border_style="green"
    ))
    console.print()
    
    # Show system status
    demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
    llm_provider = os.getenv('LLM_PROVIDER', 'anthropic')
    
    console.print(f"[dim green]LLM Provider:[/dim green] [green]{llm_provider}[/green]")
    console.print(f"[dim green]Demo Mode:[/dim green] [green]{'enabled' if demo_mode else 'disabled'}[/green]")
    console.print()
    
    # Simple yes/no prompt
    choice = Prompt.ask(
        "[bold green]Start pipeline?[/bold green]",
        choices=["yes", "no", "y", "n"],
        default="yes"
    )
    
    return choice.lower() in ["yes", "y"]


def check_api_key():
    """Check if ANTHROPIC_API_KEY is configured."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key.startswith("sk-ant-api03-"):
        return True
    return False


async def run_full_pipeline():
    """Run the complete pipeline with all agents."""
    console.print("\n[bold green]═══ Starting Pipeline ═══[/bold green]\n")
    
    # Check if in demo mode
    demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'
    if demo_mode:
        console.print("[green]DEMO_MODE enabled - using cached responses[/green]\n")
    
    # Import here to avoid loading if not needed
    from api.pipeline import Pipeline
    from data.load_incident import load_cloudflare_incident
    
    # Load incident data
    console.print("[green]Loading incident data...[/green]")
    log_events = load_cloudflare_incident()
    console.print(f"[green]✓[/green] Loaded {len(log_events)} log events\n")
    
    # Initialize pipeline
    pipeline = Pipeline(
        incident_id="cloudflare-bgp-2022",
        enable_grid=True,  # Enable grid updates for visualizer
        enable_pretty_logs=True
    )
    
    # Run pipeline
    console.print("[green]Running pipeline...[/green]\n")
    state = await pipeline.run(log_events)
    
    # Show results
    console.print("\n[bold green]✓ Pipeline Analysis Complete[/bold green]")
    console.print(f"[dim green]Root Cause:[/dim green] [green]{state.fault_report.root_cause}[/green]")
    console.print(f"[dim green]Severity:[/dim green] [green]{state.fault_report.severity}[/green]")
    console.print(f"[dim green]Commands Generated:[/dim green] [green]{len(state.remediation_plan.commands)}[/green]")
    
    # Auto-execute in demo mode, otherwise ask
    if demo_mode:
        console.print("\n[green]Auto-executing remediation (demo mode)...[/green]")
        execution_logs = pipeline.execute_approved_plan(execution_mode='dry_run')
        
        console.print(f"\n[bold green]✓ Execution Complete[/bold green]")
        console.print(f"[dim green]Commands executed:[/dim green] [green]{len(execution_logs)}[/green]")
        console.print(f"[dim green]Status:[/dim green] [green]{state.status}[/green]")
    else:
        # Ask for approval in production mode
        console.print("\n[bold green]Ready to execute remediation?[/bold green]")
        approve = Prompt.ask("[green]Execute commands?[/green]", choices=["yes", "no"], default="no")
        
        if approve == "yes":
            mode = Prompt.ask(
                "[green]Execution mode[/green]",
                choices=["dry_run", "safe", "full"],
                default="dry_run"
            )
            console.print()
            execution_logs = pipeline.execute_approved_plan(execution_mode=mode)
            
            console.print(f"\n[bold green]✓ Execution Complete[/bold green]")
            console.print(f"[dim green]Commands executed:[/dim green] [green]{len(execution_logs)}[/green]")
            console.print(f"[dim green]Status:[/dim green] [green]{state.status}[/green]")
        else:
            console.print("\n[green]Execution cancelled by user[/green]")


def run_quick_demo():
    """Run the quick execution demo."""
    console.print("\n[bold cyan]═══ Quick Execution Demo ═══[/bold cyan]\n")
    console.print("[dim]This demo focuses on execution modes without AI agents[/dim]\n")
    
    # Import and run the interactive demo
    from demo_interactive import show_mode_selection, run_demo_with_mode
    
    mode = show_mode_selection()
    run_demo_with_mode(mode)


def start_api_server():
    """Start the API server."""
    console.print("\n[bold cyan]═══ API Server Mode ═══[/bold cyan]\n")
    
    # Check API key
    if not check_api_key():
        console.print("[red]✗ ANTHROPIC_API_KEY not configured[/red]")
        console.print("[dim]Add your API key to .env file[/dim]\n")
        return
    
    console.print("[yellow]Starting API server...[/yellow]")
    console.print("[dim]Server will be available at http://localhost:8000[/dim]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    # Import and run the API server
    try:
        from api.main import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        console.print("[red]✗ uvicorn not installed[/red]")
        console.print("[dim]Install with: pip install uvicorn[/dim]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Server stopped[/yellow]")


def run_tests():
    """Run system tests."""
    console.print("\n[bold cyan]═══ Test Mode ═══[/bold cyan]\n")
    
    tests = [
        ("Executor", "test_real_execution.py"),
        ("Council Agent", "test_council_agent.py"),
        ("Writer Agent", "test_writer_agent.py"),
    ]
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Test", style="cyan", width=20)
    table.add_column("File", style="white", width=30)
    
    for name, file in tests:
        table.add_row(name, file)
    
    console.print(table)
    console.print()
    
    choice = Prompt.ask(
        "Which test to run?",
        choices=["1", "2", "3", "all"],
        default="all"
    )
    
    if choice == "all":
        for name, file in tests:
            console.print(f"\n[yellow]Running {name} tests...[/yellow]")
            os.system(f"python3 {file}")
    else:
        idx = int(choice) - 1
        name, file = tests[idx]
        console.print(f"\n[yellow]Running {name} tests...[/yellow]")
        os.system(f"python3 {file}")


def main():
    """Main entry point."""
    try:
        # Show startup prompt
        should_start = show_main_menu()
        
        if should_start:
            asyncio.run(run_full_pipeline())
        else:
            console.print("\n[green]Pipeline cancelled[/green]\n")
            sys.exit(0)
    
    except KeyboardInterrupt:
        console.print("\n\n[green]Interrupted by user[/green]")
        sys.exit(0)
    
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
