#!/usr/bin/env python3
"""Run this IMMEDIATELY after connecting the SNC-Q7.2"""
import serial
import sys

ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0']
for port in ports:
    try:
        s = serial.Serial(port, 115200, timeout=2)
        s.write(b"$$\n")
        response = s.readline().decode().strip()
        if response:
            print(f"✅ Connected to {port}")
            print(f"Response: {response}")
            s.close()
            sys.exit(0)
    except:
        continue
print("❌ No CNC found. Check USB connection.")
