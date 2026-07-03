# gateway/s7g_client.py
import httpx, time
from typing import Dict, Any

class S7GClient:
    def __init__(self, endpoint: str, timeout: float = 35.0):
        self.endpoint = endpoint
        self.client = httpx.AsyncClient(timeout=timeout)

    async def propose(self, rid: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        r = await self.client.post(f"{self.endpoint}/propose", json={
            "request_id": rid, "payload": payload, "timestamp": int(time.time())
        })
        r.raise_for_status()
        return r.json()

    async def commit(self, pid: str, summary: Dict[str, Any]) -> Dict[str, Any]:
        r = await self.client.post(f"{self.endpoint}/commit", json={
            "request_id": pid, "response_summary": summary
        })
        r.raise_for_status()
        return r.json()

    async def health(self) -> bool:
        try:
            r = await self.client.get(f"{self.endpoint}/health")
            return r.status_code == 200
        except: return False

    async def status(self) -> Dict[str, Any]:
        r = await self.client.get(f"{self.endpoint}/status")
        r.raise_for_status(); return r.json()
