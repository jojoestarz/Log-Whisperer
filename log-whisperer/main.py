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
    """Display main menu and get user choice."""
    console.clear()
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🤫 Log Whisperer[/bold cyan]\n"
        "[dim]Multi-agent incident remediation system[/dim]",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold cyan", title="Available Options")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Description", style="white", width=60)
    table.add_column("API Key", style="yellow", width=12)
    
    table.add_row(
        "1",
        "Run Full Pipeline - Complete incident remediation flow",
        "Required"
    )
    table.add_row(
        "2",
        "Quick Execution Demo - Test execution modes (dry/safe/full)",
        "Not needed"
    )
    table.add_row(
        "3",
        "Start API Server - Run as HTTP/WebSocket service",
        "Required"
    )
    table.add_row(
        "4",
        "Run Tests - Verify system components",
        "Optional"
    )
    table.add_row(
        "q",
        "Quit",
        "-"
    )
    
    console.print(table)
    console.print()
    
    choice = Prompt.ask(
        "[bold cyan]Select an option[/bold cyan]",
        choices=["1", "2", "3", "4", "q"],
        default="2"
    )
    
    return choice


def check_api_key():
    """Check if ANTHROPIC_API_KEY is configured."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key.startswith("sk-ant-api03-"):
        return True
    return False


async def run_full_pipeline():
    """Run the complete pipeline with all agents."""
    console.print("\n[bold cyan]═══ Full Pipeline Mode ═══[/bold cyan]\n")
    
    # Check API key
    if not check_api_key():
        console.print("[yellow]⚠ Warning: ANTHROPIC_API_KEY not configured[/yellow]")
        console.print("[dim]Running in DEMO_MODE with cached responses[/dim]\n")
        os.environ['DEMO_MODE'] = 'true'
    
    # Import here to avoid loading if not needed
    from api.pipeline import Pipeline
    from data.load_incident import load_cloudflare_incident
    
    # Get execution mode
    console.print("[dim]Choose execution mode for remediation commands:[/dim]")
    mode = Prompt.ask(
        "Execution mode",
        choices=["dry_run", "safe", "full"],
        default="dry_run"
    )
    console.print()
    
    # Load incident data
    console.print("[yellow]Loading incident data...[/yellow]")
    log_events = load_cloudflare_incident()
    console.print(f"[green]✓[/green] Loaded {len(log_events)} log events\n")
    
    # Initialize pipeline
    pipeline = Pipeline(
        incident_id="cloudflare-bgp-2022",
        enable_grid=False,
        enable_pretty_logs=True
    )
    
    # Run pipeline
    console.print("[yellow]Running pipeline...[/yellow]\n")
    state = await pipeline.run(log_events)
    
    # Show results
    console.print("\n[bold green]✓ Pipeline Analysis Complete[/bold green]")
    console.print(f"Root Cause: {state.fault_report.root_cause}")
    console.print(f"Severity: {state.fault_report.severity}")
    console.print(f"Commands Generated: {len(state.remediation_plan.commands)}")
    
    # Ask for approval
    console.print("\n[bold yellow]Ready to execute remediation?[/bold yellow]")
    approve = Prompt.ask("Execute commands?", choices=["yes", "no"], default="no")
    
    if approve == "yes":
        console.print()
        execution_logs = pipeline.execute_approved_plan(execution_mode=mode)
        
        console.print(f"\n[bold green]✓ Execution Complete[/bold green]")
        console.print(f"Commands executed: {len(execution_logs)}")
        console.print(f"Status: {state.status}")
    else:
        console.print("\n[yellow]Execution cancelled by user[/yellow]")


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
        while True:
            choice = show_main_menu()
            
            if choice == "1":
                asyncio.run(run_full_pipeline())
                input("\n[dim]Press Enter to return to menu...[/dim]")
            
            elif choice == "2":
                run_quick_demo()
                input("\n[dim]Press Enter to return to menu...[/dim]")
            
            elif choice == "3":
                start_api_server()
                input("\n[dim]Press Enter to return to menu...[/dim]")
            
            elif choice == "4":
                run_tests()
                input("\n[dim]Press Enter to return to menu...[/dim]")
            
            elif choice == "q":
                console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
                sys.exit(0)
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
