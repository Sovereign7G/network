# Outage Triage Cheat Sheet

| If you see... | Likely cause | Immediate action |
|---------------|--------------|------------------|
| Free tier: "upgrade" ; Paid: OK | **Capacity shedding** | Route to backup provider |
| Immediate 500 error on one model | **Software regression** | Rollback model version |
| Infinite loading / timeout | **KV cache saturation** | Reduce context window |
| DNS failure | **Edge/CDN outage** | Failover to secondary endpoint |
| 504 Gateway Timeout | **Orchestration crash** | Bypass LB, hit worker directly |

## Sovereign-only metrics to watch
- `kv_cache_usage` > 85% → pre-failure
- `slot_idle` count = 0 → saturation imminent
- Model-specific error rate divergence → compartmentalization working
