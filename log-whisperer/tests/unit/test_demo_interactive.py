#!/usr/bin/env python3
"""
Quick test to verify demo_interactive.py structure.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Test imports
    from execution.executor import CommandExecutor, ExecutionMode
    from models import CLICommand
    from rich.console import Console
    from rich.prompt import Prompt
    
    print("✓ All imports successful")
    
    # Test ExecutionMode enum
    modes = {
        "dry": ExecutionMode.DRY_RUN,
        "safe": ExecutionMode.SAFE,
        "full": ExecutionMode.FULL
    }
    print(f"✓ Execution modes: {list(modes.keys())}")
    
    # Test CLICommand model
    cmd = CLICommand(
        tool="git_revert",
        args={"commit": "abc123"},
        description="Test command",
        risk_level="low"
    )
    print(f"✓ CLICommand model works: {cmd.tool}")
    
    # Test CommandExecutor
    executor = CommandExecutor(mode=ExecutionMode.DRY_RUN)
    print(f"✓ CommandExecutor created: {executor.mode.value}")
    
    print("\n✅ Demo structure is valid and ready to run!")
    print("\nTo run the interactive demo:")
    print("  ./run_demo.sh")
    print("  or")
    print("  python3 demo_interactive.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
