#!/usr/bin/env python3
"""
Quick verification for stream_wrapper implementation
"""
import os
os.environ['DEMO_MODE'] = 'true'

from rich.console import Console
from rich.panel import Panel

console = Console()

console.print("\n")
console.print(Panel.fit(
    "[bold cyan]Stream Wrapper Verification[/bold cyan]",
    border_style="cyan"
))

results = []

# Test 1: Import check
console.print("\n[yellow]Test 1:[/yellow] Checking imports...")
try:
    from api.stream_wrapper import (
        ConsoleCapture,
        capture_console_output,
        stream_to_websocket,
        stream_pipeline_to_websocket,
        capture_output_sync,
        capture_output_async
    )
    console.print("[green]✓[/green] All imports successful")
    results.append(("Imports", True))
except Exception as e:
    console.print(f"[red]✗[/red] Import failed: {e}")
    results.append(("Imports", False))

# Test 2: ConsoleCapture class
console.print("\n[yellow]Test 2:[/yellow] Testing ConsoleCapture class...")
try:
    from api.stream_wrapper import ConsoleCapture
    
    capture = ConsoleCapture()
    assert hasattr(capture, 'buffer')
    assert hasattr(capture, 'console')
    assert hasattr(capture, 'patch_module_console')
    assert hasattr(capture, 'restore_all')
    
    console.print("[green]✓[/green] ConsoleCapture class structure valid")
    results.append(("ConsoleCapture", True))
except Exception as e:
    console.print(f"[red]✗[/red] ConsoleCapture test failed: {e}")
    results.append(("ConsoleCapture", False))

# Test 3: Context manager
console.print("\n[yellow]Test 3:[/yellow] Testing context manager...")
try:
    from api.stream_wrapper import capture_console_output
    
    with capture_console_output() as capture:
        # Inside context
        assert capture is not None
        assert hasattr(capture, 'get_output')
    
    # Outside context - should be restored
    console.print("[green]✓[/green] Context manager works")
    results.append(("Context Manager", True))
except Exception as e:
    console.print(f"[red]✗[/red] Context manager failed: {e}")
    results.append(("Context Manager", False))

# Test 4: Basic capture
console.print("\n[yellow]Test 4:[/yellow] Testing basic capture...")
try:
    from api.stream_wrapper import capture_output_sync
    
    def test_func():
        from viz.terminal_logger import log_event
        log_event("🧪", "TEST", "Capture test", "blue")
        return "success"
    
    result, output = capture_output_sync(test_func)
    
    assert result == "success"
    assert len(output) > 0
    assert "TEST" in output or "Capture" in output
    
    console.print(f"[green]✓[/green] Captured {len(output)} characters")
    results.append(("Basic Capture", True))
except Exception as e:
    console.print(f"[red]✗[/red] Basic capture failed: {e}")
    results.append(("Basic Capture", False))

# Test 5: Async capture
console.print("\n[yellow]Test 5:[/yellow] Testing async capture...")
try:
    import asyncio
    from api.stream_wrapper import capture_output_async
    
    async def test_async():
        from viz.terminal_logger import log_event
        log_event("⚡", "ASYNC", "Async test", "yellow")
        return "async_success"
    
    result, output = asyncio.run(capture_output_async(test_async))
    
    assert result == "async_success"
    assert len(output) > 0
    
    console.print(f"[green]✓[/green] Async capture works")
    results.append(("Async Capture", True))
except Exception as e:
    console.print(f"[red]✗[/red] Async capture failed: {e}")
    results.append(("Async Capture", False))

# Test 6: WebSocket endpoint exists
console.print("\n[yellow]Test 6:[/yellow] Checking WebSocket endpoint...")
try:
    from api.websocket_endpoint import app, pipeline_websocket
    
    assert app is not None
    assert pipeline_websocket is not None
    
    console.print("[green]✓[/green] WebSocket endpoint exists")
    results.append(("WebSocket Endpoint", True))
except Exception as e:
    console.print(f"[red]✗[/red] WebSocket endpoint check failed: {e}")
    results.append(("WebSocket Endpoint", False))

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
console.print("\n[cyan]Stream Wrapper Features:[/cyan]")
console.print("  • Console capture via monkey-patching")
console.print("  • StringIO buffer for output")
console.print("  • Context manager for safe restoration")
console.print("  • WebSocket streaming support")
console.print("  • Async function support")
console.print("  • ANSI code preservation")
console.print("  • Pipeline integration")

console.print("\n[cyan]To test WebSocket streaming:[/cyan]")
console.print("  python api/websocket_endpoint.py")
console.print("  # Then open http://localhost:8000")

console.print("\n[cyan]To run full test suite:[/cyan]")
console.print("  python test_stream_wrapper.py")

console.print()
