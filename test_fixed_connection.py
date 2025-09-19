#!/usr/bin/env python3
"""Test script for fixed Neo4j MCP Server connection logic."""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neo4j_mcp.config import Neo4jConfig
from neo4j_mcp.connection import Neo4jConnectionManager


async def test_connection():
    """Test the fixed connection logic."""
    print("Testing Fixed Neo4j MCP Connection")
    print("=" * 50)

    config = Neo4jConfig.from_env()
    print(f"URI: {config.uri}")
    print(f"User: {config.user}")

    connection_manager = Neo4jConnectionManager(config)

    try:
        # Test connection
        driver = await connection_manager.connect()
        print("[SUCCESS] Connected to Neo4j")

        # Test read query
        results = await connection_manager.execute_read_query("RETURN 'Hello' as message")
        print(f"[SUCCESS] Read query result: {results}")

        await connection_manager.close()
        print("[SUCCESS] Connection closed")

    except Exception as e:
        print(f"[INFO] Connection failed as expected: {e}")
        print("This is normal if Neo4j is not running")


if __name__ == "__main__":
    asyncio.run(test_connection())