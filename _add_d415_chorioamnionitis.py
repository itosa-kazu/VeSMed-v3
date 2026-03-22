"""
D415 絨毛膜羊膜炎 (Chorioamnionitis / Intraamniotic Infection) 追加スクリプト
Step 0: PMC3008318, PMC10669668, PMC6891229, PMC7293113, StatPearls NBK532251
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D415"
DNAME = "chorioamnionitis"
DNAME_JA = "絨毛膜羊膜炎"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "obstetrics",
    "states": ["absent","present"], "severity": "high",
    "note": "羊膜腔内感染。母体発熱+頻脈+WBC増多+子宮圧痛/膿性帯下。全分娩1-4%、PROM後6-10%。Gibbs基準/Triple I基準。GBS/E.coli/嫌気性菌。緊急分娩+抗菌薬"
})
print(f"Added {DID} to step1")

# ── Step 2 (11 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"絨毛膜羊膜炎: 母体発熱(>38C, 診断必須条件, ~100%, PMC3008318/Gibbs基準)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E02","to_name":"心拍数",
     "reason":"絨毛膜羊膜炎: 母体頻脈(>100bpm, 50-80%, sens 88%, PMC3008318/PMC10669668)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L01","to_name":"白血球数",
     "reason":"絨毛膜羊膜炎: WBC>15000(62-73%, sens 76%, PMC3008318)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L02","to_name":"CRP",
     "reason":"絨毛膜羊膜炎: CRP上昇(sens 69%, spec 77%, meta-analysis PMC7293113)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S12","to_name":"腹痛",
     "reason":"絨毛膜羊膜炎: 子宮圧痛(4-25%, spec 95%, PMC3008318/PMC10669668)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S89","to_name":"腹痛の部位",
     "reason":"絨毛膜羊膜炎: 子宮圧痛→下腹部(恥骨上部)/びまん性(PMC3008318)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S128","to_name":"帯下(異常分泌物)",
     "reason":"絨毛膜羊膜炎: 膿性/悪臭帯下(5-22%, spec 95%, PMC3008318/PMC10669668)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S09","to_name":"悪寒戦慄",
     "reason":"絨毛膜羊膜炎: 悪寒(敗血症移行時, 約20-30%, PMC3008318)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"R15","to_name":"妊娠",
     "reason":"絨毛膜羊膜炎: 妊娠女性にのみ発症(100%, 定義上)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"絨毛膜羊膜炎: 急性(分娩中/破水後に発症, 時間〜日単位, PMC3008318)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"絨毛膜羊膜炎: 急性発症(分娩中/PROM後に急速進行, PMC3008318)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
# Root priors: female only, reproductive age (18-39 peak)
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "絨毛膜羊膜炎。全分娩1-4%。妊娠女性のみ。育龄(18-39)ピーク。初産・PROM・GBSリスク",
    "cpt": {
        "male|0_1":     0.0,
        "male|1_5":     0.0,
        "male|6_12":    0.0,
        "male|13_17":   0.0,
        "male|18_39":   0.0,
        "male|40_64":   0.0,
        "male|65_plus": 0.0,
        "female|0_1":     0.0,
        "female|1_5":     0.0,
        "female|6_12":    0.0,
        "female|13_17":   0.00005,
        "female|18_39":   0.0008,
        "female|40_64":   0.0002,
        "female|65_plus": 0.0,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "絨毛膜羊膜炎年齢。妊娠可能年齢のみ。18-39歳ピーク",
        "cpt": {
            "0_1":0.0, "1_5":0.0, "6_12":0.0, "13_17":0.03,
            "18_39":0.75, "40_64":0.22, "65_plus":0.0
        }
    },
    "R02": {
        "description": "絨毛膜羊膜炎性別。女性のみ(妊娠必須)",
        "cpt": {"male": 0.0, "female": 1.0}
    }
}

nop = s3['noisy_or_params']

# E01: fever - nearly 100% (diagnostic criterion)
# >38C always, often 38-39C range
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.001, "under_37.5": 0.02,
    "37.5_38.0": 0.07, "38.0_39.0": 0.55,
    "39.0_40.0": 0.30, "over_40.0": 0.059
}

# E02: maternal tachycardia 50-80%
nop['E02']['parent_effects'][DID] = {
    "under_100": 0.30, "100_120": 0.50, "over_120": 0.20
}

# L01: WBC >15000 (62-73%)
nop['L01']['parent_effects'][DID] = {
    "low_under_4000": 0.02, "normal_4000_10000": 0.10,
    "high_10000_20000": 0.55, "very_high_over_20000": 0.33
}

# L02: CRP elevated (sens 69%)
nop['L02']['parent_effects'][DID] = {
    "normal_under_0.3": 0.10, "mild_0.3_3": 0.20,
    "moderate_3_10": 0.35, "high_over_10": 0.35
}

# S12: abdominal pain (uterine tenderness, 4-25%)
nop['S12']['parent_effects'][DID] = {"absent": 0.80, "present": 0.20}

# S89: abdominal pain region - suprapubic (uterine) or diffuse
nop['S89']['parent_effects'][DID] = {
    "epigastric": 0.02, "RUQ": 0.02, "RLQ": 0.05,
    "LLQ": 0.05, "suprapubic": 0.56, "diffuse": 0.30
}

# S128: vaginal discharge (purulent/foul, 5-22%)
nop['S128']['parent_effects'][DID] = {"absent": 0.85, "present": 0.15}

# S09: rigors (~25%)
nop['S09']['parent_effects'][DID] = {"absent": 0.75, "present": 0.25}

# R15: pregnancy = yes (100%)
nop['R15']['parent_effects'][DID] = {"no": 0.01, "yes": 0.99}

# T01: acute (hours to 1-2 days)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.80, "3d_to_1w": 0.15,
    "1w_to_3w": 0.04, "over_3w": 0.01
}

# T02: acute onset
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.10, "acute": 0.70,
    "subacute": 0.15, "chronic": 0.05
}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
