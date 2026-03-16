#!/usr/bin/env python3
"""Add D322-D326 cases from PMC search, stripping invalid risk factors."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

# Load the agent's cases
exec(open(os.path.join(BASE, "pmc_cases_d322_d326.py"), "r", encoding="utf-8").read())

# Strip invalid risk factors
valid_rf = {"R01", "R02"}
for c in cases:
    c["risk_factors"] = {k: v for k, v in c.get("risk_factors", {}).items() if k in valid_rf}

with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)
for c in cases:
    suite["cases"].append(c)
with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added {len(cases)} cases. Total: {len(suite['cases'])}")
