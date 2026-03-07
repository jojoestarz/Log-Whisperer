# Council Agent - Implementation Complete ✓

## Overview

Multi-agent debate system that simulates 3 AI agents analyzing incident logs from different perspectives, then reaching consensus on the root cause.

## Architecture

### The Council

Three specialized agents debate the root cause:

1. **Agent A (Conservative SRE)** - Cyan
   - Focus: Recent config changes
   - Approach: Methodical, looks for deployment correlations
   - System Prompt: "Analyze logs looking for config changes that could cause outages"

2. **Agent B (Network Specialist)** - Yellow
   - Focus: BGP/routing issues
   - Approach: Network-centric, examines routing patterns
   - System Prompt: "Analyze logs for BGP/routing failures"

3. **Agent C (Chaos Engineer)** - Magenta
   - Focus: Cascading failures
   - Approach: Systems thinking, identifies failure propagation
   - System Prompt: "Analyze logs for cascading failure patterns"

### Consensus Mechanism

After all agents present their hypotheses, a final consensus call:
- Weighs all 3 perspectives
- Considers confidence levels
- Determines most likely root cause
- Generates comprehensive FaultReport

## Implementation

### Core Function

```python
def hold_council_debate(logs: list[dict]) -> FaultReport
```

**Process:**
1. Check DEMO_MODE (returns cached debate if enabled)
2. Make 3 separate Claude API calls (one per agent)
3. Each agent returns: `{hypothesis, confidence, reasoning}`
4. Collect responses into `List[CouncilDebate]`
5. Make consensus API call with all hypotheses
6. Display debate with Rich panels and confidence bars
7. Return FaultReport with `debate_summary` included

### Models

Added to `models.py`:

```python
class CouncilDebate(BaseModel):
    agent_name: str
    hypothesis: str
    confidence: float  # 0.0-1.0
    reasoning: str

class FaultReport(BaseModel):
    # ... existing fields ...
    debate_summary: list[CouncilDebate] = []
```

## Cached DEMO_MODE Response

```python
Agent A (Conservative SRE):
  Hypothesis: "Config 4821 contains empty string"
  Confidence: 95%
  Reasoning: "Logs show validation SKIPPED immediately before withdrawal"

Agent B (Network Specialist):
  Hypothesis: "BGP route withdrawal cascade"
  Confidence: 92%
  Reasoning: "Sequence shows lon01 -> iad01 propagation pattern"

Agent C (Chaos Engineer):
  Hypothesis: "Cascading failure from config error"
  Confidence: 88%
  Reasoning: "Single point of failure cascaded to all services"

Consensus:
  Root Cause: "Empty-string config in BGP deployment 4821 triggered bulk route withdrawal"
  Severity: P1
  Confidence: 89%
```

## Visual Output

Each agent's position displayed in colored panel:

```
╭─────── Agent A (Conservative SRE) ───────╮
│ Config 4821 contains empty string        │
│                                           │
│ Reasoning: Logs show validation SKIPPED  │
│ immediately before withdrawal             │
│                                           │
│ Confidence: 95%                           │
╰───────────────────────────────────────────╯
████████████████████████████░ 95%

╭───── Agent B (Network Specialist) ───────╮
│ BGP route withdrawal cascade              │
│                                           │
│ Reasoning: Sequence shows lon01 -> iad01 │
│ propagation pattern                       │
│                                           │
│ Confidence: 92%                           │
╰───────────────────────────────────────────╯
███████████████████████████░░ 92%

╭────── Agent C (Chaos Engineer) ──────────╮
│ Cascading failure from config error      │
│                                           │
│ Reasoning: Single point of failure       │
│ cascaded to all services                 │
│                                           │
│ Confidence: 88%                           │
╰───────────────────────────────────────────╯
██████████████████████████░░░ 88%

╭────────── ✓ Consensus Reached ───────────╮
│ Empty-string config in BGP deployment    │
│ 4821 triggered bulk route withdrawal     │
│                                           │
│ Severity: P1                              │
│ Confidence: 89%                           │
│ Affected Services: 5                      │
╰───────────────────────────────────────────╯
```

## Features

- ✓ Multi-agent debate (3 agents)
- ✓ Separate API calls per agent
- ✓ Different system prompts per agent
- ✓ Consensus mechanism
- ✓ Rich panel display with colors
- ✓ Confidence bars (30-char width)
- ✓ DEMO_MODE with cached debate
- ✓ Error handling with fallback
- ✓ Async wrapper for pipeline
- ✓ debate_summary in FaultReport

## Pipeline Integration

Updated `api/pipeline.py`:

```python
from agents.council_agent import analyze_incident  # Changed from decision_agent

# Pipeline now uses council debate instead of single agent
self.state.fault_report = await analyze_incident(log_events)
```

## Usage

### Basic Usage

```python
from agents.council_agent import hold_council_debate
from data.load_incident import load_cloudflare_incident

logs = load_cloudflare_incident()
fault_report = hold_council_debate(logs)

# Access debate summary
for debate in fault_report.debate_summary:
    print(f"{debate.agent_name}: {debate.hypothesis}")
    print(f"  Confidence: {debate.confidence:.0%}")
    print(f"  Reasoning: {debate.reasoning}")
```

### With Pipeline

```python
import asyncio
from api.pipeline import Pipeline
from data.load_incident import load_cloudflare_incident

async def run():
    pipeline = Pipeline(incident_id='demo-001')
    logs = load_cloudflare_incident()
    state = await pipeline.run(logs)
    
    # Council debate results in state.fault_report
    print(f"Consensus: {state.fault_report.root_cause}")
    print(f"Debate participants: {len(state.fault_report.debate_summary)}")

asyncio.run(run())
```

## Testing

### Run Test Suite

```bash
./venv/bin/python test_council_agent.py
```

Tests:
1. DEMO_MODE (cached debate)
2. Real API (3 agents + consensus)
3. Error handling (fallback)

### Run Demo

```bash
./venv/bin/python demo_council_debate.py
```

Shows full council debate with visual output.

## Benefits of Multi-Agent Debate

1. **Diverse Perspectives**: Each agent brings different expertise
2. **Higher Confidence**: Consensus from multiple viewpoints
3. **Better Coverage**: Different failure modes considered
4. **Transparency**: See reasoning from each perspective
5. **Robustness**: Multiple hypotheses reduce blind spots

## API Calls

In real mode, makes 4 API calls:
1. Agent A analysis
2. Agent B analysis
3. Agent C analysis
4. Consensus determination

In DEMO_MODE: 0 API calls (uses cached debate)

## Error Handling

If any API call fails:
- Catches exception
- Logs error message
- Falls back to cached debate
- Continues execution
- Returns valid FaultReport

## Validation

- ✓ No syntax errors (getDiagnostics clean)
- ✓ All imports successful
- ✓ Pipeline integration working
- ✓ DEMO_MODE functional
- ✓ 3 agents + consensus
- ✓ Rich display working
- ✓ Confidence bars rendering
- ✓ Error handling functional

## Comparison: Decision Agent vs Council Agent

| Feature | Decision Agent | Council Agent |
|---------|---------------|---------------|
| Agents | 1 | 3 + consensus |
| API Calls | 1 | 4 |
| Perspectives | Single | Multiple |
| Debate Summary | No | Yes |
| Confidence Bars | No | Yes |
| Visual Output | Table | Panels + Bars |

## Next Steps

Run the demos to see the council in action:

```bash
# Test the council agent
python test_council_agent.py

# See the debate visualization
python demo_council_debate.py

# Full pipeline with council
python demo_pretty_pipeline.py
```

The council brings diverse AI perspectives together! 🏛️
