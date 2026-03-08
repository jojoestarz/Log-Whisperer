#!/usr/bin/env python3
"""
Test script for terminal_logger.py
Demonstrates all event logging functions
"""
import time
from viz.terminal_logger import (
    log_event,
    log_ingesting,
    log_diagnosis,
    log_remediation,
    log_safety_check,
    log_approval,
    log_executing,
    log_resolved,
    log_error,
    log_warning,
    log_info
)
from rich.console import Console

console = Console()

console.print("\n[bold cyan]Terminal Logger Demo[/bold cyan]")
console.print("=" * 60)
console.print()

# Test 1: Basic log_event function
console.print("[yellow]Test 1: Basic log_event function[/yellow]")
log_event("📥", "INGESTING", "Reading Cloudflare BGP incident logs...", "cyan")
time.sleep(0.5)

# Test 2: Diagnosis event
console.print("\n[yellow]Test 2: Diagnosis event[/yellow]")
log_diagnosis("Empty-string config in BGP deployment 4821 triggered bulk route withdrawal")
time.sleep(0.5)

# Test 3: Remediation event
console.print("\n[yellow]Test 3: Remediation event[/yellow]")
log_remediation(command_count=3, risk="low")
time.sleep(0.5)

# Test 4: Safety check event
console.print("\n[yellow]Test 4: Safety check event[/yellow]")
log_safety_check(status="SAFE")
time.sleep(0.5)

# Test 5: Approval event
console.print("\n[yellow]Test 5: Approval event[/yellow]")
log_approval("Awaiting human approval - Press ENTER")
time.sleep(0.5)

# Test 6: Executing event
console.print("\n[yellow]Test 6: Executing event[/yellow]")
log_executing("Applying remediation commands...")
time.sleep(0.5)

# Test 7: Resolved event
console.print("\n[yellow]Test 7: Resolved event[/yellow]")
log_resolved(mttr="04:12", baseline="57:00", reduction="93%")
time.sleep(0.5)

# Test 8: Error event
console.print("\n[yellow]Test 8: Error event[/yellow]")
log_error("API connection failed - retrying...")
time.sleep(0.5)

# Test 9: Warning event
console.print("\n[yellow]Test 9: Warning event[/yellow]")
log_warning("High risk operation detected")
time.sleep(0.5)

# Test 10: Info event
console.print("\n[yellow]Test 10: Info event[/yellow]")
log_info("SYSTEM STATUS", "All systems operational")
time.sleep(0.5)

# Test 11: Custom colors
console.print("\n[yellow]Test 11: Custom colors[/yellow]")
log_event("🚀", "CUSTOM", "Custom event with magenta color", "magenta")
log_event("💡", "TIP", "You can use any Rich color name", "bright_blue")
time.sleep(0.5)

console.print("\n" + "=" * 60)
console.print("[bold green]✓ All event templates tested successfully![/bold green]")
console.print()
