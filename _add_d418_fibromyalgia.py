"""
D418 線維筋痛症 (Fibromyalgia) 追加スクリプト
Step 0: StatPearls NBK540974, Endotext NBK279092, PMC3978642, PMC9847104, FPNotebook
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D418"
DNAME = "fibromyalgia"
DNAME_JA = "線維筋痛症"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "rheumatology",
    "states": ["absent","present"], "severity": "medium",
    "note": "線維筋痛症。広範な慢性疼痛+倦怠感+睡眠障害+認知障害。ACR2010基準(WPI+SS)。有病率2-4%。F:M=3:1。30-60歳ピーク。検査値正常(CRP/ESR/WBC)。PMR/SLE/RA/甲状腺機能低下との鑑別重要"
})
print(f"Added {DID} to step1")

# ── Step 2 (11 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"E94","to_name":"圧痛点(線維筋痛症)",
     "reason":"線維筋痛症: 圧痛点≥11/18(ACR1990基準, ~85%, Wolfe 1990 PMID 2306288)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S06","to_name":"筋肉痛",
     "reason":"線維筋痛症: 広範な筋骨格系疼痛(100%, 定義上必須, ACR criteria)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S08","to_name":"関節痛",
     "reason":"線維筋痛症: 関節痛/関節こわばり(~77%, FPNotebook)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S27","to_name":"朝のこわばり",
     "reason":"線維筋痛症: 朝のこわばり(77%, >15分, FPNotebook)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S07","to_name":"全身倦怠感",
     "reason":"線維筋痛症: 倦怠感(76-90%, moderate-severe, PMC3978642)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S05","to_name":"頭痛",
     "reason":"線維筋痛症: 再発性頭痛(53%, 緊張型+片頭痛, FPNotebook)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S12","to_name":"腹痛",
     "reason":"線維筋痛症: IBS合併(30-70%, 腹痛/腸管運動異常, FPNotebook)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S14","to_name":"下痢",
     "reason":"線維筋痛症: IBS関連下痢(~20%, FPNotebook)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"線維筋痛症: 非炎症性→通常無熱(PMR/SLE/RAとの鑑別点)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"線維筋痛症: 慢性(>3ヶ月が診断要件, ACR criteria)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"線維筋痛症: 緩徐進行性(数ヶ月~数年で発症, StatPearls)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
# Root priors: F:M=3:1, peak 30-60yo (PMC9847104, Endotext)
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "線維筋痛症。有病率2-4%。F:M=3:1(PMC9847104)。30-60歳ピーク。年齢と共に増加(2%@20yo→8%@70yo)",
    "cpt": {
        "male|0_1":     0.0,
        "male|1_5":     0.0,
        "male|6_12":    0.00005,
        "male|13_17":   0.0003,
        "male|18_39":   0.002,
        "male|40_64":   0.004,
        "male|65_plus": 0.002,
        "female|0_1":     0.0,
        "female|1_5":     0.0,
        "female|6_12":    0.0001,
        "female|13_17":   0.001,
        "female|18_39":   0.006,
        "female|40_64":   0.012,
        "female|65_plus": 0.006,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "線維筋痛症年齢。30-60歳ピーク(Endotext: 2%@20→8%@70)",
        "cpt": {
            "0_1":0.0, "1_5":0.0, "6_12":0.005, "13_17":0.04,
            "18_39":0.30, "40_64":0.45, "65_plus":0.205
        }
    },
    "R02": {
        "description": "線維筋痛症性別。F:M=3:1(PMC9847104, population studies)",
        "cpt": {"male": 0.25, "female": 0.75}
    }
}

nop = s3['noisy_or_params']

# === E94 NOP creation (new variable in NOP) ===
nop['E94'] = {
    "description": "圧痛点(線維筋痛症)",
    "states": ["absent","few_under_11","many_11_or_more"],
    "leak": {
        "absent": 0.95,
        "few_under_11": 0.04,
        "many_11_or_more": 0.01
    },
    "parent_effects": {
        DID: {
            "absent": 0.02,
            "few_under_11": 0.13,
            "many_11_or_more": 0.85
        }
    }
}

# S06: widespread pain (100%, defining criterion)
nop['S06']['parent_effects'][DID] = {"absent": 0.02, "present": 0.98}

# S08: arthralgia (77%, FPNotebook)
nop['S08']['parent_effects'][DID] = {"absent": 0.23, "present": 0.77}

# S27: morning stiffness (77%, FPNotebook)
nop['S27']['parent_effects'][DID] = {"absent": 0.23, "present": 0.77}

# S07: fatigue (76-90%, moderate-severe, PMC3978642)
nop['S07']['parent_effects'][DID] = {"absent": 0.15, "mild": 0.45, "severe": 0.40}

# S05: headache (53%, tension+migraine, FPNotebook)
nop['S05']['parent_effects'][DID] = {"absent": 0.47, "mild": 0.35, "severe": 0.18}

# S12: abdominal pain (IBS 30-70%, ~40%)
nop['S12']['parent_effects'][DID] = {"absent": 0.60, "present": 0.40}

# S14: diarrhea (IBS-related ~20%)
nop['S14']['parent_effects'][DID] = {"absent": 0.80, "present": 0.20}

# E01: temperature - afebrile (non-inflammatory condition)
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.005, "under_37.5": 0.95,
    "37.5_38.0": 0.03, "38.0_39.0": 0.01,
    "39.0_40.0": 0.003, "over_40.0": 0.002
}

# T01: chronic (>3 months by definition, ACR criteria)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.01, "3d_to_1w": 0.02,
    "1w_to_3w": 0.07, "over_3w": 0.90
}

# T02: chronic/insidious onset
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.02, "acute": 0.03,
    "subacute": 0.20, "chronic": 0.75
}

print(f"Added CPTs for {DID} (including E94 NOP creation)")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
