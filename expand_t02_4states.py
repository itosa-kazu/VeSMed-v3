#!/usr/bin/env python3
"""
Expand T02 from 2 states to 4 states.
sudden_hours → sudden_minutes + acute_hours
gradual_days → subacute_weeks + chronic_months

Uses T01 CPT distribution to guide the split.
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# 1. Update step1: T02 states
for v in s1["variables"]:
    if v["id"] == "T02":
        v["states"] = ["sudden_minutes", "acute_hours", "subacute_weeks", "chronic_months"]
        v["note"] = "sudden_minutes: 超急性(秒~分,SAH/解離/心停止)。acute_hours: 急性(時間~1-2日,感染症/中毒)。subacute_weeks: 亜急性(数日~数週,結核/自己免疫)。chronic_months: 慢性(数週~数月,腫瘍/変性)"
        break

# 2. Update step3: T02 leak
n = s3["noisy_or_params"]
if "T02" in n and isinstance(n["T02"], dict):
    # Old leak: sudden=0.60, gradual=0.40
    # New: 救急外来ベース → 超急性15% + 急性45% + 亜急性25% + 慢性15%
    n["T02"]["leak"] = {
        "sudden_minutes": 0.15,
        "acute_hours": 0.45,
        "subacute_weeks": 0.25,
        "chronic_months": 0.15
    }
    if "states" in n["T02"]:
        n["T02"]["states"] = ["sudden_minutes", "acute_hours", "subacute_weeks", "chronic_months"]

# 3. Update step3: T02 CPTs for all diseases
# Use T01 CPT to guide split:
# If T01 has high under_3d → disease is acute → sudden_hours maps to sudden_minutes + acute_hours
# If T01 has high over_3w → disease is chronic → gradual_days maps to chronic_months heavy

t01_pe = {}
if "T01" in n and isinstance(n["T01"], dict):
    t01_pe = n["T01"].get("parent_effects", {})

pe = n["T02"].get("parent_effects", {})
new_pe = {}

for did, old_cpt in pe.items():
    old_sudden = old_cpt.get("sudden_hours", 0.5)
    old_gradual = old_cpt.get("gradual_days", 0.5)

    # Get T01 distribution for this disease to guide split
    t01 = t01_pe.get(did, {"under_3d": 0.40, "3d_to_1w": 0.30, "1w_to_3w": 0.20, "over_3w": 0.10})
    t01_acute = t01.get("under_3d", 0.40)  # proportion that's very acute
    t01_chronic = t01.get("over_3w", 0.10)  # proportion that's chronic

    # Split sudden_hours:
    # High T01 under_3d + high sudden → more sudden_minutes
    # diseases like SAH (sudden=0.95, T01 under_3d=0.90) → sudden_minutes dominant
    # diseases like flu (sudden=0.50, T01 under_3d=0.40) → acute_hours dominant
    if old_sudden > 0.01:
        # Fraction of "sudden" that is truly sudden (minutes) vs acute (hours)
        # Use T01 under_3d as proxy: higher → more of the "sudden" is truly sudden
        frac_minutes = min(t01_acute * 0.5, 0.8)  # cap at 80%
        if old_sudden > 0.80:  # very sudden diseases
            frac_minutes = max(frac_minutes, 0.5)
        sudden_minutes = old_sudden * frac_minutes
        acute_hours = old_sudden * (1 - frac_minutes)
    else:
        sudden_minutes = 0.01
        acute_hours = 0.01

    # Split gradual_days:
    # High T01 over_3w → more chronic_months
    # High T01 1w_to_3w → more subacute_weeks
    if old_gradual > 0.01:
        frac_chronic = min(t01_chronic * 1.5 + 0.1, 0.8)  # base 10% + T01 influence
        subacute_weeks = old_gradual * (1 - frac_chronic)
        chronic_months = old_gradual * frac_chronic
    else:
        subacute_weeks = 0.01
        chronic_months = 0.01

    # Normalize
    total = sudden_minutes + acute_hours + subacute_weeks + chronic_months
    new_pe[did] = {
        "sudden_minutes": round(sudden_minutes / total, 3),
        "acute_hours": round(acute_hours / total, 3),
        "subacute_weeks": round(subacute_weeks / total, 3),
        "chronic_months": round(chronic_months / total, 3)
    }
    # Fix rounding
    s = sum(new_pe[did].values())
    if abs(s - 1.0) > 0.01:
        new_pe[did]["acute_hours"] += (1.0 - s)

n["T02"]["parent_effects"] = new_pe

# 4. Update case evidence
# Map old values to new based on T01 evidence
remap_count = 0
for case in suite["cases"]:
    ev = case.get("evidence", {})
    if "T02" not in ev:
        continue
    old_val = ev["T02"]
    t01_val = ev.get("T01", "3d_to_1w")

    if old_val == "sudden_hours":
        # Check T01 to decide minutes vs hours
        if t01_val == "under_3d":
            # Could be either. Check vignette for clues
            vig = case.get("vignette", "").lower()
            if any(k in vig for k in ["突然", "突発", "雷鳴", "thunderclap", "数秒", "数分", "瞬時"]):
                ev["T02"] = "sudden_minutes"
            else:
                ev["T02"] = "acute_hours"
        else:
            ev["T02"] = "acute_hours"
    elif old_val == "gradual_days":
        if t01_val in ["over_3w"]:
            ev["T02"] = "chronic_months"
        elif t01_val in ["1w_to_3w"]:
            ev["T02"] = "subacute_weeks"
        elif t01_val in ["3d_to_1w"]:
            ev["T02"] = "subacute_weeks"
        else:
            ev["T02"] = "acute_hours"  # gradual but under_3d → still acute pace
    remap_count += 1

# Save
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2),
                     ("step3_fever_cpts_v2.json", s3), ("real_case_test_suite.json", suite)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"T02 expanded: 2 states → 4 states")
print(f"CPTs remapped: {len(new_pe)} diseases")
print(f"Cases remapped: {remap_count}")

# Verify
from collections import Counter
new_vals = Counter()
for c in suite["cases"]:
    if "T02" in c.get("evidence",{}):
        new_vals[c["evidence"]["T02"]] += 1
print(f"New case distribution: {dict(new_vals)}")
