# Testing Without API / Avoiding Rate Limits

You have several options to test the system without hitting Gemini rate limits:

## Option 1: DEMO_MODE (Recommended)

Uses pre-cached responses, no API calls at all.

**Setup:**
```bash
# In .env file, set:
DEMO_MODE=true
```

**Run:**
```bash
./venv/bin/python main.py
# Select option 1 or 2
```

**What it does:**
- Uses cached FaultReports and RemediationPlans
- No API calls to Gemini
- Perfect for testing the UI, execution flow, and safety gates
- Shows you exactly what the system does without burning API credits

---

## Option 2: Use Ollama (Local LLM)

Run models locally on your machine - completely free, no rate limits.

**Setup:**
```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull a model
ollama pull llama3.2

# 3. Update .env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

**Note:** You'd need to add Ollama support to `llm_client.py` (I can help with this)

---

## Option 3: Reduce API Calls

Test specific components without running the full pipeline:

**Test individual agents:**
```bash
# Test decision agent only
./venv/bin/python -c "
from agents.decision_agent import analyze_logs
report = analyze_logs('data/cloudflare_incident.json')
print(report)
"
```

**Test with delays:**
```python
import time
# Add delays between API calls
time.sleep(60)  # Wait 1 minute between calls
```

---

## Option 4: Mock the LLM Client

Create a mock that returns test data:

```python
# In tests, use:
from unittest.mock import Mock

mock_client = Mock()
mock_client.create_message.return_value = '{"root_cause": "test", ...}'
```

---

## Current Rate Limits (Gemini Free Tier)

- **Gemini 2.5 Flash**: 15 requests/minute, 1500/day
- **Gemini 2.0 Flash**: 15 requests/minute, 1500/day  
- **Gemini 2.5 Pro**: 2 requests/minute, 50/day

The council agent makes 4 API calls (3 agents + 1 consensus), so you can only run it ~3 times per minute on free tier.

---

## Recommended Testing Strategy

1. **Use DEMO_MODE for UI/flow testing** (no API calls)
2. **Test with real API once** to verify integration works
3. **Use DEMO_MODE for all subsequent testing**
4. **Only use real API when you need to test new prompts or models**

---

## Quick Commands

```bash
# Enable demo mode
sed -i 's/DEMO_MODE=false/DEMO_MODE=true/' .env

# Disable demo mode  
sed -i 's/DEMO_MODE=true/DEMO_MODE=false/' .env

# Check current mode
grep DEMO_MODE .env
```
