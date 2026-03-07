"""Shared data models for Log Whisperer"""
from dataclasses import dataclass, field


@dataclass
class FaultReport:
    """Output from Decision Agent"""
    root_cause: str = ""
    blast_radius: str = ""
    confidence: float = 0.0
    affected_services: list = field(default_factory=list)
    timestamp: str = ""


@dataclass
class RemediationPlan:
    """Output from Writer Agent"""
    commands: list = field(default_factory=list)
    safety_level: str = "sandboxed"
    risk_score: float = 0.0
    requires_approval: bool = True
    dry_run_passed: bool = False
