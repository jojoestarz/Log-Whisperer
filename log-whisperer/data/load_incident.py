"""Load incident log data from JSON."""
import json
from pathlib import Path
from models import LogEvent

def load_incident(filename: str = "cloudflare_incident.json") -> tuple[str, list[LogEvent]]:
    """Load incident data and return (incident_id, list of LogEvent objects)."""
    path = Path(__file__).parent / filename
    raw = json.loads(path.read_text())
    
    # Handle both formats: array or object with events
    if isinstance(raw, list):
        events = raw
        incident_id = "cloudflare-bgp-2022"
    else:
        events = raw.get("events", [])
        incident_id = raw.get("incident_id", "unknown")
    
    # Convert to LogEvent objects, handling different field names
    log_events = []
    for e in events:
        # Map 'message' to 'msg' if needed
        if 'message' in e and 'msg' not in e:
            e['msg'] = e.pop('message')
        # Set default level if missing
        if 'level' not in e:
            e['level'] = 'INFO'
        # Add correlated_event if missing
        if 'correlated_event' not in e:
            e['correlated_event'] = None
        log_events.append(LogEvent(**e))
    
    return incident_id, log_events


def load_cloudflare_incident() -> list[dict]:
    """
    Load Cloudflare incident data and return list of dicts.
    Backward compatibility function for existing demos.
    """
    path = Path(__file__).parent / "cloudflare_incident.json"
    raw = json.loads(path.read_text())
    
    # Handle both formats
    if isinstance(raw, list):
        return raw
    else:
        return raw.get("events", [])
