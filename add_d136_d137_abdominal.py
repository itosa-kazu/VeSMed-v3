#!/usr/bin/env python3
"""Add D136 Peptic Ulcer Perforation + D137 Mesenteric Ischemia + R48 AF history."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# R48: AF既往 (腸間膜虚血+PE+不整脈に共通リスク)
s1["variables"].append({
    "id": "R48", "name": "atrial_fibrillation_history", "name_ja": "心房細動既往",
    "category": "risk_factor", "states": ["no", "yes"],
    "note": "心房細動既往。塞栓リスク(腸間膜虚血/PE/脳卒中)"
})
s3["root_priors"]["R48"] = {"description": "心房細動既往", "distribution": {"no": 0.90, "yes": 0.10}}

# ============ D136 Peptic Ulcer Perforation ============
s1["variables"].append({
    "id": "D136", "name": "peptic_ulcer_perforation",
    "name_ja": "消化性潰瘍穿孔",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "突然の心窩部激痛+板状硬。NSAIDs/H.pyloriがリスク。CXR free air。緊急手術"
})
for to, reason in [
    ("S12", "穿孔: 腹痛(95%+, 心窩部→びまん性, 突然発症)"),
    ("E09", "穿孔: 腹部触診 — 板状硬/腹膜刺激徴候(90%+)"),
    ("E01", "穿孔: 発熱(腹膜炎で30-50%)"),
    ("E02", "穿孔: 頻脈(60-70%, 腹膜炎/ショック)"),
    ("E03", "穿孔: 低血圧(重症/遅延例で30-40%)"),
    ("S13", "穿孔: 嘔気嘔吐(40-50%)"),
    ("L01", "穿孔: WBC上昇(80-90%)"),
    ("L02", "穿孔: CRP上昇(腹膜炎)"),
    ("L04", "穿孔: CXR — free air(横隔膜下遊離ガス, 80%)"),
    ("L31", "穿孔: 腹部CT — 遊離ガス+腹水"),
    ("T01", "穿孔: 超急性(数時間)"),
    ("T02", "穿孔: 突然発症(最初から最大)")]:
    s2["edges"].append({"from": "D136", "to": to, "from_name": "peptic_ulcer_perforation", "to_name": to, "reason": reason})

n["S12"]["parent_effects"]["D136"] = {"absent": 0.03, "epigastric": 0.45, "RUQ": 0.05, "RLQ": 0.02, "LLQ": 0.02, "suprapubic": 0.01, "diffuse": 0.42}
n["E09"]["parent_effects"]["D136"] = {"soft_nontender": 0.03, "localized_tenderness": 0.12, "peritoneal_signs": 0.85}
n["E01"]["parent_effects"]["D136"] = {"under_37.5": 0.40, "37.5_38.0": 0.25, "38.0_39.0": 0.25, "39.0_40.0": 0.08, "over_40.0": 0.02}
n["E02"]["parent_effects"]["D136"] = {"under_100": 0.25, "100_120": 0.50, "over_120": 0.25}
n["E03"]["parent_effects"]["D136"] = {"normal_over_90": 0.60, "hypotension_under_90": 0.40}
n["S13"]["parent_effects"]["D136"] = {"absent": 0.45, "present": 0.55}
n["L01"]["parent_effects"]["D136"] = {"low_under_4000": 0.02, "normal_4000_10000": 0.10, "high_10000_20000": 0.50, "very_high_over_20000": 0.38}
n["L02"]["parent_effects"]["D136"] = {"normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.30, "high_over_10": 0.55}
n["L04"]["parent_effects"]["D136"] = {"normal": 0.15, "lobar_infiltrate": 0.02, "bilateral_infiltrate": 0.03, "BHL": 0.01, "pleural_effusion": 0.05, "pneumothorax": 0.74}
# Note: free air on CXR mapped to "pneumothorax" state (closest - subdiaphragmatic air)
n["L31"]["parent_effects"]["D136"] = {"normal": 0.05, "abscess": 0.10, "mass": 0.05, "other_abnormal": 0.80}
n["T01"]["parent_effects"]["D136"] = {"under_3d": 0.85, "3d_to_1w": 0.12, "1w_to_3w": 0.02, "over_3w": 0.01}
n["T02"]["parent_effects"]["D136"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
s3["full_cpts"]["D136"] = {"parents": [], "description": "消化性潰瘍穿孔", "cpt": {"": 0.003}}

# ============ D137 Mesenteric Ischemia ============
s1["variables"].append({
    "id": "D137", "name": "acute_mesenteric_ischemia",
    "name_ja": "急性腸間膜虚血",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "SMA塞栓/血栓。激烈腹痛なのに腹部所見が乏しい(pain out of proportion)。"
           "AF既往がリスク。乳酸アシドーシス+LDH上昇。致死率50-80%(診断遅延時)"
})
for to, reason in [
    ("S12", "腸間膜虚血: 激烈腹痛(90%+, びまん性/臍周囲)"),
    ("E09", "腸間膜虚血: 腹部触診 — 初期はsoft(pain out of proportion!), 後期は腹膜刺激"),
    ("S13", "腸間膜虚血: 嘔気嘔吐(60-70%)"),
    ("E01", "腸間膜虚血: 発熱(壊死後30-40%)"),
    ("E02", "腸間膜虚血: 頻脈(70-80%)"),
    ("E03", "腸間膜虚血: 低血圧(重症/壊死後)"),
    ("L01", "腸間膜虚血: WBC上昇(70-80%)"),
    ("L02", "腸間膜虚血: CRP上昇"),
    ("L16", "腸間膜虚血: LDH著明上昇(腸管壊死)"),
    ("L52", "腸間膜虚血: D-dimer上昇(血栓)"),
    ("L31", "腸間膜虚血: 腹部CT — 腸管壁肥厚/門脈ガス"),
    ("T01", "腸間膜虚血: 急性(数時間)"),
    ("T02", "腸間膜虚血: 突然発症(塞栓型)")]:
    s2["edges"].append({"from": "D137", "to": to, "from_name": "acute_mesenteric_ischemia", "to_name": to, "reason": reason})

n["S12"]["parent_effects"]["D137"] = {"absent": 0.03, "epigastric": 0.15, "RUQ": 0.05, "RLQ": 0.05, "LLQ": 0.05, "suprapubic": 0.02, "diffuse": 0.65}
n["E09"]["parent_effects"]["D137"] = {"soft_nontender": 0.40, "localized_tenderness": 0.30, "peritoneal_signs": 0.30}
# Key: soft_nontender=0.40 reflects "pain out of proportion to exam"
n["S13"]["parent_effects"]["D137"] = {"absent": 0.25, "present": 0.75}
n["E01"]["parent_effects"]["D137"] = {"under_37.5": 0.45, "37.5_38.0": 0.20, "38.0_39.0": 0.20, "39.0_40.0": 0.10, "over_40.0": 0.05}
n["E02"]["parent_effects"]["D137"] = {"under_100": 0.15, "100_120": 0.45, "over_120": 0.40}
n["E03"]["parent_effects"]["D137"] = {"normal_over_90": 0.50, "hypotension_under_90": 0.50}
n["L01"]["parent_effects"]["D137"] = {"low_under_4000": 0.02, "normal_4000_10000": 0.15, "high_10000_20000": 0.45, "very_high_over_20000": 0.38}
n["L02"]["parent_effects"]["D137"] = {"normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.30, "high_over_10": 0.55}
n["L16"]["parent_effects"]["D137"] = {"normal": 0.15, "elevated": 0.85}
n["L52"]["parent_effects"]["D137"] = {"not_done": 0.20, "normal": 0.05, "mildly_elevated": 0.25, "very_high": 0.50}
n["L31"]["parent_effects"]["D137"] = {"normal": 0.10, "abscess": 0.05, "mass": 0.05, "other_abnormal": 0.80}
n["T01"]["parent_effects"]["D137"] = {"under_3d": 0.80, "3d_to_1w": 0.15, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D137"] = {"sudden_hours": 0.75, "gradual_days": 0.25}

s3["full_cpts"]["D137"] = {
    "parents": ["R48", "R01"],
    "description": "急性腸間膜虚血。AF既往+高齢がリスク",
    "cpt": {
        "no|18_39": 0.001, "no|40_64": 0.002, "no|65_plus": 0.003,
        "yes|18_39": 0.005, "yes|40_64": 0.010, "yes|65_plus": 0.020,
    }
}

# Also add R48 as parent for D77 (PE) - AF is a risk for VTE too
# (D77 already exists, just update its full_cpt if needed - skip for now)

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D136: 12 edges, D137: 13 edges, R48 added")
print(f"Total: {s2['total_edges']} edges, 137 diseases")
