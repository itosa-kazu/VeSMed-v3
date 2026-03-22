"""D433 Meckel憩室 追加スクリプト"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Step 1
# ============================================================
with open('step1_fever_v2.7.json', 'r', encoding='utf-8') as f:
    s1 = json.load(f)
variables = s1['variables']

d433 = {
    "id": "D433",
    "name": "meckel_diverticulum",
    "name_ja": "Meckel憩室",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "serious",
    "note": "回腸遠位の先天性憩室。人口の2%。症候性は4-6%。成人では炎症/閉塞が主体、小児では出血。M:F≈1.7:1、平均25歳"
}

d432_idx = next(i for i, v in enumerate(variables) if v['id'] == 'D432')
variables.insert(d432_idx + 1, d433)

with open('step1_fever_v2.7.json', 'w', encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
print("Step 1: D433 added")

# ============================================================
# Step 2
# ============================================================
with open('step2_fever_edges_v4.json', 'r', encoding='utf-8') as f:
    s2 = json.load(f)
edges = s2['edges']

new_edges = [
    {
        "from": "D433", "to": "S12",
        "from_name": "Meckel憩室", "to_name": "abdominal_pain",
        "reason": "Meckel: 腹痛66%(RLQ31%+lower19%+acute abdomen16%, PMC9436618)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "S89",
        "from_name": "Meckel憩室", "to_name": "abdominal_pain_region",
        "reason": "Meckel: RLQ 31%が最多、次いでdiffuse/LLQ(PMC9436618)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "T02",
        "from_name": "Meckel憩室", "to_name": "onset_speed",
        "reason": "Meckel: 急性発症が典型(StatPearls 'emergency presentation')",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "T01",
        "from_name": "Meckel憩室", "to_name": "symptom_duration",
        "reason": "Meckel: 急性で数日以内に受診(PMC9436618)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "S13",
        "from_name": "Meckel憩室", "to_name": "nausea",
        "reason": "Meckel: 悪心~50%(特に閉塞例, StatPearls)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "S66",
        "from_name": "Meckel憩室", "to_name": "vomiting",
        "reason": "Meckel: 嘔吐~40%(閉塞例, StatPearls)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "E01",
        "from_name": "Meckel憩室", "to_name": "temperature",
        "reason": "Meckel: 発熱30-40%(炎症/穿孔例, StatPearls)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "E09",
        "from_name": "Meckel憩室", "to_name": "abdominal_exam",
        "reason": "Meckel: RLQ圧痛(虫垂炎mimicry)~50%、腹膜刺激徴候15-19%(穿孔, PMC9436618)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "L01",
        "from_name": "Meckel憩室", "to_name": "WBC",
        "reason": "Meckel: WBC上昇50-60%(炎症例)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "L02",
        "from_name": "Meckel憩室", "to_name": "CRP",
        "reason": "Meckel: CRP軽度〜中等度上昇(炎症例)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "S86",
        "from_name": "Meckel憩室", "to_name": "diarrhea_quality",
        "reason": "Meckel: 血便(暗赤色)3-12%(成人, StatPearls/PMC9436618)",
        "onset_day_range": None
    },
    {
        "from": "D433", "to": "S14",
        "from_name": "Meckel憩室", "to_name": "diarrhea",
        "reason": "Meckel: 下痢/血便(PMC9436618 'bleeding per rectum 2.9%'成人)",
        "onset_day_range": None
    },
]

edges.extend(new_edges)
s2['total_edges'] = len(edges)
with open('step2_fever_edges_v4.json', 'w', encoding='utf-8') as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
print(f"Step 2: {len(new_edges)} edges added, total {len(edges)}")

# ============================================================
# Step 3
# ============================================================
with open('step3_fever_cpts_v2.json', 'r', encoding='utf-8') as f:
    s3 = json.load(f)
cpts = s3['full_cpts']
nop = s3['noisy_or_params']

# D433: no special risk factor parent. Rare symptomatic presentation
cpts['D433'] = {
    "parents": [],
    "description": "Meckel憩室(症候性)。人口2%保有、症候性は4-6%lifetime",
    "cpt": {"no": 0.999, "yes": 0.001},
    "R01": {
        "0_1": 0.005,
        "1_5": 0.004,
        "6_12": 0.003,
        "13_17": 0.003,
        "18_39": 0.003,   # mean 25y
        "40_64": 0.001,
        "65_plus": 0.0005
    },
    "R02": {
        "male": 0.63,    # M:F=63:37 (PMC9436618)
        "female": 0.37
    }
}

# S12: abdominal pain 66%
nop['S12']['parent_effects']['D433'] = 0.66

# S89: RLQ dominant (mimics appendicitis)
nop['S89']['parent_effects']['D433'] = {
    "epigastric": 0.05,
    "RUQ": 0.02,
    "RLQ": 0.5,      # 31% RLQ + periumbilical
    "LLQ": 0.08,
    "suprapubic": 0.05,
    "diffuse": 0.3    # acute abdomen 16%
}

# T02: acute dominant
nop['T02']['parent_effects']['D433'] = {
    "sudden": 0.2,
    "acute": 0.6,
    "subacute": 0.15,
    "chronic": 0.05
}

# T01: under_3d to 1w
nop['T01']['parent_effects']['D433'] = {
    "under_3d": 0.55,
    "3d_to_1w": 0.35,
    "1w_to_3w": 0.08,
    "over_3w": 0.02
}

# S13: nausea ~50%
nop['S13']['parent_effects']['D433'] = 0.5

# S66: vomiting ~40%
nop['S66']['parent_effects']['D433'] = {"absent": 0.6, "present": 0.4}

# E01: fever 30-40%
nop['E01']['parent_effects']['D433'] = {
    "under_37.5": 0.5,
    "37.5_38.0": 0.2,
    "38.0_39.0": 0.2,
    "39.0_40.0": 0.08,
    "over_40.0": 0.015,
    "hypothermia_under_35": 0.005
}

# E09: localized tenderness dominant, peritoneal signs 15-19%
nop['E09']['parent_effects']['D433'] = {
    "soft_nontender": 0.1,
    "localized_tenderness": 0.7,
    "peritoneal_signs": 0.2
}

# L01: WBC elevated ~55%
nop['L01']['parent_effects']['D433'] = {
    "low_under_4000": 0.02,
    "normal_4000_10000": 0.43,
    "high_10000_20000": 0.45,
    "very_high_over_20000": 0.1
}

# L02: CRP mild-moderate
nop['L02']['parent_effects']['D433'] = {
    "normal_under_0.3": 0.3,
    "mild_0.3_3": 0.35,
    "moderate_3_10": 0.25,
    "high_over_10": 0.1
}

# S86: bloody stool (when present)
nop_s86 = nop.get('S86', {})
if s86_nop := nop.get('S86'):
    if 'parent_effects' in s86_nop:
        s86_nop['parent_effects']['D433'] = {
            "watery": 0.3,
            "bloody": 0.7   # when diarrhea is present, it's usually bloody
        }

# S14: diarrhea/bleeding ~15%
nop_s14 = nop.get('S14', {})
if 'parent_effects' in nop_s14:
    nop_s14['parent_effects']['D433'] = 0.15

with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print("Step 3: D433 CPTs added")
print("Done!")
