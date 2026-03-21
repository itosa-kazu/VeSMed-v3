"""
D411 丹毒 (Erysipelas) 追加スクリプト
Step 0: StatPearls NBK532247, PMC4033615, PMC12347616, PMC2907977
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D411"
DNAME = "erysipelas"
DNAME_JA = "丹毒"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "skin_soft_tissue",
    "states": ["absent","present"], "severity": "moderate",
    "note": "真皮の急性細菌感染(GAS)。境界明瞭な隆起性紅斑が特徴。下肢85%、顔面20%。発熱20-70%。蜂窩織炎との鑑別: 境界明瞭+隆起性辺縁"
})
print(f"Added {DID} to step1")

# ── Step 2 (12 edges) ──
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"S18","to_name":"皮膚の訴え",
     "reason":"丹毒: 皮膚症状(~100%, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E12","to_name":"皮膚診察所見",
     "reason":"丹毒: 境界明瞭な紅斑+腫脹+熱感(~100%, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S87","to_name":"皮膚症状の種類",
     "reason":"丹毒: 局所性疼痛+発赤(常に局所性, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"丹毒: 発熱(20-70%, 平均38.1℃, PMC12347616)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S09","to_name":"悪寒",
     "reason":"丹毒: 悪寒(皮疹に48h先行可, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S07","to_name":"倦怠感",
     "reason":"丹毒: 前駆症状として倦怠感(StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E36","to_name":"浮腫",
     "reason":"丹毒: 局所浮腫(marked edema, bleb formation possible, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S96","to_name":"掻痒感",
     "reason":"丹毒: 局所掻痒感(itchiness at site, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L02","to_name":"CRP",
     "reason":"丹毒: CRP上昇(急性細菌感染)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"L01","to_name":"白血球数",
     "reason":"丹毒: 白血球増多(hyperleukocytosis, 文献review)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"丹毒: 急性(数日以内に受診)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"丹毒: 急性発症(spread rapidly within hours, StatPearls)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "丹毒。高齢者多い。M≈F。年間発症率~2/1000(PMC4033615)",
    "cpt": {
        "male|0_1":     0.0005,
        "male|1_5":     0.0005,
        "male|6_12":    0.0005,
        "male|13_17":   0.0008,
        "male|18_39":   0.001,
        "male|40_64":   0.002,
        "male|65_plus": 0.004,
        "female|0_1":     0.0005,
        "female|1_5":     0.0005,
        "female|6_12":    0.0005,
        "female|13_17":   0.0008,
        "female|18_39":   0.001,
        "female|40_64":   0.002,
        "female|65_plus": 0.004,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "丹毒年齢。高齢者に多い(PMC4033615)",
        "cpt": {
            "0_1":0.02, "1_5":0.02, "6_12":0.03, "13_17":0.04,
            "18_39":0.12, "40_64":0.30, "65_plus":0.47
        }
    },
    "R02": {
        "description": "丹毒性別。M≈F(PMC12347616: やや男性多い)",
        "cpt": {"male": 0.52, "female": 0.48}
    }
}

nop = s3['noisy_or_params']

# S18: present 0.95
nop['S18']['parent_effects'][DID] = {"absent": 0.05, "present": 0.95}

# E12: localized_erythema 0.92
nop['E12']['parent_effects'][DID] = {
    "normal": 0.01, "localized_erythema_warmth_swelling": 0.92,
    "petechiae_purpura": 0.005, "maculopapular_rash": 0.02,
    "vesicular_dermatomal": 0.005, "diffuse_erythroderma": 0.02,
    "purpura": 0.005, "vesicle_bulla": 0.01, "skin_necrosis": 0.005
}

# S87: localized_pain_redness 0.85 (always localized, vs cellulitis 0.50)
nop['S87']['parent_effects'][DID] = {"localized_pain_redness": 0.85, "rash_widespread": 0.15}

# E01: fever ~66%, typically 38-39
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.001, "under_37.5": 0.10,
    "37.5_38.0": 0.25, "38.0_39.0": 0.40,
    "39.0_40.0": 0.20, "over_40.0": 0.049
}

# S09: chills (common, prodromal)
nop['S09']['parent_effects'][DID] = {"absent": 0.40, "present": 0.60}

# S07: malaise (prodromal)
nop['S07']['parent_effects'][DID] = {"absent": 0.35, "mild": 0.45, "severe": 0.20}

# E36: edema (marked)
nop['E36']['parent_effects'][DID] = {"absent": 0.15, "present": 0.85}

# S96: localized pruritus (itchiness at site, ~50%)
nop['S96']['parent_effects'][DID] = {"absent": 0.50, "localized": 0.45, "generalized": 0.05}

# L02 (CRP): elevated
nop['L02']['parent_effects'][DID] = {"normal": 0.10, "mildly_elevated": 0.30, "highly_elevated": 0.60}

# L01 (WBC): leukocytosis
nop['L01']['parent_effects'][DID] = {"low": 0.02, "normal": 0.25, "high": 0.60, "very_high": 0.13}

# T01: acute
nop['T01']['parent_effects'][DID] = {"under_3d": 0.40, "3d_to_1w": 0.40, "1w_to_3w": 0.15, "over_3w": 0.05}

# T02: acute (rapid spread within hours)
nop['T02']['parent_effects'][DID] = {"sudden": 0.10, "acute": 0.65, "subacute": 0.20, "chronic": 0.05}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
