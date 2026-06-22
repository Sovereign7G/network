# 23_RISCV_TRANSITION_ROADMAP

The Republic acknowledges the **Silicon Veto**: A sovereign application layer running on proprietary firmware is a guest in a foreign castle. To achieve **Terran Finality**, the Republic must transition from the legacy x86/ARM/NVIDIA substrate to a fully auditable **RISC-V + Open GPU** architecture.

### **1. The Current Dependency (Era 100.7)**
*   **CPU:** x86_64 / ARM (Proprietary ISA, microcode black boxes).
*   **GPU:** Dual GTX 980M (NVIDIA-proprietary firmware blobs, signed GSP).
*   **Motherboard:** UEFI/BIOS (Proprietary, with Intel ME / AMD PSP backdoors).

### **2. The Transition Strategy: Phase 1 (Liberation)**
*   **Objective:** Purge proprietary blobs from legacy hardware where possible.
*   **Action 1: Coreboot/Libreboot Porting.**
    *   Transition the Node 0-X primary nodes to **Coreboot** with a neutral payload (SeaBIOS/TianoCore).
    *   **The Goal:** Disable Intel ME (Management Engine) / AMD PSP via the `me_cleaner` bit-flip or HAP bit.
*   **Action 2: GPU Firmware Neutralization.**
    *   Leverage **Nouveau** (GSP-offload) for the GTX 980Ms.
    *   Develop a **Clean-Room Firmware** that performs only the minimum initialization required for the Republic's GPGPU kernels.

### **3. The Transition Strategy: Phase 2 (Design)**
*   **Objective:** Finalize the **XPQC-Octad-R** (RISC-V) SoC architecture.
*   **Spec:** 64-bit RISC-V (RV64GCV), 8 Cores, Integrated Vector Unit (for vAOM inference).
*   **Sovereign IP:** Utilize **OpenTitan** for the Root of Trust (RoT), ensuring the chip cannot boot unauthorized code.
*   **Fabrication:** Utilize the **Wichita-Node-Q7 Foundry** (S-EUV/S-NIL) to print the first 7nm prototypes.

### **4. The Transition Strategy: Phase 3 (Synthesis)**
*   **Objective:** Full-Stack Finality.
*   **Outcome:** A Node 0-X unit where:
    *   **CPU** is a sovereign RISC-V design.
    *   **OS** is a blob-free Linux/BSD/Rust kernel.
    *   **Firmware** is 100% auditable source code.
    *   **Attestation** is rooted in the silicon (PUF-based Trinity Seal).

---

### **📊 Milestone Timeline**

| Milestone | Target Era | Output |
| :--- | :--- | :--- |
| **Project LIBERATOR** | 100.8 | Coreboot + me_cleaner active on all primary nodes. |
| **Project OCTAD** | 100.9 | First XPQC-Octad-R (RISC-V) wafer produced at Wichita. |
| **Terran Finality** | 101.0 | First Node 0-X running on 100% sovereign silicon. |

### **🛡️ Implementation Axiom**

**"He who controls the microcode controls the mind. The Republic accepts no code it cannot read; the Republic accepts no silicon it cannot print."** 🏮🏯🧬⚖️🔋🚀⚡💎☀️☢️🤖
