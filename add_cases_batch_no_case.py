#!/usr/bin/env python3
"""Add PMC cases for diseases with 0 test cases - Batch 1: D65, D61, D179, D182, D188"""
import json

def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def validate_cases(cases, step1):
    var_states = {}
    for v in step1['variables']:
        var_states[v['id']] = set(v['states'])
    errors = []
    for case in cases:
        all_vars = {**case.get('evidence', {}), **case.get('risk_factors', {})}
        for var_id, state in all_vars.items():
            if var_id not in var_states:
                errors.append(f"{case['id']}: variable {var_id} not found")
            elif state not in var_states[var_id]:
                errors.append(f"{case['id']}: state '{state}' invalid for {var_id}")
    return errors

# ═══ D65 痛風 (Gout) — 10 cases ═══
D65_CASES = [
    # Case 1: PMC4445055 - 61M, chronic FUO gout
    {
        "id": "R808", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "Korean J Fam Med 2015 (PMC4445055)",
        "evidence": {
            "E01": "37.5_38.0", "E02": "100_120", "E03": "normal_over_90", "E05": "normal_over_96",
            "S08": "present", "S23": "present", "E21": "present",
            "S07": "severe", "S46": "present",
            "S90": "oligoarticular", "S91": "polyarticular", "E47": "polyarticular",
            "L01": "normal_4000_10000", "L02": "high_over_10", "L28": "very_high_over_100",
            "L23": "normal",
            "T01": "over_3w", "T02": "chronic"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R16": "yes", "R03": "current"}
    },
    # Case 2: PMC8475732 - 55M, gout storm polyarticular
    {
        "id": "R809", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "Am J Case Rep 2021 (PMC8475732)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "over_120",
            "S08": "present", "S23": "present", "E21": "present",
            "S07": "severe", "S22": "present",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L01": "high_10000_20000", "L02": "moderate_3_10", "L28": "elevated",
            "L23": "normal",
            "T01": "3d_to_1w", "T02": "acute"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R04": "yes", "R54": "yes"}
    },
    # Case 4: PMC2725931 - 75M, spinal tophaceous gout
    {
        "id": "R810", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "Neurology 2009 (PMC2725931)",
        "evidence": {
            "E01": "38.0_39.0",
            "S22": "present", "S111": "present",
            "L28": "very_high_over_100", "L23": "elevated",
            "T01": "3d_to_1w", "T02": "acute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male"}
    },
    # Case 5: PMC1924738 - 66M, polyarticular mimicking sepsis T40.1
    {
        "id": "R811", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "J Gen Intern Med 2006 (PMC1924738)",
        "evidence": {
            "E01": "over_40.0", "E02": "over_120", "E03": "hypotension_under_90",
            "E04": "tachypnea_20_30",
            "S08": "present", "S23": "present", "E21": "present",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L01": "high_10000_20000", "L02": "high_over_10", "L28": "elevated",
            "L23": "normal", "L93": "mild_low_10_12",
            "T01": "under_3d", "T02": "sudden"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male", "R16": "yes", "R54": "yes", "R62": "yes"}
    },
    # Case 6: PMC7013360 - 50M, autoinflammatory sternoclavicular
    {
        "id": "R812", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "Case Rep Rheumatol 2020 (PMC7013360)",
        "evidence": {
            "E01": "39.0_40.0",
            "S08": "present", "S23": "present", "E21": "present",
            "S07": "severe", "S16": "present", "S21": "present",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L02": "high_over_10", "L28": "elevated",
            "L23": "normal",
            "T01": "over_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R04": "yes", "R54": "yes"}
    },
    # Case 7: PMC8494596 - 41M, spinal gout back pain
    {
        "id": "R813", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "Case Rep Rheumatol 2021 (PMC8494596)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "100_120",
            "E04": "tachypnea_20_30", "E38": "elevated_140_180",
            "S08": "present", "S23": "present", "E21": "present",
            "S22": "present", "S111": "present",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L01": "high_10000_20000", "L02": "high_over_10", "L28": "elevated",
            "L23": "elevated",
            "T01": "over_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "18_39", "R02": "male"}
    },
    # Case 9: PMC3170636 - 75M, multiarticular tophaceous
    {
        "id": "R814", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "J Med Case Rep 2011 (PMC3170636)",
        "evidence": {
            "E01": "37.5_38.0",
            "S08": "present", "S23": "present", "E21": "present",
            "S18": "present", "S87": "localized_pain_redness",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L01": "high_10000_20000", "L02": "moderate_3_10", "L23": "elevated",
            "T01": "3d_to_1w", "T02": "acute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male"}
    },
    # Case 10: PMC5411531 - 80M, hemodialysis-induced
    {
        "id": "R815", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "CEN Case Rep 2012 (PMC5411531)",
        "evidence": {
            "E01": "39.0_40.0",
            "S08": "present", "S23": "present", "E21": "present",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L02": "high_over_10", "L93": "very_low_under_7",
            "L55": "high_AKI",
            "T01": "under_3d", "T02": "sudden"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male", "R50": "yes"}
    },
    # Case 11: PMC4554016 - 51M, renal transplant spinal
    {
        "id": "R816", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "Medicine (Baltimore) 2015 (PMC4554016)",
        "evidence": {
            "E01": "37.5_38.0",
            "S08": "present", "S23": "present", "E21": "present",
            "S22": "present", "S113": "present",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L02": "high_over_10", "L55": "mild_elevated",
            "L23": "normal",
            "T01": "3d_to_1w", "T02": "acute"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R05": "yes"}
    },
    # Case 12: PMC10640783 - 54M, mimicking sepsis
    {
        "id": "R817", "expected_id": "D65", "expected_name": "痛風(gout)",
        "in_scope": True, "source": "Cureus 2023 (PMC10640783)",
        "evidence": {
            "E01": "39.0_40.0", "E02": "over_120",
            "S08": "present", "S23": "present", "E21": "present",
            "S10": "present", "S38": "present", "S15": "present", "S22": "present",
            "S02": "present",
            "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular",
            "L01": "very_high_over_20000", "L02": "high_over_10", "L28": "very_high_over_100",
            "L23": "elevated", "L55": "high_AKI",
            "T01": "under_3d", "T02": "sudden"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R48": "yes", "R54": "yes"}
    },
]

if __name__ == '__main__':
    s1 = load('step1_fever_v2.7.json')

    all_cases = D65_CASES  # Will add more diseases later

    # Validate
    errors = validate_cases(all_cases, s1)
    if errors:
        print(f"VALIDATION ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
    else:
        print(f"All {len(all_cases)} cases validated OK")

        # Add to test suite
        suite = load('real_case_test_suite.json')
        existing_ids = {c['id'] for c in suite['cases']}
        added = 0
        for case in all_cases:
            if case['id'] not in existing_ids:
                suite['cases'].append(case)
                added += 1

        save('real_case_test_suite.json', suite)
        print(f"Added {added} cases. Total: {len(suite['cases'])}")
