#!/usr/bin/env python3
"""
Full pipeline demo: Logs → Decision Agent → Writer Agent
Demonstrates the complete flow with rich formatting
"""
import os
os.environ['DEMO_MODE'] = 'true'

from rich.console import Console
from rich.panel import Panel
from agents.decision_agent import analyze_logs
from agents.writer_agent import generate_plan

console = Console()

console.print("\n")
console.print(Panel.fit(
    "[bold cyan]Log Whisperer Demo[/bold cyan]\n"
    "Multi-agent incident remediation pipeline",
    border_style="cyan"
))

# Step 1: Analyze logs
console.print("\n[bold yellow]Step 1:[/bold yellow] Analyzing incident logs...")
fault_report = analyze_logs('data/cloudflare_incident.json')

# Step 2: Generate remediation plan
console.print("\n[bold yellow]Step 2:[/bold yellow] Generating remediation plan...")
remediation_plan = generate_plan(fault_report)

# Summary
console.print("\n")
console.print(Panel(
    f"[green]✓[/green] Pipeline Complete\n\n"
    f"Incident: {fault_report.severity} - {fault_report.confidence:.0%} confidence\n"
    f"Plan: {len(remediation_plan.commands)} commands, {remediation_plan.overall_risk} risk\n"
    f"ETA: {remediation_plan.estimated_recovery_mins} minutes",
    title="[bold green]Summary[/bold green]",
    border_style="green"
))

console.print("\n[dim]Ready for human approval to execute remediation[/dim]\n")
