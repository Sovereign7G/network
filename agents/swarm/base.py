"""Shared base module for swarm agents — AsyncWriter, helpers, and BaseAgent."""
import json
import logging
import os
import queue
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, Optional

AETHERDB = os.getenv("AETHERDB_CANISTER", "h54dw-qyaaa-aaaaa-qhjtq-cai")


class AsyncWriter:
    """Non-blocking writer thread for ICP stores — agents don't block on _store()."""
    def __init__(self):
        self.q = queue.Queue(maxsize=500)
        self.running = True
        self.dropped = 0
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        while self.running:
            try:
                key, val = self.q.get(timeout=1)
                v = json.dumps(val).encode("utf-8")
                blob = "vec{" + ";".join(str(b) for b in v) + "}"
                r = subprocess.run(
                    ["dfx", "canister", "--network", "ic", "call", AETHERDB, "aetherdb_put",
                     f'("{key}", {blob})'],
                    capture_output=True, text=True, timeout=10,
                )
                if r.returncode != 0:
                    err = r.stderr.strip().lower()
                    if err and "deprecat" not in err and "warning" not in err:
                        logging.warning(f"[AsyncWriter] ICP write issue for {key}: {err[:60]}")
            except queue.Empty:
                continue
            except subprocess.TimeoutExpired:
                logging.warning(f"[AsyncWriter] Timeout writing {key}")
            except Exception as e:
                logging.warning(f"[AsyncWriter] Error: {e}")

    def put(self, key, val):
        try:
            self.q.put_nowait((key, val))
        except queue.Full:
            self.dropped += 1
            if self.dropped <= 5:
                logging.warning(f"[AsyncWriter] Queue full, dropped {key}")

    def stop(self):
        self.running = False
        self.thread.join(timeout=3)


_WRITER = AsyncWriter()


def _sanitize(s: str, max_len: int = 40) -> str:
    """Remove sensitive patterns from error messages before exposing via status."""
    s = re.sub(r'/media/[^\s]+', '[PATH]', s)
    s = re.sub(r'0x[0-9a-fA-F]{10,}', '[ADDR]', s)
    s = re.sub(r'[a-zA-Z0-9+/]{20,}={0,2}', '[TOKEN]', s)
    return s[:max_len]


def _store(key: str, val: dict):
    """Non-blocking write to ICP via AsyncWriter thread."""
    _WRITER.put(key, val)


class BaseAgent:
    """Base class for all swarm agents with threaded loop, error handling, and status reporting."""
    def __init__(self, name: str, interval_s: int, is_specialist: bool = False):
        self.name = name
        self.interval = interval_s
        self.log = logging.getLogger(name)
        self.running = False
        self.actions = 0
        self.error_count = 0
        self.max_errors = 10
        self._thread = None
        self.last_ok_ts = 0.0
        self.last_error_ts = 0.0
        self.last_error_msg = ""
        self.last_trace_id = ""
        self.is_specialist = is_specialist

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self.log.info(f"Started (interval: {self.interval}s)")

    def _loop(self):
        while self.running:
            from agents.trace import new_trace_id
            trace_id = new_trace_id()
            self.last_trace_id = trace_id
            try:
                result = self.execute()
                if result:
                    result["_trace_id"] = trace_id
                    self.actions += 1
                    _store(f"agent:{self.name}:{int(time.time())}", result)
                    self.last_ok_ts = time.time()
                self.error_count = 0
            except Exception as e:
                self.error_count += 1
                self.last_error_ts = time.time()
                self.last_error_msg = str(e)[:80]
                self.log.error(f"[{trace_id}] Error #{self.error_count}/{self.max_errors}: {e}")
                if self.error_count >= self.max_errors:
                    self.log.critical(f"Agent {self.name} — {self.max_errors} errors, stopping loop")
                    break
            time.sleep(self.interval)

    def execute(self) -> Optional[Dict]:
        raise NotImplementedError

    def status(self) -> Dict:
        now = time.time()
        age = now - self.last_ok_ts if self.last_ok_ts > 0 else -1
        return {
            "name": self.name,
            "actions": self.actions,
            "interval": self.interval,
            "ok_since": int(self.last_ok_ts),
            "data_age_s": int(age),
            "errors": self.error_count,
            "last_error": _sanitize(self.last_error_msg) if self.last_error_msg else "",
            "last_trace": self.last_trace_id,
        }

    def is_running(self) -> bool:
        return self.running and (self._thread is not None and self._thread.is_alive())

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=3)
