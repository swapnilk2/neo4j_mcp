"""Configuration management for Neo4j MCP Server."""

import os
import platform
import subprocess
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class Neo4jConfig(BaseModel):
    """Neo4j connection configuration with cross-platform support."""

    uri: str = Field(default="neo4j://127.0.0.1:7687")
    user: str = Field(default="neo4j")
    password: str = Field(default="password")
    database: str = Field(default="neo4j")

    # Cross-platform settings
    windows_host_ips: List[str] = Field(default_factory=list)
    connection_timeout: int = Field(default=30)
    max_connection_retries: int = Field(default=3)

    # Tool enablement settings
    enable_schema_tool: bool = Field(default=True)
    enable_read_tool: bool = Field(default=True)
    enable_write_tool: bool = Field(default=True)

    @classmethod
    def from_env(cls) -> "Neo4jConfig":
        """Create configuration from environment variables."""
        return cls(
            uri=os.getenv("NEO4J_URI", "neo4j://127.0.0.1:7687"),
            user=os.getenv("NEO4J_USER", "neo4j"),
            password=os.getenv("NEO4J_PASSWORD", "password"),
            database=os.getenv("NEO4J_DATABASE", "neo4j"),
            connection_timeout=int(os.getenv("NEO4J_TIMEOUT", "30")),
            max_connection_retries=int(os.getenv("NEO4J_RETRIES", "3")),
            enable_schema_tool=os.getenv("NEO4J_ENABLE_SCHEMA", "true").lower() == "true",
            enable_read_tool=os.getenv("NEO4J_ENABLE_READ", "true").lower() == "true",
            enable_write_tool=os.getenv("NEO4J_ENABLE_WRITE", "true").lower() == "true",
        )

    def detect_wsl_environment(self) -> bool:
        """Detect if running in WSL environment."""
        try:
            # Check for WSL in /proc/version
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
                return 'microsoft' in version_info or 'wsl' in version_info
        except:
            return False

    def get_windows_host_ip(self) -> Optional[str]:
        """Get Windows host IP from WSL environment."""
        try:
            # Method 1: Parse /etc/resolv.conf for nameserver
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.strip().startswith('nameserver'):
                        nameserver = line.split()[1]
                        return nameserver
        except:
            pass

        try:
            # Method 2: Get default gateway
            result = subprocess.run(['ip', 'route', 'show', 'default'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # Parse: default via 172.19.0.1 dev eth0 proto kernel
                for line in result.stdout.split('\n'):
                    if 'default via' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2]
        except:
            pass

        return None

    def get_connection_uris(self) -> List[str]:
        """Get list of URIs to try for connection."""
        uris = [self.uri]

        if self.detect_wsl_environment():
            windows_ip = self.get_windows_host_ip()
            if windows_ip:
                # Replace localhost/127.0.0.1 with Windows host IP
                original_uri = self.uri
                if "127.0.0.1" in original_uri:
                    windows_uri = original_uri.replace("127.0.0.1", windows_ip)
                    uris.append(windows_uri)
                elif "localhost" in original_uri:
                    windows_uri = original_uri.replace("localhost", windows_ip)
                    uris.append(windows_uri)

                # Add additional known Windows host IPs
                for ip in self.windows_host_ips:
                    if ip != windows_ip:
                        additional_uri = original_uri.replace("127.0.0.1", ip).replace("localhost", ip)
                        uris.append(additional_uri)

        return list(dict.fromkeys(uris))  # Remove duplicates while preserving order


def get_config() -> Neo4jConfig:
    """Get Neo4j configuration singleton."""
    return Neo4jConfig.from_env()