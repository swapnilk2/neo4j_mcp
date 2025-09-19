# Neo4j MCP Server

A comprehensive Model Context Protocol (MCP) server for Neo4j database integration with cross-platform support and zero APOC dependencies.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Neo4j](https://img.shields.io/badge/Neo4j-4.x%2F5.x-green.svg)](https://neo4j.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Features

- **🔌 Universal Neo4j Integration**: Works with Community, Enterprise, Cloud, and Docker Neo4j instances
- **🌍 Cross-Platform Support**: Native support for Windows, macOS, Linux, and WSL environments
- **❌ Zero APOC Dependencies**: Uses only standard Neo4j procedures - no plugin installation required
- **🎛️ Runtime Configuration**: Dynamic tool management directly from Claude Code
- **🔒 Secure Connection Management**: Smart connection handling with fallback support
- **📊 Complete Schema Introspection**: Full database structure analysis
- **⚡ High Performance**: Async operations with optimized query execution
- **🛠️ Developer Friendly**: Comprehensive error handling and debugging support

## 📋 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **Neo4j Database** (Version 4.x or 5.x)
- **Claude Code** (for MCP integration)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/neo4j_mcp.git
cd neo4j_mcp

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Configuration

1. **Set up Neo4j connection** (choose one method):

   **Option A: Environment Variables**
   ```bash
   export NEO4J_URI="neo4j://localhost:7687"
   export NEO4J_USER="neo4j"
   export NEO4J_PASSWORD="your-password"
   export NEO4J_DATABASE="neo4j"
   ```

   **Option B: .env File**
   ```bash
   # Create .env file in project directory
   NEO4J_URI=neo4j://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your-password
   NEO4J_DATABASE=neo4j
   ```

2. **Configure Claude Code** - Add to your MCP servers configuration:

   ```json
   {
     "mcpServers": {
       "neo4j": {
         "command": "python",
         "args": ["-m", "neo4j_mcp.server"],
         "cwd": "/path/to/neo4j_mcp",
         "env": {
           "NEO4J_URI": "neo4j://localhost:7687",
           "NEO4J_USER": "neo4j",
           "NEO4J_PASSWORD": "your-password"
         }
       }
     }
   }
   ```

3. **Test the connection**:
   ```bash
   python -m neo4j_mcp.server --help
   ```

## 🛠️ Available Tools

### 🔍 `get_neo4j_schema`
**Get complete database schema using standard Neo4j procedures only**
- **No APOC required** - uses plain Cypher queries
- Lists all node labels and relationship types
- Provides node counts and schema visualization
- Works with any Neo4j database

```
Usage in Claude Code: "Show me the Neo4j database schema"
```

### 📖 `read_neo4j_cypher`
**Execute read-only Cypher queries**
- Standard Cypher syntax support
- Parameterized queries
- JSON-serialized results
- No APOC procedures required

```
Usage in Claude Code: "Run this query: MATCH (n:Person) RETURN n LIMIT 5"
```

### ✏️ `write_neo4j_cypher`
**Execute write Cypher queries with transaction management**
- CREATE, MERGE, SET, DELETE operations
- Transaction statistics
- Error handling and rollback
- Standard Cypher only

```
Usage in Claude Code: "Create a Person node with name 'Alice' and age 30"
```

### ⚙️ `neo4j_configure`
**Runtime server configuration (always available)**
- Enable/disable tools dynamically
- Check server status
- No database connection required

```
Usage in Claude Code:
- "Check Neo4j server status"
- "Disable Neo4j write operations"
- "Enable all Neo4j tools"
```

### WSL to Windows Setup

For WSL users connecting to Windows Neo4j:

1. **Configure Neo4j to accept external connections:**
   ```
   # In neo4j.conf
   dbms.default_listen_address=0.0.0.0
   dbms.connector.bolt.listen_address=0.0.0.0:7687
   ```

2. **Configure Windows Firewall:**
   - Allow inbound connections on port 7687
   - Or create specific rule for Neo4j

3. **Test connectivity:**
   ```bash
   python test_connectivity.py
   ```

## Usage

### Running the Server

```bash
# Direct execution
python -m neo4j_mcp.server

# Or using the console script
neo4j-mcp-server
```

### Using with MCP Clients

Configure your MCP client to connect to this server via stdio.

Example configuration:
```json
{
  "mcpServers": {
    "neo4j": {
      "command": "python",
      "args": ["-m", "neo4j_mcp.server"],
      "env": {
        "NEO4J_URI": "neo4j://127.0.0.1:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password"
      }
    }
  }
}
```

## MCP Tools Reference

### get_neo4j_schema

Retrieves comprehensive schema information from the Neo4j database.

**Requirements:** APOC plugin must be installed and enabled.

**Parameters:** None

**Returns:** Formatted text with:
- Node labels and their properties
- Relationship types and their properties
- Property types and constraints

### read_neo4j_cypher

Executes read-only Cypher queries.

**Parameters:**
- `query` (string, required): The Cypher query to execute
- `params` (object, optional): Parameters for the query

**Returns:** Formatted query results with:
- Query text and parameters
- Number of records returned
- JSON-formatted results (limited to first 100 records for large datasets)

**Example:**
```cypher
MATCH (n:Person) RETURN n.name, n.age LIMIT 10
```

### write_neo4j_cypher

Executes write Cypher queries with transaction management.

**Parameters:**
- `query` (string, required): The Cypher query to execute
- `params` (object, optional): Parameters for the query

**Returns:** Execution summary with:
- Query text and parameters
- Database change counters (nodes/relationships created/deleted, properties set, etc.)
- Execution timing information

**Example:**
```cypher
CREATE (p:Person {name: $name, age: $age})
```

## Testing

### Unit Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=neo4j_mcp --cov-report=html
```

### Connectivity Testing
```bash
# Test actual Neo4j connectivity
python test_connectivity.py

# Test mocked functionality
python test_mock_wsl.py
```

## Troubleshooting

### Common Issues

1. **Connection Refused (WSL to Windows)**
   - Ensure Neo4j is configured to accept external connections
   - Check Windows firewall settings
   - Verify Neo4j is running and accessible

2. **Schema Tool Fails**
   - Install and enable APOC plugin in Neo4j
   - Verify APOC procedures are available: `CALL apoc.help("meta")`

3. **Authentication Errors**
   - Verify NEO4J_USER and NEO4J_PASSWORD are correct
   - Check if user has required permissions

### Connection Fallback

The server automatically tries multiple connection strategies:

1. Original URI (e.g., `neo4j://127.0.0.1:7687`)
2. Windows host IP (detected automatically in WSL)
3. Additional configured IPs

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Architecture

### Components

- **Config Management** (`config.py`) - Environment detection and configuration
- **Connection Manager** (`connection.py`) - Neo4j connectivity with fallback
- **MCP Tools** (`tools/`) - Individual MCP tool implementations
- **Server** (`server.py`) - Main MCP server implementation

### Cross-Platform Strategy

1. **Environment Detection** - Checks `/proc/version` for WSL indicators
2. **Network Discovery** - Finds Windows host IP from routing table and resolv.conf
3. **Connection Fallback** - Attempts multiple URIs in sequence
4. **Error Recovery** - Provides detailed error messages and troubleshooting hints

## Development

### Project Structure
```
neo4j_mcp/
├── src/neo4j_mcp/          # Main package
│   ├── __init__.py
│   ├── server.py           # MCP server implementation
│   ├── config.py           # Configuration management
│   ├── connection.py       # Neo4j connection handling
│   └── tools/              # MCP tools
│       ├── __init__.py
│       ├── schema.py       # Schema introspection
│       ├── read.py         # Read query execution
│       └── write.py        # Write query execution
├── tests/                  # Test suite
├── test_connectivity.py   # Manual connectivity testing
├── test_mock_wsl.py       # Mocked functionality testing
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.