#!/usr/bin/env python3
"""Add D165 Myasthenic Crisis + D166 Acetaminophen OD + D167 Accidental Hypothermia."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D165 重症筋無力症クリーゼ (Myasthenic Crisis) =====
s1["variables"].append({
    "id": "D165", "name": "myasthenic_crisis",
    "name_ja": "重症筋無力症クリーゼ",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "MG増悪による呼吸不全。嚥下障害+構音障害+呼吸筋麻痺。感染/手術/薬剤が誘因。挿管が必要"
})
for to, reason in [
    ("S04", "MGクリーゼ: 呼吸困難(呼吸筋麻痺, 100%)"),
    ("S07", "MGクリーゼ: 全身脱力(100%)"),
    ("S53", "MGクリーゼ: 構音障害(球麻痺, 70-80%)"),
    ("S52", "MGクリーゼ: 四肢脱力(60-80%)"),
    ("E07", "MGクリーゼ: 肺聴診(呼吸音減弱)"),
    ("E01", "MGクリーゼ: 発熱(感染誘因, 30-40%)"),
    ("E02", "MGクリーゼ: 頻脈(呼吸不全)"),
    ("T01", "MGクリーゼ: 急性~亜急性"),
    ("T02", "MGクリーゼ: 亜急性")]:
    s2["edges"].append({"from": "D165", "to": to, "from_name": "myasthenic_crisis", "to_name": to, "reason": reason})

n["S04"]["parent_effects"]["D165"] = {"absent": 0.02, "on_exertion": 0.18, "at_rest": 0.80}
n["S07"]["parent_effects"]["D165"] = {"absent": 0.02, "mild": 0.15, "severe": 0.83}
n["S53"]["parent_effects"]["D165"] = {"absent": 0.15, "dysarthria": 0.75, "aphasia": 0.10}
n["S52"]["parent_effects"]["D165"] = {"absent": 0.15, "unilateral_weakness": 0.10, "bilateral": 0.75}
n["E07"]["parent_effects"]["D165"] = {"clear": 0.15, "crackles": 0.10, "wheezes": 0.05, "decreased_absent": 0.70}
n["E01"]["parent_effects"]["D165"] = {"under_37.5": 0.55, "37.5_38.0": 0.15, "38.0_39.0": 0.18, "39.0_40.0": 0.10, "over_40.0": 0.02}
n["E02"]["parent_effects"]["D165"] = {"under_100": 0.20, "100_120": 0.45, "over_120": 0.35}
n["T01"]["parent_effects"]["D165"] = {"under_3d": 0.40, "3d_to_1w": 0.35, "1w_to_3w": 0.20, "over_3w": 0.05}
n["T02"]["parent_effects"]["D165"] = {"sudden_hours": 0.30, "gradual_days": 0.70}
s3["full_cpts"]["D165"] = {"parents": ["R02"], "description": "MGクリーゼ。女性に多い",
    "cpt": {"male": 0.0005, "female": 0.001}}

# ===== D166 アセトアミノフェン中毒 (Acetaminophen OD) =====
s1["variables"].append({
    "id": "D166", "name": "acetaminophen_overdose",
    "name_ja": "アセトアミノフェン中毒",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "最も一般的な中毒。4段階: 0-24h嘔気/嘔吐→24-72h肝酵素上昇→72-96hPT延長/黄疸/肝不全→回復期。NAC治療"
})
for to, reason in [
    ("S13", "APAP中毒: 嘔気/嘔吐(Stage I, 80-90%)"),
    ("S12", "APAP中毒: 右上腹部痛(Stage II, 肝腫大)"),
    ("L11", "APAP中毒: 肝酵素著高(Stage II-III, AST/ALT >1000)"),
    ("E18", "APAP中毒: 黄疸(Stage III, 肝不全)"),
    ("E16", "APAP中毒: 意識障害(Stage III, 肝性脳症)"),
    ("E01", "APAP中毒: 通常無熱"),
    ("L01", "APAP中毒: WBC(正常~軽度上昇)"),
    ("T01", "APAP中毒: 急性(24-72h後に肝障害)"),
    ("T02", "APAP中毒: 急性")]:
    s2["edges"].append({"from": "D166", "to": to, "from_name": "acetaminophen_OD", "to_name": to, "reason": reason})

n["S13"]["parent_effects"]["D166"] = {"absent": 0.10, "present": 0.90}
n["S12"]["parent_effects"]["D166"] = {"absent": 0.30, "epigastric": 0.10, "RUQ": 0.55, "RLQ": 0.01, "LLQ": 0.01, "suprapubic": 0.01, "diffuse": 0.02}
n["L11"]["parent_effects"]["D166"] = {"normal": 0.10, "mild_elevated": 0.15, "very_high": 0.75}
n["E18"]["parent_effects"]["D166"] = {"absent": 0.40, "present": 0.60}
n["E16"]["parent_effects"]["D166"] = {"normal": 0.40, "confused": 0.35, "obtunded": 0.25}
n["E01"]["parent_effects"]["D166"] = {"under_37.5": 0.75, "37.5_38.0": 0.12, "38.0_39.0": 0.08, "39.0_40.0": 0.03, "over_40.0": 0.02}
n["L01"]["parent_effects"]["D166"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.50, "high_10000_20000": 0.35, "very_high_over_20000": 0.10}
n["T01"]["parent_effects"]["D166"] = {"under_3d": 0.70, "3d_to_1w": 0.25, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D166"] = {"sudden_hours": 0.60, "gradual_days": 0.40}
s3["full_cpts"]["D166"] = {"parents": [], "description": "APAP中毒。自殺企図/誤用",
    "cpt": {"": 0.002}}

# ===== D167 偶発性低体温症 (Accidental Hypothermia) =====
s1["variables"].append({
    "id": "D167", "name": "accidental_hypothermia",
    "name_ja": "偶発性低体温症",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "核心温<35℃。軽度(32-35)→中等度(28-32)→重度(<28, VF risk)。高齢者/ホームレス/アルコール/薬物。粘液水腫性昏睡との鑑別"
})
for to, reason in [
    ("E01", "低体温: 低体温(定義的)"),
    ("E16", "低体温: 意識障害(中等度以上)"),
    ("E02", "低体温: 徐脈(中等度以上)"),
    ("E03", "低体温: 低血圧(重度)"),
    ("S07", "低体温: 全身脱力/硬直"),
    ("T01", "低体温: 急性~亜急性"),
    ("T02", "低体温: 急性")]:
    s2["edges"].append({"from": "D167", "to": to, "from_name": "hypothermia", "to_name": to, "reason": reason})

n["E01"]["parent_effects"]["D167"] = {"under_37.5": 0.95, "37.5_38.0": 0.03, "38.0_39.0": 0.01, "39.0_40.0": 0.005, "over_40.0": 0.005}
n["E16"]["parent_effects"]["D167"] = {"normal": 0.15, "confused": 0.40, "obtunded": 0.45}
n["E02"]["parent_effects"]["D167"] = {"under_100": 0.80, "100_120": 0.15, "over_120": 0.05}
n["E03"]["parent_effects"]["D167"] = {"normal_over_90": 0.30, "hypotension_under_90": 0.70}
n["S07"]["parent_effects"]["D167"] = {"absent": 0.05, "mild": 0.25, "severe": 0.70}
n["T01"]["parent_effects"]["D167"] = {"under_3d": 0.75, "3d_to_1w": 0.20, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D167"] = {"sudden_hours": 0.60, "gradual_days": 0.40}
s3["full_cpts"]["D167"] = {"parents": ["R01"], "description": "偶発性低体温症。高齢者に多い",
    "cpt": {"18_39": 0.001, "40_64": 0.001, "65_plus": 0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D165 MG crisis: 9 edges, D166 APAP: 9 edges, D167 Hypothermia: 7 edges")
print(f"Total: {s2['total_edges']} edges, 167 diseases")
