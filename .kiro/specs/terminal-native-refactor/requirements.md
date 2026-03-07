# Requirements Document

## Introduction

This document specifies the requirements for restructuring the Log Whisperer application from a web-based architecture (FastAPI + React) to a terminal-native Python monorepo. The refactored application will provide a pure terminal user experience using click for CLI, rich/textual for terminal UI, and will remove all web dependencies while preserving the core multi-agent incident remediation functionality.

## Glossary

- **Log_Whisperer**: The terminal-native incident remediation application
- **Decision_Agent**: AI agent that performs root cause analysis on incident logs
- **Writer_Agent**: AI agent that generates CLI remediation commands
- **Pipeline_Orchestrator**: Pure Python orchestrator that coordinates agent execution
- **Terminal_UI**: Rich/Textual-based terminal user interface components
- **CLI_Entry_Point**: Click-based command-line interface for user interaction
- **Safety_Gate**: Argo CD mock and MCP tools for dry-run validation
- **Monorepo**: Single repository containing all application modules with clear separation
- **Demo_Mode**: Configuration mode that uses cached responses for safe demonstrations

## Requirements

### Requirement 1: Monorepo Directory Structure

**User Story:** As a developer, I want a clear monorepo structure, so that I can easily navigate and maintain the codebase.

#### Acceptance Criteria

1. THE Log_Whisperer SHALL organize code into six top-level directories: agents, api, data, safety, viz, and cli
2. THE agents directory SHALL contain decision_agent.py and writer_agent.py modules
3. THE api directory SHALL contain pipeline.py as a pure Python orchestrator
4. THE data directory SHALL contain cloudflare_incident.json and other incident data files
5. THE safety directory SHALL contain argo_mock.py and mcp_tools.py modules
6. THE viz directory SHALL contain terminal_grid.py and terminal_logger.py modules
7. THE cli directory SHALL contain main.py as the click-based entry point
8. THE Log_Whisperer SHALL maintain a shared models.py file at the root level with Pydantic models

### Requirement 2: Shared Data Models

**User Story:** As a developer, I want shared Pydantic models, so that all modules use consistent data structures.

#### Acceptance Criteria

1. THE models.py SHALL define a FaultReport model with root_cause, affected_services, severity, fix_type, confidence, summary, and time_of_failure fields
2. THE models.py SHALL define a RemediationPlan model with plan_id, commands, rollback_commands, estimated_recovery_mins, overall_risk, and dry_run_passed fields
3. THE models.py SHALL define an ExecutionLog model for tracking command execution history
4. THE models.py SHALL define a CLICommand model with tool, args, description, and risk_level fields
5. THE models.py SHALL define a DryRunResult model for safety gate validation results
6. THE models.py SHALL define a PipelineState model for tracking overall pipeline status
7. FOR ALL Pydantic models, serializing to JSON then deserializing SHALL produce an equivalent object

### Requirement 3: Remove Web Dependencies

**User Story:** As a developer, I want to remove all web-based dependencies, so that the application runs purely in the terminal.

#### Acceptance Criteria

1. THE Log_Whisperer SHALL NOT include fastapi in requirements.txt
2. THE Log_Whisperer SHALL NOT include uvicorn in requirements.txt
3. THE Log_Whisperer SHALL NOT include any React or frontend dependencies
4. THE Log_Whisperer SHALL NOT include httpx for web server functionality
5. THE Log_Whisperer SHALL remove the ui directory containing React components
6. WHEN the application starts, THE Log_Whisperer SHALL NOT bind to any HTTP ports

### Requirement 4: Terminal-Native Dependencies

**User Story:** As a developer, I want terminal-native dependencies installed, so that I can build rich terminal interfaces.

#### Acceptance Criteria

1. THE requirements.txt SHALL include anthropic for AI agent functionality
2. THE requirements.txt SHALL include pydantic for data validation
3. THE requirements.txt SHALL include rich for terminal formatting and display
4. THE requirements.txt SHALL include textual for terminal UI components
5. THE requirements.txt SHALL include click for CLI argument parsing
6. THE requirements.txt SHALL include python-dotenv for environment configuration
7. THE requirements.txt SHALL include structlog for structured logging

### Requirement 5: Click-Based CLI Entry Point

**User Story:** As a user, I want a click-based CLI, so that I can interact with the application through terminal commands.

#### Acceptance Criteria

1. THE CLI_Entry_Point SHALL provide a main command group using click
2. WHEN invoked with --help, THE CLI_Entry_Point SHALL display available commands and options
3. THE CLI_Entry_Point SHALL provide a trigger command to start incident remediation
4. THE CLI_Entry_Point SHALL provide a status command to check pipeline state
5. THE CLI_Entry_Point SHALL provide an approve command to approve remediation plans
6. THE CLI_Entry_Point SHALL provide a demo command to run in Demo_Mode
7. WHEN invalid arguments are provided, THE CLI_Entry_Point SHALL display helpful error messages

### Requirement 6: Pure Python Pipeline Orchestrator

**User Story:** As a developer, I want a pure Python orchestrator, so that agent coordination happens without web frameworks.

#### Acceptance Criteria

1. THE Pipeline_Orchestrator SHALL coordinate Decision_Agent and Writer_Agent execution
2. THE Pipeline_Orchestrator SHALL NOT use FastAPI or any web framework
3. THE Pipeline_Orchestrator SHALL accept incident data as Python objects
4. THE Pipeline_Orchestrator SHALL return PipelineState objects
5. WHEN an incident is triggered, THE Pipeline_Orchestrator SHALL invoke Decision_Agent then Writer_Agent in sequence
6. WHEN an error occurs during orchestration, THE Pipeline_Orchestrator SHALL log the error and update PipelineState status to failed
7. THE Pipeline_Orchestrator SHALL pass FaultReport from Decision_Agent to Writer_Agent

### Requirement 7: Terminal Grid Visualization

**User Story:** As a user, I want terminal-based visualization, so that I can see the pipeline status without a web browser.

#### Acceptance Criteria

1. THE Terminal_UI SHALL display pipeline state using rich or textual components
2. THE Terminal_UI SHALL show Decision_Agent analysis results in a formatted panel
3. THE Terminal_UI SHALL show Writer_Agent remediation commands in a table
4. THE Terminal_UI SHALL show dry-run results with color-coded risk levels
5. THE Terminal_UI SHALL update display in real-time as pipeline progresses
6. WHEN displaying commands, THE Terminal_UI SHALL highlight high-risk commands in red
7. THE Terminal_UI SHALL display a timeline of pipeline stages

### Requirement 8: Terminal Logger

**User Story:** As a user, I want structured terminal logging, so that I can track application behavior during execution.

#### Acceptance Criteria

1. THE Terminal_UI SHALL provide a terminal logger using rich.console
2. THE Terminal_UI SHALL log Decision_Agent reasoning steps
3. THE Terminal_UI SHALL log Writer_Agent command generation
4. THE Terminal_UI SHALL log Safety_Gate validation results
5. WHEN Demo_Mode is enabled, THE Terminal_UI SHALL display a demo mode indicator
6. THE Terminal_UI SHALL use different colors for different log levels
7. THE Terminal_UI SHALL format structured log data as readable terminal output

### Requirement 9: Environment Configuration

**User Story:** As a developer, I want environment-based configuration, so that I can control application behavior without code changes.

#### Acceptance Criteria

1. THE Log_Whisperer SHALL provide a .env.example file with all required configuration variables
2. THE .env.example SHALL include ANTHROPIC_API_KEY for AI agent authentication
3. THE .env.example SHALL include DEMO_MODE with default value true
4. THE .env.example SHALL include LOG_LEVEL for controlling log verbosity
5. WHEN DEMO_MODE is true, THE Log_Whisperer SHALL use cached responses instead of calling external APIs
6. WHEN ANTHROPIC_API_KEY is missing and DEMO_MODE is false, THE Log_Whisperer SHALL display an error message and exit
7. THE Log_Whisperer SHALL load configuration from .env file using python-dotenv

### Requirement 10: Decision Agent Integration

**User Story:** As a user, I want the Decision Agent to analyze incidents, so that I can understand root causes.

#### Acceptance Criteria

1. THE Decision_Agent SHALL accept incident log data as input
2. THE Decision_Agent SHALL return a FaultReport object
3. WHEN analyzing logs, THE Decision_Agent SHALL identify root_cause, affected_services, and severity
4. WHEN Demo_Mode is enabled, THE Decision_Agent SHALL return cached FaultReport data
5. WHEN Demo_Mode is disabled, THE Decision_Agent SHALL call Anthropic API for analysis
6. THE Decision_Agent SHALL include confidence scores in FaultReport output
7. IF API call fails, THEN THE Decision_Agent SHALL log the error and return a FaultReport with low confidence

### Requirement 11: Writer Agent Integration

**User Story:** As a user, I want the Writer Agent to generate remediation commands, so that I can fix incidents.

#### Acceptance Criteria

1. THE Writer_Agent SHALL accept a FaultReport as input
2. THE Writer_Agent SHALL return a RemediationPlan object
3. THE Writer_Agent SHALL generate CLICommand objects with tool, args, and risk_level
4. THE Writer_Agent SHALL generate rollback_commands for each remediation command
5. WHEN Demo_Mode is enabled, THE Writer_Agent SHALL return cached RemediationPlan data
6. WHEN Demo_Mode is disabled, THE Writer_Agent SHALL call Anthropic API for command generation
7. IF API call fails, THEN THE Writer_Agent SHALL log the error and return an empty RemediationPlan

### Requirement 12: Safety Gate Validation

**User Story:** As a user, I want dry-run validation, so that I can verify commands are safe before execution.

#### Acceptance Criteria

1. THE Safety_Gate SHALL validate each CLICommand through dry-run simulation
2. THE Safety_Gate SHALL return DryRunResult objects with would_succeed and safe_to_execute flags
3. THE Safety_Gate SHALL calculate risk_score for each command
4. THE Safety_Gate SHALL identify potential side_effects of command execution
5. WHEN argo_mock is used, THE Safety_Gate SHALL simulate Argo CD validation behavior
6. IF a command has risk_score above 0.8, THEN THE Safety_Gate SHALL set safe_to_execute to false
7. THE Safety_Gate SHALL support git_revert, kubectl_apply, kubectl_scale, argo_sync, and service_restart tools

### Requirement 13: Human Approval Workflow

**User Story:** As a user, I want to approve remediation plans, so that I maintain control over system changes.

#### Acceptance Criteria

1. WHEN a RemediationPlan is generated, THE Log_Whisperer SHALL display it and wait for approval
2. THE CLI_Entry_Point SHALL provide an approve command to confirm execution
3. THE CLI_Entry_Point SHALL provide a reject command to cancel execution
4. WHEN a plan is approved, THE Pipeline_Orchestrator SHALL update PipelineState status to executing
5. WHEN a plan is rejected, THE Pipeline_Orchestrator SHALL update PipelineState status to failed
6. THE Terminal_UI SHALL display approval prompt with plan details
7. IF no approval is received within timeout period, THEN THE Log_Whisperer SHALL cancel the plan

### Requirement 14: Incident Data Management

**User Story:** As a developer, I want structured incident data, so that I can test the system with realistic scenarios.

#### Acceptance Criteria

1. THE data directory SHALL contain cloudflare_incident.json with sample incident logs
2. THE Log_Whisperer SHALL parse JSON incident files into LogEvent objects
3. WHEN loading incident data, THE Log_Whisperer SHALL validate JSON structure
4. IF incident data is malformed, THEN THE Log_Whisperer SHALL display a descriptive error message
5. THE Log_Whisperer SHALL support loading multiple incident files
6. THE CLI_Entry_Point SHALL accept a --file argument to specify incident data path
7. FOR ALL valid incident JSON files, parsing then serializing SHALL produce equivalent JSON structure

### Requirement 15: MCP Tools Integration

**User Story:** As a developer, I want MCP tools for command execution, so that I can interact with external systems safely.

#### Acceptance Criteria

1. THE Safety_Gate SHALL use mcp_tools.py for command validation
2. THE mcp_tools.py SHALL provide tool definitions for git_revert, kubectl_apply, kubectl_scale, argo_sync, and service_restart
3. THE mcp_tools.py SHALL validate command arguments against tool schemas
4. WHEN a command has invalid arguments, THE mcp_tools.py SHALL return validation errors
5. THE mcp_tools.py SHALL support dry-run mode for all tools
6. THE mcp_tools.py SHALL log all tool invocations
7. IF a tool execution fails, THEN THE mcp_tools.py SHALL return detailed error information

### Requirement 16: Demo Mode Functionality

**User Story:** As a presenter, I want demo mode, so that I can demonstrate the system without external dependencies.

#### Acceptance Criteria

1. WHEN DEMO_MODE is true, THE Log_Whisperer SHALL use cached agent responses
2. WHEN DEMO_MODE is true, THE Log_Whisperer SHALL simulate command execution without side effects
3. THE Log_Whisperer SHALL display a prominent demo mode indicator in Terminal_UI
4. THE Log_Whisperer SHALL provide realistic timing delays in demo mode to simulate real execution
5. THE Log_Whisperer SHALL load demo data from data/cloudflare_incident.json by default
6. WHEN DEMO_MODE is true, THE Safety_Gate SHALL always return safe_to_execute as true
7. THE CLI_Entry_Point SHALL provide a --demo flag to override DEMO_MODE environment variable

### Requirement 17: Error Handling and Recovery

**User Story:** As a user, I want robust error handling, so that the application fails gracefully.

#### Acceptance Criteria

1. WHEN an agent fails, THE Pipeline_Orchestrator SHALL log the error and update PipelineState
2. WHEN a network error occurs, THE Log_Whisperer SHALL retry the operation up to 3 times
3. IF all retries fail, THEN THE Log_Whisperer SHALL display an error message and exit gracefully
4. THE Log_Whisperer SHALL validate all input data before processing
5. WHEN invalid configuration is detected, THE Log_Whisperer SHALL display helpful error messages
6. THE Log_Whisperer SHALL catch and log all unhandled exceptions
7. IF a critical error occurs during execution, THEN THE Log_Whisperer SHALL attempt to save PipelineState before exiting

### Requirement 18: Logging and Observability

**User Story:** As a developer, I want structured logging, so that I can debug issues and monitor system behavior.

#### Acceptance Criteria

1. THE Log_Whisperer SHALL use structlog for all logging
2. THE Log_Whisperer SHALL log pipeline state transitions
3. THE Log_Whisperer SHALL log agent inputs and outputs
4. THE Log_Whisperer SHALL log command execution attempts
5. WHEN LOG_LEVEL is DEBUG, THE Log_Whisperer SHALL log detailed agent reasoning
6. THE Log_Whisperer SHALL include timestamps in all log entries
7. THE Log_Whisperer SHALL write logs to both terminal and log file

### Requirement 19: Configuration Parser

**User Story:** As a developer, I want a configuration parser, so that environment variables are properly loaded and validated.

#### Acceptance Criteria

1. THE Log_Whisperer SHALL parse configuration from .env file using python-dotenv
2. THE Log_Whisperer SHALL validate required configuration variables on startup
3. WHEN a required variable is missing, THE Log_Whisperer SHALL display an error listing missing variables
4. THE Log_Whisperer SHALL provide default values for optional configuration variables
5. THE Log_Whisperer SHALL support boolean, string, and integer configuration types
6. THE Log_Whisperer SHALL expose configuration through a config module
7. FOR ALL configuration values, parsing then serializing SHALL preserve the original value

### Requirement 20: Pipeline State Persistence

**User Story:** As a user, I want pipeline state saved, so that I can review execution history.

#### Acceptance Criteria

1. THE Pipeline_Orchestrator SHALL save PipelineState to disk after each stage
2. THE Log_Whisperer SHALL store pipeline states in a .pipeline_history directory
3. THE CLI_Entry_Point SHALL provide a history command to list past pipeline executions
4. THE CLI_Entry_Point SHALL provide a show command to display details of a specific pipeline execution
5. WHEN saving state, THE Pipeline_Orchestrator SHALL serialize PipelineState to JSON
6. WHEN loading state, THE Pipeline_Orchestrator SHALL deserialize JSON to PipelineState objects
7. FOR ALL valid PipelineState objects, saving then loading SHALL produce an equivalent object
