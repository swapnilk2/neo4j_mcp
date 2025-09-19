"""Comprehensive tests for Neo4j MCP Server."""

import asyncio
import pytest
import json
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

from neo4j.exceptions import ServiceUnavailable, AuthError

from neo4j_mcp.config import Neo4jConfig
from neo4j_mcp.connection import Neo4jConnectionManager
from neo4j_mcp.tools.schema import get_neo4j_schema
from neo4j_mcp.tools.read import read_neo4j_cypher
from neo4j_mcp.tools.write import write_neo4j_cypher


class TestNeo4jConfig:
    """Test Neo4j configuration management."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Neo4jConfig()
        assert config.uri == "neo4j://127.0.0.1:7687"
        assert config.user == "neo4j"
        assert config.password == "password"
        assert config.database == "neo4j"
        assert config.connection_timeout == 30

    @patch.dict('os.environ', {
        'NEO4J_URI': 'neo4j://testhost:7687',
        'NEO4J_USER': 'testuser',
        'NEO4J_PASSWORD': 'testpass',
        'NEO4J_DATABASE': 'testdb'
    })
    def test_config_from_env(self):
        """Test configuration from environment variables."""
        config = Neo4jConfig.from_env()
        assert config.uri == "neo4j://testhost:7687"
        assert config.user == "testuser"
        assert config.password == "testpass"
        assert config.database == "testdb"

    @patch('builtins.open', create=True)
    def test_detect_wsl_environment(self, mock_open):
        """Test WSL environment detection."""
        config = Neo4jConfig()

        # Test WSL detection
        mock_open.return_value.__enter__.return_value.read.return_value = "Linux version 5.4.0-microsoft-standard-WSL2"
        assert config.detect_wsl_environment() is True

        # Test non-WSL
        mock_open.return_value.__enter__.return_value.read.return_value = "Linux version 5.4.0-generic"
        assert config.detect_wsl_environment() is False

    @patch('subprocess.run')
    @patch('builtins.open', create=True)
    def test_get_windows_host_ip(self, mock_open, mock_subprocess):
        """Test Windows host IP detection."""
        config = Neo4jConfig()

        # Test resolv.conf method
        mock_open.return_value.__enter__.return_value.__iter__ = Mock(
            return_value=iter(["nameserver 172.19.0.1"])
        )
        ip = config.get_windows_host_ip()
        assert ip == "172.19.0.1"

    @patch('subprocess.run')
    @patch('builtins.open', create=True)
    def test_get_connection_uris_wsl(self, mock_open, mock_subprocess):
        """Test connection URI generation for WSL."""
        config = Neo4jConfig()

        # Mock WSL environment
        mock_open.return_value.__enter__.return_value.read.return_value = "Linux version 5.4.0-microsoft-standard-WSL2"
        mock_open.return_value.__enter__.return_value.__iter__ = Mock(
            return_value=iter(["nameserver 172.19.0.1"])
        )

        uris = config.get_connection_uris()
        assert len(uris) >= 2
        assert "neo4j://127.0.0.1:7687" in uris
        assert "neo4j://172.19.0.1:7687" in uris

    def test_get_connection_uris_non_wsl(self):
        """Test connection URI generation for non-WSL."""
        config = Neo4jConfig()

        with patch.object(config, 'detect_wsl_environment', return_value=False):
            uris = config.get_connection_uris()
            assert uris == [config.uri]


class TestNeo4jConnectionManager:
    """Test Neo4j connection management."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Neo4jConfig(
            uri="neo4j://localhost:7687",
            user="testuser",
            password="testpass"
        )

    @pytest.fixture
    def connection_manager(self, config):
        """Create connection manager for testing."""
        return Neo4jConnectionManager(config)

    @pytest.mark.asyncio
    async def test_connect_success(self, connection_manager):
        """Test successful connection."""
        mock_driver = AsyncMock()
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_record = Mock()
        mock_record.__getitem__ = Mock(return_value=1)

        mock_result.single.return_value = mock_record
        mock_session.run.return_value = mock_result
        mock_driver.session.return_value.__aenter__.return_value = mock_session

        with patch('neo4j_mcp.connection.GraphDatabase.driver', return_value=mock_driver):
            driver = await connection_manager.connect()
            assert driver == mock_driver

    @pytest.mark.asyncio
    async def test_connect_failure_all_uris(self, connection_manager):
        """Test connection failure for all URIs."""
        with patch('neo4j_mcp.connection.GraphDatabase.driver') as mock_driver_func:
            mock_driver_func.side_effect = ServiceUnavailable("Connection failed")

            with pytest.raises(ServiceUnavailable):
                await connection_manager.connect()

    @pytest.mark.asyncio
    async def test_execute_read_query(self, connection_manager):
        """Test read query execution."""
        mock_session = AsyncMock()
        mock_result = AsyncMock()

        # Mock async iteration
        async def async_iter():
            yield {"name": "Alice", "age": 30}
            yield {"name": "Bob", "age": 25}

        mock_result.__aiter__ = async_iter
        mock_session.run.return_value = mock_result

        with patch.object(connection_manager, 'get_session') as mock_get_session:
            mock_get_session.return_value.__aenter__.return_value = mock_session

            results = await connection_manager.execute_read_query("MATCH (n) RETURN n")
            assert len(results) == 2
            assert results[0]["name"] == "Alice"
            assert results[1]["name"] == "Bob"

    @pytest.mark.asyncio
    async def test_execute_write_query(self, connection_manager):
        """Test write query execution."""
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_summary = Mock()

        # Mock counters
        mock_summary.counters.nodes_created = 1
        mock_summary.counters.relationships_created = 0
        mock_summary.counters.properties_set = 2
        mock_summary.result_available_after = 10
        mock_summary.result_consumed_after = 15

        mock_result.consume.return_value = mock_summary
        mock_session.run.return_value = mock_result

        with patch.object(connection_manager, 'get_session') as mock_get_session:
            mock_get_session.return_value.__aenter__.return_value = mock_session

            summary = await connection_manager.execute_write_query("CREATE (n:Person {name: 'Alice'})")

            assert summary["counters"]["nodes_created"] == 1
            assert summary["counters"]["properties_set"] == 2
            assert summary["result_available_after"] == 10


class TestNeo4jTools:
    """Test Neo4j MCP tools."""

    @pytest.fixture
    def mock_connection_manager(self):
        """Create mock connection manager."""
        return AsyncMock(spec=Neo4jConnectionManager)

    @pytest.mark.asyncio
    async def test_get_neo4j_schema_success(self, mock_connection_manager):
        """Test successful schema retrieval."""
        mock_schema_info = {
            "nodes": [
                {
                    "label": "Person",
                    "properties": [
                        {"property": "name", "types": ["String"], "mandatory": True},
                        {"property": "age", "types": ["Integer"], "mandatory": False}
                    ]
                }
            ],
            "relationships": [
                {
                    "relationshipType": "KNOWS",
                    "properties": [
                        {"property": "since", "types": ["Date"], "mandatory": False}
                    ]
                }
            ]
        }

        mock_connection_manager.get_schema_info.return_value = mock_schema_info

        results = await get_neo4j_schema(mock_connection_manager)

        assert len(results) == 1
        assert results[0].type == "text"
        assert "Person" in results[0].text
        assert "KNOWS" in results[0].text

    @pytest.mark.asyncio
    async def test_get_neo4j_schema_failure(self, mock_connection_manager):
        """Test schema retrieval failure."""
        mock_connection_manager.get_schema_info.side_effect = Exception("Database error")

        results = await get_neo4j_schema(mock_connection_manager)

        assert len(results) == 1
        assert "Error" in results[0].text

    @pytest.mark.asyncio
    async def test_read_neo4j_cypher_success(self, mock_connection_manager):
        """Test successful read query."""
        mock_results = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]

        mock_connection_manager.execute_read_query.return_value = mock_results

        results = await read_neo4j_cypher(
            mock_connection_manager,
            "MATCH (n:Person) RETURN n.name as name, n.age as age"
        )

        assert len(results) == 1
        assert "Alice" in results[0].text
        assert "Bob" in results[0].text
        assert "Records returned: 2" in results[0].text

    @pytest.mark.asyncio
    async def test_read_neo4j_cypher_write_warning(self, mock_connection_manager):
        """Test warning for write operations in read query."""
        results = await read_neo4j_cypher(
            mock_connection_manager,
            "CREATE (n:Person {name: 'Alice'})"
        )

        assert len(results) == 1
        assert "Warning" in results[0].text
        assert "write operations" in results[0].text

    @pytest.mark.asyncio
    async def test_write_neo4j_cypher_success(self, mock_connection_manager):
        """Test successful write query."""
        mock_summary = {
            "counters": {
                "nodes_created": 1,
                "properties_set": 2,
                "nodes_deleted": 0,
                "relationships_created": 0
            },
            "result_available_after": 10,
            "result_consumed_after": 15
        }

        mock_connection_manager.execute_write_query.return_value = mock_summary

        results = await write_neo4j_cypher(
            mock_connection_manager,
            "CREATE (n:Person {name: 'Alice', age: 30})"
        )

        assert len(results) == 1
        assert "Nodes created: 1" in results[0].text
        assert "Properties set: 2" in results[0].text
        assert "✅" in results[0].text

    @pytest.mark.asyncio
    async def test_write_neo4j_cypher_failure(self, mock_connection_manager):
        """Test write query failure."""
        mock_connection_manager.execute_write_query.side_effect = Exception("Database error")

        results = await write_neo4j_cypher(
            mock_connection_manager,
            "CREATE (n:Person {name: 'Alice'})"
        )

        assert len(results) == 1
        assert "❌" in results[0].text
        assert "Error" in results[0].text


class TestCrossPlatformConnectivity:
    """Test cross-platform connectivity scenarios."""

    @pytest.mark.asyncio
    async def test_wsl_fallback_connection(self):
        """Test connection fallback in WSL environment."""
        config = Neo4jConfig(uri="neo4j://127.0.0.1:7687")
        connection_manager = Neo4jConnectionManager(config)

        # Mock WSL environment and Windows host IP
        with patch.object(config, 'detect_wsl_environment', return_value=True), \
             patch.object(config, 'get_windows_host_ip', return_value="172.19.0.1"):

            uris = config.get_connection_uris()
            assert "neo4j://127.0.0.1:7687" in uris
            assert "neo4j://172.19.0.1:7687" in uris

    @pytest.mark.asyncio
    async def test_connection_retry_logic(self):
        """Test connection retry logic with multiple URIs."""
        config = Neo4jConfig(uri="neo4j://127.0.0.1:7687")
        connection_manager = Neo4jConnectionManager(config)

        call_count = 0

        def mock_driver_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First URI fails
                raise ServiceUnavailable("Connection failed")
            else:
                # Second URI succeeds
                mock_driver = AsyncMock()
                mock_session = AsyncMock()
                mock_result = AsyncMock()
                mock_record = Mock()
                mock_record.__getitem__ = Mock(return_value=1)
                mock_result.single.return_value = mock_record
                mock_session.run.return_value = mock_result
                mock_driver.session.return_value.__aenter__.return_value = mock_session
                return mock_driver

        with patch.object(config, 'get_connection_uris', return_value=[
            "neo4j://127.0.0.1:7687",
            "neo4j://172.19.0.1:7687"
        ]), \
             patch('neo4j_mcp.connection.GraphDatabase.driver', side_effect=mock_driver_side_effect):

            driver = await connection_manager.connect()
            assert driver is not None
            assert call_count == 2  # Should have tried both URIs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])