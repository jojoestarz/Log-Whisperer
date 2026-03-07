# Architecture

```
Loki Anomaly
     │
     ▼ POST /trigger
Decision Agent ──► FaultReport
     │
     ▼
Writer Agent ──► RemediationPlan
     │
     ▼
Argo Safety Gate ──► DryRunResults
     │
     ├── PASS ──► awaiting_approval ──► POST /approve ──► Execute ──► resolved ✅
     └── FAIL ──► failed 🚫
```

## File ownership
| File | Owner |
|------|-------|
| agents/decision_agent.py | P1 |
| agents/writer_agent.py | P1 |
| tools/mcp_tools.py | P2 |
| safety/argo_hook.py | P2 |
| api/main.py | P2 |
| viz/timeline.py | P3 |
| models.py | All (read-only after hour 1) |
