"""
D409 急性中耳炎 (Acute Otitis Media, AOM) 追加スクリプト
Step 0 文献: StatPearls NBK470332, PMC3010420, PMC9422693, AAFP 2007, AAP 2013
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D409"
DNAME = "acute_otitis_media"
DNAME_JA = "急性中耳炎"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "ENT",
    "states": ["absent","present"], "severity": "mild",
    "note": "中耳の急性細菌感染。小児主体(6-24ヶ月ピーク)、成人稀。耳痛+鼓膜膨隆+伝音性難聴。URI先行~75%。発熱~66%"
})
print(f"Added {DID} to step1")

# ── Step 2: Edges (11 edges) ──
FROM = DID
FROM_NAME = DNAME_JA

new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"S79","to_name":"耳痛",
     "reason":"AOM: 耳痛(成人80%+, 小児50-60%, AAFP 2007, LR+ 3.0-7.3)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S124","to_name":"難聴",
     "reason":"AOM: 伝音性難聴(聴力検査90%異常, 25-44dB, PMC9422693)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S140","to_name":"難聴の種類",
     "reason":"AOM: 伝音性難聴(中耳腔貯留液, 定義的)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S125","to_name":"耳鳴",
     "reason":"AOM: 耳鳴は稀(中耳貯留で軽度可能, 推定15%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"AOM: 発熱~66%、通常low-grade(StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S03","to_name":"鼻汁",
     "reason":"AOM: 先行URI rhinorrhea ~75%(AAFP 2007, Sens 75%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S02","to_name":"咽頭痛",
     "reason":"AOM: 併発URI咽頭痛(推定30%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S01","to_name":"咳嗽",
     "reason":"AOM: 併発URI咳嗽(推定35%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S13","to_name":"悪心",
     "reason":"AOM: 悪心(小児で多い、成人推定15%)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"AOM: 急性(数日で受診)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"AOM: 急性発症(URI後に急性耳痛)"},
]

s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3: CPTs ──
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "AOM。6-24ヶ月ピーク。小児年間60-80/1000、成人2.5/1000。M>F軽度",
    "cpt": {
        "male|0_1":     0.05,
        "male|1_5":     0.03,
        "male|6_12":    0.01,
        "male|13_17":   0.005,
        "male|18_39":   0.002,
        "male|40_64":   0.001,
        "male|65_plus": 0.001,
        "female|0_1":     0.04,
        "female|1_5":     0.025,
        "female|6_12":    0.008,
        "female|13_17":   0.004,
        "female|18_39":   0.002,
        "female|40_64":   0.001,
        "female|65_plus": 0.001,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "AOM年齢分布。乳幼児中心(StatPearls)",
        "cpt": {
            "0_1":     0.35,
            "1_5":     0.25,
            "6_12":    0.18,
            "13_17":   0.08,
            "18_39":   0.06,
            "40_64":   0.05,
            "65_plus": 0.03
        }
    },
    "R02": {
        "description": "AOM性別。M>F軽度(StatPearls)",
        "cpt": {"male": 0.53, "female": 0.47}
    }
}

nop = s3['noisy_or_params']

# S79 (otalgia): present 0.80 (adults)
nop['S79']['parent_effects'][DID] = {"absent": 0.20, "present": 0.80}

# S124 (hearing_loss): present 0.70 (conductive, clinically noticed)
nop['S124']['parent_effects'][DID] = {"absent": 0.30, "present": 0.70}

# S140 (hearing_loss_type): conductive 0.88 (middle ear effusion)
nop['S140']['parent_effects'][DID] = {"conductive": 0.88, "sensorineural": 0.05, "mixed": 0.07}

# S125 (tinnitus): present 0.15 (uncommon in AOM)
nop['S125']['parent_effects'][DID] = {"absent": 0.85, "present": 0.15}

# E01 (fever): ~66% low-grade
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.002,
    "under_37.5": 0.34,
    "37.5_38.0": 0.40,
    "38.0_39.0": 0.20,
    "39.0_40.0": 0.05,
    "over_40.0": 0.008
}

# S03 (rhinorrhea): present 0.60 (concurrent URI ~75%)
nop['S03']['parent_effects'][DID] = {"absent": 0.40, "present": 0.60}

# S02 (sore_throat): present 0.30 (concurrent URI)
nop['S02']['parent_effects'][DID] = {"absent": 0.70, "present": 0.30}

# S01 (cough): present 0.35
nop['S01']['parent_effects'][DID] = {"absent": 0.65, "present": 0.35}

# S13 (nausea): present 0.15
nop['S13']['parent_effects'][DID] = {"absent": 0.85, "present": 0.15}

# T01: acute (days)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.40,
    "3d_to_1w": 0.40,
    "1w_to_3w": 0.15,
    "over_3w": 0.05
}

# T02: acute
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.10,
    "acute": 0.60,
    "subacute": 0.25,
    "chronic": 0.05
}

print(f"Added CPTs. S140 parents: {len(nop['S140']['parent_effects'])}")

# ── Save ──
for fname, data in [
    ('step1_fever_v2.7.json', s1),
    ('step2_fever_edges_v4.json', s2),
    ('step3_fever_cpts_v2.json', s3),
]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved all 3 files.")
