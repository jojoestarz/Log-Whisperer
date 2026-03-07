#!/usr/bin/env python3
"""Test the 3 winning innovations"""
import asyncio
import sys

def test_cost_calculator():
    """Test Innovation #1: Live Cost Ticker"""
    print("\n🧪 Testing Cost Calculator...")
    from viz.cost_calculator import CostCalculator
    
    calc = CostCalculator()
    calc.start_incident()
    
    # Simulate 4 minutes
    import time
    time.sleep(0.1)  # Small delay
    calc.resolve_incident()
    
    current = calc.get_current_cost()
    comparison = calc.compare_mttr(57.0, 4.2)
    
    assert current["total_cost"] > 0, "Cost should be calculated"
    assert comparison["savings"] > 0, "Should show savings"
    assert comparison["reduction_percent"] > 90, "Should show >90% reduction"
    
    print(f"   ✅ Cost calculation works")
    print(f"   💰 Savings: ${comparison['savings']:,}")
    print(f"   📉 Reduction: {comparison['reduction_percent']}%")

def test_confidence_tracker():
    """Test Innovation #2: Confidence Progression"""
    print("\n🧪 Testing Confidence Tracker...")
    from viz.confidence_tracker import ConfidenceTracker
    
    tracker = ConfidenceTracker()
    tracker.simulate_analysis_journey(final_confidence=0.97)
    
    chart_data = tracker.get_chart_data()
    
    assert len(chart_data["points"]) > 0, "Should have confidence points"
    assert chart_data["final_confidence"] == 0.97, "Final confidence should match"
    assert chart_data["points"][0]["confidence"] < 0.5, "Should start uncertain"
    assert chart_data["points"][-1]["confidence"] > 0.9, "Should end confident"
    
    print(f"   ✅ Confidence tracking works")
    print(f"   📊 Points tracked: {len(chart_data['points'])}")
    print(f"   🎯 Final confidence: {chart_data['final_confidence']*100:.0f}%")
    print(f"   📈 Progression: {chart_data['points'][0]['confidence']*100:.0f}% → {chart_data['points'][-1]['confidence']*100:.0f}%")

async def test_incident_simulator():
    """Test Innovation #3: Live Incident Simulation"""
    print("\n🧪 Testing Incident Simulator...")
    from simulator.incident_simulator import IncidentSimulator
    
    sim = IncidentSimulator()
    
    # Inject failure
    snapshot = await sim.inject_bgp_failure()
    
    assert snapshot["active"] == True, "Incident should be active"
    assert len(snapshot["services"]) > 0, "Should have services"
    assert any(s["status"] in ["critical", "down"] for s in snapshot["services"].values()), "Some services should be down"
    
    print(f"   ✅ Incident simulation works")
    print(f"   🔥 Services affected: {len([s for s in snapshot['services'].values() if s['status'] != 'healthy'])}")
    print(f"   📝 Logs generated: {len(sim.logs)}")
    
    # Test healing
    commands = [
        "argocd app rollback byoip-cleanup",
        "kubectl scale deployment bgp-config-deployer --replicas=0",
        "systemctl restart bgp-router"
    ]
    result = await sim.heal(commands)
    
    assert result["status"] == "resolved", "Should be resolved"
    assert result["mttr_seconds"] > 0, "Should have MTTR"
    
    print(f"   ✅ Healing works")
    print(f"   ⏱️  MTTR: {result['mttr_seconds']}s")

def test_integration():
    """Test that all components integrate properly"""
    print("\n🧪 Testing Integration...")
    
    # Test imports
    try:
        from viz.cost_calculator import get_calculator, reset_calculator
        from viz.confidence_tracker import get_tracker, reset_tracker
        from simulator.incident_simulator import get_simulator
        print("   ✅ All modules import successfully")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test server integration
    try:
        import server
        print("   ✅ Server imports innovations")
    except Exception as e:
        print(f"   ❌ Server integration failed: {e}")
        return False
    
    # Test pipeline integration
    try:
        import pipeline
        print("   ✅ Pipeline imports confidence tracker")
    except Exception as e:
        print(f"   ❌ Pipeline integration failed: {e}")
        return False
    
    return True

async def main():
    print("=" * 60)
    print("🏆 LOG WHISPERER: TESTING WINNING INNOVATIONS")
    print("=" * 60)
    
    try:
        # Test each innovation
        test_cost_calculator()
        test_confidence_tracker()
        await test_incident_simulator()
        
        # Test integration
        if not test_integration():
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - READY TO WIN!")
        print("=" * 60)
        print("\n🚀 Next steps:")
        print("   1. Run: ./start.sh")
        print("   2. Open: http://localhost:5173")
        print("   3. Click: 🔥 LIVE SIMULATION")
        print("   4. Watch the magic happen")
        print("\n💡 See WINNING_DEMO.md for the full demo script")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
