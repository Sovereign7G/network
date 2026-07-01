import logging
import os
import httpx
from typing import Dict, Any, Optional

logger = logging.getLogger("s7g_fallback")

class FallbackManager:
    """Orchestrates failover to alternative decentralized resource networks.
    
    If the S7G committee node cluster goes completely offline, requests can fall back
    to a secondary Akash provider or Bittensor subnet (e.g. SN1) to maintain service.
    """

    def __init__(self):
        self.bittensor_api_url = os.getenv("BITTENSOR_API_URL", "")
        self.akash_fallback_url = os.getenv("AKASH_FALLBACK_URL", "")
        self.fallback_enabled = os.getenv("FALLBACK_ENABLED", "true").lower() == "true"

    async def execute_fallback_inference(self, payload: dict) -> Optional[dict]:
        """Tries fallback providers sequentially if S7G is unreachable."""
        if not self.fallback_enabled:
            return None

        # 1. Try Secondary Akash Provider
        if self.akash_fallback_url:
            try:
                logger.info(f"Attempting fallback to secondary Akash provider: {self.akash_fallback_url}")
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(f"{self.akash_fallback_url}/v1/chat/completions", json=payload)
                    if response.status_code == 200:
                        return response.json()
            except Exception as e:
                logger.error(f"Secondary Akash fallback failed: {e}")

        # 2. Try Bittensor Subnet Gateway
        if self.bittensor_api_url:
            try:
                logger.info(f"Attempting fallback to Bittensor Subnet: {self.bittensor_api_url}")
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.post(f"{self.bittensor_api_url}/v1/chat/completions", json=payload)
                    if response.status_code == 200:
                        return response.json()
            except Exception as e:
                logger.error(f"Bittensor fallback failed: {e}")

        return None
