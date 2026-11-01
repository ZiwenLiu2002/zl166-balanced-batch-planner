import os
from pathlib import Path

import anyio
from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from slimconfig import build_output, output_schema, plain_output

from contract import TOOLS, Tool
from plugin import evaluate_partition, solve_partition

server = Server("zl166-balanced-batch-planner")
WORKSPACE_ENV = "NANOAGENT_WORKSPACE"
IMPLEMENTATIONS = {Tool.EVALUATE_PARTITION: evaluate_partition, Tool.SOLVE_PARTITION: solve_partition}


@server.list_tools()
async def list_tools():
    return [types.Tool(name=tool.value, inputSchema=output_schema(given), outputSchema=output_schema(made)) for tool, (given, made) in TOOLS.items()]


@server.call_tool()
async def call_tool(name, arguments):
    tool = Tool(name)
    given, made = TOOLS[tool]
    output = IMPLEMENTATIONS[tool](build_output(arguments, given), Path(os.environ[WORKSPACE_ENV]))
    if not isinstance(output, made):
        raise TypeError(f"{name} returned {type(output).__name__}, not {made.__name__}")
    return plain_output(output)


def main():
    if WORKSPACE_ENV not in os.environ:
        raise SystemExit(f"{WORKSPACE_ENV} is not set")

    async def run():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    anyio.run(run)


if __name__ == "__main__":
    main()
