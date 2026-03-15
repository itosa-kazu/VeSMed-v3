#!/usr/bin/env python3
"""Add D160 Acute Aortic Occlusion + D161 Acute Pancreatitis (severe/necrotizing)."""
# Note: D86 already covers acute pancreatitis, but we should check if it exists
# Actually D86 IS acute pancreatitis. Let me add different diseases.
# D160: 破傷風 (Tetanus) - important infectious disease
# D161: 有機リン中毒 (Organophosphate poisoning)
"""Add D160 Tetanus + D161 Organophosphate Poisoning."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D160 破傷風 (Tetanus) =====
s1["variables"].append({
    "id": "D160", "name": "tetanus",
    "name_ja": "破傷風",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "C.tetani毒素(tetanospasmin)。開口障害(trismus)+全身痙攣(opisthotonus)+自律神経障害。外傷/創傷歴。ワクチン未接種者"
})
for to, reason in [
    ("S42", "破傷風: 痙攣(全身性強直間代, 80%+)"),
    ("E06", "破傷風: 項部硬直(全身筋強直)"),
    ("E01", "破傷風: 発熱(自律神経障害, 50-60%)"),
    ("E02", "破傷風: 頻脈(自律神経障害, 70-80%)"),
    ("E03", "破傷風: 血圧不安定(自律神経障害)"),
    ("E16", "破傷風: 意識障害(重症, 意識は通常保たれる)"),
    ("S07", "破傷風: 全身脱力(筋強直)"),
    ("L01", "破傷風: WBC(正常~軽度上昇)"),
    ("L17", "破傷風: CK上昇(筋強直/横紋筋融解)"),
    ("T01", "破傷風: 亜急性(潜伏7-14日)"),
    ("T02", "破傷風: 亜急性")]:
    s2["edges"].append({"from": "D160", "to": to, "from_name": "tetanus", "to_name": to, "reason": reason})

n["S42"]["parent_effects"]["D160"] = {"absent": 0.10, "present": 0.90}
n["E06"]["parent_effects"]["D160"] = {"absent": 0.15, "present": 0.85}
n["E01"]["parent_effects"]["D160"] = {"under_37.5": 0.35, "37.5_38.0": 0.20, "38.0_39.0": 0.25, "39.0_40.0": 0.15, "over_40.0": 0.05}
n["E02"]["parent_effects"]["D160"] = {"under_100": 0.15, "100_120": 0.40, "over_120": 0.45}
n["E03"]["parent_effects"]["D160"] = {"normal_over_90": 0.40, "hypotension_under_90": 0.60}
n["E16"]["parent_effects"]["D160"] = {"normal": 0.55, "confused": 0.30, "obtunded": 0.15}
n["S07"]["parent_effects"]["D160"] = {"absent": 0.15, "mild": 0.35, "severe": 0.50}
n["L01"]["parent_effects"]["D160"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.45, "high_10000_20000": 0.40, "very_high_over_20000": 0.12}
n["L17"]["parent_effects"]["D160"] = {"normal": 0.25, "elevated": 0.50, "very_high": 0.25}
n["T01"]["parent_effects"]["D160"] = {"under_3d": 0.15, "3d_to_1w": 0.40, "1w_to_3w": 0.40, "over_3w": 0.05}
n["T02"]["parent_effects"]["D160"] = {"sudden_hours": 0.15, "gradual_days": 0.85}
s3["full_cpts"]["D160"] = {"parents": [], "description": "破傷風。創傷歴+ワクチン未接種",
    "cpt": {"": 0.001}}

# ===== D161 有機リン中毒 (Organophosphate Poisoning) =====
s1["variables"].append({
    "id": "D161", "name": "organophosphate_poisoning",
    "name_ja": "有機リン中毒",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "コリンエステラーゼ阻害。SLUDGE(唾液分泌↑/流涙/排尿/下痢/消化管症状/眼(縮瞳))+気管支痙攣+徐脈+痙攣。農薬/殺虫剤暴露"
})
for to, reason in [
    ("S13", "有機リン: 嘔吐(ムスカリン作用, 80%+)"),
    ("S14", "有機リン: 下痢(ムスカリン作用, 70-80%)"),
    ("S04", "有機リン: 呼吸困難(気管支痙攣/分泌物, 60-70%)"),
    ("E02", "有機リン: 徐脈(ムスカリン)/頻脈(ニコチン)"),
    ("E03", "有機リン: 低血圧"),
    ("E16", "有機リン: 意識障害(重症, 40-60%)"),
    ("S42", "有機リン: 痙攣(重症, 20-30%)"),
    ("S07", "有機リン: 全身脱力(ニコチン作用, 60-70%)"),
    ("E07", "有機リン: 肺聴診(湿性ラ音/wheeze, 分泌物)"),
    ("T01", "有機リン: 超急性"),
    ("T02", "有機リン: 急性(暴露後30分~数時間)")]:
    s2["edges"].append({"from": "D161", "to": to, "from_name": "organophosphate", "to_name": to, "reason": reason})

n["S13"]["parent_effects"]["D161"] = {"absent": 0.10, "present": 0.90}
n["S14"]["parent_effects"]["D161"] = {"absent": 0.20, "watery": 0.75, "bloody": 0.05}
n["S04"]["parent_effects"]["D161"] = {"absent": 0.20, "on_exertion": 0.30, "at_rest": 0.50}
n["E02"]["parent_effects"]["D161"] = {"under_100": 0.50, "100_120": 0.30, "over_120": 0.20}
n["E03"]["parent_effects"]["D161"] = {"normal_over_90": 0.35, "hypotension_under_90": 0.65}
n["E16"]["parent_effects"]["D161"] = {"normal": 0.30, "confused": 0.35, "obtunded": 0.35}
n["S42"]["parent_effects"]["D161"] = {"absent": 0.70, "present": 0.30}
n["S07"]["parent_effects"]["D161"] = {"absent": 0.15, "mild": 0.30, "severe": 0.55}
n["E07"]["parent_effects"]["D161"] = {"clear": 0.15, "crackles": 0.35, "wheezes": 0.40, "decreased_absent": 0.10}
n["T01"]["parent_effects"]["D161"] = {"under_3d": 0.90, "3d_to_1w": 0.08, "1w_to_3w": 0.02, "over_3w": 0.00}
n["T02"]["parent_effects"]["D161"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
s3["full_cpts"]["D161"] = {"parents": [], "description": "有機リン中毒。農薬暴露",
    "cpt": {"": 0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D160 Tetanus: 11 edges, D161 OP poisoning: 11 edges")
print(f"Total: {s2['total_edges']} edges, 161 diseases")
