# LIFELINE Independent Validator

This program performs zero-trust recomputation and validation on `cases.xlsx` and negative rejection testing on broken copies, strictly asserting all rules V1 through V8 of the project specification.

## Usage

### 1. Validate Master Dataset (`cases.xlsx`)
To validate the generated Excel workbook:
```bash
python validator.py ../cases.xlsx
```
Or from the project root:
```bash
python validator/validator.py cases.xlsx
```
Expected output:
```text
PASS! All 50 cases strictly comply with V1 through V8.
```

### 2. Run Complete Validation Suite & Negative Rejection Audit
To run the full suite (validating `cases.xlsx` and all 10 broken test cases in `validator/tests/`) and write the consolidated report to `validation_report.txt`:
```bash
python run_suite.py validation_report.txt
```
Or from the project root:
```bash
python validator/run_suite.py validation_report.txt
```

### 3. Generate / Recreate Broken Test Cases
To recreate the 10 broken test copies in `validator/tests/`:
```bash
python create_broken_tests.py
```

