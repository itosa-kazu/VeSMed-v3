"""D434裂肛 + D435痔瘻 + D436便秘症 案例追加"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('real_case_test_suite.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)

next_id = max(int(c['id'][1:]) for c in cases) + 1

new_cases = [
    # === D434 裂肛 (3件) ===
    # Case 1: PMC12947789 case1 - 28M, 18ヶ月間, 排便時鮮血+激痛VAS9, 便秘
    {
        "id": f"R{next_id}",
        "source": "PMC12947789 2025 case1",
        "pmcid": "PMC12947789",
        "vignette": "28M. 18ヶ月間の間欠性排便時鮮血便。重度肛門痛(VAS 9/10)。時折の便秘。後方裂肛+sentinel pile。発熱なし。",
        "final_diagnosis": "慢性裂肛",
        "expected_id": "D434",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S190": "present",
            "S26": "present",
            "S72": "present",
            "E91": "fissure",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {"R01": "18_39", "R02": "male"},
        "notes": "Chronic anal fissure 18 months. Severe pain VAS 9/10. Bleeding + constipation. Posterior fissure."
    },
    # Case 2: PMC12947789 case2 - 47M, 1年, 排便後激痛, 出血なし
    {
        "id": f"R{next_id+1}",
        "source": "PMC12947789 2025 case2",
        "pmcid": "PMC12947789",
        "vignette": "47M. 1年間の再発性排便後肛門痛(VAS 9/10)。出血・排膿なし。掻痒感あり。ニフェジピン3ヶ月無効。後方裂肛(圧痛あり)。発熱なし。",
        "final_diagnosis": "慢性裂肛",
        "expected_id": "D434",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S190": "present",
            "E91": "fissure",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {"R01": "40_64", "R02": "male"},
        "notes": "Chronic anal fissure 1 year. Pain only, no bleeding. Failed nifedipine."
    },
    # Case 3: PMC6344920 - 44M, 4年, 排便時痛+出血, 慢性
    {
        "id": f"R{next_id+2}",
        "source": "PMC6344920 2019",
        "pmcid": "PMC6344920",
        "vignette": "44M. 4年前から排便時の強い肛門痛と少量〜中等量の出血。保存的治療(鎮痛薬/軟膏)で改善なし。6時方向の慢性裂肛+3時/11時方向痔核。発熱なし。",
        "final_diagnosis": "慢性裂肛+痔核",
        "expected_id": "D434",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S190": "present",
            "S26": "present",
            "E91": "fissure",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {"R01": "40_64", "R02": "male"},
        "notes": "Chronic anal fissure 4 years. Pain + bleeding at defecation. Failed conservative treatment."
    },

    # === D435 痔瘻 (3件) ===
    # Case 1: PMC8761684 - 31M, 2年肛門周囲掻痒+排膿, 膿瘍既往, labs正常
    {
        "id": f"R{next_id+3}",
        "source": "PMC8761684 2022",
        "pmcid": "PMC8761684",
        "vignette": "31M. 2年間の肛門周囲掻痒+排出物。3年前に肛門周囲膿瘍→切開排膿。腹痛なし、排便習慣変化なし、出血なし、発熱なし。3時方向に前回手術瘢痕+外瘻孔。CBC/肝腎パネル正常。",
        "final_diagnosis": "肛門周囲瘻",
        "expected_id": "D435",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "E91": "fistula",
            "L01": "normal_4000_10000",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {"R01": "18_39", "R02": "male"},
        "notes": "Anal fistula 2 years. Prior perianal abscess. Discharge, no bleeding/fever. Labs normal."
    },
    # Case 2: PMC3649308 - 36M, 2週間肛門痛+排膿
    {
        "id": f"R{next_id+4}",
        "source": "PMC3649308 2013",
        "pmcid": "PMC3649308",
        "vignette": "36M. 2週間の肛門痛+間欠性肛門周囲排出物。既往歴なし。7時方向に外瘻孔、同部位に硬結・軽度圧痛。発熱なし。",
        "final_diagnosis": "肛門周囲瘻(異物)",
        "expected_id": "D435",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S190": "present",
            "E91": "fistula",
            "T01": "1w_to_3w",
            "T02": "subacute"
        },
        "risk_factors": {"R01": "18_39", "R02": "male"},
        "notes": "Anal fistula 2 weeks. Pain + intermittent discharge. Foreign body (pork bone)."
    },
    # Case 3: PMC12445932 - 32F, 反復性膿瘍→瘻, 発熱+悪寒, WBC 38K, CRP 141
    {
        "id": f"R{next_id+5}",
        "source": "PMC12445932 Cureus 2025",
        "pmcid": "PMC12445932",
        "vignette": "32F. 右臀部~大腿の腫脹・疼痛。発熱・悪寒。低血圧(75/52)。初回ドレナージ後の反復性肛門周囲膿瘍。右大腿圧痛+発赤+硬結+波動。WBC 38.1K, CRP 141.4。",
        "final_diagnosis": "複雑痔瘻(反復性肛門周囲膿瘍)",
        "expected_id": "D435",
        "in_scope": True,
        "evidence": {
            "E01": "38.0_39.0",
            "S190": "present",
            "S09": "present",
            "E91": "abscess",
            "L01": "very_high_over_20000",
            "L02": "high_over_10",
            "T01": "under_3d",
            "T02": "acute"
        },
        "risk_factors": {"R01": "18_39", "R02": "female"},
        "notes": "Complex fistula with recurrent abscess. Septic: WBC 38K, CRP 141, hypotension."
    },

    # === D436 便秘症 (3件) ===
    # Case 1: PMC4594448 - 13M, 慢性便秘(2歳から), 腹痛+嘔吐, labs正常
    {
        "id": f"R{next_id+6}",
        "source": "PMC4594448 2015",
        "pmcid": "PMC4594448",
        "vignette": "13M. 2歳から慢性便秘、今回3週間の糞便嵌頓。重度腹痛(痙攣性)、嘔吐、経口摂取低下。硬い大きな便、最大8日間排便なし。腹部膨隆、びまん性圧痛、硬い糞塊触知。電解質・CBC・甲状腺正常。発熱なし(36.4℃)。",
        "final_diagnosis": "慢性機能性便秘(糞便嵌頓)",
        "expected_id": "D436",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S72": "present",
            "S12": "present",
            "S89": "diffuse",
            "S66": "present",
            "E44": "severe",
            "E09": "localized_tenderness",
            "L01": "normal_4000_10000",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {"R01": "13_17", "R02": "male"},
        "notes": "Chronic functional constipation since age 2. Fecal impaction 3 weeks. Normal labs."
    },
    # Case 2: PMC12894083 - 21M, 数年間慢性便秘, 腹部膨隆, 頻脈
    {
        "id": f"R{next_id+7}",
        "source": "PMC12894083 2025",
        "pmcid": "PMC12894083",
        "vignette": "21M. 数年来の慢性便秘(複数回入院歴)。腹部膨隆、不快感、膨満感。最終排便は数週間前。腸音低下、著明な腹部膨隆、全腸管に硬便触知、軽度圧痛(反跳痛なし)。頻脈(HR 120)。",
        "final_diagnosis": "難治性慢性便秘",
        "expected_id": "D436",
        "in_scope": True,
        "evidence": {
            "E01": "under_37.5",
            "S72": "present",
            "E44": "severe",
            "E09": "localized_tenderness",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {"R01": "18_39", "R02": "male"},
        "notes": "Refractory chronic constipation. Severe abdominal distension. Multiple hospitalizations."
    },
    # Case 3: PMC7440070 - 28F, 5年間便秘, 妊娠中悪化, 腹痛+膨満
    {
        "id": f"R{next_id+8}",
        "source": "PMC7440070 2020",
        "pmcid": "PMC7440070",
        "vignette": "28F. 5年間の慢性便秘(3-4日に1回硬便)。妊娠27週で悪化。7日間の膨満感増悪+腹部疝痛。放屁・排便不能。持続性重度腹痛。",
        "final_diagnosis": "遅延性通過便秘→イレウス",
        "expected_id": "D436",
        "in_scope": True,
        "evidence": {
            "S72": "present",
            "S12": "present",
            "S64": "severe",
            "S65": "progressive",
            "E44": "severe",
            "T01": "over_3w",
            "T02": "chronic"
        },
        "risk_factors": {"R01": "18_39", "R02": "female"},
        "notes": "Slow transit constipation 5 years. Pregnancy exacerbation -> ileus. Severe pain + distension."
    },
]

cases.extend(new_cases)

with open('real_case_test_suite.json', 'w', encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases (R{next_id}-R{next_id+8}), total {len(cases)}")
