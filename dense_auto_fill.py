#!/usr/bin/env python3
"""
Dense auto-fill: For top 20 variables, add leak-value edges to ALL missing diseases.
Existing edges (clinically curated) are preserved unchanged.
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

from bn_inference import build_model
_, diseases, disease_children, noisy_or, _ = build_model(s1, s2, s3)
n = s3["noisy_or_params"]
existing = {(e["from"], e["to"]) for e in s2["edges"]}

# Top 20 variables by case frequency
target_vars = [
    "T01", "T02", "E01", "L01", "E02", "L02", "S07", "E16",
    "S04", "S13", "L11", "S12", "E05", "L04", "S05", "S01",
    "E03", "E12", "E07", "L14"
]

total_added = 0
for vid in target_vars:
    if vid not in noisy_or:
        print(f"  {vid}: NOT IN noisy_or, skip")
        continue

    leak = noisy_or[vid].get("leak", {})
    if not leak:
        print(f"  {vid}: no leak, skip")
        continue

    added = 0
    for did in diseases:
        if (did, vid) not in existing:
            # Auto-fill with leak CPT (neutral edge)
            s2["edges"].append({
                "from": did, "to": vid,
                "from_name": did, "to_name": vid,
                "reason": f"dense auto-fill (CPT=leak)"
            })
            existing.add((did, vid))
            n[vid]["parent_effects"][did] = dict(leak)  # copy leak as CPT
            added += 1

    has = sum(1 for d in diseases if (d, vid) in existing)
    print(f"  {vid}: +{added} auto-fill edges ({has}/{len(diseases)})")
    total_added += added

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal: +{total_added} edges. Now {s2['total_edges']} total.")
