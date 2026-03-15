#!/usr/bin/env python3
"""Add D133 GERD + D134 Pericarditis + D135 Costochondritis."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ============ D133 GERD ============
s1["variables"].append({
    "id": "D133", "name": "GERD", "name_ja": "逆流性食道炎(GERD)",
    "category": "disease", "states": ["no", "yes"], "severity": "low",
    "note": "非心臓性胸痛の最多原因。胸骨下灼熱感/圧迫感。ACSと誤診されやすい。"
           "トロポニン正常+ECG正常+PPI反応が鍵。内視鏡で食道炎確認"
})
for to, reason in [
    ("S21", "GERD: 胸痛(80%+, 胸骨下灼熱/圧迫, ACS様)"),
    ("S13", "GERD: 嘔気(30-40%)"), ("S07", "GERD: 倦怠感(20-30%)"),
    ("E01", "GERD: 無熱"), ("L01", "GERD: WBC正常"), ("L02", "GERD: CRP正常"),
    ("L53", "GERD: トロポニン正常(ACSとの鑑別に重要)"),
    ("L04", "GERD: CXR正常"), ("L51", "GERD: BNP正常"),
    ("T01", "GERD: 慢性/反復性"), ("T02", "GERD: 緩徐(慢性反復)")]:
    s2["edges"].append({"from": "D133", "to": to, "from_name": "GERD", "to_name": to, "reason": reason})

n["S21"]["parent_effects"]["D133"] = {"absent": 0.10, "pleuritic": 0.05, "constant": 0.85}
n["S13"]["parent_effects"]["D133"] = {"absent": 0.60, "present": 0.40}
n["S07"]["parent_effects"]["D133"] = {"absent": 0.65, "mild": 0.25, "severe": 0.10}
n["E01"]["parent_effects"]["D133"] = {"under_37.5": 0.95, "37.5_38.0": 0.04, "38.0_39.0": 0.01, "39.0_40.0": 0.00, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D133"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.90, "high_10000_20000": 0.06, "very_high_over_20000": 0.01}
n["L02"]["parent_effects"]["D133"] = {"normal_under_0.3": 0.85, "mild_0.3_3": 0.12, "moderate_3_10": 0.03, "high_over_10": 0.00}
n["L53"]["parent_effects"]["D133"] = {"not_done": 0.30, "normal": 0.65, "mildly_elevated": 0.04, "very_high": 0.01}
n["L04"]["parent_effects"]["D133"] = {"normal": 0.90, "lobar_infiltrate": 0.02, "bilateral_infiltrate": 0.02, "BHL": 0.02, "pleural_effusion": 0.02, "pneumothorax": 0.02}
n["L51"]["parent_effects"]["D133"] = {"not_done": 0.40, "normal": 0.55, "mildly_elevated": 0.04, "very_high": 0.01}
n["T01"]["parent_effects"]["D133"] = {"under_3d": 0.15, "3d_to_1w": 0.20, "1w_to_3w": 0.25, "over_3w": 0.40}
n["T02"]["parent_effects"]["D133"] = {"sudden_hours": 0.20, "gradual_days": 0.80}
s3["full_cpts"]["D133"] = {"parents": [], "description": "GERD", "cpt": {"": 0.010}}

# ============ D134 Acute Pericarditis ============
s1["variables"].append({
    "id": "D134", "name": "acute_pericarditis", "name_ja": "急性心膜炎",
    "category": "disease", "states": ["no", "yes"], "severity": "moderate",
    "note": "胸痛(前傾で改善/臥位で増悪)+心膜摩擦音+ST上昇(びまん性)。"
           "ウイルス性が最多。心筋炎(D116)との鑑別: 心膜炎はEF保持/トロポニン正常~軽度"
})
for to, reason in [
    ("S21", "心膜炎: 胸痛(90%+, 前傾改善/臥位増悪, pleuritic)"),
    ("E15", "心膜炎: 心膜摩擦音(30-50%)"),
    ("E01", "心膜炎: 発熱(30-50%, ウイルス性)"),
    ("S04", "心膜炎: 呼吸困難(20-30%)"),
    ("E02", "心膜炎: 頻脈(30-40%)"),
    ("L02", "心膜炎: CRP上昇(60-80%)"),
    ("L53", "心膜炎: トロポニン正常~軽度(心筋炎合併なら上昇)"),
    ("L01", "心膜炎: WBC正常~軽度上昇"),
    ("L28", "心膜炎: ESR上昇(60-70%)"),
    ("L04", "心膜炎: CXR通常正常(大量心嚢液なら心拡大)"),
    ("T01", "心膜炎: 急性(数日)"), ("T02", "心膜炎: 急性~亜急性")]:
    s2["edges"].append({"from": "D134", "to": to, "from_name": "acute_pericarditis", "to_name": to, "reason": reason})

n["S21"]["parent_effects"]["D134"] = {"absent": 0.05, "pleuritic": 0.65, "constant": 0.30}
n["E15"]["parent_effects"]["D134"] = {"absent": 0.55, "pre_existing": 0.05, "new": 0.40}
n["E01"]["parent_effects"]["D134"] = {"under_37.5": 0.40, "37.5_38.0": 0.25, "38.0_39.0": 0.25, "39.0_40.0": 0.08, "over_40.0": 0.02}
n["S04"]["parent_effects"]["D134"] = {"absent": 0.65, "on_exertion": 0.20, "at_rest": 0.15}
n["E02"]["parent_effects"]["D134"] = {"under_100": 0.55, "100_120": 0.35, "over_120": 0.10}
n["L02"]["parent_effects"]["D134"] = {"normal_under_0.3": 0.10, "mild_0.3_3": 0.20, "moderate_3_10": 0.40, "high_over_10": 0.30}
n["L53"]["parent_effects"]["D134"] = {"not_done": 0.15, "normal": 0.45, "mildly_elevated": 0.30, "very_high": 0.10}
n["L01"]["parent_effects"]["D134"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.50, "high_10000_20000": 0.37, "very_high_over_20000": 0.10}
n["L28"]["parent_effects"]["D134"] = {"normal": 0.20, "elevated": 0.50, "very_high_over_100": 0.30}
n["L04"]["parent_effects"]["D134"] = {"normal": 0.70, "lobar_infiltrate": 0.03, "bilateral_infiltrate": 0.05, "BHL": 0.02, "pleural_effusion": 0.15, "pneumothorax": 0.05}
n["T01"]["parent_effects"]["D134"] = {"under_3d": 0.35, "3d_to_1w": 0.40, "1w_to_3w": 0.20, "over_3w": 0.05}
n["T02"]["parent_effects"]["D134"] = {"sudden_hours": 0.45, "gradual_days": 0.55}
s3["full_cpts"]["D134"] = {"parents": [], "description": "急性心膜炎", "cpt": {"": 0.004}}

# ============ D135 Costochondritis ============
s1["variables"].append({
    "id": "D135", "name": "costochondritis", "name_ja": "肋軟骨炎（筋骨格系胸痛）",
    "category": "disease", "states": ["no", "yes"], "severity": "low",
    "note": "ER胸痛の最多原因(30-50%)。胸壁圧痛+体動で増悪。全検査正常。除外診断"
})
for to, reason in [
    ("S21", "肋軟骨炎: 胸痛(95%+, 限局性, 圧痛, 体動で増悪)"),
    ("E01", "肋軟骨炎: 無熱"), ("L01", "肋軟骨炎: WBC正常"),
    ("L02", "肋軟骨炎: CRP正常"), ("L53", "肋軟骨炎: トロポニン正常"),
    ("L04", "肋軟骨炎: CXR正常"), ("L51", "肋軟骨炎: BNP正常"),
    ("T01", "肋軟骨炎: 急性~慢性(様々)"), ("T02", "肋軟骨炎: 急性~緩徐")]:
    s2["edges"].append({"from": "D135", "to": to, "from_name": "costochondritis", "to_name": to, "reason": reason})

n["S21"]["parent_effects"]["D135"] = {"absent": 0.03, "pleuritic": 0.55, "constant": 0.42}
n["E01"]["parent_effects"]["D135"] = {"under_37.5": 0.95, "37.5_38.0": 0.04, "38.0_39.0": 0.01, "39.0_40.0": 0.00, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D135"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.90, "high_10000_20000": 0.06, "very_high_over_20000": 0.01}
n["L02"]["parent_effects"]["D135"] = {"normal_under_0.3": 0.85, "mild_0.3_3": 0.12, "moderate_3_10": 0.03, "high_over_10": 0.00}
n["L53"]["parent_effects"]["D135"] = {"not_done": 0.30, "normal": 0.65, "mildly_elevated": 0.04, "very_high": 0.01}
n["L04"]["parent_effects"]["D135"] = {"normal": 0.92, "lobar_infiltrate": 0.02, "bilateral_infiltrate": 0.01, "BHL": 0.01, "pleural_effusion": 0.02, "pneumothorax": 0.02}
n["L51"]["parent_effects"]["D135"] = {"not_done": 0.40, "normal": 0.55, "mildly_elevated": 0.04, "very_high": 0.01}
n["T01"]["parent_effects"]["D135"] = {"under_3d": 0.30, "3d_to_1w": 0.30, "1w_to_3w": 0.25, "over_3w": 0.15}
n["T02"]["parent_effects"]["D135"] = {"sudden_hours": 0.35, "gradual_days": 0.65}
s3["full_cpts"]["D135"] = {"parents": [], "description": "肋軟骨炎。ER胸痛最多", "cpt": {"": 0.015}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D133 GERD: 11 edges, D134 Pericarditis: 12 edges, D135 Costochondritis: 9 edges")
print(f"Total: {s2['total_edges']} edges, 135 diseases")
