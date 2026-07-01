# S7G Gateway Middleware Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a custom authentication and logging middleware stack for LiteLLM that connects it end-to-end with the S7G committee node cluster for request provenance and response token usage auditing.

**Architecture:** 
1. **Custom Auth Hook (`custom_auth_fn`)**: Intercepts the chat completion request, forwards the payload to `/propose` on the S7G leader, and stores the `proposal_id` in the request metadata.
2. **Custom Logger Class (`S7GLoggingHandler`)**: Intercepts successful completions, extracts usage metrics (prompt tokens, completion tokens, model name, and response hash), and posts them to the S7G committee `/commit` endpoint.

---

### Task 1: Write Custom Middleware & Logger
**Files:**
- Create: `decentralized-ai-inference/gateway/auth/s7g_middleware.py`

- [ ] **Step 1: Create decentralized-ai-inference/gateway/auth/s7g_middleware.py**
  Create the middleware with the following Python code:
  ```python
  import httpx
  import logging
  import os
  from typing import Dict, Any
  from litellm.integrations.custom_logger import CustomLogger

  logger = logging.getLogger("s7g_middleware")
  logger.setLevel(logging.INFO)

  S7G_NODE_URL = os.getenv("S7G_NODE_URL", "http://s7g-node-1:1317")

  # Global request mapping: request_id -> proposal_id
  # Used to bridge the custom auth phase to the logging callback phase
  request_proposal_map: Dict[str, str] = {}

  async def custom_auth_fn(token: str, request_body: dict, method: str) -> dict:
      """Custom authentication hook for LiteLLM.
      
      Submits the inference request payload to the S7G committee node for consensus.
      """
      # Only intercept chat completions
      if "/chat/completions" not in method:
          return {"decision": True}

      try:
          logger.info("Intercepted request. Submitting proposal to S7G committee...")
          async with httpx.AsyncClient(timeout=10.0) as client:
              response = await client.post(
                  f"{S7G_NODE_URL}/propose",
                  json={"payload": request_body}
              )
              if response.status_code != 200:
                  logger.error(f"S7G proposal rejected: {response.text}")
                  raise Exception("S7G consensus proposal failed")
                  
              res_data = response.json()
              proposal_id = res_data["proposal_id"]
              
              # Extract or generate a local request identifier to link with the callback
              # LiteLLM passes metadata, we can return user_id or team_id to route context
              logger.info(f"S7G proposal accepted. Proposal ID: {proposal_id}")
              return {
                  "decision": True,
                  "metadata": {"proposal_id": proposal_id}
              }
      except Exception as e:
          logger.error(f"S7G middleware auth failure: {e}")
          # Return false or raise exception to reject unauthorized requests
          raise Exception(f"S7G authorization consensus failed: {e}")

  class S7GLoggingHandler(CustomLogger):
      """Custom logger for LiteLLM.
      
      Submits final model output token usage and metadata to S7G node for commitment.
      """
      async def log_success_event(self, kwargs, response_obj, start_time, end_time):
          try:
              logger.info("Intercepted model response. Finalizing transaction on S7G ledger...")
              
              # Extract the proposal ID from metadata
              metadata = kwargs.get("litellm_params", {}).get("metadata", {}) or {}
              proposal_id = metadata.get("proposal_id")
              
              if not proposal_id:
                  logger.warning("No S7G proposal ID found in response metadata. Skipping commit.")
                  return

              # Construct the response summary payload
              response_summary = {
                  "model": kwargs.get("model", "unknown"),
                  "prompt_tokens": response_obj.usage.prompt_tokens,
                  "completion_tokens": response_obj.usage.completion_tokens,
                  "total_tokens": response_obj.usage.total_tokens,
                  "finish_reason": response_obj.choices[0].finish_reason if response_obj.choices else "unknown"
              }

              async with httpx.AsyncClient(timeout=10.0) as client:
                  commit_response = await client.post(
                      f"{S7G_NODE_URL}/commit",
                      json={
                          "request_id": proposal_id,
                          "response_summary": response_summary
                      }
                  )
                  if commit_response.status_code == 200:
                      logger.info(f"Successfully committed transaction {proposal_id} to S7G ledger.")
                  else:
                      logger.error(f"Failed to commit transaction to S7G: {commit_response.text}")
          except Exception as e:
              logger.error(f"Error in S7G logging callback: {e}")

      async def log_failure_event(self, kwargs, response_obj, start_time, end_time):
          # We don't commit failed requests, but we log the error
          logger.error(f"LiteLLM request failed: {response_obj}")
  ```

---

### Task 2: Configure LiteLLM
Create the configuration mapping for the custom hooks.

**Files:**
- Create: `decentralized-ai-inference/gateway/liteLLM/config.yaml`

- [ ] **Step 1: Create decentralized-ai-inference/gateway/liteLLM/config.yaml**
  Create the config file with:
  ```yaml
  model_list:
    - model_name: sovereign-llama3
      litellm_params:
        model: openai/meta-llama/Meta-Llama-3-8B-Instruct
        api_base: http://inference-engine:8000/v1
        api_key: local-secret-key

  general_settings:
    custom_auth: auth.s7g_middleware.custom_auth_fn

  litellm_settings:
    callbacks: ["auth.s7g_middleware.S7GLoggingHandler"]
  ```

---

### Task 3: Integration and Unit Tests
**Files:**
- Create: `decentralized-ai-inference/gateway/tests/test_middleware.py`

- [ ] **Step 1: Create test_middleware.py**
  Add mock testing for custom auth and callbacks:
  ```python
  import sys
  import pytest
  from unittest.mock import AsyncMock, patch
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).parent.parent))

  from auth.s7g_middleware import custom_auth_fn, S7GLoggingHandler

  @pytest.mark.asyncio
  @patch("httpx.AsyncClient.post")
  async def test_custom_auth_fn(mock_post):
      # Mock S7G node `/propose` success response
      mock_response = AsyncMock()
      mock_response.status_code = 200
      mock_response.json.return_value = {"proposal_id": "test-proposal-123"}
      mock_post.return_value = mock_response

      result = await custom_auth_fn(
          token="test-token",
          request_body={"model": "sovereign-llama3", "messages": []},
          method="/chat/completions"
      )

      assert result["decision"] is True
      assert result["metadata"]["proposal_id"] == "test-proposal-123"

  @pytest.mark.asyncio
  @patch("httpx.AsyncClient.post")
  async def test_s7g_logging_handler(mock_post):
      # Mock S7G node `/commit` success response
      mock_response = AsyncMock()
      mock_response.status_code = 200
      mock_post.return_value = mock_response

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
      mock_post.assert_called_once()
  ```

- [ ] **Step 2: Run pytest to verify**
  Run: `pytest decentralized-ai-inference/gateway/tests`
  Expected: PASS
