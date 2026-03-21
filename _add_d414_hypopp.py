"""
D414 低カリウム性周期性四肢麻痺 (Hypokalemic Periodic Paralysis, HypoPP) 追加スクリプト
+ L108 serum_potassium (血清カリウム) 新変量追加

Step 0: GeneReviews NBK1338, StatPearls NBK559178, GeneReviews NBK1496, PMC1426181
"""
import json

s1 = json.load(open('step1_fever_v2.7.json','r',encoding='utf-8'))
s2 = json.load(open('step2_fever_edges_v4.json','r',encoding='utf-8'))
s3 = json.load(open('step3_fever_cpts_v2.json','r',encoding='utf-8'))

# =============================================
# Part A: L108 serum_potassium 新変量
# =============================================
L_ID = "L108"
L_NAME = "serum_potassium"
L_NAME_JA = "血清カリウム"

s1['variables'].append({
    "id": L_ID, "name": L_NAME, "name_ja": L_NAME_JA,
    "category": "lab", "category_sub": "electrolyte",
    "states": ["severe_hypo_under_2.5", "hypo_2.5_3.5", "normal", "hyper_5.0_6.5", "severe_hyper_over_6.5"],
    "severity": "moderate",
    "note": "血清K+。基準値3.5-5.0mEq/L。低K: 筋力低下/不整脈/イレウス。高K: 不整脈(peaked T/wide QRS)/心停止。"
})
print(f"Added {L_ID} to step1")

# L108 edges from existing diseases
l108_edges = [
    {"from":"D380","from_name":"cushing_syndrome","to":L_ID,"to_name":L_NAME_JA,
     "reason":"Cushing: 低K血症(43-75%, ミネラルコルチコイド過剰, PMC4407747/PMC4215264)"},
    {"from":"D321","from_name":"primary_aldosteronism","to":L_ID,"to_name":L_NAME_JA,
     "reason":"原発性アルドステロン症: 低K血症(30-50%が低K、classic feature, StatPearls)"},
    {"from":"D72","from_name":"adrenal_crisis","to":L_ID,"to_name":L_NAME_JA,
     "reason":"副腎クリーゼ: 高K血症(アルドステロン欠乏→K排泄低下, Harrison's Ch.379)"},
    {"from":"D153","from_name":"rhabdomyolysis","to":L_ID,"to_name":L_NAME_JA,
     "reason":"横紋筋融解症: 高K血症(細胞崩壊→K放出, 30-40%, PMC5594070)"},
    {"from":"D140","from_name":"diabetic_ketoacidosis","to":L_ID,"to_name":L_NAME_JA,
     "reason":"DKA: 来院時高K(アシドーシスによるK細胞外シフト, 初期30-40%高K, StatPearls)"},
]
s2['edges'].extend(l108_edges)
print(f"Added {len(l108_edges)} L108 edges from existing diseases")

# L108 NOP (leak + 6 parents including D414)
s3['noisy_or_params'][L_ID] = {
    "leak": {
        "severe_hypo_under_2.5": 0.005,
        "hypo_2.5_3.5": 0.04,
        "normal": 0.90,
        "hyper_5.0_6.5": 0.045,
        "severe_hyper_over_6.5": 0.01
    },
    "parent_effects": {
        # D380 Cushing: hypokalemia 43-75%
        "D380": {
            "severe_hypo_under_2.5": 0.05, "hypo_2.5_3.5": 0.45,
            "normal": 0.40, "hyper_5.0_6.5": 0.08, "severe_hyper_over_6.5": 0.02
        },
        # D321 primary aldosteronism: hypokalemia classic
        "D321": {
            "severe_hypo_under_2.5": 0.10, "hypo_2.5_3.5": 0.55,
            "normal": 0.30, "hyper_5.0_6.5": 0.04, "severe_hyper_over_6.5": 0.01
        },
        # D72 adrenal crisis: hyperkalemia from aldosterone deficiency
        "D72": {
            "severe_hypo_under_2.5": 0.02, "hypo_2.5_3.5": 0.05,
            "normal": 0.38, "hyper_5.0_6.5": 0.40, "severe_hyper_over_6.5": 0.15
        },
        # D153 rhabdomyolysis: hyperkalemia from cell lysis
        "D153": {
            "severe_hypo_under_2.5": 0.02, "hypo_2.5_3.5": 0.05,
            "normal": 0.53, "hyper_5.0_6.5": 0.30, "severe_hyper_over_6.5": 0.10
        },
        # D140 DKA: initial hyperkalemia (acidosis-driven K shift)
        "D140": {
            "severe_hypo_under_2.5": 0.03, "hypo_2.5_3.5": 0.12,
            "normal": 0.35, "hyper_5.0_6.5": 0.35, "severe_hyper_over_6.5": 0.15
        },
    }
}
print(f"Added L108 NOP with 5 existing parents")

# =============================================
# Part B: D414 低カリウム性周期性四肢麻痺
# =============================================
DID = "D414"
DNAME = "hypokalemic_periodic_paralysis"
DNAME_JA = "低カリウム性周期性四肢麻痺"

s1['variables'].append({
    "id": DID, "name": DNAME, "name_ja": DNAME_JA,
    "category": "disease", "category_sub": "neurology",
    "states": ["absent","present"], "severity": "moderate",
    "note": "Ca/Naチャネル変異→低K時に筋麻痺発作。Whipple三徴(の低血糖版ではなく低K版)。発作時K<3.5(多くは<2.5)。10-20歳発症、M>F(3:1)。炭水化物摂取/運動後安静で誘発。甲状腺中毒性PPも類似"
})
print(f"Added {DID} to step1")

# D414 edges (10 edges)
FROM = DID
FROM_NAME = DNAME_JA
new_edges = [
    {"from":FROM,"from_name":FROM_NAME,"to":"L108","to_name":"血清カリウム",
     "reason":"HypoPP: 発作時低K(K+ 0.9-3.5mEq/L, 平均1.8-2.3, GeneReviews NBK1338)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S48","to_name":"近位筋力低下",
     "reason":"HypoPP: 近位筋優位の四肢麻痺(下肢>上肢、95%+, StatPearls NBK559178)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E53","to_name":"深部腱反射",
     "reason":"HypoPP: 発作時腱反射低下〜消失(下位運動ニューロン型, StatPearls NBK559178)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S106","to_name":"歩行障害",
     "reason":"HypoPP: 下肢麻痺による歩行不能(下肢>上肢, 80%+, GeneReviews NBK1338)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S07","to_name":"倦怠感・疲労感",
     "reason":"HypoPP: 疲労(89%が報告, GeneReviews NBK1338)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S06","to_name":"筋肉痛",
     "reason":"HypoPP: 筋痙攣・筋痛(発作前駆症状/随伴, 30-40%, GeneReviews NBK1338)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"S35","to_name":"動悸",
     "reason":"HypoPP: 低K→心電図異常(U波/QT延長)→動悸(15-20%, PMC1426181)"},
    {"from":FROM,"from_name":FROM_NAME,"to":"E01","to_name":"体温",
     "reason":"HypoPP: 非感染性チャネル病、発熱なし"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T01","to_name":"症状持続期間",
     "reason":"HypoPP: 発作は1-72時間(平均24h, GeneReviews NBK1338)。再発性だが各発作は急性"},
    {"from":FROM,"from_name":FROM_NAME,"to":"T02","to_name":"発症速度",
     "reason":"HypoPP: 突然〜急性発症の四肢麻痺(数分〜数時間で完成, GeneReviews NBK1338)"},
]
s2['edges'].extend(new_edges)
s2['total_edges'] = len(s2['edges'])
print(f"Added {len(new_edges)} D414 edges. Total edges: {len(s2['edges'])}")

# Also add D414 as L108 NOP parent
s3['noisy_or_params'][L_ID]['parent_effects'][DID] = {
    "severe_hypo_under_2.5": 0.60, "hypo_2.5_3.5": 0.35,
    "normal": 0.04, "hyper_5.0_6.5": 0.005, "severe_hyper_over_6.5": 0.005
}
print(f"Added D414 as L108 parent (total L108 parents: {len(s3['noisy_or_params'][L_ID]['parent_effects'])})")

# ── Step 3: R→D Priors ──
# M:F = 3:1, onset 2-30 years (peak teens)
s3['root_priors'][DID] = {
    "parents": ["R02","R01"],
    "description": "HypoPP。1/10万。M:F=3:1。10-20歳発症ピーク。AD遺伝(CACNA1S 40-60%)",
    "cpt": {
        "male|0_1":     0.000001,
        "male|1_5":     0.000005,
        "male|6_12":    0.00005,
        "male|13_17":   0.0001,
        "male|18_39":   0.00008,
        "male|40_64":   0.00003,
        "male|65_plus": 0.00001,
        "female|0_1":     0.000001,
        "female|1_5":     0.000002,
        "female|6_12":    0.00002,
        "female|13_17":   0.00004,
        "female|18_39":   0.00003,
        "female|40_64":   0.00001,
        "female|65_plus": 0.000005,
    }
}

s3['full_cpts'][DID] = {
    "R01": {
        "description": "HypoPP年齢。発症10-20歳ピーク(GeneReviews NBK1338, mean 14yr)",
        "cpt": {
            "0_1":0.001, "1_5":0.02, "6_12":0.15, "13_17":0.30,
            "18_39":0.35, "40_64":0.15, "65_plus":0.029
        }
    },
    "R02": {
        "description": "HypoPP性別。M:F=3:1(penetrance差, GeneReviews NBK1338)",
        "cpt": {"male": 0.75, "female": 0.25}
    }
}

nop = s3['noisy_or_params']

# S48: proximal muscle weakness 95%+
nop['S48']['parent_effects'][DID] = {"absent": 0.05, "present": 0.95}

# E53: DTR hyporeflexia/areflexia during attack
nop['E53']['parent_effects'][DID] = {
    "normal": 0.15, "areflexia": 0.25, "hyporeflexia": 0.60
}

# S106: gait disturbance 80%
nop['S106']['parent_effects'][DID] = {"absent": 0.20, "present": 0.80}

# S07: fatigue 89%
nop['S07']['parent_effects'][DID] = {"absent": 0.11, "mild": 0.44, "severe": 0.45}

# S06: myalgia 35%
nop['S06']['parent_effects'][DID] = {"absent": 0.65, "present": 0.35}

# S35: palpitation 15% (hypokalemia-induced cardiac awareness)
nop['S35']['parent_effects'][DID] = {"absent": 0.85, "present": 0.15}

# E01: no fever
nop['E01']['parent_effects'][DID] = {
    "hypothermia_under_35": 0.005, "under_37.5": 0.95,
    "37.5_38.0": 0.03, "38.0_39.0": 0.01,
    "39.0_40.0": 0.003, "over_40.0": 0.002
}

# T01: attacks 1-72h → under_3d dominant
nop['T01']['parent_effects'][DID] = {
    "under_3d": 0.70, "3d_to_1w": 0.20,
    "1w_to_3w": 0.08, "over_3w": 0.02
}

# T02: acute/sudden onset
nop['T02']['parent_effects'][DID] = {
    "sudden": 0.30, "acute": 0.55,
    "subacute": 0.10, "chronic": 0.05
}

print(f"Added CPTs for {DID}")

for fname, data in [('step1_fever_v2.7.json',s1),('step2_fever_edges_v4.json',s2),('step3_fever_cpts_v2.json',s3)]:
    with open(fname,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
