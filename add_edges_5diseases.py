#!/usr/bin/env python3
"""Add literature-backed edges for D219/D220/D221/D222/D252."""
import json

with open('step2_fever_edges_v4.json', encoding='utf-8') as f:
    s2 = json.load(f)
with open('step3_fever_cpts_v2.json', encoding='utf-8') as f:
    s3 = json.load(f)
with open('step1_fever_v2.7.json', encoding='utf-8') as f:
    s1 = json.load(f)

var_names = {v['id']: v.get('name_ja', v.get('name', '')) for v in s1['variables']}
nop = s3.get('noisy_or_params', {})
edge_set = {(e['from'], e['to']) for e in s2['edges']}

added = 0
def add(did, vid, cpt, reason):
    global added
    if (did, vid) in edge_set or vid not in nop:
        return
    s2['edges'].append({'from': did, 'to': vid, 'from_name': var_names.get(did, ''),
                        'to_name': var_names.get(vid, ''), 'reason': reason, 'onset_day_range': None})
    edge_set.add((did, vid))
    nop[vid]['parent_effects'][did] = cpt
    added += 1

# D219 GPA (15->26)
add('D219', 'S05', {'absent': 0.40, 'present': 0.60}, 'GPA sinusitis-related headache (PMC8429614)')
add('D219', 'S20', {'absent': 0.50, 'present': 0.50}, 'GPA paranasal sinusitis facial pain (StatPearls)')
add('D219', 'S06', {'absent': 0.40, 'present': 0.60}, 'GPA myalgia common (PMC8006774)')
add('D219', 'S17', {'absent': 0.40, 'present': 0.60}, 'GPA weight loss (PMC8026843, PMC8006774)')
add('D219', 'S33', {'absent': 0.30, 'present': 0.70}, 'GPA glomerulonephritis hematuria ~70% (StatPearls)')
add('D219', 'L78', {'not_done': 0.1, 'negative': 0.2, 'mild': 0.4, 'nephrotic': 0.3}, 'GPA renal proteinuria (PMC8006774)')
add('D219', 'S34', {'absent': 0.60, 'present': 0.40}, 'GPA DAH hemoptysis ~40% (PMC8026843)')
add('D219', 'L28', {'normal': 0.05, 'mildly_elevated': 0.25, 'highly_elevated': 0.70}, 'GPA ESR markedly elevated (PMC8006774 ESR67, PMC11925717 ESR101)')
add('D219', 'S18', {'absent': 0.60, 'present': 0.40}, 'GPA purpura/rash ~40% (PMC11925717)')
add('D219', 'E12', {'normal': 0.50, 'localized_erythema': 0.10, 'vesicles_bullae': 0.05, 'petechiae_purpura': 0.25, 'diffuse_erythema': 0.10}, 'GPA purpura from vasculitis (PMC11925717)')
add('D219', 'S09', {'absent': 0.40, 'present': 0.60}, 'GPA febrile with chills (PMC11925717)')

# D220 EGPA (11->21)
add('D220', 'S08', {'absent': 0.40, 'present': 0.60}, 'EGPA polyarthritis (PMC11772266)')
add('D220', 'S06', {'absent': 0.50, 'present': 0.50}, 'EGPA myalgia (PMC4129332)')
add('D220', 'S17', {'absent': 0.50, 'present': 0.50}, 'EGPA weight loss systemic phase (PMC11772266)')
add('D220', 'S18', {'absent': 0.30, 'present': 0.70}, 'EGPA skin 50-70% (PMC5726678, PMC10403021)')
add('D220', 'L17', {'normal': 0.50, 'mildly_elevated': 0.30, 'highly_elevated': 0.20}, 'EGPA CK from myocarditis (PMC11772266 CK913)')
add('D220', 'L28', {'normal': 0.10, 'mildly_elevated': 0.40, 'highly_elevated': 0.50}, 'EGPA ESR elevated (PMC4129332 ESR70)')
add('D220', 'S52', {'absent': 0.40, 'present': 0.60}, 'EGPA mononeuritis multiplex ~60% (PMC4129332)')
add('D220', 'L11', {'normal': 0.50, 'mildly_elevated': 0.35, 'highly_elevated': 0.15}, 'EGPA hepatopathy (PMC10403021 ALT97)')
add('D220', 'S01', {'absent': 0.30, 'present': 0.70}, 'EGPA cough from asthma/infiltrates (PMC4129332)')
add('D220', 'E36', {'absent': 0.60, 'present': 0.40}, 'EGPA edema from heart failure (PMC11772266)')

# D221 MPA (13->23)
add('D221', 'S33', {'absent': 0.20, 'present': 0.80}, 'MPA glomerular hematuria ~80% (PMC4569227)')
add('D221', 'L78', {'not_done': 0.1, 'negative': 0.1, 'mild': 0.4, 'nephrotic': 0.4}, 'MPA proteinuria from RPGN (PMC7045917)')
add('D221', 'S34', {'absent': 0.50, 'present': 0.50}, 'MPA DAH hemoptysis ~50% (PMC4569227)')
add('D221', 'S17', {'absent': 0.40, 'present': 0.60}, 'MPA weight loss (PMC4569227 12lb/1mo)')
add('D221', 'S06', {'absent': 0.50, 'present': 0.50}, 'MPA myalgia/arthralgia (PMC9641526)')
add('D221', 'L28', {'normal': 0.05, 'mildly_elevated': 0.20, 'highly_elevated': 0.75}, 'MPA ESR markedly elevated (PMC10244548 ESR82, PMC7045917 ESR125)')
add('D221', 'L04', {'normal': 0.20, 'infiltrate': 0.50, 'bilateral_infiltrate': 0.20, 'cavity': 0.05, 'effusion': 0.05}, 'MPA bilateral infiltrates from DAH (PMC4569227)')
add('D221', 'E07', {'clear': 0.30, 'wheeze': 0.05, 'crackle': 0.55, 'rhonchi': 0.05, 'diminished': 0.05}, 'MPA bilateral crackles (PMC10244548, PMC7045917)')
add('D221', 'L11', {'normal': 0.60, 'mildly_elevated': 0.30, 'highly_elevated': 0.10}, 'MPA mild transaminase elevation (PMC9641526)')
add('D221', 'S09', {'absent': 0.50, 'present': 0.50}, 'MPA fever with chills (PMC4569227)')

# D222 RA (16->25)
add('D222', 'S06', {'absent': 0.40, 'present': 0.60}, 'RA myalgia in flares (PMC10721112)')
add('D222', 'S17', {'absent': 0.50, 'present': 0.50}, 'RA weight loss (PMC8112089)')
add('D222', 'S18', {'absent': 0.60, 'present': 0.40}, 'RA vasculitis purpuric lesions (PMC8112089)')
add('D222', 'E12', {'normal': 0.55, 'localized_erythema': 0.10, 'vesicles_bullae': 0.05, 'petechiae_purpura': 0.20, 'diffuse_erythema': 0.10}, 'RA vasculitis purpura (PMC8112089)')
add('D222', 'E14', {'absent': 0.80, 'present': 0.20}, 'RA Felty: splenomegaly (PMC8565701)')
add('D222', 'L14', {'normal': 0.60, 'leukocytosis': 0.10, 'left_shift': 0.05, 'eosinophilia': 0.05, 'lymphocytosis': 0.05, 'atypical_lymphocytes': 0.05, 'thrombocytopenia': 0.05, 'neutropenia': 0.05}, 'RA Felty: neutropenia (PMC8565701 ANC440)')
add('D222', 'L11', {'normal': 0.70, 'mildly_elevated': 0.25, 'highly_elevated': 0.05}, 'RA mild liver enzyme elevation (PMC11221493)')
add('D222', 'S04', {'absent': 0.70, 'present_exertional': 0.20, 'at_rest': 0.10}, 'RA pulmonary: ILD/pleuritis (PMC8112089)')
add('D222', 'E36', {'absent': 0.60, 'present': 0.40}, 'RA edema in vasculitis (PMC8112089)')

# D252 Kawasaki (15->25)
add('D252', 'E35', {'absent': 0.20, 'present': 0.80}, 'Kawasaki: conjunctivitis ~80% (PMC10025724)')
add('D252', 'E08', {'normal': 0.20, 'erythema': 0.30, 'exudate': 0.20, 'vesicle': 0.10, 'membrane': 0.20}, 'Kawasaki: oral changes ~80% (PMC10025724)')
add('D252', 'E13', {'absent': 0.30, 'present': 0.70}, 'Kawasaki: cervical LAD ~70% (PMC8009467)')
add('D252', 'E46', {'cervical': 0.85, 'axillary': 0.05, 'inguinal': 0.03, 'supraclavicular': 0.02, 'mediastinal': 0.02, 'generalized': 0.03}, 'Kawasaki: cervical LAD predominant (PMC8009467)')
add('D252', 'E36', {'absent': 0.40, 'present': 0.60}, 'Kawasaki: extremity edema ~60% (PMC10025724)')
add('D252', 'S18', {'absent': 0.15, 'present': 0.85}, 'Kawasaki: polymorphous rash ~85% (PMC10025724)')
add('D252', 'S46', {'absent': 0.30, 'present': 0.70}, 'Kawasaki: irritability/poor feeding (PMC5341178)')
add('D252', 'L44', {'normal': 0.60, 'hyponatremia': 0.30, 'hypernatremia': 0.05, 'hypokalemia': 0.03, 'hyperkalemia': 0.02}, 'Kawasaki: hyponatremia ~30% (PMC10336680)')
add('D252', 'S05', {'absent': 0.50, 'present': 0.50}, 'Kawasaki: headache in older children (PMC3370327)')
add('D252', 'S02', {'absent': 0.40, 'present': 0.60}, 'Kawasaki: sore throat (PMC3370327)')

print(f'Added {added} edges')
print(f'Total edges: {len(s2["edges"])}')

with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print('Saved.')
