# S7G Cookbook — Walkthrough Guides

## 1. Check Swarm Health

```python
from s7g import S7GClient

client = S7GClient()
status = client.swarm_status()
print(f"Agents: {status['agents_online']}/{status['agents_total']}")
print(f"Status: {status['status']}")
```

## 2. Cross-Chain Settlement

```python
from s7g.domains.bridge import cctp_cross_chain_settle

# Settle USDC from Base to Solana
result = cctp_cross_chain_settle(
    amount=1000,
    target_chain="solana"
)
print(f"Settlement: {result.data['tx_hash']}")
```

## 3. Run the Full Test Suite

```bash
# Quick test (30 seconds)
python3 tests/test_session_comprehensive.py

# All 19 tests should pass
```

## 4. Check Solana Validator

```python
from s7g.domains.solana import solana_validator_info, solana_network_stats

info = solana_validator_info()
stats = solana_network_stats()
print(f"Validators: {stats['total_validators']}")
print(f"Stake: {info['stake']} SOL")
```

## 5. Deploy Docker Stack

```bash
# Install Docker Compose
sudo apt install docker-compose

# Deploy all services
cd /path/to/s7g
sudo docker-compose up -d

# Verify
sudo docker ps
# Expected: chatwoot, mautic, postgres, mysql, redis
```

## 6. Restart Telegram Bot

```bash
sudo systemctl restart s7g-telegram
sudo systemctl status s7g-telegram
```

Check Telegram @sovereign7g_bot — type /status

## 7. Generate Ecosystem Content

```python
# Uses local Ollama (qwen2.5:7b)
python3 agents/content_generator.py --once
```

## 8. Monitor Agent Event Bus

```python
# Test all 4 event chains
python3 -m bridge.agent_event_bus --test
# Expected: All 4 chains verified
```

## 9. Test Event Fabric

```python
python3 agents/event_fabric.py --once
# Expected: 9 events routed across 7 ecosystems
```

## 10. Verify Orchestrator

```python
python3 agents/swarm_orchestrator.py --once
# Expected: Status NOMINAL, 44+ files detected
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Telegram bot silent | Token/chat ID not set | `export TELEGRAM_BOT_TOKEN="..."` |
| Mautic not loading | MySQL not ready | Check `sudo docker logs mautic` |
| Ollama slow | GPU VRAM | Reduce model size or batch |
| Tests fail | Wrong working dir | Run from project root |
