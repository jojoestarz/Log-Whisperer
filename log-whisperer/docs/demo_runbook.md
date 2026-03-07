# Demo Runbook — 90 seconds

## Pre-demo checklist
- [ ] `python api/main.py` running (terminal 1)
- [ ] Rerun viewer open (terminal 2)
- [ ] Test full flow cold: trigger → approve → resolved
- [ ] DEMO_MODE=true ready as fallback if LLM is slow

## Commands
```bash
# Terminal 1
python api/main.py

# Terminal 2  
curl -s -X POST http://localhost:8000/trigger | python -m json.tool

# Copy incident_id from above, then:
curl -s -X POST http://localhost:8000/approve/cf-2022-06-21-bgp | python -m json.tool
```

## Script
| 0:00 | "Cloudflare. June 2022. 57 minutes of downtime." |
| 0:20 | "AI diagnoses. AI proposes. Human approves." |
| 0:35 | POST /trigger — point to Rerun filling up |
| 1:05 | "Dry-run passed. Awaiting one thing — approval." |
| 1:10 | POST /approve |
| 1:15 | "4 minutes. Not 57." |
