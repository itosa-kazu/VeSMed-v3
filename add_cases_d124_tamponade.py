#!/usr/bin/env python3
"""Add 3 tamponade cases for D124."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# R247: PMC7940096 - 69F purulent pericarditis tamponade
suite["cases"].append({
    "id": "R247", "source": "Cureus 2021", "pmcid": "PMC7940096",
    "vignette": "69F DM/高血圧/喘息. 4日間の胸膜性胸痛(背部放散)+呼吸困難. T 37.2, HR 54→100, BP 98/70→79/58, RR 24. JVD+, 心音減弱, 両側下肺粗大音. WBC 20.4k, CRP 13.83, PCT 5.14, トロポニン0.088, BNP 1833. Echo: 大量心嚢液+RV圧排2cm. 心嚢穿刺360mL血性",
    "final_diagnosis": "化膿性心膜炎+心タンポナーデ(S.anginosus)",
    "expected_id": "D124", "in_scope": True,
    "evidence": {
        "S21": "sharp", "S50": "breathing", "S04": "at_rest",
        "E03": "hypotension_under_90", "E37": "present", "E15": "new",
        "E04": "tachypnea_20_30", "E01": "under_37.5",
        "L01": "very_high_over_20000", "L02": "high_over_10",
        "L03": "high_over_0.5", "L53": "mildly_elevated", "L51": "very_high",
        "T01": "under_3d", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "65_plus", "R02": "female", "R04": "yes"},
    "result": "", "notes": "化膿性心膜炎. Beck triad(低血圧+JVD+心音減弱)全揃い. BNP 1833"
})

# R248: PMC11324266 - 72M malignant tamponade (lung adenoCA)
suite["cases"].append({
    "id": "R248", "source": "Cureus 2024", "pmcid": "PMC11324266",
    "vignette": "72M 25pack-year喫煙. 1ヶ月の咳嗽+進行性呼吸困難+9kg体重減少. T 36.5, HR 110, BP 126/72. WBC 9.4k→12.0k. Echo: 大量心嚢液+RA虚脱, EF 56%. CXR: 右下葉腫瘤. 心嚢穿刺1920mL血性, 細胞診: 肺腺癌転移. 脳MRI: 小脳転移",
    "final_diagnosis": "悪性心タンポナーデ(肺腺癌転移)",
    "expected_id": "D124", "in_scope": True,
    "evidence": {
        "S04": "on_exertion", "S01": "productive", "S17": "present",
        "E02": "100_120", "E01": "under_37.5",
        "L01": "normal_4000_10000",
        "L04": "pleural_effusion",
        "T01": "over_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "65_plus", "R02": "male", "R45": "former"},
    "result": "", "notes": "悪性タンポナーデ. 1920mL血性心嚢液. 体重減少9kgが癌示唆"
})

# R249: PMC10019786 - 58F Q fever tamponade
suite["cases"].append({
    "id": "R249", "source": "Cureus 2023", "pmcid": "PMC10019786",
    "vignette": "58F 5日間の微熱→39度高熱+倦怠感+筋肉痛+咳嗽(乾性→湿性)+びまん性胸痛+呼吸困難. T 38.5, HR 115, BP 140/80, RR 28, SpO2 96%→91%. WBC 12.3k, CRP 302, ESR 80, フェリチン706, BNP 271, Hb 7.5. 左下肺浸潤+胸水. Echo: 大量心嚢液(>3cm)+IVC拡張+呼吸変動なし. Coxiella IgG陽性(慢性Q熱)",
    "final_diagnosis": "Q熱心膜炎+心タンポナーデ",
    "expected_id": "D124", "in_scope": True,
    "evidence": {
        "S04": "at_rest", "S21": "sharp", "S50": "breathing",
        "S06": "present", "S01": "productive", "S07": "severe",
        "E02": "100_120", "E04": "tachypnea_20_30",
        "E05": "mild_hypoxia_93_96", "E01": "38.0_39.0",
        "L01": "high_10000_20000", "L02": "high_over_10",
        "L28": "elevated", "L15": "very_high_over_1000",
        "L51": "mildly_elevated", "L04": "pleural_effusion",
        "T01": "3d_to_1w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "40_64", "R02": "female"},
    "result": "", "notes": "Q熱→心膜炎→タンポナーデ. CRP 302, フェリチン706, Hb 7.5貧血"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R247-R249. Total: {len(suite['cases'])}")
