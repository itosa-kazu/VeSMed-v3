"""D430 機能性ディスペプシア(FD) 追加スクリプト"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Step 1: 変数追加
# ============================================================
with open('step1_fever_v2.7.json', 'r', encoding='utf-8') as f:
    s1 = json.load(f)

variables = s1['variables']

d430 = {
    "id": "D430",
    "name": "functional_dyspepsia",
    "name_ja": "機能性ディスペプシア(FD)",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "mild",
    "note": "Rome IV: 食後膨満感/早期満腹感/心窩部痛/心窩部灼熱感が6ヶ月以上。器質的疾患なし。有病率10-20%。女性1.5-2倍"
}

d429_idx = next(i for i, v in enumerate(variables) if v['id'] == 'D429')
variables.insert(d429_idx + 1, d430)

with open('step1_fever_v2.7.json', 'w', encoding='utf-8') as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
print("Step 1: D430 added")

# ============================================================
# Step 2: 辺追加
# ============================================================
with open('step2_fever_edges_v4.json', 'r', encoding='utf-8') as f:
    s2 = json.load(f)

edges = s2['edges']

new_edges = [
    # D430 -> T01 症状持続: 慢性(>6mo, Rome IV必須)
    {
        "from": "D430", "to": "T01",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "symptom_duration",
        "reason": "FD: Rome IV基準で6ヶ月以上の症状持続が必須(Rome IV criteria)",
        "onset_day_range": None
    },
    # D430 -> T02 発症速度: chronic
    {
        "from": "D430", "to": "T02",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "onset_speed",
        "reason": "FD: 緩徐発症、慢性経過が特徴(Rome IV, 6ヶ月以上)",
        "onset_day_range": None
    },
    # D430 -> S12 腹痛: EPS型27%+overlap35%=62%、全体で50-70%
    {
        "from": "D430", "to": "S12",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "abdominal_pain",
        "reason": "FD: 心窩部痛はEPS型62%(27%+35%overlap)(PMC8132673)",
        "onset_day_range": None
    },
    # D430 -> S89 腹痛部位: 心窩部に限局(定義)
    {
        "from": "D430", "to": "S89",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "abdominal_pain_region",
        "reason": "FD: 心窩部に限局が定義(Rome IV: 'localized to epigastrium')",
        "onset_day_range": None
    },
    # D430 -> S61 腹痛性状: burning_gnawing (EPS型の特徴)
    {
        "from": "D430", "to": "S61",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "abdominal_pain_quality",
        "reason": "FD EPS: 灼熱感/鈍痛が特徴(Rome IV 'epigastric burning')",
        "onset_day_range": None
    },
    # D430 -> S62 腹痛増悪因子: postprandial (PDS型の核心)
    {
        "from": "D430", "to": "S62",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "abdominal_pain_provocation",
        "reason": "FD PDS: 食後増悪が特徴(Rome IV 'meal-induced'、PMC8132673)",
        "onset_day_range": None
    },
    # D430 -> S65 腹痛時間パターン: intermittent
    {
        "from": "D430", "to": "S65",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "abdominal_pain_temporal",
        "reason": "FD: 間欠的、relapsing-remitting course(StatPearls NBK554563)",
        "onset_day_range": None
    },
    # D430 -> S13 悪心: ~40%
    {
        "from": "D430", "to": "S13",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "nausea",
        "reason": "FD: 悪心は約40%(PDS型で多い、StatPearls/PMC7012988)",
        "onset_day_range": None
    },
    # D430 -> S176 悪心増悪因子: postprandial
    {
        "from": "D430", "to": "S176",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "nausea_provocation",
        "reason": "FD: 悪心は食後に増悪(Rome IV 'postprandial nausea', PDS supportive feature)",
        "onset_day_range": None
    },
    # D430 -> S131 早期満腹感: PDS核心症状 ~55%
    {
        "from": "D430", "to": "S131",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "early_satiety",
        "reason": "FD PDS: 早期満腹感はPDS定義症状(38%PDS+35%overlap≈55%, PMC8132673)",
        "onset_day_range": None
    },
    # D430 -> E44 腹部膨満: mild (~50-60%)
    {
        "from": "D430", "to": "E44",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "abdominal_distention",
        "reason": "FD: 腹部膨満はPDS supportive feature、約50-60%(PMC7012988 highest subscore)",
        "onset_day_range": None
    },
    # D430 -> E01 体温: 正常(定義上)
    {
        "from": "D430", "to": "E01",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "temperature",
        "reason": "FD: 発熱なし(器質的疾患除外が前提、Rome IV)",
        "onset_day_range": None
    },
    # D430 -> L01 WBC: 正常
    {
        "from": "D430", "to": "L01",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "WBC",
        "reason": "FD: WBC正常(器質的疾患除外、AAFP 2020)",
        "onset_day_range": None
    },
    # D430 -> L02 CRP: 正常
    {
        "from": "D430", "to": "L02",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "CRP",
        "reason": "FD: CRP正常(器質的疾患除外、AAFP 2020)",
        "onset_day_range": None
    },
    # D430 -> E09 腹部触診: soft or mild tenderness
    {
        "from": "D430", "to": "E09",
        "from_name": "機能性ディスペプシア(FD)", "to_name": "abdominal_exam",
        "reason": "FD: 身体所見は正常~軽度心窩部圧痛。腹膜刺激徴候なし",
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

# D430 disease CPT: no special risk factor parents
# Prevalence ~10-20% in general pop, but as "presenting complaint" much lower
cpts['D430'] = {
    "parents": [],
    "description": "機能性ディスペプシア。有病率10-20%だが発症確率としては低め",
    "cpt": {
        "no": 0.97,
        "yes": 0.03
    },
    "R01": {
        "0_1": 0.0,
        "1_5": 0.0,
        "6_12": 0.001,
        "13_17": 0.005,
        "18_39": 0.008,     # 18-34歳が最多(高所得国, Nature 2024)
        "40_64": 0.006,
        "65_plus": 0.003
    },
    "R02": {
        "male": 0.4,   # F:M = 1.5-2:1 (PMC10553146)
        "female": 0.6
    }
}

# T01: over_3w dominant (chronic >6mo)
if 'T01' in nop and 'parent_effects' in nop['T01']:
    nop['T01']['parent_effects']['D430'] = {
        "under_3d": 0.01,
        "3d_to_1w": 0.02,
        "1w_to_3w": 0.07,
        "over_3w": 0.9
    }

# T02: chronic dominant
if 'T02' in nop and 'parent_effects' in nop['T02']:
    nop['T02']['parent_effects']['D430'] = {
        "sudden": 0.02,
        "acute": 0.05,
        "subacute": 0.18,
        "chronic": 0.75
    }

# S12: abdominal pain ~62% (EPS 27% + overlap 35%)
if 'S12' in nop and 'parent_effects' in nop['S12']:
    nop['S12']['parent_effects']['D430'] = 0.62

# S89: epigastric dominant (by definition)
if 'S89' in nop and 'parent_effects' in nop['S89']:
    nop['S89']['parent_effects']['D430'] = {
        "epigastric": 0.85,
        "RUQ": 0.03,
        "RLQ": 0.01,
        "LLQ": 0.01,
        "suprapubic": 0.01,
        "diffuse": 0.09
    }

# S61: burning_gnawing dominant (EPS: epigastric burning)
if 'S61' not in nop or not nop.get('S61'):
    nop['S61'] = {
        "description": "腹痛の性状",
        "states": ["colicky", "burning_gnawing", "sharp_stabbing", "dull_aching", "tearing"],
        "leak": {"colicky": 0.2, "burning_gnawing": 0.25, "sharp_stabbing": 0.2, "dull_aching": 0.3, "tearing": 0.05},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['S61']:
    nop['S61']['parent_effects'] = {}
nop['S61']['parent_effects']['D430'] = {
    "colicky": 0.05,
    "burning_gnawing": 0.55,   # EPS burning is hallmark
    "sharp_stabbing": 0.05,
    "dull_aching": 0.3,
    "tearing": 0.05
}

# S62: postprandial dominant (PDS meal-induced)
if 'S62' not in nop or not nop.get('S62'):
    nop['S62'] = {
        "description": "腹痛の増悪/緩和因子",
        "states": ["none_identified", "postprandial", "relieved_by_food", "worse_with_movement", "relieved_by_leaning_forward"],
        "leak": {"none_identified": 0.4, "postprandial": 0.2, "relieved_by_food": 0.15, "worse_with_movement": 0.15, "relieved_by_leaning_forward": 0.1},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['S62']:
    nop['S62']['parent_effects'] = {}
nop['S62']['parent_effects']['D430'] = {
    "none_identified": 0.1,
    "postprandial": 0.7,       # PDS: meal-induced is defining feature
    "relieved_by_food": 0.05,  # Not typical for FD
    "worse_with_movement": 0.05,
    "relieved_by_leaning_forward": 0.1
}

# S65: intermittent (relapsing-remitting)
if 'S65' not in nop or not nop.get('S65'):
    nop['S65'] = {
        "description": "腹痛の時間パターン",
        "states": ["constant", "intermittent_colicky", "progressive", "migratory"],
        "leak": {"constant": 0.3, "intermittent_colicky": 0.4, "progressive": 0.2, "migratory": 0.1},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['S65']:
    nop['S65']['parent_effects'] = {}
nop['S65']['parent_effects']['D430'] = {
    "constant": 0.15,
    "intermittent_colicky": 0.65,  # relapsing-remitting
    "progressive": 0.1,
    "migratory": 0.1
}

# S13: nausea ~40%
if 'S13' in nop and 'parent_effects' in nop['S13']:
    nop['S13']['parent_effects']['D430'] = 0.4

# S176: postprandial nausea
if 'S176' not in nop or not nop.get('S176'):
    nop['S176'] = {
        "description": "悪心の増悪因子",
        "states": ["none_identified", "postprandial", "positional", "medication_related", "morning"],
        "leak": {"none_identified": 0.4, "postprandial": 0.2, "positional": 0.1, "medication_related": 0.2, "morning": 0.1},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['S176']:
    nop['S176']['parent_effects'] = {}
nop['S176']['parent_effects']['D430'] = {
    "none_identified": 0.15,
    "postprandial": 0.7,    # PDS: postprandial nausea
    "positional": 0.05,
    "medication_related": 0.05,
    "morning": 0.05
}

# S131: early satiety ~55%
if 'S131' not in nop or not nop.get('S131'):
    nop['S131'] = {
        "description": "早期満腹感",
        "states": ["absent", "present"],
        "leak": {"absent": 0.95, "present": 0.05},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['S131']:
    nop['S131']['parent_effects'] = {}
nop['S131']['parent_effects']['D430'] = {
    "absent": 0.45,
    "present": 0.55
}

# E44: abdominal distention mild ~55%
if 'E44' not in nop or not nop.get('E44'):
    nop['E44'] = {
        "description": "腹部膨満",
        "states": ["absent", "mild", "severe"],
        "leak": {"absent": 0.85, "mild": 0.12, "severe": 0.03},
        "parent_effects": {}
    }
if 'parent_effects' not in nop['E44']:
    nop['E44']['parent_effects'] = {}
nop['E44']['parent_effects']['D430'] = {
    "absent": 0.4,
    "mild": 0.5,       # bloating is common supportive feature
    "severe": 0.1
}

# E01: afebrile (by definition)
if 'E01' in nop and 'parent_effects' in nop['E01']:
    nop['E01']['parent_effects']['D430'] = {
        "under_37.5": 0.95,
        "37.5_38.0": 0.04,
        "38.0_39.0": 0.008,
        "39.0_40.0": 0.001,
        "over_40.0": 0.0005,
        "hypothermia_under_35": 0.0005
    }

# L01: WBC normal
if 'L01' in nop and 'parent_effects' in nop['L01']:
    nop['L01']['parent_effects']['D430'] = {
        "low_under_4000": 0.03,
        "normal_4000_10000": 0.92,
        "high_10000_20000": 0.04,
        "very_high_over_20000": 0.01
    }

# L02: CRP normal
if 'L02' in nop and 'parent_effects' in nop['L02']:
    nop['L02']['parent_effects']['D430'] = {
        "normal_under_0.3": 0.88,
        "mild_0.3_3": 0.1,
        "moderate_3_10": 0.015,
        "high_over_10": 0.005
    }

# E09: soft or mild tenderness
if 'E09' in nop and 'parent_effects' in nop['E09']:
    nop['E09']['parent_effects']['D430'] = {
        "soft_nontender": 0.55,
        "localized_tenderness": 0.43,
        "peritoneal_signs": 0.02
    }

with open('step3_fever_cpts_v2.json', 'w', encoding='utf-8') as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print("Step 3: D430 CPTs added")
print("Done!")
