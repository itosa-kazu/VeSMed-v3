"""
D417 結核性腹膜炎 (Tuberculous Peritonitis) 追加スクリプト
Step 0: PMC6609850, PMC1378737, PMC11687449, PMC7035809, PMC10605989, PMC9980671
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D417"
DNAME = "tuberculous_peritonitis"
DNAME_JA = "結核性腹膜炎"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "infectious",
    "states": ["absent","present"], "severity": "high",
    "note": "結核性腹膜炎。腹水(90%)+発熱(65%)+腹痛(70%)+体重減少(60%)。亜急性~慢性経過。腹水ADA>30IU/L(sens90%+)。20-40歳ピーク、F:M=1.4:1。肺TB合併14-40%。全TBの2%、EPTB4.9%。HIV関連多い"
})
print(f"Added {DID} to step1")

# ── Step 2 (13 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"S12","to_name":"腹痛",
     "reason":"結核性腹膜炎: 腹痛(64-75%, PMC6609850 75%, PMC11687449 64.5%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S89","to_name":"腹痛の部位",
     "reason":"結核性腹膜炎: びまん性腹痛(腹膜全体の炎症, PMC6609850)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"結核性腹膜炎: 発熱(59-73%, 通常低~中等度, PMC6609850 69%, PMC11687449 59%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E28","to_name":"腹水",
     "reason":"結核性腹膜炎: 腹水(73-95%, PMC1378737 95.2%, PMC11687449 73%, PMC10605989 95.4%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S17","to_name":"体重減少",
     "reason":"結核性腹膜炎: 体重減少(53-93%, PMC6609850 53%, PMC11687449 61%, PMC10605989 93.2%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S07","to_name":"全身倦怠感",
     "reason":"結核性腹膜炎: 全身倦怠感(~45%, 全身性結核症状, PMC10439303)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S16","to_name":"盗汗",
     "reason":"結核性腹膜炎: 盗汗(6-54%, 典型的TB B症状, PMC7035809)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S46","to_name":"食欲不振",
     "reason":"結核性腹膜炎: 食欲不振(~47%, PMC1378737 46.9%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L02","to_name":"CRP",
     "reason":"結核性腹膜炎: CRP上昇(~90%, PMC9980671 CRP 34.46mg/L)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L01","to_name":"白血球数",
     "reason":"結核性腹膜炎: WBC通常正常~軽度上昇(PMC7035809, PMC10439303)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S14","to_name":"下痢",
     "reason":"結核性腹膜炎: 下痢(11-21%, PMC11687449, PMC10439303)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"結核性腹膜炎: 慢性(平均1.5ヶ月, 数週~数ヶ月, PMC1378737)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"結核性腹膜炎: 亜急性~慢性(緩徐進行性, PMC7035809)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
# Root priors: peak 20-40yo, F:M=1.4:1 (PMC7482680, PMC1378737)
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "結核性腹膜炎。全TBの2%。20-40歳ピーク(PMC1378737 median 31-35yo)。F:M=1.4:1(PMC11687449)。HIV関連。稀",
    "cpt": {
        "male|0_1":     0.0,
        "male|1_5":     0.00001,
        "male|6_12":    0.00002,
        "male|13_17":   0.00005,
        "male|18_39":   0.0003,
        "male|40_64":   0.0002,
        "male|65_plus": 0.0001,
        "female|0_1":     0.0,
        "female|1_5":     0.00001,
        "female|6_12":    0.00002,
        "female|13_17":   0.00005,
        "female|18_39":   0.0004,
        "female|40_64":   0.00025,
        "female|65_plus": 0.00015,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "結核性腹膜炎年齢。20-40歳ピーク(PMC1378737 median 31-35yo)",
        "cpt": {
            "0_1":0.005, "1_5":0.01, "6_12":0.02, "13_17":0.04,
            "18_39":0.50, "40_64":0.30, "65_plus":0.125
        }
    },
    "R02": {
        "description": "結核性腹膜炎性別。F:M=1.4:1(PMC11687449, 57-67%女性)",
        "cpt": {"male": 0.42, "female": 0.58}
    }
}

nop = s3['noisy_or_params']

# E01: fever (59-73%, usually low-grade 37.5-39C)
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.01, "under_37.5": 0.35,
    "37.5_38.0": 0.30, "38.0_39.0": 0.25,
    "39.0_40.0": 0.07, "over_40.0": 0.02
}

# S12: abdominal pain (64-75%)
nop['S12']['parent_effects'][DID] = {"absent": 0.30, "present": 0.70}

# S89: abdominal pain region - diffuse (peritoneal inflammation)
nop['S89']['parent_effects'][DID] = {
    "epigastric": 0.05, "RUQ": 0.05, "RLQ": 0.10,
    "LLQ": 0.05, "suprapubic": 0.05, "diffuse": 0.70
}

# E28: ascites (73-95%, hallmark finding)
nop['E28']['parent_effects'][DID] = {"absent": 0.10, "present": 0.90}

# S17: weight loss (53-93%)
nop['S17']['parent_effects'][DID] = {"absent": 0.40, "present": 0.60}

# S07: fatigue (~45%, mild-moderate)
nop['S07']['parent_effects'][DID] = {"absent": 0.55, "mild": 0.35, "severe": 0.10}

# S16: night sweats (6-54%, classic TB B-symptom)
nop['S16']['parent_effects'][DID] = {"absent": 0.70, "present": 0.30}

# S46: anorexia (~47%, PMC1378737)
nop['S46']['parent_effects'][DID] = {"absent": 0.55, "present": 0.45}

# L02: CRP elevated (~90%, moderate-high, PMC9980671 CRP 34.46mg/L = 3.4mg/dL)
nop['L02']['parent_effects'][DID] = {
    "normal_under_0.3": 0.08, "mild_0.3_3": 0.15,
    "moderate_3_10": 0.42, "high_over_10": 0.35
}

# L01: WBC usually normal or mild leukocytosis
nop['L01']['parent_effects'][DID] = {
    "low_under_4000": 0.03, "normal_4000_10000": 0.60,
    "high_10000_20000": 0.32, "very_high_over_20000": 0.05
}

# S14: diarrhea (11-21%)
nop['S14']['parent_effects'][DID] = {"absent": 0.85, "present": 0.15}

# T01: chronic (mean 1.5 months, weeks to months)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.03, "3d_to_1w": 0.07,
    "1w_to_3w": 0.30, "over_3w": 0.60
}

# T02: subacute to chronic onset
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.02, "acute": 0.08,
    "subacute": 0.55, "chronic": 0.35
}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
