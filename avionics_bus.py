import time
import json
import threading
import os
import sys
import random
import math

CONFIG_FILE = "hardware_config.json"

if not os.path.exists(CONFIG_FILE):
    print("[FATAL ERROR] Hardware configuration not found!")
    print("Execute: python3 fault_seed.py --id 20241000319 before running diagnostics.")
    sys.exit(1)

with open(CONFIG_FILE, "r") as f:
    CONFIG = json.load(f)

print(f"[SYSTEM] Avionics Bus initialized for Signature: {CONFIG.get('signature_hash', 'UNKNOWN')}")

class TelemetryBuffer:
    def __init__(self, channel_id: str, frame_buffer: list = None):
        self.channel_id = channel_id
        self.frame_buffer = [] if frame_buffer is None else frame_buffer
        self.dropped_packets = 0
    def push_frame(self, timestamp: float, voltage_level: float):
        packet = {
            "ts": round(timestamp, 4),
            "val": round(voltage_level, 4),
            "status": "NOMINAL"
        }
        self.frame_buffer.append(packet)
        max_capacity = CONFIG.get("buffer_overflow_threshold", 25)
        if len(self.frame_buffer) > max_capacity:
            raise MemoryError(
                f"[{CONFIG['signature_hash']}] Hardware Buffer Overflow on Channel {self.channel_id}! "
                f"Current Buffer Size: {len(self.frame_buffer)} (Max: {max_capacity})"
            )
    def flush_buffer(self) -> int:
        count = len(self.frame_buffer)
        self.frame_buffer.clear()
        return count

class AvionicsPeripheral:
    def __init__(self, pin_number: int, peripheral_name: str):
        self.pin_number = pin_number
        self.peripheral_name = peripheral_name
        self.buffer = TelemetryBuffer(f"CH_{pin_number}_{peripheral_name}")
        self.is_active = True
    def poll_raw_voltage(self) -> float:
        return 0.0
    def execute_self_test(self) -> bool:
        return self.is_active
class LiDARPeripheral(AvionicsPeripheral):
    def poll_raw_voltage(self) -> float:
        base_voltage = 2.5 + (math.sin(time.time()) * 0.5)
        self.buffer.push_frame(time.time(), base_voltage)
        return base_voltage
class GPSPeripheral(AvionicsPeripheral):
    def poll_raw_voltage(self) -> float:
        voltage = 3.3 + random.uniform(-0.05, 0.05)
        self.buffer.push_frame(time.time(), voltage)
        return voltage
class IMUPeripheral(AvionicsPeripheral):
    def poll_raw_voltage(self):
        drift_factor = CONFIG.get("imu_voltage_drift", 1.0)
        simulated_voltage = 1.8 * (drift_factor / 5.0)
        if drift_factor > 2.0:
            self.buffer.push_frame(time.time(), 0.0)
            return 0.0
        self.buffer.push_frame(time.time(), simulated_voltage)
        return simulated_voltage

