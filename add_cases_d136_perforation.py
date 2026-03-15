#!/usr/bin/env python3
"""Add 3 peptic ulcer perforation cases for D136."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# R255: PMC11026102 - 54F NSAIDs duodenal perforation (conservative)
suite["cases"].append({
    "id": "R255", "source": "Cureus 2024", "pmcid": "PMC11026102",
    "vignette": "54F 高血圧, 長期NSAIDs使用(関節痛). 2週間の上腹部痛+3日間の頻回嘔吐→12時間で右上腹部に局在化. HR 96, BP 110/70, RR 24, SpO2 94%, 無熱. WBC 24.34k, CRP 45.5mg/dL, 乳酸1.8, Cr 227(AKI). CXR: 横隔膜下遊離ガス. CT: 気腹+D1浮腫. 保存的治療で改善",
    "final_diagnosis": "十二指腸潰瘍穿孔(NSAIDs, 保存的治療)",
    "expected_id": "D136", "in_scope": True,
    "evidence": {
        "S12": "epigastric", "S13": "present",
        "E09": "peritoneal_signs", "E02": "under_100",
        "E01": "under_37.5", "E05": "mild_hypoxia_93_96",
        "L01": "very_high_over_20000", "L02": "high_over_10",
        "L04": "pneumothorax",
        "T01": "1w_to_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "40_64", "R02": "female"},
    "result": "", "notes": "NSAIDs→D1穿孔. CXR free air→L04=pneumothorax mapping. WBC 24k, CRP著高"
})

# R256: PMC6369133 - 20M H.pylori duodenal perforation (shock)
suite["cases"].append({
    "id": "R256", "source": "BMC Surg 2019", "pmcid": "PMC6369133",
    "vignette": "20M 消化性潰瘍既往. 1日前に突然の激烈腹痛. HR 140, BP 80/50(ショック), RR 36, T 36.5. Hb 10.3, 好中球95.8%, Cr 254(AKI). ABG: pH 7.354, BE -9.6, SpO2 91.3%. CXR: 横隔膜下遊離ガス. 術中: D1に1cm穿孔+2L膿性胆汁性腹水. H.pylori治療",
    "final_diagnosis": "十二指腸潰瘍穿孔(H.pylori, 腹腔内敗血症)",
    "expected_id": "D136", "in_scope": True,
    "evidence": {
        "S12": "diffuse", "E09": "peritoneal_signs",
        "E02": "over_120", "E03": "hypotension_under_90",
        "E01": "under_37.5", "E05": "mild_hypoxia_93_96",
        "L04": "pneumothorax",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "20歳ショック. HR 140, BP 80/50. pH 7.35. 2L膿性腹水"
})

# R257: PMC10841121 - 75M gastric perforation (smoking/alcohol)
suite["cases"].append({
    "id": "R257", "source": "Int J Surg Case Rep 2023", "pmcid": "PMC10841121",
    "vignette": "75M COPD 15年, 30年以上喫煙(20本/日), 20年以上飲酒. 飲酒後に突然の激烈心窩部痛+胸部圧迫+呼吸困難. 苦悶顔貌, 腹部膨満, 全腹圧痛+反跳痛+板状硬, 胸壁皮下気腫. SpO2 95%(高流量O2). WBC 13.69k, CRP 325.9, PCT 33.63, 好中球97.4%. ABG: pH 7.30, 乳酸3.8. CT: 気腹+縦隔気腫+皮下気腫. 胃前庭穿孔0.5cm",
    "final_diagnosis": "胃潰瘍穿孔(縦隔気腫合併)",
    "expected_id": "D136", "in_scope": True,
    "evidence": {
        "S12": "epigastric", "S04": "at_rest",
        "E09": "peritoneal_signs", "E01": "under_37.5",
        "L01": "high_10000_20000", "L02": "high_over_10",
        "L03": "high_over_0.5",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "65_plus", "R02": "male", "R45": "current", "R46": "yes"},
    "result": "", "notes": "飲酒後の胃穿孔. 板状硬+PCT 33.63. 縦隔気腫合併"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R255-R257. Total: {len(suite['cases'])}")
