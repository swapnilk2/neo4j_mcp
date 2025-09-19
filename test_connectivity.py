#!/usr/bin/env python3
"""Test script for Neo4j MCP Server connectivity."""

import asyncio
import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neo4j_mcp.config import Neo4jConfig
from neo4j_mcp.connection import Neo4jConnectionManager


async def test_connectivity():
    """Test Neo4j connectivity with fallback."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("=" * 60)
    print("Neo4j MCP Server Connectivity Test")
    print("=" * 60)

    # Test configuration
    config = Neo4jConfig.from_env()
    print(f"\nConfiguration:")
    print(f"  URI: {config.uri}")
    print(f"  User: {config.user}")
    print(f"  Database: {config.database}")

    # Test WSL detection
    is_wsl = config.detect_wsl_environment()
    print(f"\nEnvironment Detection:")
    print(f"  WSL Environment: {is_wsl}")

    if is_wsl:
        windows_ip = config.get_windows_host_ip()
        print(f"  Windows Host IP: {windows_ip}")

    # Get connection URIs
    uris = config.get_connection_uris()
    print(f"\nConnection URIs to try:")
    for i, uri in enumerate(uris, 1):
        print(f"  {i}. {uri}")

    # Test connection
    connection_manager = Neo4jConnectionManager(config)

    try:
        print(f"\nTesting connectivity...")
        driver = await connection_manager.connect()
        print("[SUCCESS] Successfully connected to Neo4j!")

        # Test basic query
        print("\nTesting basic query...")
        result = await connection_manager.execute_read_query("RETURN 'Hello Neo4j!' as message")
        print(f"Query result: {result}")

        # Test schema query (if APOC is available)
        print("\nTesting schema query...")
        try:
            schema_info = await connection_manager.get_schema_info()
            print(f"Schema nodes: {len(schema_info.get('nodes', []))}")
            print(f"Schema relationships: {len(schema_info.get('relationships', []))}")
        except Exception as e:
            print(f"Schema query failed (APOC may not be installed): {e}")

        await connection_manager.close()
        print("\n[SUCCESS] All tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Ensure Neo4j is running on Windows")
        print("2. Check if Neo4j is configured to accept connections from all interfaces")
        print("3. Verify Windows firewall allows port 7687")
        print("4. Try connecting directly from WSL using neo4j-shell or cypher-shell")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_connectivity())
    sys.exit(0 if success else 1)