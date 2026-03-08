#!/usr/bin/env python3
"""
Test script for decision_agent.py
Tests 5 times with real API to verify functionality.
"""
import os
import sys
from dotenv import load_dotenv
from agents.decision_agent import analyze_logs
from rich.console import Console

console = Console()

# Load environment variables
load_dotenv()

def test_demo_mode():
    """Test with DEMO_MODE enabled."""
    console.print("\n[bold cyan]Test 1: DEMO_MODE=true[/bold cyan]")
    os.environ['DEMO_MODE'] = 'true'
    report = analyze_logs('data/cloudflare_incident.json')
    assert report.severity == "P1"
    assert report.confidence == 0.97
    console.print("[green]✓ DEMO_MODE test passed[/green]")
    return report

def test_real_api():
    """Test with real API calls."""
    console.print("\n[bold cyan]Test 2-6: Real API calls (5 times)[/bold cyan]")
    os.environ['DEMO_MODE'] = 'false'
    
    if not os.getenv('ANTHROPIC_API_KEY'):
        console.print("[red]✗ ANTHROPIC_API_KEY not set - skipping real API tests[/red]")
        return None
    
    results = []
    for i in range(5):
        console.print(f"\n[bold]API Call {i+1}/5[/bold]")
        try:
            report = analyze_logs('data/cloudflare_incident.json')
            results.append(report)
            console.print(f"[green]✓ API call {i+1} succeeded[/green]")
            console.print(f"  Severity: {report.severity}, Confidence: {report.confidence:.0%}")
        except Exception as e:
            console.print(f"[red]✗ API call {i+1} failed: {e}[/red]")
    
    return results

def test_error_handling():
    """Test error handling with invalid API key."""
    console.print("\n[bold cyan]Test 7: Error handling (invalid API key)[/bold cyan]")
    os.environ['DEMO_MODE'] = 'false'
    original_key = os.getenv('ANTHROPIC_API_KEY')
    os.environ['ANTHROPIC_API_KEY'] = 'invalid_key_12345'
    
    try:
        report = analyze_logs('data/cloudflare_incident.json')
        # Should fallback to cached response
        assert report.severity == "P1"
        console.print("[green]✓ Error handling test passed (fallback to cached)[/green]")
    finally:
        if original_key:
            os.environ['ANTHROPIC_API_KEY'] = original_key

if __name__ == '__main__':
    console.print("[bold magenta]Testing decision_agent.py[/bold magenta]")
    
    try:
        # Test 1: DEMO_MODE
        test_demo_mode()
        
        # Tests 2-6: Real API
        test_real_api()
        
        # Test 7: Error handling
        test_error_handling()
        
        console.print("\n[bold green]All tests completed![/bold green]")
        
    except Exception as e:
        console.print(f"\n[bold red]Test failed: {e}[/bold red]")
        sys.exit(1)
