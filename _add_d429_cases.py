"""D429 アニサキス症 案例追加"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('real_case_test_suite.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

next_id = max(int(c['id'][1:]) for c in cases) + 1

new_cases = [
    # Case 1: PMC6137290 - 50M, 生サバ3h前, 心窩部痛+悪心+嘔吐, WBC 15300, CRP 12.29mg/L
    {
        "id": f"R{next_id}",
        "source": "Kakizaki 2018",
        "pmcid": "PMC6137290",
        "vignette": "50M. 生サバ摂取3時間後に急性心窩部痛発症。悪心・嘔吐あり。発熱なし。心窩部に軽度圧痛、反跳痛なし。WBC 15,300, 好酸球2%, CRP 12.29 mg/L。",
        "final_diagnosis": "胃アニサキス症",
        "expected_id": "D429",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S13": "present",
            "S66": "present",
            "S64": "severe",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "L02": "moderate_3_10",
            "T01": "under_3d",
            "T02": "sudden"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male",
            "R67": "yes"
        },
        "notes": "Gastric anisakiasis after raw mackerel. Second attack (prior gastric episode). CT showed gastric antral submucosal edema."
    },
    # Case 2: PMC3678070 - 47M, 生イワシ4日前, 心窩部痛3日, WBC 10350, CRP 0.34
    {
        "id": f"R{next_id+1}",
        "source": "Choi 2013",
        "pmcid": "PMC3678070",
        "vignette": "47M. 生カタクチイワシ摂取翌日から心窩部痛(3日間持続)。悪心あり、嘔吐・発熱なし。心窩部・臍周囲圧痛、反跳痛なし。BP 120/70, HR 68, BT 37.0℃。WBC 10,350, 好酸球1.6%, CRP 0.34 mg/dL。",
        "final_diagnosis": "胃アニサキス症",
        "expected_id": "D429",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S13": "present",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "L02": "mild_0.3_3",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male",
            "R67": "yes"
        },
        "notes": "Gastric anisakiasis after raw anchovies. 3-day history of epigastric pain."
    },
    # Case 3: PMC3341444 - 47M, 生ヒラメ, 心窩部痛2日+悪心嘔吐, WBC 15500, CRP 3.63
    {
        "id": f"R{next_id+2}",
        "source": "Kim 2012",
        "pmcid": "PMC3341444",
        "vignette": "47M. 生ヒラメ摂取後に鋭い心窩部痛(2日間)。悪心・嘔吐あり、下痢・発熱なし。心窩部圧痛、腸音亢進。WBC 15,500(好酸球正常), CRP 3.63 mg/dL。",
        "final_diagnosis": "胃アニサキス症",
        "expected_id": "D429",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S61": "sharp_stabbing",
            "S13": "present",
            "S66": "present",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "L02": "mild_0.3_3",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male",
            "R67": "yes"
        },
        "notes": "Gastric anisakiasis after raw flatfish. Sharp epigastric pain with nausea/vomiting."
    },
    # Case 4: PMC5020723 - 51F, 好酸球14.1%, WBC 12000, 心窩部痛9日
    {
        "id": f"R{next_id+3}",
        "source": "Zullo 2016",
        "pmcid": "PMC5020723",
        "vignette": "51F. 間欠的心窩部痛(9日間、3日前に増悪)。悪心・嘔吐(2回)。発熱なし。心窩部圧痛あり、反跳痛・筋性防御なし。WBC 12,000(好酸球14.1%), Hb 11.0。",
        "final_diagnosis": "胃アニサキス症",
        "expected_id": "D429",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S61": "sharp_stabbing",
            "S13": "present",
            "S66": "present",
            "S65": "intermittent_colicky",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "L14": "eosinophilia",
            "T01": "1w_to_3w",
            "T02": "subacute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "female",
            "R67": "yes"
        },
        "notes": "Gastric anisakiasis in Caucasian female. Initially denied fish intake. Eosinophilia 14.1% (subacute presentation). CT: antral wall thickening + perigastric LAD."
    },
    # Case 5: PMC2532642 case 2 - 45M, 生ウナギ, 腹痛+軟便, WBC 13920, 好酸球12.8%
    {
        "id": f"R{next_id+4}",
        "source": "Shin 2009",
        "pmcid": "PMC2532642",
        "vignette": "45M. 生ウナギ摂取後に腹痛と軟便(1日3-4回)。血便・粘液便なし。発熱・筋痛なし。心窩部圧痛あり、反跳痛なし。WBC 13,920(好酸球12.8%)。",
        "final_diagnosis": "胃アニサキス症",
        "expected_id": "D429",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "epigastric",
            "S13": "present",
            "S14": "present",
            "S86": "watery",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "L14": "eosinophilia",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male",
            "R67": "yes"
        },
        "notes": "Gastric anisakiasis after raw eel. Loose stools. Eosinophilia 12.8%."
    },
]

cases.extend(new_cases)

with open('real_case_test_suite.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases (R{next_id}-R{next_id+4}), total {len(cases)}")
