#!/usr/bin/env python3
"""Add D107 HLH (hemophagocytic lymphohistiocytosis)."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# === step1: Add D107 ===
s1["variables"].append({
    "id": "D107",
    "name": "hemophagocytic_lymphohistiocytosis",
    "name_ja": "血球貪食症候群(HLH/MAS)",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "HLH-2004基準: 発熱+脾腫+血球減少+高TG/低fibrinogen+高ferritin+高sIL-2R+NK活性低下+骨髄血球貪食"
})
print("step1: Added D107 HLH")

# === step2: Add edges ===
# HLH clinical features:
# - 持続性高熱(100%), 脾腫(80-90%), 肝腫大(60-80%)
# - 汎血球減少(80%+): WBC↓, Hb↓, PLT↓
# - Ferritin極高(>10000 in 70%+), LDH↑
# - 肝酵素上昇(70-80%), 黄疸(30-50%)
# - 意識障害(30-50%, CNS involvement)
# - CRP上昇, ESR上昇(ただしfibrinogen低下でESR正常化することも)
# - 出血傾向(DIC合併)
# - T01: 急性〜亜急性
edges = [
    ("E01", "HLH: 持続性高熱(100%), 通常39-41°C"),
    ("E14", "HLH: 脾腫(80-90%)"),
    ("E34", "HLH: 肝腫大(60-80%)"),
    ("L01", "HLH: 白血球減少(70-80%)"),
    ("L14", "HLH: 血小板減少+貧血(80%+)"),
    ("L22", "HLH: 汎血球減少(60-70%)"),
    ("L15", "HLH: ferritin極高(>10000が70%以上, diagnostic)"),
    ("L16", "HLH: LDH上昇(80-90%, 組織破壊)"),
    ("L11", "HLH: 肝酵素上昇(70-80%)"),
    ("E18", "HLH: 黄疸(30-50%, 肝障害)"),
    ("E16", "HLH: 意識障害(30-50%, CNS浸潤)"),
    ("L02", "HLH: CRP上昇"),
    ("L28", "HLH: ESR(fibrinogen低下で正常化しうる)"),
    ("S44", "HLH: 出血傾向(DIC合併30-50%)"),
    ("T01", "HLH: 急性〜亜急性発症"),
    ("T02", "HLH: 急性発症が多い"),
    ("S07", "HLH: 倦怠感(90%+)"),
    ("L41", "HLH: sIL-2R上昇(diagnostic, >2400)"),
    ("E12", "HLH: 皮疹(10-30%)"),
    ("S17", "HLH: 体重減少(30-50%)"),
]
for to_id, reason in edges:
    s2["edges"].append({
        "from": "D107", "to": to_id,
        "from_name": "HLH", "to_name": to_id,
        "reason": reason
    })
print(f"step2: Added {len(edges)} edges for D107")

# === step3: Add CPTs ===
n = s3["noisy_or_params"]

# E01: 持続性高熱
n["E01"]["parent_effects"]["D107"] = {
    "under_37.5": 0.02, "37.5_38.0": 0.03, "38.0_39.0": 0.15,
    "39.0_40.0": 0.45, "over_40.0": 0.35
}
# E14: 脾腫
n["E14"]["parent_effects"]["D107"] = {"absent": 0.15, "present": 0.85}
# E34: 肝腫大
n["E34"]["parent_effects"]["D107"] = {"absent": 0.30, "present": 0.70}
# L01: WBC低下
n["L01"]["parent_effects"]["D107"] = {
    "low_under_4000": 0.55, "normal_4000_10000": 0.30,
    "high_10000_20000": 0.10, "very_high_over_20000": 0.05
}
# L14: 血小板減少+貧血
n["L14"]["parent_effects"]["D107"] = {
    "normal": 0.10, "left_shift": 0.05, "atypical_lymphocytes": 0.05,
    "thrombocytopenia": 0.75, "eosinophilia": 0.05
}
# L22: 汎血球減少
n["L22"]["parent_effects"]["D107"] = {"absent": 0.30, "present": 0.70}
# L15: ferritin極高 (HLHの最重要所見)
n["L15"]["parent_effects"]["D107"] = {
    "normal": 0.02, "mild_elevated": 0.08,
    "very_high_over_1000": 0.20, "extreme_over_10000": 0.70
}
# L16: LDH上昇
n["L16"]["parent_effects"]["D107"] = {"normal": 0.10, "elevated": 0.90}
# L11: 肝酵素上昇
n["L11"]["parent_effects"]["D107"] = {
    "normal": 0.20, "mild_elevated": 0.40, "very_high": 0.40
}
# E18: 黄疸
n["E18"]["parent_effects"]["D107"] = {"absent": 0.60, "present": 0.40}
# E16: 意識障害
n["E16"]["parent_effects"]["D107"] = {
    "alert": 0.55, "confused": 0.25, "obtunded": 0.15, "coma": 0.05
}
# L02: CRP
n["L02"]["parent_effects"]["D107"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.15,
    "moderate_3_10": 0.35, "high_over_10": 0.45
}
# L28: ESR (paradoxically normal in some HLH due to low fibrinogen)
n["L28"]["parent_effects"]["D107"] = {
    "normal": 0.40, "elevated": 0.40, "very_high_over_100": 0.20
}
# S44: 出血傾向
n["S44"]["parent_effects"]["D107"] = {"absent": 0.55, "present": 0.45}
# T01: 急性〜亜急性
n["T01"]["parent_effects"]["D107"] = {
    "under_3d": 0.10, "3d_to_1w": 0.35, "1w_to_3w": 0.40, "over_3w": 0.15
}
# T02: 急性発症
n["T02"]["parent_effects"]["D107"] = {"sudden_hours": 0.30, "gradual_days": 0.70}
# S07: 倦怠感
n["S07"]["parent_effects"]["D107"] = {"absent": 0.05, "mild": 0.20, "severe": 0.75}
# L41: sIL-2R
n["L41"]["parent_effects"]["D107"] = {"normal": 0.05, "elevated": 0.95}
# E12: 皮疹
n["E12"]["parent_effects"]["D107"] = {
    "absent": 0.75, "maculopapular_rash": 0.15,
    "petechiae_purpura": 0.05, "vesicular": 0.01,
    "erythroderma": 0.01, "diffuse_erythema": 0.03
}
# S17: 体重減少
n["S17"]["parent_effects"]["D107"] = {"absent": 0.55, "present": 0.45}

print(f"step3: Added 20 CPTs for D107")

# Save
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("All saved. 107 diseases.")
