"""
D408 突発性難聴 (Sudden Sensorineural Hearing Loss, SSNHL) 追加スクリプト
Step 0 文献: PMC4040829, PMC7773829, PMC6221715, PMC9653771, PMC9587755, PMC10151530
"""
import json

# ── Load ──
s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D408"
DNAME = "sudden_sensorineural_hearing_loss"
DNAME_JA = "突発性難聴"

# ── Step 1: Disease definition ──
new_disease = {
    "id": DID,
    "name": DNAME,
    "name_ja": DNAME_JA,
    "category": "disease",
    "category_sub": "ENT",
    "states": ["absent","present"],
    "severity": "moderate",
    "note": "72時間以内に3連続周波数で≧30dBの感音性難聴。片側性>90%。耳鳴80-95%。めまい28-56%。41-55歳ピーク。M≒F"
}
s1['variables'].append(new_disease)
print(f"Added {DID} to step1")

# ── Step 2: Edges (12 edges) ──
FROM = DID
FROM_NAME = DNAME_JA

new_edges = [
    # 1. Hearing loss (by definition, >95%)
    {"from":FROM,"from_name":FROM_NAME,"to":"S124","to_name":"難聴",
     "reason":"SSNHL: 感音性難聴(定義的≧95%, PMC4040829)"},
    # 2. Hearing loss type: sensorineural
    {"from":FROM,"from_name":FROM_NAME,"to":"S140","to_name":"難聴の種類",
     "reason":"SSNHL: 感音性難聴(定義的, AAO-HNS 2019)"},
    # 3. Tinnitus (80-95%, PMC7773829)
    {"from":FROM,"from_name":FROM_NAME,"to":"S125","to_name":"耳鳴",
     "reason":"SSNHL: 耳鳴(80-95%, PMC7773829)"},
    # 4. Vertigo/dizziness (28-56%, PMC4040829)
    {"from":FROM,"from_name":FROM_NAME,"to":"S59","to_name":"めまい",
     "reason":"SSNHL: めまい(28-56%, PMC4040829)"},
    # 5. Vertigo quality: NOT episodic (differentiates from Meniere)
    {"from":FROM,"from_name":FROM_NAME,"to":"S92","to_name":"めまいの性状",
     "reason":"SSNHL: 非反復性めまい(continuous/non-rotatory, Meniere鑑別, PMC6221715)"},
    # 6. Aural fullness (32-70%, PMC7773829)
    {"from":FROM,"from_name":FROM_NAME,"to":"S79","to_name":"耳痛",
     "reason":"SSNHL: 耳閉感(32-70%, PMC7773829, S79代理)"},
    # 7. Nausea (accompanies vertigo, ~20%)
    {"from":FROM,"from_name":FROM_NAME,"to":"S13","to_name":"悪心",
     "reason":"SSNHL: 悪心(めまい随伴, 推定20-30%)"},
    # 8. Nystagmus: horizontal (in those with vertigo, 72-100%, PMC6221715)
    {"from":FROM,"from_name":FROM_NAME,"to":"E62","to_name":"眼振",
     "reason":"SSNHL: 水平性眼振(めまい合併例72-100%, PMC6221715, 全体~35%)"},
    # 9. Fever: absent
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"SSNHL: 非感染性、発熱なし(特発性90%)"},
    # 10. Symptom duration: acute (≤72h by definition)
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"SSNHL: 72時間以内発症(定義的)。多くは数日以内に受診"},
    # 11. Onset tempo: sudden (many notice upon waking)
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"SSNHL: 突然発症(多くは朝起床時に気づく, NIDCD)"},
    # 12. Vomiting (less common than nausea)
    {"from":FROM,"from_name":FROM_NAME,"to":"S66","to_name":"嘔吐",
     "reason":"SSNHL: 嘔吐(めまい随伴時、推定10-15%)"},
]

s2['edges'].extend(new_edges)
# Update declared count
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges to step2. Total: {len(s2['edges'])}")

# ── Step 3: CPTs ──

# --- Root prior ---
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "SSNHL。41-55歳ピーク。M:F≈1:1。年間発症率5-27/100,000(PMC9653771)",
    "cpt": {
        "male|0_1":     0.00001,
        "male|1_5":     0.00002,
        "male|6_12":    0.0001,
        "male|13_17":   0.0003,
        "male|18_39":   0.001,
        "male|40_64":   0.002,
        "male|65_plus": 0.0015,
        "female|0_1":     0.00001,
        "female|1_5":     0.00002,
        "female|6_12":    0.0001,
        "female|13_17":   0.0003,
        "female|18_39":   0.001,
        "female|40_64":   0.002,
        "female|65_plus": 0.0015,
    }
}

# --- Full CPTs (R01, R02) ---
s3['full_cpts'][DID] = {
    "R01": {
        "description": "SSNHL年齢分布。41-55歳ピーク(PMC9653771, PMC10151530)",
        "cpt": {
            "0_1":     0.002,
            "1_5":     0.003,
            "6_12":    0.01,
            "13_17":   0.03,
            "18_39":   0.22,
            "40_64":   0.45,
            "65_plus": 0.285
        }
    },
    "R02": {
        "description": "SSNHL性別。M:F≈1.07:1(PMC10151530)",
        "cpt": {
            "male":   0.52,
            "female": 0.48
        }
    }
}

# --- NOP parent_effects ---
nop = s3['noisy_or_params']

# S124 (hearing_loss): present 0.95 (by definition)
nop['S124']['parent_effects'][DID] = {"absent": 0.05, "present": 0.95}

# S140 (hearing_loss_type): sensorineural 0.95 (by definition)
nop['S140']['parent_effects'][DID] = {"conductive": 0.02, "sensorineural": 0.95, "mixed": 0.03}

# S125 (tinnitus): present 0.88 (80-95%, PMC7773829)
nop['S125']['parent_effects'][DID] = {"absent": 0.12, "present": 0.88}

# S59 (vertigo): present 0.40 (28-56%, PMC4040829)
nop['S59']['parent_effects'][DID] = {"absent": 0.60, "present": 0.40}

# S92 (vertigo_quality): non-episodic. When vertigo occurs, it's continuous or non-rotatory
# NOT episodic_with_hearing (key differentiation from Meniere)
nop['S92']['parent_effects'][DID] = {
    "positional_brief": 0.05,
    "continuous_rotatory": 0.45,
    "episodic_with_hearing": 0.10,
    "non_rotatory_disequilibrium": 0.40
}

# S79 (aural fullness proxy): present 0.50 (32-70%, PMC7773829)
nop['S79']['parent_effects'][DID] = {"absent": 0.50, "present": 0.50}

# S13 (nausea): present 0.22 (accompanies vertigo ~40% × vertigo 56%)
nop['S13']['parent_effects'][DID] = {"absent": 0.78, "present": 0.22}

# S66 (vomiting): present 0.12
nop['S66']['parent_effects'][DID] = {"absent": 0.88, "present": 0.12}

# E62 (nystagmus): horizontal ~35% overall (72-100% in vertigo subgroup × ~40% vertigo rate)
nop['E62']['parent_effects'][DID] = {
    "absent": 0.65,
    "horizontal": 0.30,
    "vertical": 0.02,
    "rotatory": 0.03
}

# E01 (fever): under_37.5 dominant
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.004,
    "under_37.5": 0.92,
    "37.5_38.0": 0.05,
    "38.0_39.0": 0.02,
    "39.0_40.0": 0.005,
    "over_40.0": 0.001
}

# T01: acute onset, mostly present within days
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.50,
    "3d_to_1w": 0.30,
    "1w_to_3w": 0.15,
    "over_3w": 0.05
}

# T02: sudden onset (many notice upon waking)
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.50,
    "acute": 0.35,
    "subacute": 0.10,
    "chronic": 0.05
}

print(f"Added CPTs for {DID}")
print(f"S140 now has {len(nop['S140']['parent_effects'])} parents")

# ── Save ──
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print("Saved all 3 files.")
