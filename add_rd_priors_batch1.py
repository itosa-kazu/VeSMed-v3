#!/usr/bin/env python3
"""Batch 1: Add R->D risk factor priors for worst-performing diseases + pregnancy diseases."""
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

batch1 = {
    # Worst performing diseases (batch 1)
    'D276': {'parents': ['R02'], 'description': '卵巣捻転。女性のみ',
             'cpt': {'male': 0.0, 'female': 0.003}},
    'D288': {'parents': ['R02', 'R01'], 'description': '精巣腫瘍。20-34歳男性に好発',
             'cpt': {'male|18_39': 0.004, 'male|40_64': 0.001, 'male|65_plus': 0.0005,
                     'female|18_39': 0.0, 'female|40_64': 0.0, 'female|65_plus': 0.0}},
    'D289': {'parents': ['R02', 'R01'], 'description': '前立腺癌。65歳以上の男性に好発',
             'cpt': {'male|40_64': 0.002, 'male|65_plus': 0.008,
                     'female|40_64': 0.0, 'female|65_plus': 0.0}},
    'D290': {'parents': ['R02', 'R01'], 'description': '膀胱癌。男性・高齢者に好発',
             'cpt': {'male|40_64': 0.002, 'male|65_plus': 0.006,
                     'female|40_64': 0.001, 'female|65_plus': 0.002}},
    'D291': {'parents': ['R02', 'R01'], 'description': '子宮外妊娠。妊娠可能年齢の女性',
             'cpt': {'female|18_39': 0.005, 'female|40_64': 0.001,
                     'male|18_39': 0.0, 'male|40_64': 0.0}},
    'D295': {'parents': ['R02', 'R01'], 'description': '群発頭痛。20-40歳男性に好発（男女比6:1）',
             'cpt': {'male|18_39': 0.005, 'male|40_64': 0.003,
                     'female|18_39': 0.001, 'female|40_64': 0.0005}},
    'D301': {'parents': ['R02', 'R01'], 'description': 'NMOSD。30-50歳女性に好発（女性9:1）',
             'cpt': {'female|18_39': 0.004, 'female|40_64': 0.003,
                     'male|18_39': 0.0005, 'male|40_64': 0.0003}},
    'D341': {'parents': ['R02'], 'description': 'Brugada症候群。男性に圧倒的に多い（男女比8:1）',
             'cpt': {'male': 0.003, 'female': 0.0004}},
    'D345': {'parents': ['R02'], 'description': 'Sheehan症候群。分娩後の女性のみ',
             'cpt': {'male': 0.0, 'female': 0.002}},
    'D337': {'parents': ['R01'], 'description': '肥厚性幽門狭窄症。生後2-8週に発症',
             'cpt': {'0_1': 0.01, '1_5': 0.0005}},
    'D312': {'parents': ['R02', 'R01'], 'description': '髄膜腫。中高年女性に好発',
             'cpt': {'female|40_64': 0.004, 'female|65_plus': 0.005,
                     'male|40_64': 0.002, 'male|65_plus': 0.003}},
    'D320': {'parents': ['R02', 'R01'], 'description': '喉頭癌。男性・高齢者・喫煙者に好発',
             'cpt': {'male|40_64': 0.002, 'male|65_plus': 0.005,
                     'female|40_64': 0.0003, 'female|65_plus': 0.001}},
    'D287': {'parents': ['R02', 'R01'], 'description': '胆嚢癌。高齢女性に好発',
             'cpt': {'female|40_64': 0.002, 'female|65_plus': 0.005,
                     'male|40_64': 0.001, 'male|65_plus': 0.003}},
    'D278': {'parents': ['R02', 'R01'], 'description': '悪性胸膜中皮腫。男性・高齢者に好発',
             'cpt': {'male|40_64': 0.001, 'male|65_plus': 0.004,
                     'female|40_64': 0.0003, 'female|65_plus': 0.001}},
    'D340': {'parents': ['R02'], 'description': '僧帽弁狭窄症。リウマチ熱後遺症、女性に多い',
             'cpt': {'male': 0.001, 'female': 0.003}},
    'D335': {'parents': ['R02', 'R01'], 'description': '閉塞性動脈硬化症。男性・高齢・糖尿病に好発',
             'cpt': {'male|40_64': 0.003, 'male|65_plus': 0.008,
                     'female|40_64': 0.001, 'female|65_plus': 0.003}},
    'D155': {'parents': ['R01'], 'description': 'くも膜下出血。40-60歳にピーク',
             'cpt': {'18_39': 0.002, '40_64': 0.005, '65_plus': 0.004}},
    'D94': {'parents': ['R02', 'R01'], 'description': 'IgG4関連疾患。60歳代男性に好発',
            'cpt': {'male|40_64': 0.003, 'male|65_plus': 0.005,
                    'female|40_64': 0.001, 'female|65_plus': 0.002}},
    # Pregnancy diseases (to balance D291)
    'D323': {'parents': ['R02', 'R01'], 'description': '常位胎盤早期剥離。妊娠後期の女性',
             'cpt': {'female|18_39': 0.004, 'female|40_64': 0.002,
                     'male|18_39': 0.0, 'male|40_64': 0.0}},
    'D322': {'parents': ['R02', 'R01'], 'description': 'HELLP症候群。妊娠後期の女性',
             'cpt': {'female|18_39': 0.004, 'female|40_64': 0.002,
                     'male|18_39': 0.0, 'male|40_64': 0.0}},
    'D325': {'parents': ['R02', 'R01'], 'description': 'PRES。妊娠高血圧・自己免疫で好発',
             'cpt': {'female|18_39': 0.003, 'female|40_64': 0.002,
                     'male|18_39': 0.001, 'male|40_64': 0.001}},
}

added_p = 0
added_e = 0
for did, prior_data in batch1.items():
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

print(f'Batch 1: Added {added_p} priors, {added_e} edges')
print(f'Total edges: {len(s2["edges"])}')

with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
