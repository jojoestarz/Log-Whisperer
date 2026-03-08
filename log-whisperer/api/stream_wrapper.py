"""
Stream Wrapper - Captures Rich console output and streams to WebSocket.
Monkey-patches global console objects to capture ANSI output without modifying existing code.
"""
import asyncio
import io
from typing import Callable, Any, Awaitable
from contextlib import contextmanager
from rich.console import Console


class ConsoleCapture:
    """Captures Rich console output to a buffer."""
    
    def __init__(self):
        self.buffer = io.StringIO()
        self.console = Console(file=self.buffer, force_terminal=True, width=120)
        self.original_consoles = {}
    
    def get_output(self) -> str:
        """Get captured output and clear buffer."""
        output = self.buffer.getvalue()
        self.buffer.truncate(0)
        self.buffer.seek(0)
        return output
    
    def patch_module_console(self, module, attr_name: str = 'console'):
        """Patch a console in a specific module."""
        if hasattr(module, attr_name):
            original = getattr(module, attr_name)
            self.original_consoles[id(module)] = (module, attr_name, original)
            setattr(module, attr_name, self.console)
    
    def restore_all(self):
        """Restore all patched consoles."""
        for module, attr_name, original in self.original_consoles.values():
            setattr(module, attr_name, original)
        self.original_consoles.clear()


@contextmanager
def capture_console_output():
    """
    Context manager that captures all Rich console output.
    Patches console objects in all relevant modules.
    """
    capture = ConsoleCapture()
    
    # Import modules that use console
    try:
        from agents import council_agent
        from agents import writer_agent
        from viz import terminal_logger
        
        # Patch all console instances
        capture.patch_module_console(council_agent, 'console')
        capture.patch_module_console(writer_agent, 'console')
        capture.patch_module_console(terminal_logger, 'console')
        
    except ImportError as e:
        # Modules might not exist yet, that's okay
        pass
    
    try:
        yield capture
    finally:
        # Always restore original consoles
        capture.restore_all()


async def stream_to_websocket(
    websocket,
    async_func: Callable[..., Awaitable[Any]],
    *args,
    **kwargs
) -> Any:
    """
    Run an async function while streaming its Rich console output to a WebSocket.
    
    Args:
        websocket: WebSocket connection to stream to
        async_func: Async function to execute
        *args, **kwargs: Arguments to pass to async_func
        
    Returns:
        Result from async_func
        
    Example:
        async def my_pipeline():
            # Uses rich console internally
            console.print("[green]Starting...[/green]")
            return "done"
        
        result = await stream_to_websocket(websocket, my_pipeline)
    """
    with capture_console_output() as capture:
        # Create task for the async function
        task = asyncio.create_task(async_func(*args, **kwargs))
        
        # Stream output while task runs
        while not task.done():
            # Get any new output
            output = capture.get_output()
            if output:
                try:
                    await websocket.send_text(output)
                except Exception as e:
                    # WebSocket closed, cancel task
                    task.cancel()
                    raise
            
            # Small delay to avoid busy loop
            await asyncio.sleep(0.1)
        
        # Get final output
        output = capture.get_output()
        if output:
            await websocket.send_text(output)
        
        # Return the result
        return await task


async def stream_pipeline_to_websocket(
    websocket,
    incident_id: str,
    log_events: list[dict],
    enable_grid: bool = False,
    enable_pretty_logs: bool = True
):
    """
    Stream a pipeline execution to WebSocket.
    
    Args:
        websocket: WebSocket connection
        incident_id: Incident identifier
        log_events: Log events to analyze
        enable_grid: Enable grid updates (default: False for WebSocket)
        enable_pretty_logs: Enable pretty logging (default: True)
        
    Returns:
        PipelineState after execution
        
    Example:
        from fastapi import WebSocket
        
        @app.websocket("/ws/pipeline")
        async def pipeline_endpoint(websocket: WebSocket):
            await websocket.accept()
            
            logs = load_cloudflare_incident()
            state = await stream_pipeline_to_websocket(
                websocket,
                incident_id="ws-001",
                log_events=logs
            )
            
            await websocket.send_json({
                "status": "complete",
                "incident_id": state.incident_id,
                "severity": state.fault_report.severity
            })
    """
    from api.pipeline import Pipeline
    
    # Create pipeline
    pipeline = Pipeline(
        incident_id=incident_id,
        enable_grid=enable_grid,
        enable_pretty_logs=enable_pretty_logs
    )
    
    # Stream the pipeline execution
    state = await stream_to_websocket(
        websocket,
        pipeline.run,
        log_events
    )
    
    return state


# Synchronous wrapper for testing
def capture_output_sync(func: Callable, *args, **kwargs) -> tuple[Any, str]:
    """
    Synchronous version - captures output and returns it with result.
    
    Args:
        func: Function to execute
        *args, **kwargs: Arguments to pass to func
        
    Returns:
        Tuple of (result, captured_output)
        
    Example:
        def my_function():
            console.print("[green]Hello[/green]")
            return 42
        
        result, output = capture_output_sync(my_function)
        print(f"Result: {result}")
        print(f"Output: {output}")
    """
    with capture_console_output() as capture:
        result = func(*args, **kwargs)
        output = capture.get_output()
        return result, output


# Async version for testing
async def capture_output_async(
    async_func: Callable[..., Awaitable[Any]],
    *args,
    **kwargs
) -> tuple[Any, str]:
    """
    Async version - captures output and returns it with result.
    
    Args:
        async_func: Async function to execute
        *args, **kwargs: Arguments to pass to async_func
        
    Returns:
        Tuple of (result, captured_output)
        
    Example:
        async def my_async_function():
            console.print("[green]Hello[/green]")
            return 42
        
        result, output = await capture_output_async(my_async_function)
        print(f"Result: {result}")
        print(f"Output: {output}")
    """
    with capture_console_output() as capture:
        result = await async_func(*args, **kwargs)
        output = capture.get_output()
        return result, output
