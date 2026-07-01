import sys
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from pathlib import Path

# Add gateway dir to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth.s7g_middleware import custom_auth_fn, S7GLoggingHandler

@pytest.mark.asyncio
@patch("auth.s7g_client.S7GClient.propose")
@patch("auth.s7g_client.S7GClient.commit")
async def test_full_inference_flow_e2e(mock_commit, mock_propose):
    """E2E Test: Gateway -> S7G Proposal -> Inference -> S7G Commit."""
    # 1. Mock S7G proposal response
    mock_propose.return_value = {"proposal_id": "e2e-proposal-uuid-123"}
    mock_commit.return_value = {"status": "committed"}

    # 2. Simulate Chat Completion proposal request
    auth_result = await custom_auth_fn(
        token="sk-sovereign-mesh-key",
        request_body={
            "model": "sovereign-llama3",
            "messages": [{"role": "user", "content": "What is 7G?"}]
        },
        method="/chat/completions"
    )

    assert auth_result["decision"] is True
    proposal_id = auth_result["metadata"]["proposal_id"]
    assert proposal_id == "e2e-proposal-uuid-123"

    # 3. Simulate success logging callback post-inference
    handler = S7GLoggingHandler()
    
    class MockUsage:
        prompt_tokens = 25
        completion_tokens = 45
        total_tokens = 70

    class MockChoice:
        finish_reason = "stop"

    class MockResponseObj:
        usage = MockUsage()
        choices = [MockChoice()]

    kwargs = {
        "model": "sovereign-llama3",
        "litellm_params": {
            "metadata": {"proposal_id": proposal_id}
        }
    }

    await handler.log_success_event(kwargs, MockResponseObj(), None, None)
    mock_commit.assert_called_once_with(proposal_id, {
        "model": "sovereign-llama3",
        "prompt_tokens": 25,
        "completion_tokens": 45,
        "total_tokens": 70,
        "finish_reason": "stop"
    })
