"""
D407 メニエール病 (Meniere's disease) 追加スクリプト
Step 0 文献: PMC10025214, PMC9839510, PMC10783974, PMC5782962, StatPearls NBK536955
"""
import json

# ── Load ──
s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D407"
DNAME = "menieres_disease"
DNAME_JA = "メニエール病"

# ── Step 1: Disease definition ──
new_disease = {
    "id": DID,
    "name": DNAME,
    "name_ja": DNAME_JA,
    "category": "ENT",
    "category_sub": "inner_ear",
    "states": ["absent","present"],
    "severity": "moderate",
    "note": "内リンパ水腫。三徴: 反復性回転性めまい(20分-12時間)+低音型感音性難聴+耳鳴。耳閉感。40-60歳, F>M(1.3:1)"
}
s1['variables'].append(new_disease)
print(f"Added {DID} to step1")

# ── Step 2: Edges (12 edges) ──
FROM = DID
FROM_NAME = DNAME_JA

new_edges = [
    # 1. Vertigo (90-100%, PMC10025214)
    {"from":FROM,"from_name":FROM_NAME,"to":"S59","to_name":"めまい",
     "reason":"メニエール病: 回転性めまい(90-100%, PMC10025214)"},
    # 2. Vertigo quality: episodic_with_hearing (classic triad, PMC10025214)
    {"from":FROM,"from_name":FROM_NAME,"to":"S92","to_name":"めまいの性状",
     "reason":"メニエール病: 反復性めまい+聴覚症状がclassic pattern(PMC10025214)"},
    # 3. Hearing loss (54-100%, PMC10025214)
    {"from":FROM,"from_name":FROM_NAME,"to":"S124","to_name":"難聴",
     "reason":"メニエール病: 感音性難聴(54-100%, PMC10025214)"},
    # 4. Hearing loss type: sensorineural (by definition)
    {"from":FROM,"from_name":FROM_NAME,"to":"S140","to_name":"難聴の種類",
     "reason":"メニエール病: 低音型感音性難聴(定義的, Harrison's/StatPearls)"},
    # 5. Tinnitus (72-98%, PMC10025214)
    {"from":FROM,"from_name":FROM_NAME,"to":"S125","to_name":"耳鳴",
     "reason":"メニエール病: 耳鳴(72-98%, PMC10025214)"},
    # 6. Nausea (20-91%, median ~60%, PMC10025214)
    {"from":FROM,"from_name":FROM_NAME,"to":"S13","to_name":"悪心",
     "reason":"メニエール病: 悪心(20-91%, PMC10025214)"},
    # 7. Vomiting (20-74%, PMC10025214)
    {"from":FROM,"from_name":FROM_NAME,"to":"S66","to_name":"嘔吐",
     "reason":"メニエール病: 嘔吐(20-74%, PMC10025214)"},
    # 8. Nystagmus: horizontal (during attacks ~80%, PMC10783974)
    {"from":FROM,"from_name":FROM_NAME,"to":"E62","to_name":"眼振",
     "reason":"メニエール病: 水平性眼振(発作時~80%, PMC10783974)"},
    # 9. Otalgia/aural fullness (37-81%, PMC10025214)
    {"from":FROM,"from_name":FROM_NAME,"to":"S79","to_name":"耳痛",
     "reason":"メニエール病: 耳閉感(37-81%, PMC10025214, S79をaural fullness代理として使用)"},
    # 10. Fever: absent (non-infectious)
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"メニエール病: 非感染性、発熱なし"},
    # 11. Symptom duration
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"メニエール病: 反復性エピソード、多くは慢性経過で受診"},
    # 12. Onset tempo
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"メニエール病: 発作は突然~急性発症、疾患全体は慢性反復性"},
]

s2['edges'].extend(new_edges)
print(f"Added {len(new_edges)} edges to step2. Total: {len(s2['edges'])}")

# ── Step 3: CPTs ──

# --- Root prior ---
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "メニエール病。40-60歳ピーク。F:M≈1.3:1。有病率190/100,000(PMC9839510)",
    "cpt": {
        "male|0_1":     0.00001,
        "male|1_5":     0.00001,
        "male|6_12":    0.0001,
        "male|13_17":   0.0003,
        "male|18_39":   0.0008,
        "male|40_64":   0.002,
        "male|65_plus": 0.001,
        "female|0_1":     0.00001,
        "female|1_5":     0.00001,
        "female|6_12":    0.0001,
        "female|13_17":   0.0004,
        "female|18_39":   0.001,
        "female|40_64":   0.003,
        "female|65_plus": 0.0015,
    }
}

# --- Full CPTs (R01, R02) ---
s3['full_cpts'][DID] = {
    "R01": {
        "description": "メニエール病年齢分布。40-60歳ピーク(StatPearls, PMC9839510)",
        "cpt": {
            "0_1":     0.001,
            "1_5":     0.001,
            "6_12":    0.01,
            "13_17":   0.03,
            "18_39":   0.20,
            "40_64":   0.50,
            "65_plus": 0.258
        }
    },
    "R02": {
        "description": "メニエール病性別。F:M≈1.3:1(PMC9839510)",
        "cpt": {
            "male":   0.43,
            "female": 0.57
        }
    }
}

# --- NOP parent_effects for existing NOP variables ---
nop = s3['noisy_or_params']

# S59 (vertigo): present 0.92
nop['S59']['parent_effects'][DID] = {"absent": 0.08, "present": 0.92}

# S92 (vertigo_quality): episodic_with_hearing 0.85
nop['S92']['parent_effects'][DID] = {
    "positional_brief": 0.03,
    "continuous_rotatory": 0.07,
    "episodic_with_hearing": 0.85,
    "non_rotatory_disequilibrium": 0.05
}

# S13 (nausea): present 0.60
nop['S13']['parent_effects'][DID] = {"absent": 0.40, "present": 0.60}

# S66 (vomiting): present 0.40
nop['S66']['parent_effects'][DID] = {"absent": 0.60, "present": 0.40}

# S79 (otalgia/aural fullness): present 0.50
nop['S79']['parent_effects'][DID] = {"absent": 0.50, "present": 0.50}

# E01 (fever): under_37.5 dominant
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.004,
    "under_37.5": 0.92,
    "37.5_38.0": 0.05,
    "38.0_39.0": 0.02,
    "39.0_40.0": 0.005,
    "over_40.0": 0.001
}

# T01: mostly over_3w (chronic recurrent disease)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.10,
    "3d_to_1w": 0.10,
    "1w_to_3w": 0.15,
    "over_3w": 0.65
}

# T02: mixed - attacks are sudden/acute, but disease course is chronic
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.15,
    "acute": 0.20,
    "subacute": 0.30,
    "chronic": 0.35
}

# --- Activate new NOP variables ---

# S124 (hearing_loss): 4 parents (D293, D298, D299, D407)
nop['S124'] = {
    "leak": {"absent": 0.90, "present": 0.10},
    "parent_effects": {
        "D293": {"absent": 0.95, "present": 0.05},   # BPPV: rarely hearing loss
        "D298": {"absent": 0.75, "present": 0.25},   # Bell's: hyperacusis ~30%, true HL less
        "D299": {"absent": 0.20, "present": 0.80},   # Ramsay Hunt: SNHL 60-80%
        DID:    {"absent": 0.15, "present": 0.85}    # Meniere: 54-100% (PMC10025214)
    }
}

# S140 (hearing_loss_type): 2 parents (D299, D407) - will reach 3+ with D408
nop['S140'] = {
    "leak": {"conductive": 0.30, "sensorineural": 0.50, "mixed": 0.20},
    "parent_effects": {
        "D299": {"conductive": 0.05, "sensorineural": 0.88, "mixed": 0.07},  # RH: SNHL
        DID:    {"conductive": 0.03, "sensorineural": 0.92, "mixed": 0.05}   # Meniere: SNHL
    }
}

# S125 (tinnitus): 3 parents (D293, D299, D407)
nop['S125'] = {
    "leak": {"absent": 0.85, "present": 0.15},
    "parent_effects": {
        "D293": {"absent": 0.92, "present": 0.08},   # BPPV: tinnitus uncommon
        "D299": {"absent": 0.30, "present": 0.70},   # RH: tinnitus ~70%
        DID:    {"absent": 0.15, "present": 0.85}    # Meniere: 72-98% (PMC10025214)
    }
}

# E62 (nystagmus): 4 parents (D293, D236, D295, D407)
nop['E62'] = {
    "leak": {"absent": 0.90, "horizontal": 0.04, "vertical": 0.03, "rotatory": 0.03},
    "parent_effects": {
        "D293": {"absent": 0.15, "horizontal": 0.05, "vertical": 0.05, "rotatory": 0.75},  # BPPV: torsional/rotatory
        "D236": {"absent": 0.55, "horizontal": 0.15, "vertical": 0.20, "rotatory": 0.10},  # MS: various, vertical suggestive
        "D295": {"absent": 0.88, "horizontal": 0.05, "vertical": 0.04, "rotatory": 0.03},  # Cluster: rare nystagmus
        DID:    {"absent": 0.20, "horizontal": 0.72, "vertical": 0.03, "rotatory": 0.05}   # Meniere: horizontal ~80%
    }
}

print(f"Added CPTs for {DID}")
print(f"Activated NOP for S124 (4 parents), S140 (2 parents), S125 (3 parents), E62 (4 parents)")

# ── Save ──
with open('step1_fever_v2.7.json','w',encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
with open('step2_fever_edges_v4.json','w',encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open('step3_fever_cpts_v2.json','w',encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print("Saved all 3 files.")
