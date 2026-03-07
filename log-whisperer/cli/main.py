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
def trigger(incident_id: str):
    """Trigger incident analysis pipeline."""
    log_event("cli.trigger", incident_id=incident_id)
    
    # Load incident data
    log_events = load_cloudflare_incident()
    
    # Run pipeline
    pipeline = Pipeline(incident_id)
    state = asyncio.run(pipeline.run(log_events))
    
    # Display results
    grid = TerminalGrid()
    grid.display(state, duration=10)
    
    click.echo(f"\n✅ Pipeline complete. Status: {state.status}")
    click.echo(f"Awaiting approval for {len(state.remediation_plan.commands)} commands.")


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
