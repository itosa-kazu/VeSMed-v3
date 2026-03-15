#!/usr/bin/env python3
"""Add D146 Hypertensive Emergency + D147 Testicular Torsion + D148 Boerhaave."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# Need new variable: E38 hypertensive BP
s1["variables"].append({
    "id": "E38", "name": "blood_pressure_high", "name_ja": "血圧高値(収縮期)",
    "category": "sign", "states": ["normal_under_140", "elevated_140_180", "crisis_over_180"],
    "note": "高血圧の評価。正常<140, 高値140-180, クリーゼ>180。E03(低血圧)とは独立"
})
n["E38"] = {
    "description": "血圧高値。高血圧緊急症で>180",
    "leak": {"normal_under_140": 0.70, "elevated_140_180": 0.25, "crisis_over_180": 0.05},
    "parent_effects": {}
}

# ===== D146 Hypertensive Emergency =====
s1["variables"].append({
    "id": "D146", "name": "hypertensive_emergency",
    "name_ja": "高血圧緊急症",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "BP>180/120+臓器障害(脳/心/腎/眼)。頭痛+視力障害+意識障害+胸痛。IV降圧が必要"
})
for to, reason in [
    ("E38", "高血圧緊急症: BP>180/120(定義)"),
    ("S05", "高血圧緊急症: 頭痛(60-80%)"), ("E16", "高血圧緊急症: 意識障害(脳症で30-40%)"),
    ("S04", "高血圧緊急症: 呼吸困難(肺水腫で)"), ("S21", "高血圧緊急症: 胸痛(解離/ACS合併)"),
    ("E02", "高血圧緊急症: 頻脈(40-50%)"), ("S13", "高血圧緊急症: 嘔気(30-40%)"),
    ("E01", "高血圧緊急症: 通常無熱"), ("L01", "高血圧緊急症: WBC正常~軽度上昇"),
    ("L53", "高血圧緊急症: トロポニン(心筋障害で上昇)"),
    ("T01", "高血圧緊急症: 急性"), ("T02", "高血圧緊急症: 急性~亜急性")]:
    s2["edges"].append({"from": "D146", "to": to, "from_name": "hypertensive_emergency", "to_name": to, "reason": reason})

n["E38"]["parent_effects"]["D146"] = {"normal_under_140": 0.02, "elevated_140_180": 0.08, "crisis_over_180": 0.90}
n["S05"]["parent_effects"]["D146"] = {"absent": 0.15, "mild": 0.25, "severe": 0.60}
n["E16"]["parent_effects"]["D146"] = {"normal": 0.50, "confused": 0.30, "obtunded": 0.20}
n["S04"]["parent_effects"]["D146"] = {"absent": 0.50, "on_exertion": 0.20, "at_rest": 0.30}
n["S21"]["parent_effects"]["D146"] = {"absent": 0.50, "burning": 0.05, "sharp": 0.10, "pressure": 0.30, "tearing": 0.05}
n["E02"]["parent_effects"]["D146"] = {"under_100": 0.40, "100_120": 0.40, "over_120": 0.20}
n["S13"]["parent_effects"]["D146"] = {"absent": 0.60, "present": 0.40}
n["E01"]["parent_effects"]["D146"] = {"under_37.5": 0.80, "37.5_38.0": 0.12, "38.0_39.0": 0.06, "39.0_40.0": 0.02, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D146"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.60, "high_10000_20000": 0.30, "very_high_over_20000": 0.07}
n["L53"]["parent_effects"]["D146"] = {"not_done": 0.20, "normal": 0.35, "mildly_elevated": 0.30, "very_high": 0.15}
n["T01"]["parent_effects"]["D146"] = {"under_3d": 0.70, "3d_to_1w": 0.20, "1w_to_3w": 0.08, "over_3w": 0.02}
n["T02"]["parent_effects"]["D146"] = {"sudden_hours": 0.55, "gradual_days": 0.45}
# Also add E38 edges to stroke/dissection/ACS
n["E38"]["parent_effects"]["D138"] = {"normal_under_140": 0.30, "elevated_140_180": 0.40, "crisis_over_180": 0.30}
n["E38"]["parent_effects"]["D139"] = {"normal_under_140": 0.15, "elevated_140_180": 0.30, "crisis_over_180": 0.55}
n["E38"]["parent_effects"]["D132"] = {"normal_under_140": 0.25, "elevated_140_180": 0.35, "crisis_over_180": 0.40}
n["E38"]["parent_effects"]["D131"] = {"normal_under_140": 0.35, "elevated_140_180": 0.40, "crisis_over_180": 0.25}
for did in ["D138", "D139", "D132", "D131"]:
    s2["edges"].append({"from": did, "to": "E38", "from_name": did, "to_name": "E38", "reason": f"{did}→血圧高値"})
s3["full_cpts"]["D146"] = {"parents": [], "description": "高血圧緊急症", "cpt": {"": 0.005}}

# ===== D147 Testicular Torsion =====
s1["variables"].append({
    "id": "D147", "name": "testicular_torsion",
    "name_ja": "精巣捻転",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "若年男性の突然の陰嚢痛。6h以内に手術必要。挙睾筋反射消失。Echo血流なし"
})
for to, reason in [
    ("S13", "精巣捻転: 嘔気嘔吐(60-70%)"),
    ("E01", "精巣捻転: 通常無熱"), ("E02", "精巣捻転: 頻脈(疼痛)"),
    ("L01", "精巣捻転: WBC正常~軽度上昇"), ("L02", "精巣捻転: CRP通常正常"),
    ("T01", "精巣捻転: 超急性(数時間)"), ("T02", "精巣捻転: 突然発症")]:
    s2["edges"].append({"from": "D147", "to": to, "from_name": "testicular_torsion", "to_name": to, "reason": reason})

n["S13"]["parent_effects"]["D147"] = {"absent": 0.25, "present": 0.75}
n["E01"]["parent_effects"]["D147"] = {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.00}
n["E02"]["parent_effects"]["D147"] = {"under_100": 0.30, "100_120": 0.50, "over_120": 0.20}
n["L01"]["parent_effects"]["D147"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.70, "high_10000_20000": 0.22, "very_high_over_20000": 0.05}
n["L02"]["parent_effects"]["D147"] = {"normal_under_0.3": 0.60, "mild_0.3_3": 0.25, "moderate_3_10": 0.12, "high_over_10": 0.03}
n["T01"]["parent_effects"]["D147"] = {"under_3d": 0.95, "3d_to_1w": 0.04, "1w_to_3w": 0.01, "over_3w": 0.00}
n["T02"]["parent_effects"]["D147"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
s3["full_cpts"]["D147"] = {"parents": ["R01"], "description": "精巣捻転。若年男性に多い",
    "cpt": {"18_39": 0.004, "40_64": 0.001, "65_plus": 0.001}}

# ===== D148 Boerhaave Syndrome =====
s1["variables"].append({
    "id": "D148", "name": "boerhaave_syndrome",
    "name_ja": "特発性食道破裂(Boerhaave症候群)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "嘔吐後の突然胸痛+縦隔気腫+皮下気腫。Mackler triad(嘔吐+胸痛+皮下気腫)"
})
for to, reason in [
    ("S21", "Boerhaave: 突然の激烈胸痛(90%+)"),
    ("S13", "Boerhaave: 嘔吐(先行, 90%+)"), ("S04", "Boerhaave: 呼吸困難(50-60%)"),
    ("E01", "Boerhaave: 発熱(感染合併で)"), ("E02", "Boerhaave: 頻脈(60-70%)"),
    ("E03", "Boerhaave: 低血圧(重症/敗血症で)"),
    ("L01", "Boerhaave: WBC上昇"), ("L02", "Boerhaave: CRP上昇"),
    ("L04", "Boerhaave: CXR — 縦隔気腫/胸水/皮下気腫"),
    ("T01", "Boerhaave: 超急性(数時間)"), ("T02", "Boerhaave: 突然発症")]:
    s2["edges"].append({"from": "D148", "to": to, "from_name": "boerhaave_syndrome", "to_name": to, "reason": reason})

n["S21"]["parent_effects"]["D148"] = {"absent": 0.05, "burning": 0.05, "sharp": 0.55, "pressure": 0.25, "tearing": 0.10}
n["S13"]["parent_effects"]["D148"] = {"absent": 0.05, "present": 0.95}
n["S04"]["parent_effects"]["D148"] = {"absent": 0.30, "on_exertion": 0.15, "at_rest": 0.55}
n["E01"]["parent_effects"]["D148"] = {"under_37.5": 0.35, "37.5_38.0": 0.25, "38.0_39.0": 0.25, "39.0_40.0": 0.12, "over_40.0": 0.03}
n["E02"]["parent_effects"]["D148"] = {"under_100": 0.20, "100_120": 0.50, "over_120": 0.30}
n["E03"]["parent_effects"]["D148"] = {"normal_over_90": 0.55, "hypotension_under_90": 0.45}
n["L01"]["parent_effects"]["D148"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.20, "high_10000_20000": 0.45, "very_high_over_20000": 0.32}
n["L02"]["parent_effects"]["D148"] = {"normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.30, "high_over_10": 0.55}
n["L04"]["parent_effects"]["D148"] = {"normal": 0.10, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.10, "BHL": 0.02, "pleural_effusion": 0.40, "pneumothorax": 0.33}
n["T01"]["parent_effects"]["D148"] = {"under_3d": 0.90, "3d_to_1w": 0.08, "1w_to_3w": 0.02, "over_3w": 0.00}
n["T02"]["parent_effects"]["D148"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
# S50/S51 for Boerhaave
n["S50"]["parent_effects"]["D148"] = {"not_applicable": 0.05, "none": 0.30, "exertion": 0.05, "breathing": 0.30, "position": 0.05, "meals": 0.25}
n["S51"]["parent_effects"]["D148"] = {"not_applicable": 0.05, "none": 0.60, "left_arm_jaw": 0.05, "back": 0.30}
s2["edges"].append({"from": "D148", "to": "S50", "from_name": "boerhaave_syndrome", "to_name": "S50", "reason": "Boerhaave→胸痛誘発"})
s2["edges"].append({"from": "D148", "to": "S51", "from_name": "boerhaave_syndrome", "to_name": "S51", "reason": "Boerhaave→胸痛放散(背部)"})
s3["full_cpts"]["D148"] = {"parents": [], "description": "Boerhaave症候群", "cpt": {"": 0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D146 HtnE: 12 edges, D147 Torsion: 7 edges, D148 Boerhaave: 13 edges")
print(f"E38 blood_pressure_high: 5 parents (D146/D138/D139/D132/D131)")
print(f"Total: {s2['total_edges']} edges, 148 diseases")
