"""Orchestrator Agent - Dynamically spawns and coordinates specialized agents"""
from typing import List, Dict
import asyncio

class SpecializedAgent:
    """Dynamically created specialized agent"""
    def __init__(self, name: str, expertise: str, task: str):
        self.name = name
        self.expertise = expertise
        self.task = task
        self.status = "spawned"
        self.result = None
    
    async def execute(self) -> Dict:
        """Execute the specialized task"""
        self.status = "working"
        # Simulate specialized work
        await asyncio.sleep(0.5)
        
        results = {
            "BGP_SPECIALIST": {
                "analysis": "BGP route table corruption detected in 3 edge routers",
                "recommendation": "Isolate affected routers, restore from backup config",
                "confidence": 0.94
            },
            "NETWORK_SPECIALIST": {
                "analysis": "Packet loss detected on upstream links",
                "recommendation": "Failover to secondary network path",
                "confidence": 0.88
            },
            "DATABASE_SPECIALIST": {
                "analysis": "Connection pool exhaustion imminent",
                "recommendation": "Scale connection pool, restart stale connections",
                "confidence": 0.91
            }
        }
        
        self.result = results.get(self.name, {
            "analysis": f"Specialized analysis for {self.expertise}",
            "recommendation": "Execute domain-specific remediation",
            "confidence": 0.85
        })
        self.status = "complete"
        return self.result

class OrchestratorAgent:
    """Dynamically spawns specialized agents based on incident type"""
    
    def __init__(self):
        self.spawned_agents = []
    
    async def analyze_and_spawn(self, incident_type: str, root_cause: str) -> List[SpecializedAgent]:
        """Analyze incident and spawn appropriate specialized agents"""
        agents_to_spawn = []
        
        # Determine which specialists are needed
        if "BGP" in root_cause or "routing" in root_cause.lower():
            agents_to_spawn.append(SpecializedAgent(
                "BGP_SPECIALIST",
                "BGP routing and network protocols",
                "Analyze BGP route tables and propose fixes"
            ))
        
        if "network" in root_cause.lower() or "connection" in root_cause.lower():
            agents_to_spawn.append(SpecializedAgent(
                "NETWORK_SPECIALIST",
                "Network topology and connectivity",
                "Analyze network paths and failover options"
            ))
        
        if "database" in root_cause.lower() or "connection pool" in root_cause.lower():
            agents_to_spawn.append(SpecializedAgent(
                "DATABASE_SPECIALIST",
                "Database performance and connections",
                "Analyze database health and connection pools"
            ))
        
        # Execute all specialists in parallel
        if agents_to_spawn:
            await asyncio.gather(*[agent.execute() for agent in agents_to_spawn])
            self.spawned_agents.extend(agents_to_spawn)
        
        return agents_to_spawn
    
    def get_specialist_insights(self) -> List[Dict]:
        """Get insights from all spawned specialists"""
        return [
            {
                "name": agent.name,
                "expertise": agent.expertise,
                "result": agent.result
            }
            for agent in self.spawned_agents
            if agent.status == "complete"
        ]

# Global orchestrator
_orchestrator = OrchestratorAgent()

def get_orchestrator():
    return _orchestrator
