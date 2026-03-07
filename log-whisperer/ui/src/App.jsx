import { useState, useEffect, useRef } from "react";
import "./App.css";

export default function App() {
  const [conversation, setConversation] = useState([]);
  const [thinking, setThinking] = useState(null);
  const [phase, setPhase] = useState("waiting");
  const conversationRef = useRef(null);

  useEffect(() => {
    const es = new EventSource("http://localhost:8000/events");
    
    es.onmessage = (e) => {
      const evt = JSON.parse(e.data);
      if (evt.type === "ping") return;
      
      processEvent(evt);
    };
    
    return () => es.close();
  }, []);

  const processEvent = (evt) => {
    const messages = {
      sim_start: {
        agent: "SYSTEM",
        message: "CRITICAL ALERT: Infrastructure failure detected. Activating autonomous remediation protocol.",
        type: "alert"
      },
      sim_incident: {
        agent: "SYSTEM",
        message: `${Object.keys(evt.services || {}).length} services are down. Customers are impacted. Initiating multi-agent analysis.`,
        type: "alert"
      },
      ingesting: {
        agent: "DECISION",
        message: "I'm scanning the distributed logs now. Looking for patterns across 47 nodes...",
        type: "thinking"
      },
      confidence_update: {
        agent: "DECISION",
        message: evt.reasoning,
        confidence: evt.confidence,
        type: "analysis"
      },
      diagnosis: {
        agent: "DECISION",
        message: `I've found it. ${evt.message}. I'm ${Math.round(evt.confidence * 100)}% confident this is the root cause.`,
        type: "conclusion"
      },
      memory_recall: {
        agent: "MEMORY",
        message: evt.message,
        confidence: evt.confidence,
        type: "memory"
      },
      prediction: {
        agent: "PREDICTOR",
        message: evt.message,
        type: "prediction"
      },
      fix_proposed: {
        agent: "WRITER",
        message: `Based on the Decision Agent's analysis, I propose this remediation:\n\n${(evt.all_commands || [evt.command]).map((c, i) => `${i + 1}. ${c}`).join('\n')}\n\nThis should restore service immediately.`,
        type: "proposal"
      },
      critique: {
        agent: "CRITIC",
        message: `Wait. I see ${evt.concerns?.length || 0} potential risks with this plan:\n\n${(evt.concerns || []).map((c, i) => `⚠ ${i + 1}. ${c}`).join('\n')}\n\nLet me propose a safer alternative...`,
        type: "challenge"
      },
      debate_complete: {
        agent: "CRITIC",
        message: `Here's my safer plan:\n\n${(evt.plan_b || []).map((c, i) => `${i + 1}. ${c}`).join('\n')}\n\nThis adds validation steps and reduces risk. Writer Agent, do you agree?`,
        type: "counter_proposal"
      },
      consensus: {
        agent: "CONSENSUS",
        message: evt.message,
        type: "consensus"
      },
      awaiting_approval: {
        agent: "SYSTEM",
        message: "Multi-agent consensus achieved. All safety checks passed. Awaiting human authorization to execute.",
        type: "ready"
      },
      fix_executing: {
        agent: "SYSTEM",
        message: `Executing: ${evt.command}`,
        type: "executing"
      },
      resolved: {
        agent: "SYSTEM",
        message: `Incident resolved. MTTR: ${Math.floor(evt.mttr_seconds / 60)}m ${evt.mttr_seconds % 60}s. Services restored. Customers back online.`,
        type: "success"
      }
    };

    if (messages[evt.type]) {
      addMessage(messages[evt.type]);
    }

    // Update thinking indicator
    if (["ingesting", "confidence_update"].includes(evt.type)) {
      setThinking("DECISION");
    } else if (evt.type === "memory_recall") {
      setThinking("MEMORY");
    } else if (evt.type === "prediction") {
      setThinking("PREDICTOR");
    } else if (evt.type === "fix_proposed") {
      setThinking("WRITER");
    } else if (evt.type === "critique") {
      setThinking("CRITIC");
    } else if (evt.type === "consensus") {
      setThinking("CONSENSUS");
    } else if (["diagnosis", "debate_complete", "awaiting_approval"].includes(evt.type)) {
      setThinking(null);
    }

    // Update phase
    const phases = {
      sim_start: "CRISIS",
      ingesting: "ANALYZING",
      diagnosis: "PLANNING",
      memory_recall: "LEARNING",
      prediction: "PREDICTING",
      fix_proposed: "DEBATING",
      critique: "DEBATING",
      consensus: "VOTING",
      debate_complete: "READY",
      awaiting_approval: "READY",
      fix_executing: "EXECUTING",
      resolved: "RESOLVED"
    };
    if (phases[evt.type]) setPhase(phases[evt.type]);
  };

  const addMessage = (msg) => {
    setConversation(prev => [...prev, { ...msg, id: Date.now() + Math.random(), timestamp: new Date().toLocaleTimeString() }]);
    setTimeout(() => {
      if (conversationRef.current) {
        conversationRef.current.scrollTop = conversationRef.current.scrollHeight;
      }
    }, 100);
  };

  const start = () => {
    fetch("http://localhost:8000/simulate", { method: "POST" });
    setConversation([]);
    setPhase("CRISIS");
    setThinking(null);
  };

  const approve = () => {
    fetch("http://localhost:8000/approve", { method: "POST" });
  };

  return (
    <div className="theater">
      {/* Header */}
      <div className="theater-header">
        <div className="title-section">
          <h1 className="main-title">LOG WHISPERER</h1>
          <p className="subtitle">Multi-Agent Autonomous Remediation System</p>
        </div>
        
        <div className="phase-section">
          <div className={`phase-badge phase-${phase.toLowerCase()}`}>
            {phase}
          </div>
        </div>

        <div className="action-section">
          {phase === "waiting" && (
            <button className="action-button start" onClick={start}>
              INJECT INCIDENT
            </button>
          )}
          {phase === "READY" && (
            <button className="action-button approve" onClick={approve}>
              AUTHORIZE EXECUTION
            </button>
          )}
        </div>
      </div>

      {/* Main Conversation */}
      <div className="conversation-container" ref={conversationRef}>
        {conversation.length === 0 ? (
          <div className="waiting-state">
            <div className="waiting-icon">◉</div>
            <div className="waiting-text">System Ready</div>
            <div className="waiting-hint">Click "INJECT INCIDENT" to begin autonomous remediation</div>
          </div>
        ) : (
          conversation.map(msg => (
            <div key={msg.id} className={`message message-${msg.type}`}>
              <div className="message-header">
                <span className={`agent-badge agent-${msg.agent.toLowerCase()}`}>
                  {msg.agent}
                </span>
                <span className="message-time">{msg.timestamp}</span>
              </div>
              <div className="message-content">
                {msg.message.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
              {msg.confidence > 0 && (
                <div className="confidence-indicator">
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill" 
                      style={{ width: `${msg.confidence * 100}%` }}
                    />
                  </div>
                  <span className="confidence-text">
                    Confidence: {Math.round(msg.confidence * 100)}%
                  </span>
                </div>
              )}
            </div>
          ))
        )}

        {/* Thinking Indicator */}
        {thinking && (
          <div className="thinking-indicator">
            <span className={`agent-badge agent-${thinking.toLowerCase()}`}>
              {thinking}
            </span>
            <span className="thinking-text">is thinking</span>
            <span className="thinking-dots">
              <span>.</span><span>.</span><span>.</span>
            </span>
          </div>
        )}
      </div>

      {/* Agent Status Bar */}
      <div className="agent-status-bar">
        <div className={`agent-status ${thinking === "DECISION" ? "active" : ""}`}>
          <div className="status-icon">🧠</div>
          <div className="status-label">DECISION</div>
          <div className="status-role">Root Cause</div>
        </div>
        
        <div className="status-arrow">→</div>
        
        <div className={`agent-status ${thinking === "MEMORY" ? "active" : ""}`}>
          <div className="status-icon">💾</div>
          <div className="status-label">MEMORY</div>
          <div className="status-role">Historical Learning</div>
        </div>
        
        <div className="status-arrow">→</div>
        
        <div className={`agent-status ${thinking === "PREDICTOR" ? "active" : ""}`}>
          <div className="status-icon">🔮</div>
          <div className="status-label">PREDICTOR</div>
          <div className="status-role">Cascading Failures</div>
        </div>
        
        <div className="status-arrow">→</div>
        
        <div className={`agent-status ${thinking === "WRITER" ? "active" : ""}`}>
          <div className="status-icon">✍️</div>
          <div className="status-label">WRITER</div>
          <div className="status-role">Remediation Plan</div>
        </div>
        
        <div className="status-arrow">→</div>
        
        <div className={`agent-status ${thinking === "CRITIC" ? "active" : ""}`}>
          <div className="status-icon">⚖️</div>
          <div className="status-label">CRITIC</div>
          <div className="status-role">Safety Review</div>
        </div>
        
        <div className="status-arrow">→</div>
        
        <div className={`agent-status ${thinking === "CONSENSUS" ? "active" : ""}`}>
          <div className="status-icon">🗳️</div>
          <div className="status-label">CONSENSUS</div>
          <div className="status-role">Multi-Agent Vote</div>
        </div>
      </div>
    </div>
  );
}
