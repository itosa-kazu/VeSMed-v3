#!/usr/bin/env python3
"""Add 3 GBS cases for D144."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

# R276: PMC6334053 - 41M GBS with respiratory failure
suite["cases"].append({
    "id": "R276", "source": "BMC Neurol 2019", "pmcid": "PMC6334053",
    "vignette": "41M 3日前にURI+発熱. 3日間の進行性下肢筋力低下→対麻痺(0/5). 深部反射消失. T6以下感覚低下+急性尿閉. BP 130/78, HR 92, T 37.0, SpO2 96%. 血液検査正常. CSF: 蛋白細胞解離(+). NCS: F波/H反射消失. 血漿交換5回→挿管→6週で完全回復",
    "final_diagnosis": "ギラン・バレー症候群(AIDP, 呼吸不全合併)",
    "expected_id": "D144", "in_scope": True,
    "evidence": {"S52": "bilateral", "S06": "present",
        "E01": "under_37.5", "L01": "normal_4000_10000",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "18_39", "R02": "male"},
    "result": "", "notes": "典型AIDP. 上行性麻痺+深部反射消失. 先行URI. 呼吸不全→挿管"
})

# R277: PMC8089421 - 72M GBS post-COVID
suite["cases"].append({
    "id": "R277", "source": "Med Princ Pract 2021", "pmcid": "PMC8089421",
    "vignette": "72M 高血圧/DM(コントロール良好). 3週前にCOVID-19(咳嗽+発熱+呼吸困難). 3週間の進行性上行性下肢筋力低下→上肢にも波及. 深部反射全消失. 手袋靴下型感覚鈍麻+感覚性失調. T 37.0, BP 130/85, HR 70, RR 15, SpO2 99%. WBC 8.0k, ESR 11, CRP 4. CSF: 蛋白543(↑), 細胞0(ACD+). NCS: AIDP. IVIG 5日→1ヶ月で完全回復",
    "final_diagnosis": "ギラン・バレー症候群(COVID-19後, AIDP)",
    "expected_id": "D144", "in_scope": True,
    "evidence": {"S52": "bilateral", "E01": "under_37.5",
        "L01": "normal_4000_10000", "L02": "normal_under_0.3",
        "L28": "normal",
        "T01": "over_3w", "T02": "gradual_days"},
    "risk_factors": {"R01": "65_plus", "R02": "male", "R04": "yes"},
    "result": "", "notes": "COVID後GBS. 3週間かけて進行. CSF ACD(蛋白543, 細胞0). AIDP"
})

# R278: PMC5775794 - 81M GBS post-Campylobacter, axonal
suite["cases"].append({
    "id": "R278", "source": "BMC Infect Dis 2018", "pmcid": "PMC5775794",
    "vignette": "81M 自立. 2週前に下痢+嘔吐(Campylobacter jejuni). 初日: 38.4度+混迷+頭痛→3日目: 対称性四肢弛緩性麻痺. 深部反射全消失. 自律神経障害(BP 80-90/40-50の治療抵抗性低血圧). WBC 19.4k, CRP 41. CSF: 蛋白1.0g/L(↑), WBC 72(異型). 抗GM1抗体陽性. NCS: 重症軸索型. IVIG x3サイクル→3ヶ月で部分回復",
    "final_diagnosis": "ギラン・バレー症候群(Campylobacter後, 軸索型, 重症)",
    "expected_id": "D144", "in_scope": True,
    "evidence": {"S52": "bilateral", "E16": "confused",
        "E03": "hypotension_under_90", "S05": "mild",
        "E01": "38.0_39.0",
        "L01": "high_10000_20000", "L02": "moderate_3_10",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "65_plus", "R02": "male"},
    "result": "", "notes": "Campylobacter→重症軸索型GBS. 自律神経障害(低血圧). WBC 19.4k, CRP 41(炎症反応)"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R276-R278. Total: {len(suite['cases'])}")
