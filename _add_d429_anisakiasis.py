"""D429 アニサキス症 + R67 生魚摂取歴 追加スクリプト"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Step 1: 変数追加
# ============================================================
with open('step1_fever_v2.7.json', 'r', encoding='utf-8') as f:
    s1 = json.load(f)

variables = s1['variables']

# R67: 生魚摂取歴
r67 = {
    "id": "R67",
    "name": "raw_fish_intake",
    "name_ja": "生魚摂取歴（24h以内）",
    "category": "risk",
    "states": ["no", "yes"],
    "note": "24時間以内の生魚・刺身摂取歴。アニサキス症の必須リスク因子"
}

# D429: アニサキス症
d429 = {
    "id": "D429",
    "name": "anisakiasis",
    "name_ja": "アニサキス症",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "moderate",
    "note": "生魚摂取後1-12hで激烈心窩部痛+悪心嘔吐。内視鏡で虫体除去。年間2000-3000例(日本)"
}

# Insert R67 after R66 (index 809)
r66_idx = next(i for i, v in enumerate(variables) if v['id'] == 'R66')
variables.insert(r66_idx + 1, r67)

# Insert D429 after D428 (need to re-find after R67 insertion)
d428_idx = next(i for i, v in enumerate(variables) if v['id'] == 'D428')
variables.insert(d428_idx + 1, d429)

with open('step1_fever_v2.7.json', 'w', encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)

print("Step 1: R67 + D429 added")

# ============================================================
# Step 2: 辺追加
# ============================================================
with open('step2_fever_edges_v4.json', 'r', encoding='utf-8') as f:
    s2 = json.load(f)

edges = s2['edges']

new_edges = [
    # D429 -> T01 症状持続期間: 通常1-3日で自然軽快
    {
        "from": "D429", "to": "T01",
        "from_name": "アニサキス症", "to_name": "symptom_duration",
        "reason": "アニサキス症: 通常1-3日で自然軽快(内視鏡除去後は数時間, CMR 1989)",
        "onset_day_range": None
    },
    # D429 -> T02 発症速度: 1-12h, acute~sudden
    {
        "from": "D429", "to": "T02",
        "from_name": "アニサキス症", "to_name": "onset_speed",
        "reason": "アニサキス症: 摂取後1-12時間で急性発症(PMC8223542)",
        "onset_day_range": None
    },
    # D429 -> S12 腹痛: ~78% symptomatic (PMC10353124)
    {
        "from": "D429", "to": "S12",
        "from_name": "アニサキス症", "to_name": "abdominal_pain",
        "reason": "アニサキス症: 腹痛78%(PMC10353124, n=212)",
        "onset_day_range": None
    },
    # D429 -> S89 腹痛部位: 心窩部が主(胃型90%)
    {
        "from": "D429", "to": "S89",
        "from_name": "アニサキス症", "to_name": "abdominal_pain_region",
        "reason": "アニサキス症: 胃型90%で心窩部痛が主(JIHS疫学情報)",
        "onset_day_range": None
    },
    # D429 -> S13 悪心: 67% (PubMed 16029756, n=42)
    {
        "from": "D429", "to": "S13",
        "from_name": "アニサキス症", "to_name": "nausea",
        "reason": "アニサキス症: 悪心67%(PubMed 16029756, 42例)",
        "onset_day_range": None
    },
    # D429 -> S66 嘔吐: 51% (PubMed 16029756, n=42)
    {
        "from": "D429", "to": "S66",
        "from_name": "アニサキス症", "to_name": "vomiting",
        "reason": "アニサキス症: 嘔吐51%(PubMed 16029756, 42例)",
        "onset_day_range": None
    },
    # D429 -> E09 腹部触診: 心窩部圧痛
    {
        "from": "D429", "to": "E09",
        "from_name": "アニサキス症", "to_name": "abdominal_exam",
        "reason": "アニサキス症: 心窩部圧痛が主体(PMC3732148)",
        "onset_day_range": None
    },
    # D429 -> L01 WBC: 51% elevated in symptomatic (PMC10353124)
    {
        "from": "D429", "to": "L01",
        "from_name": "アニサキス症", "to_name": "WBC",
        "reason": "アニサキス症: 有症状群の51%でWBC上昇(PMC10353124)",
        "onset_day_range": None
    },
    # D429 -> L02 CRP: 軽度上昇が多い
    {
        "from": "D429", "to": "L02",
        "from_name": "アニサキス症", "to_name": "CRP",
        "reason": "アニサキス症: CRP軽度上昇(急性期は短時間で間に合わないことも, PMC10353124)",
        "onset_day_range": None
    },
    # D429 -> R67 生魚摂取歴: 必須条件
    {
        "from": "D429", "to": "R67",
        "from_name": "アニサキス症", "to_name": "raw_fish_intake",
        "reason": "アニサキス症: 生魚摂取が必須条件(CDC, 全例に摂取歴あり)",
        "onset_day_range": None
    },
    # D429 -> S64 腹痛の程度: severe
    {
        "from": "D429", "to": "S64",
        "from_name": "アニサキス症", "to_name": "abdominal_pain_severity",
        "reason": "アニサキス症: 激烈な心窩部痛が特徴(severe, PMC5075291)",
        "onset_day_range": None
    },
    # D429 -> S61 腹痛性状: sharp_stabbing
    {
        "from": "D429", "to": "S61",
        "from_name": "アニサキス症", "to_name": "abdominal_pain_quality",
        "reason": "アニサキス症: 突き刺すような鋭い痛み(PMC3732148 'severe constant burning'も)",
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

# D429 disease CPT (full_cpts): parents=[R67]
# アニサキス: prevalence ~0.002 (年間2000-3000/1.2億人), 生魚摂取時に跳ね上がる
cpts['D429'] = {
    "parents": ["R67"],
    "description": "アニサキス症。生魚摂取が必須条件",
    "cpt": {
        "no": 0.0001,    # 生魚摂取なしではほぼ発症しない
        "yes": 0.008     # 生魚摂取後の発症率(low but non-trivial)
    },
    "R01": {
        "0_1": 0.0,
        "1_5": 0.001,
        "6_12": 0.002,
        "13_17": 0.003,
        "18_39": 0.004,
        "40_64": 0.005,
        "65_plus": 0.003
    },
    "R02": {
        "male": 0.55,  # 55:45 (PMC10353124)
        "female": 0.45
    }
}

# R67 noisy_or_params (root variable, no parent_effects needed)
# R67 is an input risk factor, doesn't need noisy_or
# But it should be in full_cpts as a root prior
cpts['R67'] = {
    "parents": [],
    "description": "生魚摂取歴。一般人口における24h以内の生魚摂取率",
    "cpt": {
        "no": 0.85,
        "yes": 0.15
    }
}

# Now add D429 to child variable noisy_or_params
# T01: under_3d dominant
nop_t01 = nop.get('T01', {})
if nop_t01 and 'parent_effects' in nop_t01:
    nop_t01['parent_effects']['D429'] = {
        "under_3d": 0.7,
        "3d_to_1w": 0.25,
        "1w_to_3w": 0.04,
        "over_3w": 0.01
    }

# T02: acute dominant (1-12h = acute)
nop_t02 = nop.get('T02', {})
if nop_t02 and 'parent_effects' in nop_t02:
    nop_t02['parent_effects']['D429'] = {
        "sudden": 0.25,   # 1-2h cases
        "acute": 0.65,    # 3-12h cases (majority)
        "subacute": 0.08,
        "chronic": 0.02
    }

# S12: abdominal pain present 78% (PMC10353124)
nop_s12 = nop.get('S12', {})
if nop_s12 and 'parent_effects' in nop_s12:
    nop_s12['parent_effects']['D429'] = 0.78

# S89: epigastric dominant (胃型90%)
nop_s89 = nop.get('S89', {})
if nop_s89 and 'parent_effects' in nop_s89:
    nop_s89['parent_effects']['D429'] = {
        "epigastric": 0.75,
        "RUQ": 0.05,
        "RLQ": 0.03,
        "LLQ": 0.02,
        "suprapubic": 0.02,
        "diffuse": 0.13
    }

# S13: nausea 67%
nop_s13 = nop.get('S13', {})
if nop_s13 and 'parent_effects' in nop_s13:
    nop_s13['parent_effects']['D429'] = 0.67

# S66: vomiting 51%
nop_s66 = nop.get('S66', {})
if nop_s66 and 'parent_effects' in nop_s66:
    nop_s66['parent_effects']['D429'] = {
        "absent": 0.49,
        "present": 0.51
    }

# E09: localized tenderness dominant
nop_e09 = nop.get('E09', {})
if nop_e09 and 'parent_effects' in nop_e09:
    nop_e09['parent_effects']['D429'] = {
        "soft_nontender": 0.15,
        "localized_tenderness": 0.8,
        "peritoneal_signs": 0.05
    }

# L01: WBC - 51% elevated, mostly mild
nop_l01 = nop.get('L01', {})
if nop_l01 and 'parent_effects' in nop_l01:
    nop_l01['parent_effects']['D429'] = {
        "low_under_4000": 0.02,
        "normal_4000_10000": 0.49,
        "high_10000_20000": 0.44,
        "very_high_over_20000": 0.05
    }

# L02: CRP - mild elevation
nop_l02 = nop.get('L02', {})
if nop_l02 and 'parent_effects' in nop_l02:
    nop_l02['parent_effects']['D429'] = {
        "normal_under_0.3": 0.35,
        "mild_0.3_3": 0.45,
        "moderate_3_10": 0.15,
        "high_over_10": 0.05
    }

# S64: severe pain dominant (satellite, may not have noisy_or yet)
if 'S64' not in nop or not nop.get('S64'):
    nop['S64'] = {
        "description": "腹痛の程度",
        "states": ["mild", "moderate", "severe"],
        "leak": {"mild": 0.3, "moderate": 0.5, "severe": 0.2},
        "parent_effects": {}
    }
nop_s64 = nop['S64']
if 'parent_effects' not in nop_s64:
    nop_s64['parent_effects'] = {}
nop_s64['parent_effects']['D429'] = {
    "mild": 0.05,
    "moderate": 0.2,
    "severe": 0.75
}

# S61: sharp/stabbing pain (satellite, may not have noisy_or yet)
if 'S61' not in nop or not nop.get('S61'):
    nop['S61'] = {
        "description": "腹痛の性状",
        "states": ["colicky", "burning_gnawing", "sharp_stabbing", "dull_aching", "tearing"],
        "leak": {"colicky": 0.2, "burning_gnawing": 0.25, "sharp_stabbing": 0.2, "dull_aching": 0.3, "tearing": 0.05},
        "parent_effects": {}
    }
nop_s61 = nop['S61']
if 'parent_effects' not in nop_s61:
    nop_s61['parent_effects'] = {}
nop_s61['parent_effects']['D429'] = {
    "colicky": 0.15,
    "burning_gnawing": 0.2,
    "sharp_stabbing": 0.5,
    "dull_aching": 0.1,
    "tearing": 0.05
}

with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print("Step 3: D429 CPTs added")
print("Done!")
