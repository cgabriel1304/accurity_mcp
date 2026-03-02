import os
import warnings

# pydantic.v1 compat layer doesn't support Python 3.14+; langchain handles
# this gracefully — suppress the noisy UserWarning it emits at import time.
warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14",
    category=UserWarning,
)

from dotenv import load_dotenv, find_dotenv

# Load .env before reading any config (searches up from cwd to project root)
load_dotenv(find_dotenv(usecwd=False))

from app import create_app  # noqa: E402 — must come after load_dotenv

app = create_app()

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug, threaded=True)
