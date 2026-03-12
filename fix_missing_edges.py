#!/usr/bin/env python3
"""
Fix missing edges detected by paper4_info_geometry.py --missing-edges

Adds 7 edges + CPTs:
  D17(肺結核) → L28(ESR), L02(CRP)
  D05(市中肺炎) → S06(筋肉痛), S07(全身倦怠感), L28(ESR)
  D55(Q熱) → T01(発熱持続期間)
  D77(DVT/PE) → T03(発熱パターン)
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── Step 2: Add edges ─────────────────────────────────────────
step2 = load_json(os.path.join(BASE, "step2_fever_edges_v4.json"))

new_edges = [
    {
        "from": "D17", "to": "L28",
        "from_name": "pulmonary_tuberculosis", "to_name": "ESR",
        "reason": "結核でESR上昇（活動性結核で高頻度）",
        "onset_day_range": {"min": 7, "max": 90}
    },
    {
        "from": "D17", "to": "L02",
        "from_name": "pulmonary_tuberculosis", "to_name": "CRP",
        "reason": "結核でCRP中等度上昇",
        "onset_day_range": {"min": 7, "max": 90}
    },
    {
        "from": "D05", "to": "S06",
        "from_name": "community_acquired_pneumonia", "to_name": "myalgia",
        "reason": "肺炎の全身症状として筋肉痛",
        "onset_day_range": {"min": 0, "max": 3}
    },
    {
        "from": "D05", "to": "S07",
        "from_name": "community_acquired_pneumonia", "to_name": "fatigue",
        "reason": "肺炎で全身倦怠感",
        "onset_day_range": {"min": 0, "max": 7}
    },
    {
        "from": "D05", "to": "L28",
        "from_name": "community_acquired_pneumonia", "to_name": "ESR",
        "reason": "細菌性肺炎でESR上昇",
        "onset_day_range": {"min": 1, "max": 14}
    },
    {
        "from": "D55", "to": "T01",
        "from_name": "Q_fever", "to_name": "fever_duration",
        "reason": "Q熱の発熱は1-3週が典型",
        "onset_day_range": {"min": 14, "max": 21}
    },
    {
        "from": "D77", "to": "T03",
        "from_name": "DVT_PE", "to_name": "fever_pattern",
        "reason": "PE関連発熱は持続性低熱が典型",
        "onset_day_range": {"min": 0, "max": 14}
    },
]

step2["edges"].extend(new_edges)
step2["total_edges"] = len(step2["edges"])

# Update changelog
existing = step2.get("changelog", "")
step2["changelog"] = existing + "; v4.5: 情報幾何分析で検出された辺欠損7本追加: D17→L28/L02, D05→S06/S07/L28, D55→T01, D77→T03"

save_json(os.path.join(BASE, "step2_fever_edges_v4.json"), step2)
print(f"Step2: {step2['total_edges']} edges (added 7)")

# ─── Step 3: Add CPTs ──────────────────────────────────────────
step3 = load_json(os.path.join(BASE, "step3_fever_cpts_v2.json"))
nop = step3["noisy_or_params"]

# D17 → L28(ESR): 活動性結核でESR上昇（80-90%でelevated, 40-50%でvery_high）
nop["L28"]["parent_effects"]["D17"] = {
    "normal": 0.05,
    "elevated": 0.45,
    "very_high_over_100": 0.50
}

# D17 → L02(CRP): 結核はCRP中等度上昇が多い
nop["L02"]["parent_effects"]["D17"] = {
    "normal_under_0.3": 0.10,
    "mild_0.3_3": 0.30,
    "moderate_3_10": 0.40,
    "high_over_10": 0.20
}

# D05 → S06(筋肉痛): 肺炎で筋肉痛は比較的common
nop["S06"]["parent_effects"]["D05"] = {
    "absent": 0.60,
    "present": 0.40
}

# D05 → S07(全身倦怠感): 肺炎で倦怠感は高頻度
nop["S07"]["parent_effects"]["D05"] = {
    "absent": 0.25,
    "mild": 0.40,
    "severe": 0.35
}

# D05 → L28(ESR): 細菌性肺炎でESR上昇
nop["L28"]["parent_effects"]["D05"] = {
    "normal": 0.10,
    "elevated": 0.50,
    "very_high_over_100": 0.40
}

# D55 → T01(発熱持続期間): Q熱は1-3週が典型
nop["T01"]["parent_effects"]["D55"] = {
    "under_3d": 0.10,
    "3d_to_1w": 0.30,
    "1w_to_3w": 0.45,
    "over_3w": 0.15
}

# D77 → T03(発熱パターン): PEの発熱は持続性低熱
nop["T03"]["parent_effects"]["D77"] = {
    "continuous": 0.60,
    "intermittent": 0.30,
    "periodic": 0.05,
    "double_quotidian": 0.05
}

save_json(os.path.join(BASE, "step3_fever_cpts_v2.json"), step3)
print("Step3: 7 parent_effects added")

# ─── Verify ────────────────────────────────────────────────────
print("\nVerification:")
for var_id, disease_id in [("L28","D17"),("L02","D17"),("S06","D05"),("S07","D05"),("L28","D05"),("T01","D55"),("T03","D77")]:
    pe = nop[var_id]["parent_effects"].get(disease_id)
    print(f"  {disease_id}→{var_id}: {pe}")
