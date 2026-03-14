#!/usr/bin/env python3
"""
Batch 2: MISS案例向け辺+CPT追加スクリプト
13のMISS案例分析に基づき、臨床的に合理的な辺を追加

追加対象:
  Disease→Variable edges (14本):
    D96→L18(ANA), D98→T02, D98→T03, D69→S46, D69→S13, D69→T02, D69→S09
    D99→L01, D99→E02, D99→E04, D99→E05
    D13→S08, D13→E21, D20→T02
  Risk factor→Disease edges (2本):
    R01→D58 (Still病若年好発), R01→D60 (ANCA血管炎中高年好発)
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
STEP2 = os.path.join(BASE, "step2_fever_edges_v4.json")
STEP3 = os.path.join(BASE, "step3_fever_cpts_v2.json")

# ── Disease→Variable edges to add ──
NEW_EDGES = [
    # === D96 菊池病 (R51 rank10) ===
    {
        "from": "D96", "to": "L18",
        "from_name": "Kikuchi disease", "to_name": "ANA",
        "reason": "菊池病ではANA陰性が典型。SLE除外の重要鑑別点"
    },
    # === D98 高安動脈炎 (R115 rank13) ===
    {
        "from": "D98", "to": "T02",
        "from_name": "Takayasu arteritis", "to_name": "onset_speed",
        "reason": "高安動脈炎は緩徐発症が典型"
    },
    {
        "from": "D98", "to": "T03",
        "from_name": "Takayasu arteritis", "to_name": "fever_pattern",
        "reason": "高安動脈炎は間欠熱パターンが典型"
    },
    # === D69 腎細胞癌 (R154 rank7) ===
    {
        "from": "D69", "to": "S46",
        "from_name": "renal cell carcinoma", "to_name": "anorexia",
        "reason": "腎細胞癌の悪液質で食欲不振は高頻度（40-50%）"
    },
    {
        "from": "D69", "to": "S13",
        "from_name": "renal cell carcinoma", "to_name": "nausea_vomiting",
        "reason": "腎細胞癌の高Ca血症に伴う悪心嘔吐（20-30%）"
    },
    {
        "from": "D69", "to": "T02",
        "from_name": "renal cell carcinoma", "to_name": "onset_speed",
        "reason": "腎細胞癌は緩徐発症"
    },
    {
        "from": "D69", "to": "S09",
        "from_name": "renal cell carcinoma", "to_name": "rigors",
        "reason": "腫瘍熱で悪寒戦慄を伴うことがある（15-20%）"
    },
    # === D99 非結核性抗酸菌症 (R116 rank16) ===
    {
        "from": "D99", "to": "L01",
        "from_name": "NTM infection", "to_name": "WBC",
        "reason": "NTM感染で白血球上昇（感染に対する炎症反応）"
    },
    {
        "from": "D99", "to": "E02",
        "from_name": "NTM infection", "to_name": "heart_rate",
        "reason": "NTM肺炎での呼吸不全・発熱に伴う頻脈"
    },
    {
        "from": "D99", "to": "E04",
        "from_name": "NTM infection", "to_name": "respiratory_rate",
        "reason": "NTM肺炎で頻呼吸"
    },
    {
        "from": "D99", "to": "E05",
        "from_name": "NTM infection", "to_name": "SpO2",
        "reason": "NTM肺炎で低酸素血症"
    },
    # === D13 髄膜炎 (R17 rank6) ===
    {
        "from": "D13", "to": "S08",
        "from_name": "meningitis", "to_name": "arthralgia",
        "reason": "髄膜炎菌性髄膜炎で反応性関節炎の合併あり（10-15%）"
    },
    {
        "from": "D13", "to": "E21",
        "from_name": "meningitis", "to_name": "joint_redness_warmth",
        "reason": "髄膜炎菌の血行性播種による化膿性関節炎（5-8%）"
    },
    # === D20 急性副鼻腔炎 (R139 rank76) ===
    {
        "from": "D20", "to": "T02",
        "from_name": "acute sinusitis", "to_name": "onset_speed",
        "reason": "副鼻腔炎は数日かけて緩徐に発症"
    },
]

# ── Corresponding CPTs for disease→variable edges ──
NEW_CPTS = {
    # D96→L18: 菊池病ではANA陰性が典型（80-90%）
    "D96": {
        "L18": {"negative": 0.85, "positive": 0.15}
    },
    # D98→T02: 緩徐発症
    "D98": {
        "T02": {"sudden_hours": 0.10, "gradual_days": 0.90},
        "T03": {"continuous": 0.20, "intermittent": 0.50, "periodic": 0.20, "double_quotidian": 0.10},
    },
    # D69→S46/S13/T02/S09: 腎細胞癌の全身症状
    "D69": {
        "S46": {"absent": 0.45, "present": 0.55},
        "S13": {"absent": 0.70, "present": 0.30},
        "T02": {"sudden_hours": 0.05, "gradual_days": 0.95},
        "S09": {"absent": 0.70, "present": 0.30},
    },
    # D99→L01/E02/E04/E05: NTM肺炎の基本所見
    "D99": {
        "L01": {
            "low_under_4000": 0.05,
            "normal_4000_10000": 0.35,
            "high_10000_20000": 0.45,
            "very_high_over_20000": 0.15,
        },
        "E02": {"under_100": 0.40, "100_120": 0.40, "over_120": 0.20},
        "E04": {
            "normal_under_20": 0.30,
            "tachypnea_20_30": 0.50,
            "severe_over_30": 0.20,
        },
        "E05": {
            "normal_over_96": 0.30,
            "mild_hypoxia_93_96": 0.40,
            "severe_hypoxia_under_93": 0.30,
        },
    },
    # D13→S08/E21: 髄膜炎の関節症状（稀だが起こる）
    "D13": {
        "S08": {"absent": 0.88, "present": 0.12},
        "E21": {"absent": 0.93, "monoarticular": 0.05, "polyarticular": 0.02},
    },
    # D20→T02: 副鼻腔炎は緩徐発症
    "D20": {
        "T02": {"sudden_hours": 0.15, "gradual_days": 0.85},
    },
}

# ── Risk factor→Disease prior CPTs ──
# These modify root_priors, not noisy_or
RISK_FACTOR_CHANGES = {
    # D58 (成人Still病): 現在parents=[], 若年成人(16-35)に好発
    "D58": {
        "parents": ["R01"],
        "description": "成人Still病。若年成人に好発（16-35歳ピーク）",
        "cpt": {
            "18_39": 0.008,
            "40_64": 0.004,
            "65_plus": 0.002,
        },
    },
    # D60 (ANCA関連血管炎): 現在parents=[], 中高年に好発（50-70代）
    "D60": {
        "parents": ["R01"],
        "description": "ANCA関連血管炎。中高年に好発",
        "cpt": {
            "18_39": 0.002,
            "40_64": 0.007,
            "65_plus": 0.008,
        },
    },
}


def main():
    # Load step2
    with open(STEP2, "r", encoding="utf-8") as f:
        step2 = json.load(f)
    edges = step2["edges"]
    existing = {(e["from"], e["to"]) for e in edges}

    # Load step3
    with open(STEP3, "r", encoding="utf-8") as f:
        step3 = json.load(f)
    noisy_or = step3["noisy_or_params"]
    root_priors = step3["root_priors"]

    added_count = 0

    # ── Add disease→variable edges to step2 ──
    for edge in NEW_EDGES:
        key = (edge["from"], edge["to"])
        if key in existing:
            print(f"  SKIP: {key} already exists")
            continue
        edges.append(edge)
        existing.add(key)
        added_count += 1

    # ── Add disease→variable CPTs to step3 noisy_or ──
    for disease_id, var_cpts in NEW_CPTS.items():
        print(f"=== {disease_id} ===")
        for var_id, cpt_values in var_cpts.items():
            if var_id not in noisy_or:
                print(f"  WARNING: {var_id} not in noisy_or_params")
                continue
            pe = noisy_or[var_id]["parent_effects"]
            if disease_id in pe:
                print(f"  SKIP: {disease_id} already in {var_id} parent_effects")
                continue
            pe[disease_id] = cpt_values
            print(f"  Added {disease_id}→{var_id}: {cpt_values}")

    # ── Add risk factor→disease edges to step2 ──
    for disease_id, rf_info in RISK_FACTOR_CHANGES.items():
        for parent in rf_info["parents"]:
            key = (parent, disease_id)
            if key not in existing:
                edges.append({
                    "from": parent, "to": disease_id,
                    "from_name": parent, "to_name": disease_id,
                    "reason": rf_info["description"],
                })
                existing.add(key)
                added_count += 1

    # ── Update root_priors in step3 ──
    for disease_id, rf_info in RISK_FACTOR_CHANGES.items():
        print(f"=== {disease_id} prior update ===")
        rp = root_priors.get(disease_id, {})
        old_parents = rp.get("parents", [])
        old_cpt = rp.get("cpt", {})
        print(f"  Old: parents={old_parents}, cpt={old_cpt}")
        root_priors[disease_id] = {
            "parents": rf_info["parents"],
            "description": rf_info["description"],
            "cpt": rf_info["cpt"],
        }
        print(f"  New: parents={rf_info['parents']}, cpt={rf_info['cpt']}")

    # ── Save ──
    with open(STEP2, "w", encoding="utf-8") as f:
        json.dump(step2, f, ensure_ascii=False, indent=2)

    with open(STEP3, "w", encoding="utf-8") as f:
        json.dump(step3, f, ensure_ascii=False, indent=2)

    print(f"\n=== Added {added_count} new edges ===")
    print(f"Total edges: {len(edges)}")


if __name__ == "__main__":
    main()
