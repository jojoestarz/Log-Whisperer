import json
import os
from llm_client import get_llm_client
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from models import FaultReport, CouncilDebate

console = Console()

# Agent system prompts
AGENT_A_PROMPT = """You are a conservative SRE. Analyze these logs looking for config changes that could cause outages. Output JSON: {"hypothesis": "str", "confidence": 0.0-1.0, "reasoning": "str"}"""

AGENT_B_PROMPT = """You are a network specialist. Analyze these logs for BGP/routing failures. Output JSON: {"hypothesis": "str", "confidence": 0.0-1.0, "reasoning": "str"}"""

AGENT_C_PROMPT = """You are a chaos engineer. Analyze these logs for cascading failure patterns. Output JSON: {"hypothesis": "str", "confidence": 0.0-1.0, "reasoning": "str"}"""

CONSENSUS_PROMPT = """Given these 3 hypotheses from different experts, determine the most likely root cause. Output JSON:
{
  "root_cause": "one sentence describing the exact cause",
  "affected_services": ["service1", "service2"],
  "severity": "P1" | "P2" | "P3",
  "fix_type": "config_rollback" | "service_restart" | "route_fix" | "cert_renewal" | "scale_up",
  "confidence": 0.0-1.0,
  "summary": "2-3 sentence summary",
  "time_of_failure": "ISO timestamp"
}"""

# Cached debate for DEMO_MODE
CACHED_DEBATE = [
    CouncilDebate(
        agent_name="Agent A (Conservative SRE)",
        hypothesis="Config 4821 contains empty string",
        confidence=0.95,
        reasoning="Logs show validation SKIPPED immediately before withdrawal"
    ),
    CouncilDebate(
        agent_name="Agent B (Network Specialist)",
        hypothesis="BGP route withdrawal cascade",
        confidence=0.92,
        reasoning="Sequence shows lon01 -> iad01 propagation pattern"
    ),
    CouncilDebate(
        agent_name="Agent C (Chaos Engineer)",
        hypothesis="Cascading failure from config error",
        confidence=0.88,
        reasoning="Single point of failure cascaded to all services"
    )
]

CACHED_FAULT_REPORT = FaultReport(
    root_cause="Empty-string config in BGP deployment 4821 triggered bulk route withdrawal",
    affected_services=["bgp-router-lon01", "bgp-router-iad01", "api-gateway", "dns-resolver", "cdn-edge"],
    severity="P1",
    fix_type="config_rollback",
    confidence=0.89,
    summary="BGP config 4821 with empty prefix list caused cascading route withdrawal across all edge routers",
    time_of_failure="2022-06-21T06:27:12Z",
    debate_summary=CACHED_DEBATE
)


def display_debate(debates: list[CouncilDebate]):
    """Display the council debate with colored panels and confidence bars."""
    colors = ["cyan", "yellow", "magenta"]
    
    console.print("\n[bold white]🏛️  Council Debate in Progress[/bold white]")
    console.print("[dim]Three agents analyzing the incident...[/dim]\n")
    
    for i, debate in enumerate(debates):
        color = colors[i % len(colors)]
        
        # Create panel with agent's position
        panel_content = f"[bold]{debate.hypothesis}[/bold]\n\n"
        panel_content += f"[dim]Reasoning:[/dim] {debate.reasoning}\n\n"
        panel_content += f"[dim]Confidence:[/dim] {debate.confidence:.0%}"
        
        panel = Panel(
            panel_content,
            title=f"[{color}]{debate.agent_name}[/{color}]",
            border_style=color
        )
        console.print(panel)
        
        # Show confidence bar
        bar_length = int(debate.confidence * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        console.print(f"[{color}]{bar}[/{color}] {debate.confidence:.0%}\n")


def hold_council_debate(logs: list[dict]) -> FaultReport:
    """
    Hold a multi-agent debate to determine root cause.
    
    Args:
        logs: List of log event dictionaries
        
    Returns:
        FaultReport with debate_summary included
    """
    # Check DEMO_MODE
    if os.getenv('DEMO_MODE') == 'true':
        console.print("[yellow]DEMO_MODE enabled - using cached debate[/yellow]\n")
        display_debate(CACHED_DEBATE)
        
        # Display consensus
        consensus_panel = Panel(
            f"[bold]{CACHED_FAULT_REPORT.root_cause}[/bold]\n\n"
            f"[dim]Severity:[/dim] {CACHED_FAULT_REPORT.severity}\n"
            f"[dim]Confidence:[/dim] {CACHED_FAULT_REPORT.confidence:.0%}\n"
            f"[dim]Affected Services:[/dim] {len(CACHED_FAULT_REPORT.affected_services)}",
            title="[bold green]✓ Consensus Reached[/bold green]",
            border_style="green"
        )
        console.print(consensus_panel)
        
        return CACHED_FAULT_REPORT
    
    # Real API mode - simulate debate
    try:
        client = get_llm_client()
        
        # Format logs for API
        logs_text = "\n".join([
            f"[{log['timestamp']}] [{log['level']}] {log['service']}: {log['message']}"
            for log in logs
        ])
        
        debates = []
        agents = [
            ("Agent A (Conservative SRE)", AGENT_A_PROMPT, "cyan"),
            ("Agent B (Network Specialist)", AGENT_B_PROMPT, "yellow"),
            ("Agent C (Chaos Engineer)", AGENT_C_PROMPT, "magenta")
        ]
        
        console.print("\n[bold white]🏛️  Initiating Council Debate[/bold white]")
        console.print("[dim]Consulting 3 expert agents...[/dim]\n")
        
        # Step 1: Get each agent's hypothesis
        for agent_name, system_prompt, color in agents:
            console.print(f"[{color}]Consulting {agent_name}...[/{color}]")
            
            response_text = client.create_message(
                model="claude-sonnet-4-20250514",  # Will be mapped to Gemini model
                max_tokens=500,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"Analyze these incident logs:\n\n{logs_text}"
                }]
            )
            
            # Parse response with better error handling
            raw = response_text.strip()
            
            # Remove markdown code blocks
            if raw.startswith("```"):
                first_newline = raw.find('\n')
                if first_newline != -1:
                    raw = raw[first_newline+1:]
                raw = raw.rstrip("```").strip()
            
            # Try to extract JSON if it's embedded
            if not raw.startswith('{'):
                start = raw.find('{')
                end = raw.rfind('}')
                if start != -1 and end != -1:
                    raw = raw[start:end+1]
            
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as je:
                console.print(f"[red]JSON parse error from {agent_name}: {je}[/red]")
                console.print(f"[dim]Response preview: {raw[:200]}...[/dim]")
                # Use fallback data
                data = {
                    "hypothesis": "Unable to parse response",
                    "confidence": 0.5,
                    "reasoning": f"JSON parsing failed: {str(je)}"
                }
            
            debate = CouncilDebate(
                agent_name=agent_name,
                hypothesis=data.get('hypothesis', 'Unknown'),
                confidence=data.get('confidence', 0.5),
                reasoning=data.get('reasoning', 'No reasoning provided')
            )
            debates.append(debate)
            console.print(f"[{color}]✓ {agent_name} analysis complete[/{color}]\n")
        
        # Display the debate
        display_debate(debates)
        
        # Step 2: Reach consensus
        console.print("\n[bold white]🤝 Reaching Consensus...[/bold white]\n")
        
        debate_summary = "\n".join([
            f"{d.agent_name}: {d.hypothesis} (confidence: {d.confidence:.0%})\nReasoning: {d.reasoning}"
            for d in debates
        ])
        
        consensus_text = client.create_message(
            model="claude-sonnet-4-20250514",  # Will be mapped to Gemini model
            max_tokens=1000,
            system=CONSENSUS_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Expert hypotheses:\n\n{debate_summary}\n\nOriginal logs:\n{logs_text}"
            }]
        )
        
        # Parse consensus with better error handling
        raw = consensus_text.strip()
        
        # Remove markdown code blocks
        if raw.startswith("```"):
            first_newline = raw.find('\n')
            if first_newline != -1:
                raw = raw[first_newline+1:]
            raw = raw.rstrip("```").strip()
        
        # Try to extract JSON if it's embedded
        if not raw.startswith('{'):
            start = raw.find('{')
            end = raw.rfind('}')
            if start != -1 and end != -1:
                raw = raw[start:end+1]
        
        try:
            consensus_data = json.loads(raw)
        except json.JSONDecodeError as je:
            console.print(f"[red]Consensus JSON parse error: {je}[/red]")
            console.print(f"[dim]Response preview: {raw[:200]}...[/dim]")
            raise
        
        # Create FaultReport with debate summary
        fault_report = FaultReport(
            **consensus_data,
            debate_summary=debates
        )
        
        # Display consensus
        consensus_panel = Panel(
            f"[bold]{fault_report.root_cause}[/bold]\n\n"
            f"[dim]Severity:[/dim] {fault_report.severity}\n"
            f"[dim]Confidence:[/dim] {fault_report.confidence:.0%}\n"
            f"[dim]Affected Services:[/dim] {len(fault_report.affected_services)}",
            title="[bold green]✓ Consensus Reached[/bold green]",
            border_style="green"
        )
        console.print(consensus_panel)
        
        return fault_report
        
    except Exception as e:
        # Error handling: fallback to cached response
        console.print(f"[red]API Error: {e}[/red]")
        console.print("[yellow]Falling back to cached debate[/yellow]\n")
        
        display_debate(CACHED_DEBATE)
        
        consensus_panel = Panel(
            f"[bold]{CACHED_FAULT_REPORT.root_cause}[/bold]\n\n"
            f"[dim]Severity:[/dim] {CACHED_FAULT_REPORT.severity}\n"
            f"[dim]Confidence:[/dim] {CACHED_FAULT_REPORT.confidence:.0%}",
            title="[bold green]✓ Consensus Reached (Cached)[/bold green]",
            border_style="green"
        )
        console.print(consensus_panel)
        
        return CACHED_FAULT_REPORT


# Async wrapper for pipeline compatibility
async def analyze_incident(log_events: list[dict]) -> FaultReport:
    """Async wrapper for pipeline compatibility."""
    return hold_council_debate(log_events)
