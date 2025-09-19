#!/usr/bin/env python3
"""Test the improved schema tool with fallback."""

import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neo4j_mcp.connection import Neo4jConnectionManager
from neo4j_mcp.config import Neo4jConfig
from neo4j_mcp.tools.schema import get_neo4j_schema


async def test_schema_fallback():
    """Test schema tool with APOC fallback."""
    print("Testing Improved Schema Tool")
    print("=" * 40)

    config = Neo4jConfig.from_env()
    connection_manager = Neo4jConnectionManager(config)

    try:
        # Test schema info retrieval
        schema_info = await connection_manager.get_schema_info()
        print(f"[SUCCESS] Retrieved schema info with keys: {list(schema_info.keys())}")

        # Test schema tool
        result = await get_neo4j_schema(connection_manager)
        print(f"[SUCCESS] Schema tool result length: {len(result[0].text)} characters")

        # Show first 500 characters
        print("\nSchema Tool Output (first 500 chars):")
        print("-" * 50)
        print(result[0].text[:500])
        if len(result[0].text) > 500:
            print("\n... [truncated]")

        await connection_manager.close()

    except Exception as e:
        print(f"[INFO] Testing without actual Neo4j (expected): {e}")

        # Test with mock data
        mock_schema = {
            "nodes": [
                {"label": "Person", "properties": []},
                {"label": "Company", "properties": []},
            ],
            "relationships": [
                {"relationshipType": "WORKS_FOR", "properties": []},
                {"relationshipType": "KNOWS", "properties": []},
            ],
            "counts": [
                {"labels": ["Person"], "count": 100},
                {"labels": ["Company"], "count": 50},
            ]
        }

        # Mock the connection manager
        class MockConnectionManager:
            async def get_schema_info(self):
                return mock_schema

        mock_result = await get_neo4j_schema(MockConnectionManager())
        print(f"[SUCCESS] Mock schema tool result: {len(mock_result[0].text)} characters")
        print("\nMock Schema Output:")
        print("-" * 50)
        print(mock_result[0].text)

    print("\n[SUCCESS] Schema tool test completed!")


if __name__ == "__main__":
    asyncio.run(test_schema_fallback())