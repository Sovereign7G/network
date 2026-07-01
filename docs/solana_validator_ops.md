# Solana Validator Operations — S7G Network

## Status: SETUP READY (awaiting SOL stake)
## Date: June 23, 2026

---

## Overview

S7G operates a Solana validator node to:
- Earn SOL staking rewards (~6-8% APY)
- Participate in Solana consensus
- Monitor MoneyGram's validator activity
- Position as DePIN infrastructure for institutional payments

---

## Deployment

### Prerequisites

| Resource | Requirement | Status |
|----------|-------------|--------|
| Server | 8+ CPU, 32GB RAM, 1TB NVMe SSD | ✅ Available |
| Network | 1 Gbps, low latency | ✅ Available |
| SOL (testnet) | ~1 SOL for testing | ❌ Need airdrop |
| SOL (mainnet) | ~1+ SOL for staking | ❌ Need purchase |
| Domain | api.7g.sol | ✅ Owned |

### Setup Commands

```bash
# Clone repo
cd /media/cherry/4A21-00001/New\ folder/AGE\ REPUBLIC

# Run setup script (testnet first for testing)
sudo bash scripts/solana_validator_setup.sh testnet

# After testnet validation, switch to mainnet
sudo bash scripts/solana_validator_setup.sh mainnet
```

### Post-Setup

```bash
# Check validator status
solana validators --url https://api.mainnet-beta.solana.com

# Monitor logs
journalctl -u solana-validator -f

# Check balance
solana balance --url https://api.mainnet-beta.solana.com
```

---

## Monitoring

### Prometheus Metrics
The validator exposes metrics on port 8899:
- `/metrics` — Prometheus endpoint
- Node exporter on port 9100

### Key Metrics to Watch

| Metric | Threshold | Alert |
|--------|-----------|-------|
| validator_credits | Increasing | Track epoch rewards |
| skip_rate | <5% | High skip rate = performance issue |
| root_slot | Increasing | Healthy chain progression |
| balance | >1 SOL | Low balance = can't pay fees |

### MoneyGram Validator Tracking

MoneyGram's Solana validator identity will be tracked and monitored via our validator monitoring agent.

---

## Operations

### Daily Checks
```bash
# Check validator status
solana validators --url https://api.mainnet-beta.solana.com | grep S7G

# Check recent performance
solana validator-info get --url https://api.mainnet-beta.solana.com

# Check disk usage
df -h /home/solana/ledger

# Check system resources
htop
```

### Epoch Management
```bash
# Check current epoch
solana epoch-info --url https://api.mainnet-beta.solana.com

# Check rewards
solana epoch-rewards --url https://api.mainnet-beta.solana.com
```

### Backup
```bash
# Backup validator keys
cp /home/solana/validator-keypair.json /backup/solana/
cp /home/solana/vote-keypair.json /backup/solana/
cp /home/solana/stake-keypair.json /backup/solana/
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Validator not starting | Insufficient SOL for rent | Fund identity account |
| High skip rate | Network latency | Check bandwidth, reduce gossip |
| Disk full | Ledger growth | Increase --limit-ledger-size |
| Slashing | Double signing | Run only one instance |
| Connection refused | Firewall | Check ufw rules |

---

## Integration with S7G Network

The Solana validator feeds rewards into the S7G YieldRouter:

```
Solana Validator
    │
    │ SOL rewards (6-8% APY)
    ▼
S7G YieldRouter
    │
    │ 20% NodeStaking / 15% Treasury
    ▼
S7G Stakers & Treasury
```

Staking SOL through S7G's validator earns:
1. Native SOL rewards (~6-8% APY)
2. S7G node operator rewards (additional S7G tokens)
3. Reputation multiplier for active validators

---

*Document maintained by S7G Operations. Updated: 2026-06-23.*
