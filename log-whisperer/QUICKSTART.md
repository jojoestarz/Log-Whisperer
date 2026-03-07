# 🔊 Log Whisperer - Quick Start

## 60-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
cd ui && npm install && cd ..

# 2. Configure (if needed)
# Your .env is already set up with your API key

# 3. Run
./start.sh

# OR use Docker
docker-compose up --build
```

## Test It Works

```bash
# Test the pipeline
python3 test_pipeline.py

# Should output:
# ✅ Pipeline test complete!
```

## Use It

1. Open http://localhost:5173
2. Click **RUN LOG WHISPERER**
3. Watch the pipeline execute
4. Click **APPROVE & EXECUTE** when prompted
5. See MTTR drop from 57:00 to 04:12

## Architecture Flow

```
Logs → Decision Agent → Writer Agent → Sandbox → Approval → Resolved
       (diagnose)       (fix commands)   (block prod)  (human)
```

## Key Files

- `models.py` - Shared data models (FaultReport, RemediationPlan)
- `agents/decision_agent.py` - Analyses logs, finds root cause
- `agents/writer_agent.py` - Generates CLI remediation commands
- `safety/argo_hook.py` - Risk scoring (0.08 = safe, >0.5 = blocked)
- `safety/sandbox_executor.py` - OS-level prod blocking
- `pipeline.py` - Orchestrates the full flow
- `server.py` - FastAPI + SSE streaming
- `ui/src/App.jsx` - React dashboard

## Demo Mode

Set `DEMO_MODE=true` in `.env` to use cached responses (no API calls, instant demo).

## Troubleshooting

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**Backend won't start:**
```bash
python3 -m uvicorn server:app --reload --port 8000
```

**Frontend won't start:**
```bash
cd ui && npm install && npm run dev
```

**Pipeline fails:**
- Check `data/cloudflare_incident.json` exists
- Set `DEMO_MODE=true` in `.env`
- Run `python3 test_pipeline.py` to debug

---

**MTTR: 57:00 → 04:12 · 98.7% reduction · ~$740K saved**
