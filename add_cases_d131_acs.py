#!/usr/bin/env python3
"""Add 3 ACS cases for D131."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

suite["cases"].append({
    "id": "R237", "source": "Case Rep Cardiol 2020", "pmcid": "PMC7711079",
    "vignette": "44M 40pack-year喫煙. 1時間の胸骨後部圧迫感(頸部/両肩放散)+大量発汗+嘔気+重度呼吸困難. HR 125, BP 85/62(心原性ショック, ドパミン下), SpO2低下. トロポニン6.31, CK-MB 694, BNP 5518, WBC 22.6k. ECG: V2-V4 ST上昇+VT. Echo: EF 20%. 冠動脈造影: 左主幹100%閉塞",
    "final_diagnosis": "前壁STEMI(左主幹閉塞, 心原性ショック)",
    "expected_id": "D131", "in_scope": True,
    "evidence": {
        "S21": "constant", "S04": "at_rest", "S13": "present",
        "E02": "over_120", "E03": "hypotension_under_90",
        "E05": "severe_hypoxia_under_93", "E07": "crackles",
        "L17": "very_high", "L51": "very_high",
        "L01": "very_high_over_20000", "E01": "under_37.5",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "40_64", "R02": "male", "R45": "current"},
    "result": "", "notes": "左主幹100%閉塞STEMI. EF 20%, ショック. トロポニン6.31, BNP 5518"
})

suite["cases"].append({
    "id": "R238", "source": "Cureus 2024", "pmcid": "PMC11135076",
    "vignette": "43M 既往なし/非喫煙. 4時間の突然の圧砕胸痛(顎/右腕放散). HR 87, BP 138/89, RR 18, T 37.2, SpO2 97%. トロポニン5.6. ECG: II/III/aVF ST上昇+aVL reciprocal. Echo: EF正常. 冠動脈: RCA 100%閉塞+LAD近位閉塞",
    "final_diagnosis": "下壁STEMI(RCA+LAD多枝病変)",
    "expected_id": "D131", "in_scope": True,
    "evidence": {
        "S21": "constant", "E02": "under_100",
        "E05": "normal_over_96", "E01": "under_37.5",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "若年でリスク因子なしのSTEMI. 顎/右腕放散が特徴. トロポニン5.6"
})

suite["cases"].append({
    "id": "R239", "source": "Cureus 2024", "pmcid": "PMC11604203",
    "vignette": "58M 高血圧/脂質異常/喫煙歴. 6時間の胸痛. トロポニン7.17, CK-MB 59, NT-proBNP 617.3. ECG: ST変化なし(NSTEMI). Echo: EF 63.1%正常. 冠動脈: mid-LAD 70-80%狭窄. PCI施行",
    "final_diagnosis": "NSTEMI(mid-LAD狭窄)",
    "expected_id": "D131", "in_scope": True,
    "evidence": {
        "S21": "constant", "L17": "elevated", "L51": "very_high",
        "E01": "under_37.5",
        "T01": "under_3d", "T02": "sudden_hours"
    },
    "risk_factors": {"R01": "40_64", "R02": "male", "R45": "former"},
    "result": "", "notes": "NSTEMI. ST変化なし. トロポニン7.17, NT-proBNP 617. バイタル未詳"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)

print(f"Added R237-R239. Total: {len(suite['cases'])}")
