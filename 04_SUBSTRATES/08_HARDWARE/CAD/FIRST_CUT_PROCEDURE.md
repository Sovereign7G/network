# First Cut - TFLN Photonic Shard Housing

## Pre-flight
1. Connect SNC-Q7.2 via USB
2. Run `python3 test_hardware_connection.py`
3. Home all axes (`$H`)
4. Secure 45x45x12mm 6061 aluminum to bed
5. Install 3mm single-flute carbide endmill

## Toolpath verification
6. Dry run at Z+5mm (spindle off)
7. Verify pocket location matches stock
8. Run probing routine to set work offset

## First cut
9. Set spindle to 18,000 RPM
10. Run job: `python3 MERIENDA_DEPIN_ORCHESTRATOR.py`
11. Stand by with feed hold button (spacebar)
12. Measure result with calipers

## Success criteria
- Pocket depth: 5.0mm ±0.1mm
- Pocket width: 20.0mm ±0.1mm
- Wall finish: No visible tool marks >0.05mm
- No endmill breakage
