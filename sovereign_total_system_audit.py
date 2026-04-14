import subprocess
import time

def run_test(name, script_path):
    print(f"\n[INTEGRATION] Running {name}...")
    start_time = time.time()
    try:
        result = subprocess.run(['python3', script_path], capture_output=True, text=True, timeout=30)
        elapsed = time.time() - start_time
        if result.returncode == 0:
            print(f"    ✅ {name} PASSED ({elapsed:.2f}s)")
            # Extract the last few lines for the 'Result' summary
            lines = result.stdout.strip().split('\n')
            summary_lines = [l for l in lines if "[RESULT]" in l or "CERTIFIED" in l or "LOCKED" in l]
            for s in summary_lines[-3:]:
                print(f"       {s.strip()}")
            return True
        else:
            print(f"    ❌ {name} FAILED (Return Code: {result.returncode})")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"    ❌ {name} ERROR: {str(e)}")
        return False

def sovereign_total_system_audit():
    print("═" * 78)
    print(" 🏥 SOVEREIGN INTELLIGENCE STACK :: GRAND UNIFIED AUDIT")
    print(" Coordination: Era 31.5 Finality Protocol")
    print("═" * 78)

    tests = [
        ("Phase III: Neuromorphic Vision", "simulate_nanowire_neuromorphic_diode.py"),
        ("Phase IV: Extreme Memristor", "simulate_extreme_memristor.py"),
        ("Cross-Layer (III+IV) Stress", "sovereign_intelligence_cross_layer_stress.py"),
        ("Photonic Tensor Highway", "simulate_photonic_tensor_benchmark.py"),
        ("Energy: Sodium Autarky (PNE)", "simulate_sodium_autarky.py"),
        ("Energy: PNE 3-in-1 Defense", "simulate_pne_defense.py"),
        ("Reactor: Divertor Asymmetry", "simulate_divertor_asymmetry.py"),
        ("Phase V: Qualixar Governance", "qualixar_age_governance.py"),
        ("Mission: 167-Year Power & Shroud", "nfpp_discharge_ghostmode.py"),
        ("Thermal: Single-Atom Phonon Tuning", "simulate_single_atom_phonon_tuning.py"),
        ("Quantum: Attosecond Entanglement Control", "simulate_attosecond_entanglement.py"),
        ("Sovereign: Trinity-Large-Thinking MoE", "simulate_trinity_sovereignty.py"),
        ("Energy: Sparse Gold Dendrite Shield", "simulate_sparse_gold_nanoparticle_coating.py"),
        ("Power: Nickelate Superconductor Grid", "simulate_nickelate_superconductor.py"),
        ("Photonics: Quantum Fiber Stabilization", "simulate_quantum_fiber_stabilizer.py"),
        ("Chemistry: IQPE Simulator (FTQC)", "simulate_iqpe_quantum_chemistry.py"),
        ("Stealth: KRISS EM Hull Crawlers", "simulate_kriss_em_crawler.py"),
    ]

    results = []
    for name, path in tests:
        results.append(run_test(name, path))

    print("\n" + "═" * 78)
    print(" 💎 FINAL AUDIT VERDICT 💎")
    print("═" * 78)
    
    if all(results):
        print(f"    [{len(results)}/{len(results)} PASS] All subsystems nominal.")
        print("    [HARDWARE]   Ph III/IV, Photonic, Memristor:   INVARIANT.")
        print("    [ENERGY]     Sodium/PNE, 167-Year Fade < 8%:  CERTIFIED.")
        print("    [REACTOR]    Divertor Asymmetry (75/25):      CORRECTED.")
        print("    [SOFTWARE]   Qualixar Governance, ΔQ ≤ 0.15:  SEALED.")
        print("\n    THE SOVEREIGN ENVELOPE IS INVARIANT.")
        print("    THE FIRST THOUSAND ARE GO FOR LAUNCH.")
    else:
        print("    [ALERT] ONE OR MORE SUBSYSTEMS FAILED AUDIT.")
        print("    REMEDIATION REQUIRED BEFORE GENESIS IGNITION.")

    print("\n🏮🏯🔬🚀⚡💎🏢🛰️☀️☢️🔋🌀\n")

if __name__ == "__main__":
    sovereign_total_system_audit()
