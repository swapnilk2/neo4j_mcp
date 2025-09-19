# Platform-Specific Setup Guide

This guide provides detailed setup instructions for Neo4j MCP server across different platforms and environments.

## 🪟 Windows Setup

### Prerequisites
- Python 3.8+ installed
- Neo4j Desktop or Server installed
- Claude Code installed

### Installation Steps

1. **Install Neo4j MCP Server**:
   ```cmd
   git clone https://github.com/your-username/neo4j_mcp.git
   cd neo4j_mcp
   pip install -r requirements.txt
   pip install -e .
   ```

2. **Configure Neo4j Database**:
   ```
   # In Neo4j Desktop, ensure database is running
   # Default connection: neo4j://localhost:7687
   ```

3. **Claude Code Configuration**:
   ```json
   {
     "mcpServers": {
       "neo4j": {
         "command": "python.exe",
         "args": ["-m", "neo4j_mcp.server"],
         "cwd": "C:\\path\\to\\neo4j_mcp",
         "env": {
           "NEO4J_URI": "neo4j://localhost:7687",
           "NEO4J_USER": "neo4j",
           "NEO4J_PASSWORD": "your-password",
           "NEO4J_DATABASE": "neo4j"
         }
       }
     }
   }
   ```

### Testing
```cmd
# Test package installation
python -c "import neo4j_mcp; print('Package installed successfully')"

# Test server startup
python -m neo4j_mcp.server --help

# Test with mock data (no Neo4j required)
set NEO4J_MOCK=true
python -m neo4j_mcp.server
```

### Common Windows Issues
- **Python Path**: Use full path to python.exe if not in PATH
- **Firewall**: Windows Defender may block connections
- **Permissions**: Run as administrator if installation fails

---

## 🍎 macOS Setup

### Prerequisites
- Python 3.8+ (use Homebrew: `brew install python`)
- Neo4j installed (via Homebrew or Neo4j Desktop)
- Claude Code installed

### Installation Steps

1. **Install Neo4j MCP Server**:
   ```bash
   git clone https://github.com/your-username/neo4j_mcp.git
   cd neo4j_mcp
   pip3 install -r requirements.txt
   pip3 install -e .
   ```

2. **Configure Neo4j Database**:
   ```bash
   # Using Homebrew Neo4j
   brew install neo4j
   neo4j start

   # Or use Neo4j Desktop
   # Download from https://neo4j.com/download/
   ```

3. **Claude Code Configuration**:
   ```json
   {
     "mcpServers": {
       "neo4j": {
         "command": "/usr/local/bin/python3",
         "args": ["-m", "neo4j_mcp.server"],
         "cwd": "/path/to/neo4j_mcp",
         "env": {
           "NEO4J_URI": "neo4j://localhost:7687",
           "NEO4J_USER": "neo4j",
           "NEO4J_PASSWORD": "your-password",
           "NEO4J_DATABASE": "neo4j"
         }
       }
     }
   }
   ```

### Testing
```bash
# Test package installation
python3 -c "import neo4j_mcp; print('Package installed successfully')"

# Test server startup
python3 -m neo4j_mcp.server --help

# Test with mock data
export NEO4J_MOCK=true
python3 -m neo4j_mcp.server
```

### Common macOS Issues
- **Python Version**: macOS comes with Python 2.7, use python3
- **SSL Certificates**: May need to update certificates for Neo4j connections
- **Permissions**: Use sudo for global installations or prefer user installs

---

## 🐧 Linux Setup

### Prerequisites
- Python 3.8+ (`sudo apt-get install python3 python3-pip`)
- Neo4j installed (Docker recommended)
- Claude Code installed

### Installation Steps

1. **Install Neo4j MCP Server**:
   ```bash
   git clone https://github.com/your-username/neo4j_mcp.git
   cd neo4j_mcp
   pip3 install -r requirements.txt
   pip3 install -e .
   ```

2. **Configure Neo4j Database**:

   **Option A: Docker (Recommended)**
   ```bash
   docker run -d \
     --name neo4j-mcp \
     -p 7687:7687 -p 7474:7474 \
     -e NEO4J_AUTH=neo4j/your-password \
     neo4j:latest
   ```

   **Option B: Package Installation**
   ```bash
   # Ubuntu/Debian
   wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
   echo 'deb https://debian.neo4j.com stable 4.4' | sudo tee /etc/apt/sources.list.d/neo4j.list
   sudo apt-get update
   sudo apt-get install neo4j
   sudo systemctl start neo4j
   ```

3. **Claude Code Configuration**:
   ```json
   {
     "mcpServers": {
       "neo4j": {
         "command": "/usr/bin/python3",
         "args": ["-m", "neo4j_mcp.server"],
         "cwd": "/path/to/neo4j_mcp",
         "env": {
           "NEO4J_URI": "neo4j://localhost:7687",
           "NEO4J_USER": "neo4j",
           "NEO4J_PASSWORD": "your-password",
           "NEO4J_DATABASE": "neo4j"
         }
       }
     }
   }
   ```

### Testing
```bash
# Test package installation
python3 -c "import neo4j_mcp; print('Package installed successfully')"

# Test server startup
python3 -m neo4j_mcp.server --help

# Test Docker Neo4j connection
docker exec neo4j-mcp cypher-shell -u neo4j -p your-password "RETURN 1"
```

### Common Linux Issues
- **Package Dependencies**: Install build-essential for some Python packages
- **Firewall**: Configure iptables/ufw for port 7687
- **SELinux**: May need to configure for Neo4j connections

---

## 🔀 WSL (Windows Subsystem for Linux) Setup

### Prerequisites
- WSL 2 with Ubuntu or similar distribution
- Python 3.8+ in WSL
- Neo4j running on Windows host
- Claude Code running in WSL

### Special WSL Considerations
The Neo4j MCP server includes automatic WSL detection and Windows host IP discovery for seamless connectivity.

### Installation Steps

1. **Install Neo4j MCP Server in WSL**:
   ```bash
   git clone https://github.com/your-username/neo4j_mcp.git
   cd neo4j_mcp
   pip3 install -r requirements.txt
   pip3 install -e .
   ```

2. **Configure Neo4j on Windows**:

   **Edit Neo4j Configuration** (Windows side):
   ```
   # In conf/neo4j.conf
   dbms.default_listen_address=0.0.0.0
   dbms.connector.bolt.listen_address=0.0.0.0:7687
   dbms.connector.http.listen_address=0.0.0.0:7474
   ```

   **Configure Windows Firewall**:
   ```cmd
   # Allow inbound connections on port 7687
   netsh advfirewall firewall add rule name="Neo4j Bolt" dir=in action=allow protocol=TCP localport=7687
   ```

3. **Claude Code Configuration (in WSL)**:
   ```json
   {
     "mcpServers": {
       "neo4j": {
         "command": "/usr/bin/python3",
         "args": ["-m", "neo4j_mcp.server"],
         "cwd": "/mnt/c/path/to/neo4j_mcp",
         "env": {
           "NEO4J_URI": "neo4j://127.0.0.1:7687",
           "NEO4J_USER": "neo4j",
           "NEO4J_PASSWORD": "your-password",
           "NEO4J_DATABASE": "neo4j"
         }
       }
     }
   }\n   ```

### Automatic WSL Detection
The server automatically:
- Detects WSL environment by checking `/proc/version`
- Discovers Windows host IP from routing table
- Tries multiple connection strategies:
  1. Original URI (127.0.0.1)
  2. Windows host IP (auto-detected)
  3. Additional fallback IPs

### Testing WSL Setup
```bash
# Test WSL environment detection
python3 -c "from neo4j_mcp.config import Neo4jConfig; print('WSL detected:', Neo4jConfig().is_wsl)"

# Test Windows host IP detection
python3 -c "from neo4j_mcp.config import Neo4jConfig; print('Windows host:', Neo4jConfig().get_windows_host_ip())"

# Test connection fallback
python3 test_connectivity.py

# Test with mock (no Neo4j required)
export NEO4J_MOCK=true
python3 -m neo4j_mcp.server
```

### Common WSL Issues
- **Network Access**: Ensure Windows allows WSL network access
- **File Permissions**: Use `/mnt/c/` paths for Windows files
- **Host IP Changes**: Windows host IP may change, server handles this automatically
- **Port Forwarding**: WSL 2 handles this automatically

---

## 🐳 Docker Setup

### Running Neo4j in Docker

**Quick Start**:
```bash
# Run Neo4j container
docker run -d \
  --name neo4j-server \
  -p 7687:7687 -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/password123 \
  -v neo4j-data:/data \
  -v neo4j-logs:/logs \
  neo4j:latest

# Run MCP server
docker run -d \
  --name neo4j-mcp \
  --link neo4j-server \
  -e NEO4J_URI=neo4j://neo4j-server:7687 \
  -e NEO4J_USER=neo4j \
  -e NEO4J_PASSWORD=password123 \
  your-username/neo4j-mcp:latest
```

**Docker Compose**:
```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:latest
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      - NEO4J_AUTH=neo4j/password123
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs

  neo4j-mcp:
    build: .
    depends_on:
      - neo4j
    environment:
      - NEO4J_URI=neo4j://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password123
    stdin_open: true
    tty: true

volumes:
  neo4j-data:
  neo4j-logs:
```

---

## ☁️ Cloud Neo4j Setup

### Neo4j AuraDB (Cloud)

1. **Create Neo4j AuraDB Instance**:
   - Visit https://neo4j.com/cloud/aura/
   - Create new instance
   - Note connection URI, username, and password

2. **Configure MCP Server**:
   ```json
   {
     "mcpServers": {
       "neo4j": {
         "command": "python",
         "args": ["-m", "neo4j_mcp.server"],
         "env": {
           "NEO4J_URI": "neo4j+s://xxxxx.databases.neo4j.io",
           "NEO4J_USER": "neo4j",
           "NEO4J_PASSWORD": "your-auradb-password",
           "NEO4J_DATABASE": "neo4j"
         }
       }
     }
   }
   ```

### AWS/GCP/Azure Neo4j

Similar configuration but use cloud instance URI and credentials.

---

## 🔧 Advanced Configuration

### Environment Variables Reference

| Variable | Description | Default | Platforms |
|----------|-------------|---------|-----------|
| `NEO4J_URI` | Neo4j connection URI | `neo4j://localhost:7687` | All |
| `NEO4J_USER` | Database username | `neo4j` | All |
| `NEO4J_PASSWORD` | Database password | - | All |
| `NEO4J_DATABASE` | Target database | `neo4j` | All |
| `NEO4J_CONNECTION_TIMEOUT` | Connection timeout (seconds) | `10` | All |
| `NEO4J_ENABLE_SCHEMA` | Enable schema tool | `true` | All |
| `NEO4J_ENABLE_READ` | Enable read tool | `true` | All |
| `NEO4J_ENABLE_WRITE` | Enable write tool | `true` | All |
| `NEO4J_MOCK` | Enable mock mode | `false` | All |

### Security Considerations

1. **Credential Management**:
   - Use environment variables, not hardcoded passwords
   - Consider using `.env` files for local development
   - Use secrets management for production deployments

2. **Network Security**:
   - Configure firewalls appropriately
   - Use encrypted connections (`neo4j+s://`) for cloud deployments
   - Limit database user permissions

3. **Access Control**:
   - Disable write operations in read-only environments
   - Use runtime configuration to manage tool access
   - Monitor MCP server logs for unusual activity

---

## 📊 Performance Tuning

### Neo4j Configuration
```
# neo4j.conf optimizations
dbms.memory.heap.initial_size=1G
dbms.memory.heap.max_size=2G
dbms.memory.pagecache.size=1G
dbms.connector.bolt.thread_pool_min_size=5
dbms.connector.bolt.thread_pool_max_size=400
```

### MCP Server Configuration
```bash
# Increase connection timeout for slow networks
export NEO4J_CONNECTION_TIMEOUT=30

# Enable connection pooling optimizations
export NEO4J_POOL_SIZE=10
export NEO4J_POOL_TIMEOUT=60
```

### Monitoring
- Monitor Neo4j logs for slow queries
- Use Claude Code's MCP server logs for debugging
- Consider using Neo4j's monitoring tools for production

---

## 🆘 Platform-Specific Troubleshooting

### Windows
- **Path Issues**: Use forward slashes in JSON configuration
- **Antivirus**: Exclude Neo4j and Python directories
- **User Permissions**: Run as administrator if needed

### macOS
- **Gatekeeper**: Allow Neo4j and Python applications
- **SSL Issues**: Update certificates with `pip install --upgrade certifi`
- **Python Path**: Use `/usr/local/bin/python3` or virtual environments

### Linux
- **Package Management**: Use distribution-specific package managers
- **SystemD**: Use systemctl for Neo4j service management
- **AppArmor/SELinux**: Configure security policies if needed

### WSL
- **Network Issues**: Restart WSL if Windows host IP changes
- **File System**: Prefer Windows paths for shared files
- **Resource Limits**: Configure WSL memory limits if needed

---

Ready to deploy on your platform? Choose the appropriate section above and follow the step-by-step instructions!