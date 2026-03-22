"""D430 機能性ディスペプシア 案例追加"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('real_case_test_suite.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

next_id = max(int(c['id'][1:]) for c in cases) + 1

new_cases = [
    # Case 1: PMC11391960 - 37F, PDS type, 7ヶ月, early satiety+bloating, WBC/labs normal
    {
        "id": f"R{next_id}",
        "source": "PMC11391960 2024",
        "pmcid": "PMC11391960",
        "vignette": "37F. 7ヶ月前から心窩部灼熱感が増悪。早期満腹感(食事量減少)、腹部膨満、交代性便通。体温正常。腹部柔軟・圧痛なし。WBC 5,500(正常), Hb 14.9, Plt 255K。",
        "final_diagnosis": "機能性ディスペプシア(PDS型)+IBS混合型",
        "expected_id": "D430",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S61": "burning_gnawing",
            "S131": "present",
            "E44": "mild",
            "E09": "soft_nontender",
            "L01": "normal_4000_10000",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "18_39",
            "R02": "female"
        },
        "notes": "PDS type FD + IBS-M. 7-month history of heartburn, early satiety, bloating. Labs normal."
    },
    # Case 2: PMC8594970 - 25F, 1年, 心窩部痛+bloating+postprandial worsening
    {
        "id": f"R{next_id+1}",
        "source": "PMC8594970 Cureus 2021",
        "pmcid": "PMC8594970",
        "vignette": "25F. 1年前から腹部膨満、心窩部痛(5/10)。食後増悪、精製炭水化物・乳製品で悪化。排気あり。体温正常。心窩部圧痛あり、筋性防御・反跳痛なし。腸音やや亢進。",
        "final_diagnosis": "機能性ディスペプシア+GERD",
        "expected_id": "D430",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S64": "moderate",
            "S62": "postprandial",
            "E44": "mild",
            "E09": "localized_tenderness",
            "S13": "present",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "18_39",
            "R02": "female"
        },
        "notes": "1-year FD + GERD. Epigastric pain 5/10, postprandial worsening. Stress-related onset (graduate school)."
    },
    # Case 3: PMC7236055 - 34F, heartburn+nausea+belching, 食後増悪
    {
        "id": f"R{next_id+2}",
        "source": "PMC7236055 2020",
        "pmcid": "PMC7236055",
        "vignette": "34F. 慢性的な心窩部灼熱感、悪心、排気。食後増悪。不規則な食事時間、ストレス環境。体温正常。心窩部(CV12/CV13)に圧痛、腹直筋硬結。",
        "final_diagnosis": "機能性ディスペプシア",
        "expected_id": "D430",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S61": "burning_gnawing",
            "S62": "postprandial",
            "S13": "present",
            "S176": "postprandial",
            "E09": "localized_tenderness",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "18_39",
            "R02": "female"
        },
        "notes": "Chronic FD with heartburn, nausea, belching. Postprandial worsening. Stress-related."
    },
    # Case 5: PMC8516136 - 54F, 15年, bloating+nausea+belching, CBC/BMP normal
    {
        "id": f"R{next_id+3}",
        "source": "PMC8516136 2021",
        "pmcid": "PMC8516136",
        "vignette": "54F. 15年来の消化不良症状。排気、腹部膨満、悪心(20時間持続)。体温正常。CBC正常、BMP正常、甲状腺機能正常。腹部XR/US正常。",
        "final_diagnosis": "機能性ディスペプシア(gastrocardiac syndrome併発)",
        "expected_id": "D430",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S13": "present",
            "E44": "mild",
            "L01": "normal_4000_10000",
            "L02": "normal_under_0.3",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "female"
        },
        "notes": "15-year FD triggering recurrent PSVT. Nausea, bloating, belching. All labs normal."
    },
]

cases.extend(new_cases)

with open('real_case_test_suite.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases (R{next_id}-R{next_id+3}), total {len(cases)}")
