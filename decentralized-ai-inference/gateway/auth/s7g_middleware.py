import os
import logging
from typing import Dict, Any, Optional
from litellm.integrations.custom_logger import CustomLogger

from auth.s7g_client import S7GClient
from auth.fallback import FallbackManager
from auth.metrics import S7G_PROPOSE_TOTAL, S7G_COMMIT_TOTAL, S7G_CONSENSUS_LATENCY

logger = logging.getLogger("s7g_middleware")
logger.setLevel(logging.INFO)

# Singletons
s7g_client = S7GClient()
fallback_manager = FallbackManager()

async def custom_auth_fn(token: str, request_body: dict, method: str) -> dict:
    """LiteLLM custom auth hook.
    
    Submits a consensus proposal to the S7G committee node before executing inference.
    """
    # Only intercept chat completions requests
    if "/chat/completions" not in method:
        return {"decision": True}

    start_time = __import__("time").time()
    try:
        logger.info("Submitting consensus proposal to S7G Committee...")
        res_data = await s7g_client.propose(request_body)
        proposal_id = res_data["proposal_id"]
        
        # Record successful consensus metrics
        S7G_PROPOSE_TOTAL.labels(status="success").inc()
        S7G_CONSENSUS_LATENCY.observe(__import__("time").time() - start_time)
        
        logger.info(f"S7G PBFT consensus reached. Proposal ID: {proposal_id}")
        return {
            "decision": True,
            "metadata": {"proposal_id": proposal_id}
        }
    except Exception as e:
        logger.error(f"S7G committee consensus failed: {e}")
        S7G_PROPOSE_TOTAL.labels(status="failed").inc()
        
        # Try fallback options (Bittensor/Secondary Akash)
        fallback_res = await fallback_manager.execute_fallback_inference(request_body)
        if fallback_res:
            logger.info("Successfully executed inference using fallback provider.")
            # If fallback handled the request directly, return decision=True and inject response
            return {
                "decision": True,
                "metadata": {"fallback_response": fallback_res}
            }
            
        raise Exception(f"S7G consensus failed and no fallback available: {e}")

class S7GLoggingHandler(CustomLogger):
    """Custom LiteLLM Logger class.
    
    Submits finalized response token usage statistics to the S7G committee.
    """
    async def log_success_event(self, kwargs, response_obj, start_time, end_time):
        try:
            # Check if this request was handled by a fallback provider
            metadata = kwargs.get("litellm_params", {}).get("metadata", {}) or {}
            fallback_res = metadata.get("fallback_response")
            if fallback_res:
                logger.info("Request was executed by fallback, skipping S7G commit.")
                return

            proposal_id = metadata.get("proposal_id")
            if not proposal_id:
                logger.warning("No S7G proposal ID found in response metadata. Skipping commit.")
                return

            # Prepare usage payload
            response_summary = {
                "model": kwargs.get("model", "unknown"),
                "prompt_tokens": response_obj.usage.prompt_tokens,
                "completion_tokens": response_obj.usage.completion_tokens,
                "total_tokens": response_obj.usage.total_tokens,
                "finish_reason": response_obj.choices[0].finish_reason if response_obj.choices else "stop"
            }

            logger.info(f"Submitting final usage commit for {proposal_id} to S7G committee...")
            await s7g_client.commit(proposal_id, response_summary)
            S7G_COMMIT_TOTAL.labels(status="success").inc()
            logger.info(f"Transaction {proposal_id} committed to S7G ledger.")
        except Exception as e:
            logger.error(f"Failed to submit S7G commit: {e}")
            S7G_COMMIT_TOTAL.labels(status="failed").inc()

    async def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        logger.error(f"Inference request failed: {response_obj}")
