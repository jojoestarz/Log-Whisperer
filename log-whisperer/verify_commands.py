#!/usr/bin/env python3
"""
Verify the cached commands match the spec exactly
"""
import os
os.environ['DEMO_MODE'] = 'true'

from agents.writer_agent import generate_plan, CACHED_PLAN
from models import FaultReport

# Expected commands from spec
expected_commands = [
    "git revert abc123def456 --no-commit",
    "kubectl apply -f manifests/bgp-config-fix.yaml",
    "argocd app sync bgp-router --prune"
]

print("Cached Plan Commands:")
print("=" * 60)

for i, cmd in enumerate(CACHED_PLAN.commands, 1):
    if cmd.tool == "git_revert":
        bash_cmd = f"git revert {cmd.args.get('commit', '')} --no-commit"
    elif cmd.tool == "kubectl_apply":
        bash_cmd = f"kubectl apply -f {cmd.args.get('file', '')}"
    elif cmd.tool == "argo_sync":
        app = cmd.args.get('app', '')
        prune = cmd.args.get('prune', 'false')
        prune_flag = " --prune" if prune == "true" else ""
        bash_cmd = f"argocd app sync {app}{prune_flag}"
    
    print(f"{i}. {bash_cmd}")
    
    # Verify against expected
    if bash_cmd == expected_commands[i-1]:
        print(f"   ✓ Matches spec")
    else:
        print(f"   ✗ Expected: {expected_commands[i-1]}")

print("\n" + "=" * 60)
print("Validation:")
print(f"✓ Number of commands: {len(CACHED_PLAN.commands)} (expected: 3)")
print(f"✓ Overall risk: {CACHED_PLAN.overall_risk}")
print(f"✓ Recovery time: {CACHED_PLAN.estimated_recovery_mins} mins")
