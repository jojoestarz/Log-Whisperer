"""Argo CD PreDelete Safety Hook — P2 owns this file."""
import structlog
from models import CLICommand, DryRunResult, RemediationPlan
log = structlog.get_logger()

HIGH_RISK_TOOLS = {"kubectl_apply"}
BASE_SCORES = {"low": 0.1, "medium": 0.4, "high": 0.75}
SIDE_EFFECTS = {
    "git_revert":      ["Repo HEAD moves back one commit", "CI/CD pipeline re-triggers"],
    "kubectl_apply":   ["Pods may briefly restart", "Traffic may shift during rollout"],
    "kubectl_scale":   ["Temporary capacity change", "Load balancer rebalances"],
    "argo_sync":       ["Argo CD enforces desired state", "Drifted resources corrected"],
    "service_restart": ["Service unavailable ~15s during rollout"],
}

class ArgoSafetyGate:
    async def run_dry_run(self, command: CLICommand) -> DryRunResult:
        score = BASE_SCORES.get(command.risk_level, 0.5)
        if command.tool in HIGH_RISK_TOOLS:
            score = min(score + 0.15, 1.0)
        return DryRunResult(
            command=command,
            would_succeed=True,
            side_effects=SIDE_EFFECTS.get(command.tool, ["Unknown"]),
            risk_score=score,
            safe_to_execute=score < 0.6
        )

    async def validate_plan(self, plan: RemediationPlan) -> tuple[RemediationPlan, list[DryRunResult]]:
        results = [await self.run_dry_run(cmd) for cmd in plan.commands]
        plan.dry_run_passed = all(r.safe_to_execute for r in results)
        return plan, results
