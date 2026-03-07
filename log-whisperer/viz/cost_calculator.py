"""Real-time Cost Calculator - Shows money burning during outages"""
import time
from typing import Dict
from dataclasses import dataclass

@dataclass
class CostMetrics:
    """Cost impact metrics"""
    cost_per_minute: float = 14_056  # Industry average from Gartner
    customers_affected: int = 1_100
    revenue_per_customer_per_hour: float = 450
    sla_penalty_per_minute: float = 2_800

class CostCalculator:
    """Calculates real-time financial impact of incidents"""
    
    def __init__(self, metrics: CostMetrics = None):
        self.metrics = metrics or CostMetrics()
        self.incident_start = None
        self.incident_end = None
    
    def start_incident(self):
        """Mark incident start time"""
        self.incident_start = time.time()
        self.incident_end = None
    
    def resolve_incident(self):
        """Mark incident resolution"""
        self.incident_end = time.time()
    
    def get_current_cost(self) -> Dict:
        """Calculate current cost (live during incident)"""
        if not self.incident_start:
            return {"total_cost": 0, "duration_seconds": 0}
        
        end_time = self.incident_end or time.time()
        duration_seconds = end_time - self.incident_start
        duration_minutes = duration_seconds / 60
        
        # Direct operational cost
        operational_cost = duration_minutes * self.metrics.cost_per_minute
        
        # Lost revenue
        lost_revenue = (duration_minutes / 60) * self.metrics.customers_affected * self.metrics.revenue_per_customer_per_hour
        
        # SLA penalties
        sla_penalties = duration_minutes * self.metrics.sla_penalty_per_minute
        
        total_cost = operational_cost + lost_revenue + sla_penalties
        
        return {
            "total_cost": int(total_cost),
            "operational_cost": int(operational_cost),
            "lost_revenue": int(lost_revenue),
            "sla_penalties": int(sla_penalties),
            "duration_seconds": int(duration_seconds),
            "duration_minutes": round(duration_minutes, 2),
            "cost_per_second": int(total_cost / duration_seconds) if duration_seconds > 0 else 0
        }
    
    def compare_mttr(self, baseline_minutes: float, actual_minutes: float) -> Dict:
        """Compare costs between baseline and actual MTTR"""
        baseline_cost = baseline_minutes * (
            self.metrics.cost_per_minute +
            (self.metrics.customers_affected * self.metrics.revenue_per_customer_per_hour / 60) +
            self.metrics.sla_penalty_per_minute
        )
        
        actual_cost = actual_minutes * (
            self.metrics.cost_per_minute +
            (self.metrics.customers_affected * self.metrics.revenue_per_customer_per_hour / 60) +
            self.metrics.sla_penalty_per_minute
        )
        
        savings = baseline_cost - actual_cost
        reduction_pct = (savings / baseline_cost) * 100 if baseline_cost > 0 else 0
        
        return {
            "baseline_cost": int(baseline_cost),
            "actual_cost": int(actual_cost),
            "savings": int(savings),
            "reduction_percent": round(reduction_pct, 1),
            "baseline_mttr_minutes": baseline_minutes,
            "actual_mttr_minutes": actual_minutes
        }
    
    def get_live_ticker_data(self) -> Dict:
        """Get data for live cost ticker animation"""
        current = self.get_current_cost()
        
        return {
            "current_cost": current["total_cost"],
            "cost_per_second": current["cost_per_second"],
            "duration": current["duration_seconds"],
            "is_active": self.incident_end is None,
            "ticker_speed_ms": 100  # Update every 100ms for smooth animation
        }


# Global calculator
_calculator = None

def get_calculator():
    global _calculator
    if _calculator is None:
        _calculator = CostCalculator()
    return _calculator

def reset_calculator():
    global _calculator
    _calculator = CostCalculator()
    return _calculator
