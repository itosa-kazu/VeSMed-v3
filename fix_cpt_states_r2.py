#!/usr/bin/env python3
"""
CPT状態名修正 Round 2:
- E12: "normal_skin"→"normal", "petechiae"→"petechiae_purpura", "erythema_nodosum"→削除(0に再配分)
- E12←D59: "vesicular"→"vesicular_dermatomal", "erythroderma"→"diffuse_erythroderma", "absent"→"normal"
- E13: "inguinal"→"generalized"
- L15←D59: "elevated_200_1000"→"mild_elevated"
- S12←D17: suprapubic=0.0 追加
- CPT_NO_EDGE 30件: step2に辺を追加
"""

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

step3 = load_json("step3_fever_cpts_v2.json")
nop = step3["noisy_or_params"]
fixed = 0

# ─── E12: Fix state names ──────────────────────────────────────
e12 = nop["E12"]
e12_renames = {
    "normal_skin": "normal",
    "petechiae": "petechiae_purpura",
}

# Fix leak
if isinstance(e12.get("leak"), dict):
    for old, new in e12_renames.items():
        if old in e12["leak"]:
            e12["leak"][new] = e12["leak"].get(new, 0) + e12["leak"].pop(old)
            fixed += 1
            print(f"  E12 leak: \"{old}\" → merged into \"{new}\"")
    # Remove erythema_nodosum from leak, redistribute to normal
    if "erythema_nodosum" in e12["leak"]:
        e12["leak"]["normal"] = e12["leak"].get("normal", 0) + e12["leak"].pop("erythema_nodosum")
        fixed += 1
        print(f"  E12 leak: removed \"erythema_nodosum\", added to \"normal\"")

# Fix parent_effects
for d_id, pe in e12.get("parent_effects", {}).items():
    if not isinstance(pe, dict):
        continue

    # Handle D59 special case (has unique invalid states)
    if d_id == "D59":
        d59_renames = {
            "normal_skin": "normal",
            "petechiae": "petechiae_purpura",
            "vesicular": "vesicular_dermatomal",
            "erythroderma": "diffuse_erythroderma",
            "absent": "normal",
        }
        for old, new in d59_renames.items():
            if old in pe:
                pe[new] = pe.get(new, 0) + pe.pop(old)
                fixed += 1
                print(f"  E12←D59: \"{old}\" → merged into \"{new}\"")
        if "erythema_nodosum" in pe:
            pe["normal"] = pe.get("normal", 0) + pe.pop("erythema_nodosum")
            fixed += 1
            print(f"  E12←D59: removed \"erythema_nodosum\", added to \"normal\"")
    else:
        # Standard renames
        for old, new in e12_renames.items():
            if old in pe:
                pe[new] = pe.get(new, 0) + pe.pop(old)
                fixed += 1
                print(f"  E12←{d_id}: \"{old}\" → merged into \"{new}\"")
        if "erythema_nodosum" in pe:
            pe["normal"] = pe.get("normal", 0) + pe.pop("erythema_nodosum")
            fixed += 1
            print(f"  E12←{d_id}: removed \"erythema_nodosum\", added to \"normal\"")

# ─── E13: "inguinal" → "generalized" ───────────────────────────
if "E13" in nop:
    for d_id, pe in nop["E13"].get("parent_effects", {}).items():
        if isinstance(pe, dict) and "inguinal" in pe:
            pe["generalized"] = pe.get("generalized", 0) + pe.pop("inguinal")
            fixed += 1
            print(f"  E13←{d_id}: \"inguinal\" → merged into \"generalized\"")

# ─── L15←D59: "elevated_200_1000" → "mild_elevated" ────────────
if "L15" in nop and "D59" in nop["L15"].get("parent_effects", {}):
    pe = nop["L15"]["parent_effects"]["D59"]
    if isinstance(pe, dict) and "elevated_200_1000" in pe:
        pe["mild_elevated"] = pe.get("mild_elevated", 0) + pe.pop("elevated_200_1000")
        fixed += 1
        print(f"  L15←D59: \"elevated_200_1000\" → \"mild_elevated\"")

# ─── S12←D17: add missing "suprapubic"=0.0 ─────────────────────
if "S12" in nop and "D17" in nop["S12"].get("parent_effects", {}):
    pe = nop["S12"]["parent_effects"]["D17"]
    if isinstance(pe, dict) and "suprapubic" not in pe:
        pe["suprapubic"] = 0.0
        fixed += 1
        print(f"  S12←D17: added missing \"suprapubic\"=0.0")

save_json("step3_fever_cpts_v2.json", step3)
print(f"\nFixed {fixed} CPT state issues in step3 (round 2).")

# ─── CPT_NO_EDGE: Add missing edges to step2 ───────────────────
step2 = load_json("step2_fever_edges_v4.json")
edge_set = set((e["from"], e["to"]) for e in step2["edges"])

missing_edges = [
    ("D100", "L02"), ("D102", "S09"), ("D32", "S09"), ("D32", "S28"),
    ("D37", "S09"), ("D42", "S09"), ("D48", "L02"), ("D49", "L01"),
    ("D51", "S13"), ("D52", "S09"), ("D53", "T03"), ("D57", "S09"),
    ("D58", "S07"), ("D62", "L28"), ("D63", "S07"), ("D64", "S08"),
    ("D67", "L22"), ("D68", "E12"), ("D68", "L01"), ("D68", "L15"),
    ("D69", "L02"), ("D80", "E09"), ("D81", "E09"), ("D88", "L02"),
    ("D90", "S07"), ("D91", "L02"), ("D92", "S17"), ("D93", "L02"),
    ("D95", "L02"), ("D99", "S07"),
]

added = 0
for d_id, v_id in missing_edges:
    if (d_id, v_id) not in edge_set:
        step2["edges"].append({
            "from": d_id, "to": v_id,
            "reason": f"CPT存在・辺欠損修正 (validate_bn検出)",
            "onset_day_range": {"min": 0, "max": 30}
        })
        edge_set.add((d_id, v_id))
        added += 1

step2["total_edges"] = len(step2["edges"])
save_json("step2_fever_edges_v4.json", step2)
print(f"\nAdded {added} missing edges to step2. Total: {step2['total_edges']}")
