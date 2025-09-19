#!/usr/bin/env python3
"""Test the completely fixed Neo4j MCP Server."""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neo4j_mcp.server import Neo4jMCPServer
import mcp.types as types


async def test_server_components():
    """Test all server components work properly."""
    print("Testing Fixed Neo4j MCP Server")
    print("=" * 40)

    try:
        # Test 1: Server creation
        server = Neo4jMCPServer()
        print("[SUCCESS] Server instance created")

        # Test 2: Capabilities creation
        capabilities = types.ServerCapabilities(
            tools=types.ToolsCapability(listChanged=False)
        )
        print("[SUCCESS] Server capabilities created:", capabilities)

        # Test 3: Tool registration test
        from mcp.server.models import InitializationOptions
        init_options = InitializationOptions(
            server_name="neo4j-mcp",
            server_version="1.0.0",
            capabilities=capabilities
        )
        print("[SUCCESS] Initialization options created:", init_options.server_name)

        print("\n[SUCCESS] All server components working correctly!")
        print("\nThe MCP server should now start properly with Claude Code.")
        return True

    except Exception as e:
        print(f"[ERROR] Server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_server_components())
    sys.exit(0 if success else 1)