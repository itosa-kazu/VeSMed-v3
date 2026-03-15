#!/usr/bin/env python3
"""Phase 4: Add consciousness differential diseases + new variables.

New variables:
  L54: blood glucose (hypoglycemia/normal/hyperglycemia/very_high)
  S52: focal neurological deficit (absent/unilateral_weakness/bilateral)
  S53: speech disturbance (absent/dysarthria/aphasia)

New diseases:
  D138: acute ischemic stroke (急性脳梗塞)
  D139: intracerebral hemorrhage (脳出血)
  D140: diabetic ketoacidosis (DKA)
  D141: hypoglycemia (低血糖)
  D142: status epilepticus (てんかん重積)
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== New Variables =====
s1["variables"].extend([
    {"id": "L54", "name": "blood_glucose", "name_ja": "血糖値",
     "category": "lab", "states": ["hypoglycemia", "normal", "hyperglycemia", "very_high_over_500"],
     "note": "低血糖<70mg/dL, 正常70-140, 高血糖140-500, 著高>500(DKA/HHS)"},
    {"id": "S52", "name": "focal_neuro_deficit", "name_ja": "局所神経症状（片麻痺）",
     "category": "symptom", "states": ["absent", "unilateral_weakness", "bilateral"],
     "note": "片側運動麻痺/感覚障害。脳梗塞/脳出血に特異的"},
    {"id": "S53", "name": "speech_disturbance", "name_ja": "構音障害/失語",
     "category": "symptom", "states": ["absent", "dysarthria", "aphasia"],
     "note": "構音障害(小脳/脳幹), 失語(左大脳半球)。脳卒中に特異的"},
])

# ===== New noisy_or entries =====
n["L54"] = {
    "description": "血糖値。DKA/HHSで著高、低血糖で低値",
    "leak": {"hypoglycemia": 0.02, "normal": 0.90, "hyperglycemia": 0.06, "very_high_over_500": 0.02},
    "parent_effects": {}
}
n["S52"] = {
    "description": "局所神経症状。脳卒中に特異的",
    "leak": {"absent": 0.95, "unilateral_weakness": 0.03, "bilateral": 0.02},
    "parent_effects": {}
}
n["S53"] = {
    "description": "構音障害/失語。脳卒中に特異的",
    "leak": {"absent": 0.95, "dysarthria": 0.03, "aphasia": 0.02},
    "parent_effects": {}
}

# ===== D138 Acute Ischemic Stroke =====
s1["variables"].append({
    "id": "D138", "name": "acute_ischemic_stroke", "name_ja": "急性脳梗塞",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "突然の局所神経症状(片麻痺/失語)。tPA(4.5h以内)/血栓回収術。AF既往が塞栓リスク"
})
d138_edges = [
    ("S52", "脳梗塞: 片麻痺(70-80%)"), ("S53", "脳梗塞: 構音障害/失語(40-60%)"),
    ("E16", "脳梗塞: 意識障害(30-50%)"), ("S05", "脳梗塞: 頭痛(20-30%)"),
    ("S42", "脳梗塞: 痙攣(5-10%)"), ("E02", "脳梗塞: 頻脈/徐脈(変動)"),
    ("S13", "脳梗塞: 嘔気嘔吐(20-30%)"), ("E01", "脳梗塞: 通常無熱"),
    ("L01", "脳梗塞: WBC通常正常~軽度上昇"), ("L02", "脳梗塞: CRP通常正常"),
    ("L54", "脳梗塞: 血糖正常(ストレス高血糖もあり)"),
    ("T01", "脳梗塞: 超急性"), ("T02", "脳梗塞: 突然発症"),
]
for to, reason in d138_edges:
    s2["edges"].append({"from": "D138", "to": to, "from_name": "acute_ischemic_stroke", "to_name": to, "reason": reason})

n["S52"]["parent_effects"]["D138"] = {"absent": 0.15, "unilateral_weakness": 0.80, "bilateral": 0.05}
n["S53"]["parent_effects"]["D138"] = {"absent": 0.35, "dysarthria": 0.30, "aphasia": 0.35}
n["E16"]["parent_effects"]["D138"] = {"normal": 0.45, "confused": 0.35, "obtunded": 0.20}
n["S05"]["parent_effects"]["D138"] = {"absent": 0.65, "mild": 0.20, "severe": 0.15}
n["S42"]["parent_effects"]["D138"] = {"absent": 0.90, "present": 0.10}
n["E02"]["parent_effects"]["D138"] = {"under_100": 0.50, "100_120": 0.35, "over_120": 0.15}
n["S13"]["parent_effects"]["D138"] = {"absent": 0.70, "present": 0.30}
n["E01"]["parent_effects"]["D138"] = {"under_37.5": 0.75, "37.5_38.0": 0.15, "38.0_39.0": 0.08, "39.0_40.0": 0.02, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D138"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.60, "high_10000_20000": 0.30, "very_high_over_20000": 0.07}
n["L02"]["parent_effects"]["D138"] = {"normal_under_0.3": 0.50, "mild_0.3_3": 0.30, "moderate_3_10": 0.15, "high_over_10": 0.05}
n["L54"]["parent_effects"]["D138"] = {"hypoglycemia": 0.02, "normal": 0.55, "hyperglycemia": 0.38, "very_high_over_500": 0.05}
n["T01"]["parent_effects"]["D138"] = {"under_3d": 0.90, "3d_to_1w": 0.08, "1w_to_3w": 0.02, "over_3w": 0.00}
n["T02"]["parent_effects"]["D138"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
s3["full_cpts"]["D138"] = {"parents": ["R48", "R01"], "description": "脳梗塞。AF+高齢がリスク",
    "cpt": {"no|18_39": 0.002, "no|40_64": 0.005, "no|65_plus": 0.010,
            "yes|18_39": 0.008, "yes|40_64": 0.015, "yes|65_plus": 0.030}}

# ===== D139 Intracerebral Hemorrhage =====
s1["variables"].append({
    "id": "D139", "name": "intracerebral_hemorrhage", "name_ja": "脳出血",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "突然の頭痛+嘔吐+意識障害+片麻痺。高血圧が最大リスク。CTで高吸収域"
})
d139_edges = [
    ("S05", "脳出血: 突然の激しい頭痛(60-70%)"), ("S13", "脳出血: 嘔吐(50-60%)"),
    ("E16", "脳出血: 意識障害(50-70%)"), ("S52", "脳出血: 片麻痺(60-70%)"),
    ("S53", "脳出血: 構音障害/失語(30-40%)"), ("S42", "脳出血: 痙攣(10-20%)"),
    ("E02", "脳出血: 頻脈/徐脈"), ("E01", "脳出血: 通常無熱(中枢性発熱あり)"),
    ("L01", "脳出血: WBC上昇(ストレス)"), ("L54", "脳出血: 血糖(ストレス高血糖)"),
    ("T01", "脳出血: 超急性"), ("T02", "脳出血: 突然発症"),
]
for to, reason in d139_edges:
    s2["edges"].append({"from": "D139", "to": to, "from_name": "intracerebral_hemorrhage", "to_name": to, "reason": reason})

n["S05"]["parent_effects"]["D139"] = {"absent": 0.20, "mild": 0.15, "severe": 0.65}
n["S13"]["parent_effects"]["D139"] = {"absent": 0.35, "present": 0.65}
n["E16"]["parent_effects"]["D139"] = {"normal": 0.20, "confused": 0.30, "obtunded": 0.50}
n["S52"]["parent_effects"]["D139"] = {"absent": 0.25, "unilateral_weakness": 0.65, "bilateral": 0.10}
n["S53"]["parent_effects"]["D139"] = {"absent": 0.55, "dysarthria": 0.25, "aphasia": 0.20}
n["S42"]["parent_effects"]["D139"] = {"absent": 0.80, "present": 0.20}
n["E02"]["parent_effects"]["D139"] = {"under_100": 0.40, "100_120": 0.40, "over_120": 0.20}
n["E01"]["parent_effects"]["D139"] = {"under_37.5": 0.65, "37.5_38.0": 0.20, "38.0_39.0": 0.12, "39.0_40.0": 0.03, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D139"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.40, "high_10000_20000": 0.40, "very_high_over_20000": 0.17}
n["L54"]["parent_effects"]["D139"] = {"hypoglycemia": 0.02, "normal": 0.45, "hyperglycemia": 0.45, "very_high_over_500": 0.08}
n["T01"]["parent_effects"]["D139"] = {"under_3d": 0.90, "3d_to_1w": 0.08, "1w_to_3w": 0.02, "over_3w": 0.00}
n["T02"]["parent_effects"]["D139"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
s3["full_cpts"]["D139"] = {"parents": ["R01"], "description": "脳出血。高齢+高血圧がリスク",
    "cpt": {"18_39": 0.002, "40_64": 0.005, "65_plus": 0.010}}

# ===== D140 DKA =====
s1["variables"].append({
    "id": "D140", "name": "diabetic_ketoacidosis", "name_ja": "糖尿病性ケトアシドーシス(DKA)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "高血糖+代謝性アシドーシス+ケトン体上昇。Kussmaul呼吸+脱水+意識障害"
})
d140_edges = [
    ("L54", "DKA: 血糖著高(>500mg/dL)"), ("S13", "DKA: 嘔気嘔吐(60-80%)"),
    ("S12", "DKA: 腹痛(40-60%)"), ("E16", "DKA: 意識障害(30-50%)"),
    ("E04", "DKA: Kussmaul呼吸(頻呼吸+深呼吸, 60-80%)"),
    ("S04", "DKA: 呼吸困難(代償性過換気)"), ("E02", "DKA: 頻脈(脱水)"),
    ("E03", "DKA: 低血圧(脱水で30-40%)"), ("S07", "DKA: 倦怠感(80%+)"),
    ("E01", "DKA: 発熱(感染誘因なら)"), ("L01", "DKA: WBC上昇(ストレス/感染)"),
    ("L02", "DKA: CRP(感染合併で上昇)"),
    ("T01", "DKA: 急性(数時間~1日)"), ("T02", "DKA: 急性~亜急性"),
]
for to, reason in d140_edges:
    s2["edges"].append({"from": "D140", "to": to, "from_name": "diabetic_ketoacidosis", "to_name": to, "reason": reason})

n["L54"]["parent_effects"]["D140"] = {"hypoglycemia": 0.01, "normal": 0.02, "hyperglycemia": 0.22, "very_high_over_500": 0.75}
n["S13"]["parent_effects"]["D140"] = {"absent": 0.20, "present": 0.80}
n["S12"]["parent_effects"]["D140"] = {"absent": 0.40, "epigastric": 0.15, "RUQ": 0.05, "RLQ": 0.03, "LLQ": 0.02, "suprapubic": 0.02, "diffuse": 0.33}
n["E16"]["parent_effects"]["D140"] = {"normal": 0.40, "confused": 0.35, "obtunded": 0.25}
n["E04"]["parent_effects"]["D140"] = {"normal_under_20": 0.10, "tachypnea_20_30": 0.45, "severe_over_30": 0.45}
n["S04"]["parent_effects"]["D140"] = {"absent": 0.25, "on_exertion": 0.20, "at_rest": 0.55}
n["E02"]["parent_effects"]["D140"] = {"under_100": 0.10, "100_120": 0.50, "over_120": 0.40}
n["E03"]["parent_effects"]["D140"] = {"normal_over_90": 0.55, "hypotension_under_90": 0.45}
n["S07"]["parent_effects"]["D140"] = {"absent": 0.05, "mild": 0.20, "severe": 0.75}
n["E01"]["parent_effects"]["D140"] = {"under_37.5": 0.45, "37.5_38.0": 0.20, "38.0_39.0": 0.20, "39.0_40.0": 0.12, "over_40.0": 0.03}
n["L01"]["parent_effects"]["D140"] = {"low_under_4000": 0.02, "normal_4000_10000": 0.25, "high_10000_20000": 0.45, "very_high_over_20000": 0.28}
n["L02"]["parent_effects"]["D140"] = {"normal_under_0.3": 0.20, "mild_0.3_3": 0.30, "moderate_3_10": 0.30, "high_over_10": 0.20}
n["T01"]["parent_effects"]["D140"] = {"under_3d": 0.75, "3d_to_1w": 0.20, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D140"] = {"sudden_hours": 0.50, "gradual_days": 0.50}
s3["full_cpts"]["D140"] = {"parents": ["R04"], "description": "DKA。糖尿病がリスク",
    "cpt": {"no": 0.001, "yes": 0.015}}

# ===== D141 Hypoglycemia =====
s1["variables"].append({
    "id": "D141", "name": "severe_hypoglycemia", "name_ja": "重症低血糖",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "血糖<50mg/dL。意識障害/痙攣/発汗/振戦。即時ブドウ糖投与で回復"
})
d141_edges = [
    ("L54", "低血糖: 血糖著明低下(<50mg/dL)"), ("E16", "低血糖: 意識障害(70-90%)"),
    ("S42", "低血糖: 痙攣(20-30%)"), ("E02", "低血糖: 頻脈(交感神経活性化)"),
    ("S07", "低血糖: 倦怠感/脱力"), ("E01", "低血糖: 通常無熱"),
    ("L01", "低血糖: WBC通常正常"), ("L02", "低血糖: CRP通常正常"),
    ("T01", "低血糖: 超急性(数分~数時間)"), ("T02", "低血糖: 突然発症"),
]
for to, reason in d141_edges:
    s2["edges"].append({"from": "D141", "to": to, "from_name": "severe_hypoglycemia", "to_name": to, "reason": reason})

n["L54"]["parent_effects"]["D141"] = {"hypoglycemia": 0.90, "normal": 0.08, "hyperglycemia": 0.01, "very_high_over_500": 0.01}
n["E16"]["parent_effects"]["D141"] = {"normal": 0.10, "confused": 0.40, "obtunded": 0.50}
n["S42"]["parent_effects"]["D141"] = {"absent": 0.70, "present": 0.30}
n["E02"]["parent_effects"]["D141"] = {"under_100": 0.15, "100_120": 0.55, "over_120": 0.30}
n["S07"]["parent_effects"]["D141"] = {"absent": 0.10, "mild": 0.25, "severe": 0.65}
n["E01"]["parent_effects"]["D141"] = {"under_37.5": 0.90, "37.5_38.0": 0.08, "38.0_39.0": 0.02, "39.0_40.0": 0.00, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D141"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.85, "high_10000_20000": 0.10, "very_high_over_20000": 0.02}
n["L02"]["parent_effects"]["D141"] = {"normal_under_0.3": 0.80, "mild_0.3_3": 0.15, "moderate_3_10": 0.04, "high_over_10": 0.01}
n["T01"]["parent_effects"]["D141"] = {"under_3d": 0.95, "3d_to_1w": 0.04, "1w_to_3w": 0.01, "over_3w": 0.00}
n["T02"]["parent_effects"]["D141"] = {"sudden_hours": 0.85, "gradual_days": 0.15}
s3["full_cpts"]["D141"] = {"parents": ["R04"], "description": "低血糖。糖尿病(インスリン/SU剤)がリスク",
    "cpt": {"no": 0.002, "yes": 0.010}}

# ===== D142 Status Epilepticus =====
s1["variables"].append({
    "id": "D142", "name": "status_epilepticus", "name_ja": "てんかん重積状態",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "5分以上持続する痙攣または反復。意識回復なし。即時ベンゾ+抗てんかん薬"
})
d142_edges = [
    ("S42", "てんかん重積: 持続性痙攣(定義上100%)"), ("E16", "てんかん重積: 意識障害(90%+)"),
    ("E02", "てんかん重積: 頻脈(80%+)"), ("E01", "てんかん重積: 発熱(痙攣後/感染誘因)"),
    ("L01", "てんかん重積: WBC上昇(ストレス)"), ("L54", "てんかん重積: 血糖(ストレス高血糖)"),
    ("E05", "てんかん重積: 低酸素(呼吸抑制)"), ("L02", "てんかん重積: CRP(感染誘因で上昇)"),
    ("T01", "てんかん重積: 超急性"), ("T02", "てんかん重積: 突然発症"),
]
for to, reason in d142_edges:
    s2["edges"].append({"from": "D142", "to": to, "from_name": "status_epilepticus", "to_name": to, "reason": reason})

n["S42"]["parent_effects"]["D142"] = {"absent": 0.02, "present": 0.98}
n["E16"]["parent_effects"]["D142"] = {"normal": 0.05, "confused": 0.25, "obtunded": 0.70}
n["E02"]["parent_effects"]["D142"] = {"under_100": 0.05, "100_120": 0.40, "over_120": 0.55}
n["E01"]["parent_effects"]["D142"] = {"under_37.5": 0.30, "37.5_38.0": 0.25, "38.0_39.0": 0.25, "39.0_40.0": 0.15, "over_40.0": 0.05}
n["L01"]["parent_effects"]["D142"] = {"low_under_4000": 0.02, "normal_4000_10000": 0.30, "high_10000_20000": 0.45, "very_high_over_20000": 0.23}
n["L54"]["parent_effects"]["D142"] = {"hypoglycemia": 0.05, "normal": 0.40, "hyperglycemia": 0.45, "very_high_over_500": 0.10}
n["E05"]["parent_effects"]["D142"] = {"normal_over_96": 0.25, "mild_hypoxia_93_96": 0.40, "severe_hypoxia_under_93": 0.35}
n["L02"]["parent_effects"]["D142"] = {"normal_under_0.3": 0.30, "mild_0.3_3": 0.30, "moderate_3_10": 0.25, "high_over_10": 0.15}
n["T01"]["parent_effects"]["D142"] = {"under_3d": 0.90, "3d_to_1w": 0.08, "1w_to_3w": 0.02, "over_3w": 0.00}
n["T02"]["parent_effects"]["D142"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
s3["full_cpts"]["D142"] = {"parents": [], "description": "てんかん重積", "cpt": {"": 0.003}}

# ===== IDF Check: L54/S52/S53 =====
import math
n_diseases = 142
for vid in ["L54", "S52", "S53"]:
    np = len(n[vid]["parent_effects"])
    idf = math.log(n_diseases / max(np, 1)) / math.log(n_diseases)
    print(f"{vid}: {np} parents, IDF={idf:.3f}")

# L54 needs more parents for IDF health
# Add edges from existing diseases that affect blood glucose
extra_l54 = {
    "D71": ("甲状腺クリーゼ: 高血糖(40-60%)", {"hypoglycemia": 0.02, "normal": 0.30, "hyperglycemia": 0.50, "very_high_over_500": 0.18}),
    "D72": ("副腎クリーゼ: 低血糖(30-50%)", {"hypoglycemia": 0.40, "normal": 0.45, "hyperglycemia": 0.12, "very_high_over_500": 0.03}),
    "D24": ("TSS/敗血症: 血糖変動", {"hypoglycemia": 0.15, "normal": 0.35, "hyperglycemia": 0.35, "very_high_over_500": 0.15}),
}
for did, (reason, cpt) in extra_l54.items():
    s2["edges"].append({"from": did, "to": "L54", "from_name": did, "to_name": "L54", "reason": reason})
    n["L54"]["parent_effects"][did] = cpt

# S52/S53 need more parents too
extra_s52 = {
    "D13": ("髄膜炎: 局所神経症状(10-20%)", {"absent": 0.80, "unilateral_weakness": 0.15, "bilateral": 0.05}),
    "D118": ("脳膿瘍: 局所神経症状(50-65%)", {"absent": 0.30, "unilateral_weakness": 0.60, "bilateral": 0.10}),
    "D110": ("トキソプラズマ脳炎: 局所神経症状(50-70%)", {"absent": 0.25, "unilateral_weakness": 0.65, "bilateral": 0.10}),
}
for did, (reason, cpt) in extra_s52.items():
    s2["edges"].append({"from": did, "to": "S52", "from_name": did, "to_name": "S52", "reason": reason})
    n["S52"]["parent_effects"][did] = cpt

extra_s53 = {
    "D13": ("髄膜炎: 構音障害(5-10%)", {"absent": 0.90, "dysarthria": 0.08, "aphasia": 0.02}),
    "D118": ("脳膿瘍: 構音/失語(30-40%)", {"absent": 0.55, "dysarthria": 0.20, "aphasia": 0.25}),
}
for did, (reason, cpt) in extra_s53.items():
    s2["edges"].append({"from": did, "to": "S53", "from_name": did, "to_name": "S53", "reason": reason})
    n["S53"]["parent_effects"][did] = cpt

s2["total_edges"] = len(s2["edges"])

# Final IDF check
for vid in ["L54", "S52", "S53"]:
    np = len(n[vid]["parent_effects"])
    idf = math.log(n_diseases / max(np, 1)) / math.log(n_diseases)
    print(f"{vid} (final): {np} parents, IDF={idf:.3f}")

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n5 diseases (D138-D142) + 3 variables (L54/S52/S53)")
print(f"Total: {s2['total_edges']} edges, 142 diseases")
