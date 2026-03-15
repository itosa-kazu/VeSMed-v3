#!/usr/bin/env python3
"""Add 3 rhabdomyolysis (D153) + 3 bowel obstruction (D154) cases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# D153 Rhabdomyolysis x3
suite["cases"].append({
    "id": "R303", "source": "Case Rep Nephrol 2020", "pmcid": "PMC7262479",
    "vignette": "22M 大麻使用+URI症状(鼻漏/咽頭痛/咳嗽). 重度全身筋肉痛+暗褐色尿. T 37.0, HR 109, RR 24, BP 152/87, SpO2 100%. CK>150000, Cr 0.77(正常!), K 4.2, AST 2299, LDH>12000. 尿: 潜血陽性+RBCなし(ミオグロビン尿). NS 250mL/h",
    "final_diagnosis": "横紋筋融解症(薬物/ウイルス性, AKIなし)",
    "expected_id": "D153", "in_scope": True,
    "evidence": {"S06": "present", "S07": "severe", "S01": "dry",
        "S02": "present", "E02": "100_120", "E04": "tachypnea_20_30",
        "E01": "under_37.5", "L17": "very_high", "L16": "elevated",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "CK>150000. 暗色尿(ミオグロビン尿). AKIなし. URI症状あり"
})

suite["cases"].append({
    "id": "R304", "source": "Case Rep Infect Dis 2017", "pmcid": "PMC5507674",
    "vignette": "36M コカイン/アルコール使用. 2日間の下痢+全身脱力(全肢3/5). T 38.9, HR 125, RR 20, BP 138/94, SpO2 98%. CK 701400(!), Cr 4.8(AKI), K 4.75, AST 2847, 尿酸15.2. 尿: 3+血液/3+蛋白. レジオネラ尿中抗原陽性. 挿管+CVVH+透析1ヶ月",
    "final_diagnosis": "横紋筋融解症(レジオネラ+コカイン, AKI合併)",
    "expected_id": "D153", "in_scope": True,
    "evidence": {"S07": "severe", "E01": "38.0_39.0", "E02": "over_120",
        "L17": "very_high", "L02": "high_over_10",
        "L44": "other",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "CK 701400! レジオネラ+コカイン+アルコール多因子. Cr 4.8 AKI"
})

suite["cases"].append({
    "id": "R305", "source": "Cureus 2024", "pmcid": "PMC11070983",
    "vignette": "30M 4日前に氷上転倒(臀部打撲). 全身痛+脱力+変色尿. 無熱, HR 89, RR 18, BP 145/89. CK 4570630(史上最高レベル!), Cr 0.6-0.9(正常!), K 6.2(高K), AST 1474, CK-MB 17.8. 尿: 潜血陽性+RBC/WBCなし. NS+重炭酸+カリウム治療",
    "final_diagnosis": "横紋筋融解症(外傷性, CK 457万, AKIなし)",
    "expected_id": "D153", "in_scope": True,
    "evidence": {"S06": "present", "S07": "severe", "E01": "under_37.5",
        "L17": "very_high", "L44": "hyperkalemia",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "CK 457万(史上最高). K 6.2高K. 外傷→?潜在性ミオパチー. AKIなし"
})

# D154 Bowel Obstruction x3
suite["cases"].append({
    "id": "R306", "source": "BMJ Case Rep 2024", "pmcid": "PMC11469642",
    "vignette": "70代M 3日間の腹痛+嘔吐. 腹部膨満/軟/非圧痛. 左鼠径ヘルニア還納不能+圧痛. HR 113, BP 161/90, 無熱. WBC 19.0k, CRP 68, Cr 116(AKI stage1). CT: 小腸拡張40mm+左鼠径ヘルニア移行部. 緊急鼠径ヘルニア修復",
    "final_diagnosis": "絞扼性鼠径ヘルニア(Richter型)",
    "expected_id": "D154", "in_scope": True,
    "evidence": {"S12": "diffuse", "S13": "present",
        "E02": "100_120", "E01": "under_37.5",
        "L01": "high_10000_20000", "L02": "moderate_3_10",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "65_plus", "R02": "male"},
    "result": "", "notes": "Richterヘルニア→SBO. WBC 19k, CRP 68. 排便は維持(特徴的)"
})

suite["cases"].append({
    "id": "R307", "source": "World J Surg 2016", "pmcid": "PMC4956957",
    "vignette": "75M 手術歴なし. 3日間の疝痛様腹痛+便秘+嘔吐. 腹部軽度膨満/非圧痛. HR 120, BP 111/60, 発熱あり. WBC 6.8k(正常!), 乳酸4.6(!). 腹部X線: 小腸拡張+多発鏡面像. CT: S状結腸間膜内ヘルニア+10cm虚血小腸. 緊急開腹→腸切除+吻合",
    "final_diagnosis": "内ヘルニア(S状結腸間膜内)+絞扼性腸閉塞",
    "expected_id": "D154", "in_scope": True,
    "evidence": {"S12": "diffuse", "S13": "present",
        "E02": "over_120", "E03": "hypotension_under_90",
        "E01": "38.0_39.0",
        "L01": "normal_4000_10000",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "65_plus", "R02": "male"},
    "result": "", "notes": "内ヘルニア→絞扼性SBO. 乳酸4.6(虚血). WBC正常(偽陰性)"
})

suite["cases"].append({
    "id": "R308", "source": "Cureus 2018", "pmcid": "PMC5965135",
    "vignette": "37M 20年以上前に交通事故歴. 16時間の持続性心窩部痛(疝痛様, 増悪時嘔気). 口腔乾燥(脱水). 心窩部圧痛あり, 防御/膨満なし. HR 75, T 36.4, RR 14, SpO2 95%. WBC 12.1k(好中球82%). CT: 胃+小腸拡張+多発鏡面像+閉鎖ループ+周囲遊離液. 開腹: 大網-空腸間癒着バンド解除",
    "final_diagnosis": "癒着性閉鎖ループ腸閉塞",
    "expected_id": "D154", "in_scope": True,
    "evidence": {"S12": "epigastric", "S13": "present",
        "E01": "under_37.5",
        "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "20年前外傷→癒着バンド→閉鎖ループ. WBC 12.1k"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R303-R308. Total: {len(suite['cases'])}")
