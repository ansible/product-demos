#!/usr/bin/env python3
"""Live presenter dashboard for config-drift Kafka audit events."""

import json
import os
import subprocess
import threading
import time
from collections import deque
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

TOPIC = os.environ.get("CONFIG_DRIFT_KAFKA_TOPIC", "linux-audit-events")
BOOTSTRAP = os.environ.get("CONFIG_DRIFT_KAFKA_BOOTSTRAP", "127.0.0.1:9094")
KAFKA_IMAGE = os.environ.get("CONFIG_DRIFT_KAFKA_IMAGE", "docker.io/apache/kafka:3.9.0")
CONTAINER = os.environ.get("CONFIG_DRIFT_KAFKA_CONTAINER", "kafka")
PORT = int(os.environ.get("CONFIG_DRIFT_DASHBOARD_PORT", "80"))
MAX_EVENTS = int(os.environ.get("CONFIG_DRIFT_DASHBOARD_MAX_EVENTS", "50"))
THROTTLE_SECONDS = int(os.environ.get("CONFIG_DRIFT_DASHBOARD_THROTTLE", "20"))

events = deque(maxlen=MAX_EVENTS)
events_lock = threading.Lock()
last_shown: dict[str, float] = {}


def parse_comm(message: str) -> str:
    marker = "comm=\""
    if marker not in message:
        return "a process"
    start = message.index(marker) + len(marker)
    end = message.index("\"", start)
    return message[start:end]


def event_kind(comm: str) -> str:
    if comm in ("platform-python", "python3") or comm.startswith("python"):
        return "remediation"
    return "drift"


def should_show(host_ip: str, kind: str) -> bool:
    key = f"{host_ip}:{kind}"
    now = time.monotonic()
    last = last_shown.get(key)
    if last is not None and now - last < THROTTLE_SECONDS:
        return False
    last_shown[key] = now
    return True


def friendly_event(body: dict) -> Optional[dict]:
    message = body.get("message", "")
    if "sshd_config_change" not in message or "type=SYSCALL" not in message:
        return None
    # One atomic save (vi temp file -> sshd_config) is usually a single rename syscall.
    if "SYSCALL=rename" not in message:
        return None

    host = body.get("host", {})
    host_ip = host.get("ip", ["unknown host"])[0]
    hostname = host.get("hostname", "")
    comm = parse_comm(message)
    kind = event_kind(comm)
    if not should_show(host_ip, kind):
        return None

    timestamp = body.get("@timestamp") or datetime.now(timezone.utc).isoformat()

    if kind == "remediation":
        return {
            "time": timestamp,
            "kind": "remediation",
            "headline": f"AAP remediation restored sshd_config on {host_ip}",
            "detail": "Automation fixed the drift — check job LINUX | SSHD Configuration Remediation",
        }

    return {
        "time": timestamp,
        "kind": "drift",
        "headline": f"/etc/ssh/sshd_config modified on {host_ip} — event published",
        "detail": f"{comm} saved sshd_config ({hostname})",
    }


def consume_kafka() -> None:
    while True:
        cmd = [
            "podman",
            "run",
            "--rm",
            "--network",
            f"container:{CONTAINER}",
            "-e",
            "KAFKA_HEAP_OPTS=-Xmx256m -Xms128m",
            KAFKA_IMAGE,
            "/opt/kafka/bin/kafka-console-consumer.sh",
            "--bootstrap-server",
            BOOTSTRAP,
            "--topic",
            TOPIC,
        ]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        if proc.stdout is None:
            continue

        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                body = json.loads(line)
            except json.JSONDecodeError:
                continue

            event = friendly_event(body)
            if event is None:
                continue

            with events_lock:
                events.appendleft(event)


def clear_dashboard() -> None:
    with events_lock:
        events.clear()
        last_shown.clear()


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Config Drift Events</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; background: #f4f6f8; color: #1a1a1a; }
    .header { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
    h1 { margin-bottom: 0.25rem; }
    .lead { color: #444; max-width: 48rem; margin-bottom: 1.5rem; }
    .reset-btn {
      padding: 0.5rem 1rem; font-size: 0.95rem; font-weight: 600;
      border: 1px solid #bbb; border-radius: 6px; background: #fff; cursor: pointer;
    }
    .reset-btn:hover { background: #f0f0f0; }
    .waiting { padding: 1rem 1.25rem; background: #fff; border: 1px dashed #bbb; border-radius: 8px; }
    .event { margin: 0.75rem 0; padding: 1rem 1.25rem; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,.08); }
    .event.drift { background: #e8f5e9; border-left: 6px solid #2e7d32; }
    .event.remediation { background: #e3f2fd; border-left: 6px solid #1565c0; }
    .event strong { display: block; font-size: 1.15rem; margin-bottom: 0.35rem; }
    .event span { color: #555; font-size: 0.95rem; }
    .footer { margin-top: 2rem; font-size: 0.9rem; color: #666; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Config Drift Event Stream</h1>
    <button type="button" class="reset-btn" id="reset">Reset</button>
  </div>
  <p class="lead">
    Edit <code>/etc/ssh/sshd_config</code> on a RHEL worker. One save shows one green line here
  (audit emits many syscalls; we collapse them). A blue line appears when AAP remediation runs.
  </p>
  <div id="events" class="waiting">Waiting for sshd_config changes…</div>
  <p class="footer">Topic: linux-audit-events · sshd_config_change · 20s throttle per host</p>
  <script>
    async function refresh() {
      const res = await fetch('/api/events');
      const data = await res.json();
      const root = document.getElementById('events');
      if (!data.length) {
        root.className = 'waiting';
        root.textContent = 'Waiting for sshd_config changes…';
        return;
      }
      root.className = '';
      root.innerHTML = data.map(e =>
        `<div class="event ${e.kind}"><strong>${e.headline}</strong><span>${e.detail} · ${e.time}</span></div>`
      ).join('');
    }
    async function resetDashboard() {
      await fetch('/api/reset', { method: 'POST' });
      refresh();
    }
    document.getElementById('reset').addEventListener('click', resetDashboard);
    setInterval(refresh, 500);
    refresh();
  </script>
</body>
</html>
"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/api/events":
            with events_lock:
                payload = json.dumps(list(events))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(payload.encode())
            return

        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path == "/api/reset":
            clear_dashboard()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, _format: str, *_args) -> None:
        return


def main() -> None:
    consumer = threading.Thread(target=consume_kafka, daemon=True)
    consumer.start()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), DashboardHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
