FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir -e .

# Disable Python output buffering so logs reach Docker immediately
ENV PYTHONUNBUFFERED=1

# Default to HTTP transport; override at runtime with -e MCP_TRANSPORT=stdio
ENV MCP_TRANSPORT=http
ENV MCP_HOST=127.0.0.1
ENV MCP_PORT=8001

EXPOSE 8001

CMD ["accurity-mcp"]
