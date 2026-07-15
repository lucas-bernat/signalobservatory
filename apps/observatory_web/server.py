"""Signal Observatory web dashboard.

This first app uses a synthetic signal source so the web/API/data flow can be
learned before the RTL-SDR hardware arrives. It intentionally depends only on
the Python standard library so it can run on a fresh Raspberry Pi.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import platform
import socket
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sources import SpectrumSource, SyntheticSpectrumSource


APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"


def create_source() -> SpectrumSource:
    return SyntheticSpectrumSource()


class ObservatoryRequestHandler(BaseHTTPRequestHandler):
    source = create_source()
    server_version = "SignalObservatoryWeb/0.1"

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path == "/":
            self._send_static_file(STATIC_DIR / "index.html")
            return

        if path == "/api/status":
            self._send_json(
                {
                    "name": "Signal Observatory",
                    "hostname": socket.gethostname(),
                    "platform": platform.platform(),
                    "python_version": platform.python_version(),
                    "server_time": time.time(),
                    "source": self.source.name,
                    "source_metadata": self.source.metadata(),
                    "working_directory": os.getcwd(),
                }
            )
            return

        if path == "/api/spectrum":
            self._send_json(self.source.snapshot())
            return

        if path.startswith("/static/"):
            requested = path.removeprefix("/static/")
            self._send_static_file(STATIC_DIR / requested)
            return

        self._send_json({"error": "not found", "path": path}, HTTPStatus.NOT_FOUND)

    def log_message(self, format_string: str, *args: Any) -> None:
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} {format_string % args}")

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_static_file(self, path: Path) -> None:
        resolved = path.resolve()
        if not resolved.is_file() or STATIC_DIR.resolve() not in resolved.parents:
            self._send_json({"error": "static file not found"}, HTTPStatus.NOT_FOUND)
            return

        body = resolved.read_bytes()
        content_type, _ = mimetypes.guess_type(resolved.name)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Signal Observatory web dashboard.")
    parser.add_argument("--host", default="127.0.0.1", help="Host/interface to bind.")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ObservatoryRequestHandler)
    print(f"Signal Observatory web app listening on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Signal Observatory web app.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
