"""LangChain agent backed by a local llama.cpp LLM and the Accurity MCP server.

The agent uses the OpenAI-compatible API exposed by llama.cpp and connects to
the MCP server via HTTP/SSE to get Accurity tools at runtime.

The public interface is `stream_agent()`, a synchronous generator that yields
SSE-formatted lines for a Flask streaming response.

SSE event types sent downstream:
    {"type": "token",      "content": "..."}        – LLM output token
    {"type": "tool_start", "tool": "...", "input": {...}} – tool call started
    {"type": "tool_end",   "tool": "..."}             – tool call finished
    {"type": "done"}                                  – stream complete
    {"type": "error",      "message": "..."}          – unrecoverable error
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import queue
import threading
from typing import Generator

logger = logging.getLogger(__name__)

from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv(find_dotenv(usecwd=False))

# ---------------------------------------------------------------------------
# Config from environment
# ---------------------------------------------------------------------------

LLAMA_BASE_URL: str = os.getenv("LLAMA_BASE_URL", "http://localhost:8080")
MCP_SERVER_URL: str = os.getenv("MCP_SERVER_URL", "http://localhost:8001")
LLM_MODEL: str = os.getenv("LLM_MODEL", "local")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0"))

SYSTEM_PROMPT = (
    "You are a helpful data governance assistant with access to the Accurity data catalog. "
    "You can search for and retrieve information about business terms, data assets, domains, "
    "data sources, data structures, attributes, business rules, entities, processes, "
    "requirements, and many other governance resources.\n\n"
    "When the user asks about data governance topics, use the available tools to find "
    "accurate information from the catalog. Always base your answers on what you find — "
    "do not guess or fabricate catalog content.\n\n"
    "If you need to search, do so before answering. Summarise the results clearly for "
    "the user in plain language."
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_llm() -> ChatOpenAI:
    return ChatOpenAI(
        base_url=f"{LLAMA_BASE_URL}/v1",
        api_key="not-needed",  # llama.cpp does not require an API key
        model=LLM_MODEL,
        streaming=True,
        temperature=LLM_TEMPERATURE,
    )


def _to_langchain_history(history: list[dict]) -> list:
    """Convert a list of {'role': ..., 'content': ...} dicts to LangChain messages."""
    result = []
    for msg in history:
        if msg["role"] == "user":
            result.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            result.append(AIMessage(content=msg["content"]))
    return result


# ---------------------------------------------------------------------------
# Async agent runner
# ---------------------------------------------------------------------------


async def _run_agent(
    message: str,
    history: list[dict],
    out_queue: queue.Queue,
) -> None:
    """Connect to MCP, build the agent, run it, and push SSE events to out_queue."""
    logger.info("Agent run started | message=%r", message[:120])
    try:
        mcp_client = MultiServerMCPClient(
            {
                "accurity": {
                    "url": f"{MCP_SERVER_URL}/sse",
                    "transport": "sse",
                }
            }
        )
        tools = await mcp_client.get_tools()
        llm = _build_llm()
        agent = create_react_agent(llm, tools)

        lc_history = _to_langchain_history(history)
        if lc_history:
            # System prompt is already embedded in the first message of history
            messages = [*lc_history, HumanMessage(content=message)]
        else:
            # Fresh conversation: embed system prompt in the first user message
            # (Gemma's chat template requires strict user/assistant alternation
            # and does not support a separate "system" role)
            messages = [HumanMessage(content=f"{SYSTEM_PROMPT}\n\n{message}")]

        async for event in agent.astream_events({"messages": messages}, version="v2"):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                chunk = event["data"].get("chunk")
                content = getattr(chunk, "content", None) if chunk else None
                if content:
                    out_queue.put({"type": "token", "content": content})

            elif kind == "on_tool_start":
                logger.debug("Tool start | tool=%s input=%s", event["name"], event["data"].get("input", {}))
                out_queue.put(
                    {
                        "type": "tool_start",
                        "tool": event["name"],
                        "input": event["data"].get("input", {}),
                    }
                )

            elif kind == "on_tool_end":
                logger.debug("Tool end   | tool=%s", event["name"])
                out_queue.put({"type": "tool_end", "tool": event["name"]})

    except Exception as exc:  # noqa: BLE001
        # ExceptionGroup (Python 3.11+) wraps TaskGroup sub-exceptions — unwrap to get the real cause
        if hasattr(exc, "exceptions"):
            msg = "; ".join(str(e) for e in exc.exceptions)
            logger.error("Agent error (ExceptionGroup): %s", msg, exc_info=exc)
        else:
            msg = str(exc)
            logger.error("Agent error: %s", msg, exc_info=exc)
        out_queue.put({"type": "error", "message": msg})
    else:
        logger.info("Agent run completed successfully")
    finally:
        out_queue.put(None)  # sentinel — tells the generator to stop


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------


def stream_agent(
    message: str,
    history: list[dict],
) -> Generator[str, None, None]:
    """Synchronous SSE generator — safe to use directly in a Flask route.

    Starts the async agent in a daemon thread so Flask's WSGI server is not
    blocked.  Each yielded string is a complete ``data: ...\\n\\n`` SSE line.
    """
    out_queue: queue.Queue = queue.Queue()

    def _thread_target() -> None:
        asyncio.run(_run_agent(message, history, out_queue))

    thread = threading.Thread(target=_thread_target, daemon=True)
    thread.start()

    while True:
        try:
            item = out_queue.get(timeout=120)
        except queue.Empty:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Agent timed out'})}\n\n"
            break

        if item is None:
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            break

        yield f"data: {json.dumps(item)}\n\n"
