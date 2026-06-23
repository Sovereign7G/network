#!/usr/bin/env python3
"""
08_HARDWARE/CAD/fabrika_api.py
Sovereign FABRIKA Engine — Dual-Token Hardware Synthesis API.
Re-exports all classes and functions from submodules.
"""

from fabrika_core import (
    TernaryState, FuelType, Material, EngineSpec, NozzleGeometry,
    HilbertSpec, HilbertGeometry, VerificationResult, FABRIKAEngine,
    HilbertSystem, PhotonicSystem, AuditResult, FoundryAudit,
    INCONEL_718, TITANIUM_64, SCANDIUM_AL, LNOI,
)
from fabrika_audits import (
    AetherMeshLinkAudit, OceanInfrastructureAudit,
    AntimatterContainmentAudit, ContinentalGridAudit,
)
from fabrika_synthesis import GeneralComponentAudit, FullFleetSynthesis
from fabrika_gcode import generate_tfln_pocket_gcode
from fabrika_cnc import CNCSubstrate

__all__ = [
    "TernaryState", "FuelType", "Material", "EngineSpec", "NozzleGeometry",
    "HilbertSpec", "HilbertGeometry", "VerificationResult", "FABRIKAEngine",
    "HilbertSystem", "PhotonicSystem", "AuditResult", "FoundryAudit",
    "INCONEL_718", "TITANIUM_64", "SCANDIUM_AL", "LNOI",
    "AetherMeshLinkAudit", "OceanInfrastructureAudit",
    "AntimatterContainmentAudit", "ContinentalGridAudit",
    "GeneralComponentAudit", "FullFleetSynthesis",
    "generate_tfln_pocket_gcode", "CNCSubstrate",
]

if __name__ == "__main__":
    print("=" * 60)
    print("  SOVEREIGN FABRIKA ENGINE — Dual-Token Settlement")
    print("=" * 60)

    # Example 1: Standard Settlement
    sat = FABRIKAEngine.from_spec(name="Sovereign-Nano-20kN", thrust_kn=20.0)
    if sat.verify():
        sat.anchor_to_icp()
        sat.export_print_instructions()

    # Example 2: Dual-Token Failure ($HIL Exhaustion)
    print("\n─── EXAMPLE: Dual-Token Settlement Failure ($HIL) ───")
    heavy = FABRIKAEngine.from_spec(name="Storm-Breaker-Heavy", thrust_kn=2500.0, wall_thickness_mm=2.0)
    if heavy.verify():
        heavy.anchor_to_icp()

    # Example 3: Hilbert Test
    hspec = HilbertSpec(name="Hilbert-Storm-Cooler", order=6)
    hhx = HilbertSystem(hspec)
    if hhx.verify():
        hhx.voxelize()
        hhx.export_print_profile()

    # Example 7: FINAL SYNTHESIS TEST (Path A)
    print("\n" + "─" * 40)
    print("FINAL MISSION SYNTHESIS: Hilbert-Storm-Cooler-TRL4")
    trl4_spec = HilbertSpec(name="Hilbert-Storm-Cooler-TRL4", thermal_load_mw=5.0, order=4, channel_gap_mm=1.2)
    trl4_hx = HilbertSystem(trl4_spec)
    if trl4_hx.verify():
        print("\n⚓ SOVEREIGN SETTLEMENT (Storm-Breaker)")
        print("🔥 MERIT BURN: -500")
        print("💰 HIL PAYMENT: -2,500 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")
        trl4_hx.export_print_profile()
        print("\n🖨️ SNC-Q7.2 FOUNDRY: Job submitted for LPBF Synthesis.")

    # Example 8: TFLN Photonic Shard Synthesis
    print("\n" + "─" * 40)
    print("PHOTONIC MISSION SYNTHESIS: TFLN-Switch-Shard-V1")
    tfln_pic = PhotonicSystem(name="TFLN-Switch-Shard-V1")
    if tfln_pic.verify():
        print("\n⚓ SOVEREIGN SETTLEMENT (Aether-Mesh Hub)")
        print("🔥 MERIT BURN: -800")
        print("💰 HIL PAYMENT: -12,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")
        tfln_pic.export_pbii_profile()
        print("\n🖨️ SNC-Q7.2 FOUNDRY: Job submitted for PBII/LNOI Synthesis.")

    # Example 12: Aether-Mesh Link Audit
    print("\n" + "─" * 40)
    print("QUANTUM MISSION SYNTHESIS: Aether-Mesh-Backbone-V1")
    link_audit = AetherMeshLinkAudit()
    link_res = link_audit.run()
    if link_res.passed:
        print("\n⚓ SOVEREIGN SETTLEMENT (Aether-Mesh Connectivity)")
        print("🔥 MERIT BURN: -500")
        print("💰 HIL PAYMENT: -25,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")

    # Example 22: Ocean Infrastructure
    print("\n" + "─" * 40)
    print("AQUATIC MISSION SYNTHESIS: Sovereign-SOI-V1")
    ocean_audit = OceanInfrastructureAudit()
    o_res = ocean_audit.run()
    if o_res.passed:
        print("\n⚓ SOVEREIGN SETTLEMENT (Ocean Infrastructure)")
        print("🔥 MERIT BURN: -5,000")
        print("💰 HIL PAYMENT: -250,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")

    # Example 21: Anti-Matter
    print("\n" + "─" * 40)
    print("ENERGY MISSION SYNTHESIS: Sovereign-SAMC-V1")
    am_audit = AntimatterContainmentAudit()
    am_res = am_audit.run()
    if am_res.passed:
        print("\n⚓ SOVEREIGN SETTLEMENT (Anti-Matter Containment)")
        print("🔥 MERIT BURN: -25,000")
        print("💰 HIL PAYMENT: -1,000,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")

    # Example 20: Continental Grid
    print("\n" + "─" * 40)
    print("GRID MISSION SYNTHESIS: Sovereign-SICG-V1")
    grid_audit = ContinentalGridAudit()
    g_res = grid_audit.run()
    if g_res.passed:
        print("\n⚓ SOVEREIGN SETTLEMENT (Continental Grid)")
        print("🔥 MERIT BURN: -10,000")
        print("💰 HIL PAYMENT: -500,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")

    # Full Fleet Synthesis
    fleet = FullFleetSynthesis()
    fleet.run_all()
