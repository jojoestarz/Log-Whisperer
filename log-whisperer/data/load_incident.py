"""Load incident log data from JSON."""
import json
from pathlib import Path
from models import LogEvent

def load_incident(filename: str = "cloudflare_incident.json") -> tuple[str, list[LogEvent]]:
    path = Path(__file__).parent / filename
    raw = json.loads(path.read_text())
    return raw["incident_id"], [LogEvent(**e) for e in raw["events"]]
