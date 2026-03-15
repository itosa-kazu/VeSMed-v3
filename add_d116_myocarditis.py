#!/usr/bin/env python3
"""Add D116 Acute Myocarditis (急性心筋炎).

Clinical basis:
  ウイルス性心筋炎が最多(コクサッキーB, アデノウイルス, パルボB19, HHV6等)。
  先行感染(URI/GI): 1-2週前に50-80%。心筋炎発症時は解熱していることも多い。
  胸痛(85-95%, 定常性/胸膜性), 呼吸困難(50-70%), 動悸(40-60%), 頻脈, 倦怠感
  検査: トロポニン著高(>90%), CK上昇(30-50%), CRP上昇(60-80%), LDH上昇
  WBC正常~軽度上昇。ESR軽度上昇。
  重症: 心不全, 不整脈, ショック → severity=critical
  References: Caforio ALP et al. Eur Heart J 2013;34:2636
              Ammirati E et al. JACC 2018;71:2016
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# step1
s1["variables"].append({
    "id": "D116",
    "name": "acute_myocarditis",
    "name_ja": "急性心筋炎",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "ウイルス性が最多。先行URI/GI 1-2週前(50-80%)。"
           "胸痛(定常性85%)+呼吸困難+動悸+頻脈。トロポニン著高, CK上昇。"
           "心筋炎発症時は解熱していることも多い。重症で心不全/ショック。"
})
print("step1: Added D116 acute_myocarditis")

# step2
d_edges = [
    ("E01",  "心筋炎: 発熱は軽度~なし(先行感染からは回復していることが多い)"),
    ("S21",  "心筋炎: 胸痛(85-95%, 定常性/前傾で改善, 臥位で増悪)"),
    ("S04",  "心筋炎: 呼吸困難(50-70%, 心不全)"),
    ("S35",  "心筋炎: 動悸(40-60%, 不整脈)"),
    ("E02",  "心筋炎: 頻脈(50-70%)"),
    ("S07",  "心筋炎: 倦怠感(60-80%)"),
    ("L17",  "心筋炎: CK上昇(30-50%, 心筋逸脱酵素)"),
    ("L02",  "心筋炎: CRP上昇(60-80%)"),
    ("L16",  "心筋炎: LDH上昇(50-70%)"),
    ("L01",  "心筋炎: WBC正常~軽度上昇"),
    ("L28",  "心筋炎: ESR軽度上昇"),
    ("T01",  "心筋炎: 急性発症(先行感染1-2週後, 胸痛は急性)"),
    ("T02",  "心筋炎: 急性発症(時間~日単位)"),
    ("E03",  "心筋炎: 重症例で低血圧(心原性ショック5-10%)"),
    ("S06",  "心筋炎: 筋肉痛(先行URI症状の残存, 20-30%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D116", "to": to_id,
        "from_name": "acute_myocarditis", "to_name": to_id,
        "reason": reason
    })
s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} edges (total: {s2['total_edges']})")

# step3
n = s3["noisy_or_params"]

# E01: 発熱は軽度~なし(先行感染から回復後に胸痛)
n["E01"]["parent_effects"]["D116"] = {
    "under_37.5": 0.35, "37.5_38.0": 0.30, "38.0_39.0": 0.25,
    "39.0_40.0": 0.08, "over_40.0": 0.02
}
# S21: 胸痛(85-95%, constant主体)
n["S21"]["parent_effects"]["D116"] = {"absent": 0.05, "pleuritic": 0.25, "constant": 0.70}
# S04: 呼吸困難(50-70%)
n["S04"]["parent_effects"]["D116"] = {"absent": 0.35, "on_exertion": 0.40, "at_rest": 0.25}
# S35: 動悸(40-60%)
n["S35"]["parent_effects"]["D116"] = {"absent": 0.45, "present": 0.55}
# E02: 頻脈(50-70%)
n["E02"]["parent_effects"]["D116"] = {"under_100": 0.35, "100_120": 0.45, "over_120": 0.20}
# S07: 倦怠感(60-80%)
n["S07"]["parent_effects"]["D116"] = {"absent": 0.20, "mild": 0.30, "severe": 0.50}
# L17: CK上昇(30-50%)
n["L17"]["parent_effects"]["D116"] = {"normal": 0.50, "elevated": 0.35, "very_high": 0.15}
# L02: CRP(60-80%上昇)
n["L02"]["parent_effects"]["D116"] = {
    "normal_under_0.3": 0.10, "mild_0.3_3": 0.15,
    "moderate_3_10": 0.35, "high_over_10": 0.40
}
# L16: LDH(50-70%上昇)
n["L16"]["parent_effects"]["D116"] = {"normal": 0.35, "elevated": 0.65}
# L01: WBC正常~軽度上昇
n["L01"]["parent_effects"]["D116"] = {
    "low_under_4000": 0.05, "normal_4000_10000": 0.55,
    "high_10000_20000": 0.30, "very_high_over_20000": 0.10
}
# L28: ESR軽度上昇
n["L28"]["parent_effects"]["D116"] = {"normal": 0.30, "elevated": 0.55, "very_high_over_100": 0.15}
# T01: 急性(胸痛は急性, 先行感染1-2週前)
n["T01"]["parent_effects"]["D116"] = {
    "under_3d": 0.40, "3d_to_1w": 0.35, "1w_to_3w": 0.20, "over_3w": 0.05
}
# T02: 急性
n["T02"]["parent_effects"]["D116"] = {"sudden_hours": 0.55, "gradual_days": 0.45}
# E03: 低血圧(重症5-10%)
n["E03"]["parent_effects"]["D116"] = {"normal_over_90": 0.90, "hypotension_under_90": 0.10}
# S06: 筋肉痛(20-30%)
n["S06"]["parent_effects"]["D116"] = {"absent": 0.70, "present": 0.30}

print(f"step3: Added {len(d_edges)} CPTs")

# full_cpt: 若年に多い
s3["full_cpts"]["D116"] = {
    "parents": ["R01"],
    "description": "急性心筋炎。若年成人に多い",
    "cpt": {"18_39": 0.004, "40_64": 0.002, "65_plus": 0.002}
}

# Save
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved. 116 diseases, {s2['total_edges']} edges.")
