#!/usr/bin/env python3
"""
FATAL修正: D55(Q熱)とD23(リケッチア症)の辺+CPT追加

R06 FATAL (Q熱 vs ブルセラ症):
  D53(ブルセラ)はS16/L01/L15/L16の辺あり → R06のevidenceでboostされる
  D55(Q熱)にはこれらの辺なし → 追加してQ熱の鑑別力を回復

  追加辺(5本):
    D55→S16 (night_sweats): Q熱で盗汗40-60%
    D55→L01 (WBC): Q熱で白血球正常〜低下(25-50%)
    D55→L15 (ferritin): Q熱は高フェリチン血症の代表疾患(>1000が30-50%)
    D55→L16 (LDH): Q熱肝炎→LDH上昇(40-60%)
    D55→E02 (heart_rate): Q熱で相対的徐脈(classic feature)

R59 FATAL (RMSF vs デング熱):
  D23にE25/L44/S01の辺なし → RMSF特異的所見でboostされない

  追加辺(3本):
    D23→E25 (conjunctival_injection): RMSF結膜充血30-40%
    D23→L44 (electrolytes): RMSF SIADH→低Na血症50-60%
    D23→S01 (cough): リケッチア症で乾性咳嗽15-25%
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
STEP2 = os.path.join(BASE, "step2_fever_edges_v4.json")
STEP3 = os.path.join(BASE, "step3_fever_cpts_v2.json")

# ── New edges ──
NEW_EDGES = [
    # === D55 Q熱: R06 FATAL修正 ===
    {
        "from": "D55", "to": "S16",
        "from_name": "Q fever", "to_name": "night_sweats",
        "reason": "Q熱で盗汗は40-60%に出現。ブルセラとの共通所見"
    },
    {
        "from": "D55", "to": "L01",
        "from_name": "Q fever", "to_name": "WBC",
        "reason": "Q熱で白血球正常〜低下(白血球減少25-50%)"
    },
    {
        "from": "D55", "to": "L15",
        "from_name": "Q fever", "to_name": "ferritin",
        "reason": "Q熱は高フェリチン血症の代表疾患。急性Q熱肝炎で>1000が30-50%"
    },
    {
        "from": "D55", "to": "L16",
        "from_name": "Q fever", "to_name": "LDH",
        "reason": "Q熱肝炎でLDH上昇(40-60%)"
    },
    {
        "from": "D55", "to": "E02",
        "from_name": "Q fever", "to_name": "heart_rate",
        "reason": "Q熱で相対的徐脈(高熱にもかかわらず頻脈少ない)が典型"
    },
    # === D23 リケッチア症: R59 FATAL修正 ===
    {
        "from": "D23", "to": "E25",
        "from_name": "spotted fever group rickettsiosis", "to_name": "conjunctival_injection",
        "reason": "RMSF結膜充血30-40%。重要な臨床的手がかり"
    },
    {
        "from": "D23", "to": "L44",
        "from_name": "spotted fever group rickettsiosis", "to_name": "electrolytes",
        "reason": "RMSF SIADH→低Na血症50-60%"
    },
    {
        "from": "D23", "to": "S01",
        "from_name": "spotted fever group rickettsiosis", "to_name": "cough",
        "reason": "リケッチア症で乾性咳嗽15-25%"
    },
]

# ── CPTs ──
NEW_CPTS = {
    "D55": {
        # 盗汗: Q熱で40-60%
        "S16": {"absent": 0.45, "present": 0.55},
        # WBC: 白血球減少25-50%, 正常が多い
        "L01": {
            "low_under_4000": 0.30,
            "normal_4000_10000": 0.50,
            "high_10000_20000": 0.15,
            "very_high_over_20000": 0.05,
        },
        # フェリチン: Q熱は高フェリチンの代表(Still病、HLH、Q熱)
        "L15": {
            "normal": 0.20,
            "mild_elevated": 0.30,
            "very_high_over_1000": 0.40,
            "extreme_over_10000": 0.10,
        },
        # LDH: Q熱肝炎で上昇60%
        "L16": {"normal": 0.40, "elevated": 0.60},
        # 心拍: Q熱の相対的徐脈(高熱でも頻脈少ない)
        "E02": {"under_100": 0.60, "100_120": 0.30, "over_120": 0.10},
    },
    "D23": {
        # 結膜充血: RMSF 30-40%
        "E25": {"absent": 0.65, "present": 0.35},
        # 電解質: RMSF SIADH→低Na血症50-60%
        "L44": {
            "normal": 0.40,
            "hyponatremia": 0.55,
            "hyperkalemia": 0.03,
            "other": 0.02,
        },
        # 咳嗽: リケッチア症で乾性咳嗽15-25%
        "S01": {"absent": 0.75, "dry": 0.20, "productive": 0.05},
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

    added_edges = 0
    added_cpts = 0

    # ── Add edges to step2 ──
    for edge in NEW_EDGES:
        key = (edge["from"], edge["to"])
        if key in existing:
            print(f"  SKIP edge: {key} already exists")
            continue
        edges.append(edge)
        existing.add(key)
        added_edges += 1
        print(f"  Added edge: {edge['from']}→{edge['to']} ({edge['to_name']})")

    # ── Add CPTs to step3 ──
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

    # ── Save ──
    with open(STEP2, "w", encoding="utf-8") as f:
        json.dump(step2, f, ensure_ascii=False, indent=2)

    with open(STEP3, "w", encoding="utf-8") as f:
        json.dump(step3, f, ensure_ascii=False, indent=2)

    print(f"\n=== Added {added_edges} edges, {added_cpts} CPTs ===")
    print(f"Total edges: {len(edges)}")


if __name__ == "__main__":
    main()
