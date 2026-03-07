"""Memory Agent - Learns from past incidents"""
import json
from datetime import datetime
from typing import List, Dict

class IncidentMemory:
    """Stores and retrieves past incident patterns"""
    
    def __init__(self):
        self.incidents = []
        self.patterns = {}
    
    def store_incident(self, root_cause: str, solution: str, mttr: int, success: bool):
        """Store a resolved incident"""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "root_cause": root_cause,
            "solution": solution,
            "mttr": mttr,
            "success": success
        }
        self.incidents.append(incident)
        
        # Extract pattern
        pattern_key = self._extract_pattern(root_cause)
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = []
        self.patterns[pattern_key].append(incident)
    
    def _extract_pattern(self, root_cause: str) -> str:
        """Extract pattern from root cause"""
        # Simple pattern extraction - in production would use embeddings
        keywords = ["BGP", "API", "database", "network", "memory", "disk"]
        for keyword in keywords:
            if keyword.lower() in root_cause.lower():
                return keyword
        return "unknown"
    
    def recall_similar(self, current_cause: str) -> List[Dict]:
        """Recall similar past incidents"""
        pattern = self._extract_pattern(current_cause)
        return self.patterns.get(pattern, [])
    
    def get_success_rate(self, pattern: str) -> float:
        """Get success rate for a pattern"""
        incidents = self.patterns.get(pattern, [])
        if not incidents:
            return 0.0
        successful = sum(1 for i in incidents if i["success"])
        return successful / len(incidents)
    
    def suggest_solution(self, current_cause: str) -> Dict:
        """Suggest solution based on past incidents"""
        similar = self.recall_similar(current_cause)
        if not similar:
            return {"suggestion": None, "confidence": 0.0}
        
        # Find most successful solution
        successful = [i for i in similar if i["success"]]
        if not successful:
            return {"suggestion": None, "confidence": 0.0}
        
        # Return most recent successful solution
        best = sorted(successful, key=lambda x: x["timestamp"])[-1]
        confidence = len(successful) / len(similar)
        
        return {
            "suggestion": best["solution"],
            "confidence": confidence,
            "past_mttr": best["mttr"],
            "similar_count": len(similar)
        }

# Global memory
_memory = IncidentMemory()

def get_memory():
    return _memory

# Pre-populate with some learned incidents
_memory.store_incident(
    "BGP route withdrawal due to configuration error",
    "argocd app rollback bgp-config",
    180,
    True
)
_memory.store_incident(
    "API gateway timeout due to upstream service",
    "kubectl rollout restart deployment/api-gateway",
    240,
    True
)
