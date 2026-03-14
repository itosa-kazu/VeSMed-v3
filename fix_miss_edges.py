#!/usr/bin/env python3
"""
MISS案例改善: D71(甲状腺クリーゼ)とD02(インフルエンザ)の辺+CPT追加

R120 MISS (甲状腺クリーゼ, rank5):
  D71に E04/E05/T02 の辺なし → 重症所見でboostされない
  追加辺(3本):
    D71→E04 (respiratory_rate): 代謝亢進→頻呼吸(80-90%)
    D71→E05 (SpO2): 心不全→肺水腫→低酸素(30-50%)
    D71→T02 (onset_speed): 誘因による急性発症

R105 MISS (インフルエンザ, rank11):
  D02に S04(呼吸困難) の辺なし
  追加辺(1本):
    D02→S04 (dyspnea): インフルエンザ肺炎で呼吸困難(15-30%)

D20(副鼻腔炎) R139:
  合併症ケース(副鼻腔炎→髄膜炎)。E16/L45は髄膜炎症状であり
  D20に追加すべきではない。E02(頻脈)のみ追加。
  追加辺(1本):
    D20→E02 (heart_rate): 重症副鼻腔炎/敗血症で頻脈
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
STEP2 = os.path.join(BASE, "step2_fever_edges_v4.json")
STEP3 = os.path.join(BASE, "step3_fever_cpts_v2.json")

NEW_EDGES = [
    # === D71 甲状腺クリーゼ (R120 rank5) ===
    {
        "from": "D71", "to": "E04",
        "from_name": "thyroid storm", "to_name": "respiratory_rate",
        "reason": "甲状腺クリーゼの代謝亢進→頻呼吸(80-90%)"
    },
    {
        "from": "D71", "to": "E05",
        "from_name": "thyroid storm", "to_name": "SpO2",
        "reason": "甲状腺クリーゼの心不全→肺水腫→低酸素血症(30-50%)"
    },
    {
        "from": "D71", "to": "T02",
        "from_name": "thyroid storm", "to_name": "onset_speed",
        "reason": "甲状腺クリーゼは誘因(感染/手術等)による急性発症"
    },
    # === D02 インフルエンザ (R105 rank11) ===
    {
        "from": "D02", "to": "S04",
        "from_name": "influenza", "to_name": "dyspnea",
        "reason": "インフルエンザ肺炎で呼吸困難(入院例の15-30%)"
    },
    # === D20 副鼻腔炎 (R139 rank51) ===
    {
        "from": "D20", "to": "E02",
        "from_name": "acute sinusitis", "to_name": "heart_rate",
        "reason": "重症/合併症を伴う副鼻腔炎で感染性頻脈(20-30%)"
    },
]

NEW_CPTS = {
    "D71": {
        # 頻呼吸: 代謝亢進→ほぼ全例で頻呼吸
        "E04": {
            "normal_under_20": 0.10,
            "tachypnea_20_30": 0.45,
            "severe_over_30": 0.45,
        },
        # SpO2: 心不全合併時に低酸素
        "E05": {
            "normal_over_96": 0.50,
            "mild_hypoxia_93_96": 0.25,
            "severe_hypoxia_under_93": 0.25,
        },
        # 発症速度: 急性発症が典型
        "T02": {"sudden_hours": 0.80, "gradual_days": 0.20},
    },
    "D02": {
        # 呼吸困難: インフルエンザ肺炎で15-30%
        "S04": {"absent": 0.75, "on_exertion": 0.15, "at_rest": 0.10},
    },
    "D20": {
        # 心拍: 重症副鼻腔炎で感染性頻脈
        "E02": {"under_100": 0.65, "100_120": 0.25, "over_120": 0.10},
    },
}


def main():
    with open(STEP2, "r", encoding="utf-8") as f:
        step2 = json.load(f)
    edges = step2["edges"]
    existing = {(e["from"], e["to"]) for e in edges}

    with open(STEP3, "r", encoding="utf-8") as f:
        step3 = json.load(f)
    noisy_or = step3["noisy_or_params"]

    added_edges = 0
    added_cpts = 0

    for edge in NEW_EDGES:
        key = (edge["from"], edge["to"])
        if key in existing:
            print(f"  SKIP edge: {key} already exists")
            continue
        edges.append(edge)
        existing.add(key)
        added_edges += 1
        print(f"  Added edge: {edge['from']}→{edge['to']} ({edge['to_name']})")

    for disease_id, var_cpts in NEW_CPTS.items():
        for var_id, cpt_values in var_cpts.items():
            if var_id not in noisy_or:
                print(f"  WARNING: {var_id} not in noisy_or_params")
                continue
            pe = noisy_or[var_id]["parent_effects"]
            if disease_id in pe:
                print(f"  SKIP CPT: {disease_id} already in {var_id}")
                continue
            pe[disease_id] = cpt_values
            added_cpts += 1
            print(f"  Added CPT: {disease_id}→{var_id}: {cpt_values}")

    with open(STEP2, "w", encoding="utf-8") as f:
        json.dump(step2, f, ensure_ascii=False, indent=2)
    with open(STEP3, "w", encoding="utf-8") as f:
        json.dump(step3, f, ensure_ascii=False, indent=2)

    print(f"\n=== Added {added_edges} edges, {added_cpts} CPTs ===")
    print(f"Total edges: {len(edges)}")


if __name__ == "__main__":
    main()
