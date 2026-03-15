#!/usr/bin/env python3
"""Add D120 Acute Decompensated Heart Failure (急性心不全/ADHF).

Clinical basis:
  ER呼吸困難の最多原因の一つ。
  呼吸困難(90%+), 起座呼吸(50-60%), 湿性ラ音(60-80%),
  下腿浮腫(60-70%), JVD(40-50%), 頻脈, 低酸素
  BNP著高(>400), 胸部X線(肺うっ血/胸水)
  リスク: 心疾患既往, 高齢, 糖尿病, 高血圧
  References: Yancy CW et al. JACC 2013;62:e147 (AHA/ACC guideline)
              Mebazaa A et al. Eur Heart J 2015 (ESC guideline)
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

s1["variables"].append({
    "id": "D120",
    "name": "acute_heart_failure",
    "name_ja": "急性心不全（ADHF）",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "呼吸困難の最多原因。起座呼吸+湿性ラ音+下腿浮腫+JVD+BNP著高。"
           "胸部X線で肺うっ血/胸水。心疾患既往+高齢がリスク。"
})

d_edges = [
    ("S04",  "心不全: 呼吸困難(90%+, 労作時→安静時に進行)"),
    ("S49",  "心不全: 起座呼吸(50-60%, 特異度90%+)"),
    ("E07",  "心不全: 肺聴診 — 湿性ラ音/crackles(60-80%)"),
    ("E36",  "心不全: 下腿浮腫 — 両側性(60-70%)"),
    ("E37",  "心不全: JVD(40-50%)"),
    ("E02",  "心不全: 頻脈(50-60%)"),
    ("E05",  "心不全: 低酸素(SpO2低下, 重症で)"),
    ("E04",  "心不全: 頻呼吸(50-70%)"),
    ("E01",  "心不全: 微熱(10-20%, 通常は無熱)"),
    ("L51",  "心不全: BNP/NT-proBNP著高(>400, 90%+)"),
    ("L04",  "心不全: 胸部X線 — 肺うっ血/胸水(bilateral_infiltrate/pleural_effusion)"),
    ("S35",  "心不全: 動悸(30-40%, 不整脈合併)"),
    ("S07",  "心不全: 倦怠感(70-80%)"),
    ("S13",  "心不全: 嘔気(20-30%, 腸管うっ血)"),
    ("L01",  "心不全: WBC通常正常(感染合併なければ)"),
    ("L02",  "心不全: CRP軽度上昇(心筋ストレス)"),
    ("T01",  "心不全: 急性~亜急性(数時間~数日)"),
    ("T02",  "心不全: 急性~亜急性"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D120", "to": to_id, "from_name": "acute_heart_failure", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

n["S04"]["parent_effects"]["D120"] = {"absent": 0.05, "on_exertion": 0.30, "at_rest": 0.65}
n["E07"]["parent_effects"]["D120"] = {"clear": 0.15, "crackles": 0.75, "wheezes": 0.10}
n["E02"]["parent_effects"]["D120"] = {"under_100": 0.35, "100_120": 0.40, "over_120": 0.25}
n["E05"]["parent_effects"]["D120"] = {"normal_over_96": 0.40, "mild_hypoxia_93_96": 0.35, "severe_hypoxia_under_93": 0.25}
n["E04"]["parent_effects"]["D120"] = {"normal_under_20": 0.25, "tachypnea_20_30": 0.50, "severe_over_30": 0.25}
n["E01"]["parent_effects"]["D120"] = {"under_37.5": 0.75, "37.5_38.0": 0.15, "38.0_39.0": 0.08, "39.0_40.0": 0.02, "over_40.0": 0.00}
n["L04"]["parent_effects"]["D120"] = {"normal": 0.10, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.45, "BHL": 0.02, "pleural_effusion": 0.38}
n["S35"]["parent_effects"]["D120"] = {"absent": 0.60, "present": 0.40}
n["S07"]["parent_effects"]["D120"] = {"absent": 0.10, "mild": 0.25, "severe": 0.65}
n["S13"]["parent_effects"]["D120"] = {"absent": 0.70, "present": 0.30}
n["L01"]["parent_effects"]["D120"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.70, "high_10000_20000": 0.20, "very_high_over_20000": 0.05}
n["L02"]["parent_effects"]["D120"] = {"normal_under_0.3": 0.30, "mild_0.3_3": 0.40, "moderate_3_10": 0.25, "high_over_10": 0.05}
n["T01"]["parent_effects"]["D120"] = {"under_3d": 0.40, "3d_to_1w": 0.35, "1w_to_3w": 0.20, "over_3w": 0.05}
n["T02"]["parent_effects"]["D120"] = {"sudden_hours": 0.45, "gradual_days": 0.55}

# New variables - need leak first
if "S49" not in n:
    n["S49"] = {"description": "起座呼吸", "leak": {"absent": 0.97, "present": 0.03}, "parent_effects": {}}
n["S49"]["parent_effects"]["D120"] = {"absent": 0.35, "present": 0.65}

if "E36" not in n:
    n["E36"] = {"description": "下腿浮腫", "leak": {"absent": 0.90, "unilateral": 0.05, "bilateral": 0.05}, "parent_effects": {}}
n["E36"]["parent_effects"]["D120"] = {"absent": 0.25, "unilateral": 0.05, "bilateral": 0.70}

if "E37" not in n:
    n["E37"] = {"description": "頸静脈怒張(JVD)", "leak": {"absent": 0.95, "present": 0.05}, "parent_effects": {}}
n["E37"]["parent_effects"]["D120"] = {"absent": 0.50, "present": 0.50}

if "L51" not in n:
    n["L51"] = {"description": "BNP/NT-proBNP", "leak": {"not_done": 0.70, "normal": 0.25, "mildly_elevated": 0.04, "very_high": 0.01}, "parent_effects": {}}
n["L51"]["parent_effects"]["D120"] = {"not_done": 0.10, "normal": 0.03, "mildly_elevated": 0.12, "very_high": 0.75}

# full_cpt: 心疾患既往 + 年齢
s3["full_cpts"]["D120"] = {
    "parents": ["R44", "R01"],
    "description": "急性心不全。心疾患既往+高齢がリスク",
    "cpt": {
        "no|18_39": 0.002, "no|40_64": 0.005, "no|65_plus": 0.010,
        "yes|18_39": 0.010, "yes|40_64": 0.025, "yes|65_plus": 0.050,
    }
}

# R44 root_prior
s3["root_priors"]["R44"] = {
    "description": "心疾患既往",
    "distribution": {"no": 0.85, "yes": 0.15}
}
# R45 root_prior
s3["root_priors"]["R45"] = {
    "description": "喫煙歴",
    "distribution": {"never": 0.55, "former": 0.25, "current": 0.20}
}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D120 acute_heart_failure: {len(d_edges)} edges. Total: {s2['total_edges']}")
print(f"New noisy_or entries: S49, E36, E37, L51")
print(f"New root_priors: R44, R45")
