"""ArgoCD PreDelete Hook Mock — validates commands before execution"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import RemediationPlan


def run_argo_mock(plan: RemediationPlan) -> RemediationPlan:
    """Simulate Argo CD 3.3 PreDelete dry-run hook"""
    for cmd in plan.commands:
        if "delete" in cmd.lower() or "destroy" in cmd.lower():
            plan.risk_score = 0.85
        elif "rollback" in cmd.lower() or "undo" in cmd.lower():
            plan.risk_score = 0.08
    
    plan.dry_run_passed = plan.risk_score < 0.5
    return plan
