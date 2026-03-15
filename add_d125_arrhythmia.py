#!/usr/bin/env python3
"""Add D125 Acute Cardiac Arrhythmia (急性不整脈: AF/SVT/VT).

Clinical basis:
  原発性の頻脈性不整脈(AF/SVT/VT)が急性症状を起こす。
  動悸(90%+), 呼吸困難(50-70%), めまい(40-60%),
  胸痛/不快感(30-40%), 意識消失(VTで)
  頻脈(HR>100, しばしば>150), 低血圧(重症で)
  ECGで確定。BNP軽度上昇, トロポニン軽度上昇(頻脈性心筋障害)
  二次性不整脈(PE/敗血症/甲状腺)は除外が必要
  References: January CT et al. JACC 2014 (AF guideline)
              Page RL et al. JACC 2016 (SVT guideline)
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
    "id": "D125", "name": "acute_arrhythmia",
    "name_ja": "急性不整脈（AF/SVT/VT）",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "原発性頻脈性不整脈。動悸+呼吸困難+めまい。HR>150が多い。"
           "ECGで確定。BNP/トロポニン軽度上昇。二次性(PE/敗血症/甲状腺)除外要"
})

d_edges = [
    ("S35",  "不整脈: 動悸(90%+, 最多症状)"),
    ("S04",  "不整脈: 呼吸困難(50-70%)"),
    ("S21",  "不整脈: 胸痛/不快感(30-40%)"),
    ("E02",  "不整脈: 頻脈(95%+, HR>150が多い)"),
    ("E03",  "不整脈: 低血圧(重症/VTで20-30%)"),
    ("E16",  "不整脈: 意識障害(VTで10-20%, 失神)"),
    ("S07",  "不整脈: 倦怠感(30-40%)"),
    ("E01",  "不整脈: 通常無熱"),
    ("L51",  "不整脈: BNP軽度上昇(頻脈性心筋障害)"),
    ("L01",  "不整脈: WBC通常正常"),
    ("L02",  "不整脈: CRP通常正常"),
    ("L04",  "不整脈: CXR通常正常(心不全合併なら肺うっ血)"),
    ("T01",  "不整脈: 急性(数分~数時間)"),
    ("T02",  "不整脈: 突然発症"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D125", "to": to_id, "from_name": "acute_arrhythmia", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

n["S35"]["parent_effects"]["D125"] = {"absent": 0.05, "present": 0.95}
n["S04"]["parent_effects"]["D125"] = {"absent": 0.30, "on_exertion": 0.30, "at_rest": 0.40}
n["S21"]["parent_effects"]["D125"] = {"absent": 0.55, "pleuritic": 0.05, "constant": 0.40}
n["E02"]["parent_effects"]["D125"] = {"under_100": 0.03, "100_120": 0.17, "over_120": 0.80}
n["E03"]["parent_effects"]["D125"] = {"normal_over_90": 0.70, "hypotension_under_90": 0.30}
n["E16"]["parent_effects"]["D125"] = {"normal": 0.80, "confused": 0.12, "obtunded": 0.08}
n["S07"]["parent_effects"]["D125"] = {"absent": 0.50, "mild": 0.30, "severe": 0.20}
n["E01"]["parent_effects"]["D125"] = {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.00}
n["L51"]["parent_effects"]["D125"] = {"not_done": 0.30, "normal": 0.20, "mildly_elevated": 0.35, "very_high": 0.15}
n["L01"]["parent_effects"]["D125"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.75, "high_10000_20000": 0.18, "very_high_over_20000": 0.04}
n["L02"]["parent_effects"]["D125"] = {"normal_under_0.3": 0.55, "mild_0.3_3": 0.30, "moderate_3_10": 0.12, "high_over_10": 0.03}
n["L04"]["parent_effects"]["D125"] = {"normal": 0.65, "lobar_infiltrate": 0.03, "bilateral_infiltrate": 0.15, "BHL": 0.02, "pleural_effusion": 0.10, "pneumothorax": 0.05}
n["T01"]["parent_effects"]["D125"] = {"under_3d": 0.70, "3d_to_1w": 0.20, "1w_to_3w": 0.08, "over_3w": 0.02}
n["T02"]["parent_effects"]["D125"] = {"sudden_hours": 0.75, "gradual_days": 0.25}

s3["full_cpts"]["D125"] = {
    "parents": ["R44"],
    "description": "急性不整脈。心疾患既往がリスク",
    "cpt": {"no": 0.003, "yes": 0.015}
}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D125: {len(d_edges)} edges. Total: {s2['total_edges']}")
