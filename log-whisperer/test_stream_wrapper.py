#!/usr/bin/env python3
"""
Test script for stream_wrapper.py
Tests console capture and output streaming
"""
import os
import asyncio
os.environ['DEMO_MODE'] = 'true'

from api.stream_wrapper import capture_output_sync, capture_output_async, capture_console_output
from rich.console import Console

console = Console()

def test_basic_capture():
    """Test basic console capture."""
    print("\n" + "=" * 60)
    print("Test 1: Basic Console Capture")
    print("=" * 60)
    
    def sample_function():
        from viz.terminal_logger import log_event
        log_event("📥", "TEST", "This should be captured", "cyan")
        return "success"
    
    result, output = capture_output_sync(sample_function)
    
    print(f"✓ Result: {result}")
    print(f"✓ Captured {len(output)} characters")
    print(f"✓ Output contains ANSI codes: {chr(27) in output}")
    
    # Show a sample of the output
    print("\nCaptured output (first 200 chars):")
    print(output[:200] + "..." if len(output) > 200 else output)
    
    return len(output) > 0


async def test_async_capture():
    """Test async console capture."""
    print("\n" + "=" * 60)
    print("Test 2: Async Console Capture")
    print("=" * 60)
    
    async def sample_async_function():
        from viz.terminal_logger import log_ingesting, log_diagnosis
        log_ingesting("Loading data...")
        await asyncio.sleep(0.1)
        log_diagnosis("Root cause identified")
        return "async_success"
    
    result, output = await capture_output_async(sample_async_function)
    
    print(f"✓ Result: {result}")
    print(f"✓ Captured {len(output)} characters")
    print(f"✓ Output contains multiple events: {'INGESTING' in output and 'DIAGNOSIS' in output}")
    
    return len(output) > 0


async def test_pipeline_capture():
    """Test capturing full pipeline output."""
    print("\n" + "=" * 60)
    print("Test 3: Pipeline Capture")
    print("=" * 60)
    
    from api.pipeline import Pipeline
    from data.load_incident import load_cloudflare_incident
    
    async def run_pipeline():
        pipeline = Pipeline(
            incident_id='test-001',
            enable_grid=False,
            enable_pretty_logs=True
        )
        log_events = load_cloudflare_incident()
        return await pipeline.run(log_events)
    
    state, output = await capture_output_async(run_pipeline)
    
    print(f"✓ Pipeline Status: {state.status}")
    print(f"✓ Captured {len(output)} characters")
    print(f"✓ Contains council debate: {'Council' in output or 'Agent' in output}")
    print(f"✓ Contains remediation: {'REMEDIATION' in output or 'commands' in output}")
    
    # Show sample
    print("\nCaptured output (first 300 chars):")
    print(output[:300] + "..." if len(output) > 300 else output)
    
    return state.status == "awaiting_approval"


def test_console_restoration():
    """Test that console is properly restored."""
    print("\n" + "=" * 60)
    print("Test 4: Console Restoration")
    print("=" * 60)
    
    from viz.terminal_logger import console as logger_console
    
    # Get original console
    original_console = logger_console
    
    # Capture some output
    with capture_console_output() as capture:
        from viz.terminal_logger import log_event
        log_event("🔧", "TEST", "Inside capture", "blue")
    
    # Check console is restored
    from viz.terminal_logger import console as restored_console
    
    print(f"✓ Console restored: {restored_console is not capture.console}")
    print(f"✓ Original console type: {type(original_console)}")
    
    return True


async def test_mock_websocket():
    """Test with a mock WebSocket."""
    print("\n" + "=" * 60)
    print("Test 5: Mock WebSocket Streaming")
    print("=" * 60)
    
    class MockWebSocket:
        def __init__(self):
            self.messages = []
        
        async def send_text(self, text: str):
            self.messages.append(text)
            print(f"  → Sent {len(text)} chars to WebSocket")
    
    from api.stream_wrapper import stream_to_websocket
    
    async def sample_task():
        from viz.terminal_logger import log_event
        log_event("🚀", "START", "Task started", "green")
        await asyncio.sleep(0.2)
        log_event("✅", "DONE", "Task completed", "green")
        return "task_result"
    
    ws = MockWebSocket()
    result = await stream_to_websocket(ws, sample_task)
    
    print(f"✓ Result: {result}")
    print(f"✓ WebSocket messages sent: {len(ws.messages)}")
    print(f"✓ Total characters streamed: {sum(len(m) for m in ws.messages)}")
    
    return len(ws.messages) > 0


async def main():
    """Run all tests."""
    console.print("\n[bold cyan]Stream Wrapper Test Suite[/bold cyan]")
    console.print("=" * 60)
    
    results = []
    
    # Test 1: Basic capture
    try:
        results.append(("Basic Capture", test_basic_capture()))
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
        results.append(("Basic Capture", False))
    
    # Test 2: Async capture
    try:
        results.append(("Async Capture", await test_async_capture()))
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
        results.append(("Async Capture", False))
    
    # Test 3: Pipeline capture
    try:
        results.append(("Pipeline Capture", await test_pipeline_capture()))
    except Exception as e:
        print(f"✗ Test 3 failed: {e}")
        results.append(("Pipeline Capture", False))
    
    # Test 4: Console restoration
    try:
        results.append(("Console Restoration", test_console_restoration()))
    except Exception as e:
        print(f"✗ Test 4 failed: {e}")
        results.append(("Console Restoration", False))
    
    # Test 5: Mock WebSocket
    try:
        results.append(("Mock WebSocket", await test_mock_websocket()))
    except Exception as e:
        print(f"✗ Test 5 failed: {e}")
        results.append(("Mock WebSocket", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✓" if success else "✗"
        print(f"{status} {name}")
    
    print("\n" + "=" * 60)
    if passed == total:
        print(f"[SUCCESS] All {total} tests passed!")
    else:
        print(f"[PARTIAL] {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == '__main__':
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted")
        exit(1)
