"""
Command Executor - Real execution of remediation commands.
Supports dry-run, safe mode, and full execution with proper error handling.
"""
import subprocess
import os
from typing import Dict, Any, Tuple
from enum import Enum
from models import CLICommand
import structlog

logger = structlog.get_logger()


class ExecutionMode(Enum):
    """Execution modes for safety."""
    DRY_RUN = "dry_run"      # Show what would happen, don't execute
    SAFE = "safe"            # Execute safe commands only (read-only, low-risk)
    FULL = "full"            # Execute all commands (requires explicit approval)


class CommandExecutor:
    """Executes CLI commands with safety checks and logging."""
    
    def __init__(self, mode: ExecutionMode = ExecutionMode.DRY_RUN, working_dir: str = None):
        self.mode = mode
        self.working_dir = working_dir or os.getcwd()
        self.safe_commands = {"git_revert", "kubectl_apply"}  # Commands safe to run
        
    def is_safe_command(self, command: CLICommand) -> bool:
        """Check if command is safe to execute."""
        return command.tool in self.safe_commands and command.risk_level in ["low", "medium"]
    
    def build_command(self, cmd: CLICommand) -> list[str]:
        """Build actual command list from CLICommand."""
        if cmd.tool == "git_revert":
            commit = cmd.args.get("commit", "")
            return ["git", "revert", commit, "--no-commit"]
        
        elif cmd.tool == "kubectl_apply":
            file_path = cmd.args.get("file", "")
            namespace = cmd.args.get("namespace", "default")
            return ["kubectl", "apply", "-f", file_path, "-n", namespace]
        
        elif cmd.tool == "kubectl_scale":
            resource = cmd.args.get("resource", "")
            replicas = cmd.args.get("replicas", "3")
            namespace = cmd.args.get("namespace", "default")
            return ["kubectl", "scale", resource, f"--replicas={replicas}", "-n", namespace]
        
        elif cmd.tool == "argo_sync":
            app = cmd.args.get("app", "")
            prune = cmd.args.get("prune", "false")
            cmd_list = ["argocd", "app", "sync", app]
            if prune == "true":
                cmd_list.append("--prune")
            return cmd_list
        
        elif cmd.tool == "service_restart":
            service = cmd.args.get("service", "")
            namespace = cmd.args.get("namespace", "default")
            return ["kubectl", "rollout", "restart", f"deployment/{service}", "-n", namespace]
        
        else:
            raise ValueError(f"Unknown tool: {cmd.tool}")
    
    def execute(self, command: CLICommand) -> Dict[str, Any]:
        """
        Execute a command based on the current mode.
        
        Returns:
            Dict with execution results including success, output, error
        """
        cmd_list = self.build_command(command)
        cmd_str = " ".join(cmd_list)
        
        logger.info("executor.execute", 
                   tool=command.tool, 
                   mode=self.mode.value,
                   command=cmd_str)
        
        # DRY_RUN mode - don't execute
        if self.mode == ExecutionMode.DRY_RUN:
            return {
                "success": True,
                "mode": "dry_run",
                "command": cmd_str,
                "output": f"[DRY RUN] Would execute: {cmd_str}",
                "error": None,
                "executed": False
            }
        
        # SAFE mode - only execute safe commands
        if self.mode == ExecutionMode.SAFE:
            if not self.is_safe_command(command):
                return {
                    "success": False,
                    "mode": "safe",
                    "command": cmd_str,
                    "output": None,
                    "error": f"Command {command.tool} not in safe list",
                    "executed": False
                }
        
        # Execute the command
        try:
            result = subprocess.run(
                cmd_list,
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            success = result.returncode == 0
            
            logger.info("executor.result",
                       tool=command.tool,
                       success=success,
                       returncode=result.returncode)
            
            return {
                "success": success,
                "mode": self.mode.value,
                "command": cmd_str,
                "output": result.stdout,
                "error": result.stderr if not success else None,
                "returncode": result.returncode,
                "executed": True
            }
            
        except subprocess.TimeoutExpired:
            logger.error("executor.timeout", tool=command.tool, command=cmd_str)
            return {
                "success": False,
                "mode": self.mode.value,
                "command": cmd_str,
                "output": None,
                "error": "Command timed out after 30 seconds",
                "executed": False
            }
        
        except FileNotFoundError:
            logger.error("executor.not_found", tool=command.tool, command=cmd_str)
            return {
                "success": False,
                "mode": self.mode.value,
                "command": cmd_str,
                "output": None,
                "error": f"Command not found: {cmd_list[0]}",
                "executed": False
            }
        
        except Exception as e:
            logger.error("executor.error", tool=command.tool, error=str(e))
            return {
                "success": False,
                "mode": self.mode.value,
                "command": cmd_str,
                "output": None,
                "error": str(e),
                "executed": False
            }
    
    def execute_plan(self, commands: list[CLICommand]) -> list[Dict[str, Any]]:
        """
        Execute a list of commands.
        
        Returns:
            List of execution results
        """
        results = []
        
        for cmd in commands:
            result = self.execute(cmd)
            results.append(result)
            
            # Stop on first failure in FULL mode
            if self.mode == ExecutionMode.FULL and not result["success"]:
                logger.warning("executor.stopped", 
                             reason="Command failed",
                             failed_command=result["command"])
                break
        
        return results


def get_executor(mode: str = None) -> CommandExecutor:
    """
    Factory function to get executor based on environment or parameter.
    
    Args:
        mode: "dry_run", "safe", or "full". If None, reads from EXECUTION_MODE env var.
        
    Returns:
        CommandExecutor instance
    """
    if mode is None:
        mode = os.getenv("EXECUTION_MODE", "dry_run")
    
    mode_map = {
        "dry_run": ExecutionMode.DRY_RUN,
        "safe": ExecutionMode.SAFE,
        "full": ExecutionMode.FULL
    }
    
    execution_mode = mode_map.get(mode.lower(), ExecutionMode.DRY_RUN)
    
    return CommandExecutor(mode=execution_mode)
