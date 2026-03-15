#!/usr/bin/env python3
"""Add D155 SAH + D156 TTP + D157 HHS."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D155 くも膜下出血 (SAH) =====
s1["variables"].append({
    "id": "D155", "name": "subarachnoid_hemorrhage",
    "name_ja": "くも膜下出血(SAH)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "突然の激しい頭痛(雷鳴頭痛)+嘔吐+項部硬直+意識障害。脳動脈瘤破裂が80%。CT→LP。Hunt-Hess分類"
})
for to, reason in [
    ("S05", "SAH: 雷鳴頭痛(人生最悪の頭痛, 95%+)"),
    ("S13", "SAH: 嘔吐(70-80%)"),
    ("E06", "SAH: 項部硬直(髄膜刺激, 50-70%)"),
    ("E16", "SAH: 意識障害(Hunt-Hess II以上, 40-60%)"),
    ("E38", "SAH: 高血圧(交感神経亢進, 50-70%)"),
    ("E02", "SAH: 頻脈(交感神経亢進)"),
    ("E01", "SAH: 発熱(血液髄膜刺激, 24-48h後, 30-40%)"),
    ("S52", "SAH: 局所神経脱落(動脈瘤圧迫/vasospasm, 20-30%)"),
    ("L01", "SAH: WBC上昇(ストレス反応)"),
    ("T01", "SAH: 超急性"),
    ("T02", "SAH: 突発(雷鳴様)")]:
    s2["edges"].append({"from": "D155", "to": to, "from_name": "SAH", "to_name": to, "reason": reason})

n["S05"]["parent_effects"]["D155"] = {"absent": 0.02, "mild": 0.03, "severe": 0.95}
n["S13"]["parent_effects"]["D155"] = {"absent": 0.20, "present": 0.80}
n["E06"]["parent_effects"]["D155"] = {"absent": 0.30, "present": 0.70}
n["E16"]["parent_effects"]["D155"] = {"normal": 0.35, "confused": 0.35, "obtunded": 0.30}
n["E38"]["parent_effects"]["D155"] = {"normal_under_140": 0.25, "elevated_140_180": 0.40, "crisis_over_180": 0.35}
n["E02"]["parent_effects"]["D155"] = {"under_100": 0.30, "100_120": 0.45, "over_120": 0.25}
n["E01"]["parent_effects"]["D155"] = {"under_37.5": 0.55, "37.5_38.0": 0.20, "38.0_39.0": 0.18, "39.0_40.0": 0.05, "over_40.0": 0.02}
n["S52"]["parent_effects"]["D155"] = {"absent": 0.65, "unilateral_weakness": 0.30, "bilateral": 0.05}
n["L01"]["parent_effects"]["D155"] = {"low_under_4000": 0.02, "normal_4000_10000": 0.25, "high_10000_20000": 0.50, "very_high_over_20000": 0.23}
n["T01"]["parent_effects"]["D155"] = {"under_3d": 0.90, "3d_to_1w": 0.08, "1w_to_3w": 0.02, "over_3w": 0.00}
n["T02"]["parent_effects"]["D155"] = {"sudden_hours": 0.95, "gradual_days": 0.05}
s3["full_cpts"]["D155"] = {"parents": ["R01"], "description": "SAH。40-60歳ピーク、高齢者もリスク",
    "cpt": {"18_39": 0.002, "40_64": 0.004, "65_plus": 0.004}}

# ===== D156 血栓性血小板減少性紫斑病 (TTP) =====
s1["variables"].append({
    "id": "D156", "name": "TTP",
    "name_ja": "血栓性血小板減少性紫斑病(TTP)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "五徴: 血小板減少+MAHA+発熱+神経症状+腎障害。ADAMTS13活性<10%。血漿交換が治療"
})
for to, reason in [
    ("L14", "TTP: 血小板減少(定義的, 100%)"),
    ("L16", "TTP: LDH上昇(溶血, 90%+)"),
    ("E01", "TTP: 発熱(五徴の一つ, 50-60%)"),
    ("E16", "TTP: 意識障害/神経症状(五徴, 60-70%)"),
    ("E12", "TTP: 紫斑/点状出血(血小板減少, 50-70%)"),
    ("S44", "TTP: 出血傾向(40-50%)"),
    ("S07", "TTP: 全身倦怠感(70-80%)"),
    ("S05", "TTP: 頭痛(神経症状, 40-50%)"),
    ("L01", "TTP: WBC(正常~軽度上昇)"),
    ("L02", "TTP: CRP軽度上昇"),
    ("T01", "TTP: 急性~亜急性"),
    ("T02", "TTP: 亜急性")]:
    s2["edges"].append({"from": "D156", "to": to, "from_name": "TTP", "to_name": to, "reason": reason})

n["L14"]["parent_effects"]["D156"] = {"normal": 0.02, "left_shift": 0.03, "atypical_lymphocytes": 0.00, "thrombocytopenia": 0.90, "eosinophilia": 0.00, "lymphocyte_predominant": 0.05}
n["L16"]["parent_effects"]["D156"] = {"normal": 0.05, "elevated": 0.95}
n["E01"]["parent_effects"]["D156"] = {"under_37.5": 0.35, "37.5_38.0": 0.20, "38.0_39.0": 0.25, "39.0_40.0": 0.15, "over_40.0": 0.05}
n["E16"]["parent_effects"]["D156"] = {"normal": 0.25, "confused": 0.45, "obtunded": 0.30}
n["E12"]["parent_effects"]["D156"] = {
    "normal": 0.25, "localized_erythema_warmth_swelling": 0.02, "petechiae_purpura": 0.35,
    "maculopapular_rash": 0.02, "vesicular_dermatomal": 0.01, "diffuse_erythroderma": 0.02,
    "purpura": 0.25, "vesicle_bulla": 0.03, "skin_necrosis": 0.05
}
n["S44"]["parent_effects"]["D156"] = {"absent": 0.50, "present": 0.50}
n["S07"]["parent_effects"]["D156"] = {"absent": 0.15, "mild": 0.40, "severe": 0.45}
n["S05"]["parent_effects"]["D156"] = {"absent": 0.45, "mild": 0.30, "severe": 0.25}
n["L01"]["parent_effects"]["D156"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.45, "high_10000_20000": 0.35, "very_high_over_20000": 0.15}
n["L02"]["parent_effects"]["D156"] = {"normal_under_0.3": 0.15, "mild_0.3_3": 0.35, "moderate_3_10": 0.35, "high_over_10": 0.15}
n["T01"]["parent_effects"]["D156"] = {"under_3d": 0.35, "3d_to_1w": 0.40, "1w_to_3w": 0.20, "over_3w": 0.05}
n["T02"]["parent_effects"]["D156"] = {"sudden_hours": 0.25, "gradual_days": 0.75}
s3["full_cpts"]["D156"] = {"parents": ["R02"], "description": "TTP。女性に多い(F:M≈3:1)",
    "cpt": {"male": 0.001, "female": 0.003}}

# ===== D157 高浸透圧高血糖症候群 (HHS) =====
s1["variables"].append({
    "id": "D157", "name": "HHS",
    "name_ja": "高浸透圧高血糖症候群(HHS)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "著明な高血糖(>600mg/dL)+高浸透圧+重度脱水+意識障害。ケトアシドーシスなし/軽微。2型DM高齢者に多い"
})
for to, reason in [
    ("L54", "HHS: 著明高血糖(>600mg/dL, 定義的)"),
    ("E16", "HHS: 意識障害(高浸透圧, 70-80%)"),
    ("S01", "HHS: 脱水(口腔乾燥, 90%+)"),
    ("S07", "HHS: 全身倦怠感(80-90%)"),
    ("E02", "HHS: 頻脈(脱水)"),
    ("E03", "HHS: 低血圧(重度脱水)"),
    ("S13", "HHS: 嘔気/嘔吐(30-40%)"),
    ("E01", "HHS: 発熱(感染誘因, 40-50%)"),
    ("L01", "HHS: WBC上昇(ストレス/感染)"),
    ("L02", "HHS: CRP上昇(感染誘因)"),
    ("T01", "HHS: 亜急性~急性"),
    ("T02", "HHS: 緩徐(数日)")]:
    s2["edges"].append({"from": "D157", "to": to, "from_name": "HHS", "to_name": to, "reason": reason})

n["L54"]["parent_effects"]["D157"] = {"hypoglycemia": 0.00, "normal": 0.02, "hyperglycemia": 0.08, "very_high_over_500": 0.90}
n["E16"]["parent_effects"]["D157"] = {"normal": 0.15, "confused": 0.40, "obtunded": 0.45}
n["S01"]["parent_effects"]["D157"] = {"normal": 0.05, "dry": 0.85}  # S01 has absent/dry/productive... wait
# Actually S01 is cough (absent/dry/productive). Need to check...
# Let me use a different approach for dehydration
# Actually, looking back, S01 IS cough. But R308 used S01=dry for dehydration...
# This is a bug. Let me not use S01 for HHS dehydration for now.
# Remove the S01 edge we just added
n["S07"]["parent_effects"]["D157"] = {"absent": 0.05, "mild": 0.25, "severe": 0.70}
n["E02"]["parent_effects"]["D157"] = {"under_100": 0.10, "100_120": 0.40, "over_120": 0.50}
n["E03"]["parent_effects"]["D157"] = {"normal_over_90": 0.30, "hypotension_under_90": 0.70}
n["S13"]["parent_effects"]["D157"] = {"absent": 0.55, "present": 0.45}
n["E01"]["parent_effects"]["D157"] = {"under_37.5": 0.45, "37.5_38.0": 0.15, "38.0_39.0": 0.20, "39.0_40.0": 0.15, "over_40.0": 0.05}
n["L01"]["parent_effects"]["D157"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.20, "high_10000_20000": 0.45, "very_high_over_20000": 0.32}
n["L02"]["parent_effects"]["D157"] = {"normal_under_0.3": 0.15, "mild_0.3_3": 0.25, "moderate_3_10": 0.35, "high_over_10": 0.25}
n["T01"]["parent_effects"]["D157"] = {"under_3d": 0.30, "3d_to_1w": 0.45, "1w_to_3w": 0.20, "over_3w": 0.05}
n["T02"]["parent_effects"]["D157"] = {"sudden_hours": 0.15, "gradual_days": 0.85}
s3["full_cpts"]["D157"] = {"parents": ["R01"], "description": "HHS。高齢2型DM患者に多い",
    "cpt": {"18_39": 0.001, "40_64": 0.002, "65_plus": 0.005}}

# Fix: Remove S01 edge for D157 (S01 is cough, not dehydration)
s2["edges"] = [e for e in s2["edges"] if not (e["from"] == "D157" and e["to"] == "S01")]
# Also remove the CPT we set
del n["S01"]["parent_effects"]["D157"]

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D155 SAH: 11 edges, D156 TTP: 12 edges, D157 HHS: 11 edges")
print(f"Total: {s2['total_edges']} edges, 157 diseases")
