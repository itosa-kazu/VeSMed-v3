#!/usr/bin/env python3
"""Add D122 Asthma Exacerbation (喘息発作/急性増悪).

Clinical basis:
  喘息既往の患者で急性呼吸困難+喘鳴+咳嗽。
  呼吸困難(95%+), 喘鳴(90%+), 咳嗽(80%+), 胸部絞扼感
  頻呼吸(RR>20), 頻脈(HR>100), 低酸素(重症)
  WBC正常~軽度上昇, CRP通常正常~軽度, CXR通常正常
  BNP正常(心不全との鑑別)
  COPDとの鑑別: 若年, 喘息既往, アレルギー歴, 可逆性
  References: GINA 2023, EPR-3 Guidelines
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# R47: 喘息既往
s1["variables"].append({
    "id": "R47", "name": "asthma_history", "name_ja": "喘息既往",
    "category": "risk_factor", "states": ["no", "yes"],
    "note": "喘息既往。喘息発作のリスク"
})

s1["variables"].append({
    "id": "D122", "name": "asthma_exacerbation",
    "name_ja": "喘息発作（急性増悪）",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "喘息既往患者の急性呼吸困難+喘鳴+咳嗽。CXR通常正常。BNP正常。"
           "COPDとの鑑別: 若年、可逆性、アレルギー歴"
})

d_edges = [
    ("S04",  "喘息発作: 呼吸困難(95%+, 発作的)"),
    ("E07",  "喘息発作: 喘鳴/wheezes(90%+, 呼気優位)"),
    ("S01",  "喘息発作: 咳嗽(80%+, 乾性が多い)"),
    ("E04",  "喘息発作: 頻呼吸(70-80%)"),
    ("E02",  "喘息発作: 頻脈(50-60%)"),
    ("E05",  "喘息発作: 低酸素(中等度~重症で)"),
    ("E01",  "喘息発作: 通常無熱(感染誘因なら微熱10-20%)"),
    ("L01",  "喘息発作: WBC正常~軽度上昇(ステロイド/ストレスで)"),
    ("L02",  "喘息発作: CRP通常正常~軽度"),
    ("L04",  "喘息発作: CXR通常正常(過膨張のみ)"),
    ("L51",  "喘息発作: BNP正常(心不全との鑑別に重要)"),
    ("S07",  "喘息発作: 倦怠感(30-40%)"),
    ("T01",  "喘息発作: 急性(数時間~数日)"),
    ("T02",  "喘息発作: 急性発症(時間単位が多い)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D122", "to": to_id, "from_name": "asthma_exacerbation", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

n["S04"]["parent_effects"]["D122"] = {"absent": 0.03, "on_exertion": 0.22, "at_rest": 0.75}
n["E07"]["parent_effects"]["D122"] = {"clear": 0.05, "crackles": 0.05, "wheezes": 0.90}
n["S01"]["parent_effects"]["D122"] = {"absent": 0.15, "dry": 0.60, "productive": 0.25}
n["E04"]["parent_effects"]["D122"] = {"normal_under_20": 0.15, "tachypnea_20_30": 0.55, "severe_over_30": 0.30}
n["E02"]["parent_effects"]["D122"] = {"under_100": 0.30, "100_120": 0.45, "over_120": 0.25}
n["E05"]["parent_effects"]["D122"] = {"normal_over_96": 0.35, "mild_hypoxia_93_96": 0.40, "severe_hypoxia_under_93": 0.25}
n["E01"]["parent_effects"]["D122"] = {"under_37.5": 0.75, "37.5_38.0": 0.15, "38.0_39.0": 0.08, "39.0_40.0": 0.02, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D122"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.50, "high_10000_20000": 0.37, "very_high_over_20000": 0.10}
n["L02"]["parent_effects"]["D122"] = {"normal_under_0.3": 0.40, "mild_0.3_3": 0.35, "moderate_3_10": 0.20, "high_over_10": 0.05}
n["L04"]["parent_effects"]["D122"] = {"normal": 0.70, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.05, "BHL": 0.02, "pleural_effusion": 0.18}
n["L51"]["parent_effects"]["D122"] = {"not_done": 0.40, "normal": 0.50, "mildly_elevated": 0.08, "very_high": 0.02}
n["S07"]["parent_effects"]["D122"] = {"absent": 0.50, "mild": 0.30, "severe": 0.20}
n["T01"]["parent_effects"]["D122"] = {"under_3d": 0.50, "3d_to_1w": 0.35, "1w_to_3w": 0.12, "over_3w": 0.03}
n["T02"]["parent_effects"]["D122"] = {"sudden_hours": 0.60, "gradual_days": 0.40}

# full_cpt
s3["full_cpts"]["D122"] = {
    "parents": ["R47"],
    "description": "喘息発作。喘息既往がリスク",
    "cpt": {"no": 0.002, "yes": 0.040}
}
s3["root_priors"]["R47"] = {"description": "喘息既往", "distribution": {"no": 0.90, "yes": 0.10}}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D122 + R47: {len(d_edges)} edges. Total: {s2['total_edges']}")
