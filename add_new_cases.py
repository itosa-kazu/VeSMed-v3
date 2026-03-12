#!/usr/bin/env python3
"""Add 18 new real cases from literature to test suite."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, "real_case_test_suite.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

new_cases = [
    # ── Rickettsia x3 ──
    {
        "id": "R59", "source": "PMC10663404",
        "description": "21M, RMSF: fever/headache/myalgia/arthralgia/dry cough/maculopapular rash, travel to Tennessee",
        "expected_id": "D23", "in_scope": True,
        "evidence": {
            "T01": "3d_to_1w", "S01": "dry", "S05": "mild", "S06": "present",
            "S08": "present", "E01": "38.0_39.0", "E12": "maculopapular_rash",
            "L03": "mildly_elevated", "L06": "thrombocytopenia"
        },
        "risk_factors": {"R01": "yes"}
    },
    {
        "id": "R60", "source": "PMC5930880",
        "description": "74F, Japanese Spotted Fever: 4-day high fever/rash/confusion/eschar on thigh, hobby farmer",
        "expected_id": "D23", "in_scope": True,
        "evidence": {
            "T01": "3d_to_1w", "E01": "39.0_40.0", "E02": "over_120",
            "E16": "confused", "E17": "present", "E12": "maculopapular_rash",
            "L03": "mildly_elevated", "L06": "thrombocytopenia"
        },
        "risk_factors": {"R06": "yes"}
    },
    {
        "id": "R61", "source": "BMC_Infect_Dis_2022",
        "description": "36F, Mediterranean Spotted Fever: 13-day fever/chills/myalgia/arthralgia/rash/jaundice",
        "expected_id": "D23", "in_scope": True,
        "evidence": {
            "T01": "1w_to_3w", "S05": "mild", "S06": "present", "S07": "severe",
            "S08": "present", "S09": "present", "E02": "over_120",
            "E12": "maculopapular_rash", "E18": "present",
            "L03": "markedly_elevated", "L06": "thrombocytopenia"
        },
        "risk_factors": {}
    },
    # ── Dengue x1 ──
    {
        "id": "R62", "source": "PMC2974995",
        "description": "21M, Dengue: 10-day fever/arthralgia/malaise/diarrhea/rectal bleeding, returned from Indonesia",
        "expected_id": "D16", "in_scope": True,
        "evidence": {
            "T01": "1w_to_3w", "S07": "severe", "S08": "present",
            "S14": "watery", "S26": "present", "E01": "38.0_39.0",
            "L02": "moderate_3_10", "L09": "negative", "L10": "negative"
        },
        "risk_factors": {"R01": "yes"}
    },
    # ── Chikungunya x2 ──
    {
        "id": "R63", "source": "PMC6456360",
        "description": "34M, Chikungunya + rhabdomyolysis: fever/myalgia/arthralgia/diarrhea, India→Qatar",
        "expected_id": "D91", "in_scope": True,
        "evidence": {
            "T01": "under_3d", "S06": "present", "S08": "present",
            "S14": "watery", "E01": "39.0_40.0", "E03": "hypotension_under_90",
            "L06": "thrombocytopenia", "L09": "negative", "L10": "negative"
        },
        "risk_factors": {"R01": "yes"}
    },
    {
        "id": "R64", "source": "PMC5864422",
        "description": "74M, Atypical Chikungunya: arthralgia/rigors/maculopapular rash, Haiti aid worker",
        "expected_id": "D91", "in_scope": True,
        "evidence": {
            "T01": "under_3d", "S08": "present", "S09": "present",
            "E12": "maculopapular_rash", "L06": "thrombocytopenia",
            "L09": "negative", "L10": "negative"
        },
        "risk_factors": {"R01": "yes"}
    },
    # ── Typhoid x2 ──
    {
        "id": "R65", "source": "PMC10793046",
        "description": "23M, Typhoid + rhabdomyolysis: high fever/myalgia, returned from Zambia, blood culture S.typhi",
        "expected_id": "D28", "in_scope": True,
        "evidence": {
            "T01": "3d_to_1w", "T03": "continuous", "S06": "present",
            "E01": "over_40.0", "E02": "over_120",
            "L01": "normal_4000_12000", "L02": "high_over_10",
            "L03": "markedly_elevated", "L04": "normal", "L09": "gram_negative"
        },
        "risk_factors": {"R01": "yes"}
    },
    {
        "id": "R66", "source": "PMC11986221",
        "description": "31M, Typhoid + meningitis: 18-day fever/headache/vomiting/diarrhea/rash/confusion/jaundice/hepatosplenomegaly",
        "expected_id": "D28", "in_scope": True,
        "evidence": {
            "T01": "1w_to_3w", "T03": "continuous", "S05": "severe",
            "S06": "present", "S09": "present", "S13": "present", "S14": "watery",
            "E01": "37.5_38.0", "E12": "maculopapular_rash",
            "E14": "present", "E16": "confused", "E18": "present", "E34": "present",
            "L01": "normal_4000_12000", "L02": "high_over_10",
            "L03": "markedly_elevated", "L09": "gram_negative"
        },
        "risk_factors": {}
    },
    # ── FMF x1 ──
    {
        "id": "R67", "source": "PMC5177713",
        "description": "17M, FMF as FUO: recurrent periodic fever 39.3C, high CRP, elevated ESR, Korea",
        "expected_id": "D66", "in_scope": True,
        "evidence": {
            "T01": "3d_to_1w", "T03": "periodic",
            "E01": "39.0_40.0", "L02": "high_over_10", "L28": "elevated"
        },
        "risk_factors": {}
    },
    # ── Behcet x1 ──
    {
        "id": "R68", "source": "PMC9840407",
        "description": "53M, Behcet's + recurrent VTE: periodic fever/oral ulcer/scrotal ulcer/DVT/PE, CRP>200, ESR>100",
        "expected_id": "D90", "in_scope": True,
        "evidence": {
            "T01": "over_3w", "T03": "periodic", "S04": "exertional",
            "S29": "present", "S39": "present", "E01": "38.0_39.0",
            "L02": "high_over_10", "L09": "negative", "L15": "elevated",
            "L28": "very_high_over_100"
        },
        "risk_factors": {}
    },
    # ── Drug fever x2 ──
    {
        "id": "R69", "source": "PMC4912248",
        "description": "62M, Tigecycline drug fever: fever 39C/leukemoid reaction/rash, WBC 38k, ESR 58, CRP 108",
        "expected_id": "D19", "in_scope": True,
        "evidence": {
            "T01": "under_3d", "E01": "39.0_40.0",
            "E12": "maculopapular_rash", "L01": "leukocytosis_over_12000",
            "L02": "high_over_10", "L09": "negative", "L28": "elevated"
        },
        "risk_factors": {"R04": "yes", "R08": "yes"}
    },
    {
        "id": "R70", "source": "PMC8502992",
        "description": "34M, Dexmedetomidine drug fever: 41.1C in ICU, all cultures negative, resolved on drug discontinuation",
        "expected_id": "D19", "in_scope": True,
        "evidence": {
            "T01": "under_3d", "E01": "over_40.0", "L09": "negative"
        },
        "risk_factors": {"R04": "yes", "R08": "yes"}
    },
    # ── DVT/PE x2 ──
    {
        "id": "R71", "source": "PMC10473233",
        "description": "86F, PE/DVT with normal CRP: intermittent fever 39.3C, normal WBC/CRP, CT angio showed PE+bilateral DVT",
        "expected_id": "D77", "in_scope": True,
        "evidence": {
            "T01": "1w_to_3w", "T03": "intermittent",
            "E01": "39.0_40.0", "L01": "normal_4000_12000",
            "L02": "normal_under_0.3", "L09": "negative", "L20": "elevated"
        },
        "risk_factors": {}
    },
    {
        "id": "R72", "source": "PMC5851743",
        "description": "40sF, Saddle PE: nausea/vomiting/diarrhea/abdominal pain, high fever, tachypnea, SpO2 88%, hypotension",
        "expected_id": "D77", "in_scope": True,
        "evidence": {
            "T01": "3d_to_1w", "S13": "present", "S14": "watery",
            "S12": "diffuse", "E01": "39.0_40.0", "E03": "hypotension_under_90",
            "E05": "severe_hypoxia_under_93", "L09": "negative"
        },
        "risk_factors": {}
    },
    # ── Meningitis x1 ──
    {
        "id": "R73", "source": "PMC11315615",
        "description": "50M, Meningococcal B meningitis: fever/loss of consciousness, diabetic, Japan, CSF PCR positive",
        "expected_id": "D13", "in_scope": True,
        "evidence": {
            "T01": "under_3d", "E01": "38.0_39.0", "E16": "comatose",
            "E06": "present", "L09": "negative"
        },
        "risk_factors": {}
    },
    # ── Osteomyelitis x1 ──
    {
        "id": "R74", "source": "PMC5174821",
        "description": "Adult, Vertebral osteomyelitis (S.aureus): back pain/sepsis/epidural abscess, blood culture MRSA",
        "expected_id": "D31", "in_scope": True,
        "evidence": {
            "S22": "present", "E01": "38.0_39.0", "E02": "over_120",
            "E03": "hypotension_under_90", "E05": "mild_hypoxia_93_96",
            "L09": "gram_positive", "L02": "high_over_10"
        },
        "risk_factors": {}
    },
    # ── Septic arthritis x1 ──
    {
        "id": "R75", "source": "PMC6814035",
        "description": "22F, Septic arthritis (knee, Streptococcus): fever/knee pain/discharge, post-arthroscopy, ESR 55, CRP 40",
        "expected_id": "D32", "in_scope": True,
        "evidence": {
            "S08": "present", "S23": "present",
            "E01": "38.0_39.0", "L02": "high_over_10",
            "L28": "elevated"
        },
        "risk_factors": {"R04": "yes"}
    },
    # ── Liver abscess x1 ──
    {
        "id": "R76", "source": "PMC3882570",
        "description": "Diabetic patient, Pyogenic liver abscess as FUO: fever, hepatomegaly on imaging",
        "expected_id": "D29", "in_scope": True,
        "evidence": {
            "T01": "1w_to_3w", "E01": "38.0_39.0",
            "E34": "present", "S12": "RUQ",
            "L01": "leukocytosis_over_12000", "L02": "high_over_10"
        },
        "risk_factors": {}
    },
]

data["cases"].extend(new_cases)
data["results_summary"]["total_cases"] = len(data["cases"])
data["results_summary"]["total_in_scope"] = sum(1 for c in data["cases"] if c["in_scope"])
data["results_summary"]["total_oos"] = sum(1 for c in data["cases"] if not c["in_scope"] or c["expected_id"] == "OOS")

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases. Total: {len(data['cases'])}")
