"""D431 食道カンジダ症 案例追加"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('real_case_test_suite.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

next_id = max(int(c['id'][1:]) for c in cases) + 1

new_cases = [
    # Case 1: PMC9122014 - 74M, DM+吸入ステロイド+PPI 25年, 嚥下障害3日, WBC/CRP正常
    {
        "id": f"R{next_id}",
        "source": "PMC9122014 2022",
        "pmcid": "PMC9122014",
        "vignette": "74M. 2型DM(コントロール良), COPD(吸入ステロイド), PPI 25年使用。3日前から嚥下障害(固形+液体)。嚥下痛・悪心・嘔吐・体重減少・発熱なし。口腔内異常なし。CBC, CRP, ESR正常。HIV陰性。",
        "final_diagnosis": "食道カンジダ症",
        "expected_id": "D431",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S25": "present",
            "S101": "solids_and_liquids",
            "E87": "absent",
            "L01": "normal_4000_10000",
            "L02": "normal_under_0.3",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "65_plus",
            "R02": "male"
        },
        "notes": "Non-HIV, DM + inhaled steroid + long-term PPI. Dysphagia only 3 days. No oral thrush."
    },
    # Case 3: PMC3609197 - 44F, 免疫正常, 1週間嚥下障害+嚥下痛+発熱, WBC正常, ESR 94
    {
        "id": f"R{next_id+1}",
        "source": "PMC3609197 2012",
        "pmcid": "PMC3609197",
        "vignette": "44F. 既往歴なし。1週間前から進行性嚥下障害、嚥下痛、発熱。口腔内異常なし。WBC 6,800(正常), Hb 11.7, Plt 404K。ESR 94(高値)。HIV陰性。",
        "final_diagnosis": "食道カンジダ症+ヘルペス食道炎",
        "expected_id": "D431",
        "in_scope": True,
        "evidence": {
            "E01": "37.5_38.0",
            "S25": "present",
            "S78": "present",
            "E87": "absent",
            "L01": "normal_4000_10000",
            "L28": "very_high_over_100",
            "T01": "3d_to_1w",
            "T02": "subacute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "female",
            "R05": "no"
        },
        "notes": "Immunocompetent 44F. Progressive dysphagia + odynophagia + fever for 1 week. Combined herpetic+candidal. ESR 94."
    },
    # Case 4: PMC3819696 - 13F, 吸入ブデソニド, 1ヶ月悪心+嚥下障害, WBC/CRP正常
    {
        "id": f"R{next_id+2}",
        "source": "PMC3819696 2013",
        "pmcid": "PMC3819696",
        "vignette": "13F. 喘息で吸入ブデソニド頻用。1ヶ月前から悪心(2週間前に増悪)、嚥下障害、心窩部痛(間欠性、食後増悪)、食欲低下。発熱なし。心窩部圧痛あり。WBC 4,600, CRP陰性。HIV陰性。",
        "final_diagnosis": "食道カンジダ症",
        "expected_id": "D431",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S25": "present",
            "S13": "present",
            "S12": "present",
            "S89": "epigastric",
            "S46": "present",
            "E09": "localized_tenderness",
            "L01": "normal_4000_10000",
            "L02": "normal_under_0.3",
            "T01": "over_3w",
            "T02": "subacute"
        },
        "risk_factors": {
            "R01": "13_17",
            "R02": "female",
            "R05": "no"
        },
        "notes": "13F with frequent inhaled budesonide. 1-month nausea + dysphagia + epigastric pain. No fever. Normal labs."
    },
    # Case 5: PMC9794232 - 74M, GERD, 12ヶ月嚥下障害+体重減少9kg
    {
        "id": f"R{next_id+3}",
        "source": "PMC9794232 2023",
        "pmcid": "PMC9794232",
        "vignette": "74M. GERD既往。12ヶ月前から進行性嚥下障害(固形物)、体重減少9kg。嚥下痛・胸痛・悪心・発熱なし。HIV陰性。",
        "final_diagnosis": "食道カンジダ症(偽腫瘤型)",
        "expected_id": "D431",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S25": "present",
            "S101": "solids_only",
            "S17": "present",
            "S183": "gradual_months",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "65_plus",
            "R02": "male",
            "R05": "no"
        },
        "notes": "Chronic 12-month dysphagia + 9kg weight loss. Pseudotumor presentation. GERD/PPI background."
    },
    # Case 8: PMC6700596 - 29F, 腎移植後免疫抑制, 嚥下障害+嚥下痛+発熱+口腔カンジダ
    {
        "id": f"R{next_id+4}",
        "source": "PMC6700596 2019",
        "pmcid": "PMC6700596",
        "vignette": "29F. 腎移植後(免疫抑制剤+prednisone 5mg)。咽頭痛、嚥下障害、嚥下痛、発熱。口腔カンジダ(口蓋・舌・扁桃に白苔)。白血球増多。",
        "final_diagnosis": "食道カンジダ症+HSV-2食道炎",
        "expected_id": "D431",
        "in_scope": True,
        "evidence": {
            "E01": "38.0_39.0",
            "S25": "present",
            "S78": "present",
            "S02": "present",
            "E87": "present",
            "E08": "exudate_or_white_patch",
            "L01": "high_10000_20000",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "18_39",
            "R02": "female",
            "R05": "yes",
            "R29": "yes"
        },
        "notes": "Renal transplant on immunosuppression. Oral thrush + dysphagia + odynophagia + fever. Leukocytosis. Combined Candida + HSV-2."
    },
]

cases.extend(new_cases)

with open('real_case_test_suite.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases (R{next_id}-R{next_id+4}), total {len(cases)}")
