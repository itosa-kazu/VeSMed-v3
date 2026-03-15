#!/usr/bin/env python3
"""Add 3 ICH cases for D139."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# R270: PMC11889578 - 61M hypertensive putaminal ICH
suite["cases"].append({
    "id": "R270", "source": "Acad Pathol 2024", "pmcid": "PMC11889578",
    "vignette": "61M コントロール不良高血圧(ロサルタン+アスピリン). 突然の嘔吐+混迷+構音障害+嘔気+頭痛+左片麻痺. BP 190/110, HR 40(徐脈!), RR 20. 左片麻痺+左Babinski+右側への共同偏視. WBC 10.7k, PT/INR正常, 血糖78. CT: 右被殻に高吸収域",
    "final_diagnosis": "脳出血(右被殻, 高血圧性)",
    "expected_id": "D139", "in_scope": True,
    "evidence": {"S05": "severe", "S13": "present", "E16": "confused",
        "S52": "unilateral_weakness", "S53": "dysarthria",
        "E01": "under_37.5", "L01": "high_10000_20000",
        "L54": "normal", "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "典型的高血圧性被殻出血. BP 190/110, HR 40徐脈(Cushing反応)"
})

# R271: PMC12061495 - 45M cerebellar ICH
suite["cases"].append({
    "id": "R271", "source": "Clin Case Rep 2025", "pmcid": "PMC12061495",
    "vignette": "45M 3年間のコントロール不良高血圧(服薬不良). 突然のthunderclap headache(10/10)+射出性嘔吐3回+全身脱力+めまい+視力障害. BP 228/140(!), HR 84, RR 24, T 37.2, SpO2 100%. GCS 13(E3V4M6)→Day5: GCS 8. 左顔面麻痺+左片麻痺+運動失調. CT: 右小脳出血+第4脳室圧排+閉塞性水頭症+SAH",
    "final_diagnosis": "脳出血(右小脳, 高血圧性, 閉塞性水頭症+SAH合併)",
    "expected_id": "D139", "in_scope": True,
    "evidence": {"S05": "severe", "S13": "present", "E16": "confused",
        "S52": "unilateral_weakness",
        "E04": "tachypnea_20_30", "E01": "under_37.5",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "小脳出血. BP 228/140. GCS 13→8→死亡. ラボなし(財政制約)"
})

# R272: PMC11440890 - 61F warfarin-associated lobar ICH
suite["cases"].append({
    "id": "R272", "source": "Cureus 2024", "pmcid": "PMC11440890",
    "vignette": "61F 高血圧/発作性AF/機械弁置換後(ワルファリン+アスピリン). 間欠的頭痛+突然の右手脱力・巧緻運動障害. BP 126/58, HR 75, RR 16, T 36.4, SpO2 96%. GCS 15, NIHSS 2. 右上肢筋力低下. 心筋マーカー陰性. CT: 左頭頂葉出血2.3x1.7x2.7cm+正中偏位0.3cm. PCCで凝固補正",
    "final_diagnosis": "脳出血(左頭頂葉, ワルファリン関連)",
    "expected_id": "D139", "in_scope": True,
    "evidence": {"S05": "mild", "S52": "unilateral_weakness",
        "E01": "under_37.5", "E05": "mild_hypoxia_93_96",
        "L53": "normal",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "female", "R48": "yes", "R44": "yes"},
    "result": "", "notes": "ワルファリン関連ICH. GCS 15, NIHSS 2(軽症). PCC+VitK"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R270-R272. Total: {len(suite['cases'])}")
