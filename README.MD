# Accurity Conversational BI

A microservice application that lets users query Accurity data governance resources through a natural language chat interface. Powered by a local LLM (llama.cpp), LangChain, and an Accurity MCP server.

---

## Architecture

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

---

## Project Structure

```
accurity_mcp/
├── mcp/                          # MCP server — exposes Accurity API as LLM tools
│   ├── src/accurity_mcp/
│   │   ├── server.py             # Entry point, transport switching
│   │   ├── client.py             # Keycloak OAuth2 + Accurity HTTP client
│   │   └── tools/resources.py   # 44 tools across 22 resource types
│   ├── tests/
│   └── pyproject.toml
├── webapp/
│   ├── backend/                  # Flask API + serves React build in production
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── db.py             # SQLite chat history (SQLAlchemy)
│   │   │   ├── agent.py          # LangChain agent (llama.cpp + MCP tools)
│   │   │   └── routes.py         # /api/chat (SSE), /api/conversations
│   │   ├── requirements.txt
│   │   └── run.py
│   └── frontend/                 # React chat UI (Vite)
│       ├── src/
│       ├── .env                  # VITE_PORT, VITE_BACKEND_URL
│       └── vite.config.js
├── docs/
├── .env                          # Root env — credentials + service config (gitignored)
├── .env.example                  # Template — copy to .env and fill in
└── docker-compose.yml
```

---

## Environment Variables

### Root `.env` — shared by MCP server and Flask backend

| Variable             | Default                          | Description                                  |
|----------------------|----------------------------------|----------------------------------------------|
| `ACCURITY_BASE_URL`  | `https://app.accurity.ai`        | Accurity REST API base URL                   |
| `ACCURITY_AUTH_URL`  | *(required)*                     | Keycloak token endpoint                      |
| `ACCURITY_USERNAME`  | *(required)*                     | Accurity login username                      |
| `ACCURITY_PASSWORD`  | *(required)*                     | Accurity login password                      |
| `MCP_TRANSPORT`      | `http`                           | `stdio` or `http`                            |
| `MCP_PORT`           | `8001`                           | MCP server port (when `MCP_TRANSPORT=http`)  |
| `MCP_HOST`           | `0.0.0.0`                        | MCP server bind host                         |
| `MCP_SERVER_URL`     | `http://localhost:8001`          | URL Flask uses to reach the MCP server       |
| `LLAMA_BASE_URL`     | `http://localhost:8080`          | llama.cpp OpenAI-compatible API base URL     |
| `LLM_MODEL`          | `local`                          | Model name forwarded to ChatOpenAI           |
| `LLM_TEMPERATURE`    | `0`                              | Sampling temperature                         |
| `FLASK_HOST`         | `0.0.0.0`                        | Flask bind host                              |
| `FLASK_PORT`         | `5000`                           | Flask listen port                            |
| `FLASK_DEBUG`        | `false`                          | Enable Flask debug/reloader                  |
| `FLASK_SECRET_KEY`   | *(required in prod)*             | Flask session signing key                    |
| `DATABASE_URL`       | `sqlite:///chat_history.db`      | SQLAlchemy DB URL                            |

### `webapp/frontend/.env` — Vite dev server only

| Variable            | Default                   | Description                              |
|---------------------|---------------------------|------------------------------------------|
| `VITE_PORT`         | `3000`                    | React dev server port                    |
| `VITE_BACKEND_URL`  | `http://localhost:5000`   | Flask backend to proxy `/api` calls to   |

---

## Development Setup

All four services run in separate terminals. Start them in this order.

### 0. Configuration

```bash
# Copy the template and fill in your Accurity credentials
cp .env.example .env
```

Edit `.env` and set `ACCURITY_AUTH_URL`, `ACCURITY_USERNAME`, and `ACCURITY_PASSWORD`.

---

### 1. llama.cpp (local LLM)

Run the model server on your host machine (GPU access). You must use an **instruction-tuned** model — look for `instruct` or `it` in the filename (e.g. `Instruct`, `it-Q4`).

```bash
# Example — adjust the path to your llama.cpp binary and model file
D:\AI\llama-b8172-bin-win-cuda-12.4-x64\llama-server.exe \
  -m "D:\AI\models\Meta-Llama-3.1-8B-Instruct-IQ2_M.gguf" \
  -ngl 35
```

`-ngl 35` offloads 35 layers to the GPU — raise or lower this based on your VRAM. Omit it entirely to run on CPU only.

Listens on `http://localhost:8080` by default. Change `LLAMA_BASE_URL` in `.env` to override.

---

### 2. MCP Server

```bash
cd mcp

# Create virtual environment
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate
# Activate — macOS/Linux
# source .venv/bin/activate

# Install (includes dev extras: pytest, respx)
pip install -e ".[dev]"

# Start (reads MCP_TRANSPORT, MCP_PORT, MCP_HOST from root .env)
python -m accurity_mcp.server
```

Run tests:

```bash
pytest
```

---

### 3. Flask Backend

```bash
cd webapp/backend

# Create virtual environment
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate
# Activate — macOS/Linux
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start (reads FLASK_HOST, FLASK_PORT, FLASK_DEBUG from root .env)
python run.py
```

Listens on `FLASK_HOST:FLASK_PORT` (default `0.0.0.0:5000`).
Set `FLASK_DEBUG=true` in `.env` to enable hot reload.

---

### 4. React Frontend (dev server)

```bash
cd webapp/frontend

# Install dependencies
npm install

# Start dev server (reads VITE_PORT, VITE_BACKEND_URL from webapp/frontend/.env)
npm run dev
```

Listens on `VITE_PORT` (default `3000`). All `/api/*` requests are proxied to `VITE_BACKEND_URL`.

Open **http://localhost:3000** in your browser.

---

## Production Deployment

In production, Flask serves both the API and the compiled React bundle — no separate frontend process needed.

### 1. Build the frontend

```bash
cd webapp/frontend
npm install
npm run build
```

Outputs the compiled app to `webapp/backend/app/static/`.

### 2. Configure the environment

Update the root `.env`:

```dotenv
FLASK_DEBUG=false
FLASK_SECRET_KEY=<strong-random-value>
```

### 3. Start the MCP server

```bash
cd mcp

# Activate — Windows
.venv\Scripts\activate
# Activate — macOS/Linux
# source .venv/bin/activate

python -m accurity_mcp.server
```

### 4. Start Flask (serves API + React)

```bash
cd webapp/backend

# Activate — Windows
.venv\Scripts\activate
# Activate — macOS/Linux
# source .venv/bin/activate

python run.py
```

Open **http://localhost:5000** (or whatever `FLASK_PORT` is set to).

> For a production-grade deployment, run Flask behind **gunicorn**:
> ```bash
> pip install gunicorn
> gunicorn -w 2 -b 0.0.0.0:5000 "app:create_app()"
> ```

---

## Docker Compose (optional)

llama.cpp runs on the host for GPU access. Everything else runs in containers:

```bash
docker compose up --build
```

When running inside Docker, override in `.env`:

```dotenv
LLAMA_BASE_URL=http://host.docker.internal:8080
MCP_SERVER_URL=http://mcp:8001
```

---

## MCP Tools

The MCP server exposes **44 tools** — `search_<resource>` and `get_<resource>_by_id` — for all 22 Accurity resource types:

`attribute`, `attribute_definition`, `business_model_mapping`, `business_rule`, `business_term`, `composite_type`, `custom_property`, `custom_property_group`, `data_asset`, `data_field`, `data_set`, `data_source`, `data_structure`, `domain`, `entity`, `process`, `process_mapping`, `process_step`, `requirement`, `status_value`, `technical_data_mapping`, `value_type`

