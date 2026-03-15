#!/usr/bin/env python3
"""Add D158 AIHA + D159 Myxedema Coma."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D158 自己免疫性溶血性貧血 (AIHA) =====
s1["variables"].append({
    "id": "D158", "name": "AIHA",
    "name_ja": "自己免疫性溶血性貧血(AIHA)",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "温式(IgG, 70%)/冷式(IgM). Coombs陽性+LDH↑+ハプトグロビン↓+間接Bil↑+網赤血球↑。黄疸+貧血+脾腫"
})
for to, reason in [
    ("S07", "AIHA: 倦怠感(貧血, 80-90%)"),
    ("E18", "AIHA: 黄疸(溶血, 60-70%)"),
    ("L16", "AIHA: LDH上昇(溶血, 90%+)"),
    ("E01", "AIHA: 発熱(20-30%, 溶血クリーゼ)"),
    ("E02", "AIHA: 頻脈(貧血代償)"),
    ("S04", "AIHA: 呼吸困難(重度貧血)"),
    ("L01", "AIHA: WBC(正常~軽度上昇)"),
    ("L02", "AIHA: CRP(正常~軽度)"),
    ("L11", "AIHA: 肝酵素(通常正常~軽度)"),
    ("T01", "AIHA: 急性~亜急性"),
    ("T02", "AIHA: 亜急性")]:
    s2["edges"].append({"from": "D158", "to": to, "from_name": "AIHA", "to_name": to, "reason": reason})

n["S07"]["parent_effects"]["D158"] = {"absent": 0.10, "mild": 0.35, "severe": 0.55}
n["E18"]["parent_effects"]["D158"] = {"absent": 0.30, "present": 0.70}
n["L16"]["parent_effects"]["D158"] = {"normal": 0.05, "elevated": 0.95}
n["E01"]["parent_effects"]["D158"] = {"under_37.5": 0.65, "37.5_38.0": 0.15, "38.0_39.0": 0.12, "39.0_40.0": 0.06, "over_40.0": 0.02}
n["E02"]["parent_effects"]["D158"] = {"under_100": 0.20, "100_120": 0.50, "over_120": 0.30}
n["S04"]["parent_effects"]["D158"] = {"absent": 0.30, "on_exertion": 0.50, "at_rest": 0.20}
n["L01"]["parent_effects"]["D158"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.50, "high_10000_20000": 0.35, "very_high_over_20000": 0.10}
n["L02"]["parent_effects"]["D158"] = {"normal_under_0.3": 0.30, "mild_0.3_3": 0.35, "moderate_3_10": 0.25, "high_over_10": 0.10}
n["L11"]["parent_effects"]["D158"] = {"normal": 0.55, "mild_elevated": 0.35, "very_high": 0.10}
n["T01"]["parent_effects"]["D158"] = {"under_3d": 0.30, "3d_to_1w": 0.40, "1w_to_3w": 0.25, "over_3w": 0.05}
n["T02"]["parent_effects"]["D158"] = {"sudden_hours": 0.20, "gradual_days": 0.80}
s3["full_cpts"]["D158"] = {"parents": ["R02"], "description": "AIHA。女性に多い(F:M≈2:1)",
    "cpt": {"male": 0.001, "female": 0.002}}

# ===== D159 粘液水腫性昏睡 (Myxedema Coma) =====
s1["variables"].append({
    "id": "D159", "name": "myxedema_coma",
    "name_ja": "粘液水腫性昏睡",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "甲状腺機能低下症の究極形態。低体温+徐脈+低血圧+意識障害+低Na血症。死亡率30-60%。冬季・高齢女性に多い"
})
for to, reason in [
    ("E16", "粘液水腫: 意識障害(定義的, 100%)"),
    ("E01", "粘液水腫: 低体温(80-90%)"),
    ("E02", "粘液水腫: 徐脈(70-80%)"),
    ("E03", "粘液水腫: 低血圧(50-60%)"),
    ("S07", "粘液水腫: 全身倦怠感(100%)"),
    ("L44", "粘液水腫: 低Na血症(50-60%)"),
    ("L54", "粘液水腫: 低血糖(30-40%)"),
    ("E36", "粘液水腫: 下肢浮腫(非圧痕性, 60-70%)"),
    ("T01", "粘液水腫: 亜急性~慢性"),
    ("T02", "粘液水腫: 緩徐(日~週)")]:
    s2["edges"].append({"from": "D159", "to": to, "from_name": "myxedema_coma", "to_name": to, "reason": reason})

n["E16"]["parent_effects"]["D159"] = {"normal": 0.05, "confused": 0.35, "obtunded": 0.60}
n["E01"]["parent_effects"]["D159"] = {"under_37.5": 0.90, "37.5_38.0": 0.05, "38.0_39.0": 0.03, "39.0_40.0": 0.01, "over_40.0": 0.01}
n["E02"]["parent_effects"]["D159"] = {"under_100": 0.85, "100_120": 0.10, "over_120": 0.05}
n["E03"]["parent_effects"]["D159"] = {"normal_over_90": 0.35, "hypotension_under_90": 0.65}
n["S07"]["parent_effects"]["D159"] = {"absent": 0.02, "mild": 0.18, "severe": 0.80}
n["L44"]["parent_effects"]["D159"] = {"normal": 0.35, "hyponatremia": 0.60, "hyperkalemia": 0.02, "other": 0.03}
n["L54"]["parent_effects"]["D159"] = {"hypoglycemia": 0.35, "normal": 0.55, "hyperglycemia": 0.08, "very_high_over_500": 0.02}
n["E36"]["parent_effects"]["D159"] = {"absent": 0.25, "pitting": 0.20, "non_pitting": 0.55}
n["T01"]["parent_effects"]["D159"] = {"under_3d": 0.20, "3d_to_1w": 0.35, "1w_to_3w": 0.30, "over_3w": 0.15}
n["T02"]["parent_effects"]["D159"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
s3["full_cpts"]["D159"] = {"parents": ["R01", "R02"], "description": "粘液水腫性昏睡。高齢女性に圧倒的に多い",
    "cpt": {"18_39,male": 0.0002, "18_39,female": 0.0005,
            "40_64,male": 0.0005, "40_64,female": 0.001,
            "65_plus,male": 0.001, "65_plus,female": 0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D158 AIHA: 11 edges, D159 Myxedema: 10 edges")
print(f"Total: {s2['total_edges']} edges, 159 diseases")
