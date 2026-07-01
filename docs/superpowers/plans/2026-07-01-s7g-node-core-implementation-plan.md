# S7G Node Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the core S7G validator node API using FastAPI, PBFT consensus engine, and SQLite persistence.

**Architecture:** A lightweight FastAPI server exposes `/health`, `/status`, `/propose`, and `/commit` endpoints. It uses dependency injection to interact with a SQLite-backed ledger and a PBFT consensus engine.

**Tech Stack:** Python 3.11, FastAPI, Uvicorn, SQLite3, Pydantic, Loguru.

## Global Constraints
- Target directory: `decentralized-ai-inference/s7g-committee`
- No remote calls in unit tests (use mocked networking/disk).
- Clean separation between HTTP API, ledger persistence, and PBFT logic.

---

### Task 1: Initialize Project Structure & Configuration
Initialize the project folder and define the basic environment configurations.

**Files:**
- Create: `decentralized-ai-inference/s7g-committee/requirements.txt`
- Create: `decentralized-ai-inference/s7g-committee/node/config.py`
- Test: `decentralized-ai-inference/s7g-committee/tests/test_config.py`

**Interfaces:**
- Produces: `settings` config singleton.

- [ ] **Step 1: Write requirements.txt**
  Create `decentralized-ai-inference/s7g-committee/requirements.txt` with:
  ```text
  fastapi>=0.100.0
  uvicorn>=0.22.0
  pydantic-settings>=2.0.0
  loguru>=0.7.0
  pytest>=7.0.0
  ```

- [ ] **Step 2: Write config.py**
  Create `decentralized-ai-inference/s7g-committee/node/config.py`:
  ```python
  import os
  from pathlib import Path
  from typing import List, Optional
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      NODE_ID: int = 1
      NODE_ROLE: str = "follower"
      COMMITTEE_SIZE: int = 4
      PEERS: List[str] = []
      GENESIS_FILE: Path = Path("/app/genesis.json")
      LEDGER_PATH: Path = Path("/app/ledger")
      API_HOST: str = "0.0.0.0"
      API_PORT: int = 1317

      class Config:
          env_file = ".env"
          case_sensitive = True

  settings = Settings()
  ```

- [ ] **Step 3: Write configuration test**
  Create `decentralized-ai-inference/s7g-committee/tests/test_config.py`:
  ```python
  from node.config import settings

  def test_default_settings():
      assert settings.NODE_ID == 1
      assert settings.NODE_ROLE == "follower"
      assert settings.COMMITTEE_SIZE == 4
  ```

- [ ] **Step 4: Run test to verify it passes**
  Run: `pytest decentralized-ai-inference/s7g-committee/tests/test_config.py -v`
  Expected: PASS

- [ ] **Step 5: Commit**
  Run:
  ```bash
  git add decentralized-ai-inference/s7g-committee/
  git commit -m "feat: init s7g-committee folder and settings configuration"
  ```

---

### Task 2: Implement SQLite Ledger Persistence
Create the SQLite-backed ledger module to log proposals and commits.

**Files:**
- Create: `decentralized-ai-inference/s7g-committee/consensus/ledger.py`
- Test: `decentralized-ai-inference/s7g-committee/tests/test_ledger.py`

**Interfaces:**
- Produces: `Ledger` class with `append`, `get_all`, and `count` methods.

- [ ] **Step 1: Write Ledger implementation**
  Create `decentralized-ai-inference/s7g-committee/consensus/ledger.py`:
  ```python
  import json
  import sqlite3
  from pathlib import Path
  from typing import List, Dict, Any, Optional

  class Ledger:
      def __init__(self, ledger_path: Path):
          self.ledger_path = ledger_path / "ledger.db"
          self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
          self._init_db()

      def _init_db(self):
          self.conn = sqlite3.connect(str(self.ledger_path))
          self.cursor = self.conn.cursor()
          self.cursor.execute("""
              CREATE TABLE IF NOT EXISTS blocks (
                  sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                  request_id TEXT UNIQUE NOT NULL,
                  payload TEXT NOT NULL,
                  response_summary TEXT,
                  timestamp INTEGER NOT NULL,
                  proposer_id INTEGER NOT NULL
              )
          """)
          self.conn.commit()

      def append(self, sequence: int, request_id: str, payload: dict, response_summary: dict, timestamp: int, proposer_id: int):
          self.cursor.execute("""
              INSERT INTO blocks (sequence, request_id, payload, response_summary, timestamp, proposer_id)
              VALUES (?, ?, ?, ?, ?, ?)
          """, (sequence, request_id, json.dumps(payload), json.dumps(response_summary), timestamp, proposer_id))
          self.conn.commit()

      def get_all(self) -> List[Dict[str, Any]]:
          self.cursor.execute("SELECT * FROM blocks ORDER BY sequence ASC")
          rows = self.cursor.fetchall()
          return [{
              "sequence": r[0],
              "request_id": r[1],
              "payload": json.loads(r[2]),
              "response_summary": json.loads(r[3]),
              "timestamp": r[4],
              "proposer_id": r[5]
          } for r in rows]

      def count(self) -> int:
          self.cursor.execute("SELECT COUNT(*) FROM blocks")
          return self.cursor.fetchone()[0]

      def close(self):
          self.conn.close()
  ```

- [ ] **Step 2: Write Ledger unit test**
  Create `decentralized-ai-inference/s7g-committee/tests/test_ledger.py`:
  ```python
  import tempfile
  from pathlib import Path
  from consensus.ledger import Ledger

  def test_ledger_append_and_retrieve():
      with tempfile.TemporaryDirectory() as tmpdir:
          ledger = Ledger(Path(tmpdir))
          assert ledger.count() == 0
          ledger.append(1, "req-1", {"model": "llama"}, {"tokens": 10}, 1600000000, 1)
          assert ledger.count() == 1
          blocks = ledger.get_all()
          assert blocks[0]["request_id"] == "req-1"
          assert blocks[0]["payload"]["model"] == "llama"
          ledger.close()
  ```

- [ ] **Step 3: Run test to verify it passes**
  Run: `pytest decentralized-ai-inference/s7g-committee/tests/test_ledger.py -v`
  Expected: PASS

- [ ] **Step 4: Commit**
  Run:
  ```bash
  git add decentralized-ai-inference/s7g-committee/
  git commit -m "feat: add SQLite persistence layer for S7G ledger"
  ```
