# Log Whisperer - Pipeline Architecture

## The Full Pipeline

Yes! The git demo uses the **same executor** that the full pipeline uses. Here's how everything connects:

## Complete Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FULL PIPELINE                                │
└─────────────────────────────────────────────────────────────────┘

1. LOG INGESTION
   ├─ data/cloudflare_incident.json
   └─ Real logs from incident
          ↓

2. COUNCIL AGENT (Multi-Agent Debate)
   ├─ agents/council_agent.py
   ├─ Agent A: Conservative SRE
   ├─ Agent B: Network Specialist  
   ├─ Agent C: Chaos Engineer
   └─ Output: FaultReport
          ↓
          Root Cause: "Empty-string config in BGP deployment 4821"
          Affected Services: ["bgp-router-lon01", "api-gateway", ...]
          ↓

3. WRITER AGENT (Generate Remediation)
   ├─ agents/writer_agent.py
   └─ Output: RemediationPlan with CLICommands
          ↓
          Commands:
          - git revert abc123 --no-commit
          - kubectl apply -f manifests/bgp-config-fix.yaml
          - argocd app sync bgp-router --prune
          ↓

4. SAFETY GATE
   ├─ safety/argo_mock.py
   └─ Dry-run validation
          ↓

5. HUMAN APPROVAL
   └─ Awaiting approval...
          ↓

6. EXECUTION ⚡ (This is where demo_interactive.py focuses)
   ├─ execution/executor.py
   ├─ CommandExecutor(mode=ExecutionMode.FULL)
   └─ Executes the git revert command
          ↓
          subprocess.run(["git", "revert", commit, "--no-commit"])
          ↓

7. VERIFICATION
   └─ Config restored, services recovered
```

## Two Ways to Experience It

### Option 1: Standalone Execution Demo (demo_interactive.py)
**What it shows:** Just the execution part (step 6)

```python
# Simplified demo - focuses on execution
command = CLICommand(
    tool="git_revert",
    args={"commit": bad_commit},
    description="Revert broken config",
    risk_level="low"
)

executor = CommandExecutor(mode=execution_mode)
result = executor.execute(command)  # ← Real git execution
```

**Purpose:**
- Prove execution works
- Show different modes (dry/safe/full)
- Quick demo without AI agents
- No API keys needed

### Option 2: Full Pipeline (demo_pretty_pipeline.py)
**What it shows:** The complete flow (steps 1-7)

```python
# Full pipeline - all components
pipeline = Pipeline(incident_id="incident-001")

# Step 1-2: Ingest logs → Council debate
await pipeline.run(log_events)

# Step 3-5: Writer agent → Safety → Approval
# (pipeline.state now has remediation_plan)

# Step 6: Execute with same executor
execution_logs = pipeline.execute_approved_plan(execution_mode="full")
```

**Purpose:**
- Show complete system
- Multi-agent debate
- Full remediation flow
- Requires API keys

## The Connection

### Same Executor, Different Entry Points

```python
# In demo_interactive.py (standalone)
from execution.executor import CommandExecutor, ExecutionMode
executor = CommandExecutor(mode=ExecutionMode.FULL)
result = executor.execute(command)

# In api/pipeline.py (full pipeline)
from execution.executor import get_executor
executor = get_executor(execution_mode)  # Same executor!
result = executor.execute(cmd)
```

### Same Command Model

```python
# Both use the same CLICommand model
from models import CLICommand

command = CLICommand(
    tool="git_revert",
    args={"commit": "abc123"},
    description="Revert broken config",
    risk_level="low"
)
```

### Same Execution Logic

```python
# execution/executor.py (used by both)
class CommandExecutor:
    def execute(self, command: CLICommand) -> Dict[str, Any]:
        # Build command
        cmd_list = self.build_command(command)
        
        # Execute based on mode
        if self.mode == ExecutionMode.DRY_RUN:
            return {"executed": False, "output": "Would execute..."}
        
        # Real execution
        result = subprocess.run(cmd_list, ...)
        return {"executed": True, "success": True, ...}
```

## File Relationships

```
log-whisperer/
├── models.py                    # Shared data models
│   ├── CLICommand              # Used by both
│   ├── FaultReport             # From council agent
│   └── RemediationPlan         # From writer agent
│
├── execution/
│   └── executor.py             # ⚡ SHARED EXECUTOR
│       └── CommandExecutor     # Used by both demos
│
├── agents/
│   ├── council_agent.py        # Step 2: Root cause analysis
│   └── writer_agent.py         # Step 3: Generate commands
│
├── api/
│   └── pipeline.py             # Full pipeline orchestration
│
├── demo_interactive.py         # Standalone execution demo
└── demo_pretty_pipeline.py     # Full pipeline demo
```

## Running Each Demo

### Standalone Execution Demo
```bash
./run_demo.sh
# Choose mode: dry/safe/full
# See: Execution only (step 6)
# No API keys needed
```

### Full Pipeline Demo
```bash
# Requires ANTHROPIC_API_KEY in .env
python3 demo_pretty_pipeline.py
# See: Complete flow (steps 1-7)
# Council debate → Writer → Execution
```

## Key Insight

The `demo_interactive.py` is like a **unit test** for the executor:
- Tests execution in isolation
- Proves it works with real git commands
- Shows all three modes
- Fast and simple

The full pipeline is the **integration test**:
- Tests all components together
- Shows AI agents making decisions
- Generates commands dynamically
- Uses the same executor at the end

## Code Proof

### In demo_interactive.py (line ~200)
```python
executor = CommandExecutor(mode=execution_mode, working_dir=demo_dir)
result = executor.execute(command)
```

### In api/pipeline.py (line ~135)
```python
from execution.executor import get_executor
executor = get_executor(execution_mode)
result = executor.execute(cmd)
```

**Same executor, same execution logic, same real git commands!**

## Summary

| Aspect | demo_interactive.py | Full Pipeline |
|--------|-------------------|---------------|
| **Scope** | Execution only | Complete flow |
| **Components** | Executor | Council + Writer + Executor |
| **Input** | Hardcoded command | AI-generated commands |
| **API Keys** | Not needed | Required |
| **Purpose** | Prove execution works | Show full system |
| **Executor** | ✅ Same | ✅ Same |
| **Commands** | ✅ Same model | ✅ Same model |
| **Git Execution** | ✅ Real | ✅ Real |

## Try Both!

### Quick Demo (No API Key)
```bash
./run_demo.sh
# Type: full
# See real git execution
```

### Full System (With API Key)
```bash
# Add ANTHROPIC_API_KEY to .env
python3 demo_pretty_pipeline.py
# See AI agents + execution
```

Both use the **same executor** to run **real git commands**. The difference is how the commands are generated:
- Interactive demo: Hardcoded command
- Full pipeline: AI-generated commands

The execution is identical! 🚀
