export default function MultiAgentDebate({ debate }) {
  if (!debate) return null;

  return (
    <div style={{
      background: "#111613",
      border: "2px solid #fbbf24",
      borderRadius: 6,
      padding: 16,
      marginBottom: 16
    }}>
      <div style={{
        color: "#fbbf24",
        fontSize: 10,
        textTransform: "uppercase",
        marginBottom: 12,
        letterSpacing: "0.1em"
      }}>
        ⚖️ Multi-Agent Debate
      </div>
      
      {debate.concerns && (
        <div style={{
          background: "#1a0f0f",
          border: "1px solid #ff4d6d33",
          borderRadius: 4,
          padding: 10,
          marginBottom: 12
        }}>
          <div style={{ fontSize: 9, color: "#ff4d6d", marginBottom: 6, textTransform: "uppercase" }}>
            Critic Concerns:
          </div>
          {debate.concerns.map((concern, i) => (
            <div key={i} style={{ fontSize: 10, color: "#f87171", marginBottom: 4 }}>
              • {concern}
            </div>
          ))}
        </div>
      )}
      
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 12
      }}>
        <div>
          <div style={{
            fontSize: 9,
            color: "#4a6358",
            marginBottom: 6,
            textTransform: "uppercase"
          }}>
            PLAN A (Writer Agent)
          </div>
          {debate.plan_a.map((cmd, i) => (
            <div
              key={i}
              style={{
                background: "#080c0b",
                padding: "6px 8px",
                fontSize: 10,
                marginBottom: 3,
                borderRadius: 3,
                fontFamily: "monospace",
                color: "#94a3b8"
              }}
            >
              $ {cmd}
            </div>
          ))}
        </div>
        
        <div>
          <div style={{
            fontSize: 9,
            color: "#00e87a",
            marginBottom: 6,
            textTransform: "uppercase"
          }}>
            PLAN B (Critic Agent) ✓ RECOMMENDED
          </div>
          {debate.plan_b.map((cmd, i) => (
            <div
              key={i}
              style={{
                background: "#0f2a1a",
                border: "1px solid #00e87a",
                padding: "6px 8px",
                fontSize: 10,
                marginBottom: 3,
                borderRadius: 3,
                fontFamily: "monospace",
                color: "#6ee7b7"
              }}
            >
              $ {cmd}
            </div>
          ))}
        </div>
      </div>
      
      {debate.reason && (
        <div style={{
          marginTop: 10,
          fontSize: 10,
          color: "#00e87a",
          fontStyle: "italic"
        }}>
          → {debate.reason}
        </div>
      )}
    </div>
  );
}
