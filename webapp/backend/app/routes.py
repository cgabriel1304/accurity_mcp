import json
import logging
import uuid

from flask import Blueprint, Response, jsonify, request, stream_with_context

from .agent import stream_agent
from .db import Conversation, Message, db

logger = logging.getLogger(__name__)

bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True) or {}
    message: str = (data.get("message") or "").strip()
    conversation_id: str = data.get("conversation_id") or str(uuid.uuid4())

    if not message:
        return jsonify({"error": "message is required"}), 400

    # Ensure conversation row exists
    conv = db.session.get(Conversation, conversation_id)
    if conv is None:
        conv = Conversation(id=conversation_id)
        db.session.add(conv)
        db.session.commit()

    # Persist the user message immediately
    db.session.add(Message(conversation_id=conversation_id, role="user", content=message))
    db.session.commit()

    # Build history (all messages before the one we just added)
    prior_messages = (
        Message.query.filter_by(conversation_id=conversation_id)
        .order_by(Message.created_at)
        .all()
    )
    history = [{"role": m.role, "content": m.content} for m in prior_messages[:-1]]

    # Accumulate assistant tokens so we can persist the full response
    response_tokens: list[str] = []

    def generate():
        for sse_line in stream_agent(message, history):
            # Parse each event to accumulate the final response
            try:
                raw = sse_line
                if raw.startswith("data: "):
                    raw = raw[6:]
                evt = json.loads(raw.strip())
                if evt.get("type") == "token":
                    response_tokens.append(evt.get("content", ""))
                elif evt.get("type") == "error":
                    logger.error("SSE error event received: %s", evt.get("message"))
                    full = "".join(response_tokens).strip()
                    if full:
                        db.session.add(
                            Message(
                                conversation_id=conversation_id,
                                role="assistant",
                                content=full,
                            )
                        )
                        db.session.commit()
                elif evt.get("type") == "done":
                    # Persist assistant message at end of stream
                    full = "".join(response_tokens).strip()
                    if full:
                        db.session.add(
                            Message(
                                conversation_id=conversation_id,
                                role="assistant",
                                content=full,
                            )
                        )
                        db.session.commit()
            except Exception:  # noqa: BLE001
                logger.exception("Failed to parse SSE line: %r", sse_line)

            yield sse_line

    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
        "X-Conversation-Id": conversation_id,
    }
    return Response(stream_with_context(generate()), headers=headers)


# ---------------------------------------------------------------------------
# Conversation history
# ---------------------------------------------------------------------------


@bp.route("/conversations/<conversation_id>/messages", methods=["GET"])
def get_messages(conversation_id: str):
    messages = (
        Message.query.filter_by(conversation_id=conversation_id)
        .order_by(Message.created_at)
        .all()
    )
    return jsonify(
        [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ]
    )


@bp.route("/conversations", methods=["GET"])
def list_conversations():
    convs = Conversation.query.order_by(Conversation.created_at.desc()).limit(50).all()
    result = []
    for c in convs:
        first = (
            Message.query.filter_by(conversation_id=c.id, role="user")
            .order_by(Message.created_at)
            .first()
        )
        result.append(
            {
                "id": c.id,
                "created_at": c.created_at.isoformat(),
                "preview": (first.content[:80] if first else ""),
            }
        )
    return jsonify(result)
