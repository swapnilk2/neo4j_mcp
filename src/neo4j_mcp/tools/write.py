"""Neo4j write query execution tool."""

import json
import logging
from typing import Any, Dict, Optional

from mcp.types import Tool, TextContent

from ..connection import Neo4jConnectionManager


logger = logging.getLogger(__name__)


async def write_neo4j_cypher(
    connection_manager: Neo4jConnectionManager,
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> list[TextContent]:
    """
    Execute a write Cypher query on the Neo4j database.

    Args:
        connection_manager: Neo4jConnectionManager instance
        query: The Cypher query to execute
        params: Optional parameters to pass to the Cypher query

    Returns:
        List of TextContent with execution summary
    """
    try:
        # Execute the write query
        summary = await connection_manager.execute_write_query(query, params)

        # Format summary
        output_lines = []
        output_lines.append(f"# Write Query Execution Summary")
        output_lines.append("")
        output_lines.append(f"**Query:** `{query}`")

        if params:
            output_lines.append(f"**Parameters:** `{json.dumps(params, indent=2)}`")

        output_lines.append("")
        output_lines.append("## Execution Statistics")

        counters = summary.get("counters", {})
        stats = []

        if counters.get("nodes_created", 0) > 0:
            stats.append(f"Nodes created: {counters['nodes_created']}")
        if counters.get("nodes_deleted", 0) > 0:
            stats.append(f"Nodes deleted: {counters['nodes_deleted']}")
        if counters.get("relationships_created", 0) > 0:
            stats.append(f"Relationships created: {counters['relationships_created']}")
        if counters.get("relationships_deleted", 0) > 0:
            stats.append(f"Relationships deleted: {counters['relationships_deleted']}")
        if counters.get("properties_set", 0) > 0:
            stats.append(f"Properties set: {counters['properties_set']}")
        if counters.get("labels_added", 0) > 0:
            stats.append(f"Labels added: {counters['labels_added']}")
        if counters.get("labels_removed", 0) > 0:
            stats.append(f"Labels removed: {counters['labels_removed']}")
        if counters.get("indexes_added", 0) > 0:
            stats.append(f"Indexes added: {counters['indexes_added']}")
        if counters.get("indexes_removed", 0) > 0:
            stats.append(f"Indexes removed: {counters['indexes_removed']}")
        if counters.get("constraints_added", 0) > 0:
            stats.append(f"Constraints added: {counters['constraints_added']}")
        if counters.get("constraints_removed", 0) > 0:
            stats.append(f"Constraints removed: {counters['constraints_removed']}")

        if stats:
            for stat in stats:
                output_lines.append(f"- {stat}")
        else:
            output_lines.append("- No changes made to the database")

        # Timing information
        output_lines.append("")
        output_lines.append("## Timing")
        if summary.get("result_available_after") is not None:
            output_lines.append(f"- Result available after: {summary['result_available_after']} ms")
        if summary.get("result_consumed_after") is not None:
            output_lines.append(f"- Result consumed after: {summary['result_consumed_after']} ms")

        # Success indicator
        total_changes = sum(counters.values()) if counters else 0
        output_lines.append("")
        if total_changes > 0:
            output_lines.append("✅ **Query executed successfully with changes**")
        else:
            output_lines.append("✅ **Query executed successfully (no changes)**")

        result_text = "\n".join(output_lines)

        return [TextContent(
            type="text",
            text=result_text
        )]

    except Exception as e:
        error_msg = f"Failed to execute write query: {str(e)}"
        logger.error(error_msg)

        return [TextContent(
            type="text",
            text=f"❌ **Error:** {error_msg}\n\nQuery: {query}\nParameters: {params}"
        )]


# Tool definition for MCP
WRITE_TOOL = Tool(
    name="write_neo4j_cypher",
    description="Execute write Cypher queries on Neo4j database with transaction management. Supports CREATE, MERGE, SET, DELETE operations using standard Cypher syntax only (no APOC required).",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The Cypher write query to execute (CREATE, MERGE, SET, DELETE, etc.)"
            },
            "params": {
                "type": "object",
                "description": "Optional parameters for parameterized queries (e.g., {name: 'John', props: {age: 30}})",
                "default": {},
                "additionalProperties": True
            }
        },
        "required": ["query"]
    }
)