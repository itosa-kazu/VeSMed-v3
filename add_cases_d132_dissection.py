#!/usr/bin/env python3
"""Add 3 aortic dissection cases for D132."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

suite["cases"].append({
    "id": "R234", "source": "Cureus 2022", "pmcid": "PMC9757650",
    "vignette": "36M BMI 34, 既往なし. 5日間の胸部圧迫感(労作時悪化)+呼吸困難. BP 185/106, HR 115, RR 16, SpO2 97%. 拡張期雑音(左下胸骨). トロポニン3.30, D-dimer 753, CRP 82.5, BNP 474, WBC 10.9k. CTA: 上行大動脈解離(冠動脈巻込み). 緊急手術中に死亡",
    "final_diagnosis": "Stanford Type A大動脈解離(冠動脈巻込み)",
    "expected_id": "D132", "in_scope": True,
    "evidence": {
        "S21": "constant", "S04": "on_exertion", "E02": "100_120",
        "E15": "new", "L17": "very_high", "L51": "very_high",
        "L01": "high_10000_20000", "L02": "high_over_10",
        "L16": "elevated", "E01": "under_37.5",
        "T01": "3d_to_1w", "T02": "gradual_days"
    },
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "ACSに見える大動脈解離. トロポニン3.30(冠動脈巻込み). 死亡転帰"
})

suite["cases"].append({
    "id": "R235", "source": "Korean Circ J 2013", "pmcid": "PMC3856285",
    "vignette": "77F 高血圧5年. 突然の胸骨下圧迫痛(NRS 8-10)+大量発汗+呼吸困難+失禁+切迫感. NTG3錠で軽減. BP 108/75, HR 82, SpO2 99%. トロポニン0.03(正常), D-dimer 13.60(著高), CK正常. CTA: 上行~腎動脈手前のType A解離, 上行大動脈50mm",
    "final_diagnosis": "Stanford Type A大動脈解離",
    "expected_id": "D132", "in_scope": True,
    "evidence": {
        "S21": "constant", "S04": "on_exertion",
        "E02": "under_100", "E01": "under_37.5",
        "L01": "normal_4000_10000", "L02": "mild_0.3_3",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "65_plus", "R02": "female"},
    "result": "", "notes": "NTGで軽減→ACS疑い. D-dimer 13.60が鍵. トロポニン正常が解離を示唆"
})

suite["cases"].append({
    "id": "R236", "source": "Cureus 2024", "pmcid": "PMC11299370",
    "vignette": "54M 高血圧/喫煙/慢性B型解離既往. 突然の引き裂くような左背部痛+軽度胸部圧迫感. BP 156/98, HR 83, SpO2 99%. WBC 10.62k, 乳酸11.9(!), トロポニン正常. CTA: Type B解離+偽腔含有破裂+大動脈周囲血腫. CICU到着20分後に死亡",
    "final_diagnosis": "Stanford Type B大動脈解離(偽腔破裂)",
    "expected_id": "D132", "in_scope": True,
    "evidence": {
        "S21": "constant", "S22": "present",
        "E02": "under_100", "E01": "under_37.5",
        "L01": "high_10000_20000",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "40_64", "R02": "male", "R45": "current"},
    "result": "", "notes": "背部痛が主体(Type B). 乳酸11.9は臓器虚血. 死亡転帰"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)

print(f"Added R234-R236. Total: {len(suite['cases'])}")
