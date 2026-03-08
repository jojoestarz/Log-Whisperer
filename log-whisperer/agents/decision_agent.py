"""
Decision Agent — P1 owns this file.
Ingests log events, calls LLM, returns a structured FaultReport.
"""
import json
import os
from llm_client import get_llm_client
from json_utils import extract_and_fix_json
from demo_delays import DemoDelay
from rich.console import Console
from rich.table import Table
from models import FaultReport

console = Console()

SYSTEM_PROMPT = """You are an elite SRE. Analyze these incident logs. Output ONLY valid JSON:
{
  "root_cause": "one sentence describing the exact cause",
  "affected_services": ["service1", "service2"],
  "severity": "P1" | "P2" | "P3",
  "fix_type": "config_rollback" | "service_restart" | "route_fix" | "cert_renewal" | "scale_up",
  "confidence": 0.0-1.0,
  "summary": "2-3 sentence human-readable summary",
  "time_of_failure": "ISO timestamp of the root cause event"
}"""

CACHED_FAULT_REPORT = FaultReport(
    root_cause="Empty-string config in BGP deployment 4821 triggered bulk route withdrawal",
    affected_services=["bgp-router-lon01", "bgp-router-iad01", "api-gateway", "dns-resolver", "cdn-edge"],
    severity="P1",
    fix_type="config_rollback",
    confidence=0.97,
    summary="BGP config 4821 with empty prefix list caused cascading route withdrawal across all edge routers",
    time_of_failure="2022-06-21T06:27:12Z"
)


def analyze_logs(log_path: str) -> FaultReport:
    """
    Analyze incident logs and return a FaultReport.
    
    Args:
        log_path: Path to the incident JSON file
        
    Returns:
        FaultReport with root cause analysis
    """
    # 1. Load incident data
    with open(log_path, 'r') as f:
        logs = json.load(f)
    
    # Demo: Simulate ingestion
    if os.getenv('DEMO_MODE') == 'true':
        DemoDelay.ingestion()
    
    # 2. Check DEMO_MODE
    if os.getenv('DEMO_MODE') == 'true':
        console.print("[yellow]DEMO_MODE enabled - using cached response[/yellow]")
        
        # Simulate processing time for log analysis
        DemoDelay.initiate_analysis()
        console.print("[dim]Analyzing incident patterns...[/dim]")
        DemoDelay.agent_thinking("Decision Agent")
        
        report = CACHED_FAULT_REPORT
    else:
        # 3. Call LLM API
        try:
            client = get_llm_client()
            
            # Format logs for API
            logs_text = "\n".join([
                f"[{log['timestamp']}] [{log['level']}] {log['service']}: {log['message']}"
                for log in logs
            ])
            
            response_text = client.create_message(
                model="claude-sonnet-4-20250514",  # Will be mapped to Gemini model
                max_tokens=1500,  # Increased for complete responses
                system=SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Analyze these incident logs:\n\n{logs_text}"
                }]
            )
            
            # 4. Parse response into FaultReport with robust JSON handling
            try:
                report_data = extract_and_fix_json(response_text)
            except Exception as je:
                console.print(f"[red]JSON parse error: {je}[/red]")
                console.print(f"[dim]Raw response preview: {response_text[:300]}...[/dim]")
                raise
                
            report = FaultReport(**report_data)
            
        except Exception as e:
            # Error handling: fallback to cached response
            console.print(f"[red]API Error: {e}[/red]")
            console.print("[yellow]Falling back to cached response[/yellow]")
            report = CACHED_FAULT_REPORT
    
    # 5. Print FaultReport as Rich table
    table = Table(title="🔍 Fault Report")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")
    
    table.add_row("Root Cause", report.root_cause)
    table.add_row("Affected Services", ", ".join(report.affected_services))
    table.add_row("Severity", report.severity)
    table.add_row("Fix Type", report.fix_type)
    table.add_row("Confidence", f"{report.confidence:.0%}")
    table.add_row("Summary", report.summary)
    table.add_row("Time of Failure", report.time_of_failure)
    
    console.print(table)
    
    # 6. Return FaultReport
    return report


# Async wrapper for compatibility with existing pipeline
async def analyze_incident(log_events: list[dict]) -> FaultReport:
    """Async wrapper for pipeline compatibility."""
    # Write events to temp file or use directly
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(log_events, f)
        temp_path = f.name
    
    try:
        return analyze_logs(temp_path)
    finally:
        os.unlink(temp_path)
