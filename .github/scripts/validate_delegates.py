#!/usr/bin/env python3

import json
import os
import pathlib
import re
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DELEGATES_PATH = REPO_ROOT / "delegates.json"
LIMITS_PATH = REPO_ROOT / ".github" / "delegates-limits.json"


def validate_ethereum_address(address):
    if not isinstance(address, str):
        return False, "Address must be a string type"

    if not re.match(r"^(0x)?[0-9a-fA-F]{40}$", address):
        return False, "Invalid address format, must be 0x followed by 40 hexadecimal characters"

    if not address.startswith("0x"):
        address = "0x" + address

    if int(address, 16) == 0:
        return False, "Address is the zero address"

    return True, address


def validate_voteweight(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        return False
    return True


def load_limits(limits_path):
    with open(limits_path, "r", encoding="utf-8") as f:
        limits = json.load(f)

    if not isinstance(limits, dict):
        raise ValueError("delegates-limits.json must be an object")

    if "max_total" not in limits:
        raise ValueError("delegates-limits.json missing required field: max_total")

    max_total = limits["max_total"]
    max_per_delegate = limits.get("max_per_delegate")

    if not validate_voteweight(max_total):
        raise ValueError("max_total must be a number >= 0")

    if max_per_delegate is not None and not validate_voteweight(max_per_delegate):
        raise ValueError("max_per_delegate must be a number >= 0")

    return max_total, max_per_delegate


def validate_delegates(delegates_path, limits_path):
    max_total, max_per_delegate = load_limits(limits_path)

    with open(delegates_path, "r", encoding="utf-8") as f:
        delegates = json.load(f)

    if not isinstance(delegates, list):
        return False, ["delegates must be an array"], [], 0

    errors = []
    warnings = []
    addresses = set()
    total_voteweight = 0

    for i, delegate in enumerate(delegates):
        index = i + 1

        if not isinstance(delegate, dict):
            errors.append(f"Delegate {index} must be an object")
            continue

        if "Voteweight" not in delegate:
            errors.append(f"Delegate {index} missing Voteweight field")
        elif not validate_voteweight(delegate["Voteweight"]):
            errors.append(f"Delegate {index} Voteweight must be a number >= 0")
        else:
            voteweight = delegate["Voteweight"]
            if max_per_delegate is not None and voteweight > max_per_delegate:
                errors.append(
                    f"Delegate {index} Voteweight {voteweight} exceeds per-delegate cap of {max_per_delegate}"
                )
            total_voteweight += voteweight

        if "Address" not in delegate:
            errors.append(f"Delegate {index} missing Address field")
        else:
            valid, result = validate_ethereum_address(delegate["Address"])
            if not valid:
                errors.append(
                    f"Delegate {index} Address validation failed: {delegate['Address']} - {result}"
                )
            else:
                normalized_address = result.lower()
                if normalized_address in addresses:
                    errors.append(f"Delegate {index} has duplicate address: {delegate['Address']}")
                else:
                    addresses.add(normalized_address)

        if "InternalReference" in delegate and not isinstance(delegate["InternalReference"], str):
            warnings.append(f"Delegate {index} InternalReference should be a string type")

    if total_voteweight > max_total:
        errors.append(f"Total Voteweight {total_voteweight} exceeds cap of {max_total}")

    return len(errors) == 0, errors, warnings, len(delegates)


def write_github_output(success, errors):
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        return

    delim = "VALIDATION_EOF"
    with open(github_output, "a", encoding="utf-8") as f:
        if success:
            f.write("validation_result=passed\n")
            f.write(f"validation_message<<{delim}\n")
            f.write("Validation passed\n")
            f.write(f"{delim}\n")
        else:
            f.write("validation_result=failed\n")
            f.write(f"validation_message<<{delim}\n")
            f.write("\n".join(errors) + "\n")
            f.write(f"{delim}\n")


def main():
    print("🔍 Starting validation of delegates.json file...")

    try:
        success, errors, warnings, delegate_count = validate_delegates(DELEGATES_PATH, LIMITS_PATH)

        if success:
            print("✅ Validation passed!")
            print(f"📊 Validated {delegate_count} delegates")
            if warnings:
                print("\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"   - {warning}")
        else:
            print("❌ Validation failed!")
            print("\nError details:")
            for error in errors:
                print(f"   - {error}")
            if warnings:
                print("\n⚠️  Warnings:")
                for warning in warnings:
                    print(f"   - {warning}")

        write_github_output(success, errors if errors else ["Validation passed"])

        if not success:
            sys.exit(1)

    except FileNotFoundError as exc:
        message = f"Required file does not exist: {exc.filename}"
        print(f"❌ Error: {message}")
        write_github_output(False, [message])
        sys.exit(1)
    except json.JSONDecodeError as exc:
        message = f"JSON format is invalid - {exc}"
        print(f"❌ Error: {message}")
        write_github_output(False, [message])
        sys.exit(1)
    except Exception as exc:
        message = f"Error occurred during validation: {exc}"
        print(f"❌ Error: {message}")
        write_github_output(False, [message])
        sys.exit(1)


if __name__ == "__main__":
    main()
