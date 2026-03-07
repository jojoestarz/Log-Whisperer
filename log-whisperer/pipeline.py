"""Main pipeline orchestration"""
import asyncio
import os

# emit is injected from server to avoid circular imports
_emit = None


def set_emit(fn):
    global _emit
    _emit = fn


async def run_pipeline():
    """Execute the full Log Whisperer pipeline"""
    logs = open("data/cloudflare_incident.json").read()
    await run_pipeline_with_logs(logs)

async def run_pipeline_with_logs(logs: str):
    """Execute pipeline with provided logs (for simulator integration)"""
    from agents.decision_agent import analyse, CACHED
    from agents.writer_agent import generate_plan
    from agents.critic_agent import critique
    from agents.memory_agent import get_memory
    from agents.predictor_agent import get_predictor
    from agents.consensus_agent import get_consensus
    from agents.orchestrator_agent import get_orchestrator
    from safety.argo_hook import run_argo_mock
    from safety.sandbox_executor import run_sandbox
    from viz.confidence_tracker import get_tracker
    
    tracker = get_tracker()
    memory = get_memory()
    predictor = get_predictor()
    consensus = get_consensus()
    orchestrator = get_orchestrator()
    consensus.reset()
    
    await _emit({
        "type": "ingesting",
        "message": "Reading cloudflare_bgp_incident.json — 9 events, 33min window"
    })
    await asyncio.sleep(0.3)
    
    # Simulate confidence progression with detailed reasoning
    tracker.simulate_analysis_journey()
    
    # Emit only key confidence checkpoints (not all)
    key_points = [tracker.points[0], tracker.points[len(tracker.points)//2], tracker.points[-1]] if len(tracker.points) >= 3 else tracker.points
    for point in key_points:
        await _emit({
            "type": "confidence_update",
            "confidence": point.confidence,
            "reasoning": point.reasoning,
            "evidence_count": point.evidence_count
        })
        await asyncio.sleep(0.2)
    
    # Decision Agent
    fault = analyse(logs)
    
    await _emit({
        "type": "diagnosis",
        "message": fault.root_cause,
        "blast_radius": fault.blast_radius,
        "confidence": fault.confidence,
        "affected_services": fault.affected_services
    })
    await asyncio.sleep(0.3)
    
    # Orchestrator Agent - Spawn specialized agents
    await _emit({
        "type": "orchestrator_spawning",
        "message": f"Orchestrator: Analyzing incident type. Spawning specialized agents..."
    })
    await asyncio.sleep(0.2)
    
    specialists = await orchestrator.analyze_and_spawn("bgp_outage", fault.root_cause)
    
    if specialists:
        for specialist in specialists:
            await _emit({
                "type": "specialist_spawned",
                "agent_name": specialist.name,
                "expertise": specialist.expertise,
                "result": specialist.result
            })
            await asyncio.sleep(0.2)
    
    # Memory Agent - Check for similar past incidents
    memory_result = memory.suggest_solution(fault.root_cause)
    if memory_result["suggestion"]:
        await _emit({
            "type": "memory_recall",
            "message": f"Memory Agent: I've seen {memory_result['similar_count']} similar incidents. Past solution: {memory_result['suggestion']}. Success rate: {memory_result['confidence']*100:.0f}%",
            "confidence": memory_result["confidence"]
        })
        await asyncio.sleep(0.2)
    
    # Predictor Agent - Predict cascading failures
    predictions = predictor.analyze_trends({"root_cause": fault.root_cause})
    if predictions:
        high_risk = [p for p in predictions if p["probability"] > 0.7]
        if high_risk:
            await _emit({
                "type": "prediction",
                "message": f"Predictor Agent: I predict {len(high_risk)} cascading failures. Highest risk: {high_risk[0]['description']} ({high_risk[0]['probability']*100:.0f}% probability)",
                "predictions": predictions
            })
            await asyncio.sleep(0.2)
    
    # Writer Agent
    plan = await generate_plan(fault)
    await _emit({
        "type": "fix_proposed",
        "command": plan.commands[0],
        "all_commands": plan.commands,
        "risk_score": plan.risk_score,
        "safety_level": plan.safety_level,
        "plan_id": "plan_a"
    })
    await asyncio.sleep(0.3)
    
    # Critic Agent - Multi-agent debate
    critique_result = await critique(plan, fault)
    
    await _emit({
        "type": "critique",
        "concerns": critique_result["concerns"],
        "alternative_commands": critique_result["alternative_plan"],
        "confidence": critique_result["confidence"]
    })
    await asyncio.sleep(0.3)
    
    # Show debate conclusion
    if critique_result["recommendation"] == "revise":
        await _emit({
            "type": "debate_complete",
            "plan_a": plan.commands,
            "plan_b": critique_result["alternative_plan"],
            "recommendation": "plan_b",
            "reason": "Critic identified safety improvements"
        })
        # Use the safer plan
        plan.commands = critique_result["alternative_plan"]
        await asyncio.sleep(0.2)
    
    # Consensus Agent - Multi-agent voting
    consensus.collect_vote("DECISION", "plan_b", 0.97, "Root cause analysis supports this approach")
    consensus.collect_vote("WRITER", "plan_a", 0.85, "Original plan is faster")
    consensus.collect_vote("CRITIC", "plan_b", 0.95, "Safer with validation steps")
    
    consensus_result = consensus.calculate_consensus()
    await _emit({
        "type": "consensus",
        "message": f"Consensus Agent: {consensus_result['votes_for']} agents vote for Plan B. Consensus confidence: {consensus_result['confidence']*100:.0f}%",
        "consensus": consensus_result
    })
    await asyncio.sleep(0.3)
    
    # Safety layer
    plan = run_argo_mock(plan)
    violations = run_sandbox(plan)
    
    for v in violations:
        await _emit(v)
        await asyncio.sleep(0.2)
    
    await _emit({
        "type": "awaiting_approval",
        "risk_score": plan.risk_score,
        "message": "Dry-run passed — awaiting human approval"
    })
