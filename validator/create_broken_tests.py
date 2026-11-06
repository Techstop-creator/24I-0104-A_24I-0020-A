"""
Generator for Broken Test Cases
Creates at least two valid cases broken in at least 5 distinct ways each (>= 10 test files)
in validator/tests/ to prove the validator rejects invalid inputs.
"""

import os
import shutil
import openpyxl

TESTS_DIR = os.path.join(os.path.dirname(__file__), 'tests')
SRC_FILE = os.path.join(os.path.dirname(__file__), '..', 'cases.xlsx')

def make_broken_copy(name, mutator_fn):
    out_path = os.path.join(TESTS_DIR, name)
    wb = openpyxl.load_workbook(SRC_FILE)
    mutator_fn(wb)
    wb.save(out_path)
    print(f"Created broken test: {name}")

def mut_v1_bad_sheet(wb):
    # Rename 'claims' sheet
    ws = wb['claims']
    ws.title = 'wrong_claims_name'

def mut_v2_crate_weight(wb):
    # Crate weight > 20
    ws = wb['crates']
    ws.cell(row=2, column=4, value=99) # row 2 is first data row (crate 1 of case 00)

def mut_v3_dangling_target(wb):
    # target_0 points to node 999
    ws = wb['cases']
    ws.cell(row=2, column=7, value=999) # target_0 column

def mut_v4_disconnected_graph(wb):
    # Remove all incident roads to node 1 in case 00
    ws = wb['roads']
    # Delete road row where u=0 and v=target
    for r in range(2, 20):
        ws.cell(row=r, column=3, value=0) # u=0
        ws.cell(row=r, column=4, value=2) # v=2 (isolating node 1)

def mut_v5_wrong_claim(wb):
    # Corrupt Tier S claim cargo_opt
    ws = wb['claims']
    ws.cell(row=2, column=2, value=99999)

def mut_v2_bad_penalty(wb):
    # Location penalty not in {0, 1, 2, 4, 6} in Case 20
    ws = wb['locations']
    # Find row belonging to case 66-20
    for r in range(2, ws.max_row + 1):
        if str(ws.cell(row=r, column=1).value).endswith('-20'):
            ws.cell(row=r, column=4, value=99)
            break

def mut_v4_overlapping_waves(wb):
    # Duplicate road across waves in Case 20
    ws = wb['waves']
    for r in range(2, ws.max_row):
        c1 = str(ws.cell(row=r, column=1).value)
        c2 = str(ws.cell(row=r+1, column=1).value)
        if c1.endswith('-20') and c2.endswith('-20'):
            w1 = ws.cell(row=r, column=2).value
            w2 = ws.cell(row=r+1, column=2).value
            if w1 != w2:
                # set same road_no
                ws.cell(row=r+1, column=3, value=ws.cell(row=r, column=3).value)
                break

def mut_v5_bad_pattern_count(wb):
    # Corrupt pattern count in Case 20
    ws = wb['radio_patterns']
    for r in range(2, ws.max_row + 1):
        if str(ws.cell(row=r, column=1).value).endswith('-20'):
            cur_cnt = ws.cell(row=r, column=4).value
            ws.cell(row=r, column=4, value=(cur_cnt + 500))
            break

def mut_v6_unsat_3sat(wb):
    # Make safety rule 1 completely unsatisfied by the planted assignment in Case 20
    # First, read the planted switches for Case 20
    ws_sp = wb['safety_planted']
    planted_vals = {}
    for r in range(2, ws_sp.max_row + 1):
        if str(ws_sp.cell(row=r, column=1).value).endswith('-20'):
            sw = ws_sp.cell(row=r, column=2).value
            v = ws_sp.cell(row=r, column=3).value
            planted_vals[sw] = v

    # Now in safety_rules for Case 20, set rule 1 literals opposite to planted values!
    ws_sr = wb['safety_rules']
    for r in range(2, ws_sr.max_row + 1):
        if str(ws_sr.cell(row=r, column=1).value).endswith('-20'):
            # Invert all three literals to guarantee unsatisfiability
            for c_idx, var_idx in [(3, 1), (4, 2), (5, 3)]:
                # If planted value is 1, literal -var_idx is false. If 0, +var_idx is false.
                pv = planted_vals.get(var_idx, 1)
                false_lit = -var_idx if pv == 1 else var_idx
                ws_sr.cell(row=r, column=c_idx, value=false_lit)
            break

def mut_v6_invalid_rations(wb):
    # Alter rations target in Case 20
    ws = wb['cases']
    for r in range(2, ws.max_row + 1):
        if str(ws.cell(row=r, column=1).value).endswith('-20'):
            ws.cell(row=r, column=15, value=999999) # rations_target
            break

def generate_all_broken_tests():
    os.makedirs(TESTS_DIR, exist_ok=True)
    tests = [
        ('case_00_broken_1_V1_bad_sheet.xlsx', mut_v1_bad_sheet),
        ('case_00_broken_2_V2_crate_weight.xlsx', mut_v2_crate_weight),
        ('case_00_broken_3_V3_dangling_target.xlsx', mut_v3_dangling_target),
        ('case_00_broken_4_V4_disconnected_graph.xlsx', mut_v4_disconnected_graph),
        ('case_00_broken_5_V5_wrong_claim.xlsx', mut_v5_wrong_claim),
        ('case_20_broken_1_V2_bad_penalty.xlsx', mut_v2_bad_penalty),
        ('case_20_broken_2_V4_overlapping_waves.xlsx', mut_v4_overlapping_waves),
        ('case_20_broken_3_V5_bad_pattern_count.xlsx', mut_v5_bad_pattern_count),
        ('case_20_broken_4_V6_unsat_3sat.xlsx', mut_v6_unsat_3sat),
        ('case_20_broken_5_V6_invalid_rations.xlsx', mut_v6_invalid_rations),
    ]

    for filename, fn in tests:
        make_broken_copy(filename, fn)

if __name__ == '__main__':
    generate_all_broken_tests()

