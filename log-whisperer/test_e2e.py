#!/usr/bin/env python3
"""End-to-end test of the full system"""
import requests
import json
import time
from threading import Thread

def listen_events():
    """Listen to SSE stream"""
    print("\n📡 Listening to event stream...")
    response = requests.get("http://localhost:8000/events", stream=True, timeout=30)
    
    event_count = 0
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith('data: '):
                data = json.loads(decoded[6:])
                if data.get('type') != 'ping':
                    event_count += 1
                    print(f"   [{event_count}] {data.get('type')} - {data.get('message', data.get('command', ''))[:60]}")
                    
                    if data.get('type') == 'awaiting_approval':
                        print("\n   ⏸️  Pipeline waiting for approval")
                        return event_count
    
    return event_count

def main():
    print("🔊 Log Whisperer E2E Test\n")
    
    # Check backend
    print("1. Checking backend...")
    try:
        r = requests.get("http://localhost:8000/status", timeout=5)
        print(f"   ✓ Backend running - {r.json()}\n")
    except Exception as e:
        print(f"   ✗ Backend not running: {e}")
        print("   Run: python3 -m uvicorn server:app --reload --port 8000")
        return
    
    # Start event listener in background
    listener = Thread(target=listen_events, daemon=True)
    listener.start()
    
    time.sleep(1)
    
    # Trigger pipeline
    print("2. Triggering pipeline...")
    r = requests.post("http://localhost:8000/trigger")
    print(f"   ✓ Pipeline started - {r.json()}\n")
    
    # Wait for events
    time.sleep(8)
    
    print("\n✅ E2E test complete!")
    print("\nNext: Open http://localhost:5173 and click RUN LOG WHISPERER")

if __name__ == "__main__":
    main()
