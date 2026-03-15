#!/usr/bin/env python3
"""Add 3 CO poisoning (D149) + 3 acute liver failure (D151) cases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# D149 CO Poisoning x3
suite["cases"].append({
    "id": "R294", "source": "Cureus 2025", "pmcid": "PMC12247657",
    "vignette": "82F 高血圧/脂質異常/虚血性心疾患. 炭火暖房で曝露. 進行性意識障害(GCS 9)+構音障害+流涎. HR 92, BP 110, SpO2 98%(偽正常!), T 38.2, RR 22. COHb 33.5%. トロポニン203→748(II型MI). 乳酸3.0. CT正常. CXR: 肺水腫. HBOT→GCS 15に回復",
    "final_diagnosis": "一酸化炭素中毒(COHb 33.5%, 脳卒中mimic)",
    "expected_id": "D149", "in_scope": True,
    "evidence": {"E16": "obtunded", "S53": "dysarthria", "S05": "severe",
        "E02": "under_100", "E01": "38.0_39.0",
        "L53": "mildly_elevated",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "female", "R44": "yes"},
    "result": "", "notes": "SpO2 98%偽正常! COHb 33.5%. 脳卒中と誤診されやすい"
})

suite["cases"].append({
    "id": "R295", "source": "BMC Emerg Med 2024", "pmcid": "PMC11653981",
    "vignette": "23M ディーゼル燃料の室内曝露. 前夜: 嘔気+下痢+腹痛. 翌朝意識不明(GCS 8→10). 両側Babinski陽性. COHb 28.8%. トロポニン1.47(上昇). ABG: pH 7.43. CT: 両側深部白質低吸収域(中毒性白質脳症). HBO 2回+ICU",
    "final_diagnosis": "一酸化炭素中毒(COHb 28.8%, 白質脳症)",
    "expected_id": "D149", "in_scope": True,
    "evidence": {"E16": "obtunded", "S13": "present", "S12": "diffuse",
        "L53": "mildly_elevated",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "前駆症状(嘔気下痢)→翌朝昏睡. COHb 28.8%. CT白質病変"
})

suite["cases"].append({
    "id": "R296", "source": "Medicine 2019", "pmcid": "PMC6485747",
    "vignette": "73F 室内ストーブ(換気不良). 3時間前からめまい+倦怠感+呼吸困難+嘔吐+胸やけ. HR 110(不整脈), BP 120/80, SpO2 90%, RR 30. COHb 17%. トロポニン4.75→69.42(NSTEMI!), CK-MB 1494, 乳酸8.7, pH 7.196, BNP 1113, 血糖22.89mmol/L. CXR: 肺水腫. Day8にPCI",
    "final_diagnosis": "一酸化炭素中毒+NSTEMI(CO誘発性心筋梗塞)",
    "expected_id": "D149", "in_scope": True,
    "evidence": {"S05": "mild", "S13": "present", "S04": "at_rest",
        "S07": "severe", "E02": "100_120", "E05": "mild_hypoxia_93_96",
        "E04": "severe_over_30",
        "L53": "very_high", "L51": "very_high",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "female"},
    "result": "", "notes": "CO→NSTEMI. トロポニン69.42(著高). 乳酸8.7, pH 7.2. BNP 1113"
})

# D151 Acute Liver Failure x3
suite["cases"].append({
    "id": "R297", "source": "BMC Gastroenterol 2021", "pmcid": "PMC8647103",
    "vignette": "45F 39-40度発熱+頭痛+食欲不振+脱力+嘔吐+腹痛→意識混濁→昏睡(GCS 3, 肝性脳症IV度). WBC 10.4k, AST 983, ALT 2173, T-Bil 10.5→12.9, INR 7.1, PT<4%. 抗HAV IgM陽性. Echo: 肝軽度腫大. NAC+ラクツロース→10日退院, 6ヶ月で完全回復",
    "final_diagnosis": "急性肝不全(A型肝炎, 劇症化)",
    "expected_id": "D151", "in_scope": True,
    "evidence": {"E01": "39.0_40.0", "E16": "obtunded", "E18": "present",
        "S13": "present", "S07": "severe", "S05": "severe",
        "L11": "very_high", "L01": "high_10000_20000",
        "T01": "3d_to_1w", "T02": "gradual_days"},
    "risk_factors": {"R01": "40_64", "R02": "female"},
    "result": "", "notes": "HAV劇症化. GCS 3. INR 7.1. ALT 2173. 移植なしで回復"
})

suite["cases"].append({
    "id": "R298", "source": "Cureus 2022", "pmcid": "PMC9125438",
    "vignette": "30F アセトアミノフェン約30g内服3日前. 混迷(GCS 13)+嘔気+右季肋部痛+口腔乾燥+末梢冷感. HR 110, BP 85/40, RR 24, SpO2 99%, CRT>5秒. ALT 6000, INR 5.5, アンモニア160, WBC 12.3k, PLT 120k, Cr 200, 血糖3.8(低血糖), pH 7.19, 乳酸6.0. CT: 肝均一, 門脈開存",
    "final_diagnosis": "急性肝不全(アセトアミノフェン中毒)",
    "expected_id": "D151", "in_scope": True,
    "evidence": {"E16": "confused", "S13": "present",
        "S12": "RUQ", "E03": "hypotension_under_90",
        "E02": "100_120", "E04": "tachypnea_20_30",
        "L11": "very_high", "L01": "high_10000_20000",
        "L54": "hypoglycemia",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "female"},
    "result": "", "notes": "アセトアミノフェン30g. ALT 6000, INR 5.5, pH 7.19. NAC+CVVH"
})

suite["cases"].append({
    "id": "R299", "source": "Case Rep Gastroenterol 2016", "pmcid": "PMC5139849",
    "vignette": "41F 1ヶ月の嘔気+食欲不振+心窩部痛+4kg体重減少→7日間の黄疸+紅茶色尿+全身掻痒. T 36.3, BP 118/82, HR 79, RR 18. AST 1261, ALT 1031, T-Bil 17.4→29.8, INR 2.12→4.23, ALP 168, IgG 2180, ANA 1:640, ASMA 1:80. Echo: 肝萎縮+腹水. Day15に生体肝移植",
    "final_diagnosis": "急性肝不全(自己免疫性肝炎1型, 劇症化→生体肝移植)",
    "expected_id": "D151", "in_scope": True,
    "evidence": {"E18": "present", "S13": "present", "S07": "severe",
        "S17": "present", "S12": "epigastric",
        "E16": "confused", "E01": "under_37.5",
        "L11": "very_high", "E34": "present",
        "L18": "positive",
        "T01": "over_3w", "T02": "gradual_days"},
    "risk_factors": {"R01": "40_64", "R02": "female"},
    "result": "", "notes": "AIH劇症化. ANA 1:640, IgG 2180. T-Bil 29.8, INR 4.23. 生体肝移植"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R294-R299. Total: {len(suite['cases'])}")
