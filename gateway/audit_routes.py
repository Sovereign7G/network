"""Audit API routes — compliance layer with verifiable proof."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from audit import AuditDB

router = APIRouter(prefix="/audit", tags=["audit"])
audit = AuditDB("audit.db")

@router.get("/requests")
async def get_requests(customer_id: Optional[str] = None, from_ts: Optional[int] = None,
                       to_ts: Optional[int] = None, limit: int = 100):
    try:
        rows = audit.query(customer_id, from_ts, to_ts)
        return {"count": len(rows), "requests": rows}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/report/{customer_id}")
async def get_report(customer_id: str, from_ts: int, to_ts: int):
    return audit.report(customer_id, from_ts, to_ts)

@router.get("/verify/{request_id}")
async def verify_request(request_id: str, signature: str = Query(...)):
    if audit.verify(request_id, signature):
        return {"request_id": request_id, "verified": True}
    raise HTTPException(404, "Not found or invalid signature")

@router.get("/provenance/{request_id}")
async def get_provenance(request_id: str):
    p = audit.provenance(request_id)
    if p: return p
    raise HTTPException(404, "Request not found")
