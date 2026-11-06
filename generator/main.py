"""
LIFELINE Main Generator Script
Produces cases.xlsx adhering to all requirements in Project Phase 1 specification.
Usage:
    python main.py [--seed <group_seed>] [--output <output_path>]
"""

import os
import sys
import argparse
import openpyxl
from case_generator import generate_case

SHEET_CONFIG = [
    ('cases', [
        'case_id', 'group_seed', 'case_no', 'tier', 'scenario', 'capacity',
        'target_0', 'target_1', 'target_2', 'edit_bound', 'tour_length',
        'sensor_nodes', 'sensor_k', 'safety_vars', 'rations_target'
    ]),
    ('crates', [
        'case_id', 'crate_id', 'cat', 'weight', 'value', 'expiry', 'serial'
    ]),
    ('locations', [
        'case_id', 'loc_id', 'type', 'penalty'
    ]),
    ('roads', [
        'case_id', 'road_no', 'u', 'v', 'minutes', 'cable'
    ]),
    ('waves', [
        'case_id', 'wave_no', 'road_no'
    ]),
    ('radio_log', [
        'case_id', 'part', 'text'
    ]),
    ('radio_patterns', [
        'case_id', 'pattern_no', 'pattern', 'count'
    ]),
    ('radio_reports', [
        'case_id', 'report_a', 'report_b'
    ]),
    ('windows', [
        'case_id', 'window_id', 'start', 'finish', 'value'
    ]),
    ('incidents', [
        'case_id', 'alarm_id', 'tick', 'priority'
    ]),
    ('sites', [
        'case_id', 'site_no', 'x', 'y'
    ]),
    ('tour', [
        'case_id', 'step', 'site_no'
    ]),
    ('pipeline_dims', [
        'case_id', 'idx', 'dim'
    ]),
    ('drum_prices', [
        'case_id', 'length', 'price'
    ]),
    ('sensor_edges', [
        'case_id', 'u', 'v'
    ]),
    ('sensor_cover', [
        'case_id', 'node'
    ]),
    ('safety_rules', [
        'case_id', 'rule_no', 'lit_1', 'lit_2', 'lit_3'
    ]),
    ('safety_planted', [
        'case_id', 'switch', 'value'
    ]),
    ('rations', [
        'case_id', 'item', 'value', 'planted'
    ]),
    ('claims', [
        'case_id', 'cargo_opt', 'window_count_opt', 'window_value_opt', 'drum_opt', 'tour_opt', 'cover_min'
    ])
]

def build_workbook(group_seed, output_path):
    print(f"Generating 50 LIFELINE cases with Group Seed s = {group_seed}...")
    wb = openpyxl.Workbook()
    # remove default sheet
    wb.remove(wb.active)

    # Initialize sheets and collections
    sheet_data = {sheet_name: [] for sheet_name, _ in SHEET_CONFIG}

    for case_no in range(50):
        print(f"  Generating case {case_no:02d} (Tier {'S' if case_no<=19 else 'M' if case_no<=39 else 'L' if case_no<=45 else 'X'})...")
        cdata = generate_case(group_seed, case_no)

        # 1. cases
        cases_row = {
            'case_id': cdata['case_id'],
            'group_seed': cdata['group_seed'],
            'case_no': cdata['case_no'],
            'tier': cdata['tier'],
            'scenario': cdata['scenario'],
            'capacity': cdata['capacity'],
            'target_0': cdata['target_0'],
            'target_1': cdata['target_1'],
            'target_2': cdata['target_2'],
            'edit_bound': cdata['edit_bound'],
            'tour_length': cdata['tour_length'],
            'sensor_nodes': cdata['sensor_nodes'],
            'sensor_k': cdata['sensor_k'],
            'safety_vars': cdata['safety_vars'],
            'rations_target': cdata['rations_target']
        }
        sheet_data['cases'].append(cases_row)

        # 2. crates
        sheet_data['crates'].extend(cdata['crates'])
        # 3. locations
        sheet_data['locations'].extend(cdata['locations'])
        # 4. roads
        sheet_data['roads'].extend(cdata['roads'])
        # 5. waves
        sheet_data['waves'].extend(cdata['waves'])
        # 6. radio_log
        sheet_data['radio_log'].extend(cdata['radio_log'])
        # 7. radio_patterns
        sheet_data['radio_patterns'].extend(cdata['radio_patterns'])
        # 8. radio_reports
        sheet_data['radio_reports'].extend(cdata['radio_reports'])
        # 9. windows
        sheet_data['windows'].extend(cdata['windows'])
        # 10. incidents
        sheet_data['incidents'].extend(cdata['incidents'])
        # 11. sites
        sheet_data['sites'].extend(cdata['sites'])
        # 12. tour
        sheet_data['tour'].extend(cdata['tour'])
        # 13. pipeline_dims
        sheet_data['pipeline_dims'].extend(cdata['pipeline_dims'])
        # 14. drum_prices
        sheet_data['drum_prices'].extend(cdata['drum_prices'])
        # 15. sensor_edges
        sheet_data['sensor_edges'].extend(cdata['sensor_edges'])
        # 16. sensor_cover
        sheet_data['sensor_cover'].extend(cdata['sensor_cover'])
        # 17. safety_rules
        sheet_data['safety_rules'].extend(cdata['safety_rules'])
        # 18. safety_planted
        sheet_data['safety_planted'].extend(cdata['safety_planted'])
        # 19. rations
        sheet_data['rations'].extend(cdata['rations'])
        # 20. claims (Tier S only)
        if 'claims' in cdata:
            sheet_data['claims'].extend(cdata['claims'])

    print("Sorting sheets by case_id, then second column...")
    for sheet_name, cols in SHEET_CONFIG:
        ws = wb.create_sheet(title=sheet_name)
        # Header row
        ws.append(cols)
        
        rows = sheet_data[sheet_name]
        sec_col = cols[1]
        
        # Sort by case_id, then second column
        # case_id format: "<s>-<kk>", we can parse integer case_no for natural sorting
        def sort_key(row):
            cid_parts = row['case_id'].split('-')
            c_num = int(cid_parts[1]) if len(cid_parts) > 1 else 0
            val2 = row[sec_col]
            # Handle string vs int sorting safely
            if isinstance(val2, str):
                return (c_num, 0, val2)
            return (c_num, 1, val2)

        rows.sort(key=sort_key)

        for row in rows:
            ws.append([row[col] for col in cols])

    print(f"Saving workbook to {output_path}...")
    wb.save(output_path)
    print("Generation complete! cases.xlsx is ready.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LIFELINE Excel Generator")
    parser.add_argument('--seed', type=int, default=66, help="Group seed (default 66)")
    parser.add_argument('--output', type=str, default='cases.xlsx', help="Output xlsx path")
    args = parser.parse_args()

    build_workbook(args.seed, args.output)

