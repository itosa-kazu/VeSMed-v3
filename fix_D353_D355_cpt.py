#!/usr/bin/env python3
"""Fix D353 (UC) and D355 (DVT) - add parent_effects to noisy_or_params"""

import json
import copy

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    data = load_json('step3_fever_cpts_v2.json')
    nop = data.get('noisy_or_params', {})

    # === Fix D353 (UC) ===
    # UC has edges to: E01, S14, S26, S12, S17, L02, L28, S46, T01, S07, L01, E02, S86, S89
    # Copy from D63 (Crohn's) and adjust for UC-specific differences

    # Get D353's edge targets
    d353_edge_targets = ['E01','S14','S26','S12','S17','L02','L28','S46','T01','S07','L01','E02','S86','S89']

    for var in d353_edge_targets:
        if var not in nop:
            continue
        pe = nop[var].get('parent_effects', {})
        if 'D63' not in pe:
            continue

        d353_pe = copy.deepcopy(pe['D63'])

        # UC-specific adjustments
        if var == 'S26':  # bloody stool: UC much higher than CD
            d353_pe = {"absent": 0.05, "present": 0.95}
            pe['D63'] = {"absent": 0.40, "present": 0.60}  # CD: less bloody
        elif var == 'S86':  # diarrhea character: UC is bloody
            d353_pe = {"watery": 0.1, "bloody": 0.9}
            pe['D63'] = {"watery": 0.5, "bloody": 0.5}  # CD: mixed
        elif var == 'S89':  # abdominal pain location: UC=LLQ, CD=RLQ
            d353_pe = {"epigastric": 0.05, "RUQ": 0.05, "RLQ": 0.05, "LLQ": 0.45, "suprapubic": 0.10, "diffuse": 0.30}
            pe['D63'] = {"epigastric": 0.05, "RUQ": 0.05, "RLQ": 0.40, "LLQ": 0.10, "suprapubic": 0.05, "diffuse": 0.35}
        elif var == 'S17':  # weight loss: UC less than CD
            d353_pe = {"absent": 0.50, "present": 0.50}
            pe['D63'] = {"absent": 0.25, "present": 0.75}
        elif var == 'S14':  # diarrhea: UC slightly higher
            d353_pe = {"absent": 0.03, "present": 0.97}

        pe['D353'] = d353_pe

    print(f"Added D353 (UC) parent_effects for {len(d353_edge_targets)} evidence vars")

    # === Fix D355 (DVT) ===
    # DVT has edges to: E01, S39, L20, S04, E02, E05, T01, T02, E36, L01, L02
    # Copy from D77 (PE) where possible and adjust for DVT

    d355_edge_targets = ['E01','S39','L20','S04','E02','E05','T01','T02','E36','L01','L02']

    for var in d355_edge_targets:
        if var not in nop:
            continue
        pe = nop[var].get('parent_effects', {})

        # Use D77 (PE) as base if available
        if 'D77' in pe:
            d355_pe = copy.deepcopy(pe['D77'])
        else:
            continue

        # DVT-specific adjustments
        if var == 'E01':  # fever: DVT very low, PE low
            d355_pe = {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.0, "hypothermia_under_35": 0.0}
        elif var == 'S39':  # leg swelling: DVT=dominant, PE=secondary
            d355_pe = {"absent": 0.05, "present": 0.95}
            pe['D77'] = {"absent": 0.60, "present": 0.40}  # PE: less common
        elif var == 'S04':  # dyspnea: DVT=rare, PE=common
            d355_pe = {"absent": 0.80, "on_exertion": 0.15, "at_rest": 0.05}
        elif var == 'E05':  # SpO2: DVT=normal, PE=low
            d355_pe = {"normal_over_96": 0.85, "mild_hypoxia_93_96": 0.12, "severe_hypoxia_under_93": 0.03}
        elif var == 'E02':  # HR: DVT=normal, PE=tachycardia
            d355_pe = {"under_100": 0.70, "100_120": 0.25, "over_120": 0.05}
        elif var == 'T01':  # fever duration: DVT=subacute
            d355_pe = {"under_3d": 0.30, "3d_to_1w": 0.40, "1w_to_3w": 0.25, "over_3w": 0.05}
        elif var == 'T02':  # onset: DVT=gradual, PE=sudden
            d355_pe = {"sudden": 0.05, "acute": 0.30, "subacute": 0.50, "chronic": 0.15}
        elif var == 'L20':  # D-dimer: both elevated
            pass  # Keep PE's values (both similar)
        elif var == 'L01':  # WBC: DVT can elevate
            d355_pe = {"low_under_4000": 0.05, "normal_4000_10000": 0.45, "high_10000_20000": 0.40, "very_high_over_20000": 0.10}
        elif var == 'L02':  # CRP: DVT mild
            d355_pe = {"normal_under_0.3": 0.30, "mild_0.3_3": 0.40, "moderate_3_10": 0.25, "high_over_10": 0.05}

        pe['D355'] = d355_pe

    # Also add E36 if not in nop (limb edema)
    if 'E36' in nop and 'D355' not in nop['E36'].get('parent_effects', {}):
        nop['E36']['parent_effects']['D355'] = {"absent": 0.05, "present": 0.95}

    print(f"Added D355 (DVT) parent_effects for {len(d355_edge_targets)} evidence vars")

    save_json('step3_fever_cpts_v2.json', data)
    print("Saved")

if __name__ == '__main__':
    main()
