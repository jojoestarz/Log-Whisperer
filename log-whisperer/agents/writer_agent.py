"""
Writer Agent — P1 owns this file.
Receives FaultReport, returns RemediationPlan with CLI commands.
"""
import json
import os
import uuid
from llm_client import get_llm_client
from json_utils import extract_and_fix_json
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from models import FaultReport, RemediationPlan, CLICommand

console = Console()

SYSTEM_PROMPT = """Given root cause, generate exactly 3 CLI commands to remediate.
Available tools: git_revert, kubectl_apply, kubectl_scale, argo_sync, service_restart.
Output JSON:
{
  "commands": [
    {"tool": "git_revert", "args": {"commit": "abc123"}, "description": "...", "risk_level": "low"},
    {"tool": "kubectl_apply", "args": {"file": "..."}, "description": "...", "risk_level": "low"},
    {"tool": "argo_sync", "args": {"app": "..."}, "description": "...", "risk_level": "low"}
  ],
  "rollback_commands": [{"tool": "git_revert", "args": {"commit": "..."}, "description": "...", "risk_level": "medium"}],
  "estimated_recovery_mins": 5,
  "overall_risk": "low"
}"""

# Cached plan for DEMO_MODE
CACHED_PLAN = RemediationPlan(
    plan_id="demo-plan-001",
    commands=[
        CLICommand(
            tool="git_revert",
            args={"commit": "abc123def456"},
            description="Revert BGP config deployment 4821",
            risk_level="low"
        ),
        CLICommand(
            tool="kubectl_apply",
            args={"file": "manifests/bgp-config-fix.yaml"},
            description="Apply corrected BGP configuration",
            risk_level="low"
        ),
        CLICommand(
            tool="argo_sync",
            args={"app": "bgp-router", "prune": "true"},
            description="Sync Argo CD to deploy fix",
            risk_level="low"
        ),
    ],
    rollback_commands=[
        CLICommand(
            tool="git_revert",
            args={"commit": "previous"},
            description="Emergency rollback if fix fails",
            risk_level="medium"
        ),
    ],
    estimated_recovery_mins=5,
    overall_risk="low"
)


def generate_plan(fault: FaultReport) -> RemediationPlan:
    """
    Generate a remediation plan from a fault report.
    
    Args:
        fault: FaultReport from decision agent
        
    Returns:
        RemediationPlan with exactly 3 commands
    """
    # 1. Check DEMO_MODE
    if os.getenv('DEMO_MODE') == 'true':
        console.print("[yellow]DEMO_MODE enabled - using cached plan[/yellow]")
        plan = CACHED_PLAN.model_copy()
    else:
        # 2. Call LLM API
        try:
            client = get_llm_client()
            
            prompt = f"""Given root cause: {fault.root_cause}
Severity: {fault.severity}
Affected services: {', '.join(fault.affected_services)}
Fix type: {fault.fix_type}

Generate exactly 3 CLI commands to remediate."""
            
            response_text = client.create_message(
                model="claude-sonnet-4-20250514",  # Will be mapped to Gemini model
                max_tokens=2500,  # Increased significantly for complete responses
                system=SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # 3. Parse response with robust JSON handling
            console.print(f"[dim]Parsing response ({len(response_text)} chars)...[/dim]")
            
            try:
                data = extract_and_fix_json(response_text)
            except Exception as je:
                console.print(f"[red]JSON parse error: {je}[/red]")
                console.print(f"[dim]Raw response preview: {response_text[:300]}...[/dim]")
                raise
            
            # Validate: must have exactly 3 commands
            if len(data.get('commands', [])) != 3:
                raise ValueError(f"Expected exactly 3 commands, got {len(data.get('commands', []))}")
            
            plan = RemediationPlan(
                plan_id=f"plan-{uuid.uuid4().hex[:8]}",
                **data
            )
            
        except Exception as e:
            console.print(f"[red]API Error: {e}[/red]")
            console.print("[yellow]Falling back to cached plan[/yellow]")
            plan = CACHED_PLAN.model_copy()
            plan.plan_id = f"plan-{uuid.uuid4().hex[:8]}"
    
    # 4. Display commands with syntax highlighting
    command_displays = []
    for i, cmd in enumerate(plan.commands, 1):
        # Convert command to bash-like string
        if cmd.tool == "git_revert":
            bash_cmd = f"git revert {cmd.args.get('commit', '')} --no-commit"
        elif cmd.tool == "kubectl_apply":
            bash_cmd = f"kubectl apply -f {cmd.args.get('file', '')}"
        elif cmd.tool == "kubectl_scale":
            bash_cmd = f"kubectl scale {cmd.args.get('resource', '')} --replicas={cmd.args.get('replicas', '3')}"
        elif cmd.tool == "argo_sync":
            app = cmd.args.get('app', '')
            prune = cmd.args.get('prune', 'false')
            prune_flag = " --prune" if prune == "true" else ""
            bash_cmd = f"argocd app sync {app}{prune_flag}"
        elif cmd.tool == "service_restart":
            bash_cmd = f"kubectl rollout restart deployment/{cmd.args.get('service', '')} -n {cmd.args.get('namespace', 'default')}"
        else:
            bash_cmd = f"{cmd.tool} {' '.join(f'{k}={v}' for k, v in cmd.args.items())}"
        
        # 5. Create syntax-highlighted display
        syntax = Syntax(bash_cmd, "bash", theme="monokai", line_numbers=False)
        command_displays.append(f"Command {i} ({cmd.risk_level} risk): {cmd.description}")
        command_displays.append(syntax)
    
    # 6. Wrap in Panel
    panel_content = "\n".join([
        f"Plan ID: {plan.plan_id}",
        f"Overall Risk: {plan.overall_risk}",
        f"Estimated Recovery: {plan.estimated_recovery_mins} minutes",
        f"Commands: {len(plan.commands)}",
        ""
    ])
    
    console.print(Panel(panel_content, title="⚙️ Remediation Plan", border_style="green"))
    
    # Display each command
    for i, cmd in enumerate(plan.commands, 1):
        if cmd.tool == "git_revert":
            bash_cmd = f"git revert {cmd.args.get('commit', '')} --no-commit"
        elif cmd.tool == "kubectl_apply":
            bash_cmd = f"kubectl apply -f {cmd.args.get('file', '')}"
        elif cmd.tool == "kubectl_scale":
            bash_cmd = f"kubectl scale {cmd.args.get('resource', '')} --replicas={cmd.args.get('replicas', '3')}"
        elif cmd.tool == "argo_sync":
            app = cmd.args.get('app', '')
            prune = cmd.args.get('prune', 'false')
            prune_flag = " --prune" if prune == "true" else ""
            bash_cmd = f"argocd app sync {app}{prune_flag}"
        elif cmd.tool == "service_restart":
            bash_cmd = f"kubectl rollout restart deployment/{cmd.args.get('service', '')} -n {cmd.args.get('namespace', 'default')}"
        else:
            bash_cmd = f"{cmd.tool}"
        
        console.print(f"\n[cyan]Command {i}[/cyan] ({cmd.risk_level} risk): {cmd.description}")
        console.print(Syntax(bash_cmd, "bash", theme="monokai", line_numbers=False))
    
    return plan


# Async wrapper for compatibility with existing pipeline
async def generate_remediation_plan(fault: FaultReport) -> RemediationPlan:
    """Async wrapper for pipeline compatibility."""
    return generate_plan(fault)
