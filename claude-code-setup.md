# Claude Code Integration Guide

## Quick Setup

### 1. MCP Server Configuration

Add this to your Claude Code MCP servers configuration:

```json
{
  "mcpServers": {
    "neo4j": {
      "command": "/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe",
      "args": ["-m", "neo4j_mcp.server"],
      "cwd": "/mnt/c/Data/Code/neo4j_mcp",
      "env": {
        "NEO4J_URI": "neo4j://127.0.0.1:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

### 2. Environment Variables (Alternative)

Or create a `.env` file in the project directory:

```bash
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j
```

Then use simpler configuration:
```json
{
  "mcpServers": {
    "neo4j": {
      "command": "/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe",
      "args": ["-m", "neo4j_mcp.server"],
      "cwd": "/mnt/c/Data/Code/neo4j_mcp"
    }
  }
}
```

## Available Tools

Once configured, these tools will be available in Claude Code:

### neo4j_configure ⚙️
- **Purpose**: Configure Neo4j MCP server settings at runtime
- **Usage**: "Check Neo4j server status", "Disable Neo4j write operations"
- **Always Available**: This tool is always enabled for configuration management

### get_neo4j_schema
- **Purpose**: Get database schema information using standard Neo4j procedures
- **Usage**: "Show me the Neo4j database schema"
- **Requirements**: **None - uses plain Cypher queries only (no APOC)**
- **Provides**: Node labels, relationship types, counts, basic structure
- **Disable with**: `NEO4J_ENABLE_SCHEMA=false` or via `neo4j_configure`

### read_neo4j_cypher
- **Purpose**: Execute read-only Cypher queries using standard syntax
- **Usage**: "Run this Cypher query: MATCH (n:Person) RETURN n LIMIT 5"
- **Requirements**: **Standard Cypher only - no APOC procedures**
- **Parameters**: query (required), params (optional)
- **Disable with**: `NEO4J_ENABLE_READ=false` or via `neo4j_configure`

### write_neo4j_cypher
- **Purpose**: Execute write Cypher queries with transaction management
- **Usage**: "Create a new Person node with name 'Alice'"
- **Requirements**: **Standard Cypher only - CREATE, MERGE, SET, DELETE**
- **Parameters**: query (required), params (optional)
- **Returns**: Execution statistics
- **Disable with**: `NEO4J_ENABLE_WRITE=false` or via `neo4j_configure`

## 🎛️ Runtime Configuration (NEW!)

You can now change tool settings **directly from Claude Code** without editing JSON files!

### Quick Commands

**Check current status:**
> "Check my Neo4j server configuration"

**Disable write operations:**
> "Disable Neo4j write operations"

**Enable write operations:**
> "Enable Neo4j write operations"

**List available tools:**
> "Show me available Neo4j tools"

### Advanced Configuration Commands

You can also use the `neo4j_configure` tool directly:

- **Check Status**: `neo4j_configure` with `action: "status"`
- **Enable Tool**: `neo4j_configure` with `action: "enable"` and `tool: "write"`
- **Disable Tool**: `neo4j_configure` with `action: "disable"` and `tool: "write"`
- **List Tools**: `neo4j_configure` with `action: "list"`

### Example Claude Code Conversations

```
You: "Check my Neo4j server status"
Claude: [Shows current configuration with enabled/disabled tools]

You: "Disable Neo4j write operations for safety"
Claude: "[DISABLED] Write tool disabled - write_neo4j_cypher is no longer available"

You: "What Neo4j tools are available now?"
Claude: [Shows list with write tool disabled]

You: "Re-enable writes"
Claude: "[SUCCESS] Write tool enabled - write_neo4j_cypher is now available"
```

## Disabling Specific Tools

You can disable specific tools by setting environment variables:

### Method 1: Environment Variables in Configuration
```json
{
  "mcpServers": {
    "neo4j": {
      "command": "/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe",
      "args": ["-m", "neo4j_mcp.server"],
      "cwd": "/mnt/c/Data/Code/neo4j_mcp",
      "env": {
        "NEO4J_URI": "neo4j://127.0.0.1:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_ENABLE_WRITE": "false",
        "NEO4J_ENABLE_SCHEMA": "false"
      }
    }
  }
}
```

### Method 2: .env File
Create a `.env` file in the project directory:
```bash
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_ENABLE_WRITE=false
NEO4J_ENABLE_SCHEMA=false
```

### Common Use Cases

**Read-Only Mode** (disable write operations):
```bash
NEO4J_ENABLE_WRITE=false
```

**Schema-less Mode** (if APOC not available):
```bash
NEO4J_ENABLE_SCHEMA=false
```

**Query-Only Mode** (read queries only):
```bash
NEO4J_ENABLE_SCHEMA=false
NEO4J_ENABLE_WRITE=false
```

## Testing the Setup

1. **Test Server Installation**:
   ```bash
   /mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe -c "import neo4j_mcp; print('OK')"
   ```

2. **Test Server Execution**:
   ```bash
   cd /mnt/c/Data/Code/neo4j_mcp
   /mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe -m neo4j_mcp.server --help
   ```

3. **Test Mock Functionality**:
   ```bash
   /mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe test_mock_wsl.py
   ```

## Troubleshooting

### Fixed Issues (v1.0.1)
- ✅ **Async/Await Error**: Fixed "object NoneType can't be used in 'await' expression"
- ✅ **Connection Startup**: Server no longer requires Neo4j connection during startup
- ✅ **Driver Compatibility**: Updated to use synchronous Neo4j driver correctly
- ✅ **MCP Capabilities Error**: Fixed "Server.get_capabilities() got an unexpected keyword argument 'notification'"

### Connection Issues
- Ensure Neo4j is running on Windows
- Check that Neo4j accepts external connections (0.0.0.0:7687)
- Verify Windows firewall allows port 7687
- **Note**: Connection errors will only occur when tools are actually used

### Path Issues
- Use full path to Python executable in WSL
- Ensure working directory is set to project root
- Verify package installation with import test

### Authentication Issues
- Double-check Neo4j username/password
- Ensure user has required permissions
- Test connection with Neo4j Browser first

### Testing the Fix
```bash
# Test complete server functionality (should work without Neo4j)
/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe test_fixed_server.py

# Test connection (requires running Neo4j)
/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe test_fixed_connection.py
```

## Example Usage in Claude Code

Once configured, you can ask Claude Code:

- "What's the schema of my Neo4j database?"
- "Show me all Person nodes with their properties"
- "Create a new node with label Product and name 'Laptop'"
- "Find all relationships between User and Order nodes"
- "Run a Cypher query to find the most connected nodes"

The server will automatically handle WSL to Windows connectivity and provide formatted results.