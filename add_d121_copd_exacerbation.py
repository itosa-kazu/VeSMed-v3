#!/usr/bin/env python3
"""Add D121 COPD Acute Exacerbation (COPD急性増悪) + R46 COPD既往.

Clinical basis (GOLD 2023):
  COPD既往の患者で急性に呼吸症状が悪化。
  呼吸困難増悪(90%+), 咳嗽増加(70-80%), 膿性痰(50-70%),
  喘鳴(60-80%), 頻呼吸(70-80%), 低酸素(50-70%)
  誘因: 感染(50%), 大気汚染, 服薬不良
  検査: WBC正常~上昇, CRP軽度~中等度, PCT低い(細菌性なら上昇)
  CXR: 通常過膨張(hyperinflation), 肺炎合併で浸潤影
  BNP: 通常正常~軽度(心不全との鑑別に重要)
  References: GOLD 2023 Report (PMC10111975)
              Wedzicha JA, Seemungal T. Lancet 2007;370:786
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# R46 COPD既往
s1["variables"].append({
    "id": "R46", "name": "COPD_history", "name_ja": "COPD既往",
    "category": "risk_factor", "states": ["no", "yes"],
    "note": "COPD既往。COPD急性増悪のリスク"
})

# D121 COPD急性増悪
s1["variables"].append({
    "id": "D121", "name": "COPD_exacerbation",
    "name_ja": "COPD急性増悪",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "COPD既往患者の急性呼吸症状悪化。呼吸困難+咳嗽+膿性痰+喘鳴。"
           "感染が誘因50%。BNP正常~軽度(心不全との鑑別)。CXR過膨張"
})

d_edges = [
    ("S04",  "COPD増悪: 呼吸困難増悪(90%+, 安静時も)"),
    ("S01",  "COPD増悪: 咳嗽増加(70-80%, 湿性が多い)"),
    ("E07",  "COPD増悪: 肺聴診 — 喘鳴/wheezes(60-80%)"),
    ("E04",  "COPD増悪: 頻呼吸(70-80%)"),
    ("E05",  "COPD増悪: 低酸素(50-70%)"),
    ("E01",  "COPD増悪: 発熱(30-50%, 感染性増悪の場合)"),
    ("E02",  "COPD増悪: 頻脈(50-60%)"),
    ("L01",  "COPD増悪: WBC正常~上昇(感染性なら上昇)"),
    ("L02",  "COPD増悪: CRP軽度~中等度(感染で上昇)"),
    ("L03",  "COPD増悪: PCT通常低い(細菌性で上昇)"),
    ("L04",  "COPD増悪: CXR — 通常正常(過膨張), 肺炎合併で浸潤影"),
    ("L51",  "COPD増悪: BNP正常~軽度上昇(心不全との鑑別に重要)"),
    ("S07",  "COPD増悪: 倦怠感(40-60%)"),
    ("S09",  "COPD増悪: 悪寒(感染性で20-30%)"),
    ("T01",  "COPD増悪: 急性(数時間~数日)"),
    ("T02",  "COPD増悪: 急性~亜急性"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D121", "to": to_id, "from_name": "COPD_exacerbation", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

n["S04"]["parent_effects"]["D121"] = {"absent": 0.05, "on_exertion": 0.25, "at_rest": 0.70}
n["S01"]["parent_effects"]["D121"] = {"absent": 0.15, "dry": 0.20, "productive": 0.65}
n["E07"]["parent_effects"]["D121"] = {"clear": 0.10, "crackles": 0.15, "wheezes": 0.75}
n["E04"]["parent_effects"]["D121"] = {"normal_under_20": 0.15, "tachypnea_20_30": 0.55, "severe_over_30": 0.30}
n["E05"]["parent_effects"]["D121"] = {"normal_over_96": 0.25, "mild_hypoxia_93_96": 0.40, "severe_hypoxia_under_93": 0.35}
n["E01"]["parent_effects"]["D121"] = {"under_37.5": 0.45, "37.5_38.0": 0.25, "38.0_39.0": 0.20, "39.0_40.0": 0.08, "over_40.0": 0.02}
n["E02"]["parent_effects"]["D121"] = {"under_100": 0.35, "100_120": 0.45, "over_120": 0.20}
n["L01"]["parent_effects"]["D121"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.45, "high_10000_20000": 0.40, "very_high_over_20000": 0.12}
n["L02"]["parent_effects"]["D121"] = {"normal_under_0.3": 0.15, "mild_0.3_3": 0.30, "moderate_3_10": 0.35, "high_over_10": 0.20}
n["L03"]["parent_effects"]["D121"] = {"not_done": 0.30, "low_under_0.25": 0.30, "gray_0.25_0.5": 0.20, "high_over_0.5": 0.20}
n["L04"]["parent_effects"]["D121"] = {"normal": 0.55, "lobar_infiltrate": 0.15, "bilateral_infiltrate": 0.10, "BHL": 0.02, "pleural_effusion": 0.18}
n["L51"]["parent_effects"]["D121"] = {"not_done": 0.30, "normal": 0.40, "mildly_elevated": 0.25, "very_high": 0.05}
n["S07"]["parent_effects"]["D121"] = {"absent": 0.35, "mild": 0.35, "severe": 0.30}
n["S09"]["parent_effects"]["D121"] = {"absent": 0.70, "present": 0.30}
n["T01"]["parent_effects"]["D121"] = {"under_3d": 0.35, "3d_to_1w": 0.40, "1w_to_3w": 0.20, "over_3w": 0.05}
n["T02"]["parent_effects"]["D121"] = {"sudden_hours": 0.40, "gradual_days": 0.60}

# full_cpt: COPD既往 + 喫煙歴 + 年齢
s3["full_cpts"]["D121"] = {
    "parents": ["R46", "R45"],
    "description": "COPD急性増悪。COPD既往+喫煙がリスク",
    "cpt": {
        "no|never": 0.001, "no|former": 0.002, "no|current": 0.003,
        "yes|never": 0.020, "yes|former": 0.035, "yes|current": 0.050,
    }
}

# R46 root_prior
s3["root_priors"]["R46"] = {
    "description": "COPD既往",
    "distribution": {"no": 0.90, "yes": 0.10}
}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D121 + R46: {len(d_edges)} edges. Total: {s2['total_edges']}")
