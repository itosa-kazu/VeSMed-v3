#!/usr/bin/env python3
"""
CPT状態名不一致の一括修正 (validate_bn.py CPT_STATE + LEAK_STATE)
- S04: "exertional" → "on_exertion"
- T02: "acute"/"sudden"/"gradual" → "sudden_hours"/"gradual_days"
- S12: "periumbilical" 削除, "lower_abdominal"→"LLQ", "diffuse_abdominal"→"diffuse"
- L11: "high_elevated" → "very_high"
- E03: "hypotension"→"hypotension_under_90", "normal"→"normal_over_90"
- E09: "normal"→"soft_nontender"
- E12: 欠落状態の追加 (確率0で)
- D19→L14 重複辺の除去
"""

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── Fix step3 CPT states ──────────────────────────────────────
step3 = load_json("step3_fever_cpts_v2.json")
nop = step3["noisy_or_params"]
fixed = 0

def rename_state(d, old, new):
    """Rename a key in a dict, preserving its value."""
    if old in d:
        d[new] = d.pop(old)
        return True
    return False

def fix_dict_states(d, renames, context=""):
    """Apply state renames to a dict. Returns count of fixes."""
    global fixed
    count = 0
    for old, new in renames.items():
        if rename_state(d, old, new):
            count += 1
            fixed += 1
            print(f"  {context}: \"{old}\" → \"{new}\"")
    return count

# ─── S04: "exertional" → "on_exertion" ─────────────────────────
if "S04" in nop:
    s04 = nop["S04"]
    # Fix leak
    if isinstance(s04.get("leak"), dict):
        fix_dict_states(s04["leak"], {"exertional": "on_exertion"}, "S04 leak")
    # Fix parent_effects
    for d_id, pe in s04.get("parent_effects", {}).items():
        if isinstance(pe, dict):
            fix_dict_states(pe, {"exertional": "on_exertion"}, f"S04←{d_id}")

# ─── T02: "acute"/"sudden"/"gradual" → "sudden_hours"/"gradual_days" ──
if "T02" in nop:
    t02 = nop["T02"]
    renames_t02 = {"sudden": "sudden_hours", "gradual": "gradual_days"}

    # Fix leak
    if isinstance(t02.get("leak"), dict):
        # T02 has 3 states in CPT (acute/sudden/gradual) but step1 has 2 (sudden_hours/gradual_days)
        # "acute" needs to be merged with "sudden" → "sudden_hours"
        leak = t02["leak"]
        if "acute" in leak and "sudden" in leak:
            leak["sudden_hours"] = leak.pop("acute") + leak.pop("sudden")
            leak.pop("gradual", None)
            leak["gradual_days"] = 1.0 - leak["sudden_hours"]
            fixed += 1
            print(f"  T02 leak: merged acute+sudden → sudden_hours, gradual → gradual_days")
        else:
            fix_dict_states(leak, renames_t02, "T02 leak")

    # Fix parent_effects
    for d_id, pe in t02.get("parent_effects", {}).items():
        if isinstance(pe, dict):
            if "acute" in pe and "sudden" in pe:
                # Merge acute + sudden → sudden_hours
                pe["sudden_hours"] = pe.pop("acute") + pe.pop("sudden")
                pe.pop("gradual", None)
                pe["gradual_days"] = 1.0 - pe["sudden_hours"]
                fixed += 1
                print(f"  T02←{d_id}: merged acute+sudden → sudden_hours, gradual → gradual_days")
            elif "acute" in pe:
                # "acute" alone → treat as sudden_hours
                fix_dict_states(pe, {"acute": "sudden_hours", "gradual": "gradual_days"}, f"T02←{d_id}")
            else:
                fix_dict_states(pe, renames_t02, f"T02←{d_id}")

# ─── S12: fix invalid states ───────────────────────────────────
if "S12" in nop:
    s12 = nop["S12"]
    s12_renames = {
        "lower_abdominal": "LLQ",
        "diffuse_abdominal": "diffuse",
    }
    for d_id, pe in s12.get("parent_effects", {}).items():
        if isinstance(pe, dict):
            # Remove "periumbilical" (not in step1)
            if "periumbilical" in pe:
                val = pe.pop("periumbilical")
                # Redistribute to "diffuse"
                pe["diffuse"] = pe.get("diffuse", 0) + val
                fixed += 1
                print(f"  S12←{d_id}: removed \"periumbilical\" ({val}), added to \"diffuse\"")
            fix_dict_states(pe, s12_renames, f"S12←{d_id}")

# ─── L11: "high_elevated" → "very_high" ────────────────────────
if "L11" in nop:
    l11 = nop["L11"]
    if isinstance(l11.get("leak"), dict):
        fix_dict_states(l11["leak"], {"high_elevated": "very_high"}, "L11 leak")
    for d_id, pe in l11.get("parent_effects", {}).items():
        if isinstance(pe, dict):
            fix_dict_states(pe, {"high_elevated": "very_high"}, f"L11←{d_id}")

# ─── E03: state renames ────────────────────────────────────────
if "E03" in nop:
    e03 = nop["E03"]
    e03_renames = {"hypotension": "hypotension_under_90", "normal": "normal_over_90"}
    if isinstance(e03.get("leak"), dict):
        fix_dict_states(e03["leak"], e03_renames, "E03 leak")
    for d_id, pe in e03.get("parent_effects", {}).items():
        if isinstance(pe, dict):
            fix_dict_states(pe, e03_renames, f"E03←{d_id}")

# ─── E09: "normal" → "soft_nontender" ──────────────────────────
if "E09" in nop:
    e09 = nop["E09"]
    e09_renames = {"normal": "soft_nontender"}
    if isinstance(e09.get("leak"), dict):
        fix_dict_states(e09["leak"], e09_renames, "E09 leak")
    for d_id, pe in e09.get("parent_effects", {}).items():
        if isinstance(pe, dict):
            fix_dict_states(pe, e09_renames, f"E09←{d_id}")

# ─── E12: add missing states with prob 0 ───────────────────────
if "E12" in nop:
    e12 = nop["E12"]
    required_states = {"normal_skin", "maculopapular_rash", "petechiae", "erythema_nodosum",
                       "skin_necrosis", "vesicle_bulla", "purpura"}
    for d_id, pe in e12.get("parent_effects", {}).items():
        if isinstance(pe, dict):
            for s in required_states:
                if s not in pe:
                    pe[s] = 0.0
                    fixed += 1
                    print(f"  E12←{d_id}: added missing state \"{s}\"=0.0")
    # Also fix leak if needed
    if isinstance(e12.get("leak"), dict):
        for s in required_states:
            if s not in e12["leak"]:
                e12["leak"][s] = 0.0
                fixed += 1
                print(f"  E12 leak: added missing state \"{s}\"=0.0")

# ─── Fix E12←D41 prob sum (1.02 → 1.0) ─────────────────────────
if "E12" in nop and "D41" in nop["E12"].get("parent_effects", {}):
    pe = nop["E12"]["parent_effects"]["D41"]
    if isinstance(pe, dict):
        s = sum(pe.values())
        if abs(s - 1.0) > 0.001:
            # Scale all values to sum to 1.0
            for k in pe:
                pe[k] = round(pe[k] / s, 4)
            print(f"  E12←D41: rescaled sum {s:.4f} → 1.0")
            fixed += 1

save_json("step3_fever_cpts_v2.json", step3)
print(f"\nFixed {fixed} CPT state issues in step3.")

# ─── Fix duplicate edge D19→L14 in step2 ───────────────────────
step2 = load_json("step2_fever_edges_v4.json")
seen = set()
deduped = []
dupes = 0
for e in step2["edges"]:
    key = (e["from"], e["to"])
    if key in seen:
        dupes += 1
        print(f"\n  Removed duplicate edge: {key[0]}→{key[1]}")
    else:
        seen.add(key)
        deduped.append(e)
step2["edges"] = deduped
step2["total_edges"] = len(deduped)
save_json("step2_fever_edges_v4.json", step2)
print(f"Removed {dupes} duplicate edges. Total edges: {len(deduped)}")
