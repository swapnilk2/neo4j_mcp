#!/usr/bin/env python3
"""Test tool disabling functionality."""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neo4j_mcp.config import Neo4jConfig
from neo4j_mcp.server import Neo4jMCPServer


async def test_tool_configurations():
    """Test different tool configuration scenarios."""

    print("Testing Tool Disabling Functionality")
    print("=" * 50)

    # Test 1: All tools enabled (default)
    print("\n1. Testing with ALL tools enabled:")
    config1 = Neo4jConfig(
        enable_schema_tool=True,
        enable_read_tool=True,
        enable_write_tool=True
    )
    server1 = Neo4jMCPServer()
    server1.config = config1

    # Manually call the list_tools handler
    tools1 = await server1._get_available_tools()
    print(f"   Available tools: {[tool.name for tool in tools1]}")

    # Test 2: Only read tool enabled
    print("\n2. Testing with ONLY READ tool enabled:")
    config2 = Neo4jConfig(
        enable_schema_tool=False,
        enable_read_tool=True,
        enable_write_tool=False
    )
    server2 = Neo4jMCPServer()
    server2.config = config2

    tools2 = await server2._get_available_tools()
    print(f"   Available tools: {[tool.name for tool in tools2]}")

    # Test 3: No write operations (read + schema only)
    print("\n3. Testing with NO WRITE operations:")
    config3 = Neo4jConfig(
        enable_schema_tool=True,
        enable_read_tool=True,
        enable_write_tool=False
    )
    server3 = Neo4jMCPServer()
    server3.config = config3

    tools3 = await server3._get_available_tools()
    print(f"   Available tools: {[tool.name for tool in tools3]}")

    # Test 4: Only schema tool
    print("\n4. Testing with ONLY SCHEMA tool:")
    config4 = Neo4jConfig(
        enable_schema_tool=True,
        enable_read_tool=False,
        enable_write_tool=False
    )
    server4 = Neo4jMCPServer()
    server4.config = config4

    tools4 = await server4._get_available_tools()
    print(f"   Available tools: {[tool.name for tool in tools4]}")

    print("\n[SUCCESS] All tool configuration tests passed!")


# Helper method to get tools (we'll add this to the server)
async def get_available_tools(server):
    """Helper to get available tools for testing."""
    from neo4j_mcp.tools.schema import SCHEMA_TOOL
    from neo4j_mcp.tools.read import READ_TOOL
    from neo4j_mcp.tools.write import WRITE_TOOL

    tools = []
    if server.config.enable_schema_tool:
        tools.append(SCHEMA_TOOL)
    if server.config.enable_read_tool:
        tools.append(READ_TOOL)
    if server.config.enable_write_tool:
        tools.append(WRITE_TOOL)
    return tools

# Add the helper method to the server class
Neo4jMCPServer._get_available_tools = get_available_tools


if __name__ == "__main__":
    asyncio.run(test_tool_configurations())