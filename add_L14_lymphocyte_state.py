#!/usr/bin/env python3
"""Add 'lymphocyte_predominant' state to L14 (peripheral blood smear).

三位一体: step1(states追加) + step3(leak + 全parent CPT更新)
L14の既存27 parentに新stateを追加し、正規化。

臨床根拠: WBC分類でリンパ球優位(>50%)はウイルス/寄生虫感染を示唆。
  高確率: D18(EBV), D44(HIV), D45(CMV), D110(トキソプラズマ), D56(百日咳)
  中確率: D17(TB), D100(HepA), D03(COVID回復期)
  低確率: 細菌感染症(通常は好中球優位)
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# === step1: add state ===
for v in s1["variables"]:
    if v["id"] == "L14":
        v["states"].append("lymphocyte_predominant")
        print(f"step1: L14 states = {v['states']}")
        break

# === step3: update leak + all parent_effects ===
n = s3["noisy_or_params"]["L14"]

# New leak (redistribute from normal)
n["leak"] = {
    "normal": 0.82, "left_shift": 0.08, "atypical_lymphocytes": 0.03,
    "thrombocytopenia": 0.02, "eosinophilia": 0.02, "lymphocyte_predominant": 0.03
}

# Diseases with HIGH lymphocyte predominance
high_lymph = {"D18": 0.25, "D44": 0.20, "D45": 0.20, "D110": 0.20, "D56": 0.30}
# Diseases with MODERATE lymphocyte predominance
mod_lymph = {"D17": 0.10, "D100": 0.15, "D03": 0.08, "D105": 0.10}
# All others: LOW (0.03)
default_lymph = 0.03

pe = n["parent_effects"]
for d_id, cpt in pe.items():
    # Determine lymphocyte probability for this disease
    if d_id in high_lymph:
        lp = high_lymph[d_id]
    elif d_id in mod_lymph:
        lp = mod_lymph[d_id]
    else:
        lp = default_lymph

    # Add new state, steal proportionally from existing states
    old_sum = sum(cpt.values())
    scale = (old_sum - lp) / old_sum if old_sum > 0 else 1.0
    for state in cpt:
        cpt[state] *= scale
    cpt["lymphocyte_predominant"] = lp

    # Verify sum
    new_sum = sum(cpt.values())
    assert abs(new_sum - old_sum) < 0.01, f"{d_id}: sum={new_sum}"

# Also add D110 to L14 parent_effects if not already there
# (D110 should already have edge from add_d110 script, but check)
if "D110" not in pe:
    pe["D110"] = {
        "normal": 0.35, "left_shift": 0.05, "atypical_lymphocytes": 0.10,
        "thrombocytopenia": 0.10, "eosinophilia": 0.05, "lymphocyte_predominant": 0.35
    }
    print("  Added D110 to L14 parent_effects (new)")

print(f"step3: Updated leak + {len(pe)} parent CPTs with lymphocyte_predominant")

# Verify a few
for d in ["D18", "D44", "D110", "D05", "D114"]:
    if d in pe:
        s = sum(pe[d].values())
        lp = pe[d].get("lymphocyte_predominant", 0)
        print(f"  {d}: lymph={lp:.2f}, sum={s:.3f}")

# === Save ===
with open(os.path.join(BASE, "step1_fever_v2.7.json"), "w", encoding="utf-8") as f:
    json.dump(s1, f, ensure_ascii=False, indent=2)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "w", encoding="utf-8") as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print("\nSaved. Now update R183 evidence with L14=lymphocyte_predominant")
