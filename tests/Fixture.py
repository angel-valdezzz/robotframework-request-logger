"""Local real HTTP fixture with deliberately fake secrets."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from time import sleep
from typing import Any

from robot.api.deco import keyword, library


@library(scope="SUITE", auto_keywords=False)
class Fixture:
    def __init__(self) -> None:
        self.server: ThreadingHTTPServer | None = None

    @keyword
    def start_api(self) -> str:
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:
                pass

            def do_GET(self) -> None:
                if self.path.startswith("/slow"):
                    sleep(0.1)
                status = 404 if self.path.startswith("/missing") else 200
                data = {
                    "folio": "ALT-1042",
                    "rfc": "",
                    "access_token": "fake-secret-TOKEN",
                    "office": {"name": "Centro", "active": True},
                }
                payload = json.dumps(data).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                try:
                    self.wfile.write(payload)
                except (BrokenPipeError, ConnectionResetError):
                    pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        Thread(target=self.server.serve_forever, daemon=True).start()
        return f"http://127.0.0.1:{self.server.server_port}"

    @keyword
    def stop_api(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
