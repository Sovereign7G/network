import pytest
import os
import httpx
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from gateway.proxy import app, s7g, billing

client = TestClient(app)

@pytest.mark.asyncio
async def test_proxy_flow(monkeypatch):
    # 1. Use a test db path
    test_db_path = "test_billing_proxy.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Point the proxy's billing instance to our test DB
    billing.db_path = test_db_path
    billing._init_db()

    # Mock S7GClient propose call
    mock_propose = AsyncMock()
    mock_propose.return_value = {
        "proposal_id": "mock-req-id",
        "status": "committed",
        "committee_signatures": ["sig1", "sig2"]
    }
    monkeypatch.setattr(s7g, "propose", mock_propose)

    # Mock token counter functions
    monkeypatch.setattr("gateway.proxy.estimate_tokens", lambda messages: 100)
    monkeypatch.setattr("gateway.proxy.calculate_cost", lambda tokens, price: 0.10)

    # Create a customer and get API key
    cust_id, api_key = billing.create_customer("Bob", "bob@example.com")
    
    # 2. Try completions without credits
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "Hello"}]}, headers=headers)
    assert resp.status_code == 402  # Insufficient credits

    # 3. Add credits
    billing.add_credits(cust_id, 10.0)
    assert billing.check_balance(cust_id) == 10.0

    # 4. Try completions with credits (should succeed)
    resp = client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "Hello"}]}, headers=headers)
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["provenance"]["status"] == "committed"
    assert res_data["usage"]["cost"] == 0.10

    # Clean up test DB
    billing.close()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
