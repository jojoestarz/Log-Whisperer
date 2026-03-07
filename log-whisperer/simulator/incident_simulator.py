"""Live Incident Simulator - Creates real outages for demo"""
import asyncio
import random
import time
from datetime import datetime
from typing import Dict, List
import json

class IncidentSimulator:
    """Simulates real infrastructure failures"""
    
    def __init__(self):
        self.services = {
            "api-gateway": {"status": "healthy", "latency_ms": 45},
            "bgp-router": {"status": "healthy", "routes": 1200},
            "cdn-edge": {"status": "healthy", "cache_hit_rate": 0.94},
            "dns-resolver": {"status": "healthy", "qps": 15000}
        }
        self.incident_active = False
        self.incident_start = None
        self.logs = []
    
    async def inject_bgp_failure(self):
        """Inject the Cloudflare-style BGP bug"""
        self.incident_active = True
        self.incident_start = time.time()
        
        # T+0: Empty string bug triggers
        await self._log("ERROR", "bgp-router", "Query().Get('pending_delete') returned empty string")
        self.services["bgp-router"]["status"] = "degraded"
        await asyncio.sleep(0.5)
        
        # T+2: Cascading failures
        await self._log("CRITICAL", "bgp-router", "Withdrawing 1,200 BGP prefixes")
        self.services["bgp-router"]["routes"] = 0
        self.services["bgp-router"]["status"] = "critical"
        await asyncio.sleep(0.3)
        
        # T+5: Customer impact
        await self._log("ERROR", "api-gateway", "Connection refused: upstream bgp-router unreachable")
        self.services["api-gateway"]["status"] = "critical"
        self.services["api-gateway"]["latency_ms"] = 9999
        await asyncio.sleep(0.4)
        
        # T+8: Full outage
        await self._log("CRITICAL", "cdn-edge", "Cache miss rate 100% - origin unreachable")
        self.services["cdn-edge"]["status"] = "down"
        self.services["cdn-edge"]["cache_hit_rate"] = 0.0
        
        await self._log("CRITICAL", "dns-resolver", "SERVFAIL - no route to authoritative NS")
        self.services["dns-resolver"]["status"] = "down"
        self.services["dns-resolver"]["qps"] = 0
        
        return self.get_incident_snapshot()
    
    async def heal(self, commands: List[str]):
        """Execute remediation and restore services"""
        for cmd in commands:
            await asyncio.sleep(0.8)
            
            if "rollback" in cmd.lower():
                await self._log("INFO", "bgp-router", f"Executing: {cmd}")
                self.services["bgp-router"]["status"] = "recovering"
                self.services["bgp-router"]["routes"] = 1200
                await asyncio.sleep(0.5)
                self.services["bgp-router"]["status"] = "healthy"
            
            elif "scale" in cmd.lower():
                await self._log("INFO", "api-gateway", f"Executing: {cmd}")
                self.services["api-gateway"]["status"] = "recovering"
                await asyncio.sleep(0.4)
                self.services["api-gateway"]["status"] = "healthy"
                self.services["api-gateway"]["latency_ms"] = 45
            
            elif "restart" in cmd.lower():
                await self._log("INFO", "cdn-edge", f"Executing: {cmd}")
                self.services["cdn-edge"]["status"] = "healthy"
                self.services["cdn-edge"]["cache_hit_rate"] = 0.94
                self.services["dns-resolver"]["status"] = "healthy"
                self.services["dns-resolver"]["qps"] = 15000
        
        self.incident_active = False
        mttr = int(time.time() - self.incident_start)
        await self._log("INFO", "system", f"All services restored. MTTR: {mttr}s")
        
        return {
            "status": "resolved",
            "mttr_seconds": mttr,
            "services": self.services
        }
    
    async def _log(self, level: str, service: str, message: str):
        """Add log entry"""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "service": service,
            "message": message
        }
        self.logs.append(entry)
    
    def get_incident_snapshot(self) -> Dict:
        """Get current incident state"""
        return {
            "active": self.incident_active,
            "duration_seconds": int(time.time() - self.incident_start) if self.incident_start else 0,
            "services": self.services,
            "logs": self.logs[-20:]  # Last 20 logs
        }
    
    def get_logs_json(self) -> str:
        """Export logs as JSON for agent consumption"""
        return json.dumps({
            "incident_id": "sim_" + str(int(time.time())),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "events": self.logs
        }, indent=2)


# Global simulator instance
_simulator = None

def get_simulator():
    global _simulator
    if _simulator is None:
        _simulator = IncidentSimulator()
    return _simulator
