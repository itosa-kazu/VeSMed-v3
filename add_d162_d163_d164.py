#!/usr/bin/env python3
"""Add D162 HUS + D163 Wernicke + D164 Chronic SDH."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D162 溶血性尿毒症症候群 (HUS) =====
s1["variables"].append({
    "id": "D162", "name": "HUS",
    "name_ja": "溶血性尿毒症症候群(HUS)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "三徴: MAHA(破砕赤血球)+血小板減少+急性腎障害。典型:EHEC(O157:H7)→血性下痢5-10日後。非典型:補体異常。TTPとの鑑別重要"
})
for to, reason in [
    ("L14", "HUS: 血小板減少(三徴, 90%+)"),
    ("L16", "HUS: LDH上昇(溶血, 90%+)"),
    ("S14", "HUS: 下痢(典型HUS:血性下痢が先行, 90%)"),
    ("E01", "HUS: 発熱(30-40%)"),
    ("E16", "HUS: 意識障害(神経症状, 20-30%)"),
    ("S13", "HUS: 嘔吐(50-60%)"),
    ("S12", "HUS: 腹痛(50-70%)"),
    ("E02", "HUS: 頻脈(脱水/貧血)"),
    ("L01", "HUS: WBC上昇"),
    ("E18", "HUS: 黄疸(溶血, 30-40%)"),
    ("T01", "HUS: 急性~亜急性"),
    ("T02", "HUS: 亜急性(下痢5-10日後)")]:
    s2["edges"].append({"from": "D162", "to": to, "from_name": "HUS", "to_name": to, "reason": reason})

n["L14"]["parent_effects"]["D162"] = {"normal": 0.03, "left_shift": 0.02, "atypical_lymphocytes": 0.00, "thrombocytopenia": 0.90, "eosinophilia": 0.00, "lymphocyte_predominant": 0.05}
n["L16"]["parent_effects"]["D162"] = {"normal": 0.05, "elevated": 0.95}
n["S14"]["parent_effects"]["D162"] = {"absent": 0.10, "watery": 0.20, "bloody": 0.70}
n["E01"]["parent_effects"]["D162"] = {"under_37.5": 0.55, "37.5_38.0": 0.15, "38.0_39.0": 0.18, "39.0_40.0": 0.10, "over_40.0": 0.02}
n["E16"]["parent_effects"]["D162"] = {"normal": 0.65, "confused": 0.25, "obtunded": 0.10}
n["S13"]["parent_effects"]["D162"] = {"absent": 0.35, "present": 0.65}
n["S12"]["parent_effects"]["D162"] = {"absent": 0.25, "epigastric": 0.10, "RUQ": 0.05, "RLQ": 0.05, "LLQ": 0.05, "suprapubic": 0.05, "diffuse": 0.45}
n["E02"]["parent_effects"]["D162"] = {"under_100": 0.25, "100_120": 0.45, "over_120": 0.30}
n["L01"]["parent_effects"]["D162"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.25, "high_10000_20000": 0.45, "very_high_over_20000": 0.27}
n["E18"]["parent_effects"]["D162"] = {"absent": 0.55, "present": 0.45}
n["T01"]["parent_effects"]["D162"] = {"under_3d": 0.25, "3d_to_1w": 0.45, "1w_to_3w": 0.25, "over_3w": 0.05}
n["T02"]["parent_effects"]["D162"] = {"sudden_hours": 0.20, "gradual_days": 0.80}
s3["full_cpts"]["D162"] = {"parents": ["R01"], "description": "HUS。小児に多いが成人もあり",
    "cpt": {"18_39": 0.001, "40_64": 0.001, "65_plus": 0.002}}

# ===== D163 ウェルニッケ脳症 (Wernicke Encephalopathy) =====
s1["variables"].append({
    "id": "D163", "name": "wernicke_encephalopathy",
    "name_ja": "ウェルニッケ脳症",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "ビタミンB1(チアミン)欠乏。三徴:意識障害+眼球運動障害+失調。アルコール依存/栄養不良/妊娠悪阻。ブドウ糖投与前にB1!"
})
for to, reason in [
    ("E16", "ウェルニッケ: 意識障害(三徴, 80-90%)"),
    ("S52", "ウェルニッケ: 眼球運動障害/失調(三徴, 30-50%が完全三徴)"),
    ("S07", "ウェルニッケ: 全身倦怠感"),
    ("E01", "ウェルニッケ: 低体温(30-40%)"),
    ("E02", "ウェルニッケ: 頻脈(自律神経障害)"),
    ("E03", "ウェルニッケ: 低血圧(自律神経障害)"),
    ("S13", "ウェルニッケ: 嘔気(栄養不良)"),
    ("T01", "ウェルニッケ: 亜急性~慢性"),
    ("T02", "ウェルニッケ: 亜急性(日~週)")]:
    s2["edges"].append({"from": "D163", "to": to, "from_name": "wernicke", "to_name": to, "reason": reason})

n["E16"]["parent_effects"]["D163"] = {"normal": 0.08, "confused": 0.55, "obtunded": 0.37}
n["S52"]["parent_effects"]["D163"] = {"absent": 0.30, "unilateral_weakness": 0.05, "bilateral": 0.65}
n["S07"]["parent_effects"]["D163"] = {"absent": 0.10, "mild": 0.30, "severe": 0.60}
n["E01"]["parent_effects"]["D163"] = {"under_37.5": 0.70, "37.5_38.0": 0.12, "38.0_39.0": 0.10, "39.0_40.0": 0.05, "over_40.0": 0.03}
n["E02"]["parent_effects"]["D163"] = {"under_100": 0.25, "100_120": 0.45, "over_120": 0.30}
n["E03"]["parent_effects"]["D163"] = {"normal_over_90": 0.45, "hypotension_under_90": 0.55}
n["S13"]["parent_effects"]["D163"] = {"absent": 0.40, "present": 0.60}
n["T01"]["parent_effects"]["D163"] = {"under_3d": 0.20, "3d_to_1w": 0.35, "1w_to_3w": 0.30, "over_3w": 0.15}
n["T02"]["parent_effects"]["D163"] = {"sudden_hours": 0.15, "gradual_days": 0.85}
s3["full_cpts"]["D163"] = {"parents": [], "description": "ウェルニッケ脳症。アルコール依存/栄養不良",
    "cpt": {"": 0.001}}

# ===== D164 慢性硬膜下血腫 (Chronic SDH) =====
s1["variables"].append({
    "id": "D164", "name": "chronic_SDH",
    "name_ja": "慢性硬膜下血腫",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "高齢者+頭部外傷歴(軽微でも)。1-3ヶ月後に進行性意識障害+片麻痺。認知症/脳卒中と誤診リスク。CT/MRIで三日月状血腫"
})
for to, reason in [
    ("E16", "慢性SDH: 意識障害(60-80%)"),
    ("S05", "慢性SDH: 頭痛(50-70%)"),
    ("S52", "慢性SDH: 片麻痺(30-50%)"),
    ("S53", "慢性SDH: 構音障害(20-30%)"),
    ("S07", "慢性SDH: 全身倦怠感"),
    ("T01", "慢性SDH: 亜急性~慢性(1-3ヶ月)"),
    ("T02", "慢性SDH: 緩徐進行")]:
    s2["edges"].append({"from": "D164", "to": to, "from_name": "chronic_SDH", "to_name": to, "reason": reason})

n["E16"]["parent_effects"]["D164"] = {"normal": 0.15, "confused": 0.50, "obtunded": 0.35}
n["S05"]["parent_effects"]["D164"] = {"absent": 0.20, "mild": 0.40, "severe": 0.40}
n["S52"]["parent_effects"]["D164"] = {"absent": 0.40, "unilateral_weakness": 0.55, "bilateral": 0.05}
n["S53"]["parent_effects"]["D164"] = {"absent": 0.65, "dysarthria": 0.30, "aphasia": 0.05}
n["S07"]["parent_effects"]["D164"] = {"absent": 0.20, "mild": 0.45, "severe": 0.35}
n["T01"]["parent_effects"]["D164"] = {"under_3d": 0.05, "3d_to_1w": 0.15, "1w_to_3w": 0.35, "over_3w": 0.45}
n["T02"]["parent_effects"]["D164"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
s3["full_cpts"]["D164"] = {"parents": ["R01", "R02"], "description": "慢性SDH。高齢男性に多い",
    "cpt": {"18_39,male": 0.0005, "18_39,female": 0.0002,
            "40_64,male": 0.001, "40_64,female": 0.0005,
            "65_plus,male": 0.004, "65_plus,female": 0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D162 HUS: 12 edges, D163 Wernicke: 9 edges, D164 cSDH: 7 edges")
print(f"Total: {s2['total_edges']} edges, 164 diseases")
