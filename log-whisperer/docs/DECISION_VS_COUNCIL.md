# Decision Agent vs Council Agent Comparison

## Overview

The Log Whisperer system has been upgraded from a single Decision Agent to a multi-agent Council system for more robust root cause analysis.

## Architecture Comparison

### Decision Agent (Original)
```
Logs → Single Agent → FaultReport
```

- 1 AI agent analyzes logs
- 1 API call
- Single perspective
- Direct analysis

### Council Agent (New)
```
Logs → Agent A (SRE) ──┐
    → Agent B (Network) ├→ Consensus → FaultReport
    → Agent C (Chaos) ──┘
```

- 3 specialized AI agents
- 4 API calls (3 agents + 1 consensus)
- Multiple perspectives
- Debate and consensus

## Feature Comparison

| Feature | Decision Agent | Council Agent |
|---------|---------------|---------------|
| **Agents** | 1 | 3 + consensus |
| **API Calls** | 1 | 4 |
| **Perspectives** | Single | Multiple (SRE, Network, Chaos) |
| **Debate Summary** | ❌ | ✅ |
| **Confidence Bars** | ❌ | ✅ |
| **Visual Output** | Rich Table | Rich Panels + Bars |
| **Agent Specialization** | General | Specialized roles |
| **Reasoning Transparency** | Limited | Full debate visible |
| **Error Handling** | Fallback | Fallback |
| **DEMO_MODE** | ✅ | ✅ |

## Agent Specializations

### Council Agent Roles

**Agent A - Conservative SRE** (Cyan)
- Focus: Configuration changes
- Approach: Methodical, deployment-focused
- Strength: Catches config-related issues
- Example: "Config 4821 contains empty string"

**Agent B - Network Specialist** (Yellow)
- Focus: BGP/routing failures
- Approach: Network topology analysis
- Strength: Identifies routing problems
- Example: "BGP route withdrawal cascade"

**Agent C - Chaos Engineer** (Magenta)
- Focus: Cascading failures
- Approach: Systems thinking
- Strength: Sees failure propagation
- Example: "Cascading failure from config error"

## Output Comparison

### Decision Agent Output
```
╭─────────── 🔍 Fault Report ───────────╮
│ Field              │ Value             │
├────────────────────┼───────────────────┤
│ Root Cause         │ Empty-string...   │
│ Affected Services  │ bgp-router-lon... │
│ Severity           │ P1                │
│ Confidence         │ 97%               │
╰────────────────────────────────────────╯
```

### Council Agent Output
```
🏛️  Council Debate in Progress
Three agents analyzing the incident...

╭─────── Agent A (Conservative SRE) ───────╮
│ Config 4821 contains empty string        │
│                                           │
│ Reasoning: Logs show validation SKIPPED  │
│ Confidence: 95%                           │
╰───────────────────────────────────────────╯
████████████████████████████░ 95%

╭───── Agent B (Network Specialist) ───────╮
│ BGP route withdrawal cascade              │
│                                           │
│ Reasoning: Sequence shows propagation    │
│ Confidence: 92%                           │
╰───────────────────────────────────────────╯
███████████████████████████░░ 92%

╭────── Agent C (Chaos Engineer) ──────────╮
│ Cascading failure from config error      │
│                                           │
│ Reasoning: Single point of failure       │
│ Confidence: 88%                           │
╰───────────────────────────────────────────╯
██████████████████████████░░░ 88%

╭────────── ✓ Consensus Reached ───────────╮
│ Empty-string config in BGP deployment    │
│ 4821 triggered bulk route withdrawal     │
│                                           │
│ Severity: P1                              │
│ Confidence: 89%                           │
╰───────────────────────────────────────────╯
```

## Code Comparison

### Decision Agent
```python
# agents/decision_agent.py
def analyze_logs(log_path: str) -> FaultReport:
    # Single API call
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": logs_text}]
    )
    
    # Parse and return
    report = FaultReport(**json.loads(raw))
    return report
```

### Council Agent
```python
# agents/council_agent.py
def hold_council_debate(logs: list[dict]) -> FaultReport:
    debates = []
    
    # 3 separate API calls (one per agent)
    for agent_name, system_prompt, color in agents:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            system=system_prompt,
            messages=[{"role": "user", "content": logs_text}]
        )
        debates.append(CouncilDebate(**json.loads(raw)))
    
    # Consensus API call
    consensus_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        system=CONSENSUS_PROMPT,
        messages=[{"role": "user", "content": debate_summary}]
    )
    
    # Return with debate summary
    return FaultReport(**consensus_data, debate_summary=debates)
```

## Benefits of Council Agent

### 1. Diverse Perspectives
- Each agent brings specialized expertise
- Reduces blind spots
- Better coverage of failure modes

### 2. Higher Confidence
- Consensus from multiple viewpoints
- Cross-validation of hypotheses
- More robust analysis

### 3. Transparency
- See reasoning from each agent
- Understand different perspectives
- Better explainability

### 4. Specialization
- Agents focus on their domain
- Deeper analysis in each area
- More nuanced understanding

### 5. Robustness
- Multiple hypotheses considered
- Less likely to miss root cause
- Better handling of complex incidents

## Performance Comparison

| Metric | Decision Agent | Council Agent |
|--------|---------------|---------------|
| **API Calls** | 1 | 4 |
| **Latency** | ~2s | ~8s |
| **Token Usage** | ~1000 | ~4000 |
| **Cost** | $0.01 | $0.04 |
| **Accuracy** | Good | Better |
| **Explainability** | Basic | Excellent |

## When to Use Each

### Use Decision Agent When:
- Speed is critical
- Cost is a concern
- Simple incidents
- Single perspective sufficient

### Use Council Agent When:
- Complex incidents
- Multiple failure modes possible
- Need high confidence
- Transparency important
- Cost is not primary concern

## Migration Path

The system now uses Council Agent by default:

```python
# api/pipeline.py
from agents.council_agent import analyze_incident  # New

# Old way (still available):
# from agents.decision_agent import analyze_incident
```

To switch back to Decision Agent:
```python
# In api/pipeline.py, change import:
from agents.decision_agent import analyze_incident
```

## Model Updates

Added to `models.py`:

```python
class CouncilDebate(BaseModel):
    agent_name: str
    hypothesis: str
    confidence: float
    reasoning: str

class FaultReport(BaseModel):
    # ... existing fields ...
    debate_summary: list[CouncilDebate] = []  # New field
```

## Testing

Both agents have comprehensive test suites:

```bash
# Test decision agent
python test_decision_agent.py

# Test council agent
python test_council_agent.py
```

## Conclusion

The Council Agent provides:
- ✅ Better analysis through multiple perspectives
- ✅ Higher confidence through consensus
- ✅ Better transparency through debate visibility
- ✅ Specialized expertise per agent
- ⚠️ Higher cost (4x API calls)
- ⚠️ Higher latency (4x time)

For production use with complex incidents, the Council Agent is recommended. For simple incidents or cost-sensitive scenarios, the Decision Agent remains available.
