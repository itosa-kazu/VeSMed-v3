#!/usr/bin/env python3
"""Test each batch 2 subgroup independently to find which ones help/hurt."""
import json, subprocess, re, copy

with open('step2_fever_edges_v4.json', encoding='utf-8') as f:
    s2_orig = json.load(f)
with open('step3_fever_cpts_v2.json', encoding='utf-8') as f:
    s3_orig = json.load(f)
with open('step1_fever_v2.7.json', encoding='utf-8') as f:
    s1 = json.load(f)

var_names = {v['id']: v.get('name_ja', v.get('name', '')) for v in s1['variables']}

groups = {
    'pediatric': {
        'D253': {'parents': ['R01'], 'cpt': {'0_1': 0.010, '1_5': 0.003}},
        'D258': {'parents': ['R01'], 'cpt': {'0_1': 0.010, '1_5': 0.005}},
        'D338': {'parents': ['R01'], 'cpt': {'0_1': 0.008, '1_5': 0.004}},
        'D256': {'parents': ['R01'], 'cpt': {'0_1': 0.006, '1_5': 0.001}},
        'D260': {'parents': ['R01'], 'cpt': {'0_1': 0.005, '1_5': 0.008, '6_12': 0.003}},
        'D261': {'parents': ['R01'], 'cpt': {'0_1': 0.005, '1_5': 0.008, '6_12': 0.003}},
        'D347': {'parents': ['R01'], 'cpt': {'0_1': 0.004, '1_5': 0.003}},
        'D348': {'parents': ['R01'], 'cpt': {'0_1': 0.002, '1_5': 0.005, '6_12': 0.001}},
        'D263': {'parents': ['R01'], 'cpt': {'6_12': 0.006, '13_17': 0.005, '18_39': 0.004, '40_64': 0.001}},
    },
    'autoimmune_sex': {
        'D202': {'parents': ['R02'], 'cpt': {'male': 0.0005, 'female': 0.004}},
        'D203': {'parents': ['R02'], 'cpt': {'male': 0.0005, 'female': 0.003}},
        'D59': {'parents': ['R02', 'R01'], 'cpt': {'female|18_39': 0.006, 'female|40_64': 0.003, 'male|18_39': 0.001, 'male|40_64': 0.0005}},
        'D171': {'parents': ['R02'], 'cpt': {'male': 0.001, 'female': 0.003}},
        'D43': {'parents': ['R02'], 'cpt': {'male': 0.003, 'female': 0.0}},
        'D147': {'parents': ['R02', 'R01'], 'cpt': {'male|6_12': 0.004, 'male|13_17': 0.008, 'male|18_39': 0.003, 'female|6_12': 0.0, 'female|13_17': 0.0, 'female|18_39': 0.0}},
    },
    'neuro_age': {
        'D138': {'parents': ['R01'], 'cpt': {'40_64': 0.004, '65_plus': 0.010}},
        'D139': {'parents': ['R01'], 'cpt': {'40_64': 0.003, '65_plus': 0.008}},
        'D164': {'parents': ['R02', 'R01'], 'cpt': {'male|65_plus': 0.006, 'male|40_64': 0.002, 'female|65_plus': 0.003, 'female|40_64': 0.001}},
        'D294': {'parents': ['R02', 'R01'], 'cpt': {'female|18_39': 0.008, 'female|40_64': 0.004, 'male|18_39': 0.003, 'male|40_64': 0.001}},
        'D142': {'parents': ['R01'], 'cpt': {'0_1': 0.004, '1_5': 0.003, '6_12': 0.002, '18_39': 0.002, '65_plus': 0.004}},
        'D302': {'parents': ['R01'], 'cpt': {'40_64': 0.002, '65_plus': 0.004}},
        'D303': {'parents': ['R01'], 'cpt': {'40_64': 0.003, '65_plus': 0.008}},
        'D304': {'parents': ['R02', 'R01'], 'cpt': {'male|65_plus': 0.005, 'male|40_64': 0.001, 'female|65_plus': 0.003, 'female|40_64': 0.0005}},
        'D84': {'parents': ['R01'], 'cpt': {'0_1': 0.003, '1_5': 0.002, '40_64': 0.002, '65_plus': 0.003}},
    },
    'cardio_cancer': {
        'D131': {'parents': ['R02', 'R01'], 'cpt': {'male|40_64': 0.006, 'male|65_plus': 0.010, 'female|40_64': 0.002, 'female|65_plus': 0.005}},
        'D132': {'parents': ['R02', 'R01'], 'cpt': {'male|40_64': 0.003, 'male|65_plus': 0.005, 'female|40_64': 0.001, 'female|65_plus': 0.002}},
        'D327': {'parents': ['R01'], 'cpt': {'40_64': 0.002, '65_plus': 0.008}},
        'D174': {'parents': ['R02', 'R01'], 'cpt': {'male|65_plus': 0.005, 'male|40_64': 0.002, 'female|65_plus': 0.002, 'female|40_64': 0.0005}},
        'D277': {'parents': ['R01'], 'cpt': {'40_64': 0.004, '65_plus': 0.008}},
        'D230': {'parents': ['R01'], 'cpt': {'40_64': 0.003, '65_plus': 0.006}},
        'D231': {'parents': ['R01'], 'cpt': {'40_64': 0.002, '65_plus': 0.005}},
        'D311': {'parents': ['R02', 'R01'], 'cpt': {'male|40_64': 0.003, 'male|65_plus': 0.002, 'female|40_64': 0.002, 'female|65_plus': 0.001}},
        'D313': {'parents': ['R01'], 'cpt': {'40_64': 0.003, '65_plus': 0.005}},
    },
}


def run_test_with_group(diseases):
    s2 = copy.deepcopy(s2_orig)
    s3 = copy.deepcopy(s3_orig)
    rp = s3.setdefault('root_priors', {})
    edge_set = {(e['from'], e['to']) for e in s2['edges']}

    for did, data in diseases.items():
        desc = var_names.get(did, did)
        rp[did] = {'parents': data['parents'], 'description': desc, 'cpt': data['cpt']}
        for rid in data['parents']:
            if (rid, did) not in edge_set:
                s2['edges'].append({
                    'from': rid, 'to': did,
                    'from_name': var_names.get(rid, ''),
                    'to_name': desc, 'reason': desc, 'onset_day_range': None
                })
                edge_set.add((rid, did))

    with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
        json.dump(s2, f, ensure_ascii=False, indent=2)
    with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
        json.dump(s3, f, ensure_ascii=False, indent=2)

    result = subprocess.run(
        ['python3', 'bn_inference.py'],
        capture_output=True, text=True, encoding='utf-8'
    )
    m = re.search(
        r'Top-1: (\d+)/\d+ \(\d+%\) \| Top-3: (\d+)/\d+ \(\d+%\) \| Confident misdiag: (\d+)',
        result.stdout
    )
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None, None, None


print('Baseline: Top1=556, Top3=661, FATAL=0')
print()

for gname, diseases in groups.items():
    t1, t3, fatal = run_test_with_group(diseases)
    if t1 is not None:
        d1 = t1 - 556
        d3 = t3 - 661
        print(f'{gname:20s} ({len(diseases):2d}): T1={t1}({d1:+d}) T3={t3}({d3:+d}) F={fatal}')
    else:
        print(f'{gname:20s}: FAILED')

# Restore original
with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2_orig, f, ensure_ascii=False, indent=2)
with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3_orig, f, ensure_ascii=False, indent=2)
print('\nRestored original files.')
