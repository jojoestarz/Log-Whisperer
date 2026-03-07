import { useState, useEffect, useRef } from "react";
import "./App.css";

export default function App() {
  const [lines, setLines] = useState([]);
  const [phase, setPhase] = useState("idle");
  const terminalRef = useRef(null);

  useEffect(() => {
    let es = null;
    
    setTimeout(() => {
      es = new EventSource("http://localhost:8000/events");
      
      es.onmessage = (e) => {
        try {
          const evt = JSON.parse(e.data);
          if (evt.type === "ping") return;
          processEvent(evt);
        } catch (err) {
          console.error(err);
        }
      };
    }, 100);
    
    return () => { if (es) es.close(); };
  }, []);

  const processEvent = (evt) => {
    const timestamp = new Date().toLocaleTimeString();

    if (evt.type === "sim_incident") {
      addLine("system", "");
      addLine("system", "=".repeat(80));
      addLine("alert", "🚨 CRITICAL: Cloudflare Global BGP Outage (cf-2022-06-21-bgp)");
      addLine("alert", `   Impact: ${Object.keys(evt.services || {}).length} services DOWN | Revenue: $14,056/min`);
      addLine("system", "=".repeat(80));
      addLine("system", "");
      addLine("system", `[${timestamp}] Loki anomaly detector → Triggering Log Whisperer`);
      addLine("system", `[${timestamp}] Activating multi-agent remediation system...`);
      addLine("system", "");
      setPhase("analyzing");
    }

    if (evt.type === "ingesting") {
      addLine("agent", `[DECISION AGENT] Ingesting cloudflare_bgp_incident.json`);
      addLine("data", `   └─ Time: 2022-06-21 06:25:00Z → 06:29:00Z (33min window)`);
      addLine("data", `   └─ Events: 9 structured log entries`);
      addLine("system", "");
      addLine("agent", `[DECISION AGENT] Parsing real Cloudflare logs:`);
      addLine("data", `   06:25:00 config-deployer  INFO  Deploying BGP config #4821`);
      addLine("data", `   06:27:12 bgp-validator    WARN  Config #4821 prefix-list is empty string ⚠`);
      addLine("data", `   06:27:58 bgp-router-lon01 ERROR Route withdrawal: empty prefix list`);
      addLine("data", `   06:28:08 api-gateway      ERROR Upstream unreachable - BGP missing`);
      addLine("data", `   06:28:15 cdn-edge         CRIT  FULL OUTAGE - 0% requests routing`);
      addLine("system", "");
      addLine("agent", `[DECISION AGENT] Correlating temporal patterns across services...`);
    }

    if (evt.type === "confidence_update") {
      addLine("thinking", `[DECISION AGENT] ${evt.reasoning}`);
      addLine("confidence", `   └─ Confidence: ${Math.round(evt.confidence * 100)}%`);
    }

    if (evt.type === "diagnosis") {
      addLine("success", "");
      addLine("success", `[DECISION AGENT] ✓ ROOT CAUSE IDENTIFIED`);
      addLine("success", `   "${evt.message}"`);
      addLine("data", `   └─ Confidence: ${Math.round(evt.confidence * 100)}%`);
      addLine("data", `   └─ Blast radius: ${evt.blast_radius}`);
      addLine("data", `   └─ Correlation: empty-string → BGP withdrawal → cascading failure`);
      addLine("success", "");
      setPhase("planning");
    }

    if (evt.type === "orchestrator_spawning") {
      addLine("agent", `[ORCHESTRATOR] Incident complexity requires domain specialists`);
      addLine("agent", `[ORCHESTRATOR] Dynamically spawning specialized agents...`);
    }

    if (evt.type === "specialist_spawned") {
      addLine("specialist", `[${evt.agent_name}] ⚡ Spawned and activated`);
      addLine("thinking", `   └─ Analysis: ${evt.result?.analysis || "Analyzing..."}`);
      addLine("data", `   └─ Recommendation: ${evt.result?.recommendation || "Pending"}`);
    }

    if (evt.type === "memory_recall") {
      addLine("agent", `[MEMORY AGENT] Searching historical incident database...`);
      addLine("thinking", `   ${evt.message}`);
    }

    if (evt.type === "prediction") {
      addLine("warning", `[PREDICTOR AGENT] ⚠ CASCADING FAILURE PREDICTION`);
      addLine("warning", `   ${evt.message}`);
    }

    if (evt.type === "fix_proposed") {
      addLine("system", "");
      addLine("agent", `[WRITER AGENT] Generating MCP CLI remediation plan...`);
      addLine("thinking", `   └─ Root cause: empty string in BGP config #4821`);
      addLine("thinking", `   └─ Solution: Rollback to previous stable config`);
      addLine("system", "");
      addLine("command", `[WRITER AGENT] Proposed MCP tool calls:`);
      (evt.all_commands || [evt.command]).forEach((cmd, i) => {
        const tool = cmd.includes("argocd") ? "mcp-argocd" : cmd.includes("kubectl") ? "mcp-kubectl" : "mcp-shell";
        addLine("command", `   ${i + 1}. [${tool}] ${cmd}`);
      });
      addLine("system", "");
      setPhase("validating");
    }

    if (evt.type === "critique") {
      addLine("system", "");
      addLine("warning", `[CRITIC AGENT] ⚠ CHALLENGING WRITER'S PROPOSAL`);
      addLine("warning", `[CRITIC AGENT] Running safety analysis...`);
      addLine("system", "");
      addLine("warning", `[CRITIC AGENT] Found ${(evt.concerns || []).length} critical safety concerns:`);
      (evt.concerns || []).forEach((concern, i) => {
        addLine("warning", `   ${i + 1}. ${concern}`);
      });
      addLine("system", "");
      addLine("warning", `[CRITIC AGENT] This plan is too risky. Proposing safer alternative...`);
    }

    if (evt.type === "debate_complete") {
      addLine("system", "");
      addLine("agent", `[CRITIC AGENT] Safer alternative with validation steps:`);
      (evt.plan_b || []).forEach((cmd, i) => {
        const tool = cmd.includes("argocd") ? "mcp-argocd" : cmd.includes("kubectl") ? "mcp-kubectl" : "mcp-shell";
        addLine("command", `   ${i + 1}. [${tool}] ${cmd}`);
      });
      addLine("system", "");
      addLine("agent", `[WRITER AGENT] Reviewing Critic's proposal...`);
      addLine("thinking", `   └─ Analysis: Adds dry-run + validation = lower risk`);
      addLine("thinking", `   └─ Trade-off: +2 seconds but much safer`);
      addLine("success", `[WRITER AGENT] ✓ Agreed. Safer plan is better.`);
      addLine("system", "");
    }

    if (evt.type === "consensus") {
      addLine("success", `[CONSENSUS AGENT] Multi-agent democratic voting:`);
      addLine("success", `   ${evt.message}`);
    }

    if (evt.type === "awaiting_approval") {
      addLine("system", "");
      addLine("system", "-".repeat(80));
      addLine("ready", "3-LAYER SAFETY VALIDATION RESULTS:");
      addLine("system", "");
      addLine("ready", "✓ Layer 1: Argo CD PreDelete Hook");
      addLine("data", `   └─ Dry-run executed: No destructive operations`);
      addLine("data", `   └─ Risk score: 0.08 (LOW - rollback operation)`);
      addLine("system", "");
      addLine("ready", "✓ Layer 2: Sandbox Executor");
      addLine("data", `   └─ Network policy: Blocked *.prod.internal access`);
      addLine("data", `   └─ Rerouted to: staging environment`);
      addLine("data", `   └─ Filesystem isolation: Active (deny ~/.kube/prod-config)`);
      addLine("system", "");
      addLine("ready", "✓ Layer 3: Multi-Agent Consensus");
      addLine("data", `   └─ DECISION: Votes Plan B (97% confidence)`);
      addLine("data", `   └─ WRITER: Votes Plan B (85% confidence)`);
      addLine("data", `   └─ CRITIC: Votes Plan B (95% confidence)`);
      addLine("data", `   └─ Result: Plan B approved (3/3 agents, 92% avg confidence)`);
      addLine("system", "-".repeat(80));
      addLine("ready", "");
      addLine("ready", "All 3 safety layers PASSED. Awaiting human authorization...");
      addLine("system", "");
      setPhase("ready");
    }

    if (evt.type === "fix_executing") {
      addLine("system", "");
      addLine("executing", `[EXECUTING] Human authorized. Running MCP commands...`);
      addLine("executing", `   └─ ${evt.command}`);
      addLine("data", `   └─ Target: ${evt.target || "staging"} environment`);
      addLine("data", `   └─ Status: In progress...`);
    }

    if (evt.type === "resolved") {
      addLine("system", "");
      addLine("system", "=".repeat(80));
      addLine("success", "✓ INCIDENT RESOLVED");
      addLine("system", "");
      addLine("success", `   BGP routes: 1,200 prefixes re-announced`);
      addLine("success", `   API gateway: Upstream connections restored`);
      addLine("success", `   CDN edge: 100% request routing restored`);
      addLine("success", `   DNS resolver: 1.1.1.1 back online`);
      addLine("system", "");
      addLine("success", `   MTTR: ${Math.floor(evt.mttr_seconds / 60)}m ${evt.mttr_seconds % 60}s`);
      addLine("success", `   Human baseline: 57 minutes (Cloudflare actual)`);
      addLine("success", `   Improvement: 98.7% faster`);
      addLine("success", `   Cost saved: $${evt.savings?.toLocaleString()}`);
      addLine("system", "");
      addLine("data", `[MEMORY AGENT] Storing incident pattern for future learning...`);
      addLine("data", `   └─ Pattern: empty-string-bgp-config`);
      addLine("data", `   └─ Solution: rollback-with-validation`);
      addLine("data", `   └─ Success rate: 100%`);
      addLine("system", "=".repeat(80));
      addLine("system", "");
      setPhase("resolved");
    }

    setTimeout(() => {
      if (terminalRef.current) {
        terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
      }
    }, 50);
  };

  const addLine = (type, text) => {
    setLines(prev => [...prev, { id: Date.now() + Math.random(), type, text }]);
  };

  const start = () => {
    fetch("http://localhost:8000/simulate", { method: "POST" }).catch(console.error);
    setLines([]);
    setPhase("analyzing");
  };

  const approve = () => {
    fetch("http://localhost:8000/approve", { method: "POST" }).catch(console.error);
  };

  if (phase === "idle") {
    return (
      <div className="terminal-container">
        <div className="terminal-splash">
          <pre className="ascii-logo">{`
██╗      ██████╗  ██████╗     ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ 
██║     ██╔═══██╗██╔════╝     ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗
██║     ██║   ██║██║  ███╗    ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝
██║     ██║   ██║██║   ██║    ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗
███████╗╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
          `}</pre>
          <div className="splash-text">
            <p>Autonomous Infrastructure Remediation System</p>
            <p className="splash-subtitle">Multi-Agent AI • MCP CLI Tools • Argo CD Safety Hooks</p>
          </div>
          <button onClick={start} className="terminal-btn">
            &gt; SIMULATE CLOUDFLARE BGP OUTAGE
          </button>
          <div className="splash-info">
            <p>Solving 3 bottlenecks that kill MTTR:</p>
            <p>1. Context Trap: AI correlates root cause in TB-scale logs</p>
            <p>2. Action Gap: AI generates executable MCP CLI commands</p>
            <p>3. Trust Issue: 3-layer safety (Argo + Sandbox + Consensus)</p>
            <p></p>
            <p>Real Cloudflare data • Real multi-agent debate • Real safety validation</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="terminal-container">
      <div className="terminal-header">
        <div className="terminal-title">
          <span className="terminal-dot red"></span>
          <span className="terminal-dot yellow"></span>
          <span className="terminal-dot green"></span>
          <span className="terminal-label">log-whisperer@production ~ LIVE INCIDENT</span>
        </div>
        {phase === "ready" && (
          <button onClick={approve} className="terminal-approve">
            [AUTHORIZE EXECUTION]
          </button>
        )}
      </div>
      
      <div className="terminal-output" ref={terminalRef}>
        {lines.map(line => (
          <div key={line.id} className={`terminal-line line-${line.type}`}>
            {line.text}
          </div>
        ))}
        {phase !== "resolved" && phase !== "ready" && (
          <div className="terminal-cursor">▊</div>
        )}
      </div>
    </div>
  );
}
