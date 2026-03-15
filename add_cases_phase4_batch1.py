#!/usr/bin/env python3
"""Add 9 cases: D140 DKA x3, D141 hypoglycemia x3, D142 status epilepticus x3."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# === D140 DKA x3 ===
suite["cases"].append({
    "id": "R261", "source": "Cureus 2021", "pmcid": "PMC7884107",
    "vignette": "22F 新規T1DM(未診断). ケトジェニックダイエット4日後に2日間の急性呼吸困難+経口摂取不能. HR 110, BP 110/80, RR 32(Kussmaul), T 38.0. 血糖356-390, pH 7.15, HCO3 4.8, AG 24.2, BHB 6.65. WBC 15800. HbA1c 14%",
    "final_diagnosis": "DKA(新規T1DM, ケトジェニックダイエット誘発)",
    "expected_id": "D140", "in_scope": True,
    "evidence": {"L54": "hyperglycemia", "S04": "at_rest", "E04": "severe_over_30",
        "E02": "100_120", "E01": "38.0_39.0", "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "female"},
    "result": "", "notes": "pH 7.15, AG 24.2. 血糖356(hyperglycemia,<500)"
})
suite["cases"].append({
    "id": "R262", "source": "Case Rep Endocrinol 2020", "pmcid": "PMC7364458",
    "vignette": "30M LADA(T2DMと誤診,メトホルミン中). ケトダイエット後に腹痛+嘔吐(コーヒー残渣様)+Kussmaul呼吸+27kg体重減少. HR 98, BP 159/100, RR 26, T 36.7, SpO2 99%. 血糖424, pH 6.97(!), HCO3 6, AG 30.7, BHB>8.0. K 4.7, Cr 1.64",
    "final_diagnosis": "DKA(LADA, ケトジェニックダイエット誘発, pH 6.97)",
    "expected_id": "D140", "in_scope": True,
    "evidence": {"L54": "hyperglycemia", "S12": "epigastric", "S13": "present",
        "S17": "present", "E04": "tachypnea_20_30", "E02": "under_100",
        "E01": "under_37.5", "L44": "other",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male", "R04": "yes"},
    "result": "", "notes": "pH 6.97極度アシドーシス. 血糖424. LADA→T1DM再分類"
})
suite["cases"].append({
    "id": "R263", "source": "Cureus 2020", "pmcid": "PMC7598147",
    "vignette": "24M T1DM(服薬不良, HbA1c 15.8%), BMI 32.1. COVID-19感染後に嘔気嘔吐+吐血+倦怠感+悪寒+乾性咳嗽. HR 122, BP 141/84, RR 16, T 36.4, SpO2 95%. 血糖507, pH 7.16, HCO3 2(!), AG 30.6. WBC 10800, K 4.6",
    "final_diagnosis": "DKA(T1DM+COVID-19誘発, 死亡転帰)",
    "expected_id": "D140", "in_scope": True,
    "evidence": {"L54": "very_high_over_500", "S13": "present", "S01": "dry",
        "S07": "severe", "E02": "over_120", "E01": "under_37.5",
        "E05": "mild_hypoxia_93_96", "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male", "R04": "yes"},
    "result": "", "notes": "血糖507(very_high). pH 7.16, HCO3 2. COVID合併. Day9死亡"
})

# === D141 Hypoglycemia x3 ===
suite["cases"].append({
    "id": "R264", "source": "J Emerg Trauma Shock 2012", "pmcid": "PMC3354941",
    "vignette": "27F 医療従事者. インスリン自己注射(自殺企図). 傾眠→90分で昏睡+全身性強直間代性痙攣. HR 34(徐脈!), BP 80/50, T 37.2. 血糖35mg/dL, インスリン402(著高), C-peptide<0.3(抑制). WBC 7400. 90時間意識不明. ブドウ糖470g投与",
    "final_diagnosis": "重症低血糖(インスリン過量投与, 自殺企図)",
    "expected_id": "D141", "in_scope": True,
    "evidence": {"L54": "hypoglycemia", "E16": "obtunded", "S42": "present",
        "E03": "hypotension_under_90", "E01": "under_37.5",
        "L01": "normal_4000_10000",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "female"},
    "result": "", "notes": "血糖35. インスリン402, C-peptide<0.3(外因性). HR 34徐脈"
})
suite["cases"].append({
    "id": "R265", "source": "Cureus 2025", "pmcid": "PMC12318583",
    "vignette": "56F 高血圧のみ(DM既往なし). 旅行中に痙攣発作→意識回復せず+発汗+混迷. T 34.3(低体温), RR 23. 血糖18→14mg/dL(著明低下). WBC 16k. 膵体尾部に1.2cm嚢胞性病変(インスリノーマ疑い)",
    "final_diagnosis": "重症低血糖(インスリノーマ疑い)",
    "expected_id": "D141", "in_scope": True,
    "evidence": {"L54": "hypoglycemia", "E16": "obtunded", "S42": "present",
        "E01": "under_37.5", "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "female"},
    "result": "", "notes": "血糖14mg/dL. DM既往なし→インスリノーマ. 低体温34.3"
})
suite["cases"].append({
    "id": "R266", "source": "Cureus 2024", "pmcid": "PMC11621970",
    "vignette": "61M T2DM. 経口血糖降下薬過量→意識不明(6時間以上). HR 68, BP 140/70, T 36.1, RR 14, SpO2 98%. GCS 7(E1V2M4), 瞳孔2mm緩慢反応. 血糖19mg/dL. CBC/電解質/腎機能正常. 50%ブドウ糖50mLで血糖110に回復",
    "final_diagnosis": "重症低血糖(経口血糖降下薬過量)",
    "expected_id": "D141", "in_scope": True,
    "evidence": {"L54": "hypoglycemia", "E16": "obtunded",
        "E02": "under_100", "E01": "under_37.5",
        "L01": "normal_4000_10000",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male", "R04": "yes"},
    "result": "", "notes": "血糖19. GCS 7. 50%ブドウ糖で速やかに回復"
})

# === D142 Status Epilepticus x3 ===
suite["cases"].append({
    "id": "R267", "source": "Cureus 2022", "pmcid": "PMC9436493",
    "vignette": "70F DM(コントロール不良)/CKD3/冠動脈疾患/甲状腺機能低下. 左半盲+左側しびれ/脱力(脳梗塞と紛らわしい). HR 67, BP 131/61, T 36.4, RR 18, SpO2 100%. WBC 11.8k, 血糖583(!), Na 131. CT正常. CTA: 左後頭葉過灌流. EEG: 左後頭葉focal SE",
    "final_diagnosis": "てんかん重積(焦点性, 後頭葉, 脳梗塞mimicker)",
    "expected_id": "D142", "in_scope": True,
    "evidence": {"S52": "unilateral_weakness", "E16": "normal",
        "L54": "very_high_over_500", "E02": "under_100",
        "E01": "under_37.5", "L01": "high_10000_20000",
        "L44": "hyponatremia",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "female", "R04": "yes"},
    "result": "", "notes": "血糖583→代謝性誘因. 脳梗塞mimickerだがEEGでSE確認. 意識清明"
})
suite["cases"].append({
    "id": "R268", "source": "Seizure 2022", "pmcid": "PMC9301094",
    "vignette": "81M 高血圧/脳梗塞既往. COVID-19感染中に左顔面攣縮+左上肢ミオクローヌス>30分. T 38.2, 左片麻痺+Babinski. WBC 8.8k, CRP 104, CPK 734, K 5.5. MRI: 右側頭葉急性脳梗塞. EEG: 右前側頭4Hz棘徐波→焦点性SE",
    "final_diagnosis": "てんかん重積(焦点性, COVID-19+脳梗塞合併)",
    "expected_id": "D142", "in_scope": True,
    "evidence": {"S42": "present", "S52": "unilateral_weakness",
        "E16": "confused", "E01": "38.0_39.0",
        "S05": "mild", "S01": "dry", "S04": "on_exertion",
        "L01": "normal_4000_10000", "L02": "high_over_10",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "male", "R48": "yes"},
    "result": "", "notes": "COVID+脳梗塞→SE. CRP 104, CPK 734. 3週後死亡"
})
suite["cases"].append({
    "id": "R269", "source": "Seizure 2020", "pmcid": "PMC7405327",
    "vignette": "32M 既往なし. COVID-19接触歴. 40分間の持続性全身性強直間代性痙攣→意識不明. HR 110, BP 125/80, T 37.1, RR 20, SpO2 96%. リンパ球800(減少), CRP 56, 血糖126(軽度上昇). CSF蛋白2212(著高). CT正常. ジアゼパム無効→ミダゾラム5mgで停止→挿管36h",
    "final_diagnosis": "てんかん重積(全身性強直間代性, COVID-19関連)",
    "expected_id": "D142", "in_scope": True,
    "evidence": {"S42": "present", "E16": "obtunded",
        "E02": "100_120", "E01": "under_37.5",
        "E05": "mild_hypoxia_93_96", "L02": "moderate_3_10",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "40分間持続GTCS. CSF蛋白2212著高. COVID-19関連. 14日後退院"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R261-R269. Total: {len(suite['cases'])}")
