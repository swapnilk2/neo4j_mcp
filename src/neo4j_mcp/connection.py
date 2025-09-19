"""Neo4j connection management with cross-platform support."""

import asyncio
import logging
from typing import Optional, Any, Dict, List

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError
from neo4j.graph import Node, Relationship, Path

from .config import Neo4jConfig


class Neo4jConnectionManager:
    """Manages Neo4j connections with fallback for cross-platform environments."""

    def __init__(self, config: Neo4jConfig):
        self.config = config
        self.driver: Optional[Driver] = None
        self.logger = logging.getLogger(__name__)

    async def connect(self) -> Driver:
        """Establish connection to Neo4j with URI fallback."""
        if self.driver:
            return self.driver

        uris = self.config.get_connection_uris()
        self.logger.info(f"Attempting connection to Neo4j with {len(uris)} URI(s)")

        last_exception = None
        for i, uri in enumerate(uris):
            try:
                self.logger.info(f"Attempting connection {i+1}/{len(uris)}: {uri}")

                driver = GraphDatabase.driver(
                    uri,
                    auth=(self.config.user, self.config.password),
                    connection_timeout=self.config.connection_timeout
                )

                # Test the connection
                self._test_connection(driver)

                self.driver = driver
                self.logger.info(f"Successfully connected to Neo4j at: {uri}")
                return driver

            except Exception as e:
                last_exception = e
                self.logger.warning(f"Connection failed for {uri}: {str(e)}")
                if 'driver' in locals():
                    try:
                        driver.close()
                    except:
                        pass

        if last_exception:
            raise ServiceUnavailable(f"Failed to connect to Neo4j after trying {len(uris)} URI(s). Last error: {str(last_exception)}")
        else:
            raise ServiceUnavailable("No URIs available for connection")

    def _test_connection(self, driver: Driver) -> None:
        """Test if the connection is working."""
        # Create a test session to verify connectivity
        with driver.session(database=self.config.database) as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            if not record or record["test"] != 1:
                raise ServiceUnavailable("Connection test failed")

    def get_session(self):
        """Get a session context manager with automatic connection management."""
        if not self.driver:
            raise ServiceUnavailable("Not connected to Neo4j. Call connect() first.")

        return self.driver.session(database=self.config.database)

    def _convert_neo4j_value(self, value: Any) -> Any:
        """Convert Neo4j-specific types to JSON-serializable types."""
        if isinstance(value, Node):
            return {
                "id": value.id,
                "labels": list(value.labels),
                "properties": dict(value.items())
            }
        elif isinstance(value, Relationship):
            return {
                "id": value.id,
                "type": value.type,
                "start_node": value.start_node.id,
                "end_node": value.end_node.id,
                "properties": dict(value.items())
            }
        elif isinstance(value, Path):
            return {
                "nodes": [self._convert_neo4j_value(node) for node in value.nodes],
                "relationships": [self._convert_neo4j_value(rel) for rel in value.relationships]
            }
        elif isinstance(value, list):
            return [self._convert_neo4j_value(item) for item in value]
        elif isinstance(value, dict):
            return {key: self._convert_neo4j_value(val) for key, val in value.items()}
        else:
            return value

    async def execute_read_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a read-only query and return results."""
        if not self.driver:
            await self.connect()

        with self.get_session() as session:
            result = session.run(query, parameters or {})
            records = []
            for record in result:
                # Convert Neo4j types to JSON-serializable types
                record_dict = {}
                for key, value in record.items():
                    record_dict[key] = self._convert_neo4j_value(value)
                records.append(record_dict)
            return records

    async def execute_write_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a write query and return summary information."""
        if not self.driver:
            await self.connect()

        with self.get_session() as session:
            result = session.run(query, parameters or {})
            summary = result.consume()

            return {
                "query": query,
                "parameters": parameters or {},
                "counters": {
                    "nodes_created": summary.counters.nodes_created,
                    "nodes_deleted": summary.counters.nodes_deleted,
                    "relationships_created": summary.counters.relationships_created,
                    "relationships_deleted": summary.counters.relationships_deleted,
                    "properties_set": summary.counters.properties_set,
                    "labels_added": summary.counters.labels_added,
                    "labels_removed": summary.counters.labels_removed,
                    "indexes_added": summary.counters.indexes_added,
                    "indexes_removed": summary.counters.indexes_removed,
                    "constraints_added": summary.counters.constraints_added,
                    "constraints_removed": summary.counters.constraints_removed,
                },
                "result_available_after": summary.result_available_after,
                "result_consumed_after": summary.result_consumed_after
            }

    async def get_schema_info(self) -> Dict[str, Any]:
        """Get comprehensive schema information using standard Neo4j procedures only."""
        # Standard Neo4j queries - no APOC required
        schema_queries = {
            "nodes": """
                CALL db.labels() YIELD label
                RETURN label, [] as properties
                ORDER BY label
            """,
            "relationships": """
                CALL db.relationshipTypes() YIELD relationshipType
                RETURN relationshipType, [] as properties
                ORDER BY relationshipType
            """,
            "schema": """
                CALL db.schema.visualization()
            """,
            "counts": """
                MATCH (n)
                RETURN labels(n) as labels, count(*) as count
                ORDER BY count DESC
            """
        }

        results = {}

        try:
            for key, query in schema_queries.items():
                results[key] = await self.execute_read_query(query)
            self.logger.info("Successfully retrieved schema information using standard Neo4j procedures")
            return results
        except Exception as e:
            self.logger.error(f"Schema queries failed: {str(e)}")
            return {"nodes": [], "relationships": [], "schema": [], "counts": []}

    async def close(self):
        """Close the database connection."""
        if self.driver:
            self.driver.close()
            self.driver = None
            self.logger.info("Neo4j connection closed")