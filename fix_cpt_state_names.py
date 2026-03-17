#!/usr/bin/env python3
"""Fix all CPT state name mismatches between step3 and step1."""
import json

with open('step1_fever_v2.7.json', encoding='utf-8') as f:
    s1 = json.load(f)
with open('step3_fever_cpts_v2.json', encoding='utf-8') as f:
    s3 = json.load(f)

var_map = {v['id']: v for v in s1['variables']}
nop = s3.get('noisy_or_params', {})

# Build rename maps per variable based on known patterns
RENAME_MAPS = {
    'E02': {'normal_60_100': 'under_100', 'bradycardia_under_60': 'under_100'},
    'E03': {'normal': 'normal_over_90', 'hypotension': 'hypotension_under_90'},
    'E04': {'normal': 'normal_under_20', 'mildly_elevated': 'tachypnea_20_30', 'tachypnea': 'tachypnea_20_30'},
    'E07': {'wheeze': 'wheezes', 'crackle': 'crackles', 'rhonchi': 'crackles', 'diminished': 'decreased_absent'},
    'E08': {'exudate': 'exudate_or_white_patch', 'vesicle': 'erythema', 'membrane': 'exudate_or_white_patch'},
    'E09': {
        'normal': 'soft_nontender', 'diffuse_tenderness': 'localized_tenderness',
        'RUQ_tenderness': 'localized_tenderness', 'RLQ_tenderness': 'localized_tenderness',
        'LLQ_tenderness': 'localized_tenderness', 'rebound_guarding': 'peritoneal_signs',
        'murphy_positive': 'localized_tenderness', 'CVA_tenderness': 'localized_tenderness',
        'suprapubic_tenderness': 'localized_tenderness', 'mass_palpable': 'localized_tenderness',
    },
    'E10': {'normal': 'negative', 'elevated': 'positive', 'markedly_elevated': 'positive'},
    'E12': {'absent': 'normal', 'vesicular': 'vesicular_dermatomal', 'erythroderma': 'diffuse_erythroderma'},
    'E15': {'systolic': 'new', 'diastolic': 'new', 'both': 'new'},
    'E16': {'alert': 'normal', 'coma': 'obtunded'},
    'L02': {
        'negative': 'normal_under_0.3', 'mildly_elevated': 'mild_0.3_3',
        'highly_elevated': 'high_over_10',
    },
    'L04': {'infiltrate': 'lobar_infiltrate', 'GGO': 'bilateral_infiltrate',
            'cavity': 'lobar_infiltrate', 'effusion': 'pleural_effusion'},
    'L14': {'leukocytosis': 'left_shift', 'lymphocytosis': 'lymphocyte_predominant', 'neutropenia': 'normal'},
    'L17': {'mildly_elevated': 'elevated', 'highly_elevated': 'very_high'},
    'L28': {'mildly_elevated': 'elevated', 'highly_elevated': 'very_high_over_100'},
    'L34': {'CD_positive': 'pathogen_detected'},
    'L44': {'hypernatremia': 'other', 'hypokalemia': 'other'},
    'L65': {'mild_NYHA1_2': 'mild_NYHA2'},
    'S04': {'exertional': 'on_exertion', 'present': 'on_exertion', 'present_exertional': 'on_exertion'},
    'S05': {'present': 'mild'},
    'S07': {'present': 'mild'},
    'S45': {'present': 'excessive', 'absent': 'normal'},
    'S47': {'under_3weeks': 'acute_under_3w', '3_to_8_weeks': 'subacute_3w_8w', 'over_8weeks': 'chronic_over_8w'},
    'T03': {'remittent': 'continuous', 'relapsing': 'periodic'},
    'E39': {'valvular': 'valvular_abnormal'},
    'E40': {'ST_change': 'ST_elevation', 'arrhythmia': 'AF', 'conduction_block': 'ST_depression'},
}

# Apply renames
total_fixed = 0
for vid, renames in RENAME_MAPS.items():
    if vid not in nop:
        continue
    params = nop[vid]

    # Fix leak
    leak = params.get('leak', {})
    if isinstance(leak, dict):
        for old, new in renames.items():
            if old in leak:
                val = leak.pop(old)
                if new in leak:
                    leak[new] = leak[new] + val  # merge
                else:
                    leak[new] = val
                total_fixed += 1

    # Fix parent_effects
    pe = params.get('parent_effects', {})
    for did, cpt in pe.items():
        if isinstance(cpt, dict):
            for old, new in renames.items():
                if old in cpt:
                    val = cpt.pop(old)
                    if new in cpt:
                        cpt[new] = cpt[new] + val  # merge
                    else:
                        cpt[new] = val
                    total_fixed += 1

print(f'Fixed {total_fixed} state name mismatches')

# Verify: re-check
errors = 0
for vid, params in nop.items():
    if vid not in var_map:
        continue
    valid_states = set(var_map[vid].get('states', []))
    if not valid_states:
        continue
    leak = params.get('leak', {})
    if isinstance(leak, dict):
        for state in leak:
            if state not in valid_states:
                print(f'  REMAINING: {vid} leak "{state}"')
                errors += 1
    pe = params.get('parent_effects', {})
    for did, cpt in pe.items():
        if isinstance(cpt, dict):
            for state in cpt:
                if state not in valid_states:
                    print(f'  REMAINING: {vid} <- {did} "{state}"')
                    errors += 1

print(f'Remaining errors: {errors}')

# Normalize: ensure all CPTs sum to ~1.0
normalized = 0
for vid, params in nop.items():
    pe = params.get('parent_effects', {})
    for did, cpt in pe.items():
        if isinstance(cpt, dict):
            total = sum(cpt.values())
            if total > 0 and abs(total - 1.0) > 0.01:
                for k in cpt:
                    cpt[k] = cpt[k] / total
                normalized += 1
    leak = params.get('leak', {})
    if isinstance(leak, dict):
        total = sum(leak.values())
        if total > 0 and abs(total - 1.0) > 0.01:
            for k in leak:
                leak[k] = leak[k] / total
            normalized += 1

print(f'Normalized {normalized} CPTs to sum=1.0')

with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print('Saved.')
