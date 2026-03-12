#!/usr/bin/env python3
"""
テストケース状態名エラー一括修正 (validate_bn.py CASE_STATE 26件)
- L06(インフル検査) → L14(末梢血塗抹) に変量ID変更
- L03(PCT) → L11(肝酵素) に変量ID変更
- R01/R06: binary "yes" → 正しい多値状態
- L01: 区切り値修正
- その他: S07, L15, S04, E16, S23
"""

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, "real_case_test_suite.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

fixes = {
    # ─── R16 ───
    "R16": {
        "evidence": {"S07": ("moderate", "mild")},
    },
    # ─── R59: 21M RMSF ───
    "R59": {
        "evidence": {
            "L06": "RENAME:L14",  # thrombocytopenia state is valid for L14
            "L03": "RENAME:L11:mild_elevated",  # mildly_elevated → L11 mild_elevated
        },
        "risk_factors": {"R01": ("yes", "18_39")},  # 21yo
    },
    # ─── R60: 74F Japanese Spotted Fever ───
    "R60": {
        "evidence": {
            "L06": "RENAME:L14",
            "L03": "RENAME:L11:mild_elevated",
        },
        "risk_factors": {"R06": ("yes", "domestic")},  # Japan farmer
    },
    # ─── R61: 36F Mediterranean Spotted Fever ───
    "R61": {
        "evidence": {
            "L06": "RENAME:L14",
            "L03": "RENAME:L11:very_high",  # markedly_elevated → very_high
        },
    },
    # ─── R62: 21M Dengue ───
    "R62": {
        "risk_factors": {"R01": ("yes", "18_39")},
    },
    # ─── R63: 34M Chikungunya ───
    "R63": {
        "evidence": {
            "L06": "RENAME:L14",
        },
        "risk_factors": {"R01": ("yes", "18_39")},
    },
    # ─── R64: 74M Chikungunya ───
    "R64": {
        "evidence": {
            "L06": "RENAME:L14",
        },
        "risk_factors": {"R01": ("yes", "65_plus")},  # 74yo
    },
    # ─── R65: 23M Typhoid ───
    "R65": {
        "evidence": {
            "L01": ("normal_4000_12000", "normal_4000_10000"),
            "L03": "RENAME:L11:very_high",
        },
        "risk_factors": {"R01": ("yes", "18_39")},
    },
    # ─── R66: 31M Typhoid ───
    "R66": {
        "evidence": {
            "L01": ("normal_4000_12000", "normal_4000_10000"),
            "L03": "RENAME:L11:very_high",
        },
    },
    # ─── R68: 53M Behcet's ───
    "R68": {
        "evidence": {
            "L15": ("elevated", "mild_elevated"),
            "S04": ("exertional", "on_exertion"),
        },
    },
    # ─── R69: 62M Drug fever (WBC 38k) ───
    "R69": {
        "evidence": {
            "L01": ("leukocytosis_over_12000", "very_high_over_20000"),
        },
    },
    # ─── R71: 86F PE ───
    "R71": {
        "evidence": {
            "L01": ("normal_4000_12000", "normal_4000_10000"),
        },
    },
    # ─── R73: 50M Meningitis (loss of consciousness) ───
    "R73": {
        "evidence": {
            "E16": ("comatose", "obtunded"),
        },
    },
    # ─── R75: 22F Septic arthritis (knee) ───
    "R75": {
        "evidence": {
            "S23": ("present", "monoarticular"),
        },
    },
    # ─── R76: Liver abscess ───
    "R76": {
        "evidence": {
            "L01": ("leukocytosis_over_12000", "high_10000_20000"),
        },
    },
}

fixed_count = 0
for case in data["cases"]:
    cid = case["id"]
    if cid not in fixes:
        continue

    fix = fixes[cid]

    for section in ["evidence", "risk_factors"]:
        if section not in fix:
            continue
        for var_id, action in fix[section].items():
            if isinstance(action, str) and action.startswith("RENAME:"):
                # Rename variable ID (and optionally change state)
                parts = action.split(":")
                new_var = parts[1]
                old_val = case[section].pop(var_id, None)
                if old_val is not None:
                    new_val = parts[2] if len(parts) > 2 else old_val
                    case[section][new_var] = new_val
                    print(f"  {cid}: {section} {var_id}=\"{old_val}\" → {new_var}=\"{new_val}\"")
                    fixed_count += 1
            elif isinstance(action, tuple):
                old_val, new_val = action
                if case[section].get(var_id) == old_val:
                    case[section][var_id] = new_val
                    print(f"  {cid}: {section} {var_id}=\"{old_val}\" → \"{new_val}\"")
                    fixed_count += 1
                else:
                    print(f"  {cid}: SKIP {var_id} (expected \"{old_val}\", got \"{case[section].get(var_id)}\")")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nFixed {fixed_count} state errors in test cases.")
