import argparse
import json
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument("--id", required=True, help="Student ID")
args = parser.parse_args()

student_id = args.id

signature_hash = hashlib.sha256(student_id.encode()).hexdigest()[:8].upper()

last_digit = int(student_id[-1])

config = {
    "signature_hash": signature_hash,
    "buffer_overflow_threshold": 20 + (last_digit % 10),
    "imu_voltage_drift": 1.0 + (last_digit / 5),
    "bus_race_delay_sec": 0.002
}

with open("hardware_config.json", "w") as f:
    json.dump(config, f, indent=4)

print("Hardware configuration generated successfully.")
print(json.dumps(config, indent=4))