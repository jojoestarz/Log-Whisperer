# Demo Mode Realistic Delays

When `DEMO_MODE=true`, the system simulates realistic processing times to demonstrate how the actual system would behave with real API calls.

## Delay Configuration

### Decision Agent (Single Analysis)
- **Task**: Analyze incident logs and identify root cause
- **Delay**: 2.0 seconds
- **Rationale**: Log parsing, pattern matching, and root cause identification

### Writer Agent (Command Generation)
- **Task**: Generate 3 remediation commands
- **Delay**: 1.5 seconds
- **Rationale**: Command synthesis and validation

### Council Agent (Multi-Agent Debate)
Most computationally intensive due to multiple LLM calls:

1. **Agent A (Conservative SRE)**
   - Delay: 2.5 seconds
   - Focus: Configuration analysis

2. **Agent B (Network Specialist)**
   - Delay: 2.8 seconds (longest)
   - Focus: Network/BGP analysis (most complex)

3. **Agent C (Chaos Engineer)**
   - Delay: 2.3 seconds
   - Focus: Cascading failure patterns

4. **Consensus Building**
   - Delay: 3.0 seconds
   - Rationale: Synthesizing 3 expert opinions into final decision

**Total Council Time**: ~10.6 seconds (realistic for 4 API calls)

## Total Pipeline Time

- **Decision Agent**: 2.0s
- **Writer Agent**: 1.5s
- **Council Agent**: 10.6s (if used instead of Decision)

**Typical Run**: 3.5 - 12 seconds depending on agent choice

## Real API Comparison

With actual Gemini API calls:
- Single call: 1-4 seconds (network + processing)
- Council debate: 8-15 seconds (4 sequential calls)

Demo mode delays are calibrated to match real-world performance.

## Adjusting Delays

To modify delays, edit the `time.sleep()` values in:
- `agents/decision_agent.py` (line ~52)
- `agents/writer_agent.py` (line ~78)
- `agents/council_agent.py` (lines ~110-130)

## Why Delays Matter

1. **Realistic UX**: Users see how the system actually performs
2. **Testing**: Validates UI responsiveness during processing
3. **Demonstrations**: Shows the complexity of multi-agent systems
4. **Rate Limiting**: Prevents instant execution that might confuse users
