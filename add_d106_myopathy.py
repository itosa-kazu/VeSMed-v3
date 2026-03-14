#!/usr/bin/env python3
"""Add D106 inflammatory myopathy (DM/PM) + S48 proximal muscle weakness."""
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
    "id": "D106", "name": "inflammatory_myopathy",
    "name_ja": "炎症性筋疾患（皮膚筋炎/多発性筋炎）",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "DM:heliotrope疹+Gottron丘疹+近位筋力低下。PM:皮膚所見なし。悪性腫瘍合併注意"
})
s1["variables"].append({
    "id": "S48", "name": "proximal_muscle_weakness",
    "name_ja": "近位筋力低下", "category": "symptom",
    "states": ["absent", "present"],
    "note": "起立困難、階段昇降困難、腕挙上困難"
})

# step2
edges = [
    ("S48", "近位筋力低下(>90%)"),
    ("L17", "CK上昇(>95%, 通常5-50倍)"),
    ("E01", "発熱(20-50%)"),
    ("E12", "DM皮膚所見(heliotrope/Gottron)"),
    ("S25", "嚥下困難(30-40%)"),
    ("S08", "関節痛(20-50%)"),
    ("S07", "倦怠感(60-80%)"),
    ("S06", "筋肉痛(50-70%)"),
    ("L04", "間質性肺炎(20-40%)"),
    ("L02", "CRP上昇(50-70%)"),
    ("L28", "ESR上昇(50-70%)"),
    ("L16", "LDH上昇(筋原性)"),
    ("S17", "体重減少(30-50%)"),
    ("T01", "亜急性〜慢性経過"),
    ("T02", "緩徐発症"),
    ("L18", "ANA陽性(60-80%)"),
    ("E20", "DM heliotrope疹(蝶形紅斑類似)"),
]
for to_id, reason in edges:
    s2["edges"].append({
        "from": "D106", "to": to_id,
        "from_name": "inflammatory_myopathy", "to_name": to_id,
        "reason": f"DM/PM: {reason}"
    })

# step3
n = s3["noisy_or_params"]
n["S48"] = {
    "description": "近位筋力低下(起立困難・腕挙上困難)",
    "states": ["absent", "present"],
    "leak": {"absent": 0.97, "present": 0.03},
    "parent_effects": {"D106": {"absent": 0.05, "present": 0.95}}
}
n["L17"]["parent_effects"]["D106"] = {"normal": 0.03, "elevated": 0.27, "very_high": 0.70}
n["E01"]["parent_effects"]["D106"] = {
    "under_37.5": 0.45, "37.5_38.0": 0.25, "38.0_39.0": 0.20,
    "39.0_40.0": 0.08, "over_40.0": 0.02
}
n["E12"]["parent_effects"]["D106"] = {
    "absent": 0.50, "maculopapular_rash": 0.30, "diffuse_erythema": 0.15,
    "petechiae_purpura": 0.01, "vesicular": 0.01, "erythroderma": 0.03
}
n["S25"]["parent_effects"]["D106"] = {"absent": 0.65, "present": 0.35}
n["S08"]["parent_effects"]["D106"] = {"absent": 0.60, "present": 0.40}
n["S07"]["parent_effects"]["D106"] = {"absent": 0.25, "mild": 0.35, "severe": 0.40}
n["S06"]["parent_effects"]["D106"] = {"absent": 0.35, "present": 0.65}
n["L04"]["parent_effects"]["D106"] = {
    "normal": 0.60, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.25,
    "BHL": 0.01, "pleural_effusion": 0.05, "GGO": 0.04
}
n["L02"]["parent_effects"]["D106"] = {
    "normal_under_0.3": 0.25, "mild_0.3_3": 0.35, "moderate_3_10": 0.30, "high_over_10": 0.10
}
n["L28"]["parent_effects"]["D106"] = {"normal": 0.30, "elevated": 0.50, "very_high_over_100": 0.20}
n["L16"]["parent_effects"]["D106"] = {"normal": 0.20, "elevated": 0.80}
n["S17"]["parent_effects"]["D106"] = {"absent": 0.55, "present": 0.45}
n["T01"]["parent_effects"]["D106"] = {
    "under_3d": 0.02, "3d_to_1w": 0.08, "1w_to_3w": 0.30, "over_3w": 0.60
}
n["T02"]["parent_effects"]["D106"] = {"sudden_hours": 0.05, "gradual_days": 0.95}
n["L18"]["parent_effects"]["D106"] = {"negative": 0.30, "positive": 0.70}
n["E20"]["parent_effects"]["D106"] = {"absent": 0.70, "present": 0.30}

# Save
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D106 added: 17 edges, 17 CPTs, S48 new variable")
print(f"Total diseases: 106")
