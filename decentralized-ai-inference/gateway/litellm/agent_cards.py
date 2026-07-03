"""Agent card schemas (A2A 0.3.0 compatible)."""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class AgentCapability(BaseModel):
    name: str
    description: str
    parameters: Optional[Dict[str, Any]] = None

class AgentCard(BaseModel):
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    did: Optional[str] = None  # did:icp:<principal>
    endpoint: str  # URL to call this agent
    capabilities: List[AgentCapability] = []
    price_per_call: float = 0.0
    price_per_token: float = 0.0
    owner: str  # customer_id who registered this agent
    created_at: int = 0
    is_active: bool = True
    tags: List[str] = []

class AgentExecutionRequest(BaseModel):
    agent_id: str
    input: Dict[str, Any]
    api_key: str

class AgentExecutionResult(BaseModel):
    execution_id: str
    agent_id: str
    output: Dict[str, Any]
    tokens_used: int
    cost: float
    status: str  # completed, failed, pending
    committee_proof: Optional[Dict[str, Any]] = None
