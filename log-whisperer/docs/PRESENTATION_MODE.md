# Presentation Mode - Demo Delays & Flow

Complete guide to the presentation-optimized demo mode with audience-friendly pacing.

## Overview

When `DEMO_MODE=true`, the system adds strategic delays to:
- Give audience time to read and comprehend
- Simulate realistic processing
- Maintain engagement without frustration

## Complete Flow Timeline

### Phase 1: Ingestion (1.2s)
```
📥 Ingesting incident logs...
```
- **Purpose**: Show data loading
- **Audience sees**: System receiving incident data

### Phase 2: Analysis Initiation (0.8s)
```
🔍 Initiating analysis...
```
- **Purpose**: Transition to processing
- **Audience sees**: System starting work

### Phase 3A: Decision Agent (Single Analysis)
**Total: ~3.6s**

1. **Analysis** (2.0s)
   ```
   💭 Decision Agent analyzing...
   Analyzing incident patterns...
   ```

2. **Results Display** (1.6s)
   - Fault report table shown
   - Audience reads root cause, severity, affected services

### Phase 3B: Council Agent (Multi-Agent Debate)
**Total: ~13.5s**

1. **Initiation** (0.8s)
   ```
   🏛️  Initiating Council Debate
   Consulting 3 expert agents for comprehensive analysis...
   ```

2. **Agent A - Conservative SRE** (2.6s)
   ```
   ▶ Consulting Agent A (Conservative SRE)
     Focus: Configuration and deployment analysis
   💭 Agent A analyzing...
   ✓ Agent A analysis complete
   ```
   - Analysis: 2.0s
   - Completion pause: 0.6s

3. **Agent B - Network Specialist** (2.6s)
   ```
   ▶ Consulting Agent B (Network Specialist)
     Focus: BGP and routing failure analysis
   💭 Agent B analyzing...
   ✓ Agent B analysis complete
   ```
   - Analysis: 2.0s
   - Completion pause: 0.6s

4. **Agent C - Chaos Engineer** (2.6s)
   ```
   ▶ Consulting Agent C (Chaos Engineer)
     Focus: Cascading failure pattern analysis
   💭 Agent C analyzing...
   ✓ Agent C analysis complete
   ```
   - Analysis: 2.0s
   - Completion pause: 0.6s

5. **Debate Results Display** (1.5s)
   - Shows all 3 hypotheses with confidence bars
   - Audience reads and compares opinions

6. **Consensus Building** (3.4s)
   ```
   🤝 Reaching Consensus
   Analyzing expert hypotheses... (2.5s)
   Weighing confidence levels and evidence... (1.2s)
   Synthesizing final diagnosis... (1.0s)
   ```

7. **Consensus Display** (1.0s)
   - Final diagnosis panel
   - Audience reads conclusion

### Phase 4: Remediation Plan Generation (1.8s)
```
⚙️  Generating remediation plan...
```
- **Purpose**: Show plan creation
- **Audience sees**: System formulating response

### Phase 5: Plan Explanation (1.5s)
```
📋 Plan Explanation:
This remediation plan will execute three sequential commands...
Each command has been validated for safety and effectiveness.
```
- **Purpose**: Context for upcoming commands
- **Audience sees**: High-level strategy

### Phase 6: Command Display (3.6s total)
**Per command: 1.8s**

1. **Command 1** (immediate)
   ```
   Command 1 (low risk): Revert commit 4821...
   git revert abc123def456 --no-commit
   ```
   - Display: instant
   - Read time: 0.8s

2. **Delay** (1.0s)
   - Pause between commands

3. **Command 2** (1.8s)
   ```
   Command 2 (low risk): Apply corrected BGP configuration
   kubectl apply -f manifests/bgp-config-fix.yaml
   ```
   - Display + read: 0.8s

4. **Delay** (1.0s)

5. **Command 3** (1.8s)
   ```
   Command 3 (low risk): Sync Argo CD to deploy fix
   argocd app sync bgp-router --prune
   ```
   - Display + read: 0.8s

## Total Timeline

| Scenario | Duration | Notes |
|----------|----------|-------|
| **Decision Agent Path** | ~10s | Fastest, single analysis |
| **Council Agent Path** | ~20s | Most comprehensive |
| **Full Pipeline** | ~25s | Council + Plan + Commands |

## Delay Calibration

All delays are in `demo_delays.py`:

```python
INGESTION = 1.2          # Log loading
INITIATE_ANALYSIS = 0.8  # Start analysis
AGENT_THINKING = 2.0     # Agent processing
AGENT_COMPLETE = 0.6     # Agent done pause
CONSENSUS_START = 0.8    # Start consensus
CONSENSUS_PROCESS = 2.5  # Build consensus
PLAN_GENERATION = 1.8    # Generate plan
PLAN_EXPLANATION = 1.5   # Explain plan
COMMAND_DISPLAY = 1.0    # Between commands
COMMAND_DETAIL = 0.8     # Command read time
```

## Presentation Tips

### For Live Demos
1. **Narrate during delays**: Explain what's happening
2. **Point out key info**: Highlight confidence scores, risk levels
3. **Pause after consensus**: Let audience absorb the diagnosis

### For Recorded Demos
1. **Add voiceover**: Explain each phase
2. **Use captions**: Highlight important values
3. **Speed up in editing**: Can reduce delays by 20-30% if needed

### For Interactive Sessions
1. **Ask questions**: "What do you think the root cause is?"
2. **Predict outcomes**: "Which agent will have highest confidence?"
3. **Discuss trade-offs**: "Why three commands instead of one?"

## Adjusting for Different Audiences

### Technical Audience (Reduce by 20%)
- They read faster
- Understand concepts quicker
- Can handle faster pace

### Executive Audience (Keep as-is)
- Need time to understand
- Appreciate thoroughness
- Value clear explanations

### Marketing/Sales Demo (Reduce by 30%)
- Focus on wow factor
- Keep momentum high
- Emphasize speed

## Testing the Flow

```bash
# Run with demo mode
./venv/bin/python main.py

# Select option 1 (Full Pipeline)
# Or option 2 (Quick Demo)

# Time the full flow
time ./venv/bin/python main.py
```

## Customization

To adjust delays for your needs:

1. Edit `demo_delays.py`
2. Modify the class constants
3. No need to change agent code
4. Centralized control

Example:
```python
# Make it faster for technical demos
AGENT_THINKING = 1.5  # Was 2.0
CONSENSUS_PROCESS = 2.0  # Was 2.5

# Make it slower for executive presentations
AGENT_THINKING = 2.5  # Was 2.0
PLAN_EXPLANATION = 2.0  # Was 1.5
```
