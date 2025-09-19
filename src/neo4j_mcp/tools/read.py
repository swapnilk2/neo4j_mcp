"""Neo4j read query execution tool."""

import json
import logging
from typing import Any, Dict, Optional

from mcp.types import Tool, TextContent

from ..connection import Neo4jConnectionManager


logger = logging.getLogger(__name__)


async def read_neo4j_cypher(
    connection_manager: Neo4jConnectionManager,
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> list[TextContent]:
    """
    Execute a read Cypher query on the Neo4j database.

    Args:
        connection_manager: Neo4jConnectionManager instance
        query: The Cypher query to execute
        params: Optional parameters to pass to the Cypher query

    Returns:
        List of TextContent with query results
    """
    try:
        # Validate that this is likely a read-only query
        query_lower = query.strip().lower()
        write_keywords = []#['create', 'merge', 'delete', 'remove', 'set', 'detach delete']

        if any(keyword in query_lower for keyword in write_keywords):
            logger.warning(f"Query contains write operations: {query}")
            return [TextContent(
                type="text",
                text="Warning: This query appears to contain write operations. Use write_neo4j_cypher for write queries."
            )]

        # Execute the read query
        results = await connection_manager.execute_read_query(query, params)

        # Format results
        output_lines = []
        output_lines.append(f"# Query Results")
        output_lines.append("")
        output_lines.append(f"**Query:** `{query}`")

        if params:
            output_lines.append(f"**Parameters:** `{json.dumps(params, indent=2)}`")

        output_lines.append(f"**Records returned:** {len(results)}")
        output_lines.append("")

        if results:
            # Show results in a formatted way
            output_lines.append("## Results")
            output_lines.append("")

            # If results are small, show them nicely formatted
            if len(results) <= 100:
                output_lines.append("```json")
                output_lines.append(json.dumps(results, indent=2, default=str))
                output_lines.append("```")
            else:
                # For large results, show first few records and summary
                output_lines.append("**First 10 records:**")
                output_lines.append("```json")
                output_lines.append(json.dumps(results[:10], indent=2, default=str))
                output_lines.append("```")
                output_lines.append("")
                output_lines.append(f"**Note:** Showing first 10 of {len(results)} total records.")

                # Show column summary if available
                if results:
                    columns = list(results[0].keys())
                    output_lines.append(f"**Columns:** {', '.join(columns)}")

        else:
            output_lines.append("## Results")
            output_lines.append("No records returned.")

        result_text = "\n".join(output_lines)

        return [TextContent(
            type="text",
            text=result_text
        )]

    except Exception as e:
        error_msg = f"Failed to execute read query: {str(e)}"
        logger.error(error_msg)

        return [TextContent(
            type="text",
            text=f"Error: {error_msg}\n\nQuery: {query}\nParameters: {params}"
        )]


# Tool definition for MCP
READ_TOOL = Tool(
    name="read_neo4j_cypher",
    description="Execute read-only Cypher queries on Neo4j database. Supports standard Cypher syntax and parameterized queries. No APOC procedures required - uses plain Cypher only.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The Cypher query to execute (read-only operations like MATCH, RETURN, WITH, etc.)"
            },
            "params": {
                "type": "object",
                "description": "Optional parameters for parameterized queries (e.g., {name: 'John', age: 30})",
                "default": {},
                "additionalProperties": True
            }
        },
        "required": ["query"]
    }
)