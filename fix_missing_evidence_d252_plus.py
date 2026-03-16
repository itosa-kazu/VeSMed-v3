#!/usr/bin/env python3
"""
Scan D252+ case vignettes and auto-extract missing evidence variables.
Only adds values that can be unambiguously determined from the vignette text.
"""
import json, re, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

updated = 0

def add_ev(case, var_id, value):
    global updated
    if var_id not in case.get("evidence", {}):
        case["evidence"][var_id] = value
        updated += 1
        return True
    return False

def extract_number(pattern, text):
    """Extract first numeric match."""
    m = re.search(pattern, text)
    if m:
        try: return float(m.group(1))
        except: return None
    return None

for case in suite["cases"]:
    if not case.get("in_scope"): continue
    expected = case.get("expected_id", "")
    if not expected[1:].isdigit(): continue
    did_num = int(expected[1:])
    if did_num < 252: continue

    vig = case.get("vignette", "")
    ev = case.get("evidence", {})

    # === E01 体温 ===
    if "E01" not in ev:
        # Try to extract temperature
        t = extract_number(r'T\s*([\d\.]+)', vig)
        if t is None:
            t = extract_number(r'体温\s*([\d\.]+)', vig)
        if t and 35 < t < 43:
            if t < 37.5: add_ev(case, "E01", "under_37.5")
            elif t < 38.0: add_ev(case, "E01", "37.5_38.0")
            elif t < 39.0: add_ev(case, "E01", "38.0_39.0")
            elif t < 40.0: add_ev(case, "E01", "39.0_40.0")
            else: add_ev(case, "E01", "over_40.0")
        elif re.search(r'無熱|afebrile|afeb', vig, re.I):
            add_ev(case, "E01", "under_37.5")

    # === E02 心拍数 ===
    if "E02" not in ev:
        hr = extract_number(r'HR\s*(\d+)', vig)
        if hr is None:
            hr = extract_number(r'心拍\s*(\d+)', vig)
        if hr:
            if hr < 100: add_ev(case, "E02", "under_100")
            elif hr <= 120: add_ev(case, "E02", "100_120")
            else: add_ev(case, "E02", "over_120")

    # === E05 SpO2 ===
    if "E05" not in ev:
        spo2 = extract_number(r'SpO2\s*(\d+)', vig)
        if spo2 is None:
            spo2 = extract_number(r'SaO2\s*(\d+)', vig)
        if spo2:
            if spo2 > 96: add_ev(case, "E05", "normal_over_96")
            elif spo2 >= 93: add_ev(case, "E05", "mild_hypoxia_93_96")
            else: add_ev(case, "E05", "severe_hypoxia_under_93")

    # === L01 白血球数 ===
    if "L01" not in ev:
        wbc = extract_number(r'WBC\s*([\d\.]+)[kK]', vig)
        if wbc is None:
            wbc_raw = extract_number(r'WBC\s*([\d\.]+)', vig)
            if wbc_raw and wbc_raw > 100:  # likely absolute count
                wbc = wbc_raw / 1000
            else:
                wbc = wbc_raw
        if wbc:
            if wbc < 4: add_ev(case, "L01", "low_under_4000")
            elif wbc <= 10: add_ev(case, "L01", "normal_4000_10000")
            elif wbc <= 20: add_ev(case, "L01", "high_10000_20000")
            else: add_ev(case, "L01", "very_high_over_20000")

    # === L02 CRP ===
    if "L02" not in ev:
        crp = extract_number(r'CRP\s*([\d\.]+)', vig)
        if crp:
            if crp < 0.3: add_ev(case, "L02", "normal_under_0.3")
            elif crp < 3: add_ev(case, "L02", "mild_0.3_3")
            elif crp < 10: add_ev(case, "L02", "moderate_3_10")
            else: add_ev(case, "L02", "high_over_10")

    # === L11 肝酵素 ===
    if "L11" not in ev:
        ast = extract_number(r'AST\s*(\d+)', vig)
        alt = extract_number(r'ALT\s*(\d+)', vig)
        got = extract_number(r'GOT\s*(\d+)', vig)
        gpt = extract_number(r'GPT\s*(\d+)', vig)
        val = ast or alt or got or gpt
        if val:
            if val <= 40: add_ev(case, "L11", "normal")
            elif val <= 200: add_ev(case, "L11", "mild_elevated")
            else: add_ev(case, "L11", "very_high")

    # === L55 クレアチニン ===
    if "L55" not in ev:
        cr = extract_number(r'Cr\s*([\d\.]+)', vig)
        if cr is None:
            cr = extract_number(r'creatinine\s*([\d\.]+)', vig)
        if cr and cr < 30:  # sanity check (not WBC etc)
            if cr <= 1.2: add_ev(case, "L55", "normal")
            elif cr <= 3.0: add_ev(case, "L55", "mild_elevated")
            else: add_ev(case, "L55", "high_AKI")

    # === L44 電解質 ===
    if "L44" not in ev:
        na = extract_number(r'Na\s*(\d+)', vig)
        k = extract_number(r'K\s*([\d\.]+)', vig)
        if na and na < 130:
            add_ev(case, "L44", "hyponatremia")
        elif k and k > 5.5:
            add_ev(case, "L44", "hyperkalemia")
        elif na and k:
            if 130 <= na <= 145 and 3.5 <= k <= 5.5:
                add_ev(case, "L44", "normal")

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Auto-extracted {updated} evidence entries for D252+ cases")
