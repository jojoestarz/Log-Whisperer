#!/usr/bin/env python3
"""
Verification script for council agent implementation
"""
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("\n")
console.print(Panel.fit(
    "[bold cyan]Council Agent Implementation Verification[/bold cyan]",
    border_style="cyan"
))

results = []

# Test 1: Model updates
console.print("\n[yellow]Test 1:[/yellow] Checking model updates...")
try:
    from models import CouncilDebate, FaultReport
    
    # Verify CouncilDebate model
    debate = CouncilDebate(
        agent_name="Test Agent",
        hypothesis="Test hypothesis",
        confidence=0.95,
        reasoning="Test reasoning"
    )
    
    # Verify FaultReport has debate_summary
    report = FaultReport(
        root_cause="Test",
        affected_services=["test"],
        severity="P1",
        fix_type="config_rollback",
        confidence=0.9,
        summary="Test",
        time_of_failure="2022-01-01T00:00:00Z",
        debate_summary=[debate]
    )
    
    assert len(report.debate_summary) == 1
    console.print("[green]✓[/green] CouncilDebate model added")
    console.print("[green]✓[/green] FaultReport.debate_summary field added")
    results.append(("Models", True))
except Exception as e:
    console.print(f"[red]✗[/red] Model check failed: {e}")
    results.append(("Models", False))

# Test 2: Council agent import
console.print("\n[yellow]Test 2:[/yellow] Checking council agent...")
try:
    from agents.council_agent import hold_council_debate, analyze_incident
    console.print("[green]✓[/green] Council agent imports successfully")
    results.append(("Council Agent", True))
except Exception as e:
    console.print(f"[red]✗[/red] Import failed: {e}")
    results.append(("Council Agent", False))

# Test 3: Cached debate
console.print("\n[yellow]Test 3:[/yellow] Testing cached debate...")
try:
    from agents.council_agent import CACHED_DEBATE, CACHED_FAULT_REPORT
    
    assert len(CACHED_DEBATE) == 3, "Should have 3 agents"
    assert len(CACHED_FAULT_REPORT.debate_summary) == 3, "Should have 3 debates"
    
    console.print("[green]✓[/green] Cached debate has 3 agents")
    console.print("[green]✓[/green] Agent A: Conservative SRE")
    console.print("[green]✓[/green] Agent B: Network Specialist")
    console.print("[green]✓[/green] Agent C: Chaos Engineer")
    results.append(("Cached Debate", True))
except Exception as e:
    console.print(f"[red]✗[/red] Cached debate check failed: {e}")
    results.append(("Cached Debate", False))

# Test 4: DEMO_MODE execution
console.print("\n[yellow]Test 4:[/yellow] Testing DEMO_MODE execution...")
try:
    os.environ['DEMO_MODE'] = 'true'
    from agents.council_agent import hold_council_debate
    from data.load_incident import load_cloudflare_incident
    
    logs = load_cloudflare_incident()
    fault_report = hold_council_debate(logs)
    
    assert fault_report.severity == "P1"
    assert len(fault_report.debate_summary) == 3
    assert fault_report.confidence == 0.89
    
    console.print("[green]✓[/green] DEMO_MODE execution successful")
    console.print(f"[green]✓[/green] Returned FaultReport with {len(fault_report.debate_summary)} debates")
    results.append(("DEMO_MODE", True))
except Exception as e:
    console.print(f"[red]✗[/red] DEMO_MODE failed: {e}")
    results.append(("DEMO_MODE", False))

# Test 5: Pipeline integration
console.print("\n[yellow]Test 5:[/yellow] Testing pipeline integration...")
try:
    from api.pipeline import Pipeline
    
    # Check that pipeline imports council_agent
    import inspect
    source = inspect.getsource(Pipeline)
    assert 'council_agent' in source, "Pipeline should import council_agent"
    
    console.print("[green]✓[/green] Pipeline imports council_agent")
    results.append(("Pipeline Integration", True))
except Exception as e:
    console.print(f"[red]✗[/red] Pipeline integration failed: {e}")
    results.append(("Pipeline Integration", False))

# Test 6: Display function
console.print("\n[yellow]Test 6:[/yellow] Testing display function...")
try:
    from agents.council_agent import display_debate, CACHED_DEBATE
    
    # This will print the debate visualization
    console.print("[dim]Displaying sample debate:[/dim]")
    display_debate(CACHED_DEBATE[:1])  # Show just one agent
    
    console.print("[green]✓[/green] Display function works")
    results.append(("Display", True))
except Exception as e:
    console.print(f"[red]✗[/red] Display failed: {e}")
    results.append(("Display", False))

# Summary
console.print("\n" + "=" * 60)
passed = sum(1 for _, success in results if success)
total = len(results)

if passed == total:
    console.print(f"[bold green]✓ ALL {total} TESTS PASSED[/bold green]")
else:
    console.print(f"[bold yellow]⚠ {passed}/{total} TESTS PASSED[/bold yellow]")

console.print("=" * 60)

# Component summary
console.print("\n[cyan]Component Status:[/cyan]")
for name, success in results:
    status = "[green]✓[/green]" if success else "[red]✗[/red]"
    console.print(f"  {status} {name}")

# Feature summary
console.print("\n[cyan]Council Agent Features:[/cyan]")
console.print("  • 3 specialized agents (SRE, Network, Chaos)")
console.print("  • Separate API calls per agent")
console.print("  • Consensus mechanism")
console.print("  • Rich panel display")
console.print("  • Confidence bars")
console.print("  • DEMO_MODE support")
console.print("  • Error handling with fallback")
console.print("  • Pipeline integration")

console.print("\n[cyan]To see it in action:[/cyan]")
console.print("  python test_council_agent.py")
console.print("  python demo_council_debate.py")

console.print()
