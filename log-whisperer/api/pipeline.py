"""
Main pipeline orchestration.
Coordinates Council Agent → Writer Agent → Safety Gate → Execution.
Integrates with terminal grid for real-time visualization.
"""
from models import PipelineState, FaultReport, RemediationPlan, ExecutionLog
from agents.council_agent import analyze_incident  # Changed from decision_agent
from agents.writer_agent import generate_remediation_plan
from safety.argo_mock import dry_run_command
from datetime import datetime
import structlog

# Import pretty event logging
from viz.terminal_logger import (
    log_ingesting,
    log_diagnosis,
    log_remediation,
    log_safety_check,
    log_approval,
    log_executing,
    log_resolved,
    log_error
)

logger = structlog.get_logger()

# Optional grid integration
try:
    from viz.grid_updater import (
        initialize_grid,
        mark_services_failed,
        mark_services_executing,
        mark_services_recovered,
        mark_services_healthy
    )
    GRID_ENABLED = True
except ImportError:
    GRID_ENABLED = False


class Pipeline:
    def __init__(self, incident_id: str, enable_grid: bool = True, enable_pretty_logs: bool = True):
        self.state = PipelineState(
            incident_id=incident_id,
            status="idle"
        )
        self.enable_grid = enable_grid and GRID_ENABLED
        self.enable_pretty_logs = enable_pretty_logs
        
        if self.enable_grid:
            initialize_grid()
    
    async def run(self, log_events: list[dict]) -> PipelineState:
        """Execute the full pipeline."""
        try:
            # Step 1: Ingest logs
            if self.enable_pretty_logs:
                log_ingesting("Reading Cloudflare BGP incident logs...")
            
            # Step 2: Council Agent analyzes logs (multi-agent debate)
            logger.info("council_agent.start", incident_id=self.state.incident_id)
            self.state.status = "investigating"
            self.state.fault_report = await analyze_incident(log_events)
            
            if self.enable_pretty_logs:
                log_diagnosis(self.state.fault_report.root_cause)
            
            # Update grid: mark affected services as failed
            if self.enable_grid and self.state.fault_report:
                mark_services_failed(self.state.fault_report.affected_services)
            
            # Step 3: Writer Agent generates remediation plan
            logger.info("writer_agent.start", incident_id=self.state.incident_id)
            self.state.status = "planning"
            self.state.remediation_plan = await generate_remediation_plan(
                self.state.fault_report
            )
            
            if self.enable_pretty_logs:
                log_remediation(
                    command_count=len(self.state.remediation_plan.commands),
                    risk=self.state.remediation_plan.overall_risk
                )
            
            # Step 4: Dry-run through safety gate
            logger.info("safety_gate.start", incident_id=self.state.incident_id)
            self.state.status = "dry_running"
            for cmd in self.state.remediation_plan.commands:
                result = dry_run_command(cmd)
                self.state.dry_run_results.append(result)
            
            # Check if all dry-runs passed
            all_safe = all(r.safe_to_execute for r in self.state.dry_run_results)
            if self.enable_pretty_logs:
                log_safety_check(status="SAFE" if all_safe else "REVIEW REQUIRED")
            
            # Step 5: Await human approval
            self.state.status = "awaiting_approval"
            logger.info("pipeline.awaiting_approval", incident_id=self.state.incident_id)
            
            if self.enable_pretty_logs:
                log_approval("Awaiting human approval - Press ENTER")
            
            return self.state
            
        except Exception as e:
            logger.error("pipeline.failed", incident_id=self.state.incident_id, error=str(e))
            if self.enable_pretty_logs:
                log_error(f"Pipeline failed: {str(e)}")
            self.state.status = "failed"
            raise
    
    def execute_approved_plan(self, execution_mode: str = None) -> list[ExecutionLog]:
        """
        Execute commands after human approval.
        
        Args:
            execution_mode: "dry_run", "safe", or "full". If None, uses EXECUTION_MODE env var.
        
        Returns:
            List of ExecutionLog entries
        """
        if self.state.status != "awaiting_approval":
            raise ValueError("Pipeline not ready for execution")
        
        self.state.status = "executing"
        
        if self.enable_pretty_logs:
            log_executing("Applying remediation commands...")
        
        # Import executor
        from execution.executor import get_executor
        executor = get_executor(execution_mode)
        
        execution_logs = []
        
        # Update grid: mark services as executing
        if self.enable_grid and self.state.fault_report:
            mark_services_executing(self.state.fault_report.affected_services)
        
        # Execute each command with real executor
        for cmd in self.state.remediation_plan.commands:
            result = executor.execute(cmd)
            
            log = ExecutionLog(
                command=cmd,
                executed_at=datetime.utcnow(),
                success=result["success"],
                output=result["output"] or "",
                error=result.get("error")
            )
            execution_logs.append(log)
            
            logger.info("command.executed", 
                       tool=cmd.tool, 
                       description=cmd.description,
                       success=result["success"],
                       mode=result["mode"])
            
            # Stop on failure
            if not result["success"]:
                logger.error("command.failed", 
                           tool=cmd.tool,
                           error=result.get("error"))
                self.state.status = "failed"
                return execution_logs
        
        self.state.status = "resolved"
        self.state.resolved_at = datetime.utcnow()
        
        # Update grid: mark services as recovered
        if self.enable_grid and self.state.fault_report:
            mark_services_recovered(self.state.fault_report.affected_services)
        
        # Calculate MTTR (mock for demo)
        if self.enable_pretty_logs:
            log_resolved(mttr="04:12", baseline="57:00", reduction="93%")
        
        return execution_logs
