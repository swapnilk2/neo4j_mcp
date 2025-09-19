# Example MCP Server Configurations

## 1. Full Access (Default)
All tools enabled - schema, read, and write operations.

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
        "NEO4J_PASSWORD": "password"
      }
    }
  }
}
```

## 2. Read-Only Mode
Perfect for production databases where you don't want write access.

```json
{
  "mcpServers": {
    "neo4j-readonly": {
      "command": "/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe",
      "args": ["-m", "neo4j_mcp.server"],
      "cwd": "/mnt/c/Data/Code/neo4j_mcp",
      "env": {
        "NEO4J_URI": "neo4j://127.0.0.1:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_ENABLE_WRITE": "false"
      }
    }
  }
}
```

## 3. Query-Only Mode
Only read queries, no schema introspection (useful without APOC).

```json
{
  "mcpServers": {
    "neo4j-query": {
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

## 4. Schema-Only Mode
Just for exploring database structure.

```json
{
  "mcpServers": {
    "neo4j-schema": {
      "command": "/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe",
      "args": ["-m", "neo4j_mcp.server"],
      "cwd": "/mnt/c/Data/Code/neo4j_mcp",
      "env": {
        "NEO4J_URI": "neo4j://127.0.0.1:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_ENABLE_READ": "false",
        "NEO4J_ENABLE_WRITE": "false"
      }
    }
  }
}
```

## 5. Multiple Server Configurations
You can have multiple MCP servers for different purposes:

```json
{
  "mcpServers": {
    "neo4j-full": {
      "command": "/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe",
      "args": ["-m", "neo4j_mcp.server"],
      "cwd": "/mnt/c/Data/Code/neo4j_mcp",
      "env": {
        "NEO4J_URI": "neo4j://127.0.0.1:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password"
      }
    },
    "neo4j-readonly": {
      "command": "/mnt/c/Users/Swapnil/anaconda3/envs/nlp_py310/python.exe",
      "args": ["-m", "neo4j_mcp.server"],
      "cwd": "/mnt/c/Data/Code/neo4j_mcp",
      "env": {
        "NEO4J_URI": "neo4j://prod-server:7687",
        "NEO4J_USER": "readonly_user",
        "NEO4J_PASSWORD": "readonly_pass",
        "NEO4J_ENABLE_WRITE": "false"
      }
    }
  }
}
```

This gives you both full access to local dev database and read-only access to production!