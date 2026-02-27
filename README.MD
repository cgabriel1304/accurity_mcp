MCP Server — File Summary

mcp/
├── src/accurity_mcp/
│   ├── __init__.py
│   ├── server.py        ← entry point, transport switching
│   ├── client.py        ← Keycloak OAuth2 + Accurity HTTP client
│   └── tools/
│       ├── __init__.py
│       └── resources.py ← 44 tools across 22 resource types
├── tests/
│   ├── test_client.py   ← token lifecycle, search, get_by_id (respx mocks)
│   └── test_tools.py    ← tool behaviour, error surfacing, coverage checks
├── pyproject.toml
└── Dockerfile
.env.example             ← updated with all new vars
Key design points:

Concern	Approach
Transport	MCP_TRANSPORT=stdio (default) or MCP_TRANSPORT=http + MCP_PORT required
Auth	Keycloak OAuth2 — fetches Bearer token, auto-refreshes 30s before expiry, falls back to re-auth if refresh token also expired
Tools	44 total: search_<resource> + get_<resource>_by_id for all 22 resource types, read-only
Errors	Caught inside tool functions and returned as {"error": "..."} JSON — never crash the agent
HTTP transport	FastMCP SSE (mcp.run(transport="sse", host=..., port=...))
To run locally:


cd mcp
python -m venv .venv && source .venv/Scripts/activate
pip install -e ".[dev]"

# stdio
python -m accurity_mcp.server

# HTTP/SSE
MCP_TRANSPORT=http MCP_PORT=8001 python -m accurity_mcp.server

# tests
pytest