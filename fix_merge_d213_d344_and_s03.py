#!/usr/bin/env python3
"""
1. Merge D213 into D344 (duplicate 収縮性心膜炎)
2. Fix S03 (鼻汁・鼻閉) missing from noisy_or_params
3. Add S03 edges for RSV/群発頭痛/H.flu etc.
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# ============================================================
# Part 1: Merge D213 → D344
# ============================================================

# Transfer D213-only edges to D344
d213_edges = {e["to"] for e in s2["edges"] if e["from"] == "D213"}
d344_edges = {e["to"] for e in s2["edges"] if e["from"] == "D344"}
d213_only = d213_edges - d344_edges
print(f"D213-only edges to transfer to D344: {d213_only}")

n = s3["noisy_or_params"]
for vid in d213_only:
    # Copy edge
    old_edge = next(e for e in s2["edges"] if e["from"] == "D213" and e["to"] == vid)
    s2["edges"].append({
        "from": "D344", "to": vid,
        "from_name": "constrictive_pericarditis", "to_name": vid,
        "reason": old_edge["reason"].replace("D213", "D344")
    })
    # Copy CPT
    if vid in n and "D213" in n[vid].get("parent_effects", {}):
        n[vid]["parent_effects"]["D344"] = n[vid]["parent_effects"]["D213"]

# Remove D213 from step1
s1["variables"] = [v for v in s1["variables"] if v["id"] != "D213"]

# Remove D213 edges from step2
s2["edges"] = [e for e in s2["edges"] if e["from"] != "D213"]

# Remove D213 CPTs from step3
for vid in n:
    if isinstance(n[vid], dict) and "parent_effects" in n[vid]:
        n[vid]["parent_effects"].pop("D213", None)
s3.get("full_cpts", {}).pop("D213", None)

# Remove D213 from root_priors if present
s3.get("root_priors", {}).pop("D213", None)

print("D213 removed and merged into D344")

# ============================================================
# Part 2: Fix S03 in noisy_or_params
# ============================================================

# S03 exists in step1 (states: absent/clear_rhinorrhea/purulent_rhinorrhea)
# and step2 (4 edges) but NOT in step3 noisy_or_params.
# Need to add leak + states + parent_effects

n["S03"] = {
    "description": "鼻汁・鼻閉",
    "leak": {
        "absent": 0.70,
        "clear_rhinorrhea": 0.20,
        "purulent_rhinorrhea": 0.10
    },
    "parent_effects": {}
}

# Transfer existing edges' CPTs
# D01 かぜ: 水様→膿性鼻漏(90%+)
n["S03"]["parent_effects"]["D01"] = {
    "absent": 0.05, "clear_rhinorrhea": 0.55, "purulent_rhinorrhea": 0.40
}
# D20 急性副鼻腔炎: 膿性鼻漏(80%+)
n["S03"]["parent_effects"]["D20"] = {
    "absent": 0.08, "clear_rhinorrhea": 0.12, "purulent_rhinorrhea": 0.80
}
# D46 麻疹: 鼻汁(coryza, 70-80%)
n["S03"]["parent_effects"]["D46"] = {
    "absent": 0.15, "clear_rhinorrhea": 0.55, "purulent_rhinorrhea": 0.30
}
# D48 風疹: 鼻汁(30-40%)
n["S03"]["parent_effects"]["D48"] = {
    "absent": 0.50, "clear_rhinorrhea": 0.35, "purulent_rhinorrhea": 0.15
}

print(f"S03 added to noisy_or with {len(n['S03']['parent_effects'])} existing CPTs")

# ============================================================
# Part 3: Add new S03 edges
# ============================================================

existing = {(e["from"], e["to"]) for e in s2["edges"]}
added = 0

def add(did, dname, to, reason, cpt):
    global added
    if (did, to) in existing: return
    if to not in n: return
    s2["edges"].append({"from": did, "to": to, "from_name": dname, "to_name": to, "reason": reason})
    existing.add((did, to))
    n[to]["parent_effects"][did] = cpt
    added += 1

# D258 RSウイルス: 鼻汁(90%+, 最も特徴的)
add("D258", "RSV", "S03", "RSV: 鼻汁(90%+, 最も特徴的症状)",
    {"absent": 0.05, "clear_rhinorrhea": 0.60, "purulent_rhinorrhea": 0.35})

# D295 群発頭痛: 鼻汁/鼻閉(自律神経症状, 70-80%)
add("D295", "cluster_headache", "S03", "群発頭痛: 鼻汁/鼻閉(自律神経症状, 70-80%)",
    {"absent": 0.15, "clear_rhinorrhea": 0.60, "purulent_rhinorrhea": 0.25})

# D265 インフルエンザ菌肺炎: 鼻汁(上気道→下降性, 40-50%)
add("D265", "H_influenzae", "S03", "H.flu肺炎: 鼻汁(上気道症状, 40-50%)",
    {"absent": 0.40, "clear_rhinorrhea": 0.35, "purulent_rhinorrhea": 0.25})

# D02 インフルエンザ: 鼻汁(30-40%)
add("D02", "influenza", "S03", "インフルエンザ: 鼻汁(30-40%)",
    {"absent": 0.50, "clear_rhinorrhea": 0.35, "purulent_rhinorrhea": 0.15})

# D253 急性細気管支炎: 鼻汁(80%+, 初期症状)
add("D253", "bronchiolitis", "S03", "急性細気管支炎: 鼻汁(80%+, 初期症状)",
    {"absent": 0.10, "clear_rhinorrhea": 0.55, "purulent_rhinorrhea": 0.35})

# D254 クループ: 鼻汁(50-60%)
add("D254", "croup", "S03", "クループ: 鼻汁(50-60%)",
    {"absent": 0.30, "clear_rhinorrhea": 0.45, "purulent_rhinorrhea": 0.25})

# D257 百日咳: 鼻汁(カタル期, 60-70%)
add("D257", "pertussis", "S03", "百日咳: 鼻汁(カタル期, 60-70%)",
    {"absent": 0.25, "clear_rhinorrhea": 0.50, "purulent_rhinorrhea": 0.25})

# D255 アデノウイルス: 鼻汁(50-60%)
add("D255", "adenovirus", "S03", "アデノウイルス: 鼻汁(50-60%)",
    {"absent": 0.30, "clear_rhinorrhea": 0.40, "purulent_rhinorrhea": 0.30})

# D256 伝染性紅斑: 鼻汁(かぜ様, 30-40%)
add("D256", "erythema_infectiosum", "S03", "伝染性紅斑: 鼻汁(かぜ様前駆期, 30-40%)",
    {"absent": 0.55, "clear_rhinorrhea": 0.30, "purulent_rhinorrhea": 0.15})

print(f"Added {added} new S03 edges")

# ============================================================
# Save
# ============================================================
s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\nTotal: {s2['total_edges']} edges, {len([v for v in s1['variables'] if v['category']=='disease'])} diseases")
