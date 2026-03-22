"""
D419 コクシジオイデス症 (Coccidioidomycosis / Valley Fever) 追加スクリプト
Step 0: PMC3294516, PMC3373055, PMC2681119, PMC3702223, PMC4631225, StatPearls NBK448161
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D419"
DNAME = "coccidioidomycosis"
DNAME_JA = "コクシジオイデス症"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "infectious",
    "states": ["absent","present"], "severity": "high",
    "note": "コクシジオイデス症(Valley Fever)。Coccidioides immitis/posadasii。60%無症状、40%有症状(肺炎様)。倦怠感(80%)+咳(67%)+呼吸困難(60%)+発熱(55%)+胸痛(50%)。好酸球増多(25-30%)が特徴。CXR浸潤影75%。米国南西部/メキシコ/中南米流行地。潜伏期7-21日。自然治癒>90%。播種性1-3%"
})
print(f"Added {DID} to step1")

# ── Step 2 (12 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"コクシジオイデス症: 発熱(50-60%, PMC3294516 54%, PMC3373055 56%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S01","to_name":"咳嗽",
     "reason":"コクシジオイデス症: 咳嗽(65-70%, PMC3294516 67%, PMC3373055 69%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S04","to_name":"呼吸困難",
     "reason":"コクシジオイデス症: 呼吸困難(55-65%, PMC3294516 59%, PMC3373055 63%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S15","to_name":"胸痛",
     "reason":"コクシジオイデス症: 胸膜性胸痛(45-55%, EID2018 53%, PMC3373055 56%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S07","to_name":"全身倦怠感",
     "reason":"コクシジオイデス症: 倦怠感(75-85%, PMC3294516 84%, EID2018 62%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S06","to_name":"筋肉痛",
     "reason":"コクシジオイデス症: 筋肉痛(30-50%, EID2018 31%, PMC3373055 69%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S08","to_name":"関節痛",
     "reason":"コクシジオイデス症: 関節痛/desert rheumatism(30-45%, EID2018 36%, PMC3373055 44%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S16","to_name":"盗汗",
     "reason":"コクシジオイデス症: 盗汗(35-55%, PMC3373055 56%, PMC2681119 33%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L14","to_name":"末梢血液像",
     "reason":"コクシジオイデス症: 好酸球増多(25-30%, 鑑別のKEY, StatPearls/PMC2681119 mean AEC 2.96)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L04","to_name":"胸部X線",
     "reason":"コクシジオイデス症: CXR浸潤影75%(83%片側, 20%BHL, 10-15%胸水, Radiopaedia/EMCrit)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"コクシジオイデス症: 亜急性~慢性(中央値38-120日, PMC3294516/EID2018)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"コクシジオイデス症: 亜急性(潜伏期7-21日後に発症, CDC/StatPearls)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
# Root priors: male predominance (63%), peak 40-65yo (PMC3702223)
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "コクシジオイデス症。M:F=1.9:1(PMC3702223)。40-65歳ピーク。流行地渡航歴必須。日本では極めて稀(輸入症例のみ)",
    "cpt": {
        "male|0_1":     0.0,
        "male|1_5":     0.00001,
        "male|6_12":    0.00002,
        "male|13_17":   0.00005,
        "male|18_39":   0.001,
        "male|40_64":   0.002,
        "male|65_plus": 0.001,
        "female|0_1":     0.0,
        "female|1_5":     0.00001,
        "female|6_12":    0.00002,
        "female|13_17":   0.00003,
        "female|18_39":   0.0005,
        "female|40_64":   0.001,
        "female|65_plus": 0.0005,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "コクシジオイデス症年齢。40-65歳ピーク(PMC3702223 CA peak 40-49, AZ peak 65+)",
        "cpt": {
            "0_1":0.005, "1_5":0.01, "6_12":0.02, "13_17":0.03,
            "18_39":0.25, "40_64":0.42, "65_plus":0.265
        }
    },
    "R02": {
        "description": "コクシジオイデス症性別。M:F=1.9:1(PMC3702223, 63%男性)",
        "cpt": {"male": 0.63, "female": 0.37}
    }
}

nop = s3['noisy_or_params']

# E01: fever (50-60%, moderate grade)
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.01, "under_37.5": 0.42,
    "37.5_38.0": 0.20, "38.0_39.0": 0.25,
    "39.0_40.0": 0.10, "over_40.0": 0.02
}

# S01: cough (65-70%, dry > productive)
nop['S01']['parent_effects'][DID] = {"absent": 0.33, "present": 0.67}

# S04: dyspnea (55-65%)
nop['S04']['parent_effects'][DID] = {"absent": 0.40, "present": 0.60}

# S15: chest pain (pleuritic, 45-55%)
nop['S15']['parent_effects'][DID] = {"absent": 0.50, "present": 0.50}

# S07: fatigue (75-85%, prominent symptom)
nop['S07']['parent_effects'][DID] = {"absent": 0.20, "mild": 0.40, "severe": 0.40}

# S06: myalgia (30-50%)
nop['S06']['parent_effects'][DID] = {"absent": 0.60, "present": 0.40}

# S08: arthralgia (30-45%, "desert rheumatism")
nop['S08']['parent_effects'][DID] = {"absent": 0.63, "present": 0.37}

# S16: night sweats (35-55%)
nop['S16']['parent_effects'][DID] = {"absent": 0.55, "present": 0.45}

# L14: peripheral blood smear - eosinophilia is KEY differentiator (25-30%)
nop['L14']['parent_effects'][DID] = {
    "normal": 0.50, "left_shift": 0.10,
    "atypical_lymphocytes": 0.03, "thrombocytopenia": 0.02,
    "eosinophilia": 0.27, "lymphocyte_predominant": 0.08
}

# L04: CXR - lobar infiltrate most common (75%, 83% unilateral)
nop['L04']['parent_effects'][DID] = {
    "normal": 0.10, "lobar_infiltrate": 0.55,
    "bilateral_infiltrate": 0.10, "BHL": 0.12,
    "pleural_effusion": 0.10, "pneumothorax": 0.03
}

# T01: subacute to chronic (median 38-120 days)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.03, "3d_to_1w": 0.10,
    "1w_to_3w": 0.35, "over_3w": 0.52
}

# T02: subacute onset (incubation 7-21 days then gradual)
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.03, "acute": 0.15,
    "subacute": 0.55, "chronic": 0.27
}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
