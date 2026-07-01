#!/usr/bin/env python3
"""
node/dependencies.py — FastAPI dependency injection

Provides singleton instances for Config, Ledger, and PBFTEngine
with proper lifecycle management.
"""

import os
import time
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI

from node.config import settings as app_settings
from consensus.ledger import Ledger
from consensus.bft import PBFTEngine


# ── Singleton holders ──────────────────────────────────────────────────
_ledger = None
_engine = None
_start_time = None


def get_config():
    """Get application configuration."""
    return app_settings


def get_ledger() -> Ledger:
    """Get or create the Ledger singleton."""
    global _ledger
    if _ledger is None:
        ledger_path = app_settings.LEDGER_PATH
        _ledger = Ledger(ledger_path)
    return _ledger


def get_engine() -> PBFTEngine:
    """Get or create the PBFTEngine singleton."""
    global _engine
    if _engine is None:
        _engine = PBFTEngine(
            node_id=app_settings.NODE_ID,
            committee_size=app_settings.COMMITTEE_SIZE,
            ledger=get_ledger(),
        )
    return _engine


def get_start_time() -> float:
    """Get server start timestamp."""
    global _start_time
    if _start_time is None:
        _start_time = time.time()
    return _start_time


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    Handles startup and shutdown of shared resources.
    """
    # Startup
    global _start_time
    _start_time = time.time()

    # Initialize ledger
    ledger = get_ledger()
    print(f"[s7g-node-{app_settings.NODE_ID}] Ledger initialized: {ledger.count()} entries")

    # Initialize PBFT engine
    engine = get_engine()
    print(f"[s7g-node-{app_settings.NODE_ID}] PBFT engine ready: f={engine.f}, quorum={engine.quorum_size}")
    print(f"[s7g-node-{app_settings.NODE_ID}] Role: {'LEADER' if engine.is_leader else 'follower'}")

    # Initialize and start P2P server and GossipSub layer
    from node.p2p_bridge import init_p2p
    await init_p2p()
    print(f"[s7g-node-{app_settings.NODE_ID}] P2P host and GossipSub layer initialized")

    yield

    # Shutdown
    from node.p2p_bridge import shutdown_p2p
    await shutdown_p2p()
    print(f"[s7g-node-{app_settings.NODE_ID}] P2P server stopped")

    if _ledger:
        _ledger.close()
        print(f"[s7g-node-{app_settings.NODE_ID}] Ledger closed")
