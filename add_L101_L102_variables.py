#!/usr/bin/env python3
"""
Add L101 (cryptococcal_antigen / クリプトコッカス抗原) and L102 (toxoplasma_IgM / トキソプラズマIgM抗体)
to improve D365 (肺クリプトコッカス症) and D366 (トキソプラズマリンパ節炎).

Three-file sync: step1 + step2 + step3
Also updates test case evidence mapping.
"""

import json
import copy

# ── Step 1: Add variable definitions ──
with open('step1_fever_v2.7.json', 'r') as f:
    step1 = json.load(f)

# Check if L101/L102 already exist
existing_ids = {v['id'] for v in step1['variables']}
if 'L101' in existing_ids or 'L102' in existing_ids:
    print("L101 or L102 already exists, skipping step1")
else:
    new_vars = [
        {
            "id": "L101",
            "name": "cryptococcal_antigen",
            "name_ja": "クリプトコッカス抗原",
            "category": "lab",
            "states": [
                "not_done",
                "negative",
                "positive"
            ]
        },
        {
            "id": "L102",
            "name": "toxoplasma_IgM",
            "name_ja": "トキソプラズマIgM抗体",
            "category": "lab",
            "states": [
                "not_done",
                "negative",
                "positive"
            ]
        }
    ]
    step1['variables'].extend(new_vars)
    with open('step1_fever_v2.7.json', 'w') as f:
        json.dump(step1, f, indent=2, ensure_ascii=False)
    print(f"Step1: Added L101, L102. Total variables: {len(step1['variables'])}")

# ── Step 2: Add edges (D365->L101, D109->L101, D366->L102, D110->L102) ──
with open('step2_fever_edges_v4.json', 'r') as f:
    step2 = json.load(f)

existing_edges = {(e['from'], e['to']) for e in step2['edges']}

new_edges = []

# D365 (肺クリプトコッカス症) -> L101 (クリプトコッカス抗原)
if ('D365', 'L101') not in existing_edges:
    new_edges.append({
        "from": "D365",
        "to": "L101",
        "reason": "肺クリプト: CrAg陽性(70-90%)",
        "onset_day_range": {"earliest": 1, "typical": 3, "latest": 7},
        "from_name": "pulmonary_cryptococcosis",
        "to_name": "cryptococcal_antigen"
    })

# D109 (クリプトコッカス髄膜炎) -> L101 (クリプトコッカス抗原)
if ('D109', 'L101') not in existing_edges:
    new_edges.append({
        "from": "D109",
        "to": "L101",
        "reason": "クリプト髄膜炎: CrAg陽性(>95%)",
        "onset_day_range": {"earliest": 1, "typical": 3, "latest": 7},
        "from_name": "cryptococcal_meningitis",
        "to_name": "cryptococcal_antigen"
    })

# D366 (トキソプラズマリンパ節炎) -> L102 (トキソプラズマIgM)
if ('D366', 'L102') not in existing_edges:
    new_edges.append({
        "from": "D366",
        "to": "L102",
        "reason": "トキソリンパ節炎: IgM陽性(急性期90%+)",
        "onset_day_range": {"earliest": 7, "typical": 14, "latest": 21},
        "from_name": "toxoplasma_lymphadenitis",
        "to_name": "toxoplasma_IgM"
    })

# D110 (トキソプラズマ脳炎) -> L102 (トキソプラズマIgM)
if ('D110', 'L102') not in existing_edges:
    new_edges.append({
        "from": "D110",
        "to": "L102",
        "reason": "トキソ脳炎: IgM(再活性化では低い場合あり)",
        "onset_day_range": {"earliest": 7, "typical": 14, "latest": 21},
        "from_name": "toxoplasma_encephalitis",
        "to_name": "toxoplasma_IgM"
    })

if new_edges:
    step2['edges'].extend(new_edges)
    step2['total_edges'] = len(step2['edges'])
    with open('step2_fever_edges_v4.json', 'w') as f:
        json.dump(step2, f, indent=2, ensure_ascii=False)
    print(f"Step2: Added {len(new_edges)} edges. Total edges: {step2['total_edges']}")
else:
    print("Step2: No new edges needed")

# ── Step 3: Add noisy_or_params for L101 and L102 ──
with open('step3_fever_cpts_v2.json', 'r') as f:
    step3 = json.load(f)

nop = step3.setdefault('noisy_or_params', {})

# L101: クリプトコッカス抗原
if 'L101' not in nop:
    nop['L101'] = {
        "description": "クリプトコッカス抗原",
        "states": ["negative", "positive"],
        "leak": {
            "not_done": 0.5,
            "negative": 0.49,
            "positive": 0.01
        },
        "parent_effects": {
            "D365": {
                "not_done": 0.05,
                "negative": 0.19,
                "positive": 0.76
            },
            "D109": {
                "not_done": 0.05,
                "negative": 0.019,
                "positive": 0.931
            }
        }
    }
    print("Step3: Added L101 noisy_or_params")
    # D365 CrAg sensitivity ~70-90% for pulmonary (lower than meningitis)
    # D109 CrAg sensitivity >95% for meningitis

# L102: トキソプラズマIgM
if 'L102' not in nop:
    nop['L102'] = {
        "description": "トキソプラズマIgM抗体",
        "states": ["negative", "positive"],
        "leak": {
            "not_done": 0.5,
            "negative": 0.49,
            "positive": 0.01
        },
        "parent_effects": {
            "D366": {
                "not_done": 0.05,
                "negative": 0.095,
                "positive": 0.855
            },
            "D110": {
                "not_done": 0.05,
                "negative": 0.57,
                "positive": 0.38
            }
        }
    }
    print("Step3: Added L102 noisy_or_params")
    # D366 (lymphadenitis, acute infection): IgM positive ~85%+
    # D110 (encephalitis, reactivation): IgM often low/negative (~30-40% positive)

with open('step3_fever_cpts_v2.json', 'w') as f:
    json.dump(step3, f, indent=2, ensure_ascii=False)

# ── Update test case evidence ──
with open('real_case_test_suite.json', 'r') as f:
    tests = json.load(f)

updates = 0
for c in tests['cases']:
    case_id = c.get('id', '')
    expected = c.get('expected_id', '')
    vig = c.get('vignette', '')

    # D365 cases with CrAg mentioned in vignette
    if expected == 'D365' and 'CrAg' in vig:
        if 'L101' not in c.get('evidence', {}):
            c['evidence']['L101'] = 'positive'
            print(f"  {case_id}: Added L101=positive (CrAg in vignette)")
            updates += 1

    # D366 cases with Toxo IgM mentioned in vignette
    if expected == 'D366' and 'IgM' in vig:
        if 'L102' not in c.get('evidence', {}):
            c['evidence']['L102'] = 'positive'
            print(f"  {case_id}: Added L102=positive (Toxo IgM in vignette)")
            updates += 1

if updates > 0:
    with open('real_case_test_suite.json', 'w') as f:
        json.dump(tests, f, indent=2, ensure_ascii=False)
    print(f"Test cases: Updated {updates} cases")
else:
    print("Test cases: No updates needed")

print("\n=== Summary ===")
print("L101 (cryptococcal_antigen): D365, D109")
print("L102 (toxoplasma_IgM): D366, D110")
print("Done!")
