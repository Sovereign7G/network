"""Agent marketplace routes — register, discover, execute agents."""
from fastapi import APIRouter, HTTPException
from typing import Optional
import uuid, time, json

from agent_cards import AgentCard, AgentCapability, AgentExecutionRequest
from agent_registry import AgentRegistry
from billing import BillingDB

router = APIRouter(prefix="/agents", tags=["agents"])
registry = AgentRegistry("agent_registry.db")
billing = BillingDB("billing.db")

@router.post("/register")
async def register_agent(card: AgentCard):
    card.id = card.id or str(uuid.uuid4())
    card.created_at = int(time.time())
    aid = registry.register(card)
    return {"agent_id": aid, "status": "registered"}

@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    agent = registry.get(agent_id)
    if not agent: raise HTTPException(404, "Agent not found")
    return agent

@router.get("/")
async def list_agents(tag: Optional[str] = None, limit: int = 50):
    return {"agents": registry.list_active(tag, limit)}

@router.post("/{agent_id}/execute")
async def execute_agent(agent_id: str, request: AgentExecutionRequest):
    cid = billing.get_customer_by_key(request.api_key)
    if not cid: raise HTTPException(401, "Invalid API key")
    bal = billing.check_balance(cid)
    agent = registry.get(agent_id)
    if not agent or not agent["is_active"]: raise HTTPException(404, "Agent not found")
    if bal < agent["price_per_call"]: raise HTTPException(402, "Insufficient credits")

    eid = str(uuid.uuid4())
    cost = agent["price_per_call"]
    tokens = 0

    try:
        import httpx
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(agent["endpoint"], json=request.input)
            resp.raise_for_status()
            output = resp.json()
    except Exception as e:
        billing.deduct_usage(cid, f"agent-{eid}", 0, 0)
        raise HTTPException(502, f"Agent execution failed: {str(e)[:200]}")

    billing.deduct_usage(cid, f"agent-{eid}", tokens, cost)
    return {
        "execution_id": eid, "agent_id": agent_id, "output": output,
        "tokens_used": tokens, "cost": cost, "status": "completed"
    }

@router.delete("/{agent_id}")
async def deactivate_agent(agent_id: str, owner: str, api_key: str):
    cid = billing.get_customer_by_key(api_key)
    if not cid: raise HTTPException(401, "Invalid API key")
    if not registry.deactivate(agent_id, owner): raise HTTPException(404, "Agent not found or not owned")
    return {"status": "deactivated"}
