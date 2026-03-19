#!/usr/bin/env python3
"""Add PMC cases for D61 PMR, D179 DILI, D188 Eosinophilic Pneumonia"""
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

# ═══ D61 リウマチ性多発筋痛症(PMR) — 6 cases ═══
D61_CASES = [
    {
        "id": "R818", "expected_id": "D61", "expected_name": "リウマチ性多発筋痛症(PMR)",
        "in_scope": True, "source": "Case Rep Med 2018 (PMC6052374)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "under_100", "E03": "normal_over_90",
            "E04": "tachypnea_20_30",
            "S113": "present", "S28": "present", "S06": "present",
            "S27": "present", "S145": "over_30min",
            "S180": "proximal_girdle", "S07": "severe",
            "L01": "normal_4000_10000", "L28": "elevated", "L02": "high_over_10",
            "L11": "mild_elevated", "L17": "normal", "L88": "negative",
            "T01": "1w_to_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "40_64", "R02": "male"}
    },
    {
        "id": "R819", "expected_id": "D61", "expected_name": "リウマチ性多発筋痛症(PMR)",
        "in_scope": True, "source": "Case Rep Rheumatol 2018 (PMC6052921)",
        "evidence": {
            "E01": "37.5_38.0",
            "S113": "present", "S06": "present",
            "S27": "present", "S145": "over_1hour",
            "S180": "proximal_girdle", "S07": "severe",
            "L28": "very_high_over_100", "L02": "high_over_10",
            "L93": "low_7_10", "L11": "mild_elevated",
            "L104": "markedly_elevated", "L103": "moderate_elevated",
            "L88": "negative", "L18": "negative", "L19": "negative",
            "T01": "over_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "female", "R21": "yes"}
    },
    {
        "id": "R820", "expected_id": "D61", "expected_name": "リウマチ性多発筋痛症(PMR)",
        "in_scope": True, "source": "Cureus 2022 (PMC8943385)",
        "evidence": {
            "E01": "37.5_38.0",
            "S113": "present", "S28": "present", "S06": "present",
            "S27": "present", "S145": "over_1hour",
            "S180": "proximal_girdle", "S17": "present", "S07": "severe",
            "L28": "elevated", "L02": "moderate_3_10",
            "L93": "mild_low_10_12", "L100": "high_over_400k", "L70": "mildly_low",
            "L88": "negative", "L76": "negative", "L19": "negative",
            "T01": "over_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "female", "R18": "yes"}
    },
    {
        "id": "R821", "expected_id": "D61", "expected_name": "リウマチ性多発筋痛症(PMR)",
        "in_scope": True, "source": "Cases J 2009 (PMC2984339)",
        "evidence": {
            "E01": "37.5_38.0",
            "S113": "present", "S22": "present", "S28": "present",
            "S06": "present", "S10": "present",
            "S180": "proximal_girdle", "T03": "intermittent",
            "L28": "very_high_over_100", "L02": "high_over_10",
            "L93": "low_7_10", "L100": "high_over_400k",
            "L15": "mild_elevated", "L70": "mildly_low",
            "L88": "negative", "L19": "negative", "L09": "negative",
            "T01": "over_3w", "T02": "chronic"
        },
        "risk_factors": {"R01": "40_64", "R02": "female"}
    },
    {
        "id": "R822", "expected_id": "D61", "expected_name": "リウマチ性多発筋痛症(PMR)",
        "in_scope": True, "source": "Case Rep Med 2018 (PMC6081045)",
        "evidence": {
            "E01": "38.0_39.0",
            "S112": "present", "S113": "present", "S06": "present",
            "S27": "present", "S180": "proximal_girdle",
            "S46": "present", "S17": "present", "S16": "present",
            "S07": "severe",
            "L28": "very_high_over_100", "L02": "high_over_10",
            "L93": "low_7_10", "L100": "high_over_400k",
            "L20": "elevated", "L88": "negative",
            "T01": "over_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "female"}
    },
    {
        "id": "R823", "expected_id": "D61", "expected_name": "リウマチ性多発筋痛症(PMR)",
        "in_scope": True, "source": "Case Rep Rheumatol 2013 (PMC3542932)",
        "evidence": {
            "E01": "37.5_38.0",
            "S112": "present", "S113": "present", "S28": "present",
            "S06": "present", "S27": "present",
            "S180": "proximal_girdle", "S46": "present", "S07": "severe",
            "L01": "high_10000_20000", "L28": "elevated", "L02": "high_over_10",
            "L93": "low_7_10",
            "L104": "moderate_elevated", "L103": "moderate_elevated",
            "L88": "negative", "L18": "negative", "L19": "negative",
            "T01": "1w_to_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male"}
    },
]

# ═══ D179 薬剤性肝障害(DILI) — 10 cases ═══
D179_CASES = [
    {
        "id": "R824", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Case Rep Gastroenterol 2023 (PMC9908420)",
        "evidence": {
            "E01": "37.5_38.0", "E02": "over_120", "E03": "normal_over_90",
            "E04": "severe_over_30", "E05": "normal_over_96",
            "E18": "present", "S07": "mild", "S18": "present",
            "L11": "mild_elevated", "L104": "markedly_elevated",
            "L87": "direct_dominant", "L01": "high_10000_20000",
            "L02": "high_over_10", "L55": "high_AKI",
            "L66": "cholestatic",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R825", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Asian J Neurosurg 2019 (PMC6703052)",
        "evidence": {
            "E01": "39.0_40.0",
            "L11": "very_high", "L66": "hepatocellular",
            "T01": "under_3d", "T02": "sudden"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R826", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Am J Case Rep 2018 (PMC6181557-1)",
        "evidence": {
            "E01": "39.0_40.0", "E68": "present",
            "S96": "generalized", "E12": "maculopapular_rash",
            "S18": "present", "S13": "present", "S12": "present", "S07": "mild",
            "L11": "very_high", "L104": "moderate_elevated",
            "L87": "direct_dominant",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "18_39", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R827", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Am J Case Rep 2018 (PMC6181557-2)",
        "evidence": {
            "E01": "39.0_40.0", "S05": "mild", "S79": "present",
            "E18": "present",
            "L01": "high_10000_20000", "L11": "very_high",
            "L104": "markedly_elevated", "L87": "direct_dominant",
            "L66": "cholestatic",
            "T01": "1w_to_3w", "T02": "acute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R828", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "BMJ Case Rep 2015 (PMC4488648)",
        "evidence": {
            "E01": "37.5_38.0", "T03": "intermittent",
            "S16": "present", "S07": "severe", "S13": "present",
            "L02": "high_over_10", "L11": "very_high",
            "L104": "moderate_elevated", "L103": "markedly_elevated",
            "L15": "very_high_over_1000",
            "T01": "1w_to_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R829", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Eur J Hosp Pharm 2021 (PMC8899667)",
        "evidence": {
            "E01": "39.0_40.0",
            "L11": "very_high", "L100": "low_50k_150k",
            "L14": "eosinophilia", "L01": "very_high_over_20000",
            "L02": "high_over_10", "L16": "elevated",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "18_39", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R830", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Clin Case Rep 2025 (PMC12682597)",
        "evidence": {
            "E01": "37.5_38.0", "S02": "present", "S78": "present",
            "S07": "mild", "E18": "present",
            "L11": "mild_elevated", "L87": "direct_dominant",
            "L104": "mild_elevated", "L100": "low_50k_150k",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "18_39", "R02": "female", "R08": "yes"}
    },
    {
        "id": "R831", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Medicine (Baltimore) 2022 (PMC9524870)",
        "evidence": {
            "E01": "39.0_40.0", "E02": "under_100", "E03": "normal_over_90",
            "E38": "elevated_140_180", "E04": "normal_under_20", "E05": "normal_over_96",
            "S96": "generalized", "S18": "present", "S07": "mild", "S46": "present",
            "T03": "intermittent",
            "L11": "very_high", "L104": "moderate_elevated",
            "L87": "direct_dominant", "L01": "normal_4000_10000",
            "L02": "moderate_3_10", "L03": "high_over_0.5",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "65_plus", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R832", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "Cureus 2022 (PMC9705226)",
        "evidence": {
            "E01": "37.5_38.0", "S07": "severe",
            "S18": "present", "E12": "diffuse_erythroderma",
            "E18": "present",
            "L11": "very_high", "L104": "markedly_elevated",
            "L87": "direct_dominant", "L14": "eosinophilia",
            "L100": "very_low_under_50k", "L55": "high_AKI",
            "T01": "1w_to_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R08": "yes"}
    },
    {
        "id": "R833", "expected_id": "D179", "expected_name": "薬剤性肝障害(DILI)",
        "in_scope": True, "source": "BMJ Case Rep 2017 (PMC5580171)",
        "evidence": {
            "E01": "38.0_39.0",
            "S96": "generalized", "S18": "present", "E12": "maculopapular_rash",
            "S12": "present", "S66": "present", "S14": "present", "S02": "present",
            "L11": "very_high", "L104": "moderate_elevated",
            "L02": "moderate_3_10", "L14": "eosinophilia",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "18_39", "R02": "female", "R08": "yes"}
    },
]

# ═══ D188 好酸球性肺炎 — 8 cases ═══
D188_CASES = [
    {
        "id": "R840", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "Cureus 2023 (PMC10615121)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "100_120", "E05": "severe_hypoxia_under_93",
            "S01": "present", "S04": "at_rest", "S21": "present",
            "S09": "present", "S07": "severe",
            "L01": "high_10000_20000", "L02": "high_over_10",
            "L03": "low_under_0.25", "L14": "normal", "L35": "GGO",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "18_39", "R02": "male", "R03": "former"}
    },
    {
        "id": "R841", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "Tanaffos 2020 (PMC8008414)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "100_120", "E04": "severe_over_30",
            "E05": "severe_hypoxia_under_93",
            "S01": "present", "S04": "at_rest", "S16": "present", "S17": "present",
            "L01": "high_10000_20000", "L02": "high_over_10",
            "L14": "eosinophilia", "L16": "elevated", "L28": "elevated",
            "L35": "consolidation",
            "T01": "over_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "18_39", "R02": "male", "R03": "never", "R47": "yes"}
    },
    {
        "id": "R842", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "BMJ Case Rep 2016 (PMC5483544)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "over_120", "E05": "severe_hypoxia_under_93",
            "S01": "present", "S04": "at_rest",
            "S13": "present", "S66": "present", "S14": "present",
            "L01": "very_high_over_20000", "L14": "normal",
            "L04": "bilateral_infiltrate",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "13_17", "R02": "female", "R03": "current"}
    },
    {
        "id": "R843", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "JIMHICR 2020 (PMC7262976)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "100_120", "E05": "severe_hypoxia_under_93",
            "S01": "present", "S04": "at_rest", "S21": "present",
            "S09": "present", "S05": "mild", "S13": "present",
            "S46": "present", "S07": "severe",
            "L01": "high_10000_20000", "L14": "eosinophilia",
            "L04": "bilateral_infiltrate",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "18_39", "R02": "male", "R03": "current"}
    },
    {
        "id": "R844", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "AAIR 2010 (PMC2846739)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "over_120", "E04": "tachypnea_20_30",
            "E05": "mild_hypoxia_93_96",
            "S01": "present", "S04": "at_rest", "S06": "present",
            "L01": "high_10000_20000", "L02": "moderate_3_10",
            "L28": "normal", "L14": "normal", "L35": "GGO",
            "T01": "3d_to_1w", "T02": "acute"
        },
        "risk_factors": {"R01": "13_17", "R02": "female", "R03": "current"}
    },
    {
        "id": "R845", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "BMC Pulm Med 2023 (PMC10413584)",
        "evidence": {
            "E01": "39.0_40.0", "E02": "100_120", "E04": "tachypnea_20_30",
            "E05": "normal_over_96",
            "S01": "present", "S04": "at_rest", "S21": "present",
            "L01": "high_10000_20000", "L14": "eosinophilia",
            "L02": "moderate_3_10", "L35": "GGO",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "13_17", "R02": "female", "R03": "current"}
    },
    {
        "id": "R846", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "JCHIMP 2018 (PMC5998281)",
        "evidence": {
            "E01": "39.0_40.0", "E02": "100_120", "E04": "normal_under_20",
            "E05": "severe_hypoxia_under_93",
            "S01": "present", "S04": "at_rest",
            "L01": "normal_4000_10000", "L14": "normal",
            "L02": "high_over_10", "L03": "high_over_0.5",
            "L28": "elevated", "L35": "pleural_effusion",
            "T01": "under_3d", "T02": "acute"
        },
        "risk_factors": {"R01": "40_64", "R02": "male", "R03": "current"}
    },
    {
        "id": "R847", "expected_id": "D188", "expected_name": "好酸球性肺炎",
        "in_scope": True, "source": "J Med Case Rep 2016 (PMC4983070)",
        "evidence": {
            "E01": "38.0_39.0", "E02": "under_100", "E04": "normal_under_20",
            "E05": "mild_hypoxia_93_96",
            "S01": "present", "S04": "at_rest", "S07": "severe",
            "S16": "present", "S17": "present",
            "L01": "very_high_over_20000", "L14": "eosinophilia",
            "L93": "mild_low_10_12", "L35": "pleural_effusion",
            "T01": "over_3w", "T02": "subacute"
        },
        "risk_factors": {"R01": "40_64", "R02": "female", "R03": "never", "R47": "yes"}
    },
]

if __name__ == '__main__':
    s1 = load('step1_fever_v2.7.json')
    all_cases = D61_CASES + D179_CASES + D188_CASES

    errors = validate_cases(all_cases, s1)
    if errors:
        print(f"VALIDATION ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
    else:
        print(f"All {len(all_cases)} cases validated OK")
        suite = load('real_case_test_suite.json')
        existing_ids = {c['id'] for c in suite['cases']}
        added = 0
        for case in all_cases:
            if case['id'] not in existing_ids:
                suite['cases'].append(case)
                added += 1
        save('real_case_test_suite.json', suite)
        print(f"Added {added} cases. Total: {len(suite['cases'])}")
