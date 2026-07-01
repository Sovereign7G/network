import time
from prometheus_client import Counter, Histogram

# ===== PROMETHEUS METRICS =====

S7G_PROPOSE_TOTAL = Counter(
    "s7g_propose_total",
    "Total number of proposal submissions to S7G committee nodes",
    ["status"]  # "success" or "failed"
)

S7G_COMMIT_TOTAL = Counter(
    "s7g_commit_total",
    "Total number of token usage commitments to S7G ledger",
    ["status"]  # "success" or "failed"
)

S7G_CONSENSUS_LATENCY = Histogram(
    "s7g_consensus_latency_seconds",
    "Time taken for S7G consensus nodes to reach PBFT agreement"
)
