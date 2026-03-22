"""D433 Meckel憩室 案例追加"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('real_case_test_suite.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

next_id = max(int(c['id'][1:]) for c in cases) + 1

new_cases = [
    # Case 1: PMC4897023 - 74M, diverticulitis, fever, bilateral lower abd pain, WBC 13.5K
    {
        "id": f"R{next_id}",
        "source": "PMC4897023 2016",
        "pmcid": "PMC4897023",
        "vignette": "74M. 26時間前から急性上腹部痛→両側下腹部痛に進展。悪心あり(嘔吐なし)。発熱(38.5℃)、悪寒。腹部柔軟だが両側下腹部圧痛+voluntary guarding、反跳痛なし。便潜血陰性。WBC 13,500(桿状核31%)。",
        "final_diagnosis": "Meckel憩室炎",
        "expected_id": "D433",
        "in_scope": True,
        "evidence": {
            "E01": "38.0_39.0",
            "S12": "present",
            "S89": "diffuse",
            "S13": "present",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "65_plus",
            "R02": "male"
        },
        "notes": "Meckel's diverticulitis. 74M, bilateral lower abd pain, fever 38.5, WBC 13.5K with 31% bands."
    },
    # Case 3: PMC8005321 - 53M, suppurative diverticulitis, epigastric, fever, CRP 22
    {
        "id": f"R{next_id+1}",
        "source": "PMC8005321 2021",
        "pmcid": "PMC8005321",
        "vignette": "53M. 2日前から激しい心窩部痛(sharp)。発熱38.1℃。心窩部に圧痛性腫瘤+localized guarding。腸音低下。WBC 8,130(好中球73%), Hb 13.8, CRP 22.1 mg/dL。",
        "final_diagnosis": "Meckel憩室炎(化膿性・壊疽性)+局所膿瘍",
        "expected_id": "D433",
        "in_scope": True,
        "evidence": {
            "E01": "38.0_39.0",
            "S12": "present",
            "S89": "epigastric",
            "S64": "severe",
            "E09": "localized_tenderness",
            "L01": "normal_4000_10000",
            "L02": "high_over_10",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male"
        },
        "notes": "Suppurative/gangrenous Meckel's diverticulitis. Epigastric mass, CRP 22.1."
    },
    # Case 2a: PMC11544376 - 40M, diverticulitis+perforation, epigastric→RLQ, WBC 10.3, CRP 17
    {
        "id": f"R{next_id+2}",
        "source": "PMC11544376 2024",
        "pmcid": "PMC11544376",
        "vignette": "40M. 1日前から増悪する非典型的心窩部痛+発熱。RLQ圧痛。WBC 10.3K(好中球87%), CRP 17.08 mg/L。",
        "final_diagnosis": "Meckel憩室炎+穿孔",
        "expected_id": "D433",
        "in_scope": True,
        "evidence": {
            "E01": "37.5_38.0",
            "S12": "present",
            "S89": "RLQ",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "L02": "moderate_3_10",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male"
        },
        "notes": "Meckel's diverticulitis with perforation. Atypical epigastric pain -> RLQ tenderness."
    },
    # Case 4: PMC6323367 - 42M, diverticulitis+obstruction, periumbilical, N/V, afebrile
    {
        "id": f"R{next_id+3}",
        "source": "PMC6323367 2018",
        "pmcid": "PMC6323367",
        "vignette": "42M. 食事中に突然発症した臍周囲腹痛(10/10, sharp)。悪心+複数回の胆汁性嘔吐。発熱なし、血便なし。臍周囲圧痛、腹膜刺激徴候なし。白血球増多+好中球優位。乳酸1.9。",
        "final_diagnosis": "Meckel憩室炎+小腸閉塞",
        "expected_id": "D433",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S12": "present",
            "S89": "diffuse",
            "S64": "severe",
            "S61": "sharp_stabbing",
            "S13": "present",
            "S66": "present",
            "S67": "bilious",
            "E09": "localized_tenderness",
            "L01": "high_10000_20000",
            "T01": "under_3d",
            "T02": "sudden"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male"
        },
        "notes": "Meckel's diverticulitis with SBO. Sudden severe periumbilical pain, bilious vomiting. Leukocytosis."
    },
    # Case 10: PMC8476338 - 33M, occult bleeding/IDA, Hb 7.0, no pain
    {
        "id": f"R{next_id+4}",
        "source": "PMC8476338 2021",
        "pmcid": "PMC8476338",
        "vignette": "33M. 3週間の進行性脱力感・倦怠感・頭痛(4日前に増悪)。顕性消化管出血なし、腹痛なし、発熱なし。顔色蒼白。BP 102/61, HR 91。Hb 7.0, WBC 11,250, CRP 1.31。鉄38, フェリチン17(鉄欠乏)。直腸診:血液/黒色便なし。",
        "final_diagnosis": "反転型Meckel憩室(潜在性出血による鉄欠乏性貧血)",
        "expected_id": "D433",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S07": "severe",
            "E85": "present",
            "L93": "low_7_10",
            "L90": "iron_deficiency",
            "L01": "high_10000_20000",
            "L02": "mild_0.3_3",
            "T01": "over_3w",
            "T02": "subacute"
        },
        "risk_factors": {
            "R01": "18_39",
            "R02": "male"
        },
        "notes": "Inverted Meckel's with occult GI bleeding causing severe IDA. Hb 7.0. No overt bleeding."
    },
]

cases.extend(new_cases)

with open('real_case_test_suite.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases (R{next_id}-R{next_id+4}), total {len(cases)}")
