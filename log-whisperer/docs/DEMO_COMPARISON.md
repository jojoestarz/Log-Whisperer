# Demo Comparison: Interactive vs Full Pipeline

## Quick Answer

**Yes!** The `demo_interactive.py` uses the **same executor** that the full pipeline uses. It's just focused on demonstrating the execution part in isolation.

## Side-by-Side Comparison

### demo_interactive.py (Standalone Execution Demo)

**What it does:**
```
Create test repo → Show broken config → Execute git revert → Verify fix
```

**Components used:**
- ✅ `execution/executor.py` - CommandExecutor
- ✅ `models.py` - CLICommand
- ❌ No AI agents
- ❌ No log ingestion
- ❌ No council debate

**Purpose:**
- Prove execution works
- Show execution modes (dry/safe/full)
- Quick demo (30 seconds)
- No API keys needed

**Run it:**
```bash
./run_demo.sh
```

---

### demo_pretty_pipeline.py (Full Pipeline Demo)

**What it does:**
```
Ingest logs → Council debate → Writer agent → Safety check → 
Human approval → Execute commands → Verify
```

**Components used:**
- ✅ `execution/executor.py` - CommandExecutor (same one!)
- ✅ `models.py` - CLICommand (same model!)
- ✅ `agents/council_agent.py` - Multi-agent debate
- ✅ `agents/writer_agent.py` - Command generation
- ✅ `data/cloudflare_incident.json` - Real incident logs
- ✅ `api/pipeline.py` - Full orchestration

**Purpose:**
- Show complete system
- AI agents making decisions
- Full remediation flow
- Production-like experience

**Run it:**
```bash
# Requires ANTHROPIC_API_KEY in .env
python3 demo_pretty_pipeline.py
```

## The Connection

### Both Use the Same Executor

**demo_interactive.py (line ~200):**
```python
from execution.executor import CommandExecutor, ExecutionMode

executor = CommandExecutor(mode=execution_mode, working_dir=demo_dir)
result = executor.execute(command)
```

**api/pipeline.py (line ~135):**
```python
from execution.executor import get_executor

executor = get_executor(execution_mode)
result = executor.execute(cmd)
```

### Both Use the Same Command Model

**demo_interactive.py:**
```python
command = CLICommand(
    tool="git_revert",
    args={"commit": bad_commit},
    description="Revert broken BGP config deployment 4821",
    risk_level="low"
)
```

**agents/writer_agent.py (generates this for pipeline):**
```python
commands = [
    CLICommand(
        tool="git_revert",
        args={"commit": "abc123def456"},
        description="Revert broken config",
        risk_level="low"
    ),
    # ... more commands
]
```

### Both Execute Real Git Commands

**execution/executor.py (used by both):**
```python
def execute(self, command: CLICommand) -> Dict[str, Any]:
    # Build command
    if command.tool == "git_revert":
        cmd_list = ["git", "revert", commit, "--no-commit"]
    
    # Execute
    result = subprocess.run(cmd_list, ...)  # ← Real execution!
    return result
```

## Visual Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  demo_interactive.py                        │
│                  (Execution Focus)                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Uses
                            ▼
                ┌───────────────────────┐
                │ execution/executor.py │
                │   CommandExecutor     │
                └───────────────────────┘
                            ▲
                            │ Uses
                            │
┌─────────────────────────────────────────────────────────────┐
│              demo_pretty_pipeline.py                        │
│              (Full System)                                  │
│                                                             │
│  Logs → Council → Writer → Safety → Approval → Execute     │
└─────────────────────────────────────────────────────────────┘
```

## What Each Demo Proves

### demo_interactive.py Proves:
1. ✅ Executor works with real git commands
2. ✅ Three execution modes work (dry/safe/full)
3. ✅ Commands actually modify files
4. ✅ Git history is updated
5. ✅ System can execute remediation

### demo_pretty_pipeline.py Proves:
1. ✅ Everything from interactive demo, PLUS:
2. ✅ AI agents can analyze logs
3. ✅ Council debate reaches consensus
4. ✅ Writer generates valid commands
5. ✅ Safety checks work
6. ✅ Full pipeline orchestration works
7. ✅ End-to-end incident remediation

## When to Use Each

### Use demo_interactive.py when:
- ❓ "Does execution actually work?"
- ❓ "Can it run real git commands?"
- ❓ "What are the execution modes?"
- ❓ "Quick demo without setup"
- ❓ "No API keys available"

### Use demo_pretty_pipeline.py when:
- ❓ "How does the full system work?"
- ❓ "How do AI agents make decisions?"
- ❓ "What's the complete flow?"
- ❓ "Production-like demonstration"
- ❓ "Have API keys configured"

## Try Both!

### 1. Start with Interactive (Quick)
```bash
cd log-whisperer
./run_demo.sh
# Type: full
# See: Real git execution in 30 seconds
```

### 2. Then Try Full Pipeline (Complete)
```bash
# Add ANTHROPIC_API_KEY to .env
python3 demo_pretty_pipeline.py
# See: AI agents + execution
```

## The Answer to Your Question

> "Is this git demo linked to the overall pipeline?"

**Yes!** They're linked through the **shared executor**:

```
demo_interactive.py ──┐
                      ├──→ execution/executor.py ──→ Real git commands
demo_pretty_pipeline.py ─┘
```

The interactive demo is like testing the **engine** in isolation.
The full pipeline is like testing the **entire car** with the engine.

Both use the same engine (executor), so proving the interactive demo works proves the execution part of the full pipeline works too!

## Code Files to Explore

1. **execution/executor.py** - The shared executor (both demos use this)
2. **models.py** - CLICommand model (both demos use this)
3. **demo_interactive.py** - Standalone execution demo
4. **api/pipeline.py** - Full pipeline orchestration
5. **demo_pretty_pipeline.py** - Full pipeline demo

## Summary Table

| Feature | Interactive Demo | Full Pipeline |
|---------|-----------------|---------------|
| **Executor** | ✅ Same | ✅ Same |
| **Commands** | Hardcoded | AI-generated |
| **Execution** | ✅ Real git | ✅ Real git |
| **AI Agents** | ❌ No | ✅ Yes |
| **Log Analysis** | ❌ No | ✅ Yes |
| **API Keys** | ❌ Not needed | ✅ Required |
| **Duration** | 30 seconds | 2-3 minutes |
| **Purpose** | Prove execution | Show full system |

Both are valuable! The interactive demo proves the core functionality works, and the full pipeline shows how all the pieces fit together. 🚀
