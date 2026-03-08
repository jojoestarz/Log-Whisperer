#!/usr/bin/env python3
"""
Test real command execution with actual git operations.
Creates a test repository and executes real commands.
"""
import os
import shutil
import tempfile
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from execution.executor import CommandExecutor, ExecutionMode
from models import CLICommand

console = Console()


def setup_test_repo() -> str:
    """Create a test git repository."""
    test_dir = tempfile.mkdtemp(prefix="log_whisperer_test_")
    
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=test_dir, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=test_dir, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=test_dir, capture_output=True)
    
    # Create initial commit
    test_file = Path(test_dir) / "config.txt"
    test_file.write_text("initial config\n")
    subprocess.run(["git", "add", "."], cwd=test_dir, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=test_dir, capture_output=True)
    
    # Create a second commit (this is what we'll revert)
    test_file.write_text("broken config\n")
    subprocess.run(["git", "add", "."], cwd=test_dir, capture_output=True)
    result = subprocess.run(["git", "commit", "-m", "Bad config"], 
                          cwd=test_dir, capture_output=True, text=True)
    
    # Get the commit hash
    result = subprocess.run(["git", "rev-parse", "HEAD"], 
                          cwd=test_dir, capture_output=True, text=True)
    commit_hash = result.stdout.strip()
    
    return test_dir, commit_hash


def cleanup_test_repo(test_dir: str):
    """Remove test repository."""
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def test_dry_run_mode():
    """Test DRY_RUN mode - should not execute."""
    console.print("\n[bold cyan]Test 1: DRY_RUN Mode[/bold cyan]")
    console.print("=" * 60)
    
    executor = CommandExecutor(mode=ExecutionMode.DRY_RUN)
    
    command = CLICommand(
        tool="git_revert",
        args={"commit": "abc123"},
        description="Test revert",
        risk_level="low"
    )
    
    result = executor.execute(command)
    
    console.print(f"Mode: {result['mode']}")
    console.print(f"Executed: {result['executed']}")
    console.print(f"Output: {result['output']}")
    
    assert result['mode'] == 'dry_run'
    assert result['executed'] == False
    assert result['success'] == True
    assert "Would execute" in result['output']
    
    console.print("[green]✓ DRY_RUN mode works correctly[/green]")
    return True


def test_safe_mode_blocking():
    """Test SAFE mode blocks unsafe commands."""
    console.print("\n[bold cyan]Test 2: SAFE Mode (Blocking Unsafe)[/bold cyan]")
    console.print("=" * 60)
    
    executor = CommandExecutor(mode=ExecutionMode.SAFE)
    
    # Try an unsafe command
    unsafe_command = CLICommand(
        tool="service_restart",  # Not in safe list
        args={"service": "test", "namespace": "default"},
        description="Restart service",
        risk_level="high"
    )
    
    result = executor.execute(unsafe_command)
    
    console.print(f"Mode: {result['mode']}")
    console.print(f"Executed: {result['executed']}")
    console.print(f"Success: {result['success']}")
    console.print(f"Error: {result['error']}")
    
    assert result['mode'] == 'safe'
    assert result['executed'] == False
    assert result['success'] == False
    assert "not in safe list" in result['error']
    
    console.print("[green]✓ SAFE mode blocks unsafe commands[/green]")
    return True


def test_real_git_execution():
    """Test FULL mode with real git execution."""
    console.print("\n[bold cyan]Test 3: FULL Mode (Real Git Execution)[/bold cyan]")
    console.print("=" * 60)
    
    # Setup test repository
    test_dir, commit_hash = setup_test_repo()
    console.print(f"Test repo: {test_dir}")
    console.print(f"Commit to revert: {commit_hash[:8]}")
    
    try:
        # Create executor in FULL mode
        executor = CommandExecutor(mode=ExecutionMode.FULL, working_dir=test_dir)
        
        # Execute real git revert
        command = CLICommand(
            tool="git_revert",
            args={"commit": commit_hash},
            description="Revert bad config",
            risk_level="low"
        )
        
        result = executor.execute(command)
        
        console.print(f"\nMode: {result['mode']}")
        console.print(f"Executed: {result['executed']}")
        console.print(f"Success: {result['success']}")
        console.print(f"Command: {result['command']}")
        console.print(f"Output: {result['output'][:200] if result['output'] else 'None'}")
        
        # Verify the revert worked
        if result['success']:
            # Check git status
            status_result = subprocess.run(
                ["git", "status", "--short"],
                cwd=test_dir,
                capture_output=True,
                text=True
            )
            console.print(f"\nGit status after revert:")
            console.print(status_result.stdout or "[no changes]")
            
            # Check file content
            config_file = Path(test_dir) / "config.txt"
            if config_file.exists():
                content = config_file.read_text()
                console.print(f"\nFile content: {content.strip()}")
        
        assert result['mode'] == 'full'
        assert result['executed'] == True
        assert result['success'] == True
        
        console.print("\n[green]✓ Real git execution works![/green]")
        return True
        
    finally:
        cleanup_test_repo(test_dir)


def test_command_not_found():
    """Test handling of non-existent commands."""
    console.print("\n[bold cyan]Test 4: Command Not Found Handling[/bold cyan]")
    console.print("=" * 60)
    
    executor = CommandExecutor(mode=ExecutionMode.FULL)
    
    # Try kubectl command (likely not installed)
    command = CLICommand(
        tool="kubectl_apply",
        args={"file": "test.yaml", "namespace": "default"},
        description="Apply manifest",
        risk_level="low"
    )
    
    result = executor.execute(command)
    
    console.print(f"Executed: {result['executed']}")
    console.print(f"Success: {result['success']}")
    console.print(f"Error: {result['error']}")
    
    # Should handle gracefully
    assert result['executed'] == False or result['success'] == False
    
    console.print("[green]✓ Handles missing commands gracefully[/green]")
    return True


def test_execution_plan():
    """Test executing multiple commands in sequence."""
    console.print("\n[bold cyan]Test 5: Execute Multiple Commands[/bold cyan]")
    console.print("=" * 60)
    
    test_dir, commit_hash = setup_test_repo()
    
    try:
        executor = CommandExecutor(mode=ExecutionMode.FULL, working_dir=test_dir)
        
        commands = [
            CLICommand(
                tool="git_revert",
                args={"commit": commit_hash},
                description="Revert commit",
                risk_level="low"
            ),
        ]
        
        results = executor.execute_plan(commands)
        
        console.print(f"\nExecuted {len(results)} commands")
        for i, result in enumerate(results, 1):
            console.print(f"  Command {i}: {'✓' if result['success'] else '✗'} {result['command']}")
        
        assert len(results) == len(commands)
        
        console.print("\n[green]✓ Multiple command execution works[/green]")
        return True
        
    finally:
        cleanup_test_repo(test_dir)


def main():
    """Run all tests."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Real Execution Test Suite[/bold cyan]\n"
        "Testing actual command execution with git operations",
        border_style="cyan"
    ))
    
    results = []
    
    # Test 1: DRY_RUN mode
    try:
        results.append(("DRY_RUN Mode", test_dry_run_mode()))
    except Exception as e:
        console.print(f"[red]✗ Test 1 failed: {e}[/red]")
        results.append(("DRY_RUN Mode", False))
    
    # Test 2: SAFE mode blocking
    try:
        results.append(("SAFE Mode Blocking", test_safe_mode_blocking()))
    except Exception as e:
        console.print(f"[red]✗ Test 2 failed: {e}[/red]")
        results.append(("SAFE Mode Blocking", False))
    
    # Test 3: Real git execution
    try:
        results.append(("Real Git Execution", test_real_git_execution()))
    except Exception as e:
        console.print(f"[red]✗ Test 3 failed: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        results.append(("Real Git Execution", False))
    
    # Test 4: Command not found
    try:
        results.append(("Command Not Found", test_command_not_found()))
    except Exception as e:
        console.print(f"[red]✗ Test 4 failed: {e}[/red]")
        results.append(("Command Not Found", False))
    
    # Test 5: Multiple commands
    try:
        results.append(("Multiple Commands", test_execution_plan()))
    except Exception as e:
        console.print(f"[red]✗ Test 5 failed: {e}[/red]")
        results.append(("Multiple Commands", False))
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold]Test Summary[/bold]")
    console.print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "[green]✓[/green]" if success else "[red]✗[/red]"
        console.print(f"{status} {name}")
    
    console.print("\n" + "=" * 60)
    if passed == total:
        console.print(f"[bold green]SUCCESS: All {total} tests passed![/bold green]")
    else:
        console.print(f"[bold yellow]PARTIAL: {passed}/{total} tests passed[/bold yellow]")
    console.print("=" * 60)
    
    console.print("\n[cyan]Real execution is now functional![/cyan]")
    console.print("Set EXECUTION_MODE in .env to control behavior:")
    console.print("  • dry_run - Show what would happen (safe)")
    console.print("  • safe - Execute only low-risk commands")
    console.print("  • full - Execute all commands (use with caution)")
    console.print()
    
    return passed == total


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
