"""
Shared Pydantic models — ALL three engineers import from here.
Never redefine these in individual modules.
"""
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class LogEvent(BaseModel):
    timestamp: str
    service: str
    level: Literal["DEBUG", "INFO", "WARN", "ERROR", "CRIT"]
    msg: str
    correlated_event: str | None = None


class CouncilDebate(BaseModel):
    """Output from a single agent in the council debate."""
    agent_name: str
    hypothesis: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class FaultReport(BaseModel):
    """Output of the Decision Agent."""
    root_cause: str
    affected_services: list[str]
    severity: Literal["P1", "P2", "P3"]
    fix_type: Literal["config_rollback", "service_restart", "route_fix", "cert_renewal", "scale_up"]
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    time_of_failure: str
    debate_summary: list[CouncilDebate] = []


class CLICommand(BaseModel):
    tool: Literal["git_revert", "kubectl_apply", "kubectl_scale", "argo_sync", "service_restart"]
    args: dict[str, str]
    description: str
    risk_level: Literal["low", "medium", "high"]


class RemediationPlan(BaseModel):
    """Output of the Writer Agent."""
    plan_id: str
    commands: list[CLICommand]
    rollback_commands: list[CLICommand]
    estimated_recovery_mins: int
    overall_risk: Literal["low", "medium", "high"]
    dry_run_passed: bool = False


class DryRunResult(BaseModel):
    """Output of the Argo CD safety gate."""
    command: CLICommand
    would_succeed: bool
    side_effects: list[str]
    risk_score: float = Field(ge=0.0, le=1.0)
    safe_to_execute: bool


class PipelineState(BaseModel):
    """Tracks state across the full pipeline."""
    incident_id: str
    status: Literal["idle", "investigating", "planning", "dry_running", "awaiting_approval", "executing", "resolved", "failed"]
    fault_report: FaultReport | None = None
    remediation_plan: RemediationPlan | None = None
    dry_run_results: list[DryRunResult] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: datetime | None = None


class ExecutionLog(BaseModel):
    """Tracks command execution history."""
    command: CLICommand
    executed_at: datetime
    success: bool
    output: str
    error: str | None = None


class PipelineHistory(BaseModel):
    """Historical record of pipeline execution."""
    incident_id: str
    state: PipelineState
    execution_logs: list[ExecutionLog] = []
    saved_at: datetime = Field(default_factory=datetime.utcnow)
