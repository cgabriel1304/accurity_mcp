"""Accurity MCP server entry point.

Transport is controlled by the MCP_TRANSPORT environment variable:

    MCP_TRANSPORT=stdio   (default) – standard-input/output, for direct LLM tool use
    MCP_TRANSPORT=http    – SSE over HTTP; MCP_PORT must also be set

Example:
    # stdio (used by LangChain MCP adapters, Claude Desktop, etc.)
    python -m accurity_mcp.server

    # HTTP/SSE
    MCP_TRANSPORT=http MCP_PORT=8001 python -m accurity_mcp.server
"""

from __future__ import annotations

import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from accurity_mcp.client import AccurityClient
from accurity_mcp.tools import register_all_tools

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Validate required env vars early so failures are obvious
# ---------------------------------------------------------------------------
_REQUIRED_ENV = [
    "ACCURITY_BASE_URL",
    "ACCURITY_AUTH_URL",
    "ACCURITY_USERNAME",
    "ACCURITY_PASSWORD",
]


def _check_env() -> None:
    missing = [v for v in _REQUIRED_ENV if not os.getenv(v)]
    if missing:
        sys.exit(f"[accurity-mcp] Missing required environment variables: {', '.join(missing)}")


# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

_client: AccurityClient | None = None


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[None]:
    global _client
    logger.info("MCP server starting — connecting to Accurity at %s", os.getenv("ACCURITY_BASE_URL"))
    _client = AccurityClient()
    try:
        yield
    except Exception:
        logger.exception("Unhandled error in MCP server lifespan")
        raise
    finally:
        logger.info("MCP server shutting down")
        if _client is not None:
            await _client.aclose()


# Read host early so FastMCP initialises the DNS-rebinding policy correctly.
# When MCP_HOST=0.0.0.0 (Docker/network), auto-protection is NOT triggered, so
# other containers can connect freely.  When MCP_HOST=127.0.0.1 (local dev),
# auto-protection IS enabled, restricting connections to localhost origins.
mcp = FastMCP("accurity-mcp", lifespan=lifespan, host=os.getenv("MCP_HOST", "127.0.0.1"))


def _register_tools() -> None:
    """Register tools after the lifespan has started.

    Because _client is set during lifespan, tools must close over a callable
    that dereferences _client at call time — we achieve this by passing a
    proxy that always reads the module-level variable.
    """
    # We use a thin proxy so tools always reference the live client instance
    # that is set during lifespan startup.
    class _ClientProxy:
        """Delegates every attribute access to the module-level _client."""

        def __getattr__(self, name: str):
            if _client is None:
                raise RuntimeError("AccurityClient not initialised (lifespan not started)")
            return getattr(_client, name)

    register_all_tools(mcp, _ClientProxy())  # type: ignore[arg-type]


_register_tools()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    _check_env()

    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()

    if transport == "http":
        port_str = os.getenv("MCP_PORT")
        if not port_str:
            sys.exit("[accurity-mcp] MCP_PORT must be set when MCP_TRANSPORT=http")
        try:
            port = int(port_str)
        except ValueError:
            sys.exit(f"[accurity-mcp] MCP_PORT must be an integer, got: {port_str!r}")

        host = os.getenv("MCP_HOST", "127.0.0.1")
        mcp.settings.port = port
        print(f"[accurity-mcp] Starting HTTP/SSE server on {host}:{port}", flush=True)
        mcp.run(transport="sse")

    elif transport == "stdio":
        mcp.run(transport="stdio")

    else:
        sys.exit(f"[accurity-mcp] Unknown MCP_TRANSPORT value: {transport!r}. Use 'stdio' or 'http'.")


if __name__ == "__main__":
    main()
