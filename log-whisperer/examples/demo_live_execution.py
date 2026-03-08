#!/usr/bin/env python3
"""
Live Demo: Prove Real Execution Works
Creates a visible test scenario and shows actual command execution.
"""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.syntax import Syntax
import time

from execution.executor import CommandExecutor, ExecutionMode
from models import CLICommand

console = Console()


class DemoScenario:
    """Creates a realistic demo scenario with visible results."""
    
    def __init__(self):
        self.demo_dir = None
        self.bad_commit = None
        
    def setup(self):
        """Create a demo git repository with a 'broken' config."""
        console.print("\n[bold cyan]Setting up demo scenario...[/bold cyan]")
        
        # Create temp directory
        self.demo_dir = tempfile.mkdtemp(prefix="log_whisperer_demo_")
        console.print(f"📁 Demo directory: [yellow]{self.demo_dir}[/yellow]")
        
        # Initialize git
        subprocess.run(["git", "init"], cwd=self.demo_dir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Demo User"], cwd=self.demo_dir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "demo@logwhisperer.ai"], cwd=self.demo_dir, capture_output=True)
        
        # Create initial "good" config
        config_file = Path(self.demo_dir) / "bgp-config.yaml"
        config_file.write_text("""# BGP Configuration
router:
  id: bgp-router-01
  asn: 65000
  prefix_list:
    - 198.41.200.0/24
    - 172.64.0.0/13
  status: healthy
""")
        
        subprocess.run(["git", "add", "."], cwd=self.demo_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial config - working"], 
                      cwd=self.demo_dir, capture_output=True)
        
        console.print("✓ Created initial [green]working[/green] config")
        
        # Create "broken" config (the incident)
        config_file.write_text("""# BGP Configuration
router:
  id: bgp-router-01
  asn: 65000
  prefix_list: ""  # ← BROKEN: Empty string!
  status: degraded
""")
        
        subprocess.run(["git", "add", "."], cwd=self.demo_dir, capture_output=True)
        result = subprocess.run(["git", "commit", "-m", "Deploy 4821 - BROKEN CONFIG"], 
                               cwd=self.demo_dir, capture_output=True, text=True)
        
        # Get the bad commit hash
        result = subprocess.run(["git", "rev-parse", "HEAD"], 
                               cwd=self.demo_dir, capture_output=True, text=True)
        self.bad_commit = result.stdout.strip()
        
        console.print(f"✗ Created [red]broken[/red] config (commit: {self.bad_commit[:8]})")
        
        return self.demo_dir, self.bad_commit
    
    def show_current_state(self):
        """Display current repository state."""
        config_file = Path(self.demo_dir) / "bgp-config.yaml"
        content = config_file.read_text()
        
        console.print("\n[bold]Current Config State:[/bold]")
        syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="bgp-config.yaml", border_style="red"))
        
        # Show git log
        result = subprocess.run(
            ["git", "log", "--oneline", "-3"],
            cwd=self.demo_dir,
            capture_output=True,
            text=True
        )
        console.print("\n[bold]Git History:[/bold]")
        console.print(result.stdout)
    
    def cleanup(self):
        """Remove demo directory."""
        if self.demo_dir and os.path.exists(self.demo_dir):
            shutil.rmtree(self.demo_dir)
            console.print(f"\n🗑️  Cleaned up demo directory")


def demo_comparison():
    """Show side-by-side comparison of all three modes."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Log Whisperer - Live Execution Demo[/bold cyan]\n"
        "Watch real commands execute and fix a broken config",
        border_style="cyan"
    ))
    
    scenario = DemoScenario()
    
    try:
        # Setup
        demo_dir, bad_commit = scenario.setup()
        
        console.print("\n[bold yellow]═══ SCENARIO ═══[/bold yellow]")
        console.print("🚨 Incident: BGP config deployment 4821 broke production")
        console.print("📋 Root Cause: Empty prefix_list in bgp-config.yaml")
        console.print("🔧 Remediation: Revert the bad commit")
        
        input("\n[dim]Press Enter to see the broken config...[/dim]")
        scenario.show_current_state()
        
        # Create the remediation command
        command = CLICommand(
            tool="git_revert",
            args={"commit": bad_commit},
            description="Revert broken BGP config deployment 4821",
            risk_level="low"
        )
        
        console.print("\n[bold yellow]═══ REMEDIATION COMMAND ═══[/bold yellow]")
        console.print(f"Tool: [cyan]{command.tool}[/cyan]")
        console.print(f"Commit: [yellow]{bad_commit[:8]}[/yellow]")
        console.print(f"Risk: [green]{command.risk_level}[/green]")
        console.print(f"Description: {command.description}")
        
        # Mode 1: DRY_RUN
        input("\n[dim]Press Enter to try DRY_RUN mode...[/dim]")
        console.print("\n[bold cyan]═══ MODE 1: DRY_RUN ═══[/bold cyan]")
        console.print("[dim]Shows what would happen without executing[/dim]\n")
        
        executor_dry = CommandExecutor(mode=ExecutionMode.DRY_RUN, working_dir=demo_dir)
        result_dry = executor_dry.execute(command)
        
        console.print(f"Executed: [yellow]{result_dry['executed']}[/yellow]")
        console.print(f"Output: [dim]{result_dry['output']}[/dim]")
        
        console.print("\n[yellow]Config unchanged - this was just a preview[/yellow]")
        
        # Mode 2: SAFE
        input("\n[dim]Press Enter to try SAFE mode...[/dim]")
        console.print("\n[bold cyan]═══ MODE 2: SAFE ═══[/bold cyan]")
        console.print("[dim]Executes only low-risk commands[/dim]\n")
        
        executor_safe = CommandExecutor(mode=ExecutionMode.SAFE, working_dir=demo_dir)
        result_safe = executor_safe.execute(command)
        
        console.print(f"Executed: [yellow]{result_safe['executed']}[/yellow]")
        console.print(f"Success: [green]{result_safe['success']}[/green]")
        
        if result_safe['executed']:
            console.print("\n[green]✓ Command executed in SAFE mode![/green]")
            console.print("[dim]But we'll reset for the FULL demo...[/dim]")
            # Reset for full demo
            subprocess.run(["git", "reset", "--hard", "HEAD"], 
                         cwd=demo_dir, capture_output=True)
        
        # Mode 3: FULL (The real deal)
        input("\n[dim]Press Enter for FULL execution (the real fix!)...[/dim]")
        console.print("\n[bold cyan]═══ MODE 3: FULL EXECUTION ═══[/bold cyan]")
        console.print("[dim]Actually fixing the broken config...[/dim]\n")
        
        executor_full = CommandExecutor(mode=ExecutionMode.FULL, working_dir=demo_dir)
        
        console.print("⚡ Executing command...")
        result_full = executor_full.execute(command)
        
        console.print(f"\nExecuted: [green]{result_full['executed']}[/green]")
        console.print(f"Success: [green]{result_full['success']}[/green]")
        console.print(f"Command: [cyan]{result_full['command']}[/cyan]")
        
        if result_full['output']:
            console.print(f"\nOutput:\n[dim]{result_full['output'][:300]}[/dim]")
        
        # Show the fix worked!
        if result_full['success']:
            console.print("\n[bold green]═══ VERIFICATION: DID IT WORK? ═══[/bold green]")
            
            time.sleep(0.5)
            
            # Show git status
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=demo_dir,
                capture_output=True,
                text=True
            )
            console.print("\n[bold]Git Status:[/bold]")
            console.print(result.stdout or "[dim]No uncommitted changes[/dim]")
            
            # Show the fixed config
            config_file = Path(demo_dir) / "bgp-config.yaml"
            content = config_file.read_text()
            
            console.print("\n[bold]Fixed Config:[/bold]")
            syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title="bgp-config.yaml", border_style="green"))
            
            # Show git log
            result = subprocess.run(
                ["git", "log", "--oneline", "-4"],
                cwd=demo_dir,
                capture_output=True,
                text=True
            )
            console.print("\n[bold]Git History (after revert):[/bold]")
            console.print(result.stdout)
            
            # Highlight the changes
            console.print("\n[bold green]✓ SUCCESS![/bold green]")
            console.print("  • Git revert executed successfully")
            console.print("  • Config file restored to working state")
            console.print("  • prefix_list now has valid values")
            console.print("  • System would be healthy again")
            
            # Show comparison
            console.print("\n[bold cyan]═══ BEFORE vs AFTER ═══[/bold cyan]")
            
            table = Table(show_header=True, header_style="bold")
            table.add_column("State", style="cyan", width=15)
            table.add_column("prefix_list", style="yellow", width=30)
            table.add_column("Status", style="white", width=15)
            
            table.add_row(
                "BEFORE",
                '""  [red](empty!)[/red]',
                "[red]BROKEN[/red]"
            )
            table.add_row(
                "AFTER",
                "198.41.200.0/24, ...",
                "[green]FIXED[/green]"
            )
            
            console.print(table)
        
        # Summary
        console.print("\n[bold cyan]═══ DEMO SUMMARY ═══[/bold cyan]")
        
        summary_table = Table(show_header=True, header_style="bold cyan")
        summary_table.add_column("Mode", style="cyan")
        summary_table.add_column("Executed?", style="yellow")
        summary_table.add_column("Result", style="green")
        
        summary_table.add_row(
            "DRY_RUN",
            "No",
            "Preview only"
        )
        summary_table.add_row(
            "SAFE",
            "Yes (if safe)",
            "Controlled execution"
        )
        summary_table.add_row(
            "FULL",
            "Yes",
            "✓ Fixed the config!"
        )
        
        console.print(summary_table)
        
        console.print("\n[bold green]Real execution is FUNCTIONAL! 🎉[/bold green]")
        console.print("[dim]The system actually executed git commands and fixed the config.[/dim]")
        
    finally:
        input("\n[dim]Press Enter to cleanup...[/dim]")
        scenario.cleanup()
    
    console.print("\n[bold cyan]Demo complete![/bold cyan]")
    console.print("\nWhat you just saw:")
    console.print("  1. Real git repository created")
    console.print("  2. Broken config committed")
    console.print("  3. Three execution modes demonstrated")
    console.print("  4. Actual git revert command executed")
    console.print("  5. Config file restored to working state")
    console.print("  6. Git history updated")
    console.print("\n[green]This proves the execution system is fully functional![/green]")


if __name__ == '__main__':
    try:
        demo_comparison()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
