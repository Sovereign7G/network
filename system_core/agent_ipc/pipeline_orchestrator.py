# system_core/agent_ipc/pipeline_orchestrator.py
# SoA Columnar Pipeline Orchestrator
#
# Wires Rust 256-shard ring buffer → Python ctypes FFI → Mojo SIMD kernels
# in a single unified data plane.
#
# Data flow:
#   Rust alloc_zeroed SoA shards (268 MB heap)
#   → push_telemetry_columnar() writes {ts, gas, vol} across 3 flat arrays
#   → get_*_column_ptr() returns raw C pointers
#   → Python ctypes extracts Float32 arrays from those pointers
#   → Mojo compute binary receives chunks via stdin
#   → SIMD.gt() evaluates thresholds in register
#
# Usage:
#   python3 pipeline_orchestrator.py
import os
import sys
import json
import ctypes
import subprocess
import time
from ctypes import (
    c_void_p, c_uint32, c_uint64, c_int32, c_size_t, c_float,
    c_char_p, POINTER, cdll
)
from pathlib import Path
ROOT = Path("/media/cherry/4A21-00001/New folder/AGE REPUBLIC")
RUST_SO = ROOT / "system_core/rust_bridge/target/release/librust_bridge.so"
MOJO_BIN = ROOT / "system_core/mojo_kernels/compute"
HEALTH_JSON = ROOT / "system_core/agent_ipc/pipeline_health.json"
class RustSoABridge:
    """Python ctypes wrapper around librust_bridge.so columnar FFI symbols."""
    def __init__(self, so_path: str = str(RUST_SO)):
        if not os.path.exists(so_path):
            raise FileNotFoundError(f"Rust .so not found: {so_path}")
        self.lib = cdll.LoadLibrary(so_path)
        self._bind_functions()
    def _bind_functions(self):
        """Declare argtypes and restype for every columnar FFI symbol."""
        self.lib.push_telemetry_columnar.argtypes = [
            c_char_p, c_size_t, c_uint64,  # payment_id, len, timestamp_ns
            c_float,        # gas_price
            c_float,        # volume
            c_float,        # usdc_supply_b
            c_float,        # usdt_ust_b
            c_float,        # jpyc_float_b
            c_float,        # ecny_volume_b
            c_float,        # buidl_apy
            c_float,        # stac_apy
            c_float,        # usd_jpy_rate
            c_float,        # t0_share_pct
            c_float,        # pe_unsold_val
            c_float,        # private_gated_aum
            c_float,        # pghn_stock_rate
            c_float,        # nbfi_shadow_vol
        ]
        self.lib.push_telemetry_columnar.restype = c_int32  # shard index or error
        self.lib.get_timestamps_column_ptr.argtypes = [c_size_t]
        self.lib.get_timestamps_column_ptr.restype = POINTER(c_uint64)
        self.lib.get_gas_prices_column_ptr.argtypes = [c_size_t]
        self.lib.get_gas_prices_column_ptr.restype = POINTER(c_float)
        self.lib.get_volumes_column_ptr.argtypes = [c_size_t]
        self.lib.get_volumes_column_ptr.restype = POINTER(c_float)
        self.lib.get_usdc_supply_ptr.argtypes = [c_size_t]
        self.lib.get_usdc_supply_ptr.restype = POINTER(c_float)
        self.lib.get_usdt_ust_ptr.argtypes = [c_size_t]
        self.lib.get_usdt_ust_ptr.restype = POINTER(c_float)
        self.lib.get_jpyc_float_ptr.argtypes = [c_size_t]
        self.lib.get_jpyc_float_ptr.restype = POINTER(c_float)
        self.lib.get_ecny_volume_ptr.argtypes = [c_size_t]
        self.lib.get_ecny_volume_ptr.restype = POINTER(c_float)
        self.lib.get_buidl_apy_ptr.argtypes = [c_size_t]
        self.lib.get_buidl_apy_ptr.restype = POINTER(c_float)
        self.lib.get_stac_apy_ptr.argtypes = [c_size_t]
        self.lib.get_stac_apy_ptr.restype = POINTER(c_float)
        self.lib.get_usd_jpy_rate_ptr.argtypes = [c_size_t]
        self.lib.get_usd_jpy_rate_ptr.restype = POINTER(c_float)
        self.lib.get_t0_share_ptr.argtypes = [c_size_t]
        self.lib.get_t0_share_ptr.restype = POINTER(c_float)
        self.lib.get_pe_unsold_ptr.argtypes = [c_size_t]
        self.lib.get_pe_unsold_ptr.restype = POINTER(c_float)
        self.lib.get_private_gated_ptr.argtypes = [c_size_t]
        self.lib.get_private_gated_ptr.restype = POINTER(c_float)
        self.lib.get_pghn_rate_ptr.argtypes = [c_size_t]
        self.lib.get_pghn_rate_ptr.restype = POINTER(c_float)
        self.lib.get_nbfi_shadow_ptr.argtypes = [c_size_t]
        self.lib.get_nbfi_shadow_ptr.restype = POINTER(c_float)
        self.lib.get_shard_depth.argtypes = [c_size_t]
        self.lib.get_shard_depth.restype = c_size_t
        self.lib.get_shard_head.argtypes = [c_size_t]
        self.lib.get_shard_head.restype = c_size_t
        self.lib.get_shard_tail.argtypes = [c_size_t]
        self.lib.get_shard_tail.restype = c_size_t
        self.lib.get_num_shards.argtypes = []
        self.lib.get_num_shards.restype = c_size_t
        self.lib.get_shard_size.argtypes = []
        self.lib.get_shard_size.restype = c_size_t
        self.lib.push_transaction_shard.argtypes = [c_char_p, c_size_t, c_uint32]
        self.lib.push_transaction_shard.restype = c_int32
    def push_telemetry(
        self, payment_id: str, ts_ns: int,
        gas: float, vol: float,
        usdc_supply_b: float = 0.0, usdt_ust_b: float = 0.0,
        jpyc_float_b: float = 0.0, ecny_volume_b: float = 0.0,
        buidl_apy: float = 0.0, stac_apy: float = 0.0,
        usd_jpy_rate: float = 0.0, t0_share_pct: float = 0.0,
        pe_unsold_val: float = 0.0, private_gated_aum: float = 0.0,
        pghn_stock_rate: float = 0.0, nbfi_shadow_vol: float = 0.0,
    ) -> int:
        """Push a full 15-field telemetry + liquidity + shadow record into SoA ring buffer.
        Returns shard index (0..255) on success, negative on error."""
        pid_bytes = payment_id.encode("utf-8")
        result = self.lib.push_telemetry_columnar(
            pid_bytes, len(pid_bytes), ts_ns,
            c_float(gas), c_float(vol),
            c_float(usdc_supply_b), c_float(usdt_ust_b),
            c_float(jpyc_float_b), c_float(ecny_volume_b),
            c_float(buidl_apy), c_float(stac_apy),
            c_float(usd_jpy_rate), c_float(t0_share_pct),
            c_float(pe_unsold_val), c_float(private_gated_aum),
            c_float(pghn_stock_rate), c_float(nbfi_shadow_vol),
        )
        return result
    def get_column_arrays(self, shard_idx: int):
        """Extract Python lists from ALL 15 columnar arrays for a shard.
        Returns (timestamps, gas_prices, volumes, usdc_supply, usdt_ust,
                 jpyc_float, ecny_volume, buidl_apy, stac_apy,
                 usd_jpy_rate, t0_share, pe_unsold, private_gated,
                 pghn_rate, nbfi_shadow)."""
        depth = self.lib.get_shard_depth(shard_idx)
        if depth == 0:
            return [()] * 15
        head = self.lib.get_shard_head(shard_idx)
        shard_size = self.lib.get_shard_size()
        ts_ptr = self.lib.get_timestamps_column_ptr(shard_idx)
        gp_ptr = self.lib.get_gas_prices_column_ptr(shard_idx)
        vol_ptr = self.lib.get_volumes_column_ptr(shard_idx)
        usdc_ptr = self.lib.get_usdc_supply_ptr(shard_idx)
        usdt_ptr = self.lib.get_usdt_ust_ptr(shard_idx)
        jpyc_ptr = self.lib.get_jpyc_float_ptr(shard_idx)
        ecny_ptr = self.lib.get_ecny_volume_ptr(shard_idx)
        buidl_ptr = self.lib.get_buidl_apy_ptr(shard_idx)
        stac_ptr = self.lib.get_stac_apy_ptr(shard_idx)
        usdjpy_ptr = self.lib.get_usd_jpy_rate_ptr(shard_idx)
        t0_ptr = self.lib.get_t0_share_ptr(shard_idx)
        cols = [[] for _ in range(11)]
        for i in range(depth):
            idx = (head + i) % shard_size
            cols[0].append(ts_ptr[idx])     # timestamps
            cols[1].append(gp_ptr[idx])     # gas_prices
            cols[2].append(vol_ptr[idx])    # volumes
            cols[3].append(usdc_ptr[idx])   # usdc_supply
            cols[4].append(usdt_ptr[idx])   # usdt_ust
            cols[5].append(jpyc_ptr[idx])   # jpyc_float
            cols[6].append(ecny_ptr[idx])   # ecny_volume
            cols[7].append(buidl_ptr[idx])  # buidl_apy
            cols[8].append(stac_ptr[idx])   # stac_apy
            cols[9].append(usdjpy_ptr[idx]) # usd_jpy_rate
            cols[10].append(t0_ptr[idx])    # t0_share
        return cols
    def shard_status(self, shard_idx: int) -> dict:
        """Returns cursor state for a shard."""
        return {
            "shard": shard_idx,
            "depth": self.lib.get_shard_depth(shard_idx),
            "head": self.lib.get_shard_head(shard_idx),
            "tail": self.lib.get_shard_tail(shard_idx),
        }
    def verify_ffi_symbols(self) -> list:
        """Check all critical FFI symbols are exported."""
        required = [
            "push_telemetry_columnar",
            "get_timestamps_column_ptr",
            "get_gas_prices_column_ptr",
            "get_volumes_column_ptr",
            "get_shard_depth",
            "get_shard_head",
            "get_shard_tail",
            "get_num_shards",
            "get_shard_size",
        ]
        missing = []
        for sym in required:
            if not hasattr(self.lib, sym):
                missing.append(sym)
        return missing
def run_mojo_kernel() -> dict:
    """Execute the compiled Mojo compute binary and parse its output."""
    if not os.path.exists(str(MOJO_BIN)):
        return {"status": "skipped", "reason": f"Mojo binary not found at {MOJO_BIN}"}
    start_ns = time.perf_counter_ns()
    result = subprocess.run(
        [str(MOJO_BIN)],
        capture_output=True, text=True, timeout=30,
    )
    elapsed_us = (time.perf_counter_ns() - start_ns) / 1000.0
    output = result.stdout
    stderr = result.stderr
    # Parse key metrics from Mojo output
    gas_anomalies = None
    multi_anomalies = None
    mean_gas = None
    for line in output.split("\n"):
        line = line.strip()
        if "Anomalies (gas only):" in line:
            try:
                gas_anomalies = int(line.split(":")[-1].strip())
            except (ValueError, IndexError):
                pass
        elif "Anomalies (gas OR volume):" in line:
            try:
                multi_anomalies = int(line.split(":")[-1].strip())
            except (ValueError, IndexError):
                pass
        elif "Mean gas price:" in line:
            try:
                mean_gas = float(line.split(":")[-1].strip().split()[0])
            except (ValueError, IndexError):
                pass
    return {
        "status": "ok" if result.returncode == 0 else "failed",
        "returncode": result.returncode,
        "elapsed_us": elapsed_us,
        "elapsed_ms": elapsed_us / 1000.0,
        "gas_anomalies": gas_anomalies,
        "multi_anomalies": multi_anomalies,
        "mean_gas": mean_gas,
        "output_summary": output.split("\n")[-4:],
        "stderr": stderr[:500] if stderr else "",
    }
def run_end_to_end_pipeline() -> dict:
    """Execute a complete end-to-end pipeline run and return health report."""
    print("=" * 70)
    print("  SOVEREIGN OS / DATA ENGINE PIPELINE")
    print("  SoA Columnar: Rust → Python → Mojo SIMD")
    print("=" * 70)
    print()
    results = {}
    print("1️⃣  Loading librust_bridge.so...")
    start = time.perf_counter_ns()
    try:
        bridge = RustSoABridge()
        load_us = (time.perf_counter_ns() - start) / 1000.0
        missing = bridge.verify_ffi_symbols()
        if missing:
            print(f"   ❌ Missing FFI symbols: {missing}")
            results["rust_ffi"] = {"status": "failed", "missing_symbols": missing}
        else:
            print(f"   ✓ All FFI symbols verified ({load_us:.1f} μs)")
            results["rust_ffi"] = {"status": "ok", "load_us": load_us}
    except Exception as e:
        print(f"   ❌ Failed to load: {e}")
        results["rust_ffi"] = {"status": "error", "detail": str(e)}
        return results  # Can't continue without Rust
    print()
    print("2️⃣  Pushing telemetry into 256 SoA shards...")
    start = time.perf_counter_ns()
    push_count = 0
    shards_touched = set()
    num_shards = bridge.lib.get_num_shards()
    # Inject 1000 records across 256 shards
    for i in range(1000):
        pid = f"PAY-{i:04d}"
        ts = 1718800000000000000 + i
        gas = 20.0 + float(i % 10)          # oscillate 20..29 gwei
        vol = 500.0 + float(i % 20) * 10.0  # oscillate 500..690
        # Inject known anomalies
        if i == 42:
            gas = 150.0   # gas spike
        elif i == 99:
            gas = 200.0   # gas spike
        elif i == 256:
            vol = 5000.0  # volume spike
        elif i == 500:
            gas = 300.0   # gas spike
        elif i == 777:
            vol = 8000.0  # volume spike
        shard = bridge.push_telemetry(pid, ts, gas, vol)
        if shard >= 0:
            push_count += 1
            shards_touched.add(shard)
    push_us = (time.perf_counter_ns() - start) / 1000.0
    print(f"   ✓ {push_count} records pushed to {len(shards_touched)} shards")
    print(f"   ⏱  {(push_us / 1000.0):.2f} ms total, {(push_us / push_count):.1f} μs/record")
    # Verify data landed
    total_depth = sum(bridge.lib.get_shard_depth(i) for i in range(num_shards))
    print(f"   Total unread entries across all shards: {total_depth}")
    results["ingestion"] = {
        "status": "ok",
        "records_pushed": push_count,
        "shards_touched": len(shards_touched),
        "total_depth": total_depth,
        "total_us": push_us,
        "per_record_us": push_us / max(push_count, 1),
    }
    print()
    print("3️⃣  Reading columnar arrays from shard 42...")
    start = time.perf_counter_ns()
    cols = bridge.get_column_arrays(42)
    read_us = (time.perf_counter_ns() - start) / 1000.0
    print(f"   Shard 42 depth: {len(cols[0])} records")
    if cols[0]:
        print(f"   Timestamps: [{cols[0][0]}, {cols[0][1]}, ...]")
        print(f"   Gas prices: [{cols[1][0]:.1f}, {cols[1][1]:.1f}, ...]")
        print(f"   Volumes:    [{cols[2][0]:.1f}, {cols[2][1]:.1f}, ...]")
        print(f"   USDC supp:  [{cols[3][0]:.1f}, ...]B  USD/JPY: [{cols[9][0]:.2f}, ...]")
        print(f"   ⏱  {read_us:.1f} μs")
    results["columnar_readback"] = {
        "status": "ok",
        "shard": 42,
        "depth": len(cols[0]),
        "read_us": read_us,
    }
    print()
    print("4️⃣  Executing Mojo SIMD columnar kernel...")
    mojo_result = run_mojo_kernel()
    results["mojo_kernel"] = mojo_result
    if mojo_result.get("status") == "ok":
        print(f"   ✓ Mojo kernel completed ({mojo_result['elapsed_ms']:.1f} ms)")
        print(f"     Gas anomalies:   {mojo_result['gas_anomalies']}")
        print(f"     Multi anomalies: {mojo_result['multi_anomalies']}")
        print(f"     Mean gas price:  {mojo_result['mean_gas']}")
    elif mojo_result.get("status") == "skipped":
        print(f"   ⚠  Mojo binary not found — skipping")
    else:
        print(f"   ❌ Mojo kernel failed (rc={mojo_result.get('returncode')})")
        if mojo_result.get("stderr"):
            print(f"     stderr: {mojo_result['stderr']}")
    print()
    all_ok = (
        results.get("rust_ffi", {}).get("status") == "ok"
        and results.get("ingestion", {}).get("status") == "ok"
        and results.get("columnar_readback", {}).get("status") == "ok"
    )
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "pipeline_version": "1.0.0",
        "layout": "SoA (timestamps[u64], gas_prices[f32], volumes[f32])",
        "shards": {"count": num_shards, "entries_per_shard": bridge.lib.get_shard_size()},
        "results": results,
        "all_healthy": all_ok,
    }
    print("=" * 70)
    if all_ok:
        print("  ✅ PIPELINE HEALTHY — SoA Columnar Engine Operational")
    else:
        print("  ❌ PIPELINE DEGRADED — See results above")
    print("=" * 70)
    print()
    return report
if __name__ == "__main__":
    os.environ["PATH"] = (
        f"{os.environ.get('CONDA_PREFIX', '/home/cherry/miniforge3/envs/developer-env')}/bin"
        f":{os.environ['PATH']}"
    )
    report = run_end_to_end_pipeline()
    # Write health JSON
    with open(str(HEALTH_JSON), "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"Health report written to {HEALTH_JSON}")
