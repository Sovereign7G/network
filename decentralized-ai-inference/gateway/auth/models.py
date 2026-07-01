from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ProposalPayload(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class ProposalResponseModel(BaseModel):
    proposal_id: str
    status: str
    committee_signatures: List[str]

class CommitPayload(BaseModel):
    request_id: str
    response_summary: Dict[str, Any]
