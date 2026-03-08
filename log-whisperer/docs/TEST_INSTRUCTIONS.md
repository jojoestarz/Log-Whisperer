# Testing decision_agent.py

## Quick Test (DEMO_MODE)
```bash
cd log-whisperer
./venv/bin/python run_tests.py
cat test_results.txt
```

## Test with Real API (5 calls)
1. Add your Anthropic API key to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   DEMO_MODE=false
   ```

2. Run tests:
   ```bash
   ./venv/bin/python run_tests.py
   cat test_results.txt
   ```

## Manual Test
```bash
./venv/bin/python -c "
import os
os.environ['DEMO_MODE'] = 'true'
from agents.decision_agent import analyze_logs
report = analyze_logs('data/cloudflare_incident.json')
print(f'Success: {report.severity}, {report.confidence}')
"
```

## Features Implemented
✓ Load data/cloudflare_incident.json
✓ DEMO_MODE returns cached FaultReport
✓ Real API calls to Anthropic Claude
✓ Parse JSON response into FaultReport
✓ Rich table display with Field/Value columns
✓ Error handling with fallback to cached response
✓ Async wrapper for pipeline compatibility
