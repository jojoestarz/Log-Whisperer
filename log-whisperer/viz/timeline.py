"""Rerun.io spatial timeline — P3 owns this file."""
import time, structlog
log = structlog.get_logger()

try:
    import rerun as rr
    RERUN_AVAILABLE = True
except ImportError:
    RERUN_AVAILABLE = False

COLORS = {"CRITICAL":(255,77,109),"ERROR":(255,100,80),"WARN":(244,162,40),"INFO":(0,232,122),"DEBUG":(100,150,130)}
ICONS  = {"CRITICAL":"🔴","ERROR":"🟠","WARN":"🟡","INFO":"🟢","DEBUG":"⚪"}

class RerunTimeline:
    def __init__(self, app_id: str = "log_whisperer"):
        if RERUN_AVAILABLE:
            rr.init(app_id, spawn=True)

    def log_event(self, path: str, message: str, level: str = "INFO"):
        if RERUN_AVAILABLE:
            rr.set_time_seconds("timeline", time.time())
            rr.log(path, rr.TextLog(message, color=COLORS.get(level,(200,200,200))))
        print(f"  {ICONS.get(level,'•')} [{path}] {message}")
