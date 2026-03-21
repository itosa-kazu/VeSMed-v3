"""
D413 インスリノーマ (Insulinoma) 追加スクリプト
Step 0: PMC3498768, PMC3574879, PMC3470467, StatPearls NBK544299, Service 2009 (Mayo 237例)
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D413"
DNAME = "insulinoma"
DNAME_JA = "インスリノーマ"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "endocrine",
    "states": ["absent","present"], "severity": "moderate",
    "note": "膵β細胞腫瘍→内因性高インスリン血症→反復性低血糖。Whipple三徴(低血糖症状+血糖<55+ブドウ糖で改善)。90%良性/単発。40-60歳、F>M"
})
print(f"Added {DID} to step1")

# ── Step 2 (11 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"L54","to_name":"血糖",
     "reason":"インスリノーマ: 低血糖(defining feature, 72h絶食で99%検出, PMC3498768)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E16","to_name":"意識レベル",
     "reason":"インスリノーマ: 意識障害/混乱(neuroglycopenic, 75-80%, PMC3498768)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S45","to_name":"発汗異常",
     "reason":"インスリノーマ: 発汗過多(adrenergic response, 69%, PMC3498768)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S07","to_name":"倦怠感・疲労感",
     "reason":"インスリノーマ: 脱力/倦怠(56%, PMC3498768)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S42","to_name":"痙攣",
     "reason":"インスリノーマ: 痙攣(neuroglycopenic, 17-23%, PMC3498768/PMC3470467)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S36","to_name":"振戦",
     "reason":"インスリノーマ: 振戦(adrenergic, 24%, PMC3498768)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S35","to_name":"動悸",
     "reason":"インスリノーマ: 動悸(adrenergic, 12%, PMC3498768)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S120","to_name":"体重増加",
     "reason":"インスリノーマ: 体重増加(過食で低血糖予防, 14-50%, PMC3498768/PMC3470467)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"インスリノーマ: 非感染性腫瘍、発熱なし"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"インスリノーマ: 慢性再発性(数ヶ月~数年の反復発作で受診, Service 2009)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"インスリノーマ: 緩徐進行(個々の発作は急性だが全体経過は慢性, Service 2009)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
# Root priors: F>M (59:41), peak 40-60歳
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "インスリノーマ。1-4/百万人/年。F:M=59:41。40-60歳ピーク。90%良性単発",
    "cpt": {
        "male|0_1":     0.000001,
        "male|1_5":     0.000001,
        "male|6_12":    0.000005,
        "male|13_17":   0.00001,
        "male|18_39":   0.00005,
        "male|40_64":   0.00015,
        "male|65_plus": 0.00008,
        "female|0_1":     0.000001,
        "female|1_5":     0.000001,
        "female|6_12":    0.000005,
        "female|13_17":   0.00001,
        "female|18_39":   0.00006,
        "female|40_64":   0.0002,
        "female|65_plus": 0.00012,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "インスリノーマ年齢。40-60歳ピーク(Service 2009 Mayo 237例)",
        "cpt": {
            "0_1":0.001, "1_5":0.002, "6_12":0.005, "13_17":0.01,
            "18_39":0.15, "40_64":0.50, "65_plus":0.332
        }
    },
    "R02": {
        "description": "インスリノーマ性別。F:M=59:41(Service 2009)",
        "cpt": {"male": 0.41, "female": 0.59}
    }
}

nop = s3['noisy_or_params']

# L54: blood glucose - hypoglycemia ~100% (defining)
nop['L54']['parent_effects'][DID] = {
    "hypoglycemia": 0.95, "normal": 0.04,
    "hyperglycemia": 0.005, "very_high_over_500": 0.005
}

# E16: consciousness - confused 65%, obtunded 12%
nop['E16']['parent_effects'][DID] = {
    "normal": 0.23, "confused": 0.65, "obtunded": 0.12
}

# S45: sweating - excessive 69%
nop['S45']['parent_effects'][DID] = {
    "normal": 0.31, "excessive": 0.69, "absent": 0.00
}

# S07: fatigue/weakness 56%
nop['S07']['parent_effects'][DID] = {
    "absent": 0.44, "mild": 0.40, "severe": 0.16
}

# S42: seizure 20% (17-23%)
nop['S42']['parent_effects'][DID] = {"absent": 0.80, "present": 0.20}

# S36: tremor 24%
nop['S36']['parent_effects'][DID] = {"absent": 0.76, "present": 0.24}

# S35: palpitation 12%
nop['S35']['parent_effects'][DID] = {"absent": 0.88, "present": 0.12}

# S120: weight gain 30% (range 14-50%, midpoint)
nop['S120']['parent_effects'][DID] = {"absent": 0.70, "present": 0.30}

# E01: no fever (non-infectious)
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.005, "under_37.5": 0.95,
    "37.5_38.0": 0.03, "38.0_39.0": 0.01,
    "39.0_40.0": 0.003, "over_40.0": 0.002
}

# T01: chronic recurrent (months-years of episodes)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.03, "3d_to_1w": 0.02,
    "1w_to_3w": 0.10, "over_3w": 0.85
}

# T02: chronic course
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.05, "acute": 0.05,
    "subacute": 0.15, "chronic": 0.75
}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
