import sys
import pytest
from unittest.mock import AsyncMock, patch
from pathlib import Path

# Add gateway dir to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth.s7g_middleware import custom_auth_fn, S7GLoggingHandler

@pytest.mark.asyncio
@patch("auth.s7g_client.S7GClient.propose")
async def test_custom_auth_fn_success(mock_propose):
    # Mock propose returning proposal ID
    mock_propose.return_value = {"proposal_id": "test-proposal-123"}

    result = await custom_auth_fn(
        token="test-token",
        request_body={"model": "sovereign-llama3", "messages": [{"role": "user", "content": "hi"}]},
        method="/chat/completions"
    )

    assert result["decision"] is True
    assert result["metadata"]["proposal_id"] == "test-proposal-123"

@pytest.mark.asyncio
@patch("auth.s7g_client.S7GClient.commit")
async def test_s7g_logging_handler_success(mock_commit):
    mock_commit.return_value = {"status": "committed"}

    handler = S7GLoggingHandler()
    
    class MockUsage:
        prompt_tokens = 10
        completion_tokens = 20
        total_tokens = 30

    class MockChoice:
        finish_reason = "stop"

    class MockResponseObj:
        usage = MockUsage()
        choices = [MockChoice()]

    kwargs = {
        "model": "sovereign-llama3",
        "litellm_params": {
            "metadata": {"proposal_id": "test-proposal-123"}
        }
    }

    await handler.log_success_event(kwargs, MockResponseObj(), None, None)
    mock_commit.assert_called_once_with("test-proposal-123", {
        "model": "sovereign-llama3",
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30,
        "finish_reason": "stop"
    })
