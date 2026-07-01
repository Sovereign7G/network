import sys
import pytest
from unittest.mock import AsyncMock, patch
from pathlib import Path

# Add gateway dir to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth.s7g_middleware import custom_auth_fn

@pytest.mark.asyncio
@patch("auth.s7g_client.S7GClient.propose", side_effect=Exception("S7G Nodes Offline (503 Service Unavailable)"))
@patch("auth.fallback.FallbackManager.execute_fallback_inference")
async def test_s7g_outage_chaos_fallback(mock_fallback, mock_propose):
    """Chaos Test: S7G nodes completely offline -> Fallback inference executed successfully."""
    # Mock fallback returning response dict
    mock_fallback.return_value = {
        "choices": [{"message": {"content": "Fallback inference result"}}]
    }

    result = await custom_auth_fn(
        token="test-token",
        request_body={"model": "sovereign-llama3", "messages": [{"role": "user", "content": "hi"}]},
        method="/chat/completions"
    )

    # Decision should be true and fallback payload should be injected in metadata
    assert result["decision"] is True
    assert "fallback_response" in result["metadata"]
    assert result["metadata"]["fallback_response"]["choices"][0]["message"]["content"] == "Fallback inference result"
    print("\n🔥 Outage chaos fallback verified successfully.")
