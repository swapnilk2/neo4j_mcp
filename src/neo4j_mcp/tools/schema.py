"""Neo4j schema introspection tool."""

import logging
from typing import Any, Dict

from mcp.types import Tool, TextContent

from ..connection import Neo4jConnectionManager


logger = logging.getLogger(__name__)


async def get_neo4j_schema(connection_manager: Neo4jConnectionManager) -> list[TextContent]:
    """
    Get comprehensive schema information from the Neo4j database.

    This tool lists all node labels, relationship types, and database structure using
    standard Neo4j procedures only. No APOC plugin required - uses plain Cypher queries.

    Args:
        connection_manager: Neo4jConnectionManager instance

    Returns:
        List of TextContent with schema information including:
        - Node labels and counts
        - Relationship types
        - Basic schema structure
        Note: For detailed property information, APOC plugin would be needed (optional)
    """
    try:
        schema_info = await connection_manager.get_schema_info()

        # Format the schema information
        output_lines = []
        output_lines.append("# Neo4j Database Schema")
        output_lines.append("")

        # Check if we have basic or detailed schema info
        has_detailed_props = schema_info.get("nodes") and any(
            node.get("properties") for node in schema_info["nodes"]
        )

        # Node labels and properties
        if schema_info.get("nodes"):
            output_lines.append("## Node Labels")
            if has_detailed_props:
                output_lines.append("(With Properties)")
            output_lines.append("")

            for node_info in schema_info["nodes"]:
                label = node_info.get("label", "Unknown")
                properties = node_info.get("properties", [])

                if has_detailed_props and properties:
                    output_lines.append(f"### {label}")
                    output_lines.append("Properties:")
                    for prop in properties:
                        prop_name = prop.get("property", "unknown")
                        prop_types = prop.get("types", [])
                        mandatory = prop.get("mandatory", False)
                        mandatory_str = " (mandatory)" if mandatory else ""
                        types_str = ", ".join(prop_types) if prop_types else "unknown"
                        output_lines.append(f"  - {prop_name}: {types_str}{mandatory_str}")
                    output_lines.append("")
                else:
                    output_lines.append(f"- **{label}**")

        # Relationship types and properties
        if schema_info.get("relationships"):
            output_lines.append("")
            output_lines.append("## Relationship Types")
            if has_detailed_props:
                output_lines.append("(With Properties)")
            output_lines.append("")

            for rel_info in schema_info["relationships"]:
                rel_type = rel_info.get("relationshipType", "Unknown")
                properties = rel_info.get("properties", [])

                if has_detailed_props and properties:
                    output_lines.append(f"### {rel_type}")
                    output_lines.append("Properties:")
                    for prop in properties:
                        prop_name = prop.get("property", "unknown")
                        prop_types = prop.get("types", [])
                        mandatory = prop.get("mandatory", False)
                        mandatory_str = " (mandatory)" if mandatory else ""
                        types_str = ", ".join(prop_types) if prop_types else "unknown"
                        output_lines.append(f"  - {prop_name}: {types_str}{mandatory_str}")
                    output_lines.append("")
                else:
                    output_lines.append(f"- **{rel_type}**")

        # Node counts if available (from basic fallback)
        if schema_info.get("counts"):
            output_lines.append("")
            output_lines.append("## Node Counts by Label")
            output_lines.append("")
            for count_info in schema_info["counts"]:
                labels = count_info.get("labels", [])
                count = count_info.get("count", 0)
                label_str = ":".join(labels) if labels else "Unknown"
                output_lines.append(f"- **{label_str}**: {count:,} nodes")

        # Full schema visualization if available
        if schema_info.get("schema") and len(schema_info["schema"]) > 0:
            output_lines.append("")
            output_lines.append("## Schema Visualization")
            output_lines.append("")
            output_lines.append("```json")
            import json
            # Limit output size for readability
            schema_data = schema_info["schema"][:5] if len(schema_info["schema"]) > 5 else schema_info["schema"]
            output_lines.append(json.dumps(schema_data, indent=2))
            if len(schema_info["schema"]) > 5:
                output_lines.append(f"\n... and {len(schema_info['schema']) - 5} more items")
            output_lines.append("```")

        # Add helpful note about functionality
        output_lines.append("")
        output_lines.append("## About This Schema")
        output_lines.append("Generated using **standard Neo4j procedures only** - no APOC plugin required.")
        output_lines.append("Provides complete database structure: labels, relationships, counts, and schema visualization.")
        output_lines.append("Compatible with all Neo4j versions and deployments.")

        schema_text = "\n".join(output_lines)

        return [TextContent(
            type="text",
            text=schema_text
        )]

    except Exception as e:
        error_msg = f"Failed to retrieve schema information: {str(e)}"
        logger.error(error_msg)

        return [TextContent(
            type="text",
            text=f"Error: {error_msg}\n\nNote: This tool uses plain Cypher queries only (no APOC required). Error may be due to connection or database access issues."
        )]


# Tool definition for MCP
SCHEMA_TOOL = Tool(
    name="get_neo4j_schema",
    description="Get Neo4j database schema using plain Cypher queries only (no APOC required). Lists node labels, relationship types, counts, and basic structure. Works with any Neo4j database.",
    inputSchema={
        "type": "object",
        "properties": {},
        "required": []
    }
)