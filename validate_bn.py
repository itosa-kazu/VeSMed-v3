#!/usr/bin/env python3
"""
BN整合性検証スクリプト
- Edge↔CPT同期チェック
- 状態名一致チェック (CPT vs step1, テストケース vs step1)
- 確率和=1.0チェック
- テストケース evidence の変量ID存在チェック
"""

import json, os, sys
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

step1 = load_json("step1_fever_v2.7.json")
step2 = load_json("step2_fever_edges_v4.json")
step3 = load_json("step3_fever_cpts_v2.json")
cases = load_json("real_case_test_suite.json")

# ─── Build lookup tables ────────────────────────────────────────
var_by_id = {}
for v in step1["variables"]:
    var_by_id[v["id"]] = v

nop = step3.get("noisy_or_params", {})

# edges as set of (from, to)
edge_set = set()
for e in step2["edges"]:
    edge_set.add((e["from"], e["to"]))

errors = []
warnings = []

def err(category, msg):
    errors.append(f"[{category}] {msg}")

def warn(category, msg):
    warnings.append(f"[{category}] {msg}")

# ─── 1. Edge count verification ────────────────────────────────
declared = step2.get("total_edges", -1)
actual = len(step2["edges"])
if declared != actual:
    err("EDGE_COUNT", f"total_edges={declared} but actual={actual}")

# ─── 2. Edge↔CPT sync ──────────────────────────────────────────
# 2a: Edge exists but no CPT (only for symptom/lab/exam/temporal variables)
for d_id, v_id in edge_set:
    if v_id.startswith("D") or v_id.startswith("R"):
        continue  # disease/risk nodes use full_cpts, not noisy_or_params
    if v_id not in nop:
        warn("NO_NOP", f"{v_id} not in noisy_or_params (edge {d_id}→{v_id})")
        continue
    if d_id not in nop[v_id].get("parent_effects", {}):
        err("EDGE_NO_CPT", f"Edge {d_id}→{v_id} exists but no parent_effects in step3")

# 2b: CPT exists but no edge (only for disease→symptom/lab links)
for v_id, params in nop.items():
    if v_id.startswith("D"):
        continue  # disease nodes in NOP have risk factor parents
    for d_id in params.get("parent_effects", {}):
        if not d_id.startswith("D"):
            continue  # skip risk factor parents
        if (d_id, v_id) not in edge_set:
            err("CPT_NO_EDGE", f"parent_effects {d_id}→{v_id} exists but no edge in step2")

# ─── 3. State name validation (CPT vs step1) ───────────────────
for v_id, params in nop.items():
    if v_id not in var_by_id:
        err("VAR_MISSING", f"noisy_or_params has {v_id} but not in step1")
        continue

    valid_states = set(var_by_id[v_id]["states"])

    # Check leak (scalar for binary, dict for multi-state)
    leak = params.get("leak", params.get("leak_probabilities", None))
    if isinstance(leak, dict):
        leak_states = set(leak.keys())
        if leak_states != valid_states:
            extra = leak_states - valid_states
            missing = valid_states - leak_states
            if extra:
                err("LEAK_STATE", f"{v_id} leak has invalid states: {extra}")
            if missing:
                err("LEAK_STATE", f"{v_id} leak missing states: {missing}")
        # Sum check
        s = sum(leak.values())
        if abs(s - 1.0) > 0.001:
            err("PROB_SUM", f"{v_id} leak sum={s:.4f}")

    # Check each parent_effects
    for d_id, pe in params.get("parent_effects", {}).items():
        if not isinstance(pe, dict):
            # Scalar = P(present|disease) for binary variables
            if isinstance(pe, (int, float)) and not (0.0 <= pe <= 1.0):
                err("PROB_RANGE", f"{v_id}←{d_id} scalar value {pe} out of [0,1]")
            continue
        # Disease nodes with risk factor parents use parent's states as keys
        # (different format: P(D=yes|R=state)), not child state distribution
        if v_id.startswith("D") and d_id.startswith("R"):
            continue
        pe_states = set(pe.keys())
        if pe_states != valid_states:
            extra = pe_states - valid_states
            missing = valid_states - pe_states
            if extra:
                err("CPT_STATE", f"{v_id}←{d_id} CPT has invalid states: {extra}")
            if missing:
                err("CPT_STATE", f"{v_id}←{d_id} CPT missing states: {missing}")
        # Sum check
        s = sum(pe.values())
        if abs(s - 1.0) > 0.001:
            err("PROB_SUM", f"{v_id}←{d_id} parent_effects sum={s:.4f}")

# ─── 4. Test case evidence validation ──────────────────────────
for case in cases["cases"]:
    cid = case["id"]

    # Check evidence variable IDs and states
    for v_id, state in case.get("evidence", {}).items():
        if v_id not in var_by_id:
            err("CASE_VAR", f"Case {cid}: evidence variable {v_id} not in step1")
            continue
        valid_states = var_by_id[v_id]["states"]
        if state not in valid_states:
            err("CASE_STATE", f"Case {cid}: {v_id}=\"{state}\" invalid. Valid: {valid_states}")

    # Check risk_factors variable IDs and states
    for v_id, state in case.get("risk_factors", {}).items():
        if v_id not in var_by_id:
            err("CASE_VAR", f"Case {cid}: risk_factor {v_id} not in step1")
            continue
        valid_states = var_by_id[v_id]["states"]
        if state not in valid_states:
            err("CASE_STATE", f"Case {cid}: {v_id}=\"{state}\" invalid. Valid: {valid_states}")

    # Check expected_id exists as a disease (unless OOS)
    exp = case.get("expected_id", "")
    if exp != "OOS" and exp not in var_by_id:
        err("CASE_DISEASE", f"Case {cid}: expected_id={exp} not in step1")

# ─── 5. Duplicate edge check ───────────────────────────────────
edge_counts = defaultdict(int)
for e in step2["edges"]:
    key = (e["from"], e["to"])
    edge_counts[key] += 1
for key, cnt in edge_counts.items():
    if cnt > 1:
        err("DUPE_EDGE", f"Edge {key[0]}→{key[1]} appears {cnt} times")

# ─── Output ─────────────────────────────────────────────────────
print("=" * 60)
print(f"BN Validation Report")
print(f"  step1: {len(var_by_id)} variables")
print(f"  step2: {actual} edges")
print(f"  step3: {len(nop)} noisy_or_params entries")
print(f"  cases: {len(cases['cases'])} test cases")
print("=" * 60)

# Group by category
by_cat = defaultdict(list)
for e in errors:
    cat = e.split("]")[0][1:]
    by_cat[cat].append(e)

if errors:
    print(f"\n❌ ERRORS: {len(errors)}")
    for cat in sorted(by_cat.keys()):
        items = by_cat[cat]
        print(f"\n  [{cat}] ({len(items)}件)")
        for e in sorted(items):
            print(f"    {e.split('] ', 1)[1]}")
else:
    print("\n✅ No errors found")

if warnings:
    print(f"\n⚠ WARNINGS: {len(warnings)}")
    for w in sorted(warnings):
        print(f"  {w}")

print(f"\nTotal: {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
