#!/usr/bin/env python3
"""
node/models.py — Pydantic models for S7G committee API
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ProposalRequest(BaseModel):
    request_id: str
    payload: Dict[str, Any]
    timestamp: Optional[int] = None


class CommitRequest(BaseModel):
    request_id: str
    response_summary: Dict[str, Any]


class ProposalResponse(BaseModel):
    proposal_id: str
    status: str
    committee_signatures: List[str] = []


class Block(BaseModel):
    sequence: int
    request_id: str
    payload: Dict[str, Any]
    proposer_id: int
    timestamp: int
    signature: str


class HealthResponse(BaseModel):
    status: str
    node_id: int
    role: str
    committee_size: int
    ledger_entries: int
    uptime_seconds: Optional[float] = None


class StatusResponse(BaseModel):
    node_id: int
    node_role: str
    sequence: int
    pending_proposals: int
    total_committed: int
    committee_size: int
    byzantine_tolerance: int
    is_leader: bool


class LedgerResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[Dict[str, Any]]


class VerifyRequest(BaseModel):
    request_id: str
    signature: str


class VerifyResponse(BaseModel):
    request_id: str
    verified: bool
