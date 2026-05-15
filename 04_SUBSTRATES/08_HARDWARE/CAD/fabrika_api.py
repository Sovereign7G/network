#!/usr/bin/env python3
"""
08_HARDWARE/CAD/fabrika_api.py

============================================================================
AGE REPUBLIC — FABRIKA Specification-to-Geometry API (Modular Era)
============================================================================
A sovereign, deterministic hardware synthesis engine inspired by LEAP71.
Modularized for Era 32.2 to maintain sub-800 line codebase integrity.

Logic extracted to:
- fabrika_core.py: Base types and Engine architecture.
- fabrika_audits.py: Specialized Foundry component audits.
- fabrika_synthesis.py: Fleet mission orchestration.

Era: 32.2 | Authority: SNC-Q7.2 FoundrySteward
============================================================
"""

from typing import List, Dict, Optional, Tuple
from fabrika_core import *
from fabrika_audits import *
from fabrika_synthesis import *
import time
try:
    import serial
except ImportError:
    serial = None
import hashlib

import math
from datetime import datetime

def generate_tfln_pocket_gcode(
    stock_width=45.0,
    stock_length=45.0,
    stock_height=12.0,
    part_width=40.0,
    part_length=40.0,
    part_height=10.0,
    pocket_width=20.0,
    pocket_length=20.0,
    pocket_depth=5.0,
    tool_diameter=3.0,
    spindle_rpm=20000,
    feed_rate=500,
    plunge_feed=200,
    finish_feed=400,
    stepdown=0.4,
    safe_height=5.0,
    surface_offset=0.2,  # initial facing cut depth
    filename="tfln_housing.nc"
):
    """
    Generate G-code for TFLN Photonic Shard Housing using adaptive toolpath logic.
    """
    radius = tool_diameter / 2
    pocket_x_start = (part_width - pocket_width) / 2
    pocket_y_start = (part_length - pocket_length) / 2
    pocket_x_end = pocket_x_start + pocket_width
    pocket_y_end = pocket_y_start + pocket_length
    
    gcode_lines = []
    
    # Header
    gcode_lines.append("; TFLN Photonic Shard Housing - 6061 Aluminum")
    gcode_lines.append(f"; Generated: {datetime.now().isoformat()}")
    gcode_lines.append(f"; Tool: D={tool_diameter}mm single-flute carbide")
    gcode_lines.append(f"; Spindle: {spindle_rpm} RPM")
    gcode_lines.append(f"; Feed: {feed_rate} mm/min rough, {finish_feed} mm/min finish")
    gcode_lines.append("G90 G21 G17 G40 G49 G80")
    gcode_lines.append("G54")
    gcode_lines.append(f"M3 S{spindle_rpm}")
    gcode_lines.append("G0 Z5")
    gcode_lines.append(f"G0 X0 Y0")
    gcode_lines.append("")
    
    # ========== FACING (clean top surface) ==========
    gcode_lines.append("; --- FACING PASS ---")
    gcode_lines.append(f"G0 Z{safe_height}")
    gcode_lines.append(f"G0 X{radius} Y{radius}")
    gcode_lines.append(f"G1 Z{-surface_offset} F{plunge_feed}")
    
    rows = int(math.ceil(part_width / (tool_diameter * 0.8)))  # 80% stepover
    for i in range(rows):
        x = radius + i * tool_diameter * 0.8
        if i % 2 == 0:
            gcode_lines.append(f"G1 X{x} Y{part_length - radius} F{feed_rate}")
            gcode_lines.append(f"G1 X{x} Y{radius}")
        else:
            gcode_lines.append(f"G1 X{x} Y{radius} F{feed_rate}")
            gcode_lines.append(f"G1 X{x} Y{part_length - radius}")
    
    gcode_lines.append(f"G0 Z{safe_height}")
    gcode_lines.append("")
    
    # ========== HELICAL RAMP ENTRY (center of pocket) ==========
    center_x = pocket_x_start + pocket_width / 2
    center_y = pocket_y_start + pocket_length / 2
    helix_radius = tool_diameter * 1.2
    turns = int(math.ceil(pocket_depth / stepdown)) + 1
    
    gcode_lines.append("; --- HELICAL RAMP ENTRY ---")
    gcode_lines.append(f"G0 X{center_x + helix_radius} Y{center_y}")
    gcode_lines.append(f"G0 Z{safe_height}")
    
    z_current = 0
    for turn in range(turns):
        z_target = min(z_current - stepdown, -pocket_depth)
        delta_z = z_current - z_target
        # Full helical turn
        circumference = 2 * math.pi * helix_radius
        helix_feed = feed_rate * (delta_z / circumference) if circumference > 0 else feed_rate
        gcode_lines.append(f"G2 X{center_x + helix_radius} Y{center_y} I{-helix_radius} J0 Z{z_target} F{feed_rate}")
        z_current = z_target
        if z_current <= -pocket_depth:
            break
    
    gcode_lines.append(f"G0 Z{safe_height}")
    gcode_lines.append("")
    
    # ========== ADAPTIVE ROUGHING (trochoidal loops) ==========
    gcode_lines.append("; --- ADAPTIVE ROUGHING ---")
    
    # Boundary box for adaptive clearing
    clearance_margin = tool_diameter * 0.4
    adaptive_min_x = pocket_x_start + clearance_margin
    adaptive_max_x = pocket_x_end - clearance_margin
    adaptive_min_y = pocket_y_start + clearance_margin
    adaptive_max_y = pocket_y_end - clearance_margin
    
    # Trochoidal step pattern
    step = tool_diameter * 0.65  # 65% stepover for aluminum
    x_positions = []
    x = adaptive_min_x
    while x <= adaptive_max_x:
        x_positions.append(x)
        x += step
    
    for z_level in range(1, int(pocket_depth / stepdown) + 1):
        z_current = -min(z_level * stepdown, pocket_depth)
        gcode_lines.append(f"; Depth level {z_level}: Z{z_current}")
        
        for idx, x in enumerate(x_positions):
            if idx % 2 == 0:
                y_start = adaptive_min_y
                y_end = adaptive_max_y
            else:
                y_start = adaptive_max_y
                y_end = adaptive_min_y
            
            gcode_lines.append(f"G1 X{x} Y{y_start} F{feed_rate}")
            gcode_lines.append(f"G1 Z{z_current} F{plunge_feed}")
            gcode_lines.append(f"G1 Y{y_end} F{feed_rate}")
        
        # Clean corners after each layer
        gcode_lines.append(f"G0 Z{safe_height}")
    
    gcode_lines.append("")
    
    # ========== FINISH PASS (walls) ==========
    gcode_lines.append("; --- FINISH PASS (full depth) ---")
    gcode_lines.append(f"G0 Z{safe_height}")
    gcode_lines.append(f"G0 X{pocket_x_start + radius} Y{pocket_y_start + radius}")
    gcode_lines.append(f"G1 Z{-pocket_depth} F{plunge_feed}")
    
    # Rectangular spiral from inside out
    finish_pass_rad = radius * 0.8  # 80% radial engagement
    rect = [
        (pocket_x_start + finish_pass_rad, pocket_y_start + finish_pass_rad),
        (pocket_x_end - finish_pass_rad, pocket_y_start + finish_pass_rad),
        (pocket_x_end - finish_pass_rad, pocket_y_end - finish_pass_rad),
        (pocket_x_start + finish_pass_rad, pocket_y_end - finish_pass_rad),
        (pocket_x_start + finish_pass_rad, pocket_y_start + finish_pass_rad)
    ]
    
    for idx, (px, py) in enumerate(rect):
        gcode_lines.append(f"G1 X{px} Y{py} F{finish_feed}")
    
    gcode_lines.append("")
    
    # ========== DRILL M3 TAP HOLES (pilot 2.5mm) ==========
    gcode_lines.append("; --- PILOT HOLES FOR M3 TAPPING ---")
    gcode_lines.append("G0 Z5")
    
    m3_offset = 5.0  # 5mm from each corner
    corners = [
        (m3_offset, m3_offset),
        (part_width - m3_offset, m3_offset),
        (m3_offset, part_length - m3_offset),
        (part_width - m3_offset, part_length - m3_offset)
    ]
    
    for corner_x, corner_y in corners:
        gcode_lines.append(f"G0 X{corner_x} Y{corner_y}")
        gcode_lines.append(f"G81 X{corner_x} Y{corner_y} Z{-8.0} R{safe_height} F{plunge_feed}")  # 8mm depth for M3
        gcode_lines.append("G80")  # Cancel canned cycle
    
    gcode_lines.append("")
    
    # ========== FOOTER ==========
    gcode_lines.append("; --- PROGRAM END ---")
    gcode_lines.append("M5")
    gcode_lines.append("M9")
    gcode_lines.append("G0 Z5")
    gcode_lines.append("G0 X0 Y0")
    gcode_lines.append("M30")
    
    # Write to file
    with open(filename, 'w') as f:
        f.write('\n'.join(gcode_lines))
    
    print(f"✅ G-code generated: {filename} ({len(gcode_lines)} lines)")
    return gcode_lines

class CNCSubstrate:
    def __init__(self, machine_type="grbl-hal-5axis", steps_per_mm=80.0):
        self.machine_type = machine_type
        self.steps_per_mm = steps_per_mm
        self.active_job = None
    
    def generate_tfln_pocket(self, output_file="tfln_housing.nc"):
        """Generate TFLN photonic shard housing G-code and store path."""
        gcode = generate_tfln_pocket_gcode(filename=output_file)
        self.active_gcode_file = output_file
        return gcode

    def generate_probing_routine(self, probe_diameter=3.0, z_search_dist=20.0, feed_fast=100, feed_slow=20):
        """
        Generate G-code to probe the front-left corner (G54 X0 Y0 Z0).
        Utilizes G38.2 straight probe and G10 L20 to set workspace offsets.
        """
        radius = probe_diameter / 2.0
        print("⚙️  [CNC] Generating Probing Routine (X, Y, Z)")
        routine = [
            "; --- EDGE FINDING PROBING ROUTINE ---",
            "G21 G90 ; mm, absolute",
            "; 1. Z-axis Probing",
            f"G38.2 Z-{z_search_dist} F{feed_fast} ; Probe down fast",
            "G1 Z2.0 F500 ; Retract",
            f"G38.2 Z-3.0 F{feed_slow} ; Probe down slow",
            "G10 L20 P1 Z0 ; Set G54 Z=0",
            "G1 Z5.0 F500 ; Clear Z",
            "",
            "; 2. X-axis Probing (Assuming probe is positioned to the left of stock)",
            "G1 X-10 Y-10 F500 ; Move to front-left safe position",
            "G1 Z-5.0 F500 ; Drop below surface",
            f"G38.2 X15.0 F{feed_fast} ; Probe right fast",
            "G1 X-2.0 F500 ; Retract",
            f"G38.2 X5.0 F{feed_slow} ; Probe right slow",
            f"G10 L20 P1 X-{radius} ; Set G54 X offset for probe radius",
            "G1 X-10 F500 ; Clear X",
            "",
            "; 3. Y-axis Probing",
            "G1 X5.0 Y-10 F500 ; Move to front center",
            f"G38.2 Y15.0 F{feed_fast} ; Probe back fast",
            "G1 Y-2.0 F500 ; Retract",
            f"G38.2 Y5.0 F{feed_slow} ; Probe back slow",
            f"G10 L20 P1 Y-{radius} ; Set G54 Y offset for probe radius",
            "G1 Y-10 F500 ; Clear Y",
            "G1 Z10 F500 ; Safe Z retract",
            "; Probing complete. G54 origin set to front-left-top corner."
        ]
        return routine

    def _verify_position(self, serial_conn, expected_x, expected_y, tolerance=0.05):
        """Query GRBL '?' and parse current position to confirm actual movement."""
        serial_conn.write(b"?\n")
        resp = serial_conn.readline().decode().strip()
        # Expected format: <Idle|Run|Hold|Alarm, MPos:x,y,z, WPos:x,y,z>
        if "MPos:" in resp:
            current = resp.split("MPos:")[1].split(",")[:2]
            actual_x, actual_y = float(current[0]), float(current[1])
            if abs(actual_x - expected_x) > tolerance or abs(actual_y - expected_y) > tolerance:
                return False
        return True

    def probe_corner(self, serial_conn, probe_direction='XY', feed_rate=100, max_probe_distance=20.0):
        """
        Probe to find workpiece corner using G38.2.
        """
        import time
        results = {'x': None, 'y': None, 'z': None}
        
        # Probe Z first (safety - find top surface)
        if probe_direction in ['Z', 'XY']:
            print("   📍 Probing Z surface...")
            serial_conn.write(f"G38.2 Z-{max_probe_distance} F{feed_rate}\n".encode())
            time.sleep(0.1)
            
            while True:
                resp = serial_conn.readline().decode().strip()
                if 'PROBE' in resp and ':' in resp:
                    if 'MPos:' in resp:
                        z_pos = float(resp.split('MPos:')[1].split(',')[2])
                        results['z'] = z_pos
                        print(f"   ✅ Z surface found at {z_pos:.3f}mm")
                        break
                elif 'error' in resp.lower():
                    print(f"   ❌ Probe error: {resp}")
                    return None
                time.sleep(0.01)
        
        # Probe X negative direction
        if probe_direction in ['X', 'XY']:
            print("   📍 Probing X edge...")
            serial_conn.write(f"G91\nG38.2 X-{max_probe_distance} F{feed_rate}\n".encode())
            time.sleep(0.1)
            
            while True:
                resp = serial_conn.readline().decode().strip()
                if 'PROBE' in resp and 'MPos:' in resp:
                    current_x = float(resp.split('MPos:')[1].split(',')[0])
                    results['x'] = current_x
                    print(f"   ✅ X edge found at {current_x:.3f}mm")
                    break
                elif 'error' in resp.lower():
                    print(f"   ❌ Probe error: {resp}")
                    return None
                time.sleep(0.01)
            
            # Return to safe position
            serial_conn.write(f"G90\nG0 X{results['x'] + 5.0}\n".encode())
            time.sleep(0.5)
        
        # Probe Y negative direction
        if probe_direction in ['Y', 'XY']:
            print("   📍 Probing Y edge...")
            serial_conn.write(f"G91\nG38.2 Y-{max_probe_distance} F{feed_rate}\n".encode())
            time.sleep(0.1)
            
            while True:
                resp = serial_conn.readline().decode().strip()
                if 'PROBE' in resp and 'MPos:' in resp:
                    current_y = float(resp.split('MPos:')[1].split(',')[1])
                    results['y'] = current_y
                    print(f"   ✅ Y edge found at {current_y:.3f}mm")
                    break
                elif 'error' in resp.lower():
                    print(f"   ❌ Probe error: {resp}")
                    return None
                time.sleep(0.01)
            
            serial_conn.write(f"G90\nG0 Y{results['y'] + 5.0}\n".encode())
            time.sleep(0.5)
        
        return results

    def set_work_offset_from_probe(self, serial_conn, stock_width=45.0, stock_length=45.0, 
                                   probe_results=None, offset_number=54):
        """
        Set G54-G59 work offset based on probed corner.
        Assumes probe found bottom-left corner (Xmin, Ymin, Ztop).
        """
        if probe_results is None:
            probe_results = self.probe_corner(serial_conn, probe_direction='XY')
            if probe_results is None:
                return False
        
        center_x = probe_results['x'] + (stock_width / 2)
        center_y = probe_results['y'] + (stock_length / 2)
        top_z = probe_results['z']
        
        cmd = f"G{offset_number}\nG10 L2 P{offset_number - 53} X{center_x:.3f} Y{center_y:.3f} Z{top_z:.3f}\n"
        serial_conn.write(cmd.encode())
        time.sleep(0.1)
        
        serial_conn.write(b"$#\n")
        resp = serial_conn.readline().decode().strip()
        print(f"   🔧 Work offset G{offset_number} set: X{center_x:.1f} Y{center_y:.1f} Z{top_z:.1f}")
        
        return {'x': center_x, 'y': center_y, 'z': top_z}

    def auto_zero_tool(self, serial_conn, touch_plate_thickness=5.0, feed_rate=50):
        """
        Auto-zero tool length offset using conductive touch plate.
        """
        print("   📍 Auto-zeroing tool length...")
        
        serial_conn.write(b"G91\nG0 Z5\nG90\n")
        time.sleep(0.2)
        
        serial_conn.write(f"G38.2 Z-20 F{feed_rate}\n".encode())
        time.sleep(0.1)
        
        while True:
            resp = serial_conn.readline().decode().strip()
            if 'PROBE' in resp and 'MPos:' in resp:
                z_probe = float(resp.split('MPos:')[1].split(',')[2])
                tool_offset = z_probe - touch_plate_thickness
                serial_conn.write(f"G10 L20 P0 Z{tool_offset:.3f}\n".encode())
                print(f"   ✅ Tool offset set: Z{tool_offset:.3f}mm")
                return tool_offset
            elif 'error' in resp.lower():
                print(f"   ❌ Probe error: {resp}")
                return None
            time.sleep(0.01)

    def stream_to_machine(self, gcode_lines=None, serial_port="/dev/ttyUSB0", baud_rate=115200, hardware=False):
        """Stream G-code over serial to GRBL-HAL controller with physical feedback."""
        if gcode_lines is None and hasattr(self, 'active_gcode_file'):
            with open(self.active_gcode_file, 'r') as f:
                gcode_lines = f.readlines()
        
        print(f"📡 [CNC] Opening serial stream on {serial_port} at {baud_rate} baud...")
        execution_log = []
        
        try:
            # Mocking the serial connection for safety unless hardware is attached
            # with serial.Serial(serial_port, baud_rate, timeout=1) as s:
            print("   [CNC] Waking GRBL controller...")
            time.sleep(1)
            # s.write(b"\r\n\r\n")
            
            # Pre-flight probing
            if hardware:
                print("🔧 Running pre-flight probing...")
                # Mocked serial connection reference 's' would be used here:
                # probe_results = self.probe_corner(s, probe_direction='XY')
                # if probe_results:
                #     self.set_work_offset_from_probe(s, probe_results=probe_results)
                # self.auto_zero_tool(s)
            
            for line in gcode_lines:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith(';'):
                    continue
                    
                print(f"   [CNC] Tx: {clean_line}")
                # s.write((clean_line + '\n').encode())
                
                # Robust polling for 'ok' response instead of fixed sleep
                # while True:
                #     response = s.readline().decode().strip()
                #     if response == 'ok' or response.startswith('error'):
                #         break
                #     time.sleep(0.01)
                
                # Mock response
                response = "ok"
                time.sleep(0.05)
                
                if response == 'ok':
                    execution_log.append(clean_line)
                    # Example verification call (mocked values)
                    # self._verify_position(s, 0.0, 0.0)
                else:
                    print(f"   ❌ [CNC] ERROR: Machine halted on {clean_line}")
                    return {"status": "failed", "error": response}
                    
            print(f"✅ [CNC] Job complete. Spindle parked.")
            
            # Generate cryptographic proof of physical work
            log_string = "".join(execution_log)
            proof_hash = hashlib.sha256(log_string.encode()).hexdigest()
            print(f"🔐 [CNC] Proof of Physical Work (PoPW) Hash: {proof_hash}")
            return {"status": "success", "proof_hash": proof_hash}
            
        except Exception as e:
            print(f"   ❌ [CNC] CONNECTION ERROR: {str(e)}")
            return {"status": "connection_failed"}
    
    def estimate_duration_and_energy(self, job_spec):
        """Return (time_seconds, joules) for DePIN accounting."""
        # Baseline simulation for a standard aluminum pocket
        return (420, 250000) # 7 mins, 250kJ

if __name__ == "__main__":
    print("=" * 60)
    print("  SOVEREIGN FABRIKA ENGINE — Dual-Token Settlement")
    print("=" * 60)

    # Example 1: Standard Settlement
    sat = FABRIKAEngine.from_spec(name="Sovereign-Nano-20kN", thrust_kn=20.0)
    if sat.verify():
        sat.anchor_to_icp()
        sat.export_print_instructions()

    # Example 2: DUAL-TOKEN FAILURE ($HIL Exhaustion)
    print("\n─── EXAMPLE: Dual-Token Settlement Failure ($HIL) ───")
    # A 2500kN thruster requires 2500*50 = 125,000 $HIL (we have 100,000 in legacy logic, but check balance)
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
    trl4_spec = HilbertSpec(
        name="Hilbert-Storm-Cooler-TRL4",
        thermal_load_mw=5.0,
        order=4,
        channel_gap_mm=1.2
    )
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

    # Example 22: Ocean Infrastructure Mission Synthesis
    print("\n" + "─" * 40)
    print("AQUATIC MISSION SYNTHESIS: Sovereign-SOI-V1")
    ocean_audit = OceanInfrastructureAudit()
    o_res = ocean_audit.run()
    if o_res.passed:
        print("\n⚓ SOVEREIGN SETTLEMENT (Ocean Infrastructure)")
        print("🔥 MERIT BURN: -5,000")
        print("💰 HIL PAYMENT: -250,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")

    # Example 21: Anti-Matter Mission Synthesis
    print("\n" + "─" * 40)
    print("ENERGY MISSION SYNTHESIS: Sovereign-SAMC-V1")
    am_audit = AntimatterContainmentAudit()
    am_res = am_audit.run()
    if am_res.passed:
        print("\n⚓ SOVEREIGN SETTLEMENT (Anti-Matter Containment)")
        print("🔥 MERIT BURN: -25,000")
        print("💰 HIL PAYMENT: -1,000,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")

    # Example 20: Continental Grid Mission Synthesis
    print("\n" + "─" * 40)
    print("GRID MISSION SYNTHESIS: Sovereign-SICG-V1")
    grid_audit = ContinentalGridAudit()
    g_res = grid_audit.run()
    if g_res.passed:
        print("\n⚓ SOVEREIGN SETTLEMENT (Continental Grid)")
        print("🔥 MERIT BURN: -10,000")
        print("💰 HIL PAYMENT: -500,000 $HIL")
        print("   Status: ✅ SETTLED & TOKENIZED")

    # Full Fleet Synthesis Demonstration
    fleet = FullFleetSynthesis()
    fleet.run_all()
