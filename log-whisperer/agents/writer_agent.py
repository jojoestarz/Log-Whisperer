"""Writer Agent — generates remediation commands from FaultReport"""
import anthropic
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import FaultReport, RemediationPlan
from config import ANTHROPIC_API_KEY, DEMO_MODE, MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

WRITER_SYSTEM = """You are an SRE remediation expert.
Given a root cause, output exactly 3 CLI commands to fix it.
Respond ONLY with valid JSON. No markdown. No backticks.
Schema: {"commands": ["cmd1","cmd2","cmd3"],
"safety_level": "sandboxed", "risk_score": 0.08,
"requires_approval": true, "dry_run_passed": false}"""

CACHED_PLAN = RemediationPlan(
    commands=[
        "argocd app rollback byoip-cleanup --revision 4820",
        "kubectl rollout undo deployment/bgp-config-deployer",
        "bgpctl reload --prefix-list /etc/bgp/safe-prefixes.conf"
    ],
    safety_level="sandboxed",
    risk_score=0.08,
    requires_approval=True,
    dry_run_passed=False
)


def generate_plan(fault: FaultReport) -> RemediationPlan:
    """Generate remediation plan from fault report"""
    if DEMO_MODE:
        return CACHED_PLAN
    
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=WRITER_SYSTEM,
            messages=[{
                "role": "user",
                "content": f"Root cause: {fault.root_cause}\nAffected: {fault.affected_services}"
            }]
        )
        data = json.loads(resp.content[0].text)
        return RemediationPlan(**data)
    except Exception as e:
        print(f"Writer error: {e} — fallback")
        return CACHED_PLAN
