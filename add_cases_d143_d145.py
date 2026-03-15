#!/usr/bin/env python3
"""Add 3 aspiration pneumonia (D143) + 3 ureteral stone (D145) cases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# D143 Aspiration Pneumonia x3
suite["cases"].append({
    "id": "R279", "source": "Cureus 2024", "pmcid": "PMC11501497",
    "vignette": "85F アルツハイマー/嚥下障害/寝たきり. 嘔吐後に38.3度発熱+SpO2低下. HR 127, BP 119/69, RR 12, SpO2 93%(O2 6L). WBC 2500(好中球81%), CRP 0.39→上昇中. CT: 両肺に多発浸潤影+GGO. 喀痰: S.dysgalactiae. CTRX+CMZ",
    "final_diagnosis": "誤嚥性肺炎(認知症+嚥下障害)",
    "expected_id": "D143", "in_scope": True,
    "evidence": {"E01": "38.0_39.0", "E02": "over_120", "E05": "mild_hypoxia_93_96",
        "S13": "present", "E16": "confused",
        "L01": "low_under_4000", "L04": "bilateral_infiltrate",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "female"},
    "result": "", "notes": "認知症+嚥下障害→誤嚥. WBC 2500低下(高齢者免疫低下)"
})

suite["cases"].append({
    "id": "R280", "source": "Cureus 2021", "pmcid": "PMC8666202",
    "vignette": "73M 2週前に脳梗塞/DM 15年/高血圧/AF. 食後嘔吐→誤嚥→5日間の持続吃逆(非典型!). T 37.8, HR 92, BP 134/92, RR 22, SpO2 97%. 右下肺crackles. WBC 14060(好中球85%), CRP 25.477. CXR: 両側下葉浸潤影. 血培陰性. AMPC/CVA+MNZ",
    "final_diagnosis": "誤嚥性肺炎(脳梗塞後嚥下障害, 吃逆で発症)",
    "expected_id": "D143", "in_scope": True,
    "evidence": {"E01": "37.5_38.0", "E07": "crackles", "E04": "tachypnea_20_30",
        "L01": "high_10000_20000", "L02": "moderate_3_10",
        "L04": "bilateral_infiltrate", "L09": "negative",
        "T01": "3d_to_1w", "T02": "gradual_days"},
    "risk_factors": {"R01": "65_plus", "R02": "male", "R04": "yes", "R48": "yes"},
    "result": "", "notes": "脳梗塞後嚥下障害→誤嚥. 吃逆が主訴(非典型). WBC 14k, CRP 25"
})

suite["cases"].append({
    "id": "R281", "source": "J Surg Case Rep 2024", "pmcid": "PMC11069041",
    "vignette": "74F アルツハイマー3年/寝たきり1年. 1週間の呼吸困難+発熱+1日の無尿. T 38.5, HR 110, BP 100/50, RR 22, SpO2 83%, GCS 13. WBC 5800, CRP 312, Hb 9.2. ABG: 呼吸性アルカローシス+PaO2 60. CT: 左肺実質性浸潤+食道内液体貯留. Day3敗血症性ショックで死亡",
    "final_diagnosis": "誤嚥性肺炎(認知症+寝たきり, 敗血症性ショックで死亡)",
    "expected_id": "D143", "in_scope": True,
    "evidence": {"E01": "38.0_39.0", "S04": "at_rest", "E02": "100_120",
        "E03": "hypotension_under_90", "E05": "severe_hypoxia_under_93",
        "E04": "tachypnea_20_30", "E16": "confused",
        "L01": "normal_4000_10000", "L02": "high_over_10",
        "L04": "lobar_infiltrate",
        "T01": "3d_to_1w", "T02": "gradual_days"},
    "risk_factors": {"R01": "65_plus", "R02": "female"},
    "result": "", "notes": "重症誤嚥性肺炎. SpO2 83%, CRP 312, BP 100/50. Day3死亡"
})

# D145 Ureteral Stone x3
suite["cases"].append({
    "id": "R282", "source": "J Med Case Rep 2013", "pmcid": "PMC3581005",
    "vignette": "52M 突然の激烈右側腹部痛(10/10, 右下腹部放散)+嘔吐2回. 発熱/排尿痛なし. BP 154/96, HR 79, RR 24, T 36.7. 尿検査: 血尿3+. CT: 右近位尿管に7mm結石+中等度水腎症. 鎮痛→ステント+タムスロシン",
    "final_diagnosis": "尿管結石(右近位尿管, 7mm)",
    "expected_id": "D145", "in_scope": True,
    "evidence": {"S15": "present", "E11": "present", "S13": "present",
        "L05": "pyuria_bacteriuria", "E01": "under_37.5",
        "E04": "tachypnea_20_30",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "典型的腎疝痛. 10/10激痛+血尿3+. 7mm結石"
})

suite["cases"].append({
    "id": "R283", "source": "J Med Case Rep 2009", "pmcid": "PMC2740126",
    "vignette": "32M 建設作業員. 激烈なびまん性腹痛(背部放散, 歩行で増悪)+嘔吐+37.8度微熱. WBC 12000, 尿: 顕微鏡的血尿+膿尿(WBC 10/HPF)+結晶. CT: 左尿管9mm+右尿管8mm結石(両側!). Echo: 両側軽度水腎症. 両側尿管鏡+DJ stent",
    "final_diagnosis": "両側尿管結石(9mm+8mm)",
    "expected_id": "D145", "in_scope": True,
    "evidence": {"S15": "present", "S12": "diffuse", "S13": "present",
        "L05": "pyuria_bacteriuria", "E01": "37.5_38.0",
        "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "両側尿管結石は稀. WBC 12k+微熱(感染合併?)"
})

suite["cases"].append({
    "id": "R284", "source": "Cureus 2023", "pmcid": "PMC10306257",
    "vignette": "19F 既往なし. 急性右下腹部痛(鼠径部放散)+嘔気嘔吐+悪寒. 発熱/血尿/排尿痛なし. BP 106/57, HR 82, RR 18, T 36.8, SpO2 99%. WBC 13200(好中球71%). 尿: RBC 3-5, WBC 30-50, LE弱陽性. CT: 右尿管膀胱接合部に3mm結石+水腎症. タムスロシン+CTRX",
    "final_diagnosis": "尿管結石(右UVJ, 3mm, 腎盂破裂合併)",
    "expected_id": "D145", "in_scope": True,
    "evidence": {"S15": "present", "S13": "present",
        "L05": "pyuria_bacteriuria", "E01": "under_37.5",
        "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "18_39", "R02": "female"},
    "result": "", "notes": "若年女性. 3mm小結石だが腎盂破裂. WBC 13.2k"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R279-R284. Total: {len(suite['cases'])}")
