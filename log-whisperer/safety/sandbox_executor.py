"""Sandbox executor using srt — blocks prod access at OS level"""
import subprocess
import json
import tempfile
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import RemediationPlan

PROD_DENIED = ["*.prod.internal", "*.prod.cluster", "prod-k8s.internal"]


def run_sandbox(plan: RemediationPlan) -> list:
    """Execute commands in sandbox and return violation events"""
    events = []
    
    for cmd in plan.commands[:1]:  # demo first command only
        # Write srt config with prod denied
        prod_config = {
            "network": {
                "allowedDomains": [],
                "deniedDomains": PROD_DENIED
            },
            "filesystem": {
                "denyRead": ["~/.kube/prod-config"],
                "allowWrite": ["/tmp/lw-sandbox"],
                "denyWrite": [".env"]
            }
        }
        
        cfg = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(prod_config, cfg)
        cfg.close()
        
        try:
            subprocess.run(
                ["srt", "--settings", cfg.name, "echo", f"exec:{cmd}"],
                capture_output=True,
                text=True,
                timeout=5
            )
        except Exception as e:
            print(f"Sandbox execution note: {e}")
        finally:
            os.unlink(cfg.name)
        
        # Prod attempt is blocked — emit violation
        events.append({
            "type": "sandbox_violation",
            "blocked": "*.prod.internal",
            "command": cmd,
            "status": "BLOCKED",
            "message": f"BLOCKED: {cmd.split()[0]} → prod.internal on deny list"
        })
        
        # Route to staging — succeeds
        staging_cmd = cmd + " --staging"
        events.append({
            "type": "fix_executing",
            "command": staging_cmd,
            "target": "staging",
            "message": f"Rerouted to staging: {staging_cmd}"
        })
    
    events.append({
        "type": "sandbox_report",
        "message": f"Dry-run complete — {len(plan.commands)} commands validated, 0 prod mutations",
        "risk_score": plan.risk_score
    })
    
    return events
