#!/usr/bin/env python3
"""
Test script for new hackathon features
Run this to verify all enhancements are working
"""

import sys
import os

def test_imports():
    """Test that all new modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from agents.critic_agent import critique
        print("  ✅ critic_agent.py imports successfully")
    except Exception as e:
        print(f"  ❌ critic_agent.py import failed: {e}")
        return False
    
    try:
        from simulator.incident_simulator import get_simulator
        print("  ✅ incident_simulator.py imports successfully")
    except Exception as e:
        print(f"  ❌ incident_simulator.py import failed: {e}")
        return False
    
    try:
        from viz.cost_calculator import get_calculator
        print("  ✅ cost_calculator.py imports successfully")
    except Exception as e:
        print(f"  ❌ cost_calculator.py import failed: {e}")
        return False
    
    try:
        from viz.confidence_tracker import get_tracker
        print("  ✅ confidence_tracker.py imports successfully")
    except Exception as e:
        print(f"  ❌ confidence_tracker.py import failed: {e}")
        return False
    
    return True


def test_critic_agent():
    """Test critic agent functionality"""
    print("\n🧪 Testing Critic Agent...")
    
    try:
        from agents.critic_agent import critique, CACHED_CRITIQUE
        from models import RemediationPlan, FaultReport
        import asyncio
        
        # Create test data
        fault = FaultReport(
            root_cause="BGP withdrawal",
            blast_radius="4 services",
            confidence=0.97,
            affected_services=["api", "bgp", "cdn", "dns"]
        )
        
        plan = RemediationPlan(
            commands=["argocd app rollback byoip-cleanup"],
            safety_level="sandboxed",
            risk_score=0.08,
            requires_approval=True,
            dry_run_passed=False
        )
        
        # Test critique
        result = asyncio.run(critique(plan, fault))
        
        assert "concerns" in result, "Missing 'concerns' in critique result"
        assert "alternative_plan" in result, "Missing 'alternative_plan' in critique result"
        assert "confidence" in result, "Missing 'confidence' in critique result"
        assert "recommendation" in result, "Missing 'recommendation' in critique result"
        
        print(f"  ✅ Critic agent returns valid critique")
        print(f"     Concerns: {len(result['concerns'])} identified")
        print(f"     Alternative commands: {len(result['alternative_plan'])}")
        print(f"     Recommendation: {result['recommendation']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Critic agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simulator():
    """Test incident simulator"""
    print("\n🧪 Testing Incident Simulator...")
    
    try:
        from simulator.incident_simulator import get_simulator
        import asyncio
        
        sim = get_simulator()
        
        # Test BGP failure injection
        snapshot = asyncio.run(sim.inject_bgp_failure())
        
        assert "services" in snapshot, "Missing 'services' in snapshot"
        assert "active" in snapshot, "Missing 'active' in snapshot"
        
        # Check services are degraded
        services = snapshot["services"]
        assert any(s["status"] in ["critical", "down"] for s in services.values()), \
            "No services in critical/down state after injection"
        
        print(f"  ✅ Simulator injects failures correctly")
        print(f"     Services affected: {sum(1 for s in services.values() if s['status'] in ['critical', 'down'])}")
        
        # Test healing
        heal_result = asyncio.run(sim.heal([
            "argocd app rollback byoip-cleanup --staging"
        ]))
        
        assert "status" in heal_result, "Missing 'status' in heal result"
        print(f"  ✅ Simulator heals services correctly")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Simulator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cost_calculator():
    """Test cost calculator"""
    print("\n🧪 Testing Cost Calculator...")
    
    try:
        from viz.cost_calculator import get_calculator, reset_calculator
        import time
        
        calc = reset_calculator()
        
        # Start incident
        calc.start_incident()
        time.sleep(0.2)  # Wait a bit for time to pass
        
        # Get current cost
        cost = calc.get_current_cost()
        
        assert cost["total_cost"] > 0, "Cost should be > 0 after incident start"
        assert cost["duration_seconds"] >= 0, "Duration should be >= 0"
        
        print(f"  ✅ Cost calculator tracks costs correctly")
        print(f"     Current cost: ${cost['total_cost']:,}")
        print(f"     Cost per second: ${cost['cost_per_second']}")
        
        # Test comparison
        comparison = calc.compare_mttr(57.0, 4.2)
        
        assert comparison["savings"] > 0, "Savings should be positive"
        assert comparison["reduction_percent"] > 90, "Reduction should be > 90%"
        
        print(f"  ✅ Cost comparison works correctly")
        print(f"     Savings: ${comparison['savings']:,}")
        print(f"     Reduction: {comparison['reduction_percent']}%")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Cost calculator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_confidence_tracker():
    """Test confidence tracker"""
    print("\n🧪 Testing Confidence Tracker...")
    
    try:
        from viz.confidence_tracker import get_tracker, reset_tracker
        
        tracker = reset_tracker()
        
        # Simulate analysis journey
        tracker.simulate_analysis_journey()
        
        assert len(tracker.points) > 0, "Should have confidence points"
        assert tracker.points[0].confidence < tracker.points[-1].confidence, \
            "Confidence should increase over time"
        
        print(f"  ✅ Confidence tracker works correctly")
        print(f"     Points tracked: {len(tracker.points)}")
        print(f"     Initial confidence: {tracker.points[0].confidence:.0%}")
        print(f"     Final confidence: {tracker.points[-1].confidence:.0%}")
        
        # Test chart data export
        chart_data = tracker.get_chart_data()
        
        assert "points" in chart_data, "Missing 'points' in chart data"
        assert "final_confidence" in chart_data, "Missing 'final_confidence'"
        
        print(f"  ✅ Chart data export works correctly")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Confidence tracker test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pipeline_integration():
    """Test that pipeline integrates all components"""
    print("\n🧪 Testing Pipeline Integration...")
    
    try:
        import pipeline
        
        # Check that critic is imported
        with open("pipeline.py", "r") as f:
            content = f.read()
            
        assert "from agents.critic_agent import critique" in content, \
            "Pipeline should import critic_agent"
        
        assert "critique_result = await critique" in content, \
            "Pipeline should call critique function"
        
        assert "debate_complete" in content, \
            "Pipeline should emit debate_complete event"
        
        print(f"  ✅ Pipeline integrates critic agent")
        print(f"  ✅ Pipeline emits debate events")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Pipeline integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ui_components():
    """Test that UI components exist"""
    print("\n🧪 Testing UI Components...")
    
    try:
        import os
        
        # Check ServiceHealth.jsx
        assert os.path.exists("ui/src/ServiceHealth.jsx"), \
            "ServiceHealth.jsx should exist"
        print(f"  ✅ ServiceHealth.jsx exists")
        
        # Check MultiAgentDebate.jsx
        assert os.path.exists("ui/src/MultiAgentDebate.jsx"), \
            "MultiAgentDebate.jsx should exist"
        print(f"  ✅ MultiAgentDebate.jsx exists")
        
        # Check App.jsx imports them
        with open("ui/src/App.jsx", "r") as f:
            content = f.read()
        
        assert "import ServiceHealth from" in content, \
            "App.jsx should import ServiceHealth"
        print(f"  ✅ App.jsx imports ServiceHealth")
        
        assert "import MultiAgentDebate from" in content, \
            "App.jsx should import MultiAgentDebate"
        print(f"  ✅ App.jsx imports MultiAgentDebate")
        
        assert "debate_complete" in content, \
            "App.jsx should handle debate_complete event"
        print(f"  ✅ App.jsx handles debate events")
        
        return True
        
    except Exception as e:
        print(f"  ❌ UI components test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Log Whisperer - New Features Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Critic Agent", test_critic_agent()))
    results.append(("Incident Simulator", test_simulator()))
    results.append(("Cost Calculator", test_cost_calculator()))
    results.append(("Confidence Tracker", test_confidence_tracker()))
    results.append(("Pipeline Integration", test_pipeline_integration()))
    results.append(("UI Components", test_ui_components()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print("\n" + "=" * 60)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! You're ready to demo!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix before demo.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
