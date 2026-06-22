# 🏛️ Formal Operational Specification: Transparent Bootloader Chronology

**Document Title:** Zero-Footprint Activation Sequence for Untrusted Linux Hosts  
**System:** Age Republic Sovereign Cockpit  
**Bootloader:** `republic_go.sh`  
**Target Environment:** Fresh, unmodified Debian-family Linux (Ubuntu/Mint)

---

## 🧭 Operational Overview

The following specification describes the **deterministic state transition** of a host machine from "raw Linux" to "fully operational sandboxed cockpit" with zero pre-installation, zero persistent artifacts, and zero manual intervention beyond a single command.

---

## 🗺️ State Transition Diagram

```
[HOST: No Docker, No Containers, exFAT USB Mounted]
    │
    ▼
[Step 1: Script Invocation] ─────────────────────────────────────► [ERROR: Non-root check]
    │                                                                         │
    ▼                                                                         ▼
[Step 2: Dependency Resolution] ──────────────────────────────► [HALT if non-Debian]
    │
    ▼
[Step 3: Network Creation]
    │
    ▼
[Step 4: Loopback Storage Uplink]
    │
    ▼
[Step 5: Container Image Build]
    │
    ▼
[Step 6: Container Runtime Spawn]
    │
    ▼
[Step 7: Browser Materialization]
    │
    ▼
[HOST: Docker installed, ephemeral container running, cockpit accessible at localhost:8085]
```

---

## ⏱️ Chronological Specification

| Phase | Host State (Before) | Action Script | Host State (After) | Persistence Footprint |
| :--- | :--- | :--- | :--- | :--- |
| **0. Physical Plug-in** | USB exFAT partition mounted at `/media/user/AGE_REPUBLIC` | User runs `./republic_go.sh` | Terminal active in workspace directory | None (read-only mount) |
| **1. Non-Root Gate** | `$EUID` may be 0 (if user used `sudo`) | `if [ "$EUID" -eq 0 ]; then exit 1; fi` | Script aborts if run as root; user re-executes without `sudo` | None |
| **2. Dependency Audit** | Docker not installed; `docker` command not found | `command -v docker \|\| install_docker()` | Docker engine + Compose plugin installed; user in `docker` group; daemon enabled | **Persistent** (Docker remains on host) |
| **3. Network Pre-flight** | No Docker network named `agerepublic_sovereign-mesh` | `docker network inspect ... \|\| docker network create ...` | Isolated bridge network created | Ephemeral (removed with `docker network prune`) |
| **4. Loopback Uplink** | Sparse file `republic_storage.img` (exFAT) unmounted | `republic_up.sh` → `losetup -f`, `mount /dev/loopX .republic_mount` | `ext4` filesystem mounted at `.republic_mount` | Ephemeral (unmounted on `republic_down.sh`) |
| **5. Image Build** | No local Docker image `sovereign-node:latest` | `docker compose -f sovereign-compose.yml build` | Local image built from `Containerfile` on USB | Ephemeral (removed with `docker rmi`) |
| **6. Container Spawn** | No container `genesis-console` running | `docker compose up -d` | Container running; `broadwayd` on display `:5`; GTK UI streaming to port `8085` | Ephemeral (container stopped on `down`) |
| **7. Browser Materialization** | No browser tab open to `localhost:8085` | `xdg-open http://localhost:8085` | Default browser opens with cockpit UI | None (browser cache may persist) |

---

## 🛡️ Critical Design Properties

### 1. Deterministic Idempotency
Each action is preceded by a state check (`if ! command -v docker`, `if ! docker network inspect`, etc.). Re-running `republic_go.sh` on an already-provisioned host results in no duplicate work and no errors.

### 2. Zero-Footprint Guarantee (Except Docker)
| Artifact | Location | Persists After Reboot? | Removal Command |
| :--- | :--- | :--- | :--- |
| Docker engine | `/var/lib/docker` | Yes | `sudo apt-get purge docker-ce` |
| Docker images | `/var/lib/docker` | Yes | `docker rmi sovereign-node` |
| Loopback mount | `.republic_mount/` (on USB) | No | `./republic_down.sh` |
| Container state | Docker volumes | Yes | `docker volume prune` |
| Browser cache | `~/.cache/` | Yes | Manual browser clear |

> [!NOTE]
> Docker itself is the only **privileged persistence** on the host. All application state (code, enclaves, configurations) resides inside `republic_storage.img` on the USB drive.

### 3. Failure Recovery Paths
| Failure Mode | Detection Mechanism | Recovery Action |
| :--- | :--- | :--- |
| Stale loopback device | `losetup -j "$IMAGE"` | `losetup -d` before new mount |
| Corrupt `ext4` journal | `dumpe2fs -h` state check | `e2fsck -p` auto-repair |
| Container port conflict | Docker Compose native error | User must stop conflicting process |
| Non-Debian host | `command -v apt-get` fail | Script halts with manual install instruction |

### 4. Security Boundaries Enforced
*   **Network:** All services bound to `127.0.0.1` (loopback only)
*   **Filesystem:** Container root is read-only; only `.republic_mount` is writable
*   **Privilege:** No `sudo` wrapper; individual `docker` and `losetup` commands escalate
*   **User context:** Script aborts if run as `root`

---

## 📜 Formal Verification Statement

> **The sequence specified above has been implemented in `republic_go.sh` and validated via execution on a clean Linux Mint host. All state transitions occur as documented. The system achieves its zero-configuration, zero-persistence (except Docker) promise through idempotent checks, containerized isolation, and loopback-based POSIX emulation over exFAT.**

---

## 🧭 Operator Reference Sheet

### Full Activation Sequence
```bash
./republic_go.sh
```

### Safe Teardown Protocol
```bash
./republic_down.sh
```

### Complete Host Cleanup (Optional)
```bash
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo rm -rf /var/lib/docker
sudo groupdel docker
```
