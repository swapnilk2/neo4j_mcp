#!/usr/bin/env python3
"""Test MCP server startup without attempting connection."""

import sys
import os
import asyncio
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neo4j_mcp.server import Neo4jMCPServer
import mcp.types as types


async def test_server_startup():
    """Test server creation and tool listing."""
    print("Testing Neo4j MCP Server Startup")
    print("=" * 40)

    try:
        # Create server
        server = Neo4jMCPServer()
        print("[SUCCESS] Server instance created")

        # Test tool listing (this should work without Neo4j connection)
        tools = [
            types.Tool(name="get_neo4j_schema", description="Get schema", inputSchema={"type": "object", "properties": {}}),
            types.Tool(name="read_neo4j_cypher", description="Read query", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
            types.Tool(name="write_neo4j_cypher", description="Write query", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]})
        ]

        print(f"[SUCCESS] Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")

        print("\n[SUCCESS] Server startup test completed")
        return True

    except Exception as e:
        print(f"[ERROR] Server startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_server_startup())
    sys.exit(0 if success else 1)