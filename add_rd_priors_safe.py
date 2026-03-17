#!/usr/bin/env python3
"""Add only safe R->D priors (autoimmune_sex + neuro_age groups)."""
import json

with open('step2_fever_edges_v4.json', encoding='utf-8') as f:
    s2 = json.load(f)
with open('step3_fever_cpts_v2.json', encoding='utf-8') as f:
    s3 = json.load(f)
with open('step1_fever_v2.7.json', encoding='utf-8') as f:
    s1 = json.load(f)

var_names = {v['id']: v.get('name_ja', v.get('name', '')) for v in s1['variables']}
rp = s3.setdefault('root_priors', {})
edge_set = {(e['from'], e['to']) for e in s2['edges']}

safe_diseases = {
    # autoimmune_sex
    'D202': {'parents': ['R02'], 'description': 'シェーグレン症候群。女性9:1',
             'cpt': {'male': 0.0005, 'female': 0.004}},
    'D203': {'parents': ['R02'], 'description': '全身性強皮症。女性5:1',
             'cpt': {'male': 0.0005, 'female': 0.003}},
    'D59': {'parents': ['R02', 'R01'], 'description': 'SLE。若年女性9:1',
            'cpt': {'female|18_39': 0.006, 'female|40_64': 0.003,
                    'male|18_39': 0.001, 'male|40_64': 0.0005}},
    'D171': {'parents': ['R02'], 'description': '抗リン脂質抗体症候群。女性に多い',
             'cpt': {'male': 0.001, 'female': 0.003}},
    'D43': {'parents': ['R02'], 'description': '精巣上体炎。男性のみ',
            'cpt': {'male': 0.003, 'female': 0.0}},
    'D147': {'parents': ['R02', 'R01'], 'description': '精巣捻転。10-25歳男性',
             'cpt': {'male|6_12': 0.004, 'male|13_17': 0.008, 'male|18_39': 0.003,
                     'female|6_12': 0.0, 'female|13_17': 0.0, 'female|18_39': 0.0}},
    # neuro_age
    'D138': {'parents': ['R01'], 'description': '急性脳梗塞。高齢者に好発',
             'cpt': {'40_64': 0.004, '65_plus': 0.010}},
    'D139': {'parents': ['R01'], 'description': '脳出血。高齢者に好発',
             'cpt': {'40_64': 0.003, '65_plus': 0.008}},
    'D164': {'parents': ['R02', 'R01'], 'description': '慢性硬膜下血腫。高齢男性',
             'cpt': {'male|65_plus': 0.006, 'male|40_64': 0.002,
                     'female|65_plus': 0.003, 'female|40_64': 0.001}},
    'D294': {'parents': ['R02', 'R01'], 'description': '片頭痛。若年女性3:1',
             'cpt': {'female|18_39': 0.008, 'female|40_64': 0.004,
                     'male|18_39': 0.003, 'male|40_64': 0.001}},
    'D142': {'parents': ['R01'], 'description': 'てんかん重積。小児と高齢者に二峰性',
             'cpt': {'0_1': 0.004, '1_5': 0.003, '6_12': 0.002, '18_39': 0.002, '65_plus': 0.004}},
    'D302': {'parents': ['R01'], 'description': '進行性核上性麻痺。60歳代',
             'cpt': {'40_64': 0.002, '65_plus': 0.004}},
    'D303': {'parents': ['R01'], 'description': 'パーキンソン病。60歳以上',
             'cpt': {'40_64': 0.003, '65_plus': 0.008}},
    'D304': {'parents': ['R02', 'R01'], 'description': 'レビー小体型認知症。高齢男性',
             'cpt': {'male|65_plus': 0.005, 'male|40_64': 0.001,
                     'female|65_plus': 0.003, 'female|40_64': 0.0005}},
    'D84': {'parents': ['R01'], 'description': '単純ヘルペス脳炎。乳幼児と50歳以上',
            'cpt': {'0_1': 0.003, '1_5': 0.002, '40_64': 0.002, '65_plus': 0.003}},
}

added_p = 0
added_e = 0
for did, data in safe_diseases.items():
    if did not in rp:
        rp[did] = data
        added_p += 1
    for rid in data['parents']:
        if (rid, did) not in edge_set:
            s2['edges'].append({
                'from': rid, 'to': did,
                'from_name': var_names.get(rid, rid),
                'to_name': var_names.get(did, did),
                'reason': data['description'],
                'onset_day_range': None
            })
            edge_set.add((rid, did))
            added_e += 1

print(f'Safe batch: Added {added_p} priors, {added_e} edges')
print(f'Total edges: {len(s2["edges"])}')

with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
