#!/usr/bin/env python3
"""Fix D354 (HL) CPTs - add parent_effects to noisy_or_params

The original D67 had parent_effects in 33 evidence variables.
After splitting, D354 needs its own parent_effects for the evidence
variables it has edges to. Also adjust D67's T03/L04 values since
the original was "averaged" between NHL+HL.
"""

import json
import copy

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {path}")

def main():
    data = load_json('step3_fever_cpts_v2.json')
    nop = data.get('noisy_or_params', {})

    # D354 (HL) has edges to these variables:
    d354_edge_targets = ['E01','S16','S17','E13','E14','L16','L41','S07',
                         'L28','S46','T01','T03','L04','L22','S01','E46']

    # For each, add D354 parent_effects (copy from D67 and adjust where needed)
    for var in d354_edge_targets:
        if var not in nop:
            print(f"  WARNING: {var} not in noisy_or_params, skipping")
            continue

        pe = nop[var].get('parent_effects', {})
        if 'D67' not in pe:
            print(f"  WARNING: D67 not in {var} parent_effects, skipping")
            continue

        # Start from D67's values
        d354_pe = copy.deepcopy(pe['D67'])

        # Adjust HL-specific differences
        if var == 'T03':
            # HL: Pel-Ebstein periodic fever is VERY characteristic (30-40%)
            # NHL: periodic is rare
            d354_pe = {"continuous": 0.2, "intermittent": 0.15, "periodic": 0.6, "double_quotidian": 0.05}
            # Also fix NHL - reduce periodic
            pe['D67'] = {"continuous": 0.35, "intermittent": 0.35, "periodic": 0.2, "double_quotidian": 0.1}
            print(f"  Adjusted T03: HL periodic=0.6, NHL periodic=0.2")

        elif var == 'L04':
            # HL: mediastinal involvement much higher (60%+)
            # NHL: mediastinal lower (20%)
            d354_pe = {"not_done": 0.05, "normal": 0.15, "lobar_infiltrate": 0.05,
                       "bilateral_infiltrate": 0.15, "BHL": 0.30, "pleural_effusion": 0.25,
                       "pneumothorax": 0.005}
            print(f"  Adjusted L04: HL mediastinal higher")

        elif var == 'E13':
            # HL: lymphadenopathy 90%+, cervical dominant
            d354_pe = {"absent": 0.02, "present": 0.98}

        elif var == 'E46':
            # HL: cervical/supraclavicular/mediastinal dominant
            d354_pe = {"cervical": 0.40, "axillary": 0.05, "inguinal": 0.02,
                       "supraclavicular": 0.10, "mediastinal": 0.30, "generalized": 0.13}
            # NHL: more generalized
            pe['D67'] = {"cervical": 0.15, "axillary": 0.05, "inguinal": 0.05,
                         "supraclavicular": 0.02, "mediastinal": 0.03, "generalized": 0.70}
            print(f"  Adjusted E46: HL cervical/mediastinal, NHL generalized")

        elif var == 'L22':
            # HL: anemia more common (40-50%)
            d354_pe = {"absent": 0.5, "present": 0.5}

        elif var == 'E14':
            # HL: splenomegaly 30-40%
            d354_pe = {"absent": 0.5, "present": 0.5}

        pe['D354'] = d354_pe

    # Also handle variables that D67 (NHL) has edges to but D354 doesn't
    # These keep their D67 entries as-is (no D354 added)

    save_json('step3_fever_cpts_v2.json', data)
    print(f"\n  Added D354 parent_effects to {len(d354_edge_targets)} evidence variables")

if __name__ == '__main__':
    print("Fix D354 (HL) CPTs in noisy_or_params")
    main()
