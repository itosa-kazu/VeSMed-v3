"""D431 食道カンジダ症 追加スクリプト"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Step 1: 変数追加
# ============================================================
with open('step1_fever_v2.7.json', 'r', encoding='utf-8') as f:
    s1 = json.load(f)

variables = s1['variables']

d431 = {
    "id": "D431",
    "name": "esophageal_candidiasis",
    "name_ja": "食道カンジダ症",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "moderate",
    "note": "免疫不全(HIV/ステロイド/DM)で嚥下困難+嚥下痛+口腔カンジダ。内視鏡で白苔。CD4<200でリスク増。年齢中央値55.5歳"
}

d430_idx = next(i for i, v in enumerate(variables) if v['id'] == 'D430')
variables.insert(d430_idx + 1, d431)

with open('step1_fever_v2.7.json', 'w', encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
print("Step 1: D431 added")

# ============================================================
# Step 2: 辺追加
# ============================================================
with open('step2_fever_edges_v4.json', 'r', encoding='utf-8') as f:
    s2 = json.load(f)

edges = s2['edges']

new_edges = [
    # D431 -> S25 嚥下困難: 70-80% (most common symptom, StatPearls)
    {
        "from": "D431", "to": "S25",
        "from_name": "食道カンジダ症", "to_name": "dysphagia",
        "reason": "食道カンジダ: 嚥下困難70-80%(StatPearls, most common symptom)",
        "onset_day_range": None
    },
    # D431 -> S78 嚥下痛: 50-70% (hallmark, StatPearls)
    {
        "from": "D431", "to": "S78",
        "from_name": "食道カンジダ症", "to_name": "odynophagia",
        "reason": "食道カンジダ: 嚥下痛50-70%(StatPearls 'hallmark of EC')",
        "onset_day_range": None
    },
    # D431 -> S101 嚥下困難の種類: solids_and_liquids (粘膜病変)
    {
        "from": "D431", "to": "S101",
        "from_name": "食道カンジダ症", "to_name": "dysphagia_type",
        "reason": "食道カンジダ: 粘膜病変で固形+液体嚥下困難(ScienceDirect)",
        "onset_day_range": None
    },
    # D431 -> S21 胸痛(retrosternal): 30-50%
    {
        "from": "D431", "to": "S21",
        "from_name": "食道カンジダ症", "to_name": "chest_pain",
        "reason": "食道カンジダ: 胸骨後部痛30-50%(StatPearls 'retrosternal pain')",
        "onset_day_range": None
    },
    # D431 -> E87 口腔カンジダ: 60-70% (1/3は無し)
    {
        "from": "D431", "to": "E87",
        "from_name": "食道カンジダ症", "to_name": "oral_candidiasis",
        "reason": "食道カンジダ: 口腔カンジダ併存60-70%(PMC3218701, 1/3は口腔所見なし)",
        "onset_day_range": None
    },
    # D431 -> S13 悪心: 20-30%
    {
        "from": "D431", "to": "S13",
        "from_name": "食道カンジダ症", "to_name": "nausea",
        "reason": "食道カンジダ: 悪心20-30%(PMC6854261 'other symptoms')",
        "onset_day_range": None
    },
    # D431 -> S17 体重減少: 20-30% (eating difficulty)
    {
        "from": "D431", "to": "S17",
        "from_name": "食道カンジダ症", "to_name": "weight_loss",
        "reason": "食道カンジダ: 体重減少20-30%(摂食困難による、PMC6854261)",
        "onset_day_range": None
    },
    # D431 -> E01 体温: 通常無熱~微熱
    {
        "from": "D431", "to": "E01",
        "from_name": "食道カンジダ症", "to_name": "temperature",
        "reason": "食道カンジダ: 通常無熱、重症例で微熱(StatPearls)",
        "onset_day_range": None
    },
    # D431 -> T02 発症速度: subacute (days to weeks)
    {
        "from": "D431", "to": "T02",
        "from_name": "食道カンジダ症", "to_name": "onset_speed",
        "reason": "食道カンジダ: 亜急性〜慢性発症(数日〜数週、StatPearls)",
        "onset_day_range": None
    },
    # D431 -> T01 症状持続期間: 1w-3w typical
    {
        "from": "D431", "to": "T01",
        "from_name": "食道カンジダ症", "to_name": "symptom_duration",
        "reason": "食道カンジダ: 通常1-3週で受診(PMC6854261)",
        "onset_day_range": None
    },
    # D431 -> S46 食欲不振: 嚥下困難による
    {
        "from": "D431", "to": "S46",
        "from_name": "食道カンジダ症", "to_name": "anorexia",
        "reason": "食道カンジダ: 食欲不振(嚥下困難・嚥下痛による摂食回避、PMC6854261)",
        "onset_day_range": None
    },
]

edges.extend(new_edges)
s2['total_edges'] = len(edges)

with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
print(f"Step 2: {len(new_edges)} edges added, total {len(edges)}")

# ============================================================
# Step 3: CPT追加
# ============================================================
with open('step3_fever_cpts_v2.json', 'r', encoding='utf-8') as f:
    s3 = json.load(f)

cpts = s3['full_cpts']
nop = s3['noisy_or_params']

# D431 disease CPT: parents=[R05(immunosuppressed)]
# 免疫不全で大幅にリスク上昇
cpts['D431'] = {
    "parents": ["R05"],
    "description": "食道カンジダ症。免疫不全で発症リスク大幅上昇",
    "cpt": {
        "no": 0.001,     # 免疫正常では非常に稀
        "yes": 0.015     # 免疫不全で10-15% lifetime risk (HIV/AIDS)
    },
    "R01": {
        "0_1": 0.001,
        "1_5": 0.001,
        "6_12": 0.001,
        "13_17": 0.002,
        "18_39": 0.004,
        "40_64": 0.005,  # median 55.5y
        "65_plus": 0.004
    },
    "R02": {
        "male": 0.5,    # 性差なし (StatPearls)
        "female": 0.5
    }
}

# S25: dysphagia 75%
if 'S25' in nop and 'parent_effects' in nop['S25']:
    nop['S25']['parent_effects']['D431'] = 0.75

# S78: odynophagia 60%
if 'S78' in nop and 'parent_effects' in nop['S78']:
    nop['S78']['parent_effects']['D431'] = 0.6

# S101: solids_and_liquids dominant
if 'S101' in nop and 'parent_effects' in nop['S101']:
    nop['S101']['parent_effects']['D431'] = {
        "solids_only": 0.2,
        "solids_and_liquids": 0.7,
        "liquids_worse": 0.1
    }

# S21: chest pain 40%
if 'S21' not in nop or not nop.get('S21') or 'parent_effects' not in nop.get('S21', {}):
    # S21 may not have noisy_or yet, check
    pass
s21_nop = nop.get('S21', {})
if s21_nop and 'parent_effects' in s21_nop:
    s21_nop['parent_effects']['D431'] = 0.4

# E87: oral candidiasis 65%
# E87 has no noisy_or yet, create it
nop['E87'] = {
    "description": "口腔カンジダ。1親",
    "states": ["absent", "present"],
    "leak": {"absent": 0.98, "present": 0.02},
    "parent_effects": {
        "D431": {
            "absent": 0.35,
            "present": 0.65
        }
    }
}

# S13: nausea 25%
if 'S13' in nop and 'parent_effects' in nop['S13']:
    nop['S13']['parent_effects']['D431'] = 0.25

# S17: weight loss 25%
if 'S17' not in nop or not nop.get('S17') or 'parent_effects' not in nop.get('S17', {}):
    pass
s17_nop = nop.get('S17', {})
if s17_nop and 'parent_effects' in s17_nop:
    s17_nop['parent_effects']['D431'] = 0.25

# E01: afebrile mostly
if 'E01' in nop and 'parent_effects' in nop['E01']:
    nop['E01']['parent_effects']['D431'] = {
        "under_37.5": 0.6,
        "37.5_38.0": 0.25,
        "38.0_39.0": 0.1,
        "39.0_40.0": 0.04,
        "over_40.0": 0.005,
        "hypothermia_under_35": 0.005
    }

# T02: subacute dominant
if 'T02' in nop and 'parent_effects' in nop['T02']:
    nop['T02']['parent_effects']['D431'] = {
        "sudden": 0.02,
        "acute": 0.15,
        "subacute": 0.55,
        "chronic": 0.28
    }

# T01: 1w-3w typical
if 'T01' in nop and 'parent_effects' in nop['T01']:
    nop['T01']['parent_effects']['D431'] = {
        "under_3d": 0.05,
        "3d_to_1w": 0.25,
        "1w_to_3w": 0.45,
        "over_3w": 0.25
    }

# S46: anorexia 40%
if 'S46' not in nop or not nop.get('S46') or 'parent_effects' not in nop.get('S46', {}):
    pass
s46_nop = nop.get('S46', {})
if s46_nop and 'parent_effects' in s46_nop:
    s46_nop['parent_effects']['D431'] = 0.4

with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print("Step 3: D431 CPTs added")
print("Done!")
