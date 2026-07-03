import pytest
import httpx
from gateway.s7g_client import S7GClient

@pytest.mark.asyncio
async def test_s7g_propose(monkeypatch):
    client = S7GClient("http://localhost:8000")
    
    async def mock_post(*args, **kwargs):
        req = httpx.Request("POST", "http://localhost:8000/propose")
        return httpx.Response(200, json={
            "proposal_id": "test-req",
            "status": "accepted",
            "committee_signatures": ["sig1"]
        }, request=req)
        
    monkeypatch.setattr(client.client, "post", mock_post)
    
    resp = await client.propose("test-req", {"test": "data"})
    assert resp["proposal_id"] == "test-req"
    assert resp["status"] == "accepted"
    await client.close()
