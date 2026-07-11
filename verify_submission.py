import argparse
import json
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--id", required=True, help="Student ID")
args = parser.parse_args()

required_files = [
    "avionics_bus.py",
    "fault_seed.py",
    "hardware_config.json",
    "AI_PROMPT_LEDGER.md",
    "history.txt"
]

print("========== SUBMISSION VERIFICATION ==========")
print(f"Student ID: {args.id}\n")

all_ok = True

# Check required files
for file in required_files:
    if os.path.exists(file):
        print(f"[PASS] {file} found.")
    else:
        print(f"[FAIL] {file} not found.")
        all_ok = False

# Check hardware configuration
if os.path.exists("hardware_config.json"):
    try:
        with open("hardware_config.json", "r") as f:
            config = json.load(f)

        required_keys = [
            "signature_hash",
            "buffer_overflow_threshold",
            "imu_voltage_drift",
            "bus_race_delay_sec"
        ]

        for key in required_keys:
            if key in config:
                print(f"[PASS] {key} found.")
            else:
                print(f"[FAIL] {key} missing.")
                all_ok = False

    except Exception as e:
        print(f"[FAIL] Unable to read hardware_config.json: {e}")
        all_ok = False

print()

if all_ok:
    print("Verification completed successfully.")
    print("Submission appears ready.")
    sys.exit(0)
else:
    print("Verification failed.")
    sys.exit(1)