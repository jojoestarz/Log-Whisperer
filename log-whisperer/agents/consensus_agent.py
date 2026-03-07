"""Consensus Agent - Coordinates multi-agent voting"""
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Vote:
    agent: str
    choice: str
    confidence: float
    reasoning: str

class ConsensusAgent:
    """Manages voting and consensus among agents"""
    
    def __init__(self):
        self.votes = []
    
    def collect_vote(self, agent: str, choice: str, confidence: float, reasoning: str):
        """Collect a vote from an agent"""
        vote = Vote(agent, choice, confidence, reasoning)
        self.votes.append(vote)
    
    def calculate_consensus(self) -> Dict:
        """Calculate consensus from votes"""
        if not self.votes:
            return {"consensus": None, "confidence": 0.0}
        
        # Weight votes by confidence
        weighted_votes = {}
        for vote in self.votes:
            if vote.choice not in weighted_votes:
                weighted_votes[vote.choice] = 0
            weighted_votes[vote.choice] += vote.confidence
        
        # Find winner
        winner = max(weighted_votes.items(), key=lambda x: x[1])
        total_weight = sum(weighted_votes.values())
        
        # Get supporting votes
        supporting = [v for v in self.votes if v.choice == winner[0]]
        
        return {
            "consensus": winner[0],
            "confidence": winner[1] / total_weight,
            "votes_for": len(supporting),
            "votes_against": len(self.votes) - len(supporting),
            "reasoning": [v.reasoning for v in supporting]
        }
    
    def reset(self):
        """Reset votes for new decision"""
        self.votes = []

# Global consensus
_consensus = ConsensusAgent()

def get_consensus():
    return _consensus
