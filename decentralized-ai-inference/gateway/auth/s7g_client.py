import httpx
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("s7g_client")

class S7GClient:
    """HTTP client for communicating with S7G validator nodes.
    
    Implements round-robin failover and retry logic across 4 committee replicas.
    """

    def __init__(self, node_urls: Optional[List[str]] = None):
        self.node_urls = node_urls or [
            "http://s7g-node-1:1317",
            "http://s7g-node-2:1317",
            "http://s7g-node-3:1317",
            "http://s7g-node-4:1317"
        ]
        self._current_index = 0

    def _next_node_url(self) -> str:
        url = self.node_urls[self._current_index]
        self._current_index = (self._current_index + 1) % len(self.node_urls)
        return url

    async def propose(self, payload: dict, retries: int = 3) -> Dict[str, Any]:
        """Submit a proposal to the committee nodes using round-robin retry failover."""
        import uuid
        import time
        
        request_id = payload.get("request_id") or str(uuid.uuid4())
        timestamp = int(time.time())
        
        json_data = {
            "request_id": request_id,
            "payload": payload,
            "timestamp": timestamp
        }
        
        for attempt in range(retries):
            url = self._next_node_url()
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(f"{url}/propose", json=json_data)
                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code == 403:
                        # 403 indicates we hit a follower node; try next node (which may be the leader)
                        logger.warning(f"Hit follower node at {url}, retrying next node...")
                    else:
                        logger.error(f"S7G node proposal returned status {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"Failed to propose to S7G node {url} on attempt {attempt+1}: {e}")
        
        raise Exception("S7G committee consensus proposal failed after retries.")

    async def commit(self, request_id: str, response_summary: dict, retries: int = 3) -> Dict[str, Any]:
        """Submit final token usage metrics for commitment."""
        for attempt in range(retries):
            url = self._next_node_url()
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.post(
                        f"{url}/commit",
                        json={
                            "request_id": request_id,
                            "response_summary": response_summary
                        }
                    )
                    if response.status_code == 200:
                        return response.json()
            except Exception as e:
                logger.error(f"Failed to commit to S7G node {url} on attempt {attempt+1}: {e}")
        
        raise Exception("S7G committee commit failed after retries.")
