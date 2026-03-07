# Implementation Plan: Terminal-Native Refactor

## Overview

This plan converts Log Whisperer from a web-based architecture (FastAPI + React) to a terminal-native Python monorepo. The implementation follows a bottom-up approach: first establishing shared data models and configuration, then building core components (agents, safety gate, orchestrator), and finally wiring everything together with CLI and terminal UI.

## Tasks

- [ ] 1. Set up monorepo structure and shared data models
  - [x] 1.1 Create directory structure for monorepo
    - Create six top-level directories: agents/, api/, cli/, data/, safety/, viz/
    - Create __init__.py files in each directory for proper Python module structure
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

  - [ ] 1.2 Implement shared Pydantic models in models.py
    - Define LogEvent model with timestamp, service, level, msg, correlated_event fields
    - Define FaultReport model with root_cause, affected_services, severity, fix_type, confidence, summary, time_of_failure fields
    - Define CLICommand model with tool, args, description, risk_level fields
    - Define RemediationPlan model with plan_id, commands, rollback_commands, estimated_recovery_mins, overall_risk, dry_run_passed fields
    - Define DryRunResult model with command, would_succeed, side_effects, risk_score, safe_to_execute fields
    - Define PipelineState model with incident_id, status, fault_report, remediation_plan, dry_run_results, created_at, resolved_at fields
    - Define ExecutionLog model with command, executed_at, success, output, error fields
    - Define PipelineHistory model with incident_id, state, execution_logs, saved_at fields
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 1.8_

  - [ ]* 1.3 Write property test for Pydantic model serialization
    - **Property 1: Pydantic Model Serialization Round-Trip**
    - **Validates: Requirements 2.7, 14.7, 19.7, 20.7**
    - Test that all models (LogEvent, FaultReport, CLICommand, RemediationPlan, DryRunResult, PipelineState, ExecutionLog, PipelineHistory) can serialize to JSON and deserialize back to equivalent objects
    - Use hypothesis generators for comprehensive input coverage

- [ ] 2. Implement configuration management
  - [ ] 2.1 Create config.py with environment variable parsing
    - Implement Config class with _get_required, _get, _get_bool helper methods
    - Parse ANTHROPIC_API_KEY, DEMO_MODE, LOG_LEVEL, ARGO_MOCK, MODEL, PIPELINE_HISTORY_DIR from environment
    - Implement validate() method to check for missing required variables
    - Use python-dotenv to load .env file
    - _Requirements: 9.7, 19.1, 19.2, 19.5, 19.6_

  - [ ] 2.2 Create .env.example with all configuration variables
    - Include ANTHROPIC_API_KEY with placeholder value
    - Include DEMO_MODE=true as default
    - Include LOG_LEVEL=INFO as default
    - Include ARGO_MOCK=true as default
    - Include MODEL=claude-sonnet-4-20250514 as default
    - Include PIPELINE_HISTORY_DIR=.pipeline_history as default
    - Add comments explaining each variable's purpose
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

  - [ ]* 2.3 Write property tests for configuration validation
    - **Property 18: Configuration Missing Variable Errors**
    - **Validates: Requirements 19.3**
    - Test that missing required variables produce helpful error messages
    - **Property 19: Configuration Default Values**
    - **Validates: Requirements 19.4**
    - Test that optional variables use documented defaults when not provided

- [ ] 3. Implement MCP tools and safety gate
  - [ ] 3.1 Create mcp_tools.py with tool definitions and validation
    - Define TOOL_SCHEMAS dictionary with git_revert, kubectl_apply, kubectl_scale, argo_sync, service_restart schemas
    - Implement MCPTools class with validate_command, execute_command, _load_tool_definitions methods
    - Implement argument validation against tool schemas
    - Implement dry-run mode support for all tools
    - Add logging for all tool invocations
    - _Requirements: 15.1, 15.2, 15.3, 15.5, 15.6_

  - [ ]* 3.2 Write property tests for MCP tools
    - **Property 8: MCP Tools Argument Validation**
    - **Validates: Requirements 15.3, 15.4**
    - Test that invalid arguments (missing required, wrong types, unknown fields) return validation errors
    - **Property 9: MCP Tools Dry-Run Support**
    - **Validates: Requirements 15.5**
    - Test that all tools support dry-run mode without side effects
    - **Property 10: MCP Tools Invocation Logging**
    - **Validates: Requirements 15.6, 15.7**
    - Test that all invocations are logged with tool name, args, mode, and result

  - [ ] 3.3 Create argo_mock.py with safety gate implementation
    - Implement ArgoSafetyGate class with run_dry_run and validate_plan methods
    - Implement risk_score calculation based on command type and arguments
    - Implement side_effects identification for each tool type
    - Set safe_to_execute to false when risk_score > 0.8
    - Support all five tool types: git_revert, kubectl_apply, kubectl_scale, argo_sync, service_restart
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.7_

  - [ ]* 3.4 Write property tests for safety gate validation
    - **Property 4: Safety Gate Command Validation**
    - **Validates: Requirements 12.1, 12.3, 12.4, 12.6**
    - Test that all commands return DryRunResult with risk_score (0.0-1.0), side_effects list, and safe_to_execute flag
    - Test that risk_score > 0.8 results in safe_to_execute = false
    - **Property 6: Demo Mode Safety Gate Behavior**
    - **Validates: Requirements 16.6**
    - Test that demo mode always returns safe_to_execute = true

- [ ] 4. Checkpoint - Verify foundation components
  - Ensure all tests pass for models, config, and safety gate
  - Verify that configuration loads correctly from .env
  - Ask the user if questions arise

- [ ] 5. Implement AI agents with demo mode support
  - [ ] 5.1 Create decision_agent.py with root cause analysis
    - Implement DecisionAgent class with analyze_incident method
    - Accept list of LogEvent objects as input
    - Return FaultReport object with root_cause, affected_services, severity, fix_type, confidence
    - Implement demo mode: return cached FaultReport when DEMO_MODE=true
    - Implement live mode: call Anthropic API with incident logs
    - Add error handling: return low-confidence FaultReport on API failure
    - Implement retry logic with exponential backoff (3 attempts)
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

  - [ ] 5.2 Create writer_agent.py with remediation command generation
    - Implement WriterAgent class with generate_plan method
    - Accept FaultReport object as input
    - Return RemediationPlan object with commands and rollback_commands
    - Generate CLICommand objects with tool, args, description, risk_level
    - Implement demo mode: return cached RemediationPlan when DEMO_MODE=true
    - Implement live mode: call Anthropic API with fault report
    - Add error handling: return empty RemediationPlan on API failure
    - Implement retry logic with exponential backoff (3 attempts)
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

  - [ ]* 5.3 Write property tests for demo mode behavior
    - **Property 5: Demo Mode Cached Responses**
    - **Validates: Requirements 9.5, 16.1, 16.2**
    - Test that agents return cached responses without API calls when DEMO_MODE=true
    - Test that command executions are simulated without side effects in demo mode
    - **Property 11: Network Error Retry**
    - **Validates: Requirements 17.2**
    - Test that network errors trigger retry with exponential backoff (3 attempts)

- [ ] 6. Implement pipeline orchestrator
  - [ ] 6.1 Create pipeline.py with pure Python orchestration
    - Implement PipelineOrchestrator class with trigger_remediation, get_status, approve_plan, reject_plan methods
    - Implement save_state and load_state methods for persistence
    - Coordinate Decision_Agent and Writer_Agent execution in sequence
    - Pass FaultReport from Decision_Agent to Writer_Agent
    - Validate remediation plan through Safety_Gate before approval
    - Update PipelineState status through all stages: idle → investigating → planning → dry_running → awaiting_approval → executing → resolved/failed
    - Create .pipeline_history directory if it doesn't exist
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.7, 20.1, 20.2, 20.5_

  - [ ]* 6.2 Write property tests for pipeline error handling
    - **Property 3: Pipeline Error Recovery**
    - **Validates: Requirements 6.6, 17.1**
    - Test that errors during orchestration are logged, state is updated to "failed", and state is persisted
    - **Property 20: Pipeline State Persistence**
    - **Validates: Requirements 20.1**
    - Test that state is saved after each stage completion
    - Test that saved state can be loaded back to equivalent object

  - [ ]* 6.3 Write unit tests for pipeline orchestration flow
    - Test full pipeline flow: trigger → investigate → plan → dry-run → approve → execute → resolve
    - Test rejection flow: trigger → investigate → plan → reject → failed
    - Test error scenarios: agent failure, validation failure, execution failure

- [ ] 7. Checkpoint - Verify core pipeline functionality
  - Ensure all tests pass for agents and orchestrator
  - Verify demo mode works end-to-end without API calls
  - Verify pipeline state transitions correctly
  - Ask the user if questions arise

- [ ] 8. Implement terminal UI components
  - [ ] 8.1 Create terminal_logger.py with structured logging
    - Implement TerminalLogger class using rich.console and structlog
    - Implement log_stage method with emoji and color coding
    - Implement log_agent_reasoning method for agent reasoning steps
    - Implement log_command_execution method for command attempts
    - Implement log_error method with context and stack traces
    - Implement display_demo_indicator method for prominent demo mode indicator
    - Configure structlog to write to both terminal and log file
    - Use different colors for different log levels (DEBUG, INFO, WARN, ERROR, CRIT)
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 18.1, 18.6, 18.7_

  - [ ] 8.2 Create terminal_grid.py with rich panel visualization
    - Implement TerminalGrid class using rich.console, rich.panel, rich.table
    - Implement display_pipeline_state method with panels for incident overview
    - Implement display_fault_report method for Decision Agent analysis
    - Implement display_remediation_plan method with table for commands
    - Implement display_dry_run_results method with color-coded risk levels (green=low, yellow=medium, red=high)
    - Implement display_approval_prompt method with plan summary
    - Implement display_timeline method for pipeline stage progression
    - Highlight high-risk commands in red
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.6, 7.7_

  - [ ]* 8.3 Write property tests for logging behavior
    - **Property 14: Pipeline State Transition Logging**
    - **Validates: Requirements 18.2**
    - Test that all state transitions are logged with timestamp, previous state, new state, and trigger
    - **Property 15: Agent Invocation Logging**
    - **Validates: Requirements 18.3**
    - Test that agent invocations are logged with name, input summary, start time, end time, output summary
    - **Property 16: Command Execution Logging**
    - **Validates: Requirements 18.4**
    - Test that command executions are logged with details, mode, result, and output/errors
    - **Property 17: Log Entry Timestamps and Dual Output**
    - **Validates: Requirements 18.6, 18.7**
    - Test that all log entries include ISO 8601 timestamps and are written to both terminal and file

  - [ ]* 8.4 Write unit tests for terminal UI display
    - Test that panels render correctly for different pipeline states
    - Test that tables format commands properly
    - Test that color coding works for risk levels
    - Test that demo mode indicator is displayed prominently

- [ ] 9. Implement CLI entry point
  - [ ] 9.1 Create cli/main.py with click command group
    - Implement main command group with --demo and --log-level options
    - Implement trigger command with --file option to start remediation
    - Implement status command with incident_id argument to check pipeline state
    - Implement approve command with incident_id argument to approve plans
    - Implement reject command with incident_id argument to reject plans
    - Implement history command to list past pipeline executions
    - Implement show command with incident_id argument to display execution details
    - Display help text with --help flag
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 13.2, 13.3, 20.3, 20.4_

  - [ ] 9.2 Wire CLI commands to pipeline orchestrator
    - Connect trigger command to PipelineOrchestrator.trigger_remediation
    - Connect status command to PipelineOrchestrator.get_status
    - Connect approve command to PipelineOrchestrator.approve_plan
    - Connect reject command to PipelineOrchestrator.reject_plan
    - Connect history command to load all states from .pipeline_history
    - Connect show command to PipelineOrchestrator.load_state
    - Pass terminal UI components to orchestrator for display
    - _Requirements: 13.1, 13.4, 13.5, 20.6_

  - [ ] 9.3 Implement incident data loading
    - Load JSON incident files from data/ directory
    - Parse JSON into list of LogEvent objects
    - Validate JSON structure against LogEvent schema
    - Display descriptive error messages for malformed data
    - Support --file argument to specify custom incident file path
    - Default to data/cloudflare_incident.json
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 16.5_

  - [ ]* 9.4 Write property tests for CLI error handling
    - **Property 2: CLI Invalid Argument Handling**
    - **Validates: Requirements 5.7**
    - Test that invalid arguments display helpful error messages and exit with non-zero status
    - **Property 7: Incident Data Validation**
    - **Validates: Requirements 14.2, 14.3, 14.4**
    - Test that valid JSON parses to LogEvent objects
    - Test that invalid JSON displays descriptive error messages
    - **Property 12: Input Data Validation**
    - **Validates: Requirements 17.4, 17.5**
    - Test that all input data is validated before processing
    - Test that validation failures display helpful error messages

  - [ ]* 9.5 Write unit tests for CLI commands
    - Test that each command has correct structure and help text
    - Test that trigger command loads incident data and starts pipeline
    - Test that status command displays current pipeline state
    - Test that approve/reject commands update pipeline state correctly
    - Test that history command lists all past executions
    - Test that show command displays execution details

- [ ] 10. Implement error handling and recovery
  - [ ] 10.1 Add comprehensive error handling to all components
    - Wrap agent calls in try-except blocks with logging
    - Wrap file I/O operations in try-except blocks
    - Wrap API calls in try-except blocks with retry logic
    - Catch unhandled exceptions at top level in CLI
    - Save pipeline state before exiting on critical errors
    - _Requirements: 17.6, 17.7_

  - [ ] 10.2 Implement user-friendly error messages
    - Format error messages with category, details, and suggestions
    - Display missing configuration variables with descriptions
    - Display validation errors with specific issues
    - Display API errors with retry information
    - Include documentation links or log file paths in error messages
    - _Requirements: 9.6, 17.3, 17.5_

  - [ ]* 10.3 Write property test for exception handling
    - **Property 13: Unhandled Exception Logging**
    - **Validates: Requirements 17.6, 17.7**
    - Test that unhandled exceptions are caught, logged with stack trace, state is saved, and system exits gracefully

- [ ] 11. Implement demo mode features
  - [ ] 11.1 Create cached demo data
    - Create cached FaultReport for cloudflare_incident.json in agents/demo_data.py
    - Create cached RemediationPlan for cloudflare_incident.json in agents/demo_data.py
    - Add realistic timing delays (1-2 seconds) to simulate agent processing
    - _Requirements: 16.1, 16.4_

  - [ ] 11.2 Wire demo mode throughout application
    - Check DEMO_MODE in Config and pass to agents
    - Display demo mode indicator in terminal UI when active
    - Override DEMO_MODE with --demo CLI flag
    - Ensure Safety_Gate returns safe_to_execute=true in demo mode
    - Simulate command execution without side effects in demo mode
    - _Requirements: 16.3, 16.7, 8.5_

  - [ ]* 11.3 Write integration test for full demo mode workflow
    - Test complete pipeline execution in demo mode
    - Verify no external API calls are made
    - Verify no actual commands are executed
    - Verify demo indicator is displayed
    - Verify realistic timing delays

- [ ] 12. Remove web dependencies and clean up
  - [ ] 12.1 Update requirements.txt
    - Remove fastapi, uvicorn, httpx, and any React/frontend dependencies
    - Add anthropic, pydantic, rich, textual, click, python-dotenv, structlog
    - Add hypothesis for property-based testing
    - Add pytest for unit testing
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [ ] 12.2 Remove web-related files and directories
    - Delete ui/ directory containing React components
    - Remove any FastAPI route files
    - Remove any uvicorn server configuration
    - Verify no HTTP port binding code remains
    - _Requirements: 3.5, 3.6_

  - [ ] 12.3 Update documentation
    - Update README.md with terminal-native usage instructions
    - Document CLI commands and options
    - Document configuration variables
    - Document demo mode usage
    - Add examples of common workflows

- [ ] 13. Final integration and testing
  - [ ] 13.1 Run full integration tests
    - Test complete pipeline flow from trigger to resolution
    - Test approval workflow with human interaction
    - Test rejection workflow
    - Test error scenarios and recovery
    - Test demo mode end-to-end
    - Test state persistence and history commands
    - _Requirements: All requirements_

  - [ ]* 13.2 Run all property-based tests
    - Execute all 20 property tests with 100+ iterations each
    - Verify all properties hold across randomized inputs
    - Fix any failing properties
    - Document any edge cases discovered

  - [ ] 13.3 Verify all requirements are met
    - Review each requirement and verify implementation
    - Test each acceptance criterion
    - Verify no web dependencies remain
    - Verify terminal UI works correctly
    - Verify demo mode works without external dependencies
    - Verify error handling is comprehensive

- [ ] 14. Final checkpoint - Complete verification
  - Ensure all tests pass (unit, property, integration)
  - Verify application runs successfully in both demo and live modes
  - Verify all CLI commands work correctly
  - Verify terminal UI displays correctly
  - Ask the user if questions arise or if ready for deployment

## Notes

- Tasks marked with `*` are optional testing tasks that can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties across all inputs
- Unit tests validate specific examples and edge cases
- The implementation follows a bottom-up approach: models → config → tools → agents → orchestrator → UI → CLI
- Demo mode is prioritized to enable safe demonstrations without external dependencies
- All 20 correctness properties from the design document are covered by property tests
