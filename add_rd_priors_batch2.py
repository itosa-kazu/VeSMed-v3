#!/usr/bin/env python3
"""Batch 2: Add R→D risk factor priors for 33 more diseases."""
import json

with open('step2_fever_edges_v4.json', encoding='utf-8') as f:
    s2 = json.load(f)
with open('step3_fever_cpts_v2.json', encoding='utf-8') as f:
    s3 = json.load(f)
with open('step1_fever_v2.7.json', encoding='utf-8') as f:
    s1 = json.load(f)

var_names = {v['id']: v.get('name_ja', v.get('name', '')) for v in s1['variables']}
rp = s3.get('root_priors', {})
edge_set = {(e['from'], e['to']) for e in s2['edges']}

batch2 = {
    # Cancer
    'D277': {'parents': ['R01'], 'description': '肺腺癌。中高年に好発',
             'cpt': {'40_64': 0.004, '65_plus': 0.008}},
    'D230': {'parents': ['R01'], 'description': '膵癌。60-70歳に好発',
             'cpt': {'40_64': 0.003, '65_plus': 0.006}},
    'D231': {'parents': ['R01'], 'description': '胆管癌。高齢者に好発',
             'cpt': {'40_64': 0.002, '65_plus': 0.005}},
    'D311': {'parents': ['R02', 'R01'], 'description': '膠芽腫。男性やや多い、50-60歳にピーク',
             'cpt': {'male|40_64': 0.003, 'male|65_plus': 0.002,
                     'female|40_64': 0.002, 'female|65_plus': 0.001}},
    'D313': {'parents': ['R01'], 'description': '転移性脳腫瘍。中高年に好発',
             'cpt': {'40_64': 0.003, '65_plus': 0.005}},
    # Neurological
    'D138': {'parents': ['R01'], 'description': '急性脳梗塞。高齢者に好発',
             'cpt': {'40_64': 0.004, '65_plus': 0.010}},
    'D139': {'parents': ['R01'], 'description': '脳出血。高齢者に好発',
             'cpt': {'40_64': 0.003, '65_plus': 0.008}},
    'D164': {'parents': ['R02', 'R01'], 'description': '慢性硬膜下血腫。高齢男性に好発',
             'cpt': {'male|65_plus': 0.006, 'male|40_64': 0.002,
                     'female|65_plus': 0.003, 'female|40_64': 0.001}},
    'D294': {'parents': ['R02', 'R01'], 'description': '片頭痛。若年女性に好発（女性3:1）',
             'cpt': {'female|18_39': 0.008, 'female|40_64': 0.004,
                     'male|18_39': 0.003, 'male|40_64': 0.001}},
    'D142': {'parents': ['R01'], 'description': 'てんかん重積。小児と高齢者に二峰性',
             'cpt': {'0_1': 0.004, '1_5': 0.003, '6_12': 0.002, '18_39': 0.002, '65_plus': 0.004}},
    'D302': {'parents': ['R01'], 'description': '進行性核上性麻痺。60歳代に好発',
             'cpt': {'40_64': 0.002, '65_plus': 0.004}},
    'D303': {'parents': ['R01'], 'description': 'パーキンソン病。60歳以上に好発',
             'cpt': {'40_64': 0.003, '65_plus': 0.008}},
    'D304': {'parents': ['R02', 'R01'], 'description': 'レビー小体型認知症。高齢男性に好発',
             'cpt': {'male|65_plus': 0.005, 'male|40_64': 0.001,
                     'female|65_plus': 0.003, 'female|40_64': 0.0005}},
    # Cardiovascular
    'D131': {'parents': ['R02', 'R01'], 'description': '急性冠症候群。男性・高齢者に好発',
             'cpt': {'male|40_64': 0.006, 'male|65_plus': 0.010,
                     'female|40_64': 0.002, 'female|65_plus': 0.005}},
    'D132': {'parents': ['R02', 'R01'], 'description': '急性大動脈解離。男性・高齢者に好発',
             'cpt': {'male|40_64': 0.003, 'male|65_plus': 0.005,
                     'female|40_64': 0.001, 'female|65_plus': 0.002}},
    'D327': {'parents': ['R01'], 'description': '大動脈弁狭窄症。高齢者に好発',
             'cpt': {'40_64': 0.002, '65_plus': 0.008}},
    'D174': {'parents': ['R02', 'R01'], 'description': '腹部大動脈瘤破裂。高齢男性に好発',
             'cpt': {'male|65_plus': 0.005, 'male|40_64': 0.002,
                     'female|65_plus': 0.002, 'female|40_64': 0.0005}},
    # Pediatric
    'D253': {'parents': ['R01'], 'description': '急性細気管支炎。2歳未満に好発',
             'cpt': {'0_1': 0.010, '1_5': 0.003}},
    'D258': {'parents': ['R01'], 'description': 'RSウイルス感染症。乳幼児に好発',
             'cpt': {'0_1': 0.010, '1_5': 0.005}},
    'D338': {'parents': ['R01'], 'description': '腸重積。生後6ヶ月-3歳に好発',
             'cpt': {'0_1': 0.008, '1_5': 0.004}},
    'D256': {'parents': ['R01'], 'description': '腸回転異常。新生児期に好発',
             'cpt': {'0_1': 0.006, '1_5': 0.001}},
    'D260': {'parents': ['R01'], 'description': 'ヘルパンギーナ。小児に好発',
             'cpt': {'0_1': 0.005, '1_5': 0.008, '6_12': 0.003}},
    'D261': {'parents': ['R01'], 'description': '手足口病。小児に好発',
             'cpt': {'0_1': 0.005, '1_5': 0.008, '6_12': 0.003}},
    'D347': {'parents': ['R01'], 'description': '神経芽腫。5歳未満の小児に好発',
             'cpt': {'0_1': 0.004, '1_5': 0.003}},
    'D348': {'parents': ['R01'], 'description': 'ウィルムス腫瘍。2-5歳に好発',
             'cpt': {'0_1': 0.002, '1_5': 0.005, '6_12': 0.001}},
    # Autoimmune
    'D202': {'parents': ['R02'], 'description': 'シェーグレン症候群。女性に圧倒的に多い（女性9:1）',
             'cpt': {'male': 0.0005, 'female': 0.004}},
    'D203': {'parents': ['R02'], 'description': '全身性強皮症。女性に多い（女性5:1）',
             'cpt': {'male': 0.0005, 'female': 0.003}},
    'D59': {'parents': ['R02', 'R01'], 'description': 'SLE。若年女性に好発（女性9:1）',
            'cpt': {'female|18_39': 0.006, 'female|40_64': 0.003,
                    'male|18_39': 0.001, 'male|40_64': 0.0005}},
    'D171': {'parents': ['R02'], 'description': '抗リン脂質抗体症候群。女性に多い',
             'cpt': {'male': 0.001, 'female': 0.003}},
    # Infection
    'D263': {'parents': ['R01'], 'description': 'マイコプラズマ肺炎。小児-若年成人に好発',
             'cpt': {'6_12': 0.006, '13_17': 0.005, '18_39': 0.004, '40_64': 0.001}},
    'D84': {'parents': ['R01'], 'description': '単純ヘルペス脳炎。乳幼児と50歳以上に二峰性',
            'cpt': {'0_1': 0.003, '1_5': 0.002, '40_64': 0.002, '65_plus': 0.003}},
    'D43': {'parents': ['R02'], 'description': '精巣上体炎。男性のみ',
            'cpt': {'male': 0.003, 'female': 0.0}},
    'D147': {'parents': ['R02', 'R01'], 'description': '精巣捻転。10-25歳の男性に好発',
             'cpt': {'male|6_12': 0.004, 'male|13_17': 0.008, 'male|18_39': 0.003,
                     'female|6_12': 0.0, 'female|13_17': 0.0, 'female|18_39': 0.0}},
}

added_p = 0
added_e = 0
for did, prior_data in batch2.items():
    if did not in rp:
        rp[did] = prior_data
        added_p += 1
    for rid in prior_data['parents']:
        if (rid, did) not in edge_set:
            s2['edges'].append({
                'from': rid, 'to': did,
                'from_name': var_names.get(rid, rid),
                'to_name': var_names.get(did, did),
                'reason': prior_data['description'],
                'onset_day_range': None
            })
            edge_set.add((rid, did))
            added_e += 1

print(f'Batch 2: Added {added_p} priors, {added_e} edges')
print(f'Total edges: {len(s2["edges"])}')
print(f'Total diseases with R->D prior: {sum(1 for k in rp if k.startswith("D"))}')

with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
