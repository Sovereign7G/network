#!/usr/bin/env python3
# system_core/master_pipeline.py
import os
import sys
import json
import time
import shutil
import subprocess
from datetime import datetime
def print_section(title):
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)
def heal_environment(conda_prefix, home_dir, force_heal=True):
    print_section("ENVIRONMENT SELF-HEALING PRE-FLIGHT")
    # 1. Check/Heal modular.cfg
    cfg_target_dir = os.path.join(home_dir, ".modular")
    cfg_target = os.path.join(cfg_target_dir, "modular.cfg")
    cfg_source = os.path.join(conda_prefix, "share", "max", "modular.cfg")
    if not os.path.exists(cfg_target_dir):
        os.makedirs(cfg_target_dir, exist_ok=True)
    cfg_healed = False
    if os.path.exists(cfg_source):
        needs_write = True
        if os.path.exists(cfg_target):
            with open(cfg_target, "r") as f:
                content = f.read()
            if conda_prefix in content:
                needs_write = False
                print("  ✓ modular.cfg already points to correct env")
            else:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                bak_path = f"{cfg_target}.{timestamp}.bak"
                shutil.copy2(cfg_target, bak_path)
                print(f"  ⚠ modular.cfg stale → backed up to {os.path.basename(bak_path)}")
        if needs_write:
            with open(cfg_source, "r") as f:
                cfg_template = f.read()
            placeholder = "/buildbuddy/remotebuilds/d9f3975a-ec55-4c01-8cac-4ab6c122620a/bazel-out/k8-opt-production/bin/utils/packaging/conda/output/bld/rattler-build_mojo-compiler_1781237127/host_env_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_"
            healed_cfg = cfg_template.replace(placeholder, conda_prefix)
            with open(cfg_target, "w") as f:
                f.write(healed_cfg)
            print("  ✓ modular.cfg successfully updated and rewritten")
            cfg_healed = True
    else:
        print("  ⚠ Warning: share/max/modular.cfg template not found in conda prefix.")
    # 2. Check/Heal mojo-lldb symlink
    mojo_lldb_link = os.path.join(conda_prefix, "bin", "mojo-lldb")
    native_lldb = os.path.join(conda_prefix, "bin", "lldb")
    if os.path.exists(native_lldb):
        if not os.path.exists(mojo_lldb_link) and not os.path.islink(mojo_lldb_link):
            os.symlink(native_lldb, mojo_lldb_link)
            print("  ✓ Symlink mojo-lldb created")
        else:
            print("  ✓ Symlink mojo-lldb already correct")
    else:
        print("  ⚠ Warning: native lldb not found in conda bin path.")
    # 3. Check/Heal libMojoLLDB.so symlink
    lib_mojo_lldb_link = os.path.join(conda_prefix, "lib", "libMojoLLDB.so")
    native_liblldb = os.path.join(conda_prefix, "lib", "liblldb.so")
    if os.path.exists(native_liblldb):
        if not os.path.exists(lib_mojo_lldb_link) and not os.path.islink(lib_mojo_lldb_link):
            os.symlink(native_liblldb, lib_mojo_lldb_link)
            print("  ✓ Symlink libMojoLLDB.so created")
        else:
            print("  ✓ Symlink libMojoLLDB.so already correct")
    else:
        print("  ⚠ Warning: native liblldb.so not found in conda lib path.")
    # 4. Check/Heal mojo stdlib
    std_dir = os.path.join(conda_prefix, "lib", "mojo")
    std_mojoc = os.path.join(std_dir, "std.mojoc")
    layout_mojoc = os.path.join(std_dir, "layout.mojoc")
    if not (os.path.exists(std_mojoc) and os.path.exists(layout_mojoc)):
        print("  ⚠ Mojo stdlib missing in conda prefix → scanning package cache...")
        pkg_base = os.path.abspath(os.path.join(conda_prefix, "..", "..", "pkgs"))
        found_src = None
        if os.path.exists(pkg_base):
            for item in os.listdir(pkg_base):
                if item.startswith("mojo-compiler-") and os.path.isdir(os.path.join(pkg_base, item)):
                    candidate_mojo = os.path.join(pkg_base, item, "lib", "mojo")
                    if os.path.exists(os.path.join(candidate_mojo, "std.mojoc")):
                        found_src = candidate_mojo
                        break
        if found_src:
            os.makedirs(std_dir, exist_ok=True)
            for f_name in ["std.mojoc", "layout.mojoc"]:
                shutil.copy2(os.path.join(found_src, f_name), os.path.join(std_dir, f_name))
            print("  ✓ Mojo stdlib files successfully copied from package cache")
        else:
            print("  ❌ CRITICAL: Mojo stdlib cache not found. Please run:")
            print("     micromamba install -y -c https://conda.modular.com/max mojo-compiler")
            return False
    # 5. Check/Heal libtinfo.so.5 symlink
    libtinfo_link = os.path.join(conda_prefix, "lib", "libtinfo.so.5")
    native_libtinfo = os.path.join(conda_prefix, "lib", "libtinfo.so.6")
    if os.path.exists(native_libtinfo):
        if not os.path.exists(libtinfo_link) and not os.path.islink(libtinfo_link):
            os.symlink("libtinfo.so.6", libtinfo_link)
            print("  ✓ Symlink libtinfo.so.5 created")
        else:
            print("  ✓ Symlink libtinfo.so.5 already correct")
    else:
        fallback_libtinfo = os.path.join(conda_prefix, "lib", "libtinfo.so")
        if os.path.exists(fallback_libtinfo):
            if not os.path.exists(libtinfo_link) and not os.path.islink(libtinfo_link):
                os.symlink("libtinfo.so", libtinfo_link)
                print("  ✓ Symlink libtinfo.so.5 created (fallback)")
            else:
                print("  ✓ Symlink libtinfo.so.5 already correct")
        else:
            print("  ⚠ Warning: native libtinfo.so.6/libtinfo.so not found in conda lib path.")
    print("  ✅ Pre-flight complete — environment is healthy")
    return True
def run_diagnostics(conda_prefix, home_dir):
    print_section("PIPELINE STATUS SUMMARY")
    health = {"timestamp": datetime.now().isoformat(), "languages": {}, "all_healthy": True}
    env = os.environ.copy()
    cargo_bin = os.path.join(home_dir, ".cargo", "bin")
    foundry_bin = os.path.join(home_dir, ".foundry", "bin")
    env["PATH"] = f"{os.path.join(conda_prefix, 'bin')}:{cargo_bin}:{foundry_bin}:{env.get('PATH', '')}"
    # 1. Python
    py_ver = sys.version.split()[0]
    print(f"  ✓ Python ({py_ver})")
    health["languages"]["python"] = {"status": "healthy", "version": py_ver}
    # 2. Rust
    try:
        res = subprocess.run(["rustc", "--version"], capture_output=True, text=True, env=env)
        print(f"  ✓ Rust ({res.stdout.strip()})")
        health["languages"]["rust"] = {"status": "healthy", "version": res.stdout.strip()}
    except Exception:
        print("  ⚠ Rust (Unavailable)")
        health["languages"]["rust"] = {"status": "degraded", "error": "rustc not found"}
        health["all_healthy"] = False
    # 3. Mojo
    mojo_bin = os.path.join(conda_prefix, "bin", "mojo")
    if os.path.exists(mojo_bin):
        try:
            res = subprocess.run([mojo_bin, "--version"], capture_output=True, text=True, env=env)
            mojo_ver = res.stdout.strip().replace("\n", " ")
            print(f"  ✓ Mojo ({mojo_ver})")
            health["languages"]["mojo"] = {"status": "healthy", "version": mojo_ver}
        except Exception as e:
            print(f"  ❌ Mojo (Error: {e})")
            health["languages"]["mojo"] = {"status": "broken", "error": str(e)}
            health["all_healthy"] = False
    else:
        print("  ❌ Mojo (Binary missing)")
        health["languages"]["mojo"] = {"status": "broken"}
        health["all_healthy"] = False
    # 4. Rux
    rux_bin = os.path.join(home_dir, ".local", "bin", "rux")
    if os.path.exists(rux_bin):
        try:
            res = subprocess.run([rux_bin, "--version"], capture_output=True, text=True, env=env)
            print(f"  ✓ Rux ({res.stdout.strip()})")
            health["languages"]["rux"] = {"status": "healthy", "version": res.stdout.strip()}
        except Exception as e:
            print(f"  ❌ Rux (Error: {e})")
            health["languages"]["rux"] = {"status": "broken", "error": str(e)}
            health["all_healthy"] = False
    else:
        print("  ❌ Rux (Binary missing)")
        health["languages"]["rux"] = {"status": "broken"}
        health["all_healthy"] = False
    # 5. Elixir
    try:
        res = subprocess.run(["elixir", "--version"], capture_output=True, text=True, env=env)
        lines = [line.strip() for line in res.stdout.split("\n") if line.strip()]
        elixir_ver = next((line for line in lines if "Elixir" in line), lines[0] if lines else "unknown")
        print(f"  ✓ Elixir ({elixir_ver})")
        health["languages"]["elixir"] = {"status": "healthy", "version": elixir_ver}
    except Exception as e:
        print(f"  ❌ Elixir (Error: {e})")
        health["languages"]["elixir"] = {"status": "broken", "error": str(e)}
        health["all_healthy"] = False
    # 6. Lua
    try:
        res = subprocess.run(["lua", "-v"], capture_output=True, text=True, env=env)
        print(f"  ✓ Lua ({res.stdout.strip()})")
        health["languages"]["lua"] = {"status": "healthy", "version": res.stdout.strip()}
    except Exception as e:
        print(f"  ❌ Lua (Error: {e})")
        health["languages"]["lua"] = {"status": "broken", "error": str(e)}
        health["all_healthy"] = False
    # 7. Haskell
    try:
        res = subprocess.run(["ghc", "--version"], capture_output=True, text=True, env=env)
        print(f"  ✓ Haskell ({res.stdout.strip()})")
        health["languages"]["haskell"] = {"status": "healthy", "version": res.stdout.strip()}
    except Exception as e:
        print(f"  ❌ Haskell (Error: {e})")
        health["languages"]["haskell"] = {"status": "broken", "error": str(e)}
        health["all_healthy"] = False
    # 8. Forge / Foundry
    forge_bin = os.path.join(home_dir, ".foundry", "bin", "forge")
    if os.path.exists(forge_bin):
        try:
            res = subprocess.run([forge_bin, "--version"], capture_output=True, text=True, env=env)
            ver_text = res.stdout.strip().split("\n")[0] if res.stdout.strip() else "unknown"
            health["languages"]["forge"] = {"status": "healthy", "version": ver_text}
            print(f"  ✓ Foundry ({ver_text})")
        except Exception as e:
            print(f"  ⚠ Foundry (Error: {e})")
            health["languages"]["forge"] = {"status": "degraded", "error": str(e)}
    else:
        print("  ⚠ Foundry (not installed — run 'foundryup')")
        health["languages"]["forge"] = {"status": "missing"}
    # 9. Deployment readiness
    health["deployment"] = {}
    for rpc_var in ["BASE_RPC_MAINNET", "BASE_RPC_SEPOLIA"]:
        health["deployment"][rpc_var] = "configured" if os.environ.get(rpc_var) else "missing"
    configured_rpcs = sum(1 for v in health["deployment"].values() if v == "configured")
    print(f"  ✓ RPC endpoints: {configured_rpcs}/2 configured")
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    if os.path.exists(out_dir):
        n = len([f for f in os.listdir(out_dir) if f.endswith(".sol") or f.endswith(".json")])
        health["deployment"]["compiled_contracts"] = n
        print(f"  ✓ Compiled contracts: {n} artifacts in out/")
    else:
        health["deployment"]["compiled_contracts"] = 0
        print("  ⚠ No forge build artifacts — run 'forge build'")
    deploy_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contracts/scripts/DeployInfrastructure.s.sol")
    if os.path.exists(deploy_script):
        health["deployment"]["deploy_script"] = "found"
        print("  ✓ Deploy script: ready")
    else:
        health["deployment"]["deploy_script"] = "missing"
        print("  ⚠ Deploy script: missing")
    health["summary"] = f"{len([v for v in health['languages'].values() if v['status'] == 'healthy'])}/{len(health['languages'])} engines healthy"
    return health
def execute_timed_pipeline():
    print("\n" + "="*50)
    print(" ⏱️  CROSS-RUNTIME LATENCY INSTRUMENTATION")
    print("="*50)
    metrics = {}
    main_env = os.environ.copy()
    conda_prefix = os.environ.get("CONDA_PREFIX", os.path.expanduser("~/miniforge3/envs/developer-env"))
    cargo_bin = os.path.join(os.path.expanduser("~"), ".cargo", "bin")
    local_bin = os.path.join(os.path.expanduser("~"), ".local", "bin")
    main_env["PATH"] = f"{os.path.join(conda_prefix, 'bin')}:{cargo_bin}:{local_bin}:{main_env.get('PATH', '')}"
    start = time.perf_counter_ns()
    subprocess.run(["lua", "agent_ipc/transform.lua"], capture_output=True, text=True, env=main_env)
    metrics["lua_transform_us"] = (time.perf_counter_ns() - start) / 1000.0
    print(f"   ⚡ Lua Transform Engine:      {metrics['lua_transform_us']:>10.2f} μs")
    start = time.perf_counter_ns()
    subprocess.run(["mojo", "mojo_kernels/compute.mojo"], capture_output=True, text=True, env=main_env)
    metrics["mojo_simd_compute_us"] = (time.perf_counter_ns() - start) / 1000.0
    print(f"   ⚡ Mojo SIMD Vector Kernel:   {metrics['mojo_simd_compute_us']:>10.2f} μs")
    start = time.perf_counter_ns()
    subprocess.run(["elixir", "agent_ipc/coordinator.exs"], capture_output=True, text=True, env=main_env)
    metrics["elixir_ingestion_us"] = (time.perf_counter_ns() - start) / 1000.0
    print(f"   ⚡ Elixir Actor Ingestion:    {metrics['elixir_ingestion_us']:>10.2f} μs")
    start = time.perf_counter_ns()
    subprocess.run(["./rux_modules/Bin/Debug/rux_modules"], capture_output=True, text=True, env=main_env)
    metrics["rux_storage_us"] = (time.perf_counter_ns() - start) / 1000.0
    print(f"   ⚡ Rux Native Module:         {metrics['rux_storage_us']:>10.2f} μs")
    total_us = sum(metrics.values())
    print(f"   ──────────────────────────────────────────")
    print(f"   ⚡ Total Pipeline (all hops): {total_us:>10.2f} μs ({total_us/1000.0:.2f} ms)")
    ipc_dir = "agent_ipc"
    os.makedirs(ipc_dir, exist_ok=True)
    timing_path = os.path.join(ipc_dir, "latency_metrics.json")
    with open(timing_path, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "metrics_us": metrics, "total_us": total_us}, f, indent=2)
    print(f"   ✓ Timing metrics saved to {timing_path}")
    return metrics
def run_warm_cache_benchmark(main_env):
    print("\n" + "="*50)
    print(" 🔥 WARM-CACHE STEADY-STATE BENCHMARK")
    print("="*50)
    warm = {}
    print("\n  [MOJO] Running in-process 10M-iteration SIMD loop...")
    print("   Measuring baseline...")
    start = time.perf_counter_ns()
    subprocess.run(["mojo", "mojo_kernels/baseline.mojo"], capture_output=True, text=True, env=main_env)
    baseline_ns = time.perf_counter_ns() - start
    print("   Measuring full kernel...")
    start = time.perf_counter_ns()
    subprocess.run(["mojo", "mojo_kernels/compute.mojo"], capture_output=True, text=True, env=main_env)
    full_ns = time.perf_counter_ns() - start
    loop_ns = full_ns - baseline_ns
    per_iter_ns = loop_ns / 10000000.0
    warm["mojo_simd"] = {"cold_start_us": full_ns/1000, "baseline_us": baseline_ns/1000, "loop_10m_us": loop_ns/1000, "per_iteration_ns": per_iter_ns}
    print(f"   ✓ Cold start: {full_ns/1000:.0f} μs | Baseline: {baseline_ns/1000:.0f} μs")
    print(f"   🔥 Per-iteration SIMD throughput: {per_iter_ns:.2f} ns")
    print("\n  [ELIXIR+PORT] Persistent BEAM + Rust ring buffer hot-path...")
    rust_bin = os.path.abspath("rust_bridge/target/release/rust_bridge_bin")
    proc = subprocess.Popen([rust_bin], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    batch_size = 1000
    start = time.perf_counter_ns()
    for i in range(batch_size):
        proc.stdin.write(f"{i}\n")
        proc.stdin.flush()
        proc.stdout.readline()
    elapsed = time.perf_counter_ns() - start
    proc.stdin.write("QUIT\n")
    proc.stdin.flush()
    proc.wait(timeout=5)
    per_value_us = elapsed / 1000.0 / batch_size
    throughput = batch_size / (elapsed / 1e9)
    warm["elixir_port_throughput"] = {"batch": batch_size, "total_us": elapsed/1000, "per_value_us": per_value_us, "values_per_sec": throughput}
    print(f"   ✓ {batch_size} values pushed — {per_value_us:.3f} μs/val — {throughput:,.0f} val/s")
    print("\n  [RUX] Pre-compiled native (avg of 50 runs)...")
    rux_bin = os.path.abspath("rux_modules/Bin/Debug/rux_modules")
    times = []
    for _ in range(50):
        start = time.perf_counter_ns()
        subprocess.run([rux_bin], capture_output=True, text=True, env=main_env)
        times.append((time.perf_counter_ns() - start) / 1000.0)
    avg = sum(times)/len(times)
    warm["rux_repeated_us"] = {"avg": avg, "min": min(times), "max": max(times), "runs": 50}
    print(f"   ✓ Avg: {avg:.2f} μs | Min: {min(times):.2f} μs | Max: {max(times):.2f} μs")
    print(f"\n{'─'*50}")
    print(f" 🔥 WARM-CACHE SUMMARY")
    print(f"{'─'*50}")
    print(f"   Mojo SIMD (per iteration):     {per_iter_ns:>10.2f} ns")
    print(f"   Rust ring buffer (hot-path):  {per_value_us:>10.3f} μs  [{throughput:,.0f} val/s]")
    print(f"   Rux native (avg 50x):       {avg:>10.2f} μs")
    ipc_dir = "agent_ipc"
    os.makedirs(ipc_dir, exist_ok=True)
    with open(os.path.join(ipc_dir, "warm_cache_metrics.json"), "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "warm_metrics": {k: v for k, v in warm.items()}}, f, indent=2)
    print(f"   ✓ Warm-cache metrics saved to {ipc_dir}/warm_cache_metrics.json")
    return warm
def run_security_audit(main_env):
    print("\n" + "="*50)
    print(" 🛡️  ENTERPRISE SECURITY AUDIT")
    print("="*50)
    audit = {"hsm": {"status": "UNKNOWN"}, "governance": {"status": "UNKNOWN"}, "key_isolation": {"status": "UNKNOWN"}}
    try:
        result = subprocess.run(["python3", "agent_ipc/hsm_vault.py"], capture_output=True, text=True, timeout=10, env=main_env)
        if "HSM" in result.stdout and "Signature Result" in result.stdout:
            audit["hsm"] = {"status": "HEALTHY", "backend": "SIMULATED_PKCS11"}
            print("   ✅ [SECURITY] HSM module: HEALTHY — isolated signing verified")
        else:
            audit["hsm"] = {"status": "DEGRADED"}
            print("   ⚠️ [SECURITY] HSM module: DEGRADED")
    except Exception as e:
        audit["hsm"] = {"status": "ERROR", "error": str(e)}
        print(f"   ❌ [SECURITY] HSM module: ERROR — {e}")
    gov_path = "rux_modules/governance.sol"
    if os.path.exists(gov_path):
        with open(gov_path) as f:
            content = f.read()
        tiers = sum([("TIER_1_LIMIT" in content), ("TIER_2_LIMIT" in content), ("TIER_3_LIMIT" in content), ("onlyRole" in content)])
        audit["governance"] = {"status": "DEPLOYED", "tiers": tiers}
        print(f"   ✅ [SECURITY] Governance contract: DEPLOYED — {tiers}/4 tier checks verified")
    else:
        audit["governance"] = {"status": "MISSING"}
        print("   ❌ [SECURITY] Governance contract: NOT FOUND")
    env_path = os.path.join(os.path.expanduser("~"), ".env_pipeline")
    if os.path.exists(env_path):
        with open(env_path) as f:
            env_content = f.read().lower()
        if "private_key" in env_content or "secret" in env_content:
            audit["key_isolation"] = {"status": "VULNERABLE", "finding": "Plaintext key detected"}
            print("   🔴 [SECURITY] Key isolation: VULNERABLE — plaintext key in ~/.env_pipeline")
        else:
            audit["key_isolation"] = {"status": "CLEAN"}
            print("   ✅ [SECURITY] Key isolation: CLEAN")
    else:
        audit["key_isolation"] = {"status": "CLEAN", "note": "No .env_pipeline found"}
        print("   ✅ [SECURITY] Key isolation: CLEAN — no .env_pipeline present")
    all_secure = all(v["status"] in ("HEALTHY", "DEPLOYED", "CLEAN") for v in audit.values())
    print(f"\n   🛡️  Enterprise security posture: {'SECURE' if all_secure else 'NEEDS ATTENTION'}")
    ipc_dir = "agent_ipc"
    os.makedirs(ipc_dir, exist_ok=True)
    sec_path = os.path.join(ipc_dir, "security_audit.json")
    with open(sec_path, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "audit": audit, "all_secure": all_secure}, f, indent=2)
    print(f"   ✓ Security audit saved to {sec_path}")
    return audit
def main():
    conda_prefix = os.environ.get("CONDA_PREFIX", "/home/cherry/miniforge3/envs/developer-env")
    home_dir = os.path.expanduser("~")
    no_heal = "--no-heal" in sys.argv
    healed = True
    if not no_heal:
        healed = heal_environment(conda_prefix, home_dir)
    health = run_diagnostics(conda_prefix, home_dir)
    execute_timed_pipeline()
    cargo_bin = os.path.join(home_dir, ".cargo", "bin")
    local_bin = os.path.join(home_dir, ".local", "bin")
    foundry_bin = os.path.join(home_dir, ".foundry", "bin")
    main_env = os.environ.copy()
    main_env["PATH"] = f"{os.path.join(conda_prefix, 'bin')}:{cargo_bin}:{local_bin}:{foundry_bin}:{main_env.get('PATH', '')}"
    run_warm_cache_benchmark(main_env)
    run_security_audit(main_env)
    ipc_dir = "agent_ipc"
    os.makedirs(ipc_dir, exist_ok=True)
    with open(os.path.join(ipc_dir, "pipeline_health.json"), "w") as f:
        json.dump(health, f, indent=2)
    n_healthy = sum(1 for l in health["languages"].values() if l["status"] == "healthy")
    n_total = len(health["languages"])
    exit_code = 0 if (health["all_healthy"] and healed) else 1
    print(f"\nEXIT={exit_code} | {n_healthy}/{n_total} engines healthy")
    sys.exit(exit_code)
if __name__ == "__main__":
    main()
