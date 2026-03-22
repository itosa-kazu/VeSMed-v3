"""D432 自己免疫性胃炎(A型) 追加スクリプト"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Step 1: 変数追加
# ============================================================
with open('step1_fever_v2.7.json', 'r', encoding='utf-8') as f:
    s1 = json.load(f)

variables = s1['variables']

d432 = {
    "id": "D432",
    "name": "autoimmune_gastritis",
    "name_ja": "自己免疫性胃炎(A型胃炎)",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "moderate",
    "note": "壁細胞自己免疫破壊→胃酸低下→B12/鉄吸収障害。悪性貧血の原因。F:M≥2:1、中央値67歳。甲状腺疾患36-44%併存。有病率0.5-2%"
}

d431_idx = next(i for i, v in enumerate(variables) if v['id'] == 'D431')
variables.insert(d431_idx + 1, d432)

with open('step1_fever_v2.7.json', 'w', encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
print("Step 1: D432 added")

# ============================================================
# Step 2: 辺追加
# ============================================================
with open('step2_fever_edges_v4.json', 'r', encoding='utf-8') as f:
    s2 = json.load(f)

edges = s2['edges']

new_edges = [
    # D432 -> T01 慢性(年単位)
    {
        "from": "D432", "to": "T01",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "symptom_duration",
        "reason": "自己免疫性胃炎: 年単位の慢性経過(PMC5065578 'late and unspecific')",
        "onset_day_range": None
    },
    # D432 -> T02 chronic
    {
        "from": "D432", "to": "T02",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "onset_speed",
        "reason": "自己免疫性胃炎: 緩徐発症、年単位(PMC5065578)",
        "onset_day_range": None
    },
    # D432 -> S12 腹痛(心窩部ディスペプシア): ~57% of symptomatic
    {
        "from": "D432", "to": "S12",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "abdominal_pain",
        "reason": "自己免疫性胃炎: ディスペプシア57%(有症状者中, PMC8414617)",
        "onset_day_range": None
    },
    # D432 -> S89 心窩部
    {
        "from": "D432", "to": "S89",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "abdominal_pain_region",
        "reason": "自己免疫性胃炎: 心窩部ディスペプシア(PMC8414617 'postprandial distress-like')",
        "onset_day_range": None
    },
    # D432 -> S07 倦怠感: 貧血に伴う40-60%
    {
        "from": "D432", "to": "S07",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "fatigue",
        "reason": "自己免疫性胃炎: 倦怠感40-60%(貧血に伴う, PMC5065578)",
        "onset_day_range": None
    },
    # D432 -> E44 腹部膨満: PDS-like
    {
        "from": "D432", "to": "E44",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "abdominal_distention",
        "reason": "自己免疫性胃炎: 食後膨満感(PDS-like dyspepsia, PMC8414617)",
        "onset_day_range": None
    },
    # D432 -> L94 MCV: macrocytic (B12欠乏) or microcytic (鉄欠乏)
    {
        "from": "D432", "to": "L94",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "MCV",
        "reason": "自己免疫性胃炎: B12欠乏でmacrocytic、鉄欠乏でmicrocytic(PMC5065578)",
        "onset_day_range": None
    },
    # D432 -> L90 鉄代謝: iron_deficiency (初期に多い)
    {
        "from": "D432", "to": "L90",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "iron_studies",
        "reason": "自己免疫性胃炎: 鉄欠乏は初期に多い(若年女性, PMC5065578)",
        "onset_day_range": None
    },
    # D432 -> E01 無熱
    {
        "from": "D432", "to": "E01",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "temperature",
        "reason": "自己免疫性胃炎: 発熱なし(慢性自己免疫疾患)",
        "onset_day_range": None
    },
    # D432 -> L01 WBC正常
    {
        "from": "D432", "to": "L01",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "WBC",
        "reason": "自己免疫性胃炎: WBC正常(器質的感染なし)",
        "onset_day_range": None
    },
    # D432 -> L02 CRP正常
    {
        "from": "D432", "to": "L02",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "CRP",
        "reason": "自己免疫性胃炎: CRP正常(自己免疫だが急性炎症はない)",
        "onset_day_range": None
    },
    # D432 -> S13 悪心: ~30%
    {
        "from": "D432", "to": "S13",
        "from_name": "自己免疫性胃炎(A型胃炎)", "to_name": "nausea",
        "reason": "自己免疫性胃炎: 悪心~30%(ディスペプシアの一部, PMC8414617)",
        "onset_day_range": None
    },
]

edges.extend(new_edges)
s2['total_edges'] = len(edges)

with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
print(f"Step 2: {len(new_edges)} edges added, total {len(edges)}")

# ============================================================
# Step 3: CPT追加
# ============================================================
with open('step3_fever_cpts_v2.json', 'r', encoding='utf-8') as f:
    s3 = json.load(f)

cpts = s3['full_cpts']
nop = s3['noisy_or_params']

# D432 disease CPT: parents=[R65(autoimmune_history)]
cpts['D432'] = {
    "parents": ["R65"],
    "description": "自己免疫性胃炎。自己免疫疾患既往でリスク上昇。有病率0.5-2%",
    "cpt": {
        "no": 0.003,     # 一般人口
        "yes": 0.015     # 自己免疫疾患既往あり(甲状腺等)
    },
    "R01": {
        "0_1": 0.0,
        "1_5": 0.0,
        "6_12": 0.0,
        "13_17": 0.001,
        "18_39": 0.002,
        "40_64": 0.004,
        "65_plus": 0.006   # median 67y, increasing with age
    },
    "R02": {
        "male": 0.33,   # F:M >= 2:1
        "female": 0.67
    }
}

# T01: over_3w (chronic, years)
if 'T01' in nop and 'parent_effects' in nop['T01']:
    nop['T01']['parent_effects']['D432'] = {
        "under_3d": 0.01,
        "3d_to_1w": 0.01,
        "1w_to_3w": 0.03,
        "over_3w": 0.95
    }

# T02: chronic
if 'T02' in nop and 'parent_effects' in nop['T02']:
    nop['T02']['parent_effects']['D432'] = {
        "sudden": 0.01,
        "acute": 0.02,
        "subacute": 0.12,
        "chronic": 0.85
    }

# S12: abdominal pain ~40% (57% of symptomatic, ~70% have some symptoms)
if 'S12' in nop and 'parent_effects' in nop['S12']:
    nop['S12']['parent_effects']['D432'] = 0.4

# S89: epigastric
if 'S89' in nop and 'parent_effects' in nop['S89']:
    nop['S89']['parent_effects']['D432'] = {
        "epigastric": 0.8,
        "RUQ": 0.03,
        "RLQ": 0.02,
        "LLQ": 0.02,
        "suprapubic": 0.02,
        "diffuse": 0.11
    }

# S07: fatigue ~50%
if 'S07' in nop and 'parent_effects' in nop['S07']:
    nop['S07']['parent_effects']['D432'] = {
        "absent": 0.5,
        "mild": 0.35,
        "severe": 0.15
    }

# E44: bloating ~40%
if 'E44' in nop and 'parent_effects' in nop['E44']:
    nop['E44']['parent_effects']['D432'] = {
        "absent": 0.6,
        "mild": 0.35,
        "severe": 0.05
    }

# L94: MCV - macrocytic dominant (B12) but mixed possible
if 'L94' not in nop or not nop.get('L94'):
    nop['L94'] = {
        "description": "MCV",
        "states": ["microcytic", "normocytic", "macrocytic"],
        "leak": {"microcytic": 0.1, "normocytic": 0.8, "macrocytic": 0.1},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['L94']:
    nop['L94']['parent_effects'] = {}
nop['L94']['parent_effects']['D432'] = {
    "microcytic": 0.25,   # iron deficiency (early, young women)
    "normocytic": 0.2,
    "macrocytic": 0.55    # B12 deficiency (classic)
}

# L90: iron deficiency
if 'L90' not in nop or not nop.get('L90'):
    nop['L90'] = {
        "description": "鉄代謝",
        "states": ["iron_deficiency", "chronic_disease", "iron_overload", "normal"],
        "leak": {"iron_deficiency": 0.05, "chronic_disease": 0.05, "iron_overload": 0.02, "normal": 0.88},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['L90']:
    nop['L90']['parent_effects'] = {}
nop['L90']['parent_effects']['D432'] = {
    "iron_deficiency": 0.5,   # common early finding
    "chronic_disease": 0.1,
    "iron_overload": 0.01,
    "normal": 0.39
}

# E01: afebrile
if 'E01' in nop and 'parent_effects' in nop['E01']:
    nop['E01']['parent_effects']['D432'] = {
        "under_37.5": 0.95,
        "37.5_38.0": 0.04,
        "38.0_39.0": 0.008,
        "39.0_40.0": 0.001,
        "over_40.0": 0.0005,
        "hypothermia_under_35": 0.0005
    }

# L01: WBC normal
if 'L01' in nop and 'parent_effects' in nop['L01']:
    nop['L01']['parent_effects']['D432'] = {
        "low_under_4000": 0.05,
        "normal_4000_10000": 0.9,
        "high_10000_20000": 0.04,
        "very_high_over_20000": 0.01
    }

# L02: CRP normal
if 'L02' in nop and 'parent_effects' in nop['L02']:
    nop['L02']['parent_effects']['D432'] = {
        "normal_under_0.3": 0.85,
        "mild_0.3_3": 0.12,
        "moderate_3_10": 0.025,
        "high_over_10": 0.005
    }

# S13: nausea ~30%
if 'S13' in nop and 'parent_effects' in nop['S13']:
    nop['S13']['parent_effects']['D432'] = 0.3

with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print("Step 3: D432 CPTs added")
print("Done!")
