"""Neo4j MCP configuration management tool."""

import logging
from typing import Any, Dict, Optional

from mcp.types import Tool, TextContent


logger = logging.getLogger(__name__)


async def neo4j_configure(
    server_instance: Any,
    action: str,
    tool: Optional[str] = None,
    status: Optional[str] = None
) -> list[TextContent]:
    """
    Configure Neo4j MCP server settings at runtime.

    Args:
        server_instance: The Neo4jMCPServer instance
        action: Action to perform - "status", "enable", "disable", "list"
        tool: Tool to configure - "schema", "read", "write"
        status: Status to set - "true", "false" (for enable/disable actions)

    Returns:
        List of TextContent with configuration results
    """
    try:
        config = server_instance.config

        if action == "status":
            # Show current configuration status
            output_lines = []
            output_lines.append("# Neo4j MCP Server Configuration Status")
            output_lines.append("")
            output_lines.append("## Connection Settings")
            output_lines.append(f"- **URI**: {config.uri}")
            output_lines.append(f"- **User**: {config.user}")
            output_lines.append(f"- **Database**: {config.database}")
            output_lines.append("")
            output_lines.append("## Tool Status")

            schema_status = "[ENABLED]" if config.enable_schema_tool else "[DISABLED]"
            read_status = "[ENABLED]" if config.enable_read_tool else "[DISABLED]"
            write_status = "[ENABLED]" if config.enable_write_tool else "[DISABLED]"

            output_lines.append(f"- **Schema Tool** (`get_neo4j_schema`): {schema_status}")
            output_lines.append(f"- **Read Tool** (`read_neo4j_cypher`): {read_status}")
            output_lines.append(f"- **Write Tool** (`write_neo4j_cypher`): {write_status}")

            output_lines.append("")
            output_lines.append("## Quick Commands")
            output_lines.append("- **Disable writes**: Use tool `neo4j_configure` with `action=disable, tool=write`")
            output_lines.append("- **Enable writes**: Use tool `neo4j_configure` with `action=enable, tool=write`")
            output_lines.append("- **Check status**: Use tool `neo4j_configure` with `action=status`")

            return [TextContent(type="text", text="\n".join(output_lines))]

        elif action == "enable":
            if not tool:
                return [TextContent(type="text", text="Error: 'tool' parameter required for enable action. Use: schema, read, or write")]

            if tool == "schema":
                config.enable_schema_tool = True
                msg = "[SUCCESS] **Schema tool enabled** - `get_neo4j_schema` is now available"
            elif tool == "read":
                config.enable_read_tool = True
                msg = "[SUCCESS] **Read tool enabled** - `read_neo4j_cypher` is now available"
            elif tool == "write":
                config.enable_write_tool = True
                msg = "[SUCCESS] **Write tool enabled** - `write_neo4j_cypher` is now available"
            else:
                return [TextContent(type="text", text=f"Error: Unknown tool '{tool}'. Use: schema, read, or write")]

            return [TextContent(type="text", text=msg)]

        elif action == "disable":
            if not tool:
                return [TextContent(type="text", text="Error: 'tool' parameter required for disable action. Use: schema, read, or write")]

            if tool == "schema":
                config.enable_schema_tool = False
                msg = "[DISABLED] **Schema tool disabled** - `get_neo4j_schema` is no longer available"
            elif tool == "read":
                config.enable_read_tool = False
                msg = "[DISABLED] **Read tool disabled** - `read_neo4j_cypher` is no longer available"
            elif tool == "write":
                config.enable_write_tool = False
                msg = "[DISABLED] **Write tool disabled** - `write_neo4j_cypher` is no longer available"
            else:
                return [TextContent(type="text", text=f"Error: Unknown tool '{tool}'. Use: schema, read, or write")]

            return [TextContent(type="text", text=msg)]

        elif action == "list":
            # List available tools
            tools = []
            if config.enable_schema_tool:
                tools.append("[ENABLED] get_neo4j_schema")
            else:
                tools.append("[DISABLED] get_neo4j_schema")

            if config.enable_read_tool:
                tools.append("[ENABLED] read_neo4j_cypher")
            else:
                tools.append("[DISABLED] read_neo4j_cypher")

            if config.enable_write_tool:
                tools.append("[ENABLED] write_neo4j_cypher")
            else:
                tools.append("[DISABLED] write_neo4j_cypher")

            output_lines = []
            output_lines.append("# Available Neo4j Tools")
            output_lines.append("")
            for tool_status in tools:
                output_lines.append(f"- {tool_status}")

            return [TextContent(type="text", text="\n".join(output_lines))]

        else:
            return [TextContent(type="text", text=f"Error: Unknown action '{action}'. Use: status, enable, disable, or list")]

    except Exception as e:
        error_msg = f"Failed to configure server: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=f"Error: {error_msg}")]


# Tool definition for MCP
CONFIG_TOOL = Tool(
    name="neo4j_configure",
    description="Runtime configuration for Neo4j MCP server. Manage tool availability, check connection status, and control access permissions. Uses plain Cypher queries only - no APOC dependencies.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "Action to perform: 'status' (show current config), 'enable' (enable specific tool), 'disable' (disable specific tool), 'list' (show available tools)",
                "enum": ["status", "enable", "disable", "list"]
            },
            "tool": {
                "type": "string",
                "description": "Tool to configure: 'schema' (schema introspection), 'read' (read queries), 'write' (write queries)",
                "enum": ["schema", "read", "write"]
            }
        },
        "required": ["action"]
    }
)