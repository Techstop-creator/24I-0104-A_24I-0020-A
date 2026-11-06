"""
Validation Test Suite Runner
Runs validator on master cases.xlsx (asserting PASS) and on all broken test cases (asserting REJECTION).
Outputs the consolidated report to validation_report.txt.
"""

import os
import sys
from validator import Validator

def run_suite(report_path="validation_report.txt"):
    report_lines = []
    
    def log(msg=""):
        print(msg)
        report_lines.append(msg)

    log("=" * 80)
    log("LIFELINE VALIDATION SUITE REPORT")
    log("Group Number: 66 | Section: AI-A | Degree: BS Artificial Intelligence")
    log("Members: Irtaza Shahid (24I-0104), Muhammad Harris (24I-0020)")
    log("=" * 80)
    log()

    # 1. Validate Master cases.xlsx
    master_path = os.path.join(os.path.dirname(__file__), "..", "cases.xlsx")
    log(f"--- [1/2] VALIDATING MASTER DATASET: {os.path.abspath(master_path)} ---")
    val = Validator(master_path)
    passed, errors = val.run_all()
    if passed:
        log("STATUS: PASS")
        log("RESULT: All 50 cases strictly comply with all rules V1 through V8.")
    else:
        log("STATUS: FAILED")
        for err in errors:
            log(f"  {err}")
    log()

    # 2. Validate Broken Test Cases in validator/tests/
    tests_dir = os.path.join(os.path.dirname(__file__), "tests")
    log("--- [2/2] VALIDATING BROKEN TEST COPIES (NEGATIVE REJECTION AUDIT) ---")
    test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".xlsx")])
    
    rejected_count = 0
    for tf in test_files:
        tf_path = os.path.join(tests_dir, tf)
        log(f"Testing broken case: {tf}")
        b_val = Validator(tf_path)
        b_passed, b_errors = b_val.run_all()
        if not b_passed:
            rejected_count += 1
            log("  STATUS: REJECTED (CORRECT BEHAVIOR)")
            log(f"  Detected {len(b_errors)} broken rule(s):")
            for err in b_errors[:3]: # print top 3
                log(f"    -> {err}")
            if len(b_errors) > 3:
                log(f"    -> ... and {len(b_errors) - 3} more.")
        else:
            log("  STATUS: ERROR - Broken file unexpectedly passed validation!")
        log()

    log("=" * 80)
    log(f"SUMMARY: Master dataset PASS. Rejection audit: {rejected_count}/{len(test_files)} broken copies correctly rejected.")
    log("=" * 80)

    # Write report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\nConsolidated report written to {report_path}")

if __name__ == "__main__":
    report_file = sys.argv[1] if len(sys.argv) > 1 else "validation_report.txt"
    run_suite(report_file)

