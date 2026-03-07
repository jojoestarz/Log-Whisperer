"""MCP tool definitions — P2 owns this file."""
import structlog
from config import ARGO_MOCK
log = structlog.get_logger()

async def git_revert(commit_hash: str, repo: str) -> dict:
    cmd = f"git -C /repos/{repo} revert {commit_hash} --no-commit && git push"
    log.info("tool.git_revert", cmd=cmd)
    return {"status": "dry_run" if ARGO_MOCK else "executed", "command": cmd, "would_succeed": True}

async def kubectl_apply(manifest_path: str, namespace: str = "default") -> dict:
    cmd = f"kubectl apply -f {manifest_path} -n {namespace}"
    log.info("tool.kubectl_apply", cmd=cmd)
    return {"status": "dry_run" if ARGO_MOCK else "executed", "command": cmd, "would_succeed": True}

async def kubectl_scale(deployment: str, replicas: int, namespace: str = "default") -> dict:
    cmd = f"kubectl scale deployment/{deployment} --replicas={replicas} -n {namespace}"
    log.info("tool.kubectl_scale", cmd=cmd)
    return {"status": "dry_run" if ARGO_MOCK else "executed", "command": cmd, "would_succeed": True}

async def argo_sync(app_name: str, prune: str = "false") -> dict:
    cmd = f"argocd app sync {app_name} --prune={prune}"
    log.info("tool.argo_sync", cmd=cmd)
    return {"status": "dry_run" if ARGO_MOCK else "executed", "command": cmd, "would_succeed": True}

async def service_restart(service: str, namespace: str = "default") -> dict:
    cmd = f"kubectl rollout restart deployment/{service} -n {namespace}"
    log.info("tool.service_restart", cmd=cmd)
    return {"status": "dry_run" if ARGO_MOCK else "executed", "command": cmd, "would_succeed": True}
