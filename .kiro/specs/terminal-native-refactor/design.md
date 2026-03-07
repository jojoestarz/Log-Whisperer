# Design Document: Terminal-Native Refactor

## Overview

This design specifies the refactoring of Log Whisperer from a web-based architecture (FastAPI + React) to a terminal-native Python monorepo. The refactored application will provide a pure terminal user experience using click for CLI, rich/textual for terminal UI, and will remove all web dependencies while preserving the core multi-agent incident remediation functionality.

### Goals

- Remove all web dependencies (FastAPI, uvicorn, React, httpx)
- Implement a click-based CLI for user interaction
- Replace web UI with rich/textual terminal components
- Refactor FastAPI orchestrator to pure Python pipeline
- Maintain existing agent functionality and safety gates
- Support demo mode for safe demonstrations
- Preserve structured logging and observability

### Non-Goals

- Changing the core AI agent logic (Decision Agent, Writer Agent)
- Modifying the incident data format or structure
- Implementing new remediation tools beyond existing ones
- Adding distributed execution or multi-node support
- Creating a TUI framework from scratch (use existing libraries)

## Architecture

### High-Level Architecture

The refactored application follows a layered architecture:

```
┌─────────────────────────────────────────────────────┐
│              CLI Entry Point (click)                │
│         cli/main.py - User Commands                 │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│         Terminal UI Layer (rich/textual)            │
│    viz/terminal_grid.py, viz/terminal_logger.py     │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│       Pipeline Orchestrator (Pure Python)           │
│              api/pipeline.py                        │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Decision   │ │    Writer    │ │    Safety    │
│    Agent     │ │    Agent     │ │     Gate     │
└──────────────┘ └──────────────┘ └──────────────┘
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│            Shared Data Models (Pydantic)            │
│                  models.py                          │
└─────────────────────────────────────────────────────┘
```

### Directory Structure

The monorepo is organized into six top-level directories:

```
log-whisperer/
├── agents/              # AI agents
│   ├── decision_agent.py
│   └── writer_agent.py
├── api/                 # Pure Python orchestrator
│   └── pipeline.py
├── cli/                 # Click-based CLI entry point
│   └── main.py
├── data/                # Incident data files
│   └── cloudflare_incident.json
├── safety/              # Safety validation
│   ├── argo_mock.py
│   └── mcp_tools.py
├── viz/                 # Terminal UI components
│   ├── terminal_grid.py
│   └── terminal_logger.py
├── models.py            # Shared Pydantic models
├── config.py            # Configuration parser
├── requirements.txt     # Dependencies
└── .env.example         # Environment template
```

### Key Architectural Decisions

1. **CLI over Web API**: Replace FastAPI endpoints with click commands for direct terminal interaction
2. **Rich/Textual for UI**: Use established terminal UI libraries instead of building custom TUI
3. **Pure Python Orchestration**: Remove async web framework overhead, use simple async/await for agent coordination
4. **Stateful CLI**: Maintain pipeline state in memory and persist to disk for history
5. **Demo Mode First**: Ensure demo mode works without external dependencies for safe demonstrations

## Components and Interfaces

### CLI Entry Point (cli/main.py)

The CLI provides the primary user interface using click.

**Commands**:

```python
@click.group()
@click.option('--demo', is_flag=True, help='Run in demo mode')
@click.option('--log-level', default='INFO', help='Logging level')
def cli(demo: bool, log_level: str):
    """Log Whisperer - Terminal-native incident remediation"""
    pass

@cli.command()
@click.option('--file', default='cloudflare_incident.json', help='Incident data file')
def trigger(file: str):
    """Trigger incident remediation pipeline"""
    pass

@cli.command()
@click.argument('incident_id')
def status(incident_id: str):
    """Check pipeline status for an incident"""
    pass

@cli.command()
@click.argument('incident_id')
def approve(incident_id: str):
    """Approve remediation plan for execution"""
    pass

@cli.command()
@click.argument('incident_id')
def reject(incident_id: str):
    """Reject remediation plan"""
    pass

@cli.command()
def history():
    """List past pipeline executions"""
    pass

@cli.command()
@click.argument('incident_id')
def show(incident_id: str):
    """Show details of a specific pipeline execution"""
    pass
```

**Interface Contract**:
- Input: Command-line arguments and options
- Output: Terminal display via rich/textual components
- Side Effects: Updates pipeline state, persists to disk
- Error Handling: Display user-friendly error messages with click.echo()

### Pipeline Orchestrator (api/pipeline.py)

Pure Python orchestrator that coordinates agent execution without web framework dependencies.

**Key Functions**:

```python
class PipelineOrchestrator:
    def __init__(self):
        self.states: dict[str, PipelineState] = {}
        self.gate = ArgoSafetyGate()
        
    async def trigger_remediation(
        self, 
        incident_id: str, 
        events: list[LogEvent]
    ) -> PipelineState:
        """Execute full remediation pipeline"""
        pass
        
    async def get_status(self, incident_id: str) -> PipelineState:
        """Retrieve pipeline state"""
        pass
        
    async def approve_plan(self, incident_id: str) -> PipelineState:
        """Approve and execute remediation plan"""
        pass
        
    async def reject_plan(self, incident_id: str) -> PipelineState:
        """Reject remediation plan"""
        pass
        
    def save_state(self, state: PipelineState) -> None:
        """Persist pipeline state to disk"""
        pass
        
    def load_state(self, incident_id: str) -> PipelineState:
        """Load pipeline state from disk"""
        pass
```

**Interface Contract**:
- Input: Incident data as Python objects (LogEvent list)
- Output: PipelineState objects
- Side Effects: Calls agents, updates state, persists to disk
- Error Handling: Catch exceptions, update state.status to "failed", log errors

**Pipeline Flow**:

1. **Investigation Phase**: Call Decision Agent with log events
2. **Planning Phase**: Call Writer Agent with fault report
3. **Dry-Run Phase**: Validate commands through Safety Gate
4. **Approval Phase**: Wait for human approval (blocking)
5. **Execution Phase**: Execute approved commands (simulated in demo mode)
6. **Resolution Phase**: Mark incident as resolved, calculate MTTR

### Terminal Grid Visualization (viz/terminal_grid.py)

Displays pipeline state using rich panels and tables.

**Key Functions**:

```python
class TerminalGrid:
    def __init__(self):
        self.console = Console()
        
    def display_pipeline_state(self, state: PipelineState) -> None:
        """Display full pipeline state with panels"""
        pass
        
    def display_fault_report(self, report: FaultReport) -> None:
        """Display Decision Agent analysis results"""
        pass
        
    def display_remediation_plan(self, plan: RemediationPlan) -> None:
        """Display Writer Agent commands in table format"""
        pass
        
    def display_dry_run_results(self, results: list[DryRunResult]) -> None:
        """Display safety validation results with color coding"""
        pass
        
    def display_approval_prompt(self, plan: RemediationPlan) -> None:
        """Display approval prompt with plan summary"""
        pass
        
    def display_timeline(self, state: PipelineState) -> None:
        """Display pipeline stage timeline"""
        pass
```

**Display Format**:

```
╭─────────────────────────────────────────────────────╮
│ 🚨 Incident: inc-abc123                             │
│ Status: awaiting_approval                           │
│ Created: 2024-01-15 10:23:45 UTC                    │
╰─────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────╮
│ 🔍 Decision Agent Analysis                          │
├─────────────────────────────────────────────────────┤
│ Root Cause: BGP config push #4821 contained an     │
│ empty-string prefix list                            │
│                                                      │
│ Severity: P1                                        │
│ Confidence: 97%                                     │
│ Affected Services: bgp-router-lon01, api-gateway   │
╰─────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────╮
│ 📋 Remediation Plan (plan-abc123)                   │
├─────────────────────────────────────────────────────┤
│ ┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ Tool          ┃ Description                   ┃ │
│ ┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ git_revert    │ Revert bad BGP config #4821  │ │
│ │ argo_sync     │ Sync Argo CD to apply config │ │
│ │ service_restart│ Restart DNS resolver        │ │
│ └───────────────┴───────────────────────────────┘ │
│                                                      │
│ Overall Risk: low                                   │
│ Estimated Recovery: 4 minutes                       │
│ Dry-Run: ✅ PASSED                                  │
╰─────────────────────────────────────────────────────╯

Approve this plan? (yes/no):
```

### Terminal Logger (viz/terminal_logger.py)

Structured logging with rich formatting.

**Key Functions**:

```python
class TerminalLogger:
    def __init__(self, console: Console):
        self.console = console
        self.log = structlog.get_logger()
        
    def log_stage(self, stage: str, message: str, level: str) -> None:
        """Log pipeline stage with emoji and color"""
        pass
        
    def log_agent_reasoning(self, agent: str, reasoning: str) -> None:
        """Log agent reasoning steps"""
        pass
        
    def log_command_execution(self, command: CLICommand) -> None:
        """Log command execution attempt"""
        pass
        
    def log_error(self, error: Exception, context: dict) -> None:
        """Log error with context"""
        pass
        
    def display_demo_indicator(self) -> None:
        """Display prominent demo mode indicator"""
        pass
```

**Log Format**:

```
[10:23:45] 🚨 CRITICAL  incident/anomaly    Anomaly detected — starting investigation
[10:23:46] ℹ️  INFO      agents/decision     Analyzing 47 log events
[10:23:48] ✅ INFO      agents/decision     Root cause: BGP config push #4821
[10:23:48] ℹ️  INFO      agents/writer       Generating remediation commands
[10:23:50] 📋 INFO      agents/writer       3 commands generated
[10:23:50] 🔒 WARN      safety/dryrun       Running Argo CD safety dry-run...
[10:23:51] ✅ INFO      safety/dryrun       Dry-run passed — awaiting human approval
```

### Safety Gate (safety/argo_mock.py, safety/mcp_tools.py)

Validates commands through dry-run simulation.

**argo_mock.py**:

```python
class ArgoSafetyGate:
    async def run_dry_run(self, command: CLICommand) -> DryRunResult:
        """Simulate Argo CD dry-run validation"""
        pass
        
    async def validate_plan(
        self, 
        plan: RemediationPlan
    ) -> tuple[RemediationPlan, list[DryRunResult]]:
        """Validate all commands in plan"""
        pass
```

**mcp_tools.py**:

```python
class MCPTools:
    def __init__(self):
        self.tools = self._load_tool_definitions()
        
    def validate_command(self, command: CLICommand) -> bool:
        """Validate command arguments against tool schema"""
        pass
        
    def execute_command(
        self, 
        command: CLICommand, 
        dry_run: bool = True
    ) -> dict:
        """Execute or simulate command execution"""
        pass
        
    def _load_tool_definitions(self) -> dict:
        """Load MCP tool schemas"""
        pass
```

**Tool Definitions**:

```python
TOOL_SCHEMAS = {
    "git_revert": {
        "args": {
            "commit_hash": {"type": "string", "required": True},
            "repo": {"type": "string", "required": True}
        },
        "risk_factors": ["repo_head_moves", "ci_cd_triggers"]
    },
    "kubectl_apply": {
        "args": {
            "manifest": {"type": "string", "required": True},
            "namespace": {"type": "string", "required": True}
        },
        "risk_factors": ["pod_restart", "traffic_shift"]
    },
    "kubectl_scale": {
        "args": {
            "deployment": {"type": "string", "required": True},
            "replicas": {"type": "integer", "required": True},
            "namespace": {"type": "string", "required": True}
        },
        "risk_factors": ["capacity_change", "load_balancer_rebalance"]
    },
    "argo_sync": {
        "args": {
            "app_name": {"type": "string", "required": True},
            "prune": {"type": "boolean", "required": False}
        },
        "risk_factors": ["state_enforcement", "drift_correction"]
    },
    "service_restart": {
        "args": {
            "service": {"type": "string", "required": True},
            "namespace": {"type": "string", "required": True}
        },
        "risk_factors": ["service_downtime_15s"]
    }
}
```

### Configuration Parser (config.py)

Loads and validates environment configuration.

**Enhanced Configuration**:

```python
class Config:
    def __init__(self):
        load_dotenv()
        self.anthropic_api_key = self._get_required("ANTHROPIC_API_KEY")
        self.demo_mode = self._get_bool("DEMO_MODE", default=True)
        self.log_level = self._get("LOG_LEVEL", default="INFO")
        self.argo_mock = self._get_bool("ARGO_MOCK", default=True)
        self.model = self._get("MODEL", default="claude-sonnet-4-20250514")
        self.pipeline_history_dir = self._get("PIPELINE_HISTORY_DIR", default=".pipeline_history")
        
    def _get_required(self, key: str) -> str:
        """Get required environment variable or raise error"""
        pass
        
    def _get(self, key: str, default: str) -> str:
        """Get optional environment variable with default"""
        pass
        
    def _get_bool(self, key: str, default: bool) -> bool:
        """Get boolean environment variable"""
        pass
        
    def validate(self) -> list[str]:
        """Validate configuration and return list of errors"""
        pass
```

## Data Models

All data models are defined in `models.py` using Pydantic for validation and serialization.

### Existing Models (Preserved)

```python
class LogEvent(BaseModel):
    timestamp: str
    service: str
    level: Literal["DEBUG", "INFO", "WARN", "ERROR", "CRIT"]
    msg: str
    correlated_event: str | None = None

class FaultReport(BaseModel):
    root_cause: str
    affected_services: list[str]
    severity: Literal["P1", "P2", "P3"]
    fix_type: Literal["config_rollback", "service_restart", "route_fix", "cert_renewal", "scale_up"]
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    time_of_failure: str

class CLICommand(BaseModel):
    tool: Literal["git_revert", "kubectl_apply", "kubectl_scale", "argo_sync", "service_restart"]
    args: dict[str, str]
    description: str
    risk_level: Literal["low", "medium", "high"]

class RemediationPlan(BaseModel):
    plan_id: str
    commands: list[CLICommand]
    rollback_commands: list[CLICommand]
    estimated_recovery_mins: int
    overall_risk: Literal["low", "medium", "high"]
    dry_run_passed: bool = False

class DryRunResult(BaseModel):
    command: CLICommand
    would_succeed: bool
    side_effects: list[str]
    risk_score: float = Field(ge=0.0, le=1.0)
    safe_to_execute: bool

class PipelineState(BaseModel):
    incident_id: str
    status: Literal["idle", "investigating", "planning", "dry_running", "awaiting_approval", "executing", "resolved", "failed"]
    fault_report: FaultReport | None = None
    remediation_plan: RemediationPlan | None = None
    dry_run_results: list[DryRunResult] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: datetime | None = None
```

### New Models

```python
class ExecutionLog(BaseModel):
    """Tracks command execution history"""
    command: CLICommand
    executed_at: datetime
    success: bool
    output: str
    error: str | None = None

class PipelineHistory(BaseModel):
    """Historical record of pipeline execution"""
    incident_id: str
    state: PipelineState
    execution_logs: list[ExecutionLog] = []
    saved_at: datetime = Field(default_factory=datetime.utcnow)
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Pydantic Model Serialization Round-Trip

For any valid instance of any Pydantic model (FaultReport, RemediationPlan, CLICommand, DryRunResult, PipelineState, ExecutionLog, LogEvent), serializing to JSON then deserializing SHALL produce an equivalent object with all fields preserved.

**Validates: Requirements 2.7, 14.7, 19.7, 20.7**

### Property 2: CLI Invalid Argument Handling

For any invalid command-line arguments provided to any CLI command, the CLI SHALL display a helpful error message and exit with a non-zero status code without executing the command.

**Validates: Requirements 5.7**

### Property 3: Pipeline Error Recovery

For any error that occurs during pipeline orchestration (agent failure, network error, validation failure), the Pipeline_Orchestrator SHALL log the error with context, update the PipelineState status to "failed", and persist the state to disk.

**Validates: Requirements 6.6, 17.1**

### Property 4: Safety Gate Command Validation

For any CLICommand, the Safety_Gate SHALL validate it through dry-run simulation and return a DryRunResult containing: (1) a calculated risk_score between 0.0 and 1.0, (2) a list of identified side_effects, and (3) a safe_to_execute flag that is false when risk_score exceeds 0.8.

**Validates: Requirements 12.1, 12.3, 12.4, 12.6**

### Property 5: Demo Mode Cached Responses

For any agent invocation (Decision_Agent or Writer_Agent) when DEMO_MODE is true, the agent SHALL return cached responses without making external API calls, and all command executions SHALL be simulated without side effects.

**Validates: Requirements 9.5, 16.1, 16.2**

### Property 6: Demo Mode Safety Gate Behavior

For any CLICommand validated by the Safety_Gate when DEMO_MODE is true, the returned DryRunResult SHALL have safe_to_execute set to true regardless of the command's risk_level.

**Validates: Requirements 16.6**

### Property 7: Incident Data Validation

For any JSON file provided as incident data, the Log_Whisperer SHALL validate its structure against the LogEvent schema, and if the structure is valid, parse it into a list of LogEvent objects; if the structure is invalid, display a descriptive error message indicating which fields are malformed.

**Validates: Requirements 14.2, 14.3, 14.4**

### Property 8: MCP Tools Argument Validation

For any CLICommand, the mcp_tools module SHALL validate the command's arguments against the tool's schema, and if arguments are invalid (missing required fields, wrong types, or unknown fields), return validation errors listing the specific issues.

**Validates: Requirements 15.3, 15.4**

### Property 9: MCP Tools Dry-Run Support

For any supported tool (git_revert, kubectl_apply, kubectl_scale, argo_sync, service_restart), the mcp_tools module SHALL support dry-run mode execution that simulates the command without side effects and returns the expected outcome.

**Validates: Requirements 15.5**

### Property 10: MCP Tools Invocation Logging

For any tool invocation through mcp_tools, the module SHALL log the invocation with the tool name, arguments, execution mode (dry-run or live), and result (success or failure with error details).

**Validates: Requirements 15.6, 15.7**

### Property 11: Network Error Retry

For any network error that occurs during external API calls, the Log_Whisperer SHALL retry the operation up to 3 times with exponential backoff, and if all retries fail, log the final error and update the pipeline state accordingly.

**Validates: Requirements 17.2**

### Property 12: Input Data Validation

For any input data provided to the Log_Whisperer (incident files, configuration values, CLI arguments), the system SHALL validate the data before processing, and if validation fails, display a helpful error message indicating what is invalid and how to fix it.

**Validates: Requirements 17.4, 17.5**

### Property 13: Unhandled Exception Logging

For any unhandled exception that occurs during execution, the Log_Whisperer SHALL catch the exception, log it with full stack trace and context, attempt to save the current PipelineState to disk, and exit gracefully with an appropriate error message.

**Validates: Requirements 17.6, 17.7**

### Property 14: Pipeline State Transition Logging

For any pipeline state transition (idle → investigating → planning → dry_running → awaiting_approval → executing → resolved/failed), the Log_Whisperer SHALL log the transition with timestamp, previous state, new state, and the trigger that caused the transition.

**Validates: Requirements 18.2**

### Property 15: Agent Invocation Logging

For any agent invocation (Decision_Agent or Writer_Agent), the Log_Whisperer SHALL log the agent name, input data summary, execution start time, execution end time, and output data summary.

**Validates: Requirements 18.3**

### Property 16: Command Execution Logging

For any command execution attempt, the Log_Whisperer SHALL log the command details (tool, args, description), execution mode (dry-run or live), execution result (success or failure), and any output or error messages.

**Validates: Requirements 18.4**

### Property 17: Log Entry Timestamps and Dual Output

For any log entry generated by the Log_Whisperer, the entry SHALL include a timestamp in ISO 8601 format and be written to both the terminal (via rich.console) and a log file in the .pipeline_history directory.

**Validates: Requirements 18.6, 18.7**

### Property 18: Configuration Missing Variable Errors

For any required configuration variable that is missing from the environment, the Log_Whisperer SHALL display an error message listing all missing variables with descriptions of what they are used for, and exit without attempting to start the application.

**Validates: Requirements 19.3**

### Property 19: Configuration Default Values

For any optional configuration variable that is not provided in the environment, the Log_Whisperer SHALL use a documented default value and log that the default is being used.

**Validates: Requirements 19.4**

### Property 20: Pipeline State Persistence

For any pipeline stage completion (investigation, planning, dry-run, approval, execution), the Pipeline_Orchestrator SHALL serialize the current PipelineState to JSON and save it to the .pipeline_history directory with a filename based on the incident_id and timestamp.

**Validates: Requirements 20.1**

## Error Handling

### Error Categories

The application handles four categories of errors:

1. **User Input Errors**: Invalid CLI arguments, malformed incident data, missing configuration
2. **External Service Errors**: Anthropic API failures, network timeouts, rate limiting
3. **Validation Errors**: Invalid command arguments, unsafe commands, schema violations
4. **System Errors**: File I/O failures, permission errors, unexpected exceptions

### Error Handling Strategy

**User Input Errors**:
- Validate all input before processing
- Display clear, actionable error messages
- Suggest corrections when possible
- Exit with non-zero status code
- Never proceed with invalid input

**External Service Errors**:
- Implement retry logic with exponential backoff (3 attempts)
- Log all retry attempts with context
- Fall back to demo mode if configured
- Update pipeline state to "failed" if all retries exhausted
- Preserve partial results when possible

**Validation Errors**:
- Validate commands through Safety Gate before execution
- Block unsafe commands (risk_score > 0.8)
- Display validation errors with specific issues
- Require human approval for medium-risk commands
- Log all validation attempts and results

**System Errors**:
- Catch all unhandled exceptions at top level
- Log full stack trace with context
- Attempt to save pipeline state before exit
- Display user-friendly error message
- Exit gracefully with appropriate status code

### Error Recovery

The application implements graceful degradation:

1. **Demo Mode Fallback**: If external APIs fail and DEMO_MODE is configured, fall back to cached responses
2. **State Persistence**: Save pipeline state after each stage to enable recovery
3. **Partial Results**: Preserve and display partial results even if pipeline fails
4. **Rollback Commands**: Generate rollback commands for all remediation actions
5. **Safe Defaults**: Use safe default values for optional configuration

### Error Messages

All error messages follow this format:

```
❌ ERROR: [Category] [Brief Description]

Details:
  - [Specific issue 1]
  - [Specific issue 2]

Suggestion:
  [Actionable advice on how to fix]

For more information, see: [documentation link or log file path]
```

Example:

```
❌ ERROR: Configuration - Missing Required Variables

Details:
  - ANTHROPIC_API_KEY is not set
  - This is required for AI agent functionality

Suggestion:
  1. Copy .env.example to .env
  2. Add your Anthropic API key to .env
  3. Or enable DEMO_MODE=true for demonstration without API

For more information, see: .env.example
```

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit tests and property-based tests to ensure comprehensive coverage:

**Unit Tests**:
- Specific examples demonstrating correct behavior
- Edge cases and boundary conditions
- Integration points between components
- Error conditions and exception handling
- Demo mode behavior verification
- CLI command structure and help text

**Property-Based Tests**:
- Universal properties that hold for all inputs
- Comprehensive input coverage through randomization
- Round-trip serialization for all models
- Error handling across all error types
- Validation behavior for all command types
- State transitions for all pipeline stages

Both approaches are complementary and necessary: unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across the input space.

### Property-Based Testing Configuration

**Library Selection**: Use `hypothesis` for Python property-based testing

**Test Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Configurable seed for reproducibility
- Shrinking enabled to find minimal failing examples
- Deadline of 5 seconds per test case

**Test Tagging**:
Each property test MUST include a comment referencing its design document property:

```python
@given(pipeline_state=pipeline_states())
def test_pipeline_state_serialization_roundtrip(pipeline_state):
    """
    Feature: terminal-native-refactor, Property 1: Pydantic Model Serialization Round-Trip
    
    For any valid PipelineState, serializing to JSON then deserializing
    SHALL produce an equivalent object.
    """
    json_str = pipeline_state.model_dump_json()
    restored = PipelineState.model_validate_json(json_str)
    assert restored == pipeline_state
```

### Test Organization

```
log-whisperer/tests/
├── unit/
│   ├── test_cli_commands.py          # CLI structure and help text
│   ├── test_pipeline_orchestrator.py # Pipeline flow and integration
│   ├── test_agents.py                # Agent behavior and demo mode
│   ├── test_safety_gate.py           # Safety validation logic
│   ├── test_terminal_ui.py           # UI component behavior
│   ├── test_config.py                # Configuration parsing
│   └── test_incident_loading.py      # Incident data loading
├── property/
│   ├── test_model_serialization.py   # Property 1: Round-trip serialization
│   ├── test_cli_error_handling.py    # Property 2: Invalid argument handling
│   ├── test_error_recovery.py        # Property 3: Pipeline error recovery
│   ├── test_safety_validation.py     # Property 4-6: Safety gate properties
│   ├── test_incident_validation.py   # Property 7: Incident data validation
│   ├── test_mcp_tools.py             # Property 8-10: MCP tools properties
│   ├── test_network_retry.py         # Property 11: Network error retry
│   ├── test_input_validation.py      # Property 12: Input data validation
│   ├── test_exception_handling.py    # Property 13: Unhandled exceptions
│   ├── test_logging.py               # Property 14-17: Logging properties
│   ├── test_configuration.py         # Property 18-19: Configuration properties
│   └── test_state_persistence.py     # Property 20: State persistence
├── integration/
│   ├── test_full_pipeline.py         # End-to-end pipeline execution
│   ├── test_demo_mode.py             # Full demo mode workflow
│   └── test_approval_workflow.py     # Human approval workflow
└── conftest.py                        # Shared fixtures and generators
```

### Hypothesis Generators

Define custom generators for domain models:

```python
from hypothesis import strategies as st
from models import *

@st.composite
def log_events(draw):
    return LogEvent(
        timestamp=draw(st.datetimes().map(lambda dt: dt.isoformat())),
        service=draw(st.text(min_size=1, max_size=50)),
        level=draw(st.sampled_from(["DEBUG", "INFO", "WARN", "ERROR", "CRIT"])),
        msg=draw(st.text(min_size=1, max_size=200)),
        correlated_event=draw(st.none() | st.text(min_size=1, max_size=50))
    )

@st.composite
def fault_reports(draw):
    return FaultReport(
        root_cause=draw(st.text(min_size=10, max_size=200)),
        affected_services=draw(st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=10)),
        severity=draw(st.sampled_from(["P1", "P2", "P3"])),
        fix_type=draw(st.sampled_from(["config_rollback", "service_restart", "route_fix", "cert_renewal", "scale_up"])),
        confidence=draw(st.floats(min_value=0.0, max_value=1.0)),
        summary=draw(st.text(min_size=10, max_size=500)),
        time_of_failure=draw(st.datetimes().map(lambda dt: dt.isoformat()))
    )

@st.composite
def cli_commands(draw):
    tool = draw(st.sampled_from(["git_revert", "kubectl_apply", "kubectl_scale", "argo_sync", "service_restart"]))
    args = draw(st.dictionaries(st.text(min_size=1, max_size=20), st.text(min_size=1, max_size=100)))
    return CLICommand(
        tool=tool,
        args=args,
        description=draw(st.text(min_size=10, max_size=200)),
        risk_level=draw(st.sampled_from(["low", "medium", "high"]))
    )

@st.composite
def pipeline_states(draw):
    return PipelineState(
        incident_id=draw(st.text(min_size=5, max_size=50)),
        status=draw(st.sampled_from(["idle", "investigating", "planning", "dry_running", "awaiting_approval", "executing", "resolved", "failed"])),
        fault_report=draw(st.none() | fault_reports()),
        remediation_plan=draw(st.none() | remediation_plans()),
        dry_run_results=draw(st.lists(dry_run_results(), max_size=10)),
        created_at=draw(st.datetimes()),
        resolved_at=draw(st.none() | st.datetimes())
    )
```

### Test Coverage Goals

- Unit test coverage: 80% minimum
- Property test coverage: All 20 properties implemented
- Integration test coverage: All critical user workflows
- Edge case coverage: All identified edge cases from requirements

### Continuous Testing

- Run unit tests on every commit
- Run property tests on every pull request
- Run integration tests before release
- Monitor test execution time and optimize slow tests
- Track flaky tests and fix root causes

