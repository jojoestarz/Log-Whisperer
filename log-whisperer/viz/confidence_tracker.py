"""Confidence Decay Tracker - Shows AI uncertainty over time"""
import time
from typing import List, Dict
from dataclasses import dataclass
import math

@dataclass
class ConfidencePoint:
    timestamp: float
    confidence: float
    reasoning: str
    evidence_count: int

class ConfidenceTracker:
    """Tracks how AI confidence changes as it analyzes logs"""
    
    def __init__(self):
        self.points: List[ConfidencePoint] = []
        self.start_time = time.time()
    
    def add_point(self, confidence: float, reasoning: str, evidence_count: int):
        """Record a confidence measurement"""
        self.points.append(ConfidencePoint(
            timestamp=time.time() - self.start_time,
            confidence=confidence,
            reasoning=reasoning,
            evidence_count=evidence_count
        ))
    
    def simulate_analysis_journey(self, final_confidence: float = 0.97):
        """Simulate realistic confidence progression during log analysis"""
        # Start uncertain
        self.add_point(0.23, "Initial scan - multiple error patterns detected", 3)
        
        # Find correlations
        self.add_point(0.45, "Temporal correlation found: BGP withdrawal → API failures", 8)
        
        # Narrow down
        self.add_point(0.68, "Root cause candidate: empty string in Query().Get()", 15)
        
        # Validate
        self.add_point(0.82, "Pattern matches CVE-2026-1337 (Cloudflare incident)", 22)
        
        # High confidence
        self.add_point(final_confidence, "Confirmed: identical stack trace in 3 services", 28)
    
    def get_chart_data(self) -> Dict:
        """Export data for frontend visualization"""
        return {
            "points": [
                {
                    "time": p.timestamp,
                    "confidence": p.confidence,
                    "reasoning": p.reasoning,
                    "evidence": p.evidence_count
                }
                for p in self.points
            ],
            "final_confidence": self.points[-1].confidence if self.points else 0,
            "analysis_duration": self.points[-1].timestamp if self.points else 0
        }
    
    def get_uncertainty_score(self) -> float:
        """Calculate uncertainty metric (1 - confidence)"""
        if not self.points:
            return 1.0
        return 1.0 - self.points[-1].confidence
    
    def should_request_human_review(self) -> bool:
        """Determine if confidence is too low for auto-execution"""
        if not self.points:
            return True
        
        final = self.points[-1].confidence
        
        # Check for confidence decay (getting less certain over time)
        if len(self.points) >= 3:
            recent_trend = self.points[-1].confidence - self.points[-3].confidence
            if recent_trend < -0.1:  # Confidence dropped
                return True
        
        # Absolute threshold
        return final < 0.75


# Global tracker
_tracker = None

def get_tracker():
    global _tracker
    if _tracker is None:
        _tracker = ConfidenceTracker()
    return _tracker

def reset_tracker():
    global _tracker
    _tracker = ConfidenceTracker()
    return _tracker
