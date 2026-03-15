#!/usr/bin/env python3
"""Add D127 Pleural Effusion non-infectious (胸水/非感染性).

Clinical basis:
  原因: 悪性腫瘍(滲出性), 心不全(漏出性), ネフローゼ(漏出性), 膠原病
  呼吸困難(90%+), 咳嗽(40-60%), 胸痛(30-50%, 胸膜性)
  聴診: 呼吸音減弱(患側), CXR: 胸水貯留
  BNP: 心不全性なら著高, 悪性なら正常
  胸水穿刺: Light's criteria で漏出性/滲出性を分類
  D36(膿胸)は感染性胸水として既存 — こちらは非感染性
  References: Light RW. NEJM 2002;346:1971
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
    "id": "D127", "name": "pleural_effusion_noninfectious",
    "name_ja": "胸水（非感染性）",
    "category": "disease", "states": ["no", "yes"], "severity": "moderate",
    "note": "悪性腫瘍/心不全/ネフローゼ/膠原病による非感染性胸水。"
           "呼吸困難+呼吸音減弱+CXR胸水。Light's criteriaで分類"
})

d_edges = [
    ("S04",  "胸水: 呼吸困難(90%+, 大量で安静時)"),
    ("S01",  "胸水: 咳嗽(40-60%, 乾性)"),
    ("S21",  "胸水: 胸痛(30-50%, 胸膜性)"),
    ("E07",  "胸水: 聴診 — 患側呼吸音減弱/消失"),
    ("L04",  "胸水: CXR — 胸水貯留"),
    ("E04",  "胸水: 頻呼吸(50-60%)"),
    ("E05",  "胸水: 低酸素(大量で)"),
    ("S49",  "胸水: 起座呼吸(大量で30-40%)"),
    ("E01",  "胸水: 通常無熱(悪性/心不全性)"),
    ("L01",  "胸水: WBC通常正常"),
    ("L02",  "胸水: CRP通常正常~軽度(悪性/膠原病で上昇)"),
    ("L51",  "胸水: BNP — 心不全性なら著高, 悪性なら正常"),
    ("S17",  "胸水: 体重減少(悪性の場合30-40%)"),
    ("S07",  "胸水: 倦怠感(50-60%)"),
    ("T01",  "胸水: 亜急性~慢性(数日~数週)"),
    ("T02",  "胸水: 緩徐発症"),
    ("E36",  "胸水: 下腿浮腫(心不全/ネフローゼで両側)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D127", "to": to_id, "from_name": "pleural_effusion_noninfectious", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

n["S04"]["parent_effects"]["D127"] = {"absent": 0.08, "on_exertion": 0.35, "at_rest": 0.57}
n["S01"]["parent_effects"]["D127"] = {"absent": 0.40, "dry": 0.45, "productive": 0.15}
n["S21"]["parent_effects"]["D127"] = {"absent": 0.50, "pleuritic": 0.35, "constant": 0.15}
n["E07"]["parent_effects"]["D127"] = {"clear": 0.10, "crackles": 0.10, "wheezes": 0.05, "decreased_absent": 0.75}
n["L04"]["parent_effects"]["D127"] = {"normal": 0.05, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.10, "BHL": 0.02, "pleural_effusion": 0.75, "pneumothorax": 0.03}
n["E04"]["parent_effects"]["D127"] = {"normal_under_20": 0.30, "tachypnea_20_30": 0.50, "severe_over_30": 0.20}
n["E05"]["parent_effects"]["D127"] = {"normal_over_96": 0.35, "mild_hypoxia_93_96": 0.40, "severe_hypoxia_under_93": 0.25}
n["S49"]["parent_effects"]["D127"] = {"absent": 0.60, "present": 0.40}
n["E01"]["parent_effects"]["D127"] = {"under_37.5": 0.70, "37.5_38.0": 0.15, "38.0_39.0": 0.10, "39.0_40.0": 0.04, "over_40.0": 0.01}
n["L01"]["parent_effects"]["D127"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.65, "high_10000_20000": 0.25, "very_high_over_20000": 0.05}
n["L02"]["parent_effects"]["D127"] = {"normal_under_0.3": 0.35, "mild_0.3_3": 0.30, "moderate_3_10": 0.25, "high_over_10": 0.10}
n["L51"]["parent_effects"]["D127"] = {"not_done": 0.25, "normal": 0.30, "mildly_elevated": 0.25, "very_high": 0.20}
n["S17"]["parent_effects"]["D127"] = {"absent": 0.60, "present": 0.40}
n["S07"]["parent_effects"]["D127"] = {"absent": 0.25, "mild": 0.35, "severe": 0.40}
n["T01"]["parent_effects"]["D127"] = {"under_3d": 0.05, "3d_to_1w": 0.20, "1w_to_3w": 0.40, "over_3w": 0.35}
n["T02"]["parent_effects"]["D127"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
n["E36"]["parent_effects"]["D127"] = {"absent": 0.45, "unilateral": 0.05, "bilateral": 0.50}

s3["full_cpts"]["D127"] = {
    "parents": [],
    "description": "非感染性胸水。悪性腫瘍/心不全/ネフローゼ",
    "cpt": {"": 0.005}
}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D127: {len(d_edges)} edges. Total: {s2['total_edges']}")
