"""inventory-service - demo application for CI/CD pipeline demo."""
import http.server
import json
import os
import pathlib

APP_NAME = os.getenv("APP_NAME", "inventory-service")
APP_VERSION = pathlib.Path(__file__).parent.joinpath("version.txt").read_text().strip()
APP_ENV = os.getenv("APP_ENV", "dev")
APP_PORT = int(os.getenv("APP_PORT", "8080"))


class AppHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code, body, content_type="application/json"):
        encoded = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(encoded))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/health":
            self._send(
                200,
                json.dumps(
                    {
                        "status": "ok",
                        "app": APP_NAME,
                        "version": APP_VERSION,
                        "env": APP_ENV,
                    }
                ),
            )
        elif self.path == "/version.txt":
            body = f"app={APP_NAME}\nversion={APP_VERSION}\nenv={APP_ENV}\n"
            self._send(200, body, "text/plain")
        elif self.path == "/":
            body = (
                f"<html><body>"
                f"<h1>{APP_NAME}</h1>"
                f"<p>Version: {APP_VERSION}</p>"
                f"<p>Environment: {APP_ENV.upper()}</p>"
                f"</body></html>"
            )
            self._send(200, body, "text/html")
        else:
            self._send(404, json.dumps({"error": "not found"}))


if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", APP_PORT), AppHandler)
    print(f"Starting {APP_NAME} {APP_VERSION} on port {APP_PORT} [{APP_ENV}]", flush=True)
    server.serve_forever()
