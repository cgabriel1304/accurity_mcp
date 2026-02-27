# Accurity MCP Project Memory

## Status
- MCP server: **built** (see mcp/)
- Flask backend: not started
- React frontend: not started

## Key Decisions
- Auth: Keycloak OAuth2 (Bearer token). Env vars: ACCURITY_AUTH_URL, ACCURITY_BASE_URL, ACCURITY_USERNAME, ACCURITY_PASSWORD
- Transport: MCP_TRANSPORT=stdio (default) | http. HTTP requires MCP_PORT. MCP_HOST defaults to 0.0.0.0
- Tools: read-only (search + get_by_id) for all 22 resource types
- Tool naming: search_<key> / get_<key>_by_id (snake_case keys, e.g. business_term)
- client_id for Keycloak token requests: "accurity"

## MCP Server Files
- mcp/src/accurity_mcp/server.py – FastMCP entry point, transport switching, lifespan
- mcp/src/accurity_mcp/client.py – httpx async client, token refresh logic
- mcp/src/accurity_mcp/tools/resources.py – 22-resource factory, RESOURCES list
- mcp/pyproject.toml – deps: mcp>=1.0.0, httpx, python-dotenv, uvicorn, starlette

## 22 Accurity Resources
attribute, attribute-definition, business-model-mapping, business-rule, business-term,
composite-type, custom-property, custom-property-group, data-asset, data-field,
data-set, data-source, data-structure, domain, entity, process, process-mapping,
process-step, requirement, status (Status Value), technical-data-mapping, value-type

## Ports
Flask: 5000 | React dev: 3000 | MCP: 8001 | llama.cpp: 8080
