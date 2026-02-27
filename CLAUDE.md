# Conversational BI

A microservice application that lets users query Accurity data governance resources through a natural language chat interface. Powered by a local LLM (llama.cpp), LangChain, and an Accurity MCP server.

---

## Architecture Overview

```
[React Chat UI] ──HTTP──> [Flask Backend]
                               │
                    ┌──────────┴──────────┐
                    │                     │
            [llama.cpp server]   [LangChain + MCP Adapter]
            (local LLM :8080)            │
                                  [MCP Server :8001]
                                         │
                                  [Accurity REST API]
```

**Request flow:**
1. User types a natural language query in the React chat UI
2. Flask backend receives the message
3. LangChain sends the message to the local llama.cpp LLM
4. LLM decides which MCP tools to call (search, fetch, etc.)
5. `langchain-mcp-adapters` executes the tool calls against the MCP server
6. MCP server queries the Accurity REST API
7. LLM synthesizes a natural language response, returned to the user

---

## Monorepo Structure

```
accurity_mcp/
├── mcp/                          # MCP server component
│   ├── src/
│   │   └── accurity_mcp/
│   │       ├── __init__.py
│   │       ├── server.py         # MCP server entry point
│   │       ├── client.py         # Accurity HTTP client
│   │       └── tools/            # MCP tool definitions
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── webapp/                       # Web application component
│   ├── backend/                  # Flask backend
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py         # Chat API endpoints
│   │   │   ├── agent.py          # LangChain agent setup
│   │   │   └── db.py             # SQLite chat history
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/                 # React chat UI
│       ├── src/
│       ├── public/
│       ├── package.json
│       └── Dockerfile            # Build-only, output copied to Flask static
├── docs/
│   ├── llama-docs.md
│   └── swagger/
│       ├── api-reference.md
│       └── accurity.html
├── docker-compose.yml
├── .env.example
└── CLAUDE.md
```

---

## Services & Ports

| Service       | Port | Notes                                      |
|---------------|------|--------------------------------------------|
| Flask backend | 5000 | Serves API + React production build        |
| React dev     | 3000 | Dev only (`npm start`), proxies to Flask   |
| MCP server    | 8001 | HTTP/SSE transport                         |
| llama.cpp     | 8080 | Local model server                         |

---

## Component: MCP Server (`/mcp`)

- **Language:** Python
- **SDK:** `mcp` (official Python MCP SDK)
- **Transport:** HTTP/SSE on port `8001`
- **Purpose:** Exposes Accurity Glossary API as MCP tools (search/query focused)
- **Package manager:** pip / venv
- **Testing:** pytest

### Accurity API

- **Base URL:** `$ACCURITY_BASE_URL` (default: `https://app.accurity.ai`)
- **Auth:** `ACCURITY_USERNAME` + `ACCURITY_PASSWORD` env vars
- **Reference:** [docs/swagger/api-reference.md](docs/swagger/api-reference.md)

Search endpoint pattern:
```json
POST /api/{resource}/search
{
  "startFrom": 0,
  "maxResults": 50,
  "filters": [{ "type": "SIMPLE_QUERY", "property": "name", "value": "..." }],
  "sort": { "type": "ASCENDING", "property": "name" }
}
```

---

## Component: Web Application (`/webapp`)

### Backend (Flask)

- **Framework:** Flask
- **LLM:** llama.cpp local server (`http://localhost:8080`)
- **Orchestration:** LangChain + `langchain-mcp-adapters`
- **Chat history:** SQLite (persisted per session)
- **Production:** Flask serves the compiled React build from `/static` or root

Key dependencies:
```
flask
langchain
langchain-mcp-adapters
langchain-community       # or langchain-openai-compatible for llama.cpp
sqlalchemy                # for SQLite session history
httpx
```

### Frontend (React)

- **Framework:** React (create-react-app or Vite)
- **Purpose:** Chat interface — user sends messages, displays streamed or full LLM responses
- **Dev:** `npm start` on port `3000`, proxy to Flask `5000`
- **Production:** `npm run build` outputs to `webapp/backend/app/static/` — served by Flask

---

## Local LLM (llama.cpp)

When asked to connect to a llama server, **always prompt the user** whether they want to start the local llama.cpp model first.

**Windows command:**
```
llama-server.exe -m "D:/AI/models/gemma-3-4b-it-Q4_K_M.gguf"
```

Default URL: `http://localhost:8080` — set via `LLAMA_BASE_URL` env var.

---

## Environment Variables

```
# Accurity
ACCURITY_BASE_URL=https://app.accurity.ai
ACCURITY_USERNAME=your_username
ACCURITY_PASSWORD=your_password

# LLM
LLAMA_BASE_URL=http://localhost:8080

# MCP
MCP_SERVER_URL=http://localhost:8001

# Flask
FLASK_SECRET_KEY=change_me
DATABASE_URL=sqlite:///chat_history.db
```

---

## Docker Compose

Three containers (llama.cpp runs on the host, not in Docker):

```yaml
services:
  mcp:
    build: ./mcp
    ports: ["8001:8001"]
    env_file: .env

  backend:
    build: ./webapp/backend
    ports: ["5000:5000"]
    depends_on: [mcp]
    env_file: .env
    volumes:
      - ./webapp/frontend/build:/app/static  # React build output

  frontend-builder:
    build: ./webapp/frontend
    volumes:
      - ./webapp/frontend/build:/build       # Outputs build for backend to serve
```

> llama.cpp runs natively on the host machine (GPU access). Point `LLAMA_BASE_URL` to `http://host.docker.internal:8080` when running Flask inside Docker.

---

## Development Setup

```bash
# MCP server
cd mcp && python -m venv .venv && source .venv/Scripts/activate
pip install -e ".[dev]"
python -m accurity_mcp.server

# Flask backend
cd webapp/backend && python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements.txt
flask run --port 5000

# React frontend
cd webapp/frontend && npm install && npm start

# llama.cpp (host)
llama-server.exe -m "D:/AI/models/gemma-3-4b-it-Q4_K_M.gguf"
```

---

## Testing

```bash
# MCP tests
cd mcp && pytest

# Backend tests
cd webapp/backend && pytest
```

- Unit tests mock HTTP clients — no live Accurity API or llama.cpp calls in tests
- Integration tests require `.env` credentials, marked `@pytest.mark.integration`

---

## Conventions

- MCP tool names: `snake_case` (e.g., `search_business_terms`, `get_glossary_by_id`)
- Flask routes: REST under `/api/` prefix (e.g., `POST /api/chat`)
- All MCP tools must have a `description` and typed arguments
- LangChain agent lives in `webapp/backend/app/agent.py` — keep route handlers thin
- Errors from Accurity or llama.cpp surface as structured JSON error responses, not 500s
