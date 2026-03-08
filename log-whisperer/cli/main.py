"""
CLI entry point for Log Whisperer.
Provides commands to trigger incidents, view status, and approve plans.
"""
import click
import asyncio
from api.pipeline import Pipeline
from data.load_incident import load_cloudflare_incident
from viz.terminal_grid import TerminalGrid
from viz.terminal_logger import setup_logging, log_event
import structlog


@click.group()
def cli():
    """Log Whisperer CLI - Multi-agent incident remediation."""
    setup_logging()


@cli.command()
@click.option('--incident-id', default='demo-001', help='Incident identifier')
@click.option('--mode', default='demo', help='Execution mode: demo, dry_run, safe, full')
def trigger(incident_id: str, mode: str):
    """Trigger incident analysis pipeline."""
    log_event("cli.trigger", incident_id=incident_id, mode=mode)
    
    # Load incident data
    log_events = load_cloudflare_incident()
    
    # Run pipeline
    pipeline = Pipeline(incident_id)
    state = asyncio.run(pipeline.run(log_events))
    
    click.echo(f"\n✅ Analysis complete. Status: {state.status}")
    click.echo(f"Found {len(state.remediation_plan.commands)} remediation commands.")
    
    # In demo mode, auto-execute
    if mode == 'demo':
        click.echo("\n🎬 DEMO MODE: Auto-executing remediation plan...")
        execution_logs = pipeline.execute_approved_plan(execution_mode='dry_run')
        click.echo(f"\n✅ Remediation complete. Executed {len(execution_logs)} commands.")
        click.echo(f"Final status: {state.status}")
    else:
        click.echo(f"\nAwaiting approval for {len(state.remediation_plan.commands)} commands.")
        click.echo(f"Run: log-whisperer approve {incident_id}")


@cli.command()
@click.argument('incident_id')
def approve(incident_id: str):
    """Approve and execute remediation plan."""
    log_event("cli.approve", incident_id=incident_id)
    click.echo(f"⚠️  Executing remediation for {incident_id}...")
    # TODO: Load pipeline state and execute
    click.echo("✅ Remediation complete.")


@cli.command()
@click.argument('incident_id')
def status(incident_id: str):
    """Check pipeline status."""
    log_event("cli.status", incident_id=incident_id)
    # TODO: Load and display pipeline state
    click.echo(f"Status for {incident_id}: awaiting_approval")


if __name__ == '__main__':
    cli()
