"""
Writer Agent — P1 owns this file.
Receives FaultReport, returns RemediationPlan with CLI commands.
"""
import json, uuid, structlog
from anthropic import Anthropic
from models import FaultReport, RemediationPlan, CLICommand
from config import ANTHROPIC_API_KEY, DEMO_MODE, MODEL

log = structlog.get_logger()
client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """
You are a senior infrastructure engineer. Given a fault report, generate exact CLI remediation commands.
Available tools: git_revert, kubectl_apply, kubectl_scale, argo_sync, service_restart.
Respond ONLY with valid JSON:
{
  "commands": [{"tool": "git_revert", "args": {"commit_hash": "4821", "repo": "infra-bgp-config"}, "description": "...", "risk_level": "low"}],
  "rollback_commands": [...],
  "estimated_recovery_mins": 4,
  "overall_risk": "low"
}
"""

CACHED_PLAN = RemediationPlan(
    plan_id="demo-plan-001",
    commands=[
        CLICommand(tool="git_revert", args={"commit_hash":"4821","repo":"infra-bgp-config"}, description="Revert bad BGP config #4821", risk_level="low"),
        CLICommand(tool="argo_sync", args={"app_name":"bgp-edge-routers","prune":"false"}, description="Sync Argo CD to apply reverted config", risk_level="low"),
        CLICommand(tool="service_restart", args={"service":"dns-resolver","namespace":"infra"}, description="Restart DNS resolver", risk_level="low"),
    ],
    rollback_commands=[
        CLICommand(tool="git_revert", args={"commit_hash":"4820","repo":"infra-bgp-config"}, description="Emergency rollback", risk_level="medium"),
    ],
    estimated_recovery_mins=4,
    overall_risk="low"
)

async def run(fault: FaultReport) -> RemediationPlan:
    if DEMO_MODE:
        log.info("writer_agent.demo_mode")
        plan = CACHED_PLAN.model_copy()
        plan.plan_id = f"plan-{uuid.uuid4().hex[:8]}"
        return plan

    response = client.messages.create(
        model=MODEL, max_tokens=1000, system=SYSTEM_PROMPT,
        messages=[{"role":"user","content":f"Generate remediation for:\n{fault.model_dump_json(indent=2)}"}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    data = json.loads(raw)
    return RemediationPlan(plan_id=f"plan-{uuid.uuid4().hex[:8]}", **data)
