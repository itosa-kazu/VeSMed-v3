#!/usr/bin/env python3
"""Add 3 ischemic stroke cases for D138."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# R273: PMC11453048 - 65M atherothrombotic MCA
suite["cases"].append({
    "id": "R273", "source": "Cureus 2024", "pmcid": "PMC11453048",
    "vignette": "65M 高血圧/DM/心筋梗塞既往. 突然の左片麻痺+表出性失語+意識低下+嘔気+めまい. BP 160/100, HR 82, RR 20, SpO2 93%, T 36.9. 血糖180. NIHSS 15. CT陰性→CTA: 右MCA近位閉塞. tPA+血栓回収術. Day2: NIHSS 25+梗塞内出血",
    "final_diagnosis": "急性脳梗塞(右MCA, アテローム血栓性, 悪性梗塞)",
    "expected_id": "D138", "in_scope": True,
    "evidence": {"S52": "unilateral_weakness", "S53": "aphasia",
        "E16": "confused", "S13": "present",
        "E05": "mild_hypoxia_93_96", "E01": "under_37.5",
        "L54": "hyperglycemia",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "male", "R04": "yes", "R44": "yes"},
    "result": "", "notes": "典型的大血管閉塞. NIHSS 15. 血糖180(ストレス). tPA+EVT"
})

# R274: PMC12861334 - 64M cardioembolic (LV thrombus)
suite["cases"].append({
    "id": "R274", "source": "Cureus 2025", "pmcid": "PMC12861334",
    "vignette": "64M 高血圧/T2DM/脂質異常. 突然の左上肢脱力+左口角偏位+軽度構音障害. 意識清明. BP 128/68, HR 95, SpO2 94%. WBC 5.02k, CRP 1.29, 血糖203, PLT 136k(低). hs-トロポニン1724(!), CK 219. ECG: V1-V5 ST上昇(evolving anterior MI). Echo: 左室心尖部血栓+EF 41%. CT: ASPECTS 10. 24h CT: 右レンズ核線条体梗塞",
    "final_diagnosis": "急性脳梗塞(心原性, LV血栓, silent STEMI)",
    "expected_id": "D138", "in_scope": True,
    "evidence": {"S52": "unilateral_weakness", "S53": "dysarthria",
        "E16": "normal", "E02": "under_100",
        "E05": "mild_hypoxia_93_96", "E01": "under_37.5",
        "L01": "normal_4000_10000", "L02": "mild_0.3_3",
        "L54": "hyperglycemia", "L53": "very_high",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male", "R04": "yes"},
    "result": "", "notes": "Silent MI→LV血栓→脳塞栓. トロポニン1724. ECG ST上昇"
})

# R275: PMC11659910 - 38M lacunar (pontine + PRES)
suite["cases"].append({
    "id": "R275", "source": "Cureus 2024", "pmcid": "PMC11659910",
    "vignette": "38M CKD(eGFR 28). 2ヶ月の頭痛悪化+新規めまい+左半身しびれ. 意識清明. BP 245/171(!), HR 97, RR 20, SpO2 98%, T 36.9. WBC 5.17k, Cr 2.82, 血糖99(正常), ProBNP 5902, トロポニン1361. MRI: 左橋にDWI高信号(急性ラクナ梗塞)+小脳浮腫(PRES)",
    "final_diagnosis": "急性脳梗塞(橋ラクナ梗塞, 高血圧緊急症+PRES合併)",
    "expected_id": "D138", "in_scope": True,
    "evidence": {"S05": "severe", "S52": "absent",
        "E16": "normal", "E02": "under_100",
        "E05": "normal_over_96", "E01": "under_37.5",
        "L01": "normal_4000_10000", "L54": "normal",
        "L53": "very_high", "L51": "very_high",
        "T01": "over_3w", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "BP 245/171高血圧緊急症. 橋ラクナ+PRES. 片麻痺なし(しびれのみ). ProBNP 5902"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R273-R275. Total: {len(suite['cases'])}")
