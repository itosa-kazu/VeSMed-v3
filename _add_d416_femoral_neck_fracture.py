"""
D416 大腿骨頸部骨折 (Femoral Neck Fracture) 追加スクリプト
Step 0: StatPearls NBK537347/NBK557514, PMC8580199, PMC7482680, PMC7155350, AAFP 2022
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D416"
DNAME = "femoral_neck_fracture"
DNAME_JA = "大腿骨頸部骨折"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "orthopedic",
    "states": ["absent","present"], "severity": "high",
    "note": "大腿骨頸部骨折。高齢女性の低エネルギー転倒が90%以上。股関節痛+荷重不能+下肢短縮外旋が三徴。平均年齢80歳、F:M=2.9:1。Garden分類(I-IV)。displaced(72%)は人工骨頭、non-displaced(28%)は骨接合。せん妄13-33%。1年死亡率~30%"
})
print(f"Added {DID} to step1")

# ── Step 2 (12 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"S28","to_name":"股関節/鼠径部痛",
     "reason":"大腿骨頸部骨折: 股関節/鼠径部痛(95-100%, cardinal symptom, StatPearls NBK537347/AAFP 2022)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S08","to_name":"関節痛",
     "reason":"大腿骨頸部骨折: 関節痛(股関節は関節, ~95%, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S48","to_name":"近位筋力低下",
     "reason":"大腿骨頸部骨折: 荷重不能/起立不能(sensitivity 88.5%, PMC8580199)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S106","to_name":"歩行障害",
     "reason":"大腿骨頸部骨折: 歩行不能(displaced fracture ~88%, PMC8580199)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S137","to_name":"歩行障害のパターン",
     "reason":"大腿骨頸部骨折: antalgic gait=疼痛回避歩行(non-displaced/不全骨折, PMC4017306)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S06","to_name":"筋肉痛",
     "reason":"大腿骨頸部骨折: 大腿部筋肉痛/鈍痛(~55%, 骨折周囲筋のスパズム, AAFP 2022)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S23","to_name":"関節腫脹",
     "reason":"大腿骨頸部骨折: 股関節腫脹(~25%, 被膜内骨折で腫脹軽度, PMC8580199 spec 96%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S39","to_name":"片側下肢腫脹",
     "reason":"大腿骨頸部骨折: 患側下肢腫脹(~20%, 軟部組織出血/浮腫, PMC8580199)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E16","to_name":"意識レベル",
     "reason":"大腿骨頸部骨折: せん妄(13.5-33%, 高齢+疼痛+入院, StatPearls NBK557514)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"大腿骨頸部骨折: 通常無熱(非感染性外傷, 術後発熱は合併症)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"大腿骨頸部骨折: 転倒後急性発症(数時間以内に受診, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"大腿骨頸部骨折: 突然発症(転倒の瞬間に骨折, StatPearls)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
# Root priors: elderly female predominant (PMC7482680: F:M=2.9:1, mean age 80)
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "大腿骨頸部骨折。年間発生率0.1-0.2%。>90%が65歳以上。F:M=2.9:1(PMC7482680)。低エネルギー転倒+骨粗鬆症",
    "cpt": {
        "male|0_1":     0.0,
        "male|1_5":     0.0,
        "male|6_12":    0.00005,
        "male|13_17":   0.0001,
        "male|18_39":   0.0005,
        "male|40_64":   0.002,
        "male|65_plus": 0.008,
        "female|0_1":     0.0,
        "female|1_5":     0.0,
        "female|6_12":    0.00005,
        "female|13_17":   0.0001,
        "female|18_39":   0.0004,
        "female|40_64":   0.003,
        "female|65_plus": 0.020,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "大腿骨頸部骨折年齢。>90%が65歳以上(PMC7482680, mean 80yo)",
        "cpt": {
            "0_1":0.0, "1_5":0.0, "6_12":0.001, "13_17":0.005,
            "18_39":0.03, "40_64":0.10, "65_plus":0.864
        }
    },
    "R02": {
        "description": "大腿骨頸部骨折性別。F:M=2.9:1(PMC7482680, 74%女性)",
        "cpt": {"male": 0.26, "female": 0.74}
    }
}

nop = s3['noisy_or_params']

# S28: hip/groin pain - cardinal symptom, ~95-100%
nop['S28']['parent_effects'][DID] = {"absent": 0.03, "present": 0.97}

# S08: arthralgia (hip is a joint) ~95%
nop['S08']['parent_effects'][DID] = {"absent": 0.05, "present": 0.95}

# S48: proximal weakness (inability to stand/walk, sens 88.5% PMC8580199)
nop['S48']['parent_effects'][DID] = {"absent": 0.15, "present": 0.85}

# S106: gait disturbance (~88% can't walk)
nop['S106']['parent_effects'][DID] = {"absent": 0.12, "present": 0.88}

# S137: gait pattern - antalgic (pain-avoidance gait, PMC4017306)
nop['S137']['parent_effects'][DID] = {
    "ataxic": 0.02, "shuffling": 0.01, "steppage": 0.01,
    "spastic": 0.01, "waddling": 0.01, "antalgic": 0.94
}

# S06: myalgia (thigh/hip muscle pain ~55%, AAFP 2022)
nop['S06']['parent_effects'][DID] = {"absent": 0.45, "present": 0.55}

# S23: joint swelling (~25%, intracapsular → less visible, PMC8580199)
nop['S23']['parent_effects'][DID] = {"absent": 0.75, "present": 0.25}

# S39: unilateral leg swelling (~20%, soft tissue hemorrhage, PMC8580199)
nop['S39']['parent_effects'][DID] = {"absent": 0.80, "present": 0.20}

# E16: consciousness - delirium 13-33% (elderly, StatPearls NBK557514)
nop['E16']['parent_effects'][DID] = {"normal": 0.75, "confused": 0.22, "obtunded": 0.03}

# E01: temperature - usually afebrile (non-infectious trauma)
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.01, "under_37.5": 0.85,
    "37.5_38.0": 0.08, "38.0_39.0": 0.04,
    "39.0_40.0": 0.015, "over_40.0": 0.005
}

# T01: symptom duration - acute (fall → immediate pain)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.85, "3d_to_1w": 0.10,
    "1w_to_3w": 0.04, "over_3w": 0.01
}

# T02: onset speed - sudden (instantaneous at fall)
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.85, "acute": 0.10,
    "subacute": 0.04, "chronic": 0.01
}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
