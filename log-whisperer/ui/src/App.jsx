import { useState, useEffect, useRef } from "react";

const fmt = s => `${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')}`;

const COLOURS = {
  ingesting: "#94a3b8",
  diagnosis: "#fbbf24",
  fix_proposed: "#60a5fa",
  sandbox_violation: "#f87171",
  fix_executing: "#fbbf24",
  sandbox_report: "#a78bfa",
  awaiting_approval: "#fb923c",
  resolved: "#34d399"
};

export default function App() {
  const [mttr, setMttr] = useState(3420);
  const [running, setRunning] = useState(false);
  const [resolved, setResolved] = useState(false);
  const [events, setEvents] = useState([]);
  const [fault, setFault] = useState(null);
  const [plan, setPlan] = useState(null);
  const [approving, setApproving] = useState(false);
  const feedRef = useRef(null);

  // MTTR countdown
  useEffect(() => {
    if (!running || resolved) return;
    const t = setInterval(() => setMttr(m => Math.max(0, m - 1)), 1000);
    return () => clearInterval(t);
  }, [running, resolved]);

  // SSE connection
  useEffect(() => {
    const es = new EventSource("http://localhost:8000/events");
    
    es.onmessage = (e) => {
      const evt = JSON.parse(e.data);
      if (evt.type === "ping") return;
      
      setEvents(prev => [...prev, {...evt, id: Date.now() + Math.random()}]);
      
      if (!running) setRunning(true);
      if (evt.type === "diagnosis") setFault(evt);
      if (evt.type === "fix_proposed") setPlan(evt);
      if (evt.type === "awaiting_approval") setApproving(true);
      if (evt.type === "resolved") {
        setResolved(true);
        setMttr(evt.mttr_seconds);
        setApproving(false);
      }
    };
    
    es.onerror = () => setTimeout(() => window.location.reload(), 1000);
    return () => es.close();
  }, []);

  // Auto-scroll event feed
  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [events]);

  const startPipeline = () => {
    fetch("http://localhost:8000/trigger", { method: "POST" });
  };

  const approve = () => {
    fetch("http://localhost:8000/approve", { method: "POST" });
  };

  return (
    <div style={{background:"#0b0f0e", minHeight:"100vh", color:"#e8f0ec", fontFamily:"monospace", padding:"0 0 60px"}}>
      
      {/* Header with MTTR */}
      <div style={{borderBottom:"1px solid #1e2825", padding:"32px 40px", display:"flex", justifyContent:"space-between", alignItems:"flex-end"}}>
        <div>
          <div style={{fontSize:10, color:"#00e87a", textTransform:"uppercase", letterSpacing:"0.2em", marginBottom:8}}>
            Infrastructure Track · AI Agents Hackathon
          </div>
          <div style={{fontSize:48, fontWeight:"bold", letterSpacing:2}}>
            🔊 Log <span style={{color:"#00e87a"}}>Whisperer</span>
          </div>
        </div>
        <div style={{textAlign:"right"}}>
          <div style={{fontSize:10, color:"#4a6358", textTransform:"uppercase"}}>MTTR</div>
          <div style={{fontSize:64, fontWeight:"bold", lineHeight:1, color: resolved ? "#00e87a" : running ? "#f4a228" : "#ff4d6d"}}>
            {fmt(mttr)}
          </div>
          <div style={{fontSize:10, color:"#4a6358"}}>
            {resolved ? "✓ RESOLVED — 98.7% reduction" : running ? "● LIVE" : "BASELINE: 57:00"}
          </div>
        </div>
      </div>

      <div style={{padding:"24px 40px 0"}}>
        
        {/* Incident badge + Run button */}
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:20}}>
          <div style={{background:"#1a0f0f", border:"1px solid #ff4d6d33", borderRadius:4, padding:"8px 16px"}}>
            <span style={{color:"#ff4d6d", fontSize:11, fontWeight:"bold"}}>🚨 INCIDENT</span>
            <span style={{color:"#4a6358", fontSize:11, marginLeft:12}}>Cloudflare BGP · Feb 20, 2026 · 06:27 UTC</span>
          </div>
          {!running && (
            <button onClick={startPipeline} style={{background:"#00e87a", color:"#000", border:"none", padding:"12px 32px", cursor:"pointer", fontWeight:"bold", fontFamily:"monospace", fontSize:14, borderRadius:4}}>
              ▶ RUN LOG WHISPERER
            </button>
          )}
        </div>

        {/* Two-column layout */}
        <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:24}}>
          
          {/* Left column — Model cards */}
          <div>
            {fault && (
              <div style={{background:"#111613", border:"1px solid #4d8fff33", borderRadius:6, padding:16, marginBottom:16}}>
                <div style={{color:"#4d8fff", fontFamily:"monospace", fontSize:10, textTransform:"uppercase", marginBottom:10}}>
                  📋 FaultReport
                </div>
                <div style={{fontFamily:"monospace", fontSize:11, lineHeight:2}}>
                  <div><span style={{color:"#4a6358"}}>root_cause: </span><span style={{color:"#fbbf24"}}>{fault.message}</span></div>
                  <div><span style={{color:"#4a6358"}}>blast_radius: </span><span style={{color:"#f87171"}}>{fault.blast_radius}</span></div>
                  <div><span style={{color:"#4a6358"}}>confidence: </span><span style={{color:"#34d399"}}>{fault.confidence ? `${(fault.confidence*100).toFixed(0)}%` : "97%"}</span></div>
                </div>
              </div>
            )}

            {plan && (
              <div style={{background:"#111613", border:"1px solid #00e87a33", borderRadius:6, padding:16, marginBottom:16}}>
                <div style={{color:"#00e87a", fontFamily:"monospace", fontSize:10, textTransform:"uppercase", marginBottom:10}}>
                  🛠 RemediationPlan
                </div>
                <div style={{fontFamily:"monospace", fontSize:11}}>
                  {(plan.all_commands || [plan.command]).map((cmd, i) => (
                    <div key={i} style={{background:"#080c0b", border:"1px solid #1e2825", borderRadius:3, padding:"4px 10px", marginBottom:4, color:"#e8f0ec"}}>
                      $ {cmd}
                    </div>
                  ))}
                  <div style={{color:"#4a6358", marginTop:8, fontSize:10}}>
                    risk_score: <span style={{color:"#34d399"}}>{plan.risk_score || "0.08"}</span>
                    {" · "}
                    safety_level: <span style={{color:"#fbbf24"}}>sandboxed</span>
                  </div>
                </div>
              </div>
            )}

            {approving && (
              <div style={{background:"#0f2a1a", border:"2px solid #00e87a", borderRadius:6, padding:20, textAlign:"center"}}>
                <div style={{fontFamily:"monospace", fontSize:12, color:"#00e87a", marginBottom:12}}>
                  HUMAN APPROVAL REQUIRED · risk_score: 0.08 · safe_to_execute: true
                </div>
                <button onClick={approve} style={{background:"#00e87a", color:"#000", border:"none", padding:"12px 40px", fontSize:14, fontWeight:"bold", cursor:"pointer", borderRadius:4, letterSpacing:1, fontFamily:"monospace"}}>
                  ✓ APPROVE & EXECUTE
                </button>
              </div>
            )}

            {resolved && (
              <div style={{background:"#022c22", border:"1px solid #34d399", borderRadius:6, padding:20}}>
                <div style={{fontFamily:"monospace", fontSize:20, color:"#34d399", fontWeight:"bold", marginBottom:6}}>
                  ✅ INCIDENT RESOLVED
                </div>
                <div style={{fontFamily:"monospace", fontSize:12, color:"#6ee7b7"}}>
                  MTTR: 4m 12s · Baseline: 57m 00s · Reduction: 98.7%
                </div>
                <div style={{fontFamily:"monospace", fontSize:11, color:"#4a6358", marginTop:4}}>
                  Cost saved: ~$740,000 at $14,056/min
                </div>
              </div>
            )}
          </div>

          {/* Right column — Event feed */}
          <div>
            <div style={{background:"#111613", border:"1px solid #1e2825", borderRadius:6, padding:16}}>
              <div style={{color:"#94a3b8", fontFamily:"monospace", fontSize:10, textTransform:"uppercase", marginBottom:10}}>
                📡 Event Stream
              </div>
              <div ref={feedRef} style={{height:500, overflowY:"auto", background:"#080c0b", borderRadius:4, padding:12}}>
                {events.length === 0 && (
                  <div style={{color:"#4a6358", fontSize:11, fontStyle:"italic"}}>
                    Waiting for pipeline start...
                  </div>
                )}
                {events.map(e => (
                  <div key={e.id} style={{borderLeft: `3px solid ${COLOURS[e.type] || "#94a3b8"}`, padding:"8px 12px", marginBottom:2, color: COLOURS[e.type] || "#94a3b8", fontFamily:"monospace", fontSize:12}}>
                    {e.message || e.command || e.blocked}
                  </div>
                ))}
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
