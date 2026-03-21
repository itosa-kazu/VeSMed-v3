"""
D410 尋常性乾癬 (Psoriasis Vulgaris) 追加スクリプト
Step 0: StatPearls NBK430879, PMC5134160, PMC3047933, PMC4008063, PMC7122924
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

DID = "D410"
DNAME = "psoriasis_vulgaris"
DNAME_JA = "尋常性乾癬"

# ── Step 1 ──
s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "dermatology",
    "states": ["absent","present"], "severity": "moderate",
    "note": "慢性免疫介在性皮膚疾患。境界明瞭な紅斑+銀白色鱗屑(伸側優位)。PsA 20-30%。掻痒60-90%。二峰性発症(20-30歳/55-60歳)"
})
print(f"Added {DID} to step1")

# ── Step 2: Edges (12 edges) ──
FROM = DID
FROM_NAME = DNAME_JA

new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"S18","to_name":"皮膚の訴え",
     "reason":"乾癬: 皮膚症状がprimary complaint(~100%, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E12","to_name":"皮膚診察所見",
     "reason":"乾癬: 紅斑+鱗屑プラーク→maculopapular_rash(~100%, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S96","to_name":"掻痒感",
     "reason":"乾癬: 掻痒(60-90%, PMC3047933)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S87","to_name":"皮膚症状の種類",
     "reason":"乾癬: 広範な皮疹(plaque型80-90%, StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S75","to_name":"皮疹の分布",
     "reason":"乾癬: 伸側(肘/膝)優位→extremities_centrifugal(StatPearls)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S08","to_name":"関節痛",
     "reason":"乾癬: 関節痛~50%(PsA 20-30%, PMC7122924)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S90","to_name":"関節痛の分布",
     "reason":"乾癬性関節炎: 非対称性少関節/多関節(PMC5134160)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S43","to_name":"手掌・足底の皮疹",
     "reason":"乾癬: 掌蹠型12-16%(Psoriasis.org)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S27","to_name":"朝のこわばり",
     "reason":"乾癬性関節炎: 朝のこわばり(PsA患者~50%, PMC5134160)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"乾癬: 非感染性、発熱なし(erythrodermic除く)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"乾癬: 慢性疾患(数週~数ヶ月以上で受診)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"乾癬: 慢性・緩徐発症"},
]

s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} edges. Total: {len(s2['edges'])}")

# ── Step 3 ──
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "乾癬。二峰性(20-30歳/55-60歳)。M≈F。有病率2-3%(PMC5134160)",
    "cpt": {
        "male|0_1":     0.0001,
        "male|1_5":     0.0002,
        "male|6_12":    0.0005,
        "male|13_17":   0.001,
        "male|18_39":   0.003,
        "male|40_64":   0.003,
        "male|65_plus": 0.002,
        "female|0_1":     0.0001,
        "female|1_5":     0.0002,
        "female|6_12":    0.0005,
        "female|13_17":   0.001,
        "female|18_39":   0.003,
        "female|40_64":   0.003,
        "female|65_plus": 0.002,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "乾癬年齢。二峰性Type I(20-30歳)75%+Type II(55-60歳)25%",
        "cpt": {
            "0_1":     0.01,
            "1_5":     0.02,
            "6_12":    0.05,
            "13_17":   0.08,
            "18_39":   0.30,
            "40_64":   0.35,
            "65_plus": 0.19
        }
    },
    "R02": {
        "description": "乾癬性別。M≈F(M:F~1:1, PMC5134160)",
        "cpt": {"male": 0.51, "female": 0.49}
    }
}

nop = s3['noisy_or_params']

# S18 (skin_complaint): present 0.95
nop['S18']['parent_effects'][DID] = {"absent": 0.05, "present": 0.95}

# E12 (skin_exam): maculopapular_rash 0.82 (plaque), diffuse_erythroderma 0.02
nop['E12']['parent_effects'][DID] = {
    "normal": 0.02,
    "localized_erythema_warmth_swelling": 0.02,
    "petechiae_purpura": 0.001,
    "maculopapular_rash": 0.82,
    "vesicular_dermatomal": 0.001,
    "diffuse_erythroderma": 0.02,
    "purpura": 0.001,
    "vesicle_bulla": 0.001,
    "skin_necrosis": 0.001
}
# Verify sum
e12_sum = sum(nop['E12']['parent_effects'][DID].values())
nop['E12']['parent_effects'][DID]['maculopapular_rash'] += (1.0 - e12_sum)

# S96 (pruritus): localized 0.40, generalized 0.35 (total ~75%)
nop['S96']['parent_effects'][DID] = {
    "absent": 0.25,
    "localized": 0.40,
    "generalized": 0.35
}

# S87 (skin_complaint_type): rash_widespread 0.75
nop['S87']['parent_effects'][DID] = {
    "localized_pain_redness": 0.25,
    "rash_widespread": 0.75
}

# S75 (rash_distribution): extremities_centrifugal 0.65
nop['S75']['parent_effects'][DID] = {
    "trunk_centripetal": 0.10,
    "extremities_centrifugal": 0.65,
    "acral": 0.10,
    "mucosal": 0.01,
    "generalized": 0.14
}

# S08 (arthralgia): present 0.35 (~50% have joint pain, PMC7122924)
nop['S08']['parent_effects'][DID] = {"absent": 0.65, "present": 0.35}

# S90 (arthralgia_distribution): oligoarticular or polyarticular_asymmetric
nop['S90']['parent_effects'][DID] = {
    "monoarticular": 0.15,
    "oligoarticular": 0.35,
    "polyarticular_symmetric": 0.10,
    "polyarticular_asymmetric": 0.30,
    "migratory": 0.10
}

# S43 (palm_sole_rash): present 0.15 (12-16%)
nop['S43']['parent_effects'][DID] = {"absent": 0.85, "present": 0.15}

# S27 (morning_stiffness): present 0.20 (PsA patients)
nop['S27']['parent_effects'][DID] = {"absent": 0.80, "present": 0.20}

# E01: under_37.5 dominant
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.004,
    "under_37.5": 0.92,
    "37.5_38.0": 0.05,
    "38.0_39.0": 0.02,
    "39.0_40.0": 0.005,
    "over_40.0": 0.001
}

# T01: chronic (weeks to months)
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.02,
    "3d_to_1w": 0.05,
    "1w_to_3w": 0.18,
    "over_3w": 0.75
}

# T02: chronic
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.02,
    "acute": 0.05,
    "subacute": 0.18,
    "chronic": 0.75
}

print(f"Added CPTs for {DID}")

# ── Save ──
for fname, data in [
    ('step1_fever_v2.7.json', s1),
    ('step2_fever_edges_v4.json', s2),
    ('step3_fever_cpts_v2.json', s3),
]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved all 3 files.")
