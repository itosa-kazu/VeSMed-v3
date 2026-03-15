#!/usr/bin/env python3
"""Add 3 Takotsubo cases for D150."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

suite["cases"].append({
    "id": "R300", "source": "Case Rep Med 2009", "pmcid": "PMC2672240",
    "vignette": "67F 前日に姉がMIで死亡(精神的ストレス). 胸骨下痛(5/10, 左腕放散)+呼吸困難. HR 86, BP 140/86, RR 14, SpO2 100%(O2 2L), T 37.1. トロポニンI 2.5(軽度上昇), CK-MB 11, WBC 11.2k. ECG: V3 ST上昇+TWI. Echo: 心尖部無動→回復EF 78%. 冠動脈造影: 正常",
    "final_diagnosis": "たこつぼ心筋症(精神的ストレス誘発)",
    "expected_id": "D150", "in_scope": True,
    "evidence": {"S21": "pressure", "S50": "none", "S51": "left_arm_jaw",
        "S04": "on_exertion", "E02": "under_100", "E01": "under_37.5",
        "L53": "mildly_elevated", "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "female"},
    "result": "", "notes": "ACSを完全に模倣. トロポニン2.5は軽度(ACSなら数十~数百). 冠動脈正常が確定の鍵"
})

suite["cases"].append({
    "id": "R301", "source": "Case Rep Med 2009", "pmcid": "PMC2672240",
    "vignette": "86F Asian. 2週前に息子事故死(精神的ストレス). 胸骨下圧迫痛(9/10, 非放散). HR 71, BP 185/88, RR 20, SpO2 98%, T 35.7. トロポニンI 3.23, WBC 12k. ECG: V2-V3 ST上昇. Echo: EF 30-34%, 心尖部バルーニング. 冠動脈造影: 正常",
    "final_diagnosis": "たこつぼ心筋症(EF 30%, 重症)",
    "expected_id": "D150", "in_scope": True,
    "evidence": {"S21": "pressure", "S50": "none", "S51": "none",
        "E38": "crisis_over_180", "E02": "under_100", "E01": "under_37.5",
        "L53": "mildly_elevated", "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "65_plus", "R02": "female"},
    "result": "", "notes": "9/10胸痛+EF 30%だがACSではなくたこつぼ. BP 185(高血圧合併). トロポニン3.23"
})

suite["cases"].append({
    "id": "R302", "source": "Cureus 2023", "pmcid": "PMC9828072",
    "vignette": "52F 閉経後. 夫がCOVID-19で死亡(精神的ストレス). 左胸痛(鈍い, 非放散, 安静で改善)+呼吸困難. HR 76, BP 110/70, SpO2 97%. トロポニンT 35ng/L(軽度上昇), NT-proBNP 1346. ECG: I/aVL/V2-V5 TWI. Echo: EF 38%, 心尖部バルーニング. 冠動脈: 非閉塞性. MRI: LGEなし(梗塞否定)",
    "final_diagnosis": "たこつぼ心筋症(broken heart syndrome)",
    "expected_id": "D150", "in_scope": True,
    "evidence": {"S21": "pressure", "S50": "none", "S51": "none",
        "S04": "on_exertion", "E02": "under_100", "E01": "under_37.5",
        "L53": "mildly_elevated", "L51": "very_high",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "female"},
    "result": "", "notes": "Broken heart syndrome. NT-proBNP 1346. MRIでLGEなし→梗塞除外"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R300-R302. Total: {len(suite['cases'])}")
