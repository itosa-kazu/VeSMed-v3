#!/usr/bin/env python3
"""Backfill 4 new cases for D111/D112/D115/D118."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# D111 SJS/TEN - PMC7176330 46F amoxicillin
suite["cases"].append({
    "id": "R240", "source": "Cureus 2020", "pmcid": "PMC7176330",
    "vignette": "46F 高血圧. アモキシシリン3週前処方. 眼痛/充血+口唇びらん+咽頭痛+背部/下肢/胸部の紫斑性丘疹+手掌足底水疱+悪寒. WBC 15.0k, CRP 207.9, ESR 106. Nikolsky sign+. 皮膚生検:全層表皮壊死+表皮下水疱",
    "final_diagnosis": "スティーブンス・ジョンソン症候群(アモキシシリン)",
    "expected_id": "D111", "in_scope": True,
    "evidence": {
        "E12": "vesicle_bulla", "E35": "conjunctivitis", "S02": "present",
        "S18": "rash_widespread", "L01": "high_10000_20000",
        "L02": "high_over_10", "L28": "very_high_over_100",
        "T01": "1w_to_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "40_64", "R02": "female", "R08": "yes"},
    "result": "", "notes": "WBC 15k, CRP 207.9, ESR 106. Nikolsky+. 全層表皮壊死"
})

# D112 PAN - PMC10979759 48M splenic aneurysm rupture
suite["cases"].append({
    "id": "R241", "source": "Cureus 2024", "pmcid": "PMC10979759",
    "vignette": "48M コカイン/覚醒剤使用歴. 3日間の進行性びまん性腹痛+嘔気. T 38.42, HR 105, BP 90/60, RR 30, SpO2 98%(O2 2L). Hb 8.5->6.3, Cr 2.3, 乳酸6.3, PCT 1.31, CRP 59, ESR 24, ANCA陰性. CT:脾動脈瘤2cm+腹腔内出血. IR塞栓術+ステロイド+シクロホスファミド",
    "final_diagnosis": "結節性多発動脈炎(脾動脈瘤破裂)",
    "expected_id": "D112", "in_scope": True,
    "evidence": {
        "S12": "diffuse", "S13": "present", "E01": "38.0_39.0",
        "E02": "100_120", "E03": "hypotension_under_90",
        "L02": "moderate_3_10", "L03": "high_over_0.5",
        "L28": "elevated", "L19": "negative",
        "T01": "under_3d", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "PAN+脾動脈瘤破裂. 乳酸6.3, Hb急落. 非典型的PAN"
})

# D115 DGI - PMC8383516 27F
suite["cases"].append({
    "id": "R242", "source": "J Med Cases 2021", "pmcid": "PMC8383516",
    "vignette": "27F 健康. 4日間の発熱39度+咽頭痛+有痛性皮疹(手掌膿疱/壊死性丘疹)+筋肉痛+左足首/右肘/手首の関節痛+倦怠感. HR 82, BP 127/72, RR 16, SpO2 100%. WBC 12.89k(好中球73.6%), CRP 69.8. 左足首腱鞘炎. 血培: N.gonorrhoeae陽性",
    "final_diagnosis": "播種性淋菌感染症(関節炎-皮膚炎症候群)",
    "expected_id": "D115", "in_scope": True,
    "evidence": {
        "E01": "39.0_40.0", "S08": "present", "S02": "present",
        "S06": "present", "E12": "petechiae_purpura",
        "L01": "high_10000_20000", "L02": "moderate_3_10",
        "L09": "gram_negative",
        "T01": "under_3d", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "18_39", "R02": "female"},
    "result": "", "notes": "典型的DGI. 血培GN diplococci陽性. 膿疱+腱鞘炎"
})

# D118 Brain abscess - PMC4181053 31M otogenic
suite["cases"].append({
    "id": "R243", "source": "Case Rep Med 2014", "pmcid": "PMC4181053",
    "vignette": "31M 3週間の発熱39.5+頭痛+右耳痛+耳漏→急性意識変容. HR 99, RR 28, BP 160/100. WBC 28900, CRP 136. 側頭骨CT:右中耳/乳突洞に軟部組織充満. 脳MRI:右視床に1.6x1.2cm被膜化膿瘍. CSF: WBC 12800. 肺炎球菌",
    "final_diagnosis": "耳原性脳膿瘍(右視床, S.pneumoniae)",
    "expected_id": "D118", "in_scope": True,
    "evidence": {
        "E01": "39.0_40.0", "S05": "severe", "E16": "confused",
        "L01": "very_high_over_20000", "L02": "high_over_10",
        "L46": "other", "E04": "tachypnea_20_30",
        "T01": "over_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "耳原性脳膿瘍. WBC 28900, CRP 136. 3週間経過"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)

print(f"Added R240-R243. Total: {len(suite['cases'])}")
