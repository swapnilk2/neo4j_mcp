"""Main Neo4j MCP Server implementation."""

import asyncio
import logging
from typing import Any, Sequence

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions

from .config import get_config
from .connection import Neo4jConnectionManager
from .tools.schema import get_neo4j_schema, SCHEMA_TOOL
from .tools.read import read_neo4j_cypher, READ_TOOL
from .tools.write import write_neo4j_cypher, WRITE_TOOL
from .tools.config_tool import neo4j_configure, CONFIG_TOOL


class Neo4jMCPServer:
    """Neo4j MCP Server with cross-platform support."""

    def __init__(self):
        self.server = Server("neo4j-mcp")
        self.config = get_config()
        self.connection_manager = Neo4jConnectionManager(self.config)
        self.logger = logging.getLogger(__name__)

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register MCP server handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools based on configuration."""
            tools = [CONFIG_TOOL]  # Configuration tool is always available
            if self.config.enable_schema_tool:
                tools.append(SCHEMA_TOOL)
            if self.config.enable_read_tool:
                tools.append(READ_TOOL)
            if self.config.enable_write_tool:
                tools.append(WRITE_TOOL)
            return tools

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle tool calls."""
            if arguments is None:
                arguments = {}

            self.logger.info(f"Tool called: {name} with arguments: {arguments}")

            try:
                if name == "neo4j_configure":
                    action = arguments.get("action")
                    tool = arguments.get("tool")

                    if not action:
                        raise ValueError("Action parameter is required")

                    return await neo4j_configure(self, action, tool)

                elif name == "get_neo4j_schema" and self.config.enable_schema_tool:
                    return await get_neo4j_schema(self.connection_manager)

                elif name == "read_neo4j_cypher" and self.config.enable_read_tool:
                    query = arguments.get("query")
                    params = arguments.get("params", {})

                    if not query:
                        raise ValueError("Query parameter is required")

                    return await read_neo4j_cypher(self.connection_manager, query, params)

                elif name == "write_neo4j_cypher" and self.config.enable_write_tool:
                    query = arguments.get("query")
                    params = arguments.get("params", {})

                    if not query:
                        raise ValueError("Query parameter is required")

                    return await write_neo4j_cypher(self.connection_manager, query, params)

                else:
                    raise ValueError(f"Tool '{name}' is not available or has been disabled")

            except Exception as e:
                error_msg = f"Error executing tool '{name}': {str(e)}"
                self.logger.error(error_msg)
                return [types.TextContent(type="text", text=f"Error: {error_msg}")]

    async def run(self):
        """Run the MCP server."""
        try:
            self.logger.info("Starting Neo4j MCP Server...")

            # Run the server (connection will be established on first use)
            from mcp.server.stdio import stdio_server

            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="neo4j-mcp",
                        server_version="1.0.0",
                        capabilities=types.ServerCapabilities(
                            tools=types.ToolsCapability(listChanged=False),
                        ),
                    ),
                )
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
            raise
        finally:
            await self.connection_manager.close()

    async def shutdown(self):
        """Shutdown the server gracefully."""
        self.logger.info("Shutting down Neo4j MCP Server...")
        await self.connection_manager.close()


async def main():
    """Main entry point for the server."""
    # Setup rich logging based on user preference
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    server = Neo4jMCPServer()

    try:
        await server.run()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        logging.error(f"Server failed: {str(e)}")
        raise
    finally:
        await server.shutdown()


if __name__ == "__main__":
    asyncio.run(main())