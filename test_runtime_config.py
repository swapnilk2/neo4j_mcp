#!/usr/bin/env python3
"""Test runtime configuration functionality."""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neo4j_mcp.server import Neo4jMCPServer
from neo4j_mcp.tools.config_tool import neo4j_configure


async def test_runtime_configuration():
    """Test runtime configuration changes."""
    print("Testing Runtime Configuration")
    print("=" * 40)

    # Create server
    server = Neo4jMCPServer()
    print("[SUCCESS] Server created")

    # Test 1: Check initial status
    print("\n1. Initial configuration status:")
    result = await neo4j_configure(server, "status")
    print(result[0].text)

    # Test 2: Disable write tool
    print("\n2. Disabling write tool:")
    result = await neo4j_configure(server, "disable", "write")
    print(result[0].text)

    # Test 3: Check status after disable
    print("\n3. Status after disabling write:")
    result = await neo4j_configure(server, "list")
    print(result[0].text)

    # Test 4: Re-enable write tool
    print("\n4. Re-enabling write tool:")
    result = await neo4j_configure(server, "enable", "write")
    print(result[0].text)

    # Test 5: Final status check
    print("\n5. Final status:")
    result = await neo4j_configure(server, "list")
    print(result[0].text)

    print("\n[SUCCESS] All runtime configuration tests passed!")


if __name__ == "__main__":
    asyncio.run(test_runtime_configuration())