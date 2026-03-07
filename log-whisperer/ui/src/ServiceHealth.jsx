import { useState, useEffect } from "react";

const statusColor = {
  healthy: "#34d399",
  degraded: "#fbbf24",
  critical: "#ff4d6d",
  down: "#7f1d1d",
  recovering: "#60a5fa"
};

const statusIcon = {
  healthy: "✓",
  degraded: "⚠",
  critical: "✗",
  down: "●",
  recovering: "↻"
};

export default function ServiceHealth({ services, visible }) {
  if (!services || !visible) return null;

  return (
    <div style={{
      background: "#111613",
      border: "1px solid #1e2825",
      borderRadius: 6,
      padding: 16,
      marginBottom: 16
    }}>
      <div style={{
        color: "#94a3b8",
        fontSize: 10,
        textTransform: "uppercase",
        marginBottom: 10,
        letterSpacing: "0.1em"
      }}>
        🏥 Service Health
      </div>
      {Object.entries(services).map(([name, data]) => (
        <div
          key={name}
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "8px 0",
            borderBottom: "1px solid #1e2825"
          }}
        >
          <span style={{ fontSize: 11, fontFamily: "monospace" }}>
            {name}
          </span>
          <span
            style={{
              fontSize: 11,
              color: statusColor[data.status] || "#94a3b8",
              fontWeight: "bold",
              fontFamily: "monospace"
            }}
          >
            {statusIcon[data.status]} {data.status.toUpperCase()}
          </span>
        </div>
      ))}
    </div>
  );
}
