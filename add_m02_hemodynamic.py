#!/usr/bin/env python3
"""
Add M02 (hemodynamic_compromise) as an intermediate/sign variable.
Modifies step1, step2, step3 JSON files and bn_inference.py.
"""

import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {path}")


# ============================================================
# 2a. Add M02 to step1_fever_v2.7.json
# ============================================================
print("=== Step 2a: Adding M02 to step1 ===")
step1_path = os.path.join(BASE, "step1_fever_v2.7.json")
step1 = load_json(step1_path)

# Check if M02 already exists
existing_ids = [v["id"] for v in step1["variables"]]
if "M02" in existing_ids:
    print("  M02 already exists in step1, skipping.")
else:
    m02_var = {
        "id": "M02",
        "name": "hemodynamic_compromise",
        "name_ja": "血行動態異常（ショック徴候）",
        "category": "sign",
        "states": ["stable", "compensated", "shock"],
        "note": "臨床的ショック徴候の総合判断。compensated=頻脈あるがBP維持、shock=低血圧+臓器障害"
    }
    # Insert after M01
    m01_idx = None
    for i, v in enumerate(step1["variables"]):
        if v["id"] == "M01":
            m01_idx = i
            break
    if m01_idx is not None:
        step1["variables"].insert(m01_idx + 1, m02_var)
    else:
        step1["variables"].append(m02_var)
    save_json(step1_path, step1)
    print(f"  Added M02 after index {m01_idx}")


# ============================================================
# 2b. Add edges to step2_fever_edges_v4.json
# ============================================================
print("\n=== Step 2b: Adding M02 edges to step2 ===")
step2_path = os.path.join(BASE, "step2_fever_edges_v4.json")
step2 = load_json(step2_path)

new_edges = [
    {"from": "D24", "to": "M02", "from_name": "TSS", "to_name": "hemodynamic_compromise", "reason": "TSS: 重症敗血症→ショック(80-90%)"},
    {"from": "D57", "to": "M02", "from_name": "necrotizing fasciitis", "to_name": "hemodynamic_compromise", "reason": "壊死性筋膜炎: 敗血症性ショック(50-70%)"},
    {"from": "D72", "to": "M02", "from_name": "adrenal crisis", "to_name": "hemodynamic_compromise", "reason": "副腎クリーゼ: 循環虚脱(80-90%)"},
    {"from": "D77", "to": "M02", "from_name": "DVT/PE", "to_name": "hemodynamic_compromise", "reason": "大量PE: 右心不全→ショック(30-50%)"},
    {"from": "D78", "to": "M02", "from_name": "heat stroke", "to_name": "hemodynamic_compromise", "reason": "重症熱中症: 循環不全(60-80%)"},
    {"from": "D73", "to": "M02", "from_name": "pheochromocytoma", "to_name": "hemodynamic_compromise", "reason": "褐色細胞腫クリーゼ: 血行動態不安定(40-60%)"},
    {"from": "D74", "to": "M02", "from_name": "NMS", "to_name": "hemodynamic_compromise", "reason": "悪性症候群: 自律神経障害→血行動態異常(30-50%)"},
    {"from": "D15", "to": "M02", "from_name": "malaria", "to_name": "hemodynamic_compromise", "reason": "重症マラリア: ショック(20-40%)"},
    {"from": "D89", "to": "M02", "from_name": "malignant hyperthermia", "to_name": "hemodynamic_compromise", "reason": "悪性高熱症: 循環虚脱(50-70%)"},
    {"from": "D25", "to": "M02", "from_name": "cholangitis", "to_name": "hemodynamic_compromise", "reason": "急性胆管炎(Charcot→Reynolds): 敗血症性ショック(30-50%)"},
    {"from": "D40", "to": "M02", "from_name": "CRBSI", "to_name": "hemodynamic_compromise", "reason": "カテーテル関連血流感染: 敗血症性ショック(30-50%)"},
    {"from": "D13", "to": "M02", "from_name": "meningitis", "to_name": "hemodynamic_compromise", "reason": "細菌性髄膜炎: 敗血症性ショック(30-50%)"},
    {"from": "D71", "to": "M02", "from_name": "thyroid storm", "to_name": "hemodynamic_compromise", "reason": "甲状腺クリーゼ: 高拍出性心不全→ショック(30-50%)"},
]

# Check for duplicates
existing_edges = set()
for e in step2["edges"]:
    existing_edges.add((e["from"], e["to"]))

added = 0
for e in new_edges:
    key = (e["from"], e["to"])
    if key not in existing_edges:
        step2["edges"].append(e)
        existing_edges.add(key)
        added += 1
    else:
        print(f"  Edge {e['from']}→{e['to']} already exists, skipping.")

# Update total_edges
step2["total_edges"] = len(step2["edges"])
save_json(step2_path, step2)
print(f"  Added {added} new edges. Total: {step2['total_edges']}")


# ============================================================
# 2c. Add M02 CPTs to step3_fever_cpts_v2.json
# ============================================================
print("\n=== Step 2c: Adding M02 CPTs to step3 ===")
step3_path = os.path.join(BASE, "step3_fever_cpts_v2.json")
step3 = load_json(step3_path)

m02_cpt = {
    "description": "血行動態異常（ショック徴候）",
    "states": ["stable", "compensated", "shock"],
    "leak": {"stable": 0.95, "compensated": 0.04, "shock": 0.01},
    "parent_effects": {
        "D24": {"stable": 0.05, "compensated": 0.15, "shock": 0.80},
        "D57": {"stable": 0.15, "compensated": 0.25, "shock": 0.60},
        "D72": {"stable": 0.05, "compensated": 0.15, "shock": 0.80},
        "D77": {"stable": 0.40, "compensated": 0.30, "shock": 0.30},
        "D78": {"stable": 0.15, "compensated": 0.25, "shock": 0.60},
        "D73": {"stable": 0.25, "compensated": 0.35, "shock": 0.40},
        "D74": {"stable": 0.30, "compensated": 0.40, "shock": 0.30},
        "D15": {"stable": 0.45, "compensated": 0.30, "shock": 0.25},
        "D89": {"stable": 0.15, "compensated": 0.25, "shock": 0.60},
        "D25": {"stable": 0.40, "compensated": 0.30, "shock": 0.30},
        "D40": {"stable": 0.35, "compensated": 0.35, "shock": 0.30},
        "D13": {"stable": 0.35, "compensated": 0.30, "shock": 0.35},
        "D71": {"stable": 0.30, "compensated": 0.35, "shock": 0.35},
    }
}

if "M02" in step3.get("noisy_or_params", {}):
    print("  M02 already exists in step3 noisy_or_params, skipping.")
else:
    step3["noisy_or_params"]["M02"] = m02_cpt
    save_json(step3_path, step3)
    print("  Added M02 CPT to noisy_or_params")


# ============================================================
# 2d. Update bn_inference.py
# ============================================================
print("\n=== Step 2d: Updating bn_inference.py ===")
bn_path = os.path.join(BASE, "bn_inference.py")
with open(bn_path, "r", encoding="utf-8") as f:
    content = f.read()

changes = 0

# Change 1: build_model() - disease_children pattern
old1 = 'if frm.startswith("D") or frm == "M01":'
new1 = 'if frm.startswith("D") or frm.startswith("M"):'
if old1 in content:
    content = content.replace(old1, new1, 1)  # Replace first occurrence (build_model)
    changes += 1
    print("  Updated build_model(): disease_children pattern")
else:
    print("  build_model() pattern not found or already updated")

# Change 2: compute_idf_disc() - same pattern (second occurrence)
# After the first replacement, find remaining occurrences
if old1 in content:
    content = content.replace(old1, new1, 1)  # Replace second occurrence (compute_idf_disc)
    changes += 1
    print("  Updated compute_idf_disc(): edge_count pattern")
else:
    print("  compute_idf_disc() pattern not found or already updated")

# Change 3: infer() - skip M nodes from scoring as diseases
old3 = '        if d == "M01":\n            continue'
new3 = '        if d.startswith("M"):\n            continue'
if old3 in content:
    content = content.replace(old3, new3)
    changes += 1
    print("  Updated infer(): skip M-prefix nodes")
else:
    print("  infer() M01 skip pattern not found or already updated")

# Change 4: next_best_test() - also has M01 skip
old4 = '                if d == "M01":\n                    continue'
new4 = '                if d.startswith("M"):\n                    continue'
if old4 in content:
    content = content.replace(old4, new4)
    changes += 1
    print("  Updated next_best_test(): skip M-prefix nodes")
else:
    print("  next_best_test() M01 skip pattern not found or already updated")

with open(bn_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"  Total changes to bn_inference.py: {changes}")

print("\n=== Done! ===")
