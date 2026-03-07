"""
Pretty event logging for terminal output.
Uses Rich panels for visually appealing event notifications.
"""
from rich.console import Console
from rich.panel import Panel

console = Console()


def log_event(icon: str, title: str, message: str, color: str = "white"):
    """
    Log a pretty event with icon, title, and message in a Rich panel.
    
    Args:
        icon: Emoji icon for the event
        title: Event title (e.g., "INGESTING", "DIAGNOSIS")
        message: Event message/details
        color: Border and title color (default: "white")
    
    Example:
        log_event("📥", "INGESTING", "Reading logs...", "cyan")
    """
    panel = Panel.fit(
        f"{icon} {message}",
        title=f"[{color}]{title}[/]",
        border_style=color
    )
    console.print(panel)


# Event template functions for common pipeline events

def log_ingesting(message: str = "Reading Cloudflare BGP incident logs..."):
    """Log data ingestion event."""
    log_event("📥", "INGESTING", message, "cyan")


def log_diagnosis(root_cause: str):
    """Log diagnosis/fault report event."""
    log_event("🔍", "DIAGNOSIS", f"Root cause: {root_cause}", "green")


def log_remediation(command_count: int, risk: str):
    """Log remediation plan event."""
    log_event("⚙️", "REMEDIATION", f"{command_count} commands staged | Risk: {risk}", "yellow")


def log_safety_check(status: str = "SAFE"):
    """Log safety check event."""
    log_event("🛡️", "SAFETY CHECK", f"Dry-run passed | Status: {status}", "blue")


def log_approval(message: str = "Awaiting human approval - Press ENTER"):
    """Log approval request event."""
    log_event("⏸", "APPROVAL", message, "yellow")


def log_executing(message: str = "Applying remediation commands..."):
    """Log execution event."""
    log_event("✅", "EXECUTING", message, "yellow")


def log_resolved(mttr: str, baseline: str, reduction: str):
    """Log resolution event with metrics."""
    log_event("🎉", "RESOLVED", f"MTTR: {mttr} | Baseline: {baseline} | Reduction: {reduction}", "green")


def log_error(message: str):
    """Log error event."""
    log_event("❌", "ERROR", message, "red")


def log_warning(message: str):
    """Log warning event."""
    log_event("⚠️", "WARNING", message, "yellow")


def log_info(title: str, message: str):
    """Log general info event."""
    log_event("ℹ️", title, message, "blue")
