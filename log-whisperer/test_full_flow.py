#!/usr/bin/env python3
"""Test the full pipeline flow"""
import asyncio
import sys

async def test_pipeline():
    """Test the complete pipeline with all agents"""
    print("🧪 Testing Log Whisperer Full Pipeline\n")
    
    # Import all components
    from pipeline import run_pipeline_with_logs, set_emit
    import json
    
    events_captured = []
    
    async def capture_emit(event):
        """Capture emitted events"""
        events_captured.append(event)
        event_type = event.get('type', 'unknown')
        
        # Print key events
        if event_type == 'diagnosis':
            print(f"✓ DECISION: {event.get('message', '')[:80]}")
        elif event_type == 'orchestrator_spawning':
            print(f"✓ ORCHESTRATOR: Spawning specialists...")
        elif event_type == 'specialist_spawned':
            print(f"  → {event.get('agent_name', '')}: {event.get('result', {}).get('analysis', '')[:60]}")
        elif event_type == 'memory_recall':
            print(f"✓ MEMORY: Recalled similar incidents")
        elif event_type == 'prediction':
            print(f"✓ PREDICTOR: Predicted cascading failures")
        elif event_type == 'fix_proposed':
            print(f"✓ WRITER: Proposed remediation")
        elif event_type == 'critique':
            print(f"✓ CRITIC: Identified {len(event.get('concerns', []))} safety concerns")
        elif event_type == 'consensus':
            print(f"✓ CONSENSUS: {event.get('message', '')[:80]}")
    
    set_emit(capture_emit)
    
    # Load incident data
    with open('data/cloudflare_incident.json', 'r') as f:
        logs = f.read()
    
    # Run pipeline
    print("🚀 Starting pipeline...\n")
    await run_pipeline_with_logs(logs)
    
    print(f"\n✅ Pipeline complete! Captured {len(events_captured)} events")
    
    # Verify key agents ran
    event_types = [e.get('type') for e in events_captured]
    
    required_events = [
        'diagnosis',
        'orchestrator_spawning',
        'specialist_spawned',
        'memory_recall',
        'prediction',
        'fix_proposed',
        'critique',
        'consensus'
    ]
    
    print("\n📊 Agent Verification:")
    for req in required_events:
        if req in event_types:
            print(f"  ✓ {req}")
        else:
            print(f"  ✗ {req} - MISSING!")
    
    # Check for specialists
    specialists = [e for e in events_captured if e.get('type') == 'specialist_spawned']
    print(f"\n🤖 Spawned {len(specialists)} specialist agents")
    
    return len([e for e in required_events if e in event_types]) == len(required_events)

if __name__ == "__main__":
    success = asyncio.run(test_pipeline())
    sys.exit(0 if success else 1)
