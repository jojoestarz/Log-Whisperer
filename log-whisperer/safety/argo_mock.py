"""
Mock Argo CD safety gate for dry-run validation.
Simulates what would happen if commands were executed.
"""
from models import CLICommand, DryRunResult
import random


def dry_run_command(command: CLICommand) -> DryRunResult:
    """
    Simulate Argo CD dry-run for a given command.
    Returns whether it would succeed and what side effects would occur.
    """
    risk_scores = {"low": 0.1, "medium": 0.5, "high": 0.8}
    risk_score = risk_scores.get(command.risk_level, 0.5)
    
    # Simulate success probability based on risk
    would_succeed = random.random() > (risk_score * 0.3)
    
    side_effects = []
    if command.tool == "kubectl_scale":
        replicas = command.args.get("replicas", "3")
        side_effects.append(f"Would scale to {replicas} replicas")
        side_effects.append("Pod churn expected for ~30s")
    elif command.tool == "git_revert":
        side_effects.append("Config rollback to previous commit")
        side_effects.append("Requires Argo sync to apply")
    elif command.tool == "argo_sync":
        side_effects.append("Deploys latest Git state to cluster")
    elif command.tool == "service_restart":
        side_effects.append("Brief downtime during restart")
    elif command.tool == "kubectl_apply":
        side_effects.append("Applies manifest changes")
    
    safe_to_execute = would_succeed and risk_score < 0.7
    
    return DryRunResult(
        command=command,
        would_succeed=would_succeed,
        side_effects=side_effects,
        risk_score=risk_score,
        safe_to_execute=safe_to_execute
    )
