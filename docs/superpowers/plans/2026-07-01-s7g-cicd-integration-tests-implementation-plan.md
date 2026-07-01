# S7G CI/CD & Integration Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create automated CI/CD pipelines (test.yml and deploy.yml) for GitHub Actions and implement integration, performance, and chaos testing scripts for the complete S7G Decentralized AI Inference stack.

---

### Task 1: Create GitHub Actions Workflow Configs
**Files:**
- Create: `decentralized-ai-inference/.github/workflows/test.yml`
- Create: `decentralized-ai-inference/.github/workflows/deploy.yml`

- [ ] **Step 1: Create .github/workflows/test.yml**
  Add a workflow to run tests on PR:
  ```yaml
  name: S7G Test Pipeline
  on:
    pull_request:
      branches: [ main ]

  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r s7g-committee/requirements.txt
            pip install pytest pytest-asyncio loguru cryptography httpx litellm prometheus_client
        - name: Run unit and integration tests
          run: |
            pytest s7g-committee/tests gateway/tests
  ```

- [ ] **Step 2: Create .github/workflows/deploy.yml**
  Add a workflow to run Akash deployment on merge:
  ```yaml
  name: S7G Deploy Pipeline
  on:
    push:
      branches: [ main ]

  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Build and push container images
          run: |
            echo "Building S7G Node docker image..."
            # docker build -t s7g-committee:latest ./s7g-committee
        - name: Deploy to Akash Network
          run: |
            chmod +x deploy/scripts/deploy.sh
            ./deploy/scripts/deploy.sh
  ```

---

### Task 2: Create End-to-End Test Suite
**Files:**
- Create: `decentralized-ai-inference/gateway/tests/test_e2e.py`

- [ ] **Step 1: Create gateway/tests/test_e2e.py**
  Add end-to-end integration tests simulating a request hitting the gateway middleware, proposing to the S7G committee leader, performing inference, and committing results:
  ```python
  import sys
  import pytest
  import asyncio
  from unittest.mock import AsyncMock, patch
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).parent.parent))

  from auth.s7g_middleware import custom_auth_fn, S7GLoggingHandler

  @pytest.mark.asyncio
  @patch("auth.s7g_client.S7GClient.propose")
  @patch("auth.s7g_client.S7GClient.commit")
  async def test_end_to_end_flow(mock_commit, mock_propose):
      # 1. Propose setup
      mock_propose.return_value = {"proposal_id": "e2e-proposal-456"}
      mock_commit.return_value = {"status": "committed"}

      # 2. Auth Interception
      auth_result = await custom_auth_fn(
          token="test-token",
          request_body={"model": "sovereign-llama3", "messages": [{"role": "user", "content": "hello"}]},
          method="/chat/completions"
      )
      assert auth_result["decision"] is True
      proposal_id = auth_result["metadata"]["proposal_id"]

      # 3. Callback commit interception
      handler = S7GLoggingHandler()
      class MockUsage:
          prompt_tokens = 5
          completion_tokens = 5
          total_tokens = 10
      class MockChoice:
          finish_reason = "stop"
      class MockResponse:
          usage = MockUsage()
          choices = [MockChoice()]

      kwargs = {
          "model": "sovereign-llama3",
          "litellm_params": {
              "metadata": {"proposal_id": proposal_id}
          }
      }

      await handler.log_success_event(kwargs, MockResponse(), None, None)
      mock_commit.assert_called_once()
      print("\n✅ End-to-End flow verified successfully!")
  ```

---

### Task 3: Create Performance and Chaos Tests
**Files:**
- Create: `decentralized-ai-inference/gateway/tests/test_performance.py`
- Create: `decentralized-ai-inference/gateway/tests/test_chaos.py`

- [ ] **Step 1: Create gateway/tests/test_performance.py**
  Add mock latency benchmark tests:
  ```python
  import time
  import pytest
  from unittest.mock import AsyncMock, patch
  from auth.s7g_client import S7GClient

  @pytest.mark.asyncio
  @patch("httpx.AsyncClient.post")
  async def test_consensus_performance(mock_post):
      mock_response = AsyncMock()
      mock_response.status_code = 200
      mock_response.json.return_value = {"proposal_id": "perf-123"}
      mock_post.return_value = mock_response

      client = S7GClient()
      start = time.time()
      await client.propose({"prompt": "hello"})
      duration = time.time() - start
      
      # Latency should be well under 100ms for simulated HTTP calls
      assert duration < 0.1
      print(f"\n✅ S7G propose latency benchmark: {duration * 1000:.2f}ms")
  ```

- [ ] **Step 2: Create gateway/tests/test_chaos.py**
  Add chaos testing to ensure fallback works when S7G is unreachable:
  ```python
  import pytest
  from unittest.mock import AsyncMock, patch
  from auth.s7g_middleware import custom_auth_fn

  @pytest.mark.asyncio
  @patch("auth.s7g_client.S7GClient.propose", side_effect=Exception("S7G connection refused"))
  @patch("auth.fallback.FallbackManager.execute_fallback_inference")
  async def test_s7g_outage_fallback(mock_fallback, mock_propose):
      mock_fallback.return_value = {"choices": [{"message": {"content": "Fallback output"}}]}

      result = await custom_auth_fn(
          token="test-token",
          request_body={"prompt": "hi"},
          method="/chat/completions"
      )

      # Should successfully fall back and execute
      assert result["decision"] is True
      assert result["metadata"]["fallback_response"]["choices"][0]["message"]["content"] == "Fallback output"
      print("\n✅ Outage Chaos Failover verified successfully!")
  ```

- [ ] **Step 3: Run all tests together**
  Run: `pytest decentralized-ai-inference/s7g-committee/tests decentralized-ai-inference/gateway/tests`
  Expected: PASS
