import httpx
import time
from typing import Dict, Any

class S7GClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.client = httpx.AsyncClient(timeout=30.0)

    async def propose(self, request_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = await self.client.post(
            f"{self.endpoint}/propose",
            json={
                "request_id": request_id,
                "payload": payload,
                "timestamp": int(time.time())
            }
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
