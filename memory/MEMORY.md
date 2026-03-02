# Accurity MCP Project Memory

## Status
- MCP server: **built** (see mcp/)
- Flask backend: **built** (see webapp/backend/)
- React frontend: **built** (see webapp/frontend/) — Vite + React

## Key Decisions
- Auth: Keycloak OAuth2 (Bearer token). Env vars: ACCURITY_AUTH_URL, ACCURITY_BASE_URL, ACCURITY_USERNAME, ACCURITY_PASSWORD
- MCP Transport: MCP_TRANSPORT=http (port MCP_PORT). Backend connects via SSE at MCP_SERVER_URL/sse
- Tools: read-only (search + get_by_id) for all 22 resource types
- Tool naming: search_<key> / get_<key>_by_id (snake_case keys, e.g. business_term)
- client_id for Keycloak token requests: "accurity"
- LangChain agent: create_openai_tools_agent + AgentExecutor (not langgraph)
- LLM: ChatOpenAI with base_url=LLAMA_BASE_URL/v1, api_key="not-needed"
- SSE streaming: asyncio.run() in a daemon thread + queue.Queue to feed sync Flask generator
- Conversations: UUID per session, stored in localStorage, persisted in SQLite
- Frontend streaming: fetch() + ReadableStream (not EventSource, since POST is needed)

## MCP Server Files
- mcp/src/accurity_mcp/server.py – FastMCP entry point, transport switching, lifespan
- mcp/src/accurity_mcp/client.py – httpx async client, token refresh logic
- mcp/src/accurity_mcp/tools/resources.py – 22-resource factory, RESOURCES list
- mcp/pyproject.toml – deps: mcp>=1.0.0, httpx, python-dotenv, uvicorn, starlette

## Flask Backend Files
- webapp/backend/run.py – entry point
- webapp/backend/app/__init__.py – Flask app factory
- webapp/backend/app/db.py – SQLAlchemy models: Conversation, Message
- webapp/backend/app/agent.py – LangChain agent with MCP + llama.cpp, stream_agent() generator
- webapp/backend/app/routes.py – /api/chat (SSE), /api/conversations/<id>/messages, /api/conversations
- webapp/backend/requirements.txt

## React Frontend Files
- webapp/frontend/vite.config.js – dev proxy /api→:5000, build→../backend/app/static
- webapp/frontend/src/hooks/useChat.js – main state: messages, activeTools, sendMessage, startNewConversation
- webapp/frontend/src/utils/conversation.js – UUID management (localStorage)
- webapp/frontend/src/components/ChatWindow.jsx – message list + ToolStatus
- webapp/frontend/src/components/MessageBubble.jsx – user/assistant bubbles with streaming cursor
- webapp/frontend/src/components/ToolStatus.jsx – spinner pills showing active tool calls
- webapp/frontend/src/components/InputBar.jsx – textarea + send button (Enter to send)

## 22 Accurity Resources
attribute, attribute-definition, business-model-mapping, business-rule, business-term,
composite-type, custom-property, custom-property-group, data-asset, data-field,
data-set, data-source, data-structure, domain, entity, process, process-mapping,
process-step, requirement, status (Status Value), technical-data-mapping, value-type

## Ports
Flask: 5000 | React dev: 3000 | MCP: 8001 | llama.cpp: 8080

## SSE Event Protocol (agent→frontend)
{"type": "token", "content": "..."}           – LLM token
{"type": "tool_start", "tool": "...", "input": {...}} – tool invoked
{"type": "tool_end", "tool": "..."}            – tool done
{"type": "done"}                               – stream complete
{"type": "error", "message": "..."}            – error
