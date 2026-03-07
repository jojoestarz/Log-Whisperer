"""Critic Agent - Challenges remediation plans for safety"""
import anthropic
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import RemediationPlan, FaultReport
from config import ANTHROPIC_API_KEY, DEMO_MODE, MODEL

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

CRITIC_SYSTEM = """You are a senior SRE reviewing a remediation plan.
Your job: find risks and propose safer alternatives.
Respond ONLY with valid JSON. No markdown.
Schema: {
  "concerns": ["risk 1", "risk 2"],
  "alternative_plan": ["safer command 1", "safer command 2"],
  "confidence": 0.85,
  "recommendation": "approve" or "revise"
}"""

CACHED_CRITIQUE = {
    "concerns": [
        "Direct rollback may not restore BGP state if routes were cached",
        "No validation step before declaring success",
        "Missing dry-run flag increases risk"
    ],
    "alternative_plan": [
        "argocd app rollback byoip-cleanup --staging --dry-run",
        "kubectl get bgproutes -n edge | grep -c ESTABLISHED",
        "argocd app rollback byoip-cleanup --staging"
    ],
    "confidence": 0.88,
    "recommendation": "revise"
}


async def critique(plan: RemediationPlan, fault: FaultReport) -> dict:
    """Review plan and propose alternatives"""
    if DEMO_MODE:
        return CACHED_CRITIQUE
    
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=500,
            system=CRITIC_SYSTEM,
            messages=[{
                "role": "user",
                "content": f"Review this plan:\nCommands: {plan.commands}\nRoot cause: {fault.root_cause}\nRisk score: {plan.risk_score}"
            }]
        )
        return json.loads(resp.content[0].text)
    except Exception as e:
        print(f"Critic error: {e} — fallback")
        return CACHED_CRITIQUE
