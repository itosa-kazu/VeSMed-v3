#!/usr/bin/env python3
"""Add 3 GERD cases for D133."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# R244: PMC1949125 - 48M classic GERD chest pain
suite["cases"].append({
    "id": "R244", "source": "Can Fam Physician 2007", "pmcid": "PMC1949125",
    "vignette": "48M BMI 31, 座位仕事, ストレス多. 1年以上の反復性胸骨下胸痛(仕事ストレスで増悪). 典型的胸焼けなし. ED心臓精査: 冠動脈疾患低確率. PPI 2週間でほぼ完全消失",
    "final_diagnosis": "GERD(非心臓性胸痛)",
    "expected_id": "D133", "in_scope": True,
    "evidence": {
        "S21": "constant", "E01": "under_37.5",
        "L53": "normal", "L04": "normal",
        "T01": "over_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "典型的GERD。トロポニン正常+ECG正常+PPI反応が確定の鍵"
})

# R245: PMC10621402 - 42M exercise-induced chest pain + troponin elevation
suite["cases"].append({
    "id": "R245", "source": "Cureus 2023", "pmcid": "PMC10621402",
    "vignette": "42M サイクリスト. 運動中の胸痛+酸逆流3-4回/週. HR 102, BP 144/84, SpO2 96%. トロポニン0.06->1.20->0.00(一過性上昇!), BNP 63(正常). ECG正常, Echo正常(EF 55-60%). 内視鏡: 下部食道炎. PPI+運動制限で改善",
    "final_diagnosis": "GERD(運動誘発性トロポニン上昇合併)",
    "expected_id": "D133", "in_scope": True,
    "evidence": {
        "S21": "constant", "E02": "100_120",
        "E01": "under_37.5", "L53": "mildly_elevated",
        "L51": "normal", "L04": "normal",
        "T01": "over_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "トロポニン一過性上昇(運動誘発)でACS疑い。内視鏡で食道炎確認"
})

# R246: PMC7733775 - 81F hiatal hernia + esophageal ulcers
suite["cases"].append({
    "id": "R246", "source": "Cureus 2020", "pmcid": "PMC7733775",
    "vignette": "81F GERD/DVT/高血圧/高脂血症/CAD/CVA既往. 鋭い中等度胸骨後部痛(呼吸/体動で増悪)+間欠的灼熱感+金属味. T 37.2, HR 95, BP 132/110, RR 18, SpO2 100%. ECG:左軸偏位のみ. トロポニン正常, CBC/CMP正常. CXR:心後方ヘルニア. 内視鏡: Grade IV食道裂孔ヘルニア+多発食道潰瘍+萎縮性胃炎",
    "final_diagnosis": "GERD(Grade IV食道裂孔ヘルニア+食道潰瘍)",
    "expected_id": "D133", "in_scope": True,
    "evidence": {
        "S21": "pleuritic", "E02": "under_100",
        "E01": "under_37.5", "L53": "normal",
        "L01": "normal_4000_10000", "L04": "normal",
        "T01": "over_3w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "65_plus", "R02": "female", "R44": "yes"},
    "result": "", "notes": "心疾患既往あり→ACS除外が重要. トロポニン正常が鍵"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R244-R246. Total: {len(suite['cases'])}")
