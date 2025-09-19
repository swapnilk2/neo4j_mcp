# Project Details - Neo4j MCP Server

## Project Overview

**Project Name:** neo4j_mcp
**Version:** 1.0.0
**Description:** Model Context Protocol (MCP) server for Neo4j database connectivity with cross-platform support
**Created:** September 18, 2025
**Technology Stack:** Python 3.8+, MCP, Neo4j, Pydantic, Rich

## Design Details

### Architecture

The Neo4j MCP Server follows a modular architecture designed for cross-platform connectivity and robust error handling:

1. **Configuration Layer** (`config.py`)
   - Environment variable management
   - WSL environment detection
   - Windows host IP discovery
   - Connection URI generation with fallback strategies

2. **Connection Layer** (`connection.py`)
   - Neo4j driver management
   - Connection pooling and session handling
   - Multi-URI connection attempts with automatic fallback
   - Transaction management for read/write operations

3. **Tools Layer** (`tools/`)
   - Schema introspection tool (APOC-based)
   - Read query execution with result formatting
   - Write query execution with statistics reporting
   - Input validation and error handling

4. **Server Layer** (`server.py`)
   - MCP protocol implementation
   - Tool registration and dispatching
   - Async/await pattern for concurrent operations
   - Graceful startup and shutdown

### Cross-Platform Strategy

**Problem:** WSL clients need to connect to Neo4j running on Windows host

**Solution Components:**
1. **Environment Detection** - Automatic WSL detection via `/proc/version`
2. **Network Discovery** - Windows host IP from routing table and DNS resolver
3. **Connection Fallback** - Sequential URI attempts (localhost → Windows host IP)
4. **Error Recovery** - Detailed diagnostics and troubleshooting guidance

### Logging Framework

**Decision:** Rich logger (as per user preference)
**Implementation:** Configured in server.py with structured logging
**Levels:** INFO (default), DEBUG (troubleshooting), WARNING (fallback scenarios), ERROR (failures)

## Directory Structure

```
neo4j_mcp/
├── src/                          # Source code directory
│   └── neo4j_mcp/               # Main package
│       ├── __init__.py          # Package initialization and metadata
│       ├── server.py            # MCP server implementation (main entry point)
│       ├── config.py            # Configuration management and environment detection
│       ├── connection.py        # Neo4j connection handling with fallback logic
│       └── tools/               # MCP tool implementations
│           ├── __init__.py      # Tools package initialization
│           ├── schema.py        # Schema introspection tool (get_neo4j_schema)
│           ├── read.py          # Read query tool (read_neo4j_cypher)
│           └── write.py         # Write query tool (write_neo4j_cypher)
├── tests/                       # Test suite
│   ├── __init__.py             # Test package initialization
│   └── test_neo4j_mcp.py       # Comprehensive unit and integration tests
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup and installation configuration
├── pytest.ini                  # Test configuration
├── test_connectivity.py        # Manual connectivity testing script
├── test_mock_wsl.py            # Mocked functionality testing script
├── README.md                   # Comprehensive user documentation
├── PLAN_NEO4J_MCP.md           # Implementation planning document
├── PROJECT_DETAILS_NEO4J_MCP.md # This file - detailed project information
└── CHANGE_LOG_NEO4J_MCP.md     # Change history and version tracking
```

### File Descriptions

**Core Implementation Files:**
- `server.py` - Main MCP server with tool registration and request handling
- `config.py` - Environment detection, configuration management, and URI generation
- `connection.py` - Neo4j driver wrapper with connection pooling and fallback logic
- `tools/schema.py` - Database schema introspection using APOC procedures
- `tools/read.py` - Read-only query execution with result formatting
- `tools/write.py` - Write query execution with transaction management and statistics

**Configuration Files:**
- `requirements.txt` - Python package dependencies (MCP, Neo4j driver, Pydantic, Rich)
- `setup.py` - Package metadata, entry points, and installation configuration
- `pytest.ini` - Test runner configuration with coverage and async support

**Testing Files:**
- `test_neo4j_mcp.py` - Unit tests for all components with mocking
- `test_connectivity.py` - Real-world connectivity testing script
- `test_mock_wsl.py` - Functionality testing with WSL environment simulation

**Documentation Files:**
- `README.md` - User guide with installation, configuration, and usage instructions
- `PLAN_NEO4J_MCP.md` - Implementation plan and architectural decisions
- `PROJECT_DETAILS_NEO4J_MCP.md` - This file with comprehensive project details

## How to Use

### Installation
```bash
# Clone repository and install in development mode
git clone <repository-url>
cd neo4j_mcp
pip install -e .
```

### Configuration
Set environment variables in `.env` file or shell:
```bash
NEO4J_URI="neo4j://127.0.0.1:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"
NEO4J_DATABASE="neo4j"
```

### Running the Server
```bash
# Direct execution
python -m neo4j_mcp.server

# Console script (after installation)
neo4j-mcp-server
```

### MCP Client Configuration
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

## Configuration Details

### Environment Variables
- `NEO4J_URI` - Neo4j connection URI (default: neo4j://127.0.0.1:7687)
- `NEO4J_USER` - Database username (default: neo4j)
- `NEO4J_PASSWORD` - Database password (default: password)
- `NEO4J_DATABASE` - Target database (default: neo4j)
- `NEO4J_TIMEOUT` - Connection timeout in seconds (default: 30)
- `NEO4J_RETRIES` - Maximum connection retry attempts (default: 3)

### WSL Specific Configuration
The server automatically detects WSL environment and configures:
- Windows host IP discovery from routing table
- Connection URI fallback from localhost to Windows host
- Enhanced error messages for cross-platform connectivity issues

### Neo4j Configuration for WSL
```
# In neo4j.conf for WSL access
dbms.default_listen_address=0.0.0.0
dbms.connector.bolt.listen_address=0.0.0.0:7687
```

## How to Test

### Unit Testing
```bash
# Run all tests with coverage
pytest tests/ -v --cov=neo4j_mcp --cov-report=html

# Run specific test categories
pytest tests/test_neo4j_mcp.py::TestNeo4jConfig -v
pytest tests/test_neo4j_mcp.py::TestNeo4jConnectionManager -v
pytest tests/test_neo4j_mcp.py::TestNeo4jTools -v
```

### Connectivity Testing
```bash
# Test real Neo4j connectivity
python test_connectivity.py

# Test functionality with mocked components
python test_mock_wsl.py
```

### Manual Testing
1. Start Neo4j database
2. Configure environment variables
3. Run server: `python -m neo4j_mcp.server`
4. Test with MCP client or direct tool calls

## Dependencies

### Core Dependencies
- `mcp>=1.0.0` - Model Context Protocol implementation
- `neo4j>=5.15.0` - Official Neo4j Python driver
- `pydantic>=2.0.0` - Configuration validation and management
- `python-dotenv>=1.0.0` - Environment variable loading
- `rich>=13.0.0` - Enhanced logging and formatting

### Development Dependencies
- `pytest>=7.0.0` - Test framework
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-cov>=4.0.0` - Coverage reporting
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Code linting
- `mypy>=1.0.0` - Type checking

## Performance Considerations

- **Connection Pooling** - Neo4j driver handles connection pooling automatically
- **Async Operations** - All database operations use async/await for non-blocking execution
- **Query Optimization** - Large result sets are limited and formatted for readability
- **Memory Management** - Sessions are properly closed and resources cleaned up
- **Error Recovery** - Failed connections trigger immediate fallback attempts

## Security Considerations

- **Credential Management** - Passwords stored in environment variables, not code
- **Input Validation** - All Cypher queries and parameters validated before execution
- **Query Classification** - Read/write operations separated with appropriate transaction handling
- **Error Disclosure** - Detailed errors logged but sanitized for client responses
- **Connection Security** - Supports encrypted connections when configured in Neo4j

## Future Enhancements

1. **Authentication Methods** - Support for OAuth2, Kerberos, and certificate-based auth
2. **Connection Pooling** - Custom connection pool configuration options
3. **Query Caching** - Result caching for frequently executed read queries
4. **Metrics Collection** - Performance monitoring and usage statistics
5. **Multi-Database Support** - Enhanced support for Neo4j 4.0+ multi-database features
6. **Streaming Results** - Support for streaming large result sets
7. **Query Explain Plans** - Tool for query performance analysis