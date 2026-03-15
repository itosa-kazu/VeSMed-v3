#!/usr/bin/env python3
"""Add D126 Anaphylaxis (アナフィラキシー).

Clinical basis:
  IgE介在の全身性過敏反応。数分~数時間で発症。
  皮膚(蕁麻疹/血管浮腫 80-90%), 呼吸器(喘鳴/喉頭浮腫 50-70%),
  循環器(低血圧/ショック 30-50%), 消化器(嘔気/腹痛 25-30%)
  誘因: 薬剤(最多), 食物, 虫刺し
  検査: トリプターゼ上昇(確定), WBC/CRP通常正常
  References: Sampson HA et al. JACI 2006 (WAO criteria)
              Simons FER et al. JACI 2011
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

s1["variables"].append({
    "id": "D126", "name": "anaphylaxis",
    "name_ja": "アナフィラキシー",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "全身性過敏反応。蕁麻疹/血管浮腫+喘鳴/喉頭浮腫+低血圧/ショック。"
           "数分で発症。エピネフリンが第一選択。薬剤/食物/虫刺しが誘因"
})

d_edges = [
    ("E12",  "アナフィラキシー: 皮膚(80-90%) — 蕁麻疹/紅斑/血管浮腫"),
    ("S18",  "アナフィラキシー: 皮膚の訴え(80-90%, 広範囲)"),
    ("S04",  "アナフィラキシー: 呼吸困難(50-70%, 喉頭浮腫/気管支攣縮)"),
    ("E07",  "アナフィラキシー: 喘鳴(50-60%, 気管支攣縮)"),
    ("E03",  "アナフィラキシー: 低血圧/ショック(30-50%)"),
    ("E02",  "アナフィラキシー: 頻脈(80%+, 代償性)"),
    ("E05",  "アナフィラキシー: 低酸素(重症で)"),
    ("S13",  "アナフィラキシー: 嘔気嘔吐(25-30%)"),
    ("E01",  "アナフィラキシー: 通常無熱"),
    ("L01",  "アナフィラキシー: WBC通常正常"),
    ("L02",  "アナフィラキシー: CRP通常正常"),
    ("T01",  "アナフィラキシー: 超急性(数分~数時間)"),
    ("T02",  "アナフィラキシー: 突然発症(分単位)"),
    ("E16",  "アナフィラキシー: 意識障害(ショック時20-30%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D126", "to": to_id, "from_name": "anaphylaxis", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

# 皮膚: 蕁麻疹 → maculopapular_rash or diffuse_erythroderma
n["E12"]["parent_effects"]["D126"] = {
    "normal": 0.08, "localized_erythema_warmth_swelling": 0.10,
    "petechiae_purpura": 0.02, "maculopapular_rash": 0.15,
    "vesicular_dermatomal": 0.02, "diffuse_erythroderma": 0.50,
    "purpura": 0.03, "vesicle_bulla": 0.05, "skin_necrosis": 0.05
}
n["S18"]["parent_effects"]["D126"] = {"absent": 0.08, "localized_pain_redness": 0.12, "rash_widespread": 0.80}
n["S04"]["parent_effects"]["D126"] = {"absent": 0.25, "on_exertion": 0.15, "at_rest": 0.60}
n["E07"]["parent_effects"]["D126"] = {"clear": 0.30, "crackles": 0.05, "wheezes": 0.60, "decreased_absent": 0.05}
n["E03"]["parent_effects"]["D126"] = {"normal_over_90": 0.45, "hypotension_under_90": 0.55}
n["E02"]["parent_effects"]["D126"] = {"under_100": 0.08, "100_120": 0.32, "over_120": 0.60}
n["E05"]["parent_effects"]["D126"] = {"normal_over_96": 0.30, "mild_hypoxia_93_96": 0.35, "severe_hypoxia_under_93": 0.35}
n["S13"]["parent_effects"]["D126"] = {"absent": 0.65, "present": 0.35}
n["E01"]["parent_effects"]["D126"] = {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D126"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.75, "high_10000_20000": 0.18, "very_high_over_20000": 0.04}
n["L02"]["parent_effects"]["D126"] = {"normal_under_0.3": 0.60, "mild_0.3_3": 0.25, "moderate_3_10": 0.12, "high_over_10": 0.03}
n["T01"]["parent_effects"]["D126"] = {"under_3d": 0.95, "3d_to_1w": 0.04, "1w_to_3w": 0.01, "over_3w": 0.00}
n["T02"]["parent_effects"]["D126"] = {"sudden_hours": 0.95, "gradual_days": 0.05}
n["E16"]["parent_effects"]["D126"] = {"normal": 0.65, "confused": 0.20, "obtunded": 0.15}

s3["full_cpts"]["D126"] = {
    "parents": ["R08"],
    "description": "アナフィラキシー。薬剤が最多誘因",
    "cpt": {"no": 0.001, "yes": 0.005}
}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D126: {len(d_edges)} edges. Total: {s2['total_edges']}")
