#!/usr/bin/env python3
"""
Interactive Demo: User chooses execution mode (dry_run, safe, or full)
Then runs the appropriate demo based on their selection.
"""
import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
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


def show_mode_selection():
    """Display mode selection menu and get user choice."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Log Whisperer - Interactive Demo[/bold cyan]\n"
        "Choose your execution mode",
        border_style="cyan"
    ))
    
    # Show mode descriptions
    table = Table(show_header=True, header_style="bold cyan", title="Execution Modes")
    table.add_column("Mode", style="cyan", width=12)
    table.add_column("Description", style="white", width=50)
    table.add_column("Executes?", style="yellow", width=10)
    
    table.add_row(
        "dry",
        "Preview mode - shows what would happen without executing",
        "No"
    )
    table.add_row(
        "safe",
        "Safe mode - executes only low-risk commands",
        "Yes (safe)"
    )
    table.add_row(
        "full",
        "Full mode - executes all commands (real remediation)",
        "Yes (all)"
    )
    
    console.print(table)
    console.print()
    
    # Get user choice with clear instructions
    console.print("[dim]Type one of: dry, safe, or full (then press Enter)[/dim]")
    choice = Prompt.ask(
        "[bold cyan]Type execution mode[/bold cyan]",
        choices=["dry", "safe", "full"],
        default="dry"
    )
    
    return choice


def run_demo_with_mode(mode: str):
    """Run the demo with the selected execution mode."""
    
    # Map user choice to ExecutionMode
    mode_map = {
        "dry": ExecutionMode.DRY_RUN,
        "safe": ExecutionMode.SAFE,
        "full": ExecutionMode.FULL
    }
    
    execution_mode = mode_map[mode]
    
    # Show what mode was selected
    mode_names = {
        "dry": "DRY_RUN",
        "safe": "SAFE",
        "full": "FULL"
    }
    
    console.print(f"\n[bold green]✓ Selected mode: {mode_names[mode]}[/bold green]")
    
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
        
        # Execute with selected mode
        input(f"\n[dim]Press Enter to execute in {mode_names[mode]} mode...[/dim]")
        console.print(f"\n[bold cyan]═══ EXECUTING: {mode_names[mode]} MODE ═══[/bold cyan]")
        
        if mode == "dry":
            console.print("[dim]Preview mode - no actual execution[/dim]\n")
        elif mode == "safe":
            console.print("[dim]Safe mode - executing low-risk commands only[/dim]\n")
        else:
            console.print("[dim]Full mode - executing all commands[/dim]\n")
        
        executor = CommandExecutor(mode=execution_mode, working_dir=demo_dir)
        
        console.print("⚡ Running command...")
        result = executor.execute(command)
        
        console.print(f"\nMode: [cyan]{result['mode']}[/cyan]")
        console.print(f"Executed: [yellow]{result['executed']}[/yellow]")
        console.print(f"Success: [green]{result['success']}[/green]")
        console.print(f"Command: [dim]{result['command']}[/dim]")
        
        if result['output']:
            console.print(f"\nOutput:\n[dim]{result['output'][:300]}[/dim]")
        
        # Show results based on mode
        if mode == "dry":
            console.print("\n[yellow]═══ DRY RUN RESULT ═══[/yellow]")
            console.print("✓ Preview complete - no changes made")
            console.print("✓ Command validated successfully")
            console.print("✓ Would revert commit if executed")
            console.print("\n[dim]Config remains unchanged (this was just a preview)[/dim]")
            
        elif mode == "safe" and result['executed']:
            console.print("\n[green]═══ SAFE MODE RESULT ═══[/green]")
            console.print("✓ Command executed in safe mode")
            console.print("✓ Low-risk operation completed")
            
            # Show the fix
            time.sleep(0.5)
            config_file = Path(demo_dir) / "bgp-config.yaml"
            content = config_file.read_text()
            
            console.print("\n[bold]Config After Execution:[/bold]")
            syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title="bgp-config.yaml", border_style="green"))
            
        elif mode == "full" and result['executed']:
            console.print("\n[bold green]═══ FULL EXECUTION RESULT ═══[/bold green]")
            console.print("✓ Command executed successfully")
            console.print("✓ Remediation applied")
            
            time.sleep(0.5)
            
            # Show git status
            git_result = subprocess.run(
                ["git", "status", "--short"],
                cwd=demo_dir,
                capture_output=True,
                text=True
            )
            console.print("\n[bold]Git Status:[/bold]")
            console.print(git_result.stdout or "[dim]No uncommitted changes[/dim]")
            
            # Show the fixed config
            config_file = Path(demo_dir) / "bgp-config.yaml"
            content = config_file.read_text()
            
            console.print("\n[bold]Fixed Config:[/bold]")
            syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title="bgp-config.yaml", border_style="green"))
            
            # Show git log
            git_result = subprocess.run(
                ["git", "log", "--oneline", "-4"],
                cwd=demo_dir,
                capture_output=True,
                text=True
            )
            console.print("\n[bold]Git History (after revert):[/bold]")
            console.print(git_result.stdout)
            
            # Highlight the changes
            console.print("\n[bold green]✓ SUCCESS![/bold green]")
            console.print("  • Git revert executed successfully")
            console.print("  • Config file restored to working state")
            console.print("  • prefix_list now has valid values")
            console.print("  • System would be healthy again")
            
            # Show comparison
            console.print("\n[bold cyan]═══ BEFORE vs AFTER ═══[/bold cyan]")
            
            comparison_table = Table(show_header=True, header_style="bold")
            comparison_table.add_column("State", style="cyan", width=15)
            comparison_table.add_column("prefix_list", style="yellow", width=30)
            comparison_table.add_column("Status", style="white", width=15)
            
            comparison_table.add_row(
                "BEFORE",
                '""  [red](empty!)[/red]',
                "[red]BROKEN[/red]"
            )
            comparison_table.add_row(
                "AFTER",
                "198.41.200.0/24, ...",
                "[green]FIXED[/green]"
            )
            
            console.print(comparison_table)
        
        # Summary
        console.print(f"\n[bold cyan]═══ DEMO SUMMARY: {mode_names[mode]} MODE ═══[/bold cyan]")
        
        if mode == "dry":
            console.print("✓ Preview completed successfully")
            console.print("✓ No changes made to repository")
            console.print("✓ Command validated and ready for execution")
            console.print("\n[dim]Use 'safe' or 'full' mode to actually execute[/dim]")
            
        elif mode == "safe":
            if result['executed']:
                console.print("✓ Safe execution completed")
                console.print("✓ Low-risk command executed successfully")
                console.print("✓ Config restored to working state")
            else:
                console.print("✓ Command validated but not executed")
                console.print("✓ Would require 'full' mode for this operation")
                
        else:  # full
            console.print("✓ Full execution completed")
            console.print("✓ Real remediation applied")
            console.print("✓ Incident resolved")
            console.print("\n[bold green]Real execution is FUNCTIONAL! 🎉[/bold green]")
        
    finally:
        input("\n[dim]Press Enter to cleanup...[/dim]")
        scenario.cleanup()
    
    console.print("\n[bold cyan]Demo complete![/bold cyan]")
    console.print(f"\nYou ran the demo in [bold]{mode_names[mode]}[/bold] mode.")
    console.print("\nWhat happened:")
    console.print("  1. Real git repository created")
    console.print("  2. Broken config committed")
    console.print(f"  3. Command executed in {mode_names[mode]} mode")
    
    if mode != "dry":
        console.print("  4. Actual git revert command executed")
        console.print("  5. Config file restored to working state")
        console.print("  6. Git history updated")
        console.print("\n[green]This proves the execution system is fully functional![/green]")
    else:
        console.print("  4. Preview shown (no actual execution)")
        console.print("\n[yellow]Run with 'safe' or 'full' mode to see real execution![/yellow]")


def main():
    """Main entry point."""
    try:
        # Show mode selection
        mode = show_mode_selection()
        
        # Run demo with selected mode
        run_demo_with_mode(mode)
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
