#!/usr/bin/env python3
"""
consensus/bft.py — PBFT Consensus Engine

Implements a simplified Practical Byzantine Fault Tolerance consensus
for the S7G committee. Supports 4-node clusters (f=1, tolerance=1).

Lifecycle:
  1. Propose: Leader creates a block and broadcasts PRE-PREPARE
  2. PrePrepare: Nodes validate and acknowledge the proposal
  3. Prepare: Nodes broadcast PREPARE, collect 2f+1 signatures
  4. Commit: Nodes broadcast COMMIT, collect 2f+1 signatures
  5. Finalize: Block is appended to the local SQLite ledger

In Phase A, crypto is simulated with SHA256 hashes.
Production will use Ed25519 threshold signatures (3-of-5 multi-sig).
"""

import hashlib
import json
import time
from typing import Dict, List, Any, Optional


class PBFTEngine:
    """PBFT consensus engine for S7G committee nodes."""

    def __init__(self, node_id: int, committee_size: int, ledger):
        self.node_id = node_id
        self.committee_size = committee_size
        self.ledger = ledger

        # Byzantine tolerance: f = floor((n-1)/3)
        # For 4 nodes: f=1 (tolerates 1 faulty node)
        # For 7 nodes: f=2 (tolerates 2 faulty nodes)
        self.f = (committee_size - 1) // 3

        # Minimum signatures needed for prepare/commit phases
        self.quorum_size = 2 * self.f + 1

        # Sequence tracking
        self._sequence = ledger.count() if ledger else 0
        self._view = 0

        # Pending proposals (not yet committed)
        self.pending_proposals: Dict[str, dict] = {}

        # Prepare phase: {request_id: {from_node: signature}}
        self.prepare_collection: Dict[str, Dict[int, str]] = {}

        # Commit phase: {request_id: {from_node: signature}}
        self.commit_collection: Dict[str, Dict[int, str]] = {}

        # Validators: {node_id: public_key_hex}
        # In Phase A, public keys are simulated as SHA256 hashes
        self.validators: Dict[int, str] = {}
        self._init_validators()

    def _init_validators(self):
        """Initialize validator set with simulated keys."""
        for i in range(1, self.committee_size + 1):
            seed = f"s7g-validator-{i}-2026"
            self.validators[i] = hashlib.sha256(seed.encode()).hexdigest()

    @property
    def sequence(self) -> int:
        """Current sequence number."""
        return self._sequence

    @property
    def is_leader(self) -> bool:
        """Check if this node is the current leader (round-robin)."""
        return self.node_id == (self._view % self.committee_size) + 1

    def propose(self, payload: dict) -> dict:
        """
        Create a new proposal as the leader.

        Returns a Block dict ready for PRE-PREPARE broadcast.
        """
        self._sequence += 1

        block = {
            "sequence": self._sequence,
            "request_id": hashlib.sha256(
                json.dumps(payload, sort_keys=True).encode() +
                str(time.time_ns()).encode()
            ).hexdigest()[:16],
            "payload": payload,
            "proposer_id": self.node_id,
            "view": self._view,
            "timestamp": int(time.time()),
            "signature": self._sign(payload),
        }

        # Store as pending
        self.pending_proposals[block["request_id"]] = block
        self.prepare_collection[block["request_id"]] = {}
        self.commit_collection[block["request_id"]] = {}

        return block

    def pre_prepare(self, block: dict) -> bool:
        """
        Handle PRE-PREPARE message from leader.

        Validates the proposal and stores it for the prepare phase.
        Returns True if accepted.
        """
        # Validate leader
        expected_leader = (self._view % self.committee_size) + 1
        if block.get("proposer_id") != expected_leader:
            return False

        # Validate sequence
        if block.get("sequence", 0) <= self._sequence:
            return False

        # Validate signature
        payload = block.get("payload", {})
        signature = block.get("signature", "")
        if not self._verify(payload, signature, block.get("proposer_id", 0)):
            return False

        # Accept proposal
        rid = block["request_id"]
        self._sequence = block["sequence"]
        self.pending_proposals[rid] = block
        self.prepare_collection[rid] = {}
        self.commit_collection[rid] = {}

        return True

    def prepare(self, block: dict, from_node: int, signature: str) -> bool:
        """
        Handle PREPARE message from a peer.

        Collects prepare signatures until quorum is reached.
        Returns True when 2f+1 prepares collected (ready for commit).
        """
        rid = block.get("request_id", "")

        # Validate request exists
        if rid not in self.pending_proposals:
            return False

        # Validate signature
        if not self._verify(block, signature, from_node):
            return False

        # Collect prepare
        self.prepare_collection[rid][from_node] = signature

        # Check if we have quorum (2f+1)
        if len(self.prepare_collection[rid]) >= self.quorum_size:
            return True

        return False

    def commit(self, block: dict, from_node: int, signature: str) -> bool:
        """
        Handle COMMIT message from a peer.

        Collects commit signatures until quorum is reached.
        Returns True when 2f+1 commits collected (ready to finalize).
        """
        rid = block.get("request_id", "")

        # Validate request exists
        if rid not in self.pending_proposals:
            return False

        # Validate signature
        if not self._verify(block, signature, from_node):
            return False

        # Collect commit
        self.commit_collection[rid][from_node] = signature

        # Check if we have quorum (2f+1)
        if len(self.commit_collection[rid]) >= self.quorum_size:
            # Finalize: append to ledger
            self._finalize(rid)
            return True

        return False

    def _finalize(self, request_id: str):
        """
        Finalize a committed proposal by appending to the SQLite ledger.
        """
        block = self.pending_proposals.get(request_id)
        if not block:
            return

        # Append to ledger
        self.ledger.append(
            sequence=block["sequence"],
            request_id=request_id,
            payload=block.get("payload", {}),
            response_summary={},  # Will be filled by commit endpoint
            timestamp=block.get("timestamp", int(time.time())),
            proposer_id=block.get("proposer_id", 0),
        )

        # Cleanup pending state
        self.pending_proposals.pop(request_id, None)
        self.prepare_collection.pop(request_id, None)
        self.commit_collection.pop(request_id, None)

    def get_ledger(self) -> list:
        """Get all committed ledger entries."""
        return self.ledger.get_all() if self.ledger else []

    # ── Signature Helpers (Phase A: SHA256 simulation) ─────────────

    def _sign(self, data: dict) -> str:
        """Create a simulated signature using SHA256."""
        content = json.dumps(data, sort_keys=True) + str(self.node_id)
        return hashlib.sha256(content.encode()).hexdigest()

    def _verify(self, data: dict, signature: str, node_id: int) -> bool:
        """Verify a simulated signature."""
        expected = hashlib.sha256(
            (json.dumps(data, sort_keys=True) + str(node_id)).encode()
        ).hexdigest()
        return signature == expected

    def verify_signature(self, data: dict, signature: str, node_id: int) -> bool:
        """Public method to verify any signature."""
        return self._verify(data, signature, node_id)
