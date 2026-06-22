---
created: '2026-06-22T13:35:56Z'
tags:
- antigravity
- artifact
- plan
title: 'Antigravity Artifact: Implementation Plan'
type: Note
updated: '2026-06-22T13:45:21.262598Z'
---

# Integrating Hermes OKF Bundle with Google Antigravity

This plan outlines the steps to fuse the Hermes OKF (Open Knowledge Format) persistent memory bundle with the Google Antigravity agentic IDE. This creates a shared memory layer enabling automated knowledge updates, artifact synchronization, subagent spawning, and peer-to-peer real-time collaboration.

## User Review Required

> [!IMPORTANT]
> - **Path Changes**: The workspace mount point has shifted from `/media/fiji/` to `/media/cherry/`. We will automatically update `.vscode/settings.json` and `orchestrate_sync.ts` to reflect this change.
> - **MCP Registration**: The `magix_okf.py` server will run on port 9000. We will register it under `mcp.servers` in `.vscode/settings.json` as a stdio-based tool to allow direct local integration.

## Open Questions

> [!NOTE]
> - **Sync Interval**: We propose a 5-second polling interval for the artifact sync daemon to check for file edits/feedback. Please confirm if a file-system watcher (like `watchdog` or `inotify`) is preferred, although simple polling is highly robust across standard Linux filesystems.

---

## Proposed Changes

### Configuration Repairs

#### [MODIFY] [settings.json](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/.vscode/settings.json)
- Update all occurrences of `/media/fiji/` to `/media/cherry/`.
- Correct the `sovereign-multiplexer` path to point to `siphon_mcp_multiplexer.py`.
- Add `magix-okf` to `mcp.servers` list for seamless stdio integration.

#### [MODIFY] [orchestrate_sync.ts](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/orchestrate_sync.ts)
- Update `REPORT_DIR` to use the correct `/media/cherry/` path.

---

### Layer 1: MCP-Oriented IDE

#### [MODIFY] [magix_okf.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/magix_okf.py)
- Implement a FastAPI/uvicorn server inside `magix_okf.py` that listens on port 9000 when started with `run-server`.
- Handle standard JSON-RPC over HTTP/SSE as well as direct REST endpoints for MCP compatibility.
- Implement standard input/output (stdio) JSON-RPC loop in addition to the HTTP server, allowing it to act as a native stdio MCP server for the IDE.

---

### Layers 2 & 4: Artifact Sync and Feedback Loop

#### [NEW] [artifact_okf_sync.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/artifact_okf_sync.py)
- Create a python daemon script that periodically polls `/home/cherry/.gemini/antigravity-ide/brain/acc63587-c2ee-4819-af6a-fd0f04eaecf4` for artifacts (`implementation_plan.md`, `task.md`, `walkthrough.md`).
- Parse the markdown, extract/generate valid YAML frontmatter, and save them as OKF concepts in `00_KNOWLEDGE/artifacts/`.
- Handle human feedback updates written to these artifacts by propagating them back to OKF.
- Call `okf_git_sync.sh` to keep changes tracked under git.

---

### Layer 3: Agent Spawning

#### [MODIFY] [magix_okf.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/magix_okf.py)
- Add a new MCP tool `spawn_hermes_subagent` to spawn specialized Hermes agents in the background.

---

### Layer 5: Peer Connection

#### [NEW] [okf_peer_bridge.py](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/06_INFRA/okf_peer_bridge.py)
- Implement a WebSocket-based server (listening on port 9005) to sync OKF concept changes in real time between Antigravity and Hermes Desktop.

#### [MODIFY] [mcp.js](file:///media/cherry/4A21-00001/New%20folder/AGE%20REPUBLIC/js/mcp.js)
- Add a visual status widget inside the dashboard UI to monitor "OKF Sync" peer connectivity status.

---

## Verification Plan

### Automated Tests
- Run `python3 magix_okf.py serve_concept '{"path": "research"}'` to verify CLI interface.
- Run `python3 okf_validator.py` to confirm SCHEMA.md parses cleanly.

### Manual Verification
- Start the `magix_okf.py` server on port 9000: `python3 magix_okf.py run-server`.
- Start the `artifact_okf_sync.py` daemon and observe artifacts being mirrored under `00_KNOWLEDGE/artifacts/`.
- Verify the OKF Sync status in the dashboard cockpit.
