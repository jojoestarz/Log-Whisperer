# 🔊 Log Whisperer

**The trust layer between AI diagnosis and infrastructure action**

> Infrastructure Track · AI Agents Hackathon

---

## Quick Start

```bash
# 1. Set up environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run with Docker (recommended)
docker-compose up --build

# OR run locally
uvicorn server:app --reload --port 8000
cd ui && npm install && npm run dev
```

Open http://localhost:5173 and click **RUN LOG WHISPERER**

---

## Architecture

```
Raw Logs → Decision Agent → Writer Agent → Sandbox Gate → Human Approve → System Heals
```

**Decision Agent**: Analyses incident logs, identifies root cause  
**Writer Agent**: Generates exact CLI remediation commands  
**Sandbox Gate**: Blocks prod access at OS level using `srt`  
**Human Approval**: One-click approval interface  

---

## Demo Mode

Set `DEMO_MODE=true` in `.env` to use cached responses (no API calls, instant demo).

---

## The Problem

IT downtime costs **$14,056/minute**. Cloudflare's Feb 2026 outage: 57 minutes MTTR.  
With Log Whisperer: **4 minutes MTTR** — 98.7% reduction, ~$740K saved.

---

## Tech Stack

- **LLM**: Claude (Anthropic API)
- **Backend**: Python, FastAPI, SSE
- **Frontend**: React, Vite
- **Safety**: `srt` sandbox, Argo CD mock
- **Container**: Docker Compose

---

**"Existing tools observe. We act — safely."**
