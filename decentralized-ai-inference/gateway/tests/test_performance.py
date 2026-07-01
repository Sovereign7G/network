import time
import sys
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# Add gateway dir to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth.s7g_client import S7GClient

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_propose_latency_performance(mock_post):
    """Measures consensus propose overhead to ensure latency remains under threshold."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"proposal_id": "perf-123"}
    mock_post.return_value = mock_response

    client = S7GClient()
    start_time = time.time()
    
    # Run 10 sequential proposal requests
    for _ in range(10):
        await client.propose({"prompt": "performance test"})
        
    total_duration = time.time() - start_time
    avg_latency = (total_duration / 10) * 1000
    
    # Assert average mock latency is well under 100ms
    assert avg_latency < 100.0
    print(f"\n⚡ Average proposal latency: {avg_latency:.2f}ms")
