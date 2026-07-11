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