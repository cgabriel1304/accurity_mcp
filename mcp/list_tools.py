"""Quick script to list all tools exposed by the running MCP server.

Usage (server must already be running in HTTP mode):
    python list_tools.py
    python list_tools.py --url http://localhost:8001/sse
"""

import argparse
import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client


async def main(url: str) -> None:
    print(f"Connecting to {url} ...\n")
    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()          # required handshake
            result = await session.list_tools()
            print(f"{'Tool name':<45} Description")
            print("-" * 100)
            for tool in sorted(result.tools, key=lambda t: t.name):
                desc = (tool.description or "").split("\n")[0][:54]
                print(f"{tool.name:<45} {desc}")
            print(f"\nTotal: {len(result.tools)} tools")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:1002/sse")
    args = parser.parse_args()
    asyncio.run(main(args.url))
