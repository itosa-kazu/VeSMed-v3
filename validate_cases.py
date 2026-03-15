#!/usr/bin/env python3
"""Validate test cases against step1 variable definitions.

Checks:
1. Evidence variable IDs exist in step1
2. State values are valid for each variable
3. Risk factor IDs/values are valid
4. Semantic warnings (variable name vs vignette mismatch)
"""
import json, os, sys, re

BASE = os.path.dirname(os.path.abspath(__file__))

def load(fname):
    with open(os.path.join(BASE, fname), "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    s1 = load("step1_fever_v2.7.json")
    suite = load("real_case_test_suite.json")

    # Build variable lookup
    var_map = {}
    for v in s1["variables"]:
        var_map[v["id"]] = {
            "name": v["name"],
            "name_ja": v.get("name_ja", ""),
            "states": v["states"],
            "category": v["category"]
        }

    errors = []
    warnings = []

    # Semantic hints: variable ID → expected vignette keywords
    semantic_hints = {
        "S01": {"name": "cough(咳嗽)", "keywords": ["咳", "cough", "URI", "咳嗽"]},
        "S02": {"name": "sore_throat", "keywords": ["咽頭", "sore throat", "throat"]},
        "S05": {"name": "headache(頭痛)", "keywords": ["頭痛", "headache", "head"]},
        "S06": {"name": "myalgia(筋肉痛)", "keywords": ["筋肉痛", "myalgia", "筋痛"]},
        "S10": {"name": "dysuria(排尿痛)", "keywords": ["排尿", "dysuria", "尿"]},
        "S12": {"name": "abdominal_pain(腹痛)", "keywords": ["腹痛", "abdominal", "腹部"]},
        "S15": {"name": "flank_pain(側腹部痛)", "keywords": ["側腹", "flank", "腰背"]},
        "S21": {"name": "chest_pain(胸痛)", "keywords": ["胸痛", "chest", "胸骨"]},
    }

    for case in suite["cases"]:
        cid = case["id"]
        vig = case.get("vignette", "")

        # Check evidence
        for var_id, state_val in case.get("evidence", {}).items():
            if var_id not in var_map:
                errors.append(f"[ERROR] {cid}: evidence '{var_id}' does not exist in step1")
                continue

            info = var_map[var_id]
            if state_val not in info["states"]:
                errors.append(
                    f"[ERROR] {cid}: {var_id}({info['name']}) state '{state_val}' "
                    f"is invalid. Valid: {info['states']}"
                )

            # Semantic check
            if var_id in semantic_hints and vig:
                hint = semantic_hints[var_id]
                has_keyword = any(kw in vig for kw in hint["keywords"])
                if not has_keyword:
                    warnings.append(
                        f"[WARN]  {cid}: {var_id}={state_val} ({hint['name']}) "
                        f"but vignette has none of {hint['keywords']}"
                    )

        # Check risk factors
        for var_id, state_val in case.get("risk_factors", {}).items():
            if var_id not in var_map:
                errors.append(f"[ERROR] {cid}: risk_factor '{var_id}' does not exist in step1")
                continue
            info = var_map[var_id]
            if state_val not in info["states"]:
                errors.append(
                    f"[ERROR] {cid}: {var_id}({info['name']}) state '{state_val}' "
                    f"is invalid. Valid: {info['states']}"
                )

        # Check expected_id exists as disease
        exp = case.get("expected_id", "")
        if exp and exp != "OOS" and exp not in var_map:
            errors.append(f"[ERROR] {cid}: expected_id '{exp}' does not exist in step1")

    # Print results
    if errors:
        print(f"\n=== ERRORS ({len(errors)}) ===")
        for e in errors:
            print(e)
    else:
        print("\n=== No errors found ===")

    if warnings:
        print(f"\n=== WARNINGS ({len(warnings)}) ===")
        for w in warnings:
            print(w)
    else:
        print("\n=== No warnings ===")

    print(f"\nTotal: {len(suite['cases'])} cases, {len(errors)} errors, {len(warnings)} warnings")
    return len(errors)

if __name__ == "__main__":
    sys.exit(main())
