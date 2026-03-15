#!/usr/bin/env python3
"""Add 3 mesenteric ischemia cases for D137."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# R258: PMC12296313 - 60M SMA thrombosis (atherosclerotic)
suite["cases"].append({
    "id": "R258", "source": "Cureus 2025", "pmcid": "PMC12296313",
    "vignette": "60M 広範動脈硬化. 4日間の突然右腹痛(背部放散)+嘔吐+便秘→腹部膨満+腸蠕動消失. HR 120, BP 140/90, 微熱. WBC 18.2k, CRP 88, 乳酸5.2, D-dimer 3.1, Cr 1.5. CTA: SMA近位部血栓+小腸壁菲薄化+腸管気腫. 緊急開腹: 243cm腸切除",
    "final_diagnosis": "急性腸間膜虚血(SMA血栓症, 広範腸管壊死)",
    "expected_id": "D137", "in_scope": True,
    "evidence": {
        "S12": "diffuse", "S13": "present",
        "E09": "peritoneal_signs", "E02": "over_120",
        "E01": "37.5_38.0",
        "L01": "high_10000_20000", "L02": "high_over_10",
        "L52": "very_high", "L16": "elevated",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "SMA血栓. 乳酸5.2+腸管気腫→壊死. 243cm切除"
})

# R259: PMC12727365 - 70F SMA embolism (AF) + renal infarction
suite["cases"].append({
    "id": "R259", "source": "Medicine 2025", "pmcid": "PMC12727365",
    "vignette": "70F AF/高血圧/脂質異常. 3時間の持続性下腹部鈍痛(5/10)+軽度嘔気. 反跳痛なし/筋性防御なし(pain out of proportion!). HR 74, BP 131/81, T 36.0, RR 18, SpO2 99%. WBC 7.93k, CRP 1.35(正常!), D-dimer 6.08(著高!). CTA: SMA充満欠損+右腎梗塞. 保存的治療(エドキサバン)で改善",
    "final_diagnosis": "SMA塞栓症+右腎梗塞(心房細動由来)",
    "expected_id": "D137", "in_scope": True,
    "evidence": {
        "S12": "diffuse", "S13": "present",
        "E09": "soft_nontender",
        "E02": "under_100", "E01": "under_37.5",
        "L01": "normal_4000_10000", "L02": "normal_under_0.3",
        "L52": "very_high",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "65_plus", "R02": "female", "R48": "yes"},
    "result": "", "notes": "典型的pain out of proportion. WBC/CRP正常だがD-dimer 6.08著高. AF既往が鍵"
})

# R260: PMC9885642 - 70F SMA embolism post-RFA (AF)
suite["cases"].append({
    "id": "R260", "source": "BMC Cardiovasc Disord 2023", "pmcid": "PMC9885642",
    "vignette": "70F 発作性AF 3年/冠動脈疾患/EF30%/DM/高血圧. RFA後にびまん性腹痛+膨満+頻回嘔吐→72hで血便. 腹部軟(初期)+上腹部軽度圧痛. WBC 20.83k→14.64k, CRP 442, PCT 4.62, D-dimer 2882, 乳酸2.7. CT: 骨盤小腸壊死. 開腹: 回腸38cm切除",
    "final_diagnosis": "SMA塞栓症(RFA後, 回腸壊死+穿孔)",
    "expected_id": "D137", "in_scope": True,
    "evidence": {
        "S12": "diffuse", "S13": "present",
        "E09": "soft_nontender",
        "E01": "under_37.5",
        "L01": "very_high_over_20000", "L02": "high_over_10",
        "L03": "high_over_0.5", "L52": "very_high",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "65_plus", "R02": "female", "R48": "yes", "R04": "yes", "R44": "yes"},
    "result": "", "notes": "RFA後SMA塞栓. CRP 442, PCT 4.62. 初期は腹部軟(pain out of proportion)"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R258-R260. Total: {len(suite['cases'])}")
