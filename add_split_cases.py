#!/usr/bin/env python3
"""Add PMC cases for the new split diseases.

Cases added:
- D353 (UC): R740, R741 (29F acute severe UC, 80F UC as FUO)
- D354 (HL): R742, R743 (44M Pel-Ebstein, 53F bone marrow HL)
- D355 (DVT): R744 (35M post-COVID DVT)
- D128 (epiglottitis): R745, R746 (44M diabetic, 20M young)
"""

import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {path}")

def main():
    data = load_json('real_case_test_suite.json')

    new_cases = [
        # ============ UC (D353) ============
        {
            "id": "R740",
            "source": "Case Rep Gastroenterol 2024 (PMC10882854)",
            "pmcid": "PMC10882854",
            "vignette": "29F, 2-year remission UC. Presented with 20 bloody bowel movements/day, fecal urgency, crampy abdominal pain, mild LLQ tenderness. Temp 38.3°C, HR 120. CRP 104 mg/L, WBC 14000, Hb 90 g/L, albumin 28 g/L. Colonoscopy: diffuse ulcers throughout colon. Dx: acute severe ulcerative colitis flare (Truelove-Witts criteria met).",
            "final_diagnosis": "潰瘍性大腸炎(UC)急性重症フレア",
            "expected_id": "D353",
            "in_scope": True,
            "evidence": {
                "E01": "38.0_39.0",
                "E02": "100_120",
                "S14": "present",
                "S26": "present",
                "S12": "present",
                "S46": "present",
                "L01": "high_10000_20000",
                "L02": "high_over_10",
                "L22": "present",
                "T01": "under_3d",
                "T02": "acute",
                "S86": "bloody",
                "S89": "LLQ"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "female",
                "R35": "yes"
            }
        },
        {
            "id": "R741",
            "source": "Case Rep Gastroenterol 2016 (PMC4967693)",
            "pmcid": "PMC4967693",
            "vignette": "80F, UC diagnosed 7 years prior on mesalazine. Presented with 12-day fever (38.5°C) without bowel symptoms (no diarrhea, no abdominal pain). ESR >100, CRP 71.4 mg/L, Hb 7.2 g/dL. Gallium-67 scintigraphy showed diffuse ascending colon uptake. Dx: UC activity presenting as FUO.",
            "final_diagnosis": "潰瘍性大腸炎(UC)活動性（FUOとして発症）",
            "expected_id": "D353",
            "in_scope": True,
            "evidence": {
                "E01": "38.0_39.0",
                "T01": "3d_to_1w",
                "L02": "high_over_10",
                "L28": "very_high_over_100",
                "L22": "present",
                "S07": "severe"
            },
            "risk_factors": {
                "R01": "65_plus",
                "R02": "female",
                "R35": "yes"
            }
        },

        # ============ HL (D354) ============
        {
            "id": "R742",
            "source": "Cancer Reports 2024 (PMC11578651)",
            "pmcid": "PMC11578651",
            "vignette": "44M from rural India. >1 year of cyclic fever (5-7 days high fever followed by 5-7 days afebrile = Pel-Ebstein pattern). 15 kg weight loss over 6 months. Multiple bilateral cervical and supraclavicular lymph node swellings (6 months). Moderate splenomegaly. Hb 9.0 g/dL, platelets 120k, albumin 3.0 g/dL, ALP 910.7, LDH 907.7 U/L. PET-CT: metabolically active bilateral lymph nodes, splenic/marrow involvement. Biopsy: Reed-Sternberg cells, CD15+/CD30+/EBV-LMP1+. Dx: Hodgkin lymphoma mixed cellularity Stage IV, IPS 4.",
            "final_diagnosis": "ホジキンリンパ腫(混合細胞型, Stage IV)",
            "expected_id": "D354",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "T03": "periodic",
                "T01": "over_3w",
                "S17": "present",
                "E13": "present",
                "E14": "present",
                "L16": "elevated",
                "L22": "present",
                "S07": "severe",
                "S46": "present",
                "E46": "cervical"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "male"
            }
        },
        {
            "id": "R743",
            "source": "Cureus 2022 (PMC8903813)",
            "pmcid": "PMC8903813",
            "vignette": "53F with intermittent fever up to 104°F (40°C) for 2.5 weeks, dry cough. Initially diagnosed as pneumonia. WBC 2.2k (leucopenia), Hb 8.6 g/dL, lymphocytes 6%, sodium 127 (SIADH). CXR normal. Fever peaked at 104°F with hypotension (SBP 90s). Bone marrow biopsy: Hodgkin's lymphoma. Cyclic fever pattern (every 2-3 days) consistent with Pel-Ebstein fever. Dx: Hodgkin lymphoma with Pel-Ebstein fever.",
            "final_diagnosis": "ホジキンリンパ腫(Pel-Ebstein熱)",
            "expected_id": "D354",
            "in_scope": True,
            "evidence": {
                "E01": "over_40.0",
                "T03": "periodic",
                "T01": "1w_to_3w",
                "S01": "present",
                "L01": "low_under_4000",
                "L22": "present",
                "E03": "hypotension_under_90",
                "S07": "severe",
                "L44": "hyponatremia"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "female"
            }
        },

        # ============ DVT (D355) ============
        {
            "id": "R744",
            "source": "Vasc Health Risk Manag 2021 (PMC8354738)",
            "pmcid": "PMC8354738",
            "vignette": "35M, discharged 4 days ago after severe COVID-19. Presented with left lower leg pain and swelling, difficulty moving limb, headache, low-grade fever for 2 days. HR 80, RR 22, temp 36.9°C, SpO2 93-96%. WBC 17500, platelets 241k. Doppler: thrombus in distal popliteal, anterior/posterior tibial veins and perforators. CXR normal. Dx: distal deep vein thrombosis left leg, post-COVID.",
            "final_diagnosis": "深部静脈血栓症(DVT, 左下肢, COVID後)",
            "expected_id": "D355",
            "in_scope": True,
            "evidence": {
                "E01": "under_37.5",
                "S39": "present",
                "E05": "mild_hypoxia_93_96",
                "L01": "high_10000_20000",
                "T01": "under_3d",
                "T02": "subacute"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "male"
            }
        },

        # ============ Epiglottitis (D128) ============
        {
            "id": "R745",
            "source": "Anesth Essays Res 2024 (PMC11408896)",
            "pmcid": "PMC11408896",
            "vignette": "44M, diabetic (non-compliant), smoker, unvaccinated against Hib. Several days of throat soreness, then acute shortness of breath and stridor. Self-measured fever 39.4°C the night before. Drooling, forward-leaning posture. BP 121/68, HR 121, RR 32, SpO2 95%. WBC 21×10³/L (83% neutrophils). Lateral neck X-ray: 'thumb sign' and 'vallecula sign'. Nasopharyngoscopy: enlarged epiglottis, edematous arytenoids/supraglottic space. Dx: acute epiglottitis.",
            "final_diagnosis": "急性喉頭蓋炎",
            "expected_id": "D128",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "S04": "at_rest",
                "S02": "present",
                "E02": "100_120",
                "E04": "severe_over_30",
                "E05": "mild_hypoxia_93_96",
                "L01": "very_high_over_20000",
                "E07": "wheezes",
                "T01": "under_3d",
                "T02": "acute",
                "E31": "present",
                "S25": "present"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "male",
                "R04": "yes"
            }
        },
        {
            "id": "R746",
            "source": "Cureus 2023 (PMC10766345)",
            "pmcid": "PMC10766345",
            "vignette": "20M, previously healthy. 2-day sore throat, difficulty swallowing, fever, body aches, hoarse voice. HR 118, BP 152/92, temp 39.1°C, RR 18, SpO2 97%. CRP 185 mg/L, WBC 29.7×10⁹/L (neutrophils 27.1). Lateral neck X-ray: swollen epiglottis, narrowing of supraglottic airway. Nasopharyngoscopy: edematous uvula, bilateral edematous aryepiglottic folds. Dx: acute epiglottitis.",
            "final_diagnosis": "急性喉頭蓋炎",
            "expected_id": "D128",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "S02": "present",
                "S25": "present",
                "S55": "present",
                "E02": "100_120",
                "L02": "high_over_10",
                "L01": "very_high_over_20000",
                "T01": "under_3d",
                "T02": "acute",
                "S07": "mild"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "male"
            }
        },
    ]

    data['cases'].extend(new_cases)

    print(f"Added {len(new_cases)} new cases (R740-R746)")
    for c in new_cases:
        print(f"  {c['id']}: {c['expected_id']} — {c['final_diagnosis'][:40]}")

    save_json('real_case_test_suite.json', data)

if __name__ == '__main__':
    main()
