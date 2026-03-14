#!/usr/bin/env python3
"""Add D108 acute hepatitis B."""
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
    "id": "D108",
    "name": "acute_hepatitis_B",
    "name_ja": "B型急性肝炎",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "high",
    "note": "HBV急性感染。発熱+黄疸+肝酵素著増。劇症化リスクあり。性感染/血液感染"
})
print("step1: Added D108")

# step2: edges
# B型急性肝炎の臨床所見:
# - 発熱(38-39°C, 前駆期30-50%), 倦怠感(90%+), 食欲不振(80%+)
# - 嘔気嘔吐(60-80%), 黄疸(50-70%), 右上腹部痛(40-60%)
# - 肝腫大(30-50%), 関節痛(前駆期10-30%, 免疫複合体)
# - AST/ALT著増(>1000が多い), ビリルビン上昇
# - WBC正常〜低下, CRP軽度
# - 肝炎ウイルス検査: HBV(L39)
# - T01: 亜急性(1-4週の前駆期→黄疸期)
edges = [
    ("E01", "HBV急性: 前駆期発熱(30-50%)"),
    ("S07", "HBV急性: 倦怠感(90%+)"),
    ("S46", "HBV急性: 食欲不振(80%+)"),
    ("S13", "HBV急性: 嘔気嘔吐(60-80%)"),
    ("E18", "HBV急性: 黄疸(50-70%)"),
    ("S12", "HBV急性: 右上腹部痛(40-60%)"),
    ("E34", "HBV急性: 肝腫大(30-50%)"),
    ("S08", "HBV急性: 関節痛(前駆期10-30%, 免疫複合体)"),
    ("L11", "HBV急性: AST/ALT著増(通常>1000)"),
    ("L01", "HBV急性: WBC正常〜軽度低下"),
    ("L02", "HBV急性: CRP軽度上昇"),
    ("L39", "HBV急性: HBs抗原/IgM-HBc陽性"),
    ("T01", "HBV急性: 亜急性経過(前駆期1-4週→黄疸期)"),
    ("T02", "HBV急性: 緩徐発症"),
    ("S17", "HBV急性: 体重減少(30-40%)"),
    ("E12", "HBV急性: 皮疹(蕁麻疹/血管炎, 10-20%)"),
]
for to_id, reason in edges:
    s2["edges"].append({
        "from": "D108", "to": to_id,
        "from_name": "acute_hepatitis_B", "to_name": to_id,
        "reason": reason
    })
print(f"step2: Added {len(edges)} edges")

# step3: CPTs
n = s3["noisy_or_params"]

n["E01"]["parent_effects"]["D108"] = {
    "under_37.5": 0.40, "37.5_38.0": 0.30, "38.0_39.0": 0.20,
    "39.0_40.0": 0.08, "over_40.0": 0.02
}
n["S07"]["parent_effects"]["D108"] = {"absent": 0.05, "mild": 0.30, "severe": 0.65}
n["S46"]["parent_effects"]["D108"] = {"absent": 0.15, "present": 0.85}
n["S13"]["parent_effects"]["D108"] = {"absent": 0.30, "present": 0.70}
n["E18"]["parent_effects"]["D108"] = {"absent": 0.40, "present": 0.60}
n["S12"]["parent_effects"]["D108"] = {
    "absent": 0.45, "epigastric": 0.10, "RUQ": 0.40,
    "RLQ": 0.01, "LLQ": 0.01, "suprapubic": 0.01, "diffuse": 0.02
}
n["E34"]["parent_effects"]["D108"] = {"absent": 0.55, "present": 0.45}
n["S08"]["parent_effects"]["D108"] = {"absent": 0.75, "present": 0.25}
n["L11"]["parent_effects"]["D108"] = {"normal": 0.02, "mild_elevated": 0.08, "very_high": 0.90}
n["L01"]["parent_effects"]["D108"] = {
    "low_under_4000": 0.25, "normal_4000_10000": 0.60,
    "high_10000_20000": 0.12, "very_high_over_20000": 0.03
}
n["L02"]["parent_effects"]["D108"] = {
    "normal_under_0.3": 0.30, "mild_0.3_3": 0.45,
    "moderate_3_10": 0.20, "high_over_10": 0.05
}
# L39: HBV state
n["L39"]["parent_effects"]["D108"] = {
    "negative": 0.02, "HAV_IgM": 0.01, "HBV": 0.95, "HCV": 0.02
}
n["T01"]["parent_effects"]["D108"] = {
    "under_3d": 0.05, "3d_to_1w": 0.20, "1w_to_3w": 0.50, "over_3w": 0.25
}
n["T02"]["parent_effects"]["D108"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
n["S17"]["parent_effects"]["D108"] = {"absent": 0.60, "present": 0.40}
n["E12"]["parent_effects"]["D108"] = {
    "absent": 0.80, "maculopapular_rash": 0.10, "diffuse_erythema": 0.05,
    "petechiae_purpura": 0.02, "vesicular": 0.01, "erythroderma": 0.02
}
print(f"step3: Added {len(edges)} CPTs")

# Save
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("All saved. 108 diseases.")
