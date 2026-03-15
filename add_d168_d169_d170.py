#!/usr/bin/env python3
"""Add D168 RPGN + D169 Autoimmune Hepatitis + D170 Alcoholic Hepatitis."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D168 急速進行性糸球体腎炎 (RPGN) =====
s1["variables"].append({
    "id": "D168", "name": "RPGN",
    "name_ja": "急速進行性糸球体腎炎(RPGN)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "週~月単位で急速に腎機能が悪化。ANCA関連(GPA/MPA)/抗GBM(Goodpasture)/免疫複合体型。血尿+蛋白尿+AKI+全身症状"
})
for to, reason in [
    ("L55", "RPGN: AKI(急速進行, 100%)"),
    ("L05", "RPGN: 尿検査異常(血尿+蛋白尿, 90%+)"),
    ("E01", "RPGN: 発熱(ANCA関連血管炎で50-60%)"),
    ("S07", "RPGN: 全身倦怠感(80-90%)"),
    ("S08", "RPGN: 関節痛(ANCA関連, 30-40%)"),
    ("L01", "RPGN: WBC上昇(炎症)"),
    ("L02", "RPGN: CRP上昇"),
    ("S04", "RPGN: 呼吸困難(肺出血/肺腎症候群, 20-30%)"),
    ("T01", "RPGN: 亜急性(週~月)"),
    ("T02", "RPGN: 亜急性")]:
    s2["edges"].append({"from": "D168", "to": to, "from_name": "RPGN", "to_name": to, "reason": reason})

n["L55"]["parent_effects"]["D168"] = {"normal": 0.03, "mild_elevated": 0.15, "high_AKI": 0.82}
n["L05"]["parent_effects"]["D168"] = {"normal": 0.05, "pyuria_bacteriuria": 0.95}
n["E01"]["parent_effects"]["D168"] = {"under_37.5": 0.35, "37.5_38.0": 0.20, "38.0_39.0": 0.25, "39.0_40.0": 0.15, "over_40.0": 0.05}
n["S07"]["parent_effects"]["D168"] = {"absent": 0.08, "mild": 0.32, "severe": 0.60}
n["S08"]["parent_effects"]["D168"] = {"absent": 0.55, "present": 0.45}
n["L01"]["parent_effects"]["D168"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.30, "high_10000_20000": 0.45, "very_high_over_20000": 0.20}
n["L02"]["parent_effects"]["D168"] = {"normal_under_0.3": 0.08, "mild_0.3_3": 0.15, "moderate_3_10": 0.37, "high_over_10": 0.40}
n["S04"]["parent_effects"]["D168"] = {"absent": 0.65, "on_exertion": 0.20, "at_rest": 0.15}
n["T01"]["parent_effects"]["D168"] = {"under_3d": 0.05, "3d_to_1w": 0.20, "1w_to_3w": 0.45, "over_3w": 0.30}
n["T02"]["parent_effects"]["D168"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
s3["full_cpts"]["D168"] = {"parents": ["R01"], "description": "RPGN。中高年に多い",
    "cpt": {"18_39": 0.001, "40_64": 0.002, "65_plus": 0.003}}

# ===== D169 自己免疫性肝炎 (AIH) =====
s1["variables"].append({
    "id": "D169", "name": "autoimmune_hepatitis",
    "name_ja": "自己免疫性肝炎(AIH)",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "自己免疫による肝細胞障害。若年女性に多い。ANA/SMA陽性+IgG高値+肝酵素上昇。急性発症(30%)は劇症化リスク"
})
for to, reason in [
    ("L11", "AIH: 肝酵素上昇(AST/ALT, 100%)"),
    ("E18", "AIH: 黄疸(急性発症で60-70%)"),
    ("S07", "AIH: 倦怠感(80-90%)"),
    ("S12", "AIH: 腹痛(RUQ, 30-40%)"),
    ("E01", "AIH: 発熱(急性発症で30-40%)"),
    ("S08", "AIH: 関節痛(20-30%)"),
    ("L01", "AIH: WBC(正常~軽度)"),
    ("L02", "AIH: CRP(正常~軽度)"),
    ("T01", "AIH: 急性~慢性"),
    ("T02", "AIH: 亜急性~慢性")]:
    s2["edges"].append({"from": "D169", "to": to, "from_name": "AIH", "to_name": to, "reason": reason})

n["L11"]["parent_effects"]["D169"] = {"normal": 0.03, "mild_elevated": 0.25, "very_high": 0.72}
n["E18"]["parent_effects"]["D169"] = {"absent": 0.30, "present": 0.70}
n["S07"]["parent_effects"]["D169"] = {"absent": 0.08, "mild": 0.42, "severe": 0.50}
n["S12"]["parent_effects"]["D169"] = {"absent": 0.55, "epigastric": 0.05, "RUQ": 0.35, "RLQ": 0.01, "LLQ": 0.01, "suprapubic": 0.01, "diffuse": 0.02}
n["E01"]["parent_effects"]["D169"] = {"under_37.5": 0.55, "37.5_38.0": 0.18, "38.0_39.0": 0.15, "39.0_40.0": 0.10, "over_40.0": 0.02}
n["S08"]["parent_effects"]["D169"] = {"absent": 0.65, "present": 0.35}
n["L01"]["parent_effects"]["D169"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.55, "high_10000_20000": 0.30, "very_high_over_20000": 0.10}
n["L02"]["parent_effects"]["D169"] = {"normal_under_0.3": 0.20, "mild_0.3_3": 0.35, "moderate_3_10": 0.30, "high_over_10": 0.15}
n["T01"]["parent_effects"]["D169"] = {"under_3d": 0.10, "3d_to_1w": 0.25, "1w_to_3w": 0.35, "over_3w": 0.30}
n["T02"]["parent_effects"]["D169"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
s3["full_cpts"]["D169"] = {"parents": ["R02"], "description": "AIH。若年女性に多い(F:M≈4:1)",
    "cpt": {"male": 0.0005, "female": 0.002}}

# ===== D170 アルコール性肝炎 (Alcoholic Hepatitis) =====
s1["variables"].append({
    "id": "D170", "name": "alcoholic_hepatitis",
    "name_ja": "アルコール性肝炎",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "大量飲酒歴+黄疸+肝腫大+発熱。AST/ALT比>2が特徴(通常<300)。重症はMaddrey score≧32でステロイド適応。死亡率20-50%"
})
for to, reason in [
    ("E18", "アルコール性肝炎: 黄疸(90%+)"),
    ("L11", "アルコール性肝炎: 肝酵素上昇(AST>ALT, AST/ALT>2)"),
    ("E01", "アルコール性肝炎: 発熱(50-60%)"),
    ("S12", "アルコール性肝炎: 腹痛(RUQ, 50-60%)"),
    ("S07", "アルコール性肝炎: 倦怠感(80%+)"),
    ("S13", "アルコール性肝炎: 嘔気(50-60%)"),
    ("E16", "アルコール性肝炎: 意識障害(肝性脳症, 20-30%)"),
    ("L01", "アルコール性肝炎: WBC上昇(50-60%)"),
    ("L02", "アルコール性肝炎: CRP上昇"),
    ("T01", "アルコール性肝炎: 急性~亜急性"),
    ("T02", "アルコール性肝炎: 亜急性")]:
    s2["edges"].append({"from": "D170", "to": to, "from_name": "alcoholic_hepatitis", "to_name": to, "reason": reason})

n["E18"]["parent_effects"]["D170"] = {"absent": 0.05, "present": 0.95}
n["L11"]["parent_effects"]["D170"] = {"normal": 0.05, "mild_elevated": 0.65, "very_high": 0.30}
n["E01"]["parent_effects"]["D170"] = {"under_37.5": 0.35, "37.5_38.0": 0.20, "38.0_39.0": 0.25, "39.0_40.0": 0.15, "over_40.0": 0.05}
n["S12"]["parent_effects"]["D170"] = {"absent": 0.30, "epigastric": 0.10, "RUQ": 0.50, "RLQ": 0.02, "LLQ": 0.02, "suprapubic": 0.01, "diffuse": 0.05}
n["S07"]["parent_effects"]["D170"] = {"absent": 0.08, "mild": 0.32, "severe": 0.60}
n["S13"]["parent_effects"]["D170"] = {"absent": 0.35, "present": 0.65}
n["E16"]["parent_effects"]["D170"] = {"normal": 0.65, "confused": 0.25, "obtunded": 0.10}
n["L01"]["parent_effects"]["D170"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.25, "high_10000_20000": 0.45, "very_high_over_20000": 0.27}
n["L02"]["parent_effects"]["D170"] = {"normal_under_0.3": 0.08, "mild_0.3_3": 0.15, "moderate_3_10": 0.37, "high_over_10": 0.40}
n["T01"]["parent_effects"]["D170"] = {"under_3d": 0.10, "3d_to_1w": 0.30, "1w_to_3w": 0.40, "over_3w": 0.20}
n["T02"]["parent_effects"]["D170"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
s3["full_cpts"]["D170"] = {"parents": ["R02"], "description": "アルコール性肝炎。男性に多い",
    "cpt": {"male": 0.003, "female": 0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D168 RPGN: 10 edges, D169 AIH: 10 edges, D170 AlcHep: 11 edges")
print(f"Total: {s2['total_edges']} edges, 170 diseases")
