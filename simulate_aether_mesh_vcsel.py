import math

class OpticalWirelessTransceiver:
    """
    Simulation of the 360 Gbps VCSEL-based Optical Wireless link
    (Advanced Photonics Nexus, 2026).
    Maps to the AGE Protocol's Aether-Mesh intra-ship communications.
    """
    def __init__(self, array_size=(5, 5)):
        self.array_size = array_size
        self.num_lasers = array_size[0] * array_size[1]
        
        # Performance specs from the paper
        self.active_lasers = 21  # 21 out of 25 active in the test
        self.avg_speed_per_laser = 17.27  # Gbps (362.7 total / 21 lasers)
        self.energy_per_bit_nJ = 1.4  # nanojoules per bit
        
        # Wi-Fi baseline for comparison
        self.wifi_energy_per_bit_nJ = 2.8  # "roughly half that of leading Wi-Fi"
        self.wifi_speed_gbps = 9.6  # WiFi 6 max theoretical, usually much lower

    def calculate_link_capacity(self):
        """Returns total Gbps and TB/hr for the active array."""
        total_gbps = self.active_lasers * self.avg_speed_per_laser
        tb_per_hour = (total_gbps / 8) * 3600 / 1000  # Gbps -> GBps -> sec/hr -> TB
        return total_gbps, tb_per_hour

    def calculate_energy_efficiency(self, data_tb):
        """Compares energy usage against standard Wi-Fi for a given data load."""
        bits = data_tb * 8000 * 1e9  # TB to bits (1 TB = 8000 Gb)
        
        # Energy in Joules (nanojoules * 1e-9)
        optical_energy_joules = bits * (self.energy_per_bit_nJ * 1e-9)
        wifi_energy_joules = bits * (self.wifi_energy_per_bit_nJ * 1e-9)
        
        # Convert to Watt-hours (3600 J = 1 Wh)
        optical_wh = optical_energy_joules / 3600
        wifi_wh = wifi_energy_joules / 3600
        
        return optical_wh, wifi_wh

def run_aether_mesh_simulation():
    print("═" * 78)
    print(" 📡 AETHER-MESH INTRA-SHIP OPTICAL LINK (Advanced Photonics Nexus 2026)")
    print(" Architecture: 5x5 VCSEL Array | Metric: 362.7 Gbps | Target: SV Storm-Breaker")
    print("═" * 78)

    transceiver = OpticalWirelessTransceiver()
    
    # [1] Link Capacity
    gbps, tb_hr = transceiver.calculate_link_capacity()
    print(f"\n[THROUGHPUT] VCSEL Array Active ({transceiver.active_lasers}/{transceiver.num_lasers} units)")
    print(f"  • Single-Beam Rate:  {transceiver.avg_speed_per_laser:.2f} Gbps")
    print(f"  • Total Link Rate:   {gbps:.2f} Gbps")
    print(f"  • Hourly Transfer:   {tb_hr:.1f} Terabytes/hour")
    
    # [2] Energy Profile for 1 Petabyte Transfer (Standard Genome/Telemetry sync)
    petabyte = 1000  # TB
    opt_wh, wifi_wh = transceiver.calculate_energy_efficiency(petabyte)
    
    print(f"\n[ENERGY EFFICIENCY] 1 Petabyte Intra-Ship Transfer Simulation")
    print(f"  {'Protocol':<20} | {'Energy Req.':>15} | {'Speed Limit'}")
    print(f"  {'─'*20} | {'─'*15} | {'─'*15}")
    print(f"  {'Legacy Wi-Fi 6':<20} | {wifi_wh:>10.2f} Wh    |   9.6 Gbps")
    print(f"  {'VCSEL Optical Mesh':<20} | {opt_wh:>10.2f} Wh    | 362.7 Gbps")
    print(f"  {'Savings (%):':<20} | {((wifi_wh - opt_wh)/wifi_wh)*100:>10.1f}%     | +3,678 %")

    # [3] Sovereignty Mapping
    print("\n[SOVEREIGN IMPACT] The End of RF Crosstalk")
    print("    By phasing out Radio Frequency (RF) intra-ship comms in favor of")
    print("    steered VCSEL optical grids, the AGE Protocol eliminates electromagnetic")
    print("    interference (EMI) near the SBR-1 magnetic confinement coils.")
    print("\n    The Ghost-Shroud (-55.1 dB signature) is preserved. No radio bleed.")
    print("    The Aether-Mesh is physically un-hardenable by external EM warfare.")
    
    print("\n🏮🏯🔬🚀⚡💎🏢🛰️☀️☢️🔋🌀\n")

if __name__ == "__main__":
    run_aether_mesh_simulation()
