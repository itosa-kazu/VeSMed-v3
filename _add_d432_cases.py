"""D432 自己免疫性胃炎 案例追加"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('real_case_test_suite.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

next_id = max(int(c['id'][1:]) for c in cases) + 1

new_cases = [
    # Case 6: PMC8610879 - 71F, macrocytic+汎血球減少, B12著減, 舌炎, めまい
    {
        "id": f"R{next_id}",
        "source": "PMC8610879 2021",
        "pmcid": "PMC8610879",
        "vignette": "71F. 1年以上のめまい・頭痛・脱力感。食欲不振。舌腫脹+平滑(glossitis)。42kg/155cm(やせ)。Hb 4.5, MCV 124.3(大球性), WBC 520, Plt 54K(汎血球減少)。B12著減。フェリチン正常。",
        "final_diagnosis": "自己免疫性胃炎(悪性貧血)",
        "expected_id": "D432",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S07": "severe",
            "S46": "present",
            "L93": "very_low_under_7",
            "L94": "macrocytic",
            "L01": "low_under_4000",
            "L100": "very_low_under_50k",
            "L22": "present",
            "L90": "normal",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "65_plus",
            "R02": "female"
        },
        "notes": "Classic pernicious anemia. MCV 124, pancytopenia. Glossitis. Anti-PCA+ anti-IF+."
    },
    # Case 2: PMC11079695 - 59M, macrocytic MCV 118, Hb 4.4, LDH 2551
    {
        "id": f"R{next_id+1}",
        "source": "PMC11079695 Cureus 2024",
        "pmcid": "PMC11079695",
        "vignette": "59M. 2週間の便秘+直腸痛。悪心・嘔吐、食欲低下、動悸、労作時呼吸困難、倦怠感。慢性アルコール歴。Hb 4.4, MCV 118.2(大球性), WBC 7.4K, Plt 179K。LDH 2551, T-Bil 3.1。B12著減。鉄正常。",
        "final_diagnosis": "自己免疫性胃炎(悪性貧血+溶血)",
        "expected_id": "D432",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S07": "severe",
            "S13": "present",
            "S46": "present",
            "S35": "present",
            "S04": "on_exertion",
            "L93": "very_low_under_7",
            "L94": "macrocytic",
            "L01": "normal_4000_10000",
            "L16": "elevated",
            "L90": "normal",
            "T01": "1w_to_3w",
            "T02": "subacute"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "male"
        },
        "notes": "Severe pernicious anemia with intravascular hemolysis. MCV 118, LDH 2551. Anti-IF+ anti-PCA+."
    },
    # Case 5: PMC3028225 - 41F, microcytic+鉄欠乏, 橋本+白斑, 6年
    {
        "id": f"R{next_id+2}",
        "source": "PMC3028225 BMJ 2011",
        "pmcid": "PMC3028225",
        "vignette": "41F. 6年来の鉄欠乏性貧血(経口鉄不応)、慢性倦怠感。橋本甲状腺炎(潜在性)+白斑33年。過多月経。Hb 10.3, MCV 78(小球性), Fe 67, フェリチン<25(鉄欠乏)。ガストリン1151(著高)。",
        "final_diagnosis": "自己免疫性胃炎(鉄欠乏型)",
        "expected_id": "D432",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S07": "mild",
            "L93": "mild_low_10_12",
            "L94": "microcytic",
            "L90": "iron_deficiency",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "female",
            "R65": "yes"
        },
        "notes": "Iron-refractory IDA type. Hashimoto's + vitiligo. Anti-gastric mucosa Ab+. Gastrin 1151."
    },
    # Case 4: PMC11963364 - 40F, normocytic, 橋本, 神経症状10年, 倦怠
    {
        "id": f"R{next_id+3}",
        "source": "PMC11963364 2025",
        "pmcid": "PMC11963364",
        "vignette": "40F. 10年来の倦怠感、広範な筋骨格痛、しびれ感、認知機能障害。橋本甲状腺炎(レボチロキシン内服中)。Hb 10.9, MCV 81.2(正球性低正常)。B12<150(欠乏)。フェリチン57(正常)。ANA 1:160。",
        "final_diagnosis": "自己免疫性胃炎(B12欠乏+神経障害型)",
        "expected_id": "D432",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S07": "mild",
            "L93": "mild_low_10_12",
            "L94": "normocytic",
            "L90": "normal",
            "L18": "positive",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "40_64",
            "R02": "female",
            "R65": "yes"
        },
        "notes": "Neuro-dominant presentation. 10-year diagnostic delay. Hashimoto's comorbid. ANA 1:160. Anti-TPO>1000."
    },
    # Case 3: PMC4983393 - 22F, normocytic, Hb 4.8, LDH 1868, 重度
    {
        "id": f"R{next_id+4}",
        "source": "PMC4983393 2016",
        "pmcid": "PMC4983393",
        "vignette": "22F. 3週間の倦怠感+労作時呼吸困難。鉄欠乏性貧血既往(輸血歴)。HR 132。結膜蒼白+強膜黄染。Hb 4.8, MCV 87.7(正球性), Plt 91K。LDH 1868。B12 60(著減)。ハプトグロビン2(著減)。",
        "final_diagnosis": "自己免疫性胃炎(悪性貧血+溶血)",
        "expected_id": "D432",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S07": "severe",
            "S04": "on_exertion",
            "E85": "present",
            "E86": "present",
            "L93": "very_low_under_7",
            "L94": "normocytic",
            "L100": "low_50k_150k",
            "L16": "elevated",
            "L98": "absent",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {
            "R01": "18_39",
            "R02": "female"
        },
        "notes": "Young 22F with severe anemia. B12 60 + iron mixed -> normocytic. Hemolysis (LDH 1868, haptoglobin 2). Anti-IF+ anti-PCA+."
    },
]

cases.extend(new_cases)

with open('real_case_test_suite.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases (R{next_id}-R{next_id+4}), total {len(cases)}")
