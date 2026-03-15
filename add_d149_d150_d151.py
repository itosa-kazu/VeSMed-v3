#!/usr/bin/env python3
"""Add D149 CO Poisoning + D150 Takotsubo + D151 Acute Liver Failure."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D149 CO Poisoning =====
s1["variables"].append({
    "id": "D149", "name": "carbon_monoxide_poisoning",
    "name_ja": "一酸化炭素中毒",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "頭痛+嘔気+意識障害。SpO2偽正常(パルスオキシメータはCOHbを区別できない)。COHb測定で確定。高濃度O2/HBO治療"
})
for to, reason in [
    ("S05", "CO中毒: 頭痛(90%+, 最多症状)"), ("S13", "CO中毒: 嘔気嘔吐(50-70%)"),
    ("E16", "CO中毒: 意識障害(重症で)"), ("S42", "CO中毒: 痙攣(重症で)"),
    ("S07", "CO中毒: 倦怠感/脱力(60-80%)"), ("E02", "CO中毒: 頻脈(50-60%)"),
    ("S21", "CO中毒: 胸痛(心筋虚血20-30%)"),
    ("E01", "CO中毒: 通常無熱"), ("L01", "CO中毒: WBC正常~軽度上昇"),
    ("L53", "CO中毒: トロポニン上昇(心筋障害20-30%)"),
    ("T01", "CO中毒: 超急性(曝露時間に依存)"), ("T02", "CO中毒: 急性発症")]:
    s2["edges"].append({"from": "D149", "to": to, "from_name": "carbon_monoxide_poisoning", "to_name": to, "reason": reason})

n["S05"]["parent_effects"]["D149"] = {"absent": 0.05, "mild": 0.25, "severe": 0.70}
n["S13"]["parent_effects"]["D149"] = {"absent": 0.25, "present": 0.75}
n["E16"]["parent_effects"]["D149"] = {"normal": 0.30, "confused": 0.40, "obtunded": 0.30}
n["S42"]["parent_effects"]["D149"] = {"absent": 0.80, "present": 0.20}
n["S07"]["parent_effects"]["D149"] = {"absent": 0.10, "mild": 0.30, "severe": 0.60}
n["E02"]["parent_effects"]["D149"] = {"under_100": 0.30, "100_120": 0.50, "over_120": 0.20}
n["S21"]["parent_effects"]["D149"] = {"absent": 0.65, "burning": 0.05, "sharp": 0.05, "pressure": 0.20, "tearing": 0.05}
n["E01"]["parent_effects"]["D149"] = {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D149"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.60, "high_10000_20000": 0.30, "very_high_over_20000": 0.07}
n["L53"]["parent_effects"]["D149"] = {"not_done": 0.20, "normal": 0.40, "mildly_elevated": 0.30, "very_high": 0.10}
n["T01"]["parent_effects"]["D149"] = {"under_3d": 0.95, "3d_to_1w": 0.04, "1w_to_3w": 0.01, "over_3w": 0.00}
n["T02"]["parent_effects"]["D149"] = {"sudden_hours": 0.80, "gradual_days": 0.20}
s3["full_cpts"]["D149"] = {"parents": [], "description": "CO中毒", "cpt": {"": 0.002}}

# ===== D150 Takotsubo =====
s1["variables"].append({
    "id": "D150", "name": "takotsubo_cardiomyopathy",
    "name_ja": "たこつぼ心筋症",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "ストレス誘発性心筋症。ACS様の胸痛+ST上昇+トロポニン軽度上昇。冠動脈正常。心尖部バルーニング。閉経後女性に多い"
})
for to, reason in [
    ("S21", "たこつぼ: 胸痛(80%+, ACS様)"), ("S04", "たこつぼ: 呼吸困難(40-60%)"),
    ("S50", "たこつぼ: 胸痛誘発(ストレス後)"), ("S51", "たこつぼ: 放散(左腕等, ACS様)"),
    ("E02", "たこつぼ: 頻脈(40-50%)"), ("E03", "たこつぼ: 低血圧(ショック5-10%)"),
    ("L53", "たこつぼ: トロポニン軽度上昇(ACSより低い)"),
    ("L51", "たこつぼ: BNP上昇(心不全)"), ("L17", "たこつぼ: CK軽度上昇"),
    ("E01", "たこつぼ: 通常無熱"), ("L01", "たこつぼ: WBC正常~軽度上昇"),
    ("T01", "たこつぼ: 超急性"), ("T02", "たこつぼ: 突然発症")]:
    s2["edges"].append({"from": "D150", "to": to, "from_name": "takotsubo_cardiomyopathy", "to_name": to, "reason": reason})

n["S21"]["parent_effects"]["D150"] = {"absent": 0.10, "burning": 0.05, "sharp": 0.10, "pressure": 0.65, "tearing": 0.10}
n["S04"]["parent_effects"]["D150"] = {"absent": 0.35, "on_exertion": 0.25, "at_rest": 0.40}
n["S50"]["parent_effects"]["D150"] = {"not_applicable": 0.10, "none": 0.40, "exertion": 0.15, "breathing": 0.05, "position": 0.05, "meals": 0.25}
n["S51"]["parent_effects"]["D150"] = {"not_applicable": 0.10, "none": 0.50, "left_arm_jaw": 0.30, "back": 0.10}
n["E02"]["parent_effects"]["D150"] = {"under_100": 0.35, "100_120": 0.45, "over_120": 0.20}
n["E03"]["parent_effects"]["D150"] = {"normal_over_90": 0.85, "hypotension_under_90": 0.15}
n["L53"]["parent_effects"]["D150"] = {"not_done": 0.10, "normal": 0.10, "mildly_elevated": 0.60, "very_high": 0.20}
n["L51"]["parent_effects"]["D150"] = {"not_done": 0.15, "normal": 0.10, "mildly_elevated": 0.30, "very_high": 0.45}
n["L17"]["parent_effects"]["D150"] = {"normal": 0.40, "elevated": 0.45, "very_high": 0.15}
n["E01"]["parent_effects"]["D150"] = {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D150"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.55, "high_10000_20000": 0.35, "very_high_over_20000": 0.07}
n["T01"]["parent_effects"]["D150"] = {"under_3d": 0.85, "3d_to_1w": 0.12, "1w_to_3w": 0.03, "over_3w": 0.00}
n["T02"]["parent_effects"]["D150"] = {"sudden_hours": 0.80, "gradual_days": 0.20}
s3["full_cpts"]["D150"] = {"parents": ["R01"], "description": "たこつぼ。閉経後女性に多い",
    "cpt": {"18_39": 0.001, "40_64": 0.003, "65_plus": 0.005}}

# ===== D151 Acute Liver Failure =====
s1["variables"].append({
    "id": "D151", "name": "acute_liver_failure",
    "name_ja": "急性肝不全（劇症肝炎）",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "急性肝障害+肝性脳症+凝固障害。AST/ALT著高+黄疸+PT延長。ウイルス/薬剤/自己免疫。肝移植が必要なことも"
})
for to, reason in [
    ("E18", "急性肝不全: 黄疸(80%+)"), ("E16", "急性肝不全: 意識障害/肝性脳症(50-70%)"),
    ("L11", "急性肝不全: AST/ALT著高(>1000)"), ("S13", "急性肝不全: 嘔気嘔吐(60-70%)"),
    ("S07", "急性肝不全: 倦怠感(80%+)"), ("S12", "急性肝不全: 腹痛(右季肋部, 30-40%)"),
    ("E01", "急性肝不全: 発熱(ウイルス性で30-40%)"),
    ("L01", "急性肝不全: WBC正常~上昇"), ("L02", "急性肝不全: CRP軽度~中等度"),
    ("E34", "急性肝不全: 肝腫大(急性期)→縮小(壊死期)"),
    ("T01", "急性肝不全: 急性~亜急性(数日~数週)"), ("T02", "急性肝不全: 急性~亜急性")]:
    s2["edges"].append({"from": "D151", "to": to, "from_name": "acute_liver_failure", "to_name": to, "reason": reason})

n["E18"]["parent_effects"]["D151"] = {"absent": 0.10, "present": 0.90}
n["E16"]["parent_effects"]["D151"] = {"normal": 0.25, "confused": 0.40, "obtunded": 0.35}
n["L11"]["parent_effects"]["D151"] = {"normal": 0.02, "mild_elevated": 0.08, "very_high": 0.90}
n["S13"]["parent_effects"]["D151"] = {"absent": 0.25, "present": 0.75}
n["S07"]["parent_effects"]["D151"] = {"absent": 0.05, "mild": 0.20, "severe": 0.75}
n["S12"]["parent_effects"]["D151"] = {"absent": 0.55, "epigastric": 0.05, "RUQ": 0.30, "RLQ": 0.02, "LLQ": 0.02, "suprapubic": 0.01, "diffuse": 0.05}
n["E01"]["parent_effects"]["D151"] = {"under_37.5": 0.40, "37.5_38.0": 0.25, "38.0_39.0": 0.20, "39.0_40.0": 0.12, "over_40.0": 0.03}
n["L01"]["parent_effects"]["D151"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.40, "high_10000_20000": 0.40, "very_high_over_20000": 0.15}
n["L02"]["parent_effects"]["D151"] = {"normal_under_0.3": 0.15, "mild_0.3_3": 0.25, "moderate_3_10": 0.35, "high_over_10": 0.25}
n["E34"]["parent_effects"]["D151"] = {"absent": 0.40, "present": 0.60}
n["T01"]["parent_effects"]["D151"] = {"under_3d": 0.25, "3d_to_1w": 0.40, "1w_to_3w": 0.30, "over_3w": 0.05}
n["T02"]["parent_effects"]["D151"] = {"sudden_hours": 0.30, "gradual_days": 0.70}
s3["full_cpts"]["D151"] = {"parents": [], "description": "急性肝不全", "cpt": {"": 0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D149: 12 edges, D150: 13 edges, D151: 12 edges")
print(f"Total: {s2['total_edges']} edges, 151 diseases")
