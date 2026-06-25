"""
validate_format.py
Validates the blended JSONL files have the correct format for Adaptive Data ingestion.
Checks: JSONL validity, required columns, empty values, encoding, stats.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "swahili_blended"
REQUIRED_COLUMNS = ["instruction", "response", "source"]

def validate_file(filepath, label):
    if not filepath.exists():
        print(f"[FAIL] {label}: File not found at {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print(f"[FAIL] {label}: File is empty")
        return False

    errors = []
    total = len(lines)
    empty_instruction = 0
    empty_response = 0

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            errors.append(f"  Line {i}: empty line")
            continue

        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"  Line {i}: invalid JSON - {e}")
            continue

        if not isinstance(obj, dict):
            errors.append(f"  Line {i}: not a JSON object")
            continue

        for col in REQUIRED_COLUMNS:
            if col not in obj:
                errors.append(f"  Line {i}: missing column '{col}'")

        inst = obj.get("instruction", "")
        resp = obj.get("response", "")
        if not inst or not isinstance(inst, str):
            empty_instruction += 1
        if not resp or not isinstance(resp, str):
            empty_response += 1

    print(f"\n=== {label} ===")
    print(f"  Rows: {total}")
    print(f"  Empty instructions: {empty_instruction}")
    print(f"  Empty responses: {empty_response}")

    if errors:
        print(f"  Errors: {len(errors)}")
        for e in errors[:10]:
            print(e)
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        return False
    else:
        print(f"  Errors: 0")
        print(f"  [PASS] {label} is valid")
        return True

def main():
    print("=== Validating Swahili Blended Dataset ===\n")

    train_file = DATA_DIR / "train.jsonl"
    val_file = DATA_DIR / "validation.jsonl"

    train_ok = validate_file(train_file, "TRAIN")
    val_ok = validate_file(val_file, "VALIDATION")

    if train_file.exists():
        total_size = train_file.stat().st_size + (val_file.stat().st_size if val_file.exists() else 0)
        print(f"\nTotal file size: {total_size / (1024*1024):.2f} MB")

    print(f"\n=== Overall: {'PASS' if (train_ok and val_ok) else 'FAIL'} ===")

if __name__ == "__main__":
    main()
