"""Lightweight internal HTTP server.

Currently provides a `/health` endpoint and can be extended.
"""

__all__ = ["start", "check", "app"]

import atexit
import http.client
import json
import logging
import os
import threading

import uvicorn
from fastapi import FastAPI

from app import models

logger = logging.getLogger(__name__)
app = FastAPI()

_thread: threading.Thread | None = None
_server: uvicorn.Server | None = None


@app.get("/health")
def health_route() -> dict[str, object]:
    return {"status": "ok", "pid": os.getpid()}


def start(settings: models.Settings) -> None:
    """Start the background server."""
    global _thread
    if _thread and _thread.is_alive():
        return

    def _run() -> None:
        global _server

        config = uvicorn.Config(
            app, host="0.0.0.0", port=settings.server_port, log_config=None
        )
        _server = uvicorn.Server(config)

        try:
            _server.run()
        except Exception as ex:
            logger.warning(f"internal server error: {ex}")

    atexit.register(_shutdown)
    _thread = threading.Thread(target=_run, name="internal-server", daemon=True)
    _thread.start()


def check(settings: models.Settings) -> str | None:
    """Check if the server is responding.

    Returns the PID as a string if healthy, otherwise ``None``.
    """
    try:
        conn = http.client.HTTPConnection("localhost", settings.server_port, timeout=2)
        conn.request("GET", "/health")
        resp = conn.getresponse()

        if resp.status == 200:
            payload: dict[str, str] = json.loads(resp.read().decode())
            return str(payload.get("pid")) or None

        return None
    except Exception:
        return None


def _shutdown() -> None:
    global _server
    if _server and _thread:
        _server.should_exit = True
        _thread.join()
