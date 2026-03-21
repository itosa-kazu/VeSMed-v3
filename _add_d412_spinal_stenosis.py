"""
D412 脊柱管狭窄症 (Lumbar Spinal Stenosis, LSS) 追加スクリプト
Step 0: StatPearls NBK430872, PMC7101166, PMC7595829, PMC4017306, PMC10447202
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D412"
DNAME = "lumbar_spinal_stenosis"
DNAME_JA = "腰部脊柱管狭窄症"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "orthopedic",
    "states": ["absent","present"], "severity": "moderate",
    "note": "腰椎の変性狭窄→神経性間欠性跛行。歩行/立位で下肢痛+しびれ、前屈/座位で軽快。50-70歳。PAD鑑別重要(ABI)"
})
print(f"Added {DID} to step1")

# ── Step 2 (12 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"S56","to_name":"間欠性跛行",
     "reason":"LSS: 神経性間欠性跛行(hallmark, ~80-90%, PMC7101166)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S111","to_name":"腰痛",
     "reason":"LSS: 腰痛(65-90%, PMC7595829)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S22","to_name":"背部痛",
     "reason":"LSS: 背部痛(腰部中心, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S106","to_name":"歩行障害",
     "reason":"LSS: 歩行障害(claudication + 不安定歩行, PMC7101166)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S137","to_name":"歩行障害のパターン",
     "reason":"LSS: 疼痛性跛行(antalgic gait, 前傾姿勢, PMC4017306)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S76","to_name":"感覚障害のパターン",
     "reason":"LSS: 神経根型=dermatomal, 馬尾型=saddle(PMC7101166)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E53","to_name":"深部腱反射",
     "reason":"LSS: 腱反射低下(下位運動ニューロン障害, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S48","to_name":"近位筋力低下",
     "reason":"LSS: 下肢筋力低下(重症例30-50%, PMC7595829)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E41","to_name":"ABI",
     "reason":"LSS: ABI正常(PADとの鑑別, PMC3513595)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"LSS: 非感染性変性疾患、発熱なし"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"LSS: 慢性進行性(数ヶ月~数年で受診)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"LSS: 緩徐進行性"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "LSS。50-70歳ピーク。M>F(1.5:1)。有病率: 画像11-38%, 症候性~8%",
    "cpt": {
        "male|0_1":     0.00001,
        "male|1_5":     0.00001,
        "male|6_12":    0.00005,
        "male|13_17":   0.0001,
        "male|18_39":   0.0005,
        "male|40_64":   0.004,
        "male|65_plus": 0.008,
        "female|0_1":     0.00001,
        "female|1_5":     0.00001,
        "female|6_12":    0.00005,
        "female|13_17":   0.0001,
        "female|18_39":   0.0003,
        "female|40_64":   0.003,
        "female|65_plus": 0.006,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "LSS年齢。50-70歳ピーク、高齢者に多い",
        "cpt": {
            "0_1":0.001, "1_5":0.001, "6_12":0.002, "13_17":0.005,
            "18_39":0.05, "40_64":0.35, "65_plus":0.591
        }
    },
    "R02": {
        "description": "LSS性別。M:F≈1.5:1",
        "cpt": {"male": 0.60, "female": 0.40}
    }
}

nop = s3['noisy_or_params']

# S56: intermittent claudication 0.85
nop['S56']['parent_effects'][DID] = {"absent": 0.15, "present": 0.85}

# S111: low back pain 0.65
nop['S111']['parent_effects'][DID] = {"absent": 0.35, "present": 0.65}

# S22: back pain 0.70
nop['S22']['parent_effects'][DID] = {"absent": 0.30, "present": 0.70}

# S106: gait disturbance 0.60
nop['S106']['parent_effects'][DID] = {"absent": 0.40, "present": 0.60}

# S137: gait pattern - antalgic 0.55 (pain-limited, forward leaning)
nop['S137']['parent_effects'][DID] = {
    "ataxic": 0.10, "shuffling": 0.05, "steppage": 0.10,
    "spastic": 0.05, "waddling": 0.05, "antalgic": 0.65
}

# S76: sensory disturbance - dermatomal 0.45, saddle 0.08
nop['S76']['parent_effects'][DID] = {
    "stocking_glove": 0.10, "ascending": 0.05,
    "dermatomal": 0.45, "hemisensory": 0.02, "saddle": 0.38
}

# E53: DTR hyporeflexia 0.40
nop['E53']['parent_effects'][DID] = {
    "normal": 0.45, "areflexia": 0.05, "hyporeflexia": 0.40,
    "hyperreflexia": 0.10
}

# S48: proximal weakness 0.30
nop['S48']['parent_effects'][DID] = {"absent": 0.70, "present": 0.30}

# E41: ABI normal (differentiates from PAD)
nop['E41']['parent_effects'][DID] = {"normal_over_0.9": 0.92, "low_under_0.9": 0.08}

# E01: no fever
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.004, "under_37.5": 0.92,
    "37.5_38.0": 0.05, "38.0_39.0": 0.02,
    "39.0_40.0": 0.005, "over_40.0": 0.001
}

# T01: chronic
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.02, "3d_to_1w": 0.03,
    "1w_to_3w": 0.10, "over_3w": 0.85
}

# T02: chronic
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.02, "acute": 0.03,
    "subacute": 0.15, "chronic": 0.80
}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
