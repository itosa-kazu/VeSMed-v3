#!/usr/bin/env python3
"""Add 3 Boerhaave cases for D148."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

suite["cases"].append({
    "id": "R285", "source": "Cureus 2024", "pmcid": "PMC11311301",
    "vignette": "46M 健康. 激しい嘔吐数時間後に突然の胸痛(頸部/心窩部放散)+呼吸困難+発汗+チアノーゼ. HR 80, BP 120/70, SpO2 98%, 無熱. WBC 15090, CK 6480. CT: 縦隔気腫+右微量気胸+食道下部瘻孔+造影剤縦隔内漏出. 緊急手術→12日退院",
    "final_diagnosis": "Boerhaave症候群(食道破裂)",
    "expected_id": "D148", "in_scope": True,
    "evidence": {"S21": "sharp", "S50": "none", "S51": "back",
        "S13": "present", "S04": "at_rest",
        "E01": "under_37.5", "L01": "high_10000_20000",
        "L04": "pneumothorax",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "典型Boerhaave. 嘔吐→胸痛→縦隔気腫. CK 6480(嘔吐+縦隔炎)"
})

suite["cases"].append({
    "id": "R286", "source": "Am J Case Rep 2014", "pmcid": "PMC4010036",
    "vignette": "41M 3日間の進行性呼吸困難+胸骨後部痛(背部放散)+反復嘔吐+38.5度発熱. HR 150, RR 40. WBC 18500, CRP 303, 乳酸7.4. CXR: 縦隔透亮線+右心縁silhouette sign. CT: 縦隔気腫+食道遠位裂傷+両側胸水. 保存→ステント→VATS. ICU 33日",
    "final_diagnosis": "Boerhaave症候群(遅延診断, 敗血症合併)",
    "expected_id": "D148", "in_scope": True,
    "evidence": {"S21": "sharp", "S50": "breathing", "S51": "back",
        "S13": "present", "S04": "at_rest",
        "E01": "38.0_39.0", "E02": "over_120", "E04": "severe_over_30",
        "L01": "high_10000_20000", "L02": "high_over_10",
        "L04": "pleural_effusion",
        "T01": "under_3d", "T02": "gradual_days"},
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "3日遅延. CRP 303, 乳酸7.4. 敗血症. ICU 33日"
})

suite["cases"].append({
    "id": "R287", "source": "Cureus 2025", "pmcid": "PMC12628348",
    "vignette": "50M 既往なし. 豚肉摂取後に10-15分の激しい嘔吐→直後に急性胸痛(左側放散)+進行性呼吸困難. HR 95, BP 159/76, RR 22, SpO2 97%. 上胸部~頸部に皮下気腫触知. 検査全て正常(トロポニン/CBC/肝腎). CT: 縦隔気腫+頸部気腫+食道破裂+食物残渣. 保存的治療→20日退院",
    "final_diagnosis": "Boerhaave症候群(保存的治療)",
    "expected_id": "D148", "in_scope": True,
    "evidence": {"S21": "sharp", "S50": "none", "S51": "none",
        "S13": "present", "S04": "on_exertion",
        "E01": "under_37.5", "L53": "normal",
        "L01": "normal_4000_10000", "L02": "normal_under_0.3",
        "T01": "under_3d", "T02": "sudden_hours"},
    "risk_factors": {"R01": "40_64", "R02": "male"},
    "result": "", "notes": "皮下気腫が鍵所見. 検査全て正常(早期). 保存的治療で回復"
})

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added R285-R287. Total: {len(suite['cases'])}")
