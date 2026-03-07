"""Writer Agent — generates remediation via MCP tools"""
import anthropic
import json
import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import FaultReport, RemediationPlan
from config import ANTHROPIC_API_KEY, DEMO_MODE, MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Import MCP tools - THIS IS THE KEY INTEGRATION
from tools.mcp_tools import argo_sync, kubectl_scale, service_restart

WRITER_SYSTEM = """You are an SRE remediation expert using MCP tools.
Given a root cause, determine which MCP tools to invoke.
Available tools: argo_sync, kubectl_scale, service_restart
Respond ONLY with valid JSON. No markdown. No backticks.
Schema: {"tool_calls": [
  {"tool": "argo_sync", "args": {"app_name": "byoip-cleanup", "prune": "false"}},
  {"tool": "kubectl_scale", "args": {"deployment": "bgp-config-deployer", "replicas": 0, "namespace": "default"}},
  {"tool": "service_restart", "args": {"service": "bgp-router", "namespace": "edge"}}
], "safety_level": "sandboxed", "risk_score": 0.08}"""

# Cached MCP tool calls for DEMO_MODE
CACHED_TOOL_CALLS = [
    {"tool": "argo_sync", "args": {"app_name": "byoip-cleanup", "prune": "false"}},
    {"tool": "kubectl_scale", "args": {"deployment": "bgp-config-deployer", "replicas": 0, "namespace": "default"}},
    {"tool": "service_restart", "args": {"service": "bgp-router", "namespace": "edge"}}
]


async def execute_mcp_tool(tool_name: str, args: dict) -> dict:
    """Execute an MCP tool and return result"""
    if tool_name == "argo_sync":
        return await argo_sync(args.get("app_name"), args.get("prune", "false"))
    elif tool_name == "kubectl_scale":
        return await kubectl_scale(args.get("deployment"), args.get("replicas"), args.get("namespace", "default"))
    elif tool_name == "service_restart":
        return await service_restart(args.get("service"), args.get("namespace", "default"))
    else:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}


async def generate_plan(fault: FaultReport) -> RemediationPlan:
    """Generate remediation plan using MCP tools"""
    
    # Get tool calls from LLM or use cached
    if DEMO_MODE:
        tool_calls = CACHED_TOOL_CALLS
        risk_score = 0.08
    else:
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=500,
                system=WRITER_SYSTEM,
                messages=[{
                    "role": "user",
                    "content": f"Root cause: {fault.root_cause}\nAffected: {fault.affected_services}"
                }]
            )
            data = json.loads(resp.content[0].text)
            tool_calls = data.get("tool_calls", CACHED_TOOL_CALLS)
            risk_score = data.get("risk_score", 0.08)
        except Exception as e:
            print(f"Writer error: {e} — fallback to cached")
            tool_calls = CACHED_TOOL_CALLS
            risk_score = 0.08
    
    # Execute MCP tools and build command list
    commands = []
    for call in tool_calls:
        result = await execute_mcp_tool(call["tool"], call["args"])
        # Store both the MCP result and human-readable command
        cmd_str = result.get("command", f"{call['tool']}({call['args']})")
        commands.append(cmd_str)
    
    return RemediationPlan(
        commands=commands,
        safety_level="sandboxed",
        risk_score=risk_score,
        requires_approval=True,
        dry_run_passed=False
    )


# Sync wrapper for backward compatibility
def generate_plan_sync(fault: FaultReport) -> RemediationPlan:
    """Synchronous wrapper for generate_plan"""
    return asyncio.run(generate_plan(fault))
