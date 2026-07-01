#!/usr/bin/env python3
"""ICP Canister Agent — create, deploy, upgrade canisters via icp-cli. One command, no NNS dapp."""

import subprocess, sys, os, json, time

PRINCIPAL = "l7qm5-nlxsp-3y4hu-iwzb2-y24rc-4qbvt-ageb2-nmh6d-n5gwa-offrj-fqe"
CYCLE_MIN = 600_000_000_000  # 600B cycles — includes 500B minimum + fee buffer

def cmd(c, check=True, timeout=60):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        stderr = r.stderr.strip()[:200]
        print(f"❌ {c.split()[0]}: {stderr}", file=sys.stderr)
        sys.exit(1)
    return r

def ensure_icp_identity():
    """Import dfx deployer identity into icp-cli if not already there."""
    r = subprocess.run("icp identity list", shell=True, capture_output=True, text=True, timeout=10)
    if "deployer" not in r.stdout:
        print("Importing deployer identity into icp-cli...")
        cmd("dfx identity export deployer > /tmp/deployer.pem")
        cmd("icp identity import deployer --from-pem /tmp/deployer.pem")
    cmd("icp identity default deployer")

def ensure_cycles(needed=CYCLE_MIN):
    """Check cycles balance, convert ICP if needed."""
    r = cmd("icp cycles balance -e ic", timeout=15)
    bal_str = r.stdout.strip()
    # Parse "Balance: X cycles" or "X TC (trillion cycles)"
    bal = 0
    for part in bal_str.replace(",", "").split():
        part = part.replace("_", "")
        if part.isdigit():
            bal = int(part)
            break
    if bal < needed:
        print(f"Need {needed:,} cycles, have {bal:,}. Converting ICP...")
        cmd("dfx cycles convert --amount 0.5 --network ic", timeout=60)
        # Verify
        r = cmd("icp cycles balance -e ic", timeout=15)
        print(f"✅ Balance: {r.stdout.strip()}")
    else:
        print(f"✅ Sufficient cycles: {bal:,}")

def create(name, controller=PRINCIPAL, cycles=CYCLE_MIN):
    """Create a canister on ICP mainnet."""
    print(f"Creating canister '{name}'...")
    r = cmd(f"icp canister create {name} -e ic --controller {controller} --cycles {cycles}", timeout=60)
    # Extract canister ID from output
    cid = None
    for line in r.stdout.split("\n"):
        if "with ID" in line:
            cid = line.split("with ID ")[-1].strip()
            break
    if cid:
        print(f"✅ Canister '{name}' created: {cid}")
        return cid
    print(f"✅ Created (ID in output above)")
    return None

def upgrade(name, wasm_path, cid=None):
    """Upgrade an existing canister with new WASM."""
    if cid:
        print(f"Upgrading {cid} with {wasm_path}...")
        r = cmd(f"dfx canister --network ic install {cid} --wasm {wasm_path} --mode upgrade", timeout=120)
    else:
        print(f"Upgrading '{name}'...")
        r = cmd(f"dfx canister --network ic install {name} --wasm {wasm_path} --mode upgrade", timeout=120)
    print(f"✅ Upgrade complete")
    return r

def status(name_or_id):
    """Get canister status."""
    r = cmd(f"dfx canister --network ic status {name_or_id}", timeout=15)
    for line in r.stdout.split("\n"):
        line = line.strip()
        if "Balance:" in line or "Status:" in line or "Memory:" in line:
            print(f"  {line}")
    return r.stdout

def delete(name_or_id):
    """Delete a canister (refunds cycles)."""
    print(f"Deleting {name_or_id}...")
    cmd(f"dfx canister --network ic stop {name_or_id}", timeout=30)
    cmd(f"dfx canister --network ic delete {name_or_id}", timeout=30)
    print(f"✅ Deleted")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="ICP Canister Agent — create, deploy, upgrade")
    p.add_argument("action", choices=["create", "upgrade", "status", "delete", "setup"])
    p.add_argument("name", nargs="?", help="Canister name or ID")
    p.add_argument("--wasm", help="Path to .wasm file (for upgrade)")
    p.add_argument("--controller", default=PRINCIPAL, help="Controller principal")
    p.add_argument("--cycles", type=int, default=CYCLE_MIN, help="Cycles for creation")
    args = p.parse_args()

    ensure_icp_identity()

    if args.action == "setup":
        ensure_cycles()
        print("✅ Setup complete — icp-cli ready")
    elif args.action == "create":
        if not args.name:
            print("❌ Need canister name"); sys.exit(1)
        ensure_cycles(args.cycles)
        create(args.name, args.controller, args.cycles)
    elif args.action == "upgrade":
        if not args.name or not args.wasm:
            print("❌ Need canister name and --wasm path"); sys.exit(1)
        upgrade(args.name, args.wasm)
    elif args.action == "status":
        if not args.name:
            print("❌ Need canister name or ID"); sys.exit(1)
        status(args.name)
    elif args.action == "delete":
        if not args.name:
            print("❌ Need canister name or ID"); sys.exit(1)
        delete(args.name)
