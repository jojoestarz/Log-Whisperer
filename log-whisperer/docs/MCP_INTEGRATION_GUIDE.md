# MCP Tools Integration for Log Whisperer

## Overview

MCP (Model Context Protocol) tools can significantly enhance Log Whisperer by providing:
- **Standardized tool interfaces** for infrastructure operations
- **Remote execution capabilities** via MCP servers
- **Tool discovery** and automatic integration
- **Safety validation** through MCP server policies
- **Audit logging** at the protocol level

## Why MCP Tools for Log Whisperer?

### Current State
Log Whisperer uses direct subprocess execution:
```python
subprocess.run(["git", "revert", commit, "--no-commit"])
subprocess.run(["kubectl", "apply", "-f", manifest])
```

### With MCP Tools
```python
# Tools exposed via MCP servers
await mcp_client.call_tool("git_revert", {"commit": commit})
await mcp_client.call_tool("kubectl_apply", {"manifest": manifest})
```

### Benefits

1. **Separation of Concerns**
   - AI agents focus on decision-making
   - MCP servers handle execution
   - Clear security boundaries

2. **Remote Execution**
   - Execute on different machines
   - Access to privileged environments
   - No local credentials needed

3. **Standardized Interface**
   - Consistent tool signatures
   - Automatic validation
   - Built-in error handling

4. **Safety & Auditing**
   - MCP server policies
   - Centralized logging
   - Approval workflows

5. **Tool Discovery**
   - Agents discover available tools
   - Dynamic capability detection
   - Version management

## MCP Server Architecture for Log Whisperer

```
┌─────────────────────────────────────────────────────────┐
│                   Log Whisperer                         │
│                                                         │
│  ┌──────────────┐      ┌──────────────┐               │
│  │ Council      │      │ Writer       │               │
│  │ Agent        │──────│ Agent        │               │
│  └──────────────┘      └──────────────┘               │
│         │                      │                       │
│         └──────────┬───────────┘                       │
│                    │                                   │
│              ┌─────▼─────┐                            │
│              │ MCP Client │                            │
│              └─────┬─────┘                            │
└────────────────────┼──────────────────────────────────┘
                     │ MCP Protocol
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
   │ Git    │  │ K8s    │  │ Argo   │
   │ MCP    │  │ MCP    │  │ MCP    │
   │ Server │  │ Server │  │ Server │
   └────┬───┘  └────┬───┘  └────┬───┘
        │           │           │
   ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
   │ Git    │  │kubectl │  │argocd  │
   │ Repos  │  │ API    │  │ API    │
   └────────┘  └────────┘  └────────┘
```

## MCP Servers for Log Whisperer

### 1. Git Operations MCP Server

**Purpose:** Manage git operations for config rollbacks

**Tools:**
- `git_revert` - Revert commits
- `git_status` - Check repository status
- `git_log` - View commit history
- `git_diff` - Show changes

**Configuration:**
```json
{
  "mcpServers": {
    "git-ops": {
      "command": "uvx",
      "args": ["log-whisperer-git-mcp"],
      "env": {
        "GIT_REPOS_PATH": "/repos",
        "ALLOWED_REPOS": "infra-config,bgp-config"
      }
    }
  }
}
```

### 2. Kubernetes MCP Server

**Purpose:** Execute kubectl operations

**Tools:**
- `kubectl_apply` - Apply manifests
- `kubectl_scale` - Scale deployments
- `kubectl_rollout` - Manage rollouts
- `kubectl_get` - Get resource status

**Configuration:**
```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "uvx",
      "args": ["kubernetes-mcp-server"],
      "env": {
        "KUBECONFIG": "/path/to/kubeconfig",
        "ALLOWED_NAMESPACES": "prod,staging"
      }
    }
  }
}
```

### 3. Argo CD MCP Server

**Purpose:** Manage Argo CD applications

**Tools:**
- `argo_sync` - Sync applications
- `argo_rollback` - Rollback applications
- `argo_get` - Get app status

**Configuration:**
```json
{
  "mcpServers": {
    "argocd": {
      "command": "uvx",
      "args": ["argocd-mcp-server"],
      "env": {
        "ARGOCD_SERVER": "argocd.example.com",
        "ARGOCD_AUTH_TOKEN": "${ARGOCD_TOKEN}"
      }
    }
  }
}
```

### 4. Observability MCP Server

**Purpose:** Query logs and metrics

**Tools:**
- `loki_query` - Query Loki logs
- `prometheus_query` - Query Prometheus metrics
- `grafana_dashboard` - Get dashboard data

**Configuration:**
```json
{
  "mcpServers": {
    "observability": {
      "command": "uvx",
      "args": ["observability-mcp-server"],
      "env": {
        "LOKI_URL": "http://loki:3100",
        "PROMETHEUS_URL": "http://prometheus:9090"
      }
    }
  }
}
```

## Implementation

### 1. MCP Client Integration

```python
# execution/mcp_executor.py
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from models import CLICommand
import structlog

logger = structlog.get_logger()


class MCPExecutor:
    """Execute commands via MCP servers."""
    
    def __init__(self):
        self.sessions = {}
        self.tool_mapping = {
            "git_revert": "git-ops",
            "kubectl_apply": "kubernetes",
            "kubectl_scale": "kubernetes",
            "argo_sync": "argocd",
            "service_restart": "kubernetes"
        }
    
    async def connect_server(self, server_name: str, config: dict):
        """Connect to an MCP server."""
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=config.get("env", {})
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.sessions[server_name] = session
                
                # List available tools
                tools = await session.list_tools()
                logger.info("mcp.connected", 
                           server=server_name,
                           tools=[t.name for t in tools.tools])
    
    async def execute(self, command: CLICommand) -> dict:
        """Execute command via appropriate MCP server."""
        server_name = self.tool_mapping.get(command.tool)
        
        if not server_name:
            return {
                "success": False,
                "error": f"No MCP server for tool: {command.tool}"
            }
        
        session = self.sessions.get(server_name)
        if not session:
            return {
                "success": False,
                "error": f"MCP server not connected: {server_name}"
            }
        
        try:
            # Call tool via MCP
            result = await session.call_tool(
                command.tool,
                arguments=command.args
            )
            
            logger.info("mcp.tool_called",
                       tool=command.tool,
                       server=server_name)
            
            return {
                "success": True,
                "mode": "mcp",
                "server": server_name,
                "output": str(result.content),
                "executed": True
            }
            
        except Exception as e:
            logger.error("mcp.tool_failed",
                        tool=command.tool,
                        error=str(e))
            return {
                "success": False,
                "error": str(e),
                "executed": False
            }
```

### 2. Hybrid Executor (MCP + Subprocess)

```python
# execution/hybrid_executor.py
from execution.executor import CommandExecutor, ExecutionMode
from execution.mcp_executor import MCPExecutor
from models import CLICommand


class HybridExecutor:
    """Execute via MCP when available, fallback to subprocess."""
    
    def __init__(self, mode: ExecutionMode, use_mcp: bool = True):
        self.subprocess_executor = CommandExecutor(mode=mode)
        self.mcp_executor = MCPExecutor() if use_mcp else None
        self.prefer_mcp = use_mcp
    
    async def execute(self, command: CLICommand) -> dict:
        """Execute command, preferring MCP if available."""
        
        # Try MCP first if enabled
        if self.prefer_mcp and self.mcp_executor:
            result = await self.mcp_executor.execute(command)
            if result["success"] or "not connected" not in result.get("error", ""):
                return result
        
        # Fallback to subprocess
        return self.subprocess_executor.execute(command)
```

### 3. Agent Integration

```python
# agents/writer_agent.py (enhanced)
async def generate_remediation_plan(fault: FaultReport) -> RemediationPlan:
    """Generate plan with MCP tool awareness."""
    
    # Discover available MCP tools
    available_tools = await discover_mcp_tools()
    
    # Include tool availability in prompt
    prompt = f"""
    Available tools via MCP: {available_tools}
    
    Generate remediation plan for: {fault.root_cause}
    """
    
    # Generate plan as before
    plan = await generate_plan(fault)
    
    return plan
```

## Use Cases

### Use Case 1: Remote Execution

**Scenario:** Log Whisperer runs in a monitoring cluster, but needs to execute commands in production cluster.

**Solution:**
```
Log Whisperer (monitoring) 
    ↓ MCP Protocol
Kubernetes MCP Server (production)
    ↓ kubectl
Production K8s Cluster
```

**Benefits:**
- No direct cluster access needed
- MCP server handles authentication
- Centralized audit logging

### Use Case 2: Multi-Cloud Operations

**Scenario:** Infrastructure spans AWS, GCP, and on-prem.

**Solution:**
```json
{
  "mcpServers": {
    "aws-ops": {...},
    "gcp-ops": {...},
    "onprem-ops": {...}
  }
}
```

**Benefits:**
- Unified interface
- Cloud-agnostic agents
- Consistent error handling

### Use Case 3: Approval Workflows

**Scenario:** High-risk operations require approval.

**Solution:**
```python
# MCP server with approval gate
async def git_revert(commit: str):
    # Request approval
    approval = await request_approval(
        operation="git_revert",
        commit=commit,
        risk="high"
    )
    
    if not approval.granted:
        raise PermissionError("Approval denied")
    
    # Execute
    return execute_git_revert(commit)
```

**Benefits:**
- Approval at execution layer
- Audit trail
- Policy enforcement

### Use Case 4: Tool Discovery

**Scenario:** Different environments have different capabilities.

**Solution:**
```python
# Agent discovers available tools
tools = await mcp_client.list_tools()

# Generates plan based on available tools
if "argo_sync" in tools:
    use_argocd_workflow()
else:
    use_kubectl_workflow()
```

**Benefits:**
- Environment-aware
- Graceful degradation
- Flexible deployment

## Migration Path

### Phase 1: Parallel Execution
```python
# Execute via both methods, compare results
subprocess_result = subprocess_executor.execute(cmd)
mcp_result = await mcp_executor.execute(cmd)

# Log differences
if subprocess_result != mcp_result:
    logger.warning("execution.mismatch")
```

### Phase 2: MCP Primary
```python
# Try MCP first, fallback to subprocess
try:
    return await mcp_executor.execute(cmd)
except MCPError:
    return subprocess_executor.execute(cmd)
```

### Phase 3: MCP Only
```python
# All execution via MCP
return await mcp_executor.execute(cmd)
```

## Configuration

### Log Whisperer MCP Config

```json
{
  "mcpServers": {
    "git-ops": {
      "command": "uvx",
      "args": ["log-whisperer-git-mcp"],
      "env": {
        "GIT_REPOS_PATH": "/repos",
        "EXECUTION_MODE": "safe"
      },
      "autoApprove": ["git_status", "git_log"]
    },
    "kubernetes": {
      "command": "uvx",
      "args": ["kubernetes-mcp-server"],
      "env": {
        "KUBECONFIG": "/path/to/kubeconfig"
      },
      "autoApprove": ["kubectl_get"]
    },
    "argocd": {
      "command": "uvx",
      "args": ["argocd-mcp-server"],
      "env": {
        "ARGOCD_SERVER": "argocd.example.com"
      },
      "autoApprove": []
    }
  }
}
```

### Environment Variables

```bash
# .env
USE_MCP=true                    # Enable MCP execution
MCP_CONFIG_PATH=mcp.json        # MCP configuration file
MCP_FALLBACK=true               # Fallback to subprocess if MCP fails
```

## Benefits Summary

| Aspect | Subprocess | MCP Tools |
|--------|-----------|-----------|
| **Execution** | Local only | Local or remote |
| **Authentication** | Local credentials | MCP server handles |
| **Audit** | Application logs | Protocol-level |
| **Discovery** | Hardcoded | Dynamic |
| **Approval** | Application layer | Server layer |
| **Multi-cloud** | Complex | Unified |
| **Safety** | Application logic | Server policies |

## Next Steps

### 1. Create MCP Servers

```bash
# Create git-ops MCP server
mkdir log-whisperer-git-mcp
cd log-whisperer-git-mcp
# Implement MCP server for git operations
```

### 2. Implement MCP Client

```bash
# Add MCP client to Log Whisperer
pip install mcp
# Implement MCPExecutor class
```

### 3. Configure MCP Servers

```bash
# Add to mcp.json
# Configure server endpoints
# Set up authentication
```

### 4. Test Integration

```bash
# Test MCP tool calls
python test_mcp_integration.py
```

### 5. Gradual Rollout

```bash
# Start with read-only tools
# Add write operations
# Enable in production
```

## Conclusion

MCP tools would provide Log Whisperer with:
- ✅ Standardized tool interfaces
- ✅ Remote execution capabilities
- ✅ Better security boundaries
- ✅ Centralized audit logging
- ✅ Dynamic tool discovery
- ✅ Multi-cloud support

The hybrid approach (MCP + subprocess fallback) provides the best of both worlds during migration.
