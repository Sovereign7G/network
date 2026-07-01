#!/usr/bin/env python3
"""
node/api.py — FastAPI application for S7G committee node

Provides REST API for:
- Health checking
- Proposal submission (PBFT Propose → PrePrepare)
- Response commitment (PBFT Commit → Finalize)
- Ledger queries
- Signature verification

Powered by Uvicorn.
"""

import time
from fastapi import FastAPI, HTTPException, Depends

from node.models import (
    ProposalRequest, ProposalResponse, CommitRequest,
    HealthResponse, StatusResponse, LedgerResponse,
    VerifyRequest, VerifyResponse,
)
from node.dependencies import (
    lifespan, get_config, get_engine, get_ledger, get_start_time,
)
from consensus.bft import PBFTEngine
from consensus.ledger import Ledger
from node.p2p_bridge import router as p2p_router, get_gossip


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=f"S7G Committee Node",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Include P2P endpoints
    app.include_router(p2p_router)

    # ── Health ────────────────────────────────────────────────────────

    @app.get("/health", response_model=HealthResponse)
    async def health(
        config=Depends(get_config),
        ledger=Depends(get_ledger),
        start_time=Depends(get_start_time),
    ):
        return HealthResponse(
            status="healthy",
            node_id=config.NODE_ID,
            role=config.NODE_ROLE,
            committee_size=config.COMMITTEE_SIZE,
            ledger_entries=ledger.count(),
            uptime_seconds=time.time() - start_time,
        )

    # ── Status ────────────────────────────────────────────────────────

    @app.get("/status", response_model=StatusResponse)
    async def status(
        engine: PBFTEngine = Depends(get_engine),
    ):
        return StatusResponse(
            node_id=engine.node_id,
            node_role="leader" if engine.is_leader else "follower",
            sequence=engine.sequence,
            pending_proposals=len(engine.pending_proposals),
            total_committed=engine.ledger.count() if engine.ledger else 0,
            committee_size=engine.committee_size,
            byzantine_tolerance=engine.f,
            is_leader=engine.is_leader,
        )

    # ── Propose ───────────────────────────────────────────────────────

    @app.post("/propose", response_model=ProposalResponse)
    async def propose(
        request: ProposalRequest,
        engine: PBFTEngine = Depends(get_engine),
    ):
        if not engine.is_leader:
            raise HTTPException(
                status_code=403,
                detail=f"Node {engine.node_id} is not the leader. "
                       f"Leader is node {(engine.sequence % engine.committee_size) + 1}"
            )

        try:
            # PBFT propose → returns block
            block = engine.propose(request.payload)

            # PRE-PREPARE (self-acknowledge)
            engine.pre_prepare(block)

            # Broadcast PRE-PREPARE via GossipSub
            gossip = get_gossip()
            if gossip:
                await gossip.publish("consensus", {
                    "type": "PRE-PREPARE",
                    "block": block
                })

            # PREPARE (self-sign)
            sig = engine._sign(block)
            quorum_reached = engine.prepare(block, engine.node_id, sig)

            # Broadcast PREPARE via GossipSub
            if gossip:
                await gossip.publish("consensus", {
                    "type": "PREPARE",
                    "block": block,
                    "from_node": engine.node_id,
                    "signature": sig
                })

            return ProposalResponse(
                proposal_id=block["request_id"],
                status="committed" if quorum_reached else "pending",
                committee_signatures=list(engine.prepare_collection.get(
                    block["request_id"], {}
                ).values()),
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # ── Commit ────────────────────────────────────────────────────────

    @app.post("/commit", response_model=dict)
    async def commit(
        request: CommitRequest,
        engine: PBFTEngine = Depends(get_engine),
        ledger: Ledger = Depends(get_ledger),
    ):
        # Check if proposal exists
        block = engine.pending_proposals.get(request.request_id)
        if not block:
            # Check if already committed
            for b in engine.get_ledger():
                if b.get("request_id") == request.request_id:
                    return {"status": "already_committed", "request_id": request.request_id}
            raise HTTPException(status_code=404, detail="Proposal not found")

        # Append response to block payload
        block["response"] = request.response_summary
        block["committed_at"] = int(time.time())

        # COMMIT (self-acknowledge)
        sig = engine._sign(block)
        finalized = engine.commit(block, engine.node_id, sig)

        # Broadcast COMMIT via GossipSub
        gossip = get_gossip()
        if gossip:
            await gossip.publish("consensus", {
                "type": "COMMIT",
                "block": block,
                "from_node": engine.node_id,
                "signature": sig
            })

        return {
            "status": "committed" if finalized else "pending",
            "sequence": engine.sequence,
            "request_id": request.request_id,
        }

    # ── Ledger ────────────────────────────────────────────────────────

    @app.get("/ledger", response_model=LedgerResponse)
    async def get_ledger(
        limit: int = 100,
        offset: int = 0,
        engine: PBFTEngine = Depends(get_engine),
    ):
        entries = engine.get_ledger()
        total = len(entries)
        return LedgerResponse(
            total=total,
            limit=limit,
            offset=offset,
            data=entries[-limit:] if total > 0 else [],
        )

    @app.get("/ledger/{request_id}")
    async def get_block(
        request_id: str,
        engine: PBFTEngine = Depends(get_engine),
    ):
        for block in engine.get_ledger():
            if block.get("request_id") == request_id:
                return block
        raise HTTPException(status_code=404, detail="Block not found")

    # ── Verify ────────────────────────────────────────────────────────

    @app.post("/verify", response_model=VerifyResponse)
    async def verify(
        request: VerifyRequest,
        engine: PBFTEngine = Depends(get_engine),
    ):
        # Extract the block data from ledger
        block_data = None
        for b in engine.get_ledger():
            if b.get("request_id") == request.request_id:
                block_data = b
                break

        if not block_data:
            raise HTTPException(status_code=404, detail="Request not found in ledger")

        # Verify signature against proposer
        # In Phase A, we verify against the proposer_id stored in the block
        verified = engine.verify_signature(
            block_data,
            request.signature,
            block_data.get("proposer_id", 0),
        )

        return VerifyResponse(
            request_id=request.request_id,
            verified=verified,
        )

    return app


# ── Create app instance ──────────────────────────────────────────────
app = create_app()


if __name__ == "__main__":
    import uvicorn
    from node.config import settings
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
