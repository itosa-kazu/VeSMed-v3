#!/usr/bin/env python3
"""Add more PMC cases for split diseases (batch 2).

R747-R761: 15 cases total
- D353 UC: R747-R749 (3 more → total 5)
- D354 HL: R750-R751 (2 more → total 4)
- D355 DVT: R752 (1 more → total 2)
- D351 Salmonella: R753-R755 (3 new)
- D352 Shigella: R756-R758 (3 new)
- D125 AF: R759-R760 (2 new)
- D358 FB: R761 (1 new)
"""

import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    data = load_json('real_case_test_suite.json')

    new_cases = [
        # ============ UC (D353) — 3 more ============
        {
            "id": "R747",
            "source": "Case Rep Med 2015 (PMC4649069)",
            "pmcid": "PMC4649069",
            "vignette": "76F, ESRD on dialysis. Persistent fever 37-38°C progressing to 39.1°C over 2 months. Then bloody diarrhea developed. HR 72, BP 134/66, RR 12. WBC 4810, Hb 85 g/L, albumin 21 g/L, CRP elevated. X-ray: loss of haustra. CT: extensive wall thickening ascending colon to rectum. Colonoscopy: ulceration, loss of vascular pattern, spontaneous bleeding. Biopsy: chronic active inflammation with crypt damage, goblet cell depletion. Dx: UC pancolitis.",
            "final_diagnosis": "潰瘍性大腸炎(UC)全大腸型",
            "expected_id": "D353",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "S14": "present",
                "S26": "present",
                "L22": "present",
                "T01": "over_3w",
                "S07": "severe",
                "S17": "present",
                "L02": "moderate_3_10"
            },
            "risk_factors": {
                "R01": "65_plus",
                "R02": "female",
                "R35": "no"
            }
        },
        {
            "id": "R748",
            "source": "Int J Surg Case Rep 2019 (PMC6698301)",
            "pmcid": "PMC6698301",
            "vignette": "80F. 3-month diarrhea, anorexia, fatigue, weakness. Then high-grade fever 39°C for 3 days. Abdominal pain. BP 80/50 (shock), HR 120. WBC 11000 (neutrophils 80%). Severe dehydration. Abdominal distention, generalized tenderness with involuntary guarding. Colonoscopy: continuous circumferential erythematous friable mucosa, multiple shallow ulcers. Dx: acute severe UC with sepsis-like presentation.",
            "final_diagnosis": "潰瘍性大腸炎(UC)急性重症(敗血症様)",
            "expected_id": "D353",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "E02": "100_120",
                "E03": "hypotension_under_90",
                "S14": "present",
                "S12": "present",
                "S46": "present",
                "S07": "severe",
                "L01": "high_10000_20000",
                "T01": "over_3w",
                "T02": "subacute"
            },
            "risk_factors": {
                "R01": "65_plus",
                "R02": "female"
            }
        },
        {
            "id": "R749",
            "source": "Medicine 2023 (PMC10194520)",
            "pmcid": "PMC10194520",
            "vignette": "30F. Diarrhea 3-4x/day progressing to 5-6x/day, watery mixed with blood. Nausea, vomiting. Fever max 38.9°C. No abdominal pain. WBC 19070, Hb 79 g/L→64 g/L (severe anemia), platelets 584k (reactive thrombocytosis), CRP 166. CT: ileocecal/colorectal wall thickening. Colonoscopy: hyperemia, shallow ulceration, crypt abscess. Dx: severe UC with thrombocytosis.",
            "final_diagnosis": "潰瘍性大腸炎(UC)重症(反応性血小板増多)",
            "expected_id": "D353",
            "in_scope": True,
            "evidence": {
                "E01": "38.0_39.0",
                "S14": "present",
                "S26": "present",
                "S13": "present",
                "L01": "high_10000_20000",
                "L02": "high_over_10",
                "L22": "present",
                "T01": "3d_to_1w",
                "S86": "bloody"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "female"
            }
        },

        # ============ HL (D354) — 2 more ============
        {
            "id": "R750",
            "source": "Cureus 2024 (PMC11682868)",
            "pmcid": "PMC11682868",
            "vignette": "24F. Fever, drenching night sweats, ~20 kg weight loss over 3 months. Dry cough 3 months. Anorexia, fatigue, pleuritic chest pain. Right supraclavicular, bilateral cervical, right inguinal lymphadenopathy. Hb 9.2 g/dL (microcytic), WBC 14k, ANC 11k, platelets 501k, CRP 25.15 mg/dL, ESR 120 mm/hr. CXR: mediastinal widening. CT: anterior mediastinal mass 8×3.5cm, splenomegaly 13.7cm. Biopsy: Reed-Sternberg cells. Dx: nodular sclerosis HL Stage IVB.",
            "final_diagnosis": "ホジキンリンパ腫(結節硬化型, Stage IVB)",
            "expected_id": "D354",
            "in_scope": True,
            "evidence": {
                "E01": "38.0_39.0",
                "S16": "present",
                "S17": "present",
                "S01": "present",
                "S46": "present",
                "S07": "severe",
                "E13": "present",
                "E14": "present",
                "L22": "present",
                "L28": "very_high_over_100",
                "L04": "bilateral_infiltrate",
                "T01": "over_3w",
                "E46": "cervical"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "female"
            }
        },
        {
            "id": "R751",
            "source": "Case Rep Hematol 2018 (PMC5968292)",
            "pmcid": "PMC5968292",
            "vignette": "45M. Persistent fever 39.4°C with 4 weeks weakness, fatigue, weight loss. Abdominal pain, nausea, vomiting. BP 111/60, HR 140, RR 22. Pancytopenia: WBC 2.8k, Hb 7.1 g/dL, platelets 33k. Ferritin 6149 ng/mL. Total bilirubin 3.1→12.6, albumin 2.3, Na 124, INR 1.73. CT: hepatosplenomegaly, retroperitoneal lymphadenopathy. Bone marrow: lymphocyte-rich classical HL. Dx: HL with HLH.",
            "final_diagnosis": "ホジキンリンパ腫(リンパ球豊富型)+HLH",
            "expected_id": "D354",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "E02": "over_120",
                "E03": "normal_over_90",
                "S17": "present",
                "S07": "severe",
                "S12": "present",
                "S13": "present",
                "L01": "low_under_4000",
                "L22": "present",
                "L15": "very_high_over_1000",
                "E34": "present",
                "E14": "present",
                "T01": "over_3w",
                "L44": "hyponatremia"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "male"
            }
        },

        # ============ DVT (D355) — 1 more ============
        {
            "id": "R752",
            "source": "Cureus 2020 (PMC7273555)",
            "pmcid": "PMC7273555",
            "vignette": "57F. Left leg swelling, pain, warmth, redness. Mild dry cough 3 days. Fever 38.0°C, SpO2 90%. WBC 2300 (leukopenia, neutrophils 65.7%, lymphocytes 23%), platelets 138k, CRP 47 mg/L, LDH 655, D-dimer 1.3 µg/mL. Doppler: thrombosis in external iliac, left iliac, superficial/small saphenous veins. CTA: NO pulmonary embolism. Dx: extensive DVT (no PE).",
            "final_diagnosis": "深部静脈血栓症(DVT, 左下肢広範, PE陰性)",
            "expected_id": "D355",
            "in_scope": True,
            "evidence": {
                "E01": "37.5_38.0",
                "S39": "present",
                "E05": "severe_hypoxia_under_93",
                "L01": "low_under_4000",
                "L20": "mildly_elevated",
                "L02": "moderate_3_10",
                "T01": "under_3d",
                "T02": "subacute",
                "S01": "present"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "female"
            }
        },

        # ============ Salmonella (D351) — 3 new ============
        {
            "id": "R753",
            "source": "Intern Med 2024 (PMC10733605)",
            "pmcid": "PMC10733605",
            "vignette": "87F. Fever 37.8°C→39.1°C, body discomfort, large-volume watery diarrhea. HR 96, BP 136/80, RR 22, SpO2 96%. WBC 8200 (neutrophils 90.5%), CRP 7.21 mg/dL, Hb 11.0, platelets 158k. Abdomen soft, no tenderness. Blood/urine/stool all positive for non-typhoidal Salmonella. Dx: NTS bacteremia with enteritis.",
            "final_diagnosis": "サルモネラ腸炎(NTS菌血症)",
            "expected_id": "D351",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "S14": "present",
                "L01": "normal_4000_10000",
                "L02": "moderate_3_10",
                "L34": "pathogen_detected",
                "T01": "under_3d",
                "S86": "watery"
            },
            "risk_factors": {
                "R01": "65_plus",
                "R02": "female"
            }
        },
        {
            "id": "R754",
            "source": "IDCases 2020 (PMC7460271)",
            "pmcid": "PMC7460271",
            "vignette": "30M, previously healthy. Abdominal pain, vomiting, diarrhea hours after kebab meal (goat meat). Fever up to 41°C. Alert, dehydrated. WBC 5270 (PMN 56%), CRP 5.67 mg/dL, Hb 16.1, platelets 226k. Abdominal US: hepatic steatosis. Stool Film Array positive for Salmonella. Blood culture: S. Hessarek. Dx: Salmonella Hessarek gastroenteritis with bacteremia.",
            "final_diagnosis": "サルモネラ腸炎(S. Hessarek, 食品由来菌血症)",
            "expected_id": "D351",
            "in_scope": True,
            "evidence": {
                "E01": "over_40.0",
                "S14": "present",
                "S12": "present",
                "S13": "present",
                "L01": "normal_4000_10000",
                "L02": "moderate_3_10",
                "L34": "pathogen_detected",
                "T01": "under_3d",
                "T02": "acute",
                "S89": "diffuse"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "male"
            }
        },
        {
            "id": "R755",
            "source": "IDCases 2019 (PMC6753814)",
            "pmcid": "PMC6753814",
            "vignette": "45F, ER nurse. Lower abdominal pain (colicky), 3 episodes nonbloody diarrhea, 1-day fever 38.7°C. HR 110, BP 155/79, SpO2 100%. WBC 3000 (leukopenia), CRP 124 mg/dL, ESR 14. CT: colitis involving cecum/ascending colon with inflammatory stranding. Stool: Salmonella + C. difficile PCR positive. Blood cultures sterile. Dx: NTS + CDI co-infection.",
            "final_diagnosis": "サルモネラ腸炎(+C. difficile重複感染)",
            "expected_id": "D351",
            "in_scope": True,
            "evidence": {
                "E01": "38.0_39.0",
                "E02": "100_120",
                "S14": "present",
                "S12": "present",
                "L01": "low_under_4000",
                "L02": "high_over_10",
                "L34": "pathogen_detected",
                "T01": "under_3d",
                "T02": "acute",
                "S89": "RLQ"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "female"
            }
        },

        # ============ Shigella (D352) — 3 new ============
        {
            "id": "R756",
            "source": "IDCases 2024 (PMC12071271-C1)",
            "pmcid": "PMC12071271",
            "vignette": "52M. High-grade fever 39.1-40.1°C, multiple episodes foul-smelling watery yellowish diarrhea, loss of appetite. WBC 19000 (leukocytosis, mainly neutrophils), CRP 325.3 mg/L, creatinine 127 µmol/L. CT: rectal submucosal edema. Stool culture: Shigella flexneri. Dx: S. flexneri dysentery.",
            "final_diagnosis": "細菌性赤痢(S. flexneri)",
            "expected_id": "D352",
            "in_scope": True,
            "evidence": {
                "E01": "over_40.0",
                "S14": "present",
                "S46": "present",
                "L01": "high_10000_20000",
                "L02": "high_over_10",
                "L34": "pathogen_detected",
                "T01": "under_3d",
                "T02": "acute",
                "S86": "watery"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "male"
            }
        },
        {
            "id": "R757",
            "source": "IDCases 2018 (PMC5775773)",
            "pmcid": "PMC5775773",
            "vignette": "45M, MSM. Altered mental status, 1-day history of diarrhea and fever 39.5°C. Confusion, lethargy. HR 104, BP 100/50. WBC 2400 (leukopenia), CRP 210 mg/L, creatinine 136 µmol/L, Na 130. CSF: mild pleocytosis. Stool culture: S. flexneri (ciprofloxacin-resistant). Dx: Shigella-associated encephalopathy.",
            "final_diagnosis": "細菌性赤痢(S. flexneri, 脳症合併)",
            "expected_id": "D352",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "E02": "100_120",
                "E03": "normal_over_90",
                "E16": "confused",
                "S14": "present",
                "L01": "low_under_4000",
                "L02": "high_over_10",
                "L34": "pathogen_detected",
                "T01": "under_3d",
                "T02": "acute",
                "L44": "hyponatremia"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "male"
            }
        },
        {
            "id": "R758",
            "source": "IDCases 2021 (PMC8155794)",
            "pmcid": "PMC8155794",
            "vignette": "39M, Mexican origin. Confusion, watery non-bloody diarrhea (10 episodes in 2 days), vomiting x4, abdominal pain, dizziness, fever 39.5°C, chills, myalgias, headache, neck stiffness. HR 132, BP 106/71, RR 18, SpO2 98%. WBC 13100. CT abdomen: diffuse colonic wall thickening (pancolitis). Stool: S. flexneri. Dx: Shigella infectious colitis with meningism.",
            "final_diagnosis": "細菌性赤痢(S. flexneri, 髄膜刺激症状合併)",
            "expected_id": "D352",
            "in_scope": True,
            "evidence": {
                "E01": "39.0_40.0",
                "E02": "over_120",
                "S14": "present",
                "S13": "present",
                "S12": "present",
                "S09": "present",
                "S06": "present",
                "S05": "severe",
                "L01": "high_10000_20000",
                "L34": "pathogen_detected",
                "T01": "under_3d",
                "T02": "acute",
                "S86": "watery",
                "S89": "diffuse"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "male"
            }
        },

        # ============ AF (D125) — 2 new ============
        {
            "id": "R759",
            "source": "Heart Rhythm Case Rep 2018 (PMC5965180)",
            "pmcid": "PMC5965180",
            "vignette": "37M, no significant PMH. Palpitations. HR 129 (irregular), hemodynamically stable. CBC/CMP unremarkable, troponin negative. ECG: atrial fibrillation with rapid ventricular response 129 bpm. Echo: normal. IV diltiazem, oral diltiazem. Spontaneously converted to sinus rhythm next morning. Dx: new-onset paroxysmal AF (lone AF).",
            "final_diagnosis": "急性心房細動(AF, 孤立性, 新規発症)",
            "expected_id": "D125",
            "in_scope": True,
            "evidence": {
                "S35": "present",
                "E02": "over_120",
                "E01": "under_37.5",
                "E40": "AF",
                "L01": "normal_4000_10000",
                "L02": "normal_under_0.3",
                "T01": "under_3d",
                "T02": "sudden"
            },
            "risk_factors": {
                "R01": "18_39",
                "R02": "male"
            }
        },
        {
            "id": "R760",
            "source": "Cureus 2020 (PMC7290110-C1)",
            "pmcid": "PMC7290110",
            "vignette": "53M, BMI 30.7, no significant PMH. Sudden onset palpitations at 2 AM, dyspnea on exertion, fatigue. HR 136 (irregular), BP 134/90, RR 16, SpO2 96%, temp 37.3°C. NT-proBNP 1834, D-dimer 0.57. ECG: AF with rate 134, abnormal R wave progression. CTA: no PE. Echo: moderate LVH, LVEF 60%. IV diltiazem ×2. Dx: new-onset AF (COVID-19 detected during admission).",
            "final_diagnosis": "急性心房細動(AF, 新規発症)",
            "expected_id": "D125",
            "in_scope": True,
            "evidence": {
                "S35": "present",
                "S04": "on_exertion",
                "S07": "mild",
                "E02": "over_120",
                "E01": "under_37.5",
                "E40": "AF",
                "L51": "very_high",
                "T01": "under_3d",
                "T02": "sudden"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "male"
            }
        },

        # ============ Airway FB (D358) — 1 new ============
        {
            "id": "R761",
            "source": "Cureus 2023 (PMC10478783)",
            "pmcid": "PMC10478783",
            "vignette": "45M. Worsening respiratory distress after using salbutamol inhaler. Foreign body sensation below larynx, coughing up bloody sputum. Acute onset, 1 hour before presentation. BP 131/67, RR 22, HR 103, SpO2 92%. CXR: emphysema signs, no visible FB. Emergency bronchoscopy: plastic cable clip occluding terminal right main bronchus. Dx: foreign body aspiration (inhaler cap).",
            "final_diagnosis": "気道異物(吸入器キャップ)",
            "expected_id": "D358",
            "in_scope": True,
            "evidence": {
                "S04": "at_rest",
                "E02": "100_120",
                "E05": "mild_hypoxia_93_96",
                "E01": "under_37.5",
                "T01": "under_3d",
                "T02": "sudden",
                "E04": "tachypnea_20_30"
            },
            "risk_factors": {
                "R01": "40_64",
                "R02": "male"
            }
        },
    ]

    data['cases'].extend(new_cases)

    print(f"Added {len(new_cases)} new cases (R747-R761)")
    for c in new_cases:
        print(f"  {c['id']}: {c['expected_id']} — {c['final_diagnosis'][:40]}")

    save_json('real_case_test_suite.json', data)

if __name__ == '__main__':
    main()
