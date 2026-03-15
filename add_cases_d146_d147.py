#!/usr/bin/env python3
"""Add 3 hypertensive emergency (D146) + 3 testicular torsion (D147) cases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# D146 Hypertensive Emergency x3
suite["cases"].append({
    "id": "R288", "source": "Cureus 2022", "pmcid": "PMC9377384",
    "vignette": "32M BP 224/113. 意識変容+混迷+頭痛+過眠+一過性左片麻痺+間代性運動. HR 64, SpO2 96%. Cr 2.48, トロポニン0.14, T-Bil 2.3. CT: 右頭頂葉灰白質境界不明瞭. MRI: 右側頭頭頂後頭梗塞+PRES+脳ヘルニア. 両側減圧開頭術",
    "final_diagnosis": "高血圧緊急症(PRES+脳梗塞+AKI)",
    "expected_id": "D146", "in_scope": True,
    "evidence": {"E38": "crisis_over_180", "S05": "severe",
        "E16": "obtunded", "S52": "unilateral_weakness", "S42": "present",
        "L53": "mildly_elevated", "E01": "under_37.5",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "BP 224/113. PRES+脳梗塞+ヘルニア. 両側減圧開頭. Cr 2.48 AKI"
})

suite["cases"].append({
    "id": "R289", "source": "BMJ Case Rep 2014", "pmcid": "PMC4240409",
    "vignette": "28M Black. BP 218/120. 頭痛+嘔気嘔吐. Cr 264→1144umol/L(重症AKI→9ヶ月透析). Hb 10.8, PLT 71k, LDH 1392, ハプトグロビン<30, 末梢血破砕赤血球(TMA). 眼底: 火炎状出血+滲出物(III-IV度). 腎生検: TMA",
    "final_diagnosis": "悪性高血圧(AKI+TMA+高血圧性網膜症)",
    "expected_id": "D146", "in_scope": True,
    "evidence": {"E38": "crisis_over_180", "S05": "severe", "S13": "present",
        "E01": "under_37.5", "L16": "elevated",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "悪性高血圧. LDH 1392+PLT 71k+破砕赤血球=TMA. 9ヶ月透析"
})

suite["cases"].append({
    "id": "R290", "source": "Case Rep Cardiol 2021", "pmcid": "PMC8110033",
    "vignette": "55M BP 300/180(!). 中等度腹痛(胸痛/背部痛なし→非典型解離). ECG: 完全房室ブロック. Cr 2.0, CRP 364. CXR: 縦隔拡大. CT: Stanford B型解離(左鎖骨下→左腎動脈上). Echo: LVH+拡張障害. 眼底: I度網膜症. VDDペースメーカー",
    "final_diagnosis": "高血圧緊急症(Type B解離+完全AVブロック)",
    "expected_id": "D146", "in_scope": True,
    "evidence": {"E38": "crisis_over_180", "S12": "diffuse",
        "L02": "high_over_10", "E01": "under_37.5",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "BP 300/180極度. 非典型解離(腹痛のみ). 完全AVブロック. CRP 364"
})

# D147 Testicular Torsion x3
suite["cases"].append({
    "id": "R291", "source": "Cureus 2022", "pmcid": "PMC9197752",
    "vignette": "21M 既往なし. 3.5時間前から突然の右下腹部痛(陰嚢放散)+陰嚢圧痛. 排便促迫+下痢+放屁増加. 排尿症状なし. BP 128/71, HR 92, RR 16, T 36.6, SpO2 100%. 右精巣高位+著明圧痛. WBC 11.6k. 尿: WBC 3/HPF, LE/亜硝酸陰性. CT: whirl sign. 48h後Echo: 血流なし. 精巣摘除(540度捻転, 壊死)",
    "final_diagnosis": "精巣捻転(右, 540度, 壊死→摘除)",
    "expected_id": "D147", "in_scope": True,
    "evidence": {"S13": "present", "E01": "under_37.5",
        "E02": "under_100", "L01": "high_10000_20000",
        "L05": "normal",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "RLQ痛で受診→精巣捻転見逃し48h→壊死. whirl sign on CT"
})

suite["cases"].append({
    "id": "R292", "source": "Urol Case Rep 2018", "pmcid": "PMC6050561",
    "vignette": "15M 48時間の左陰嚢痛+腫脹+嘔気嘔吐+37.4度微熱. 左陰嚢著明発赤腫脹. WBC 16300. 尿正常. Echo: 左精巣血流なし(360-720度捻転, 壊死→摘除). 入院中に右陰嚢急性痛→Echo: 右も血流なし(360度捻転→整復+固定). Bell clapper変形",
    "final_diagnosis": "両側精巣捻転(左壊死摘除, 右整復成功)",
    "expected_id": "D147", "in_scope": True,
    "evidence": {"S13": "present", "E01": "37.5_38.0",
        "L01": "high_10000_20000", "L05": "normal",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "両側捻転は極めて稀. 左48h遅延→壊死. WBC 16.3k"
})

suite["cases"].append({
    "id": "R293", "source": "Cureus 2019", "pmcid": "PMC6863585",
    "vignette": "18M 1時間前から突然の右精巣痛(10/10, 鋭い, 持続性). 座位で発症. 右精巣硬い・高位・腫脹・圧痛. 挙睾筋反射消失. Echo: 右精巣血流なし+低エコー+精巣上体腫大+水瘤. 手術: 720度捻転→整復+両側固定",
    "final_diagnosis": "精巣捻転(右, 720度, 整復成功)",
    "expected_id": "D147", "in_scope": True,
    "evidence": {"E01": "under_37.5",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "1時間の超急性. 10/10激痛. 挙睾筋反射消失(特異的). 720度→救済"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R288-R293. Total: {len(suite['cases'])}")
