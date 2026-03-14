#!/usr/bin/env python3
"""
E03 blood_pressure_systolic: 2 states -> 3 states
  old: normal_over_90, hypotension_under_90
  new: normal_over_100, borderline_90_100, hypotension_under_90
"""
import json
import sys

def round2(x):
    return round(x, 2)

# ============================================================
# 2a. Update step1_fever_v2.7.json
# ============================================================
with open("step1_fever_v2.7.json", "r", encoding="utf-8") as f:
    step1 = json.load(f)

found_step1 = False
for var in step1.get("variables", step1 if isinstance(step1, list) else []):
    if isinstance(var, dict) and var.get("id") == "E03":
        old_states = var["states"]
        var["states"] = ["normal_over_100", "borderline_90_100", "hypotension_under_90"]
        print(f"step1: E03 states changed from {old_states} to {var['states']}")
        found_step1 = True
        break

if not found_step1:
    # step1 might be a dict with "variables" key or similar structure
    # Try to find E03 recursively
    def find_and_update_step1(obj):
        if isinstance(obj, dict):
            if obj.get("id") == "E03" and "states" in obj:
                old = obj["states"]
                obj["states"] = ["normal_over_100", "borderline_90_100", "hypotension_under_90"]
                print(f"step1: E03 states changed from {old} to {obj['states']}")
                return True
            for v in obj.values():
                if find_and_update_step1(v):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if find_and_update_step1(item):
                    return True
        return False
    found_step1 = find_and_update_step1(step1)

if not found_step1:
    print("ERROR: E03 not found in step1_fever_v2.7.json")
    sys.exit(1)

with open("step1_fever_v2.7.json", "w", encoding="utf-8") as f:
    json.dump(step1, f, ensure_ascii=False, indent=2)
print("step1_fever_v2.7.json updated.")

# ============================================================
# 2b. Update step3_fever_cpts_v2.json
# ============================================================
with open("step3_fever_cpts_v2.json", "r", encoding="utf-8") as f:
    cpts = json.load(f)

e03 = cpts["noisy_or_params"]["E03"]

# Update states
e03["states"] = ["normal_over_100", "borderline_90_100", "hypotension_under_90"]
print(f"CPT: E03 states updated to {e03['states']}")

# Update leak
e03["leak"] = {
    "normal_over_100": 0.90,
    "borderline_90_100": 0.07,
    "hypotension_under_90": 0.03
}
print(f"CPT: E03 leak updated to {e03['leak']}")

# Update parent_effects
for disease_id, probs in e03["parent_effects"].items():
    # Normalize key names - handle both "normal"/"hypotension" and "normal_over_90"/"hypotension_under_90"
    old_normal = None
    old_hypo = None
    normal_key = None
    hypo_key = None

    for k, v in probs.items():
        if k in ("normal", "normal_over_90"):
            old_normal = v
            normal_key = k
        elif k in ("hypotension", "hypotension_under_90"):
            old_hypo = v
            hypo_key = k

    if old_normal is None or old_hypo is None:
        print(f"WARNING: {disease_id} has unexpected keys: {probs}")
        continue

    # Determine split ratio based on hypotension probability
    if old_hypo >= 0.4:
        # HIGH hypotension - shock diseases
        ratio_normal = 0.5
        ratio_border = 0.5
    elif old_hypo >= 0.2:
        # MODERATE hypotension
        ratio_normal = 0.65
        ratio_border = 0.35
    else:
        # LOW hypotension
        ratio_normal = 0.85
        ratio_border = 0.15

    new_normal = round2(old_normal * ratio_normal)
    new_border = round2(old_normal * ratio_border)
    new_hypo = old_hypo

    # Ensure sum = 1.0
    total = new_normal + new_border + new_hypo
    if abs(total - 1.0) > 0.01:
        # Adjust normal to make sum exactly 1.0
        new_normal = round2(1.0 - new_border - new_hypo)

    e03["parent_effects"][disease_id] = {
        "normal_over_100": new_normal,
        "borderline_90_100": new_border,
        "hypotension_under_90": new_hypo
    }

    category = "HIGH" if old_hypo >= 0.4 else ("MODERATE" if old_hypo >= 0.2 else "LOW")
    print(f"  {disease_id}: ({category}) normal={old_normal}->{new_normal}, border={new_border}, hypo={old_hypo}")

with open("step3_fever_cpts_v2.json", "w", encoding="utf-8") as f:
    json.dump(cpts, f, ensure_ascii=False, indent=2)
print("step3_fever_cpts_v2.json updated.")

# ============================================================
# 2c. Update real_case_test_suite.json
# ============================================================
with open("real_case_test_suite.json", "r", encoding="utf-8") as f:
    test_suite = json.load(f)

cases_list = test_suite["cases"]
count_normal = 0
count_hypo = 0
for case in cases_list:
    evidence = case.get("evidence", {})
    if "E03" in evidence:
        old_val = evidence["E03"]
        if old_val == "normal_over_90":
            evidence["E03"] = "normal_over_100"
            count_normal += 1
        elif old_val == "hypotension_under_90":
            # stays as is
            count_hypo += 1
        else:
            print(f"WARNING: unexpected E03 value '{old_val}' in case {case.get('id', '?')}")

print(f"real_case_test_suite.json: {count_normal} normal_over_90->normal_over_100, {count_hypo} hypotension_under_90 unchanged")

with open("real_case_test_suite.json", "w", encoding="utf-8") as f:
    json.dump(test_suite, f, ensure_ascii=False, indent=2)
print("real_case_test_suite.json updated.")

print("\nAll changes applied successfully!")
