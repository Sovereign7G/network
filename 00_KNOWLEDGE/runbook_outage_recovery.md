# Runbook: AI Outage Recovery

## Diagnosis: KV Cache Saturation (Infinite hang / timeout)

**Observed:** Requests hang >30s, LFM server logs show `slot unavailable` or `kv_cache full`

**Immediate Actions:**

```bash
# 1. Check current cache pressure
curl -s http://localhost:8081/metrics | grep kv_cache_usage

# 2. If >85%, restart the inference worker (clears cache)
systemctl --user restart age-lfm-server.service

# 3. Reduce default max_tokens for affected model
sqlite3 ~/.config/bifrost/config.db \
  "UPDATE governance_model_parameters SET max_tokens=2048 WHERE model='lfm2.5-8b-a1b'"
```

**Prevention:**  
Add alert: `kv_cache_usage > 0.85` → page on-call before saturation.

---

## Diagnosis: Capacity Shedding

**Observed:** Free tier blocked, paid tier working. Upgrade prompt displayed.

**Immediate Actions:**

```bash
# 1. Verify shed policy is intentional
grep "capacity_shedding" /var/log/sovereign/gateway.log | tail -5

# 2. If unintentional, re-enable free tier
sqlite3 ~/.config/bifrost/config.db \
  "UPDATE config_keys SET rate_limit_tier='unlimited' WHERE provider='bifrost-local'"

# 3. Route some paid traffic to backup (if available)
# In bifrost_config.yml: add fallback provider
```

**Prevention:**  
Implement honest `429 Retry-After` responses (no deceptive upgrade prompts).

---

## Diagnosis: Software Regression (Immediate 5xx)

**Observed:** Model returns 500 error instantly after an update.

**Immediate Actions:**

```bash
# 1. Rollback to previous known-good version
cd /media/fiji/4A21-00001/New\ folder/AGE\ REPUBLIC/07_MODELS/
mv LFM2.5-8B-A1B-Q4_K_M.gguf LFM2.5-8B-A1B-Q4_K_M.gguf.bad
cp LFM2.5-8B-A1B-Q4_K_M.gguf.good LFM2.5-8B-A1B-Q4_K_M.gguf

# 2. Restart the model server
systemctl --user restart age-lfm-server.service

# 3. Verify rollback worked
curl -s http://localhost:8081/v1/models | grep "LFM2.5"
```

**Prevention:**  
Keep last 3 working `.gguf` snapshots. Use canary deployment: test new model on port 8083 before swapping.
