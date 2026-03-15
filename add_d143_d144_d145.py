#!/usr/bin/env python3
"""Add D143 Aspiration Pneumonia + D144 GBS + D145 Ureteral Stone."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D143 Aspiration Pneumonia =====
s1["variables"].append({
    "id": "D143", "name": "aspiration_pneumonia",
    "name_ja": "誤嚥性肺炎",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "高齢者/嚥下障害/脳卒中後/認知症。右下葉に多い。起炎菌:嫌気性菌+口腔内常在菌"
})
for to, reason in [
    ("E01", "誤嚥性肺炎: 発熱(70-80%)"), ("S01", "誤嚥性肺炎: 咳嗽(60-70%, 湿性)"),
    ("S04", "誤嚥性肺炎: 呼吸困難(50-60%)"), ("E07", "誤嚥性肺炎: 肺聴診crackles(70-80%)"),
    ("E04", "誤嚥性肺炎: 頻呼吸(50-60%)"), ("E05", "誤嚥性肺炎: 低酸素(40-50%)"),
    ("E02", "誤嚥性肺炎: 頻脈(50-60%)"),
    ("L01", "誤嚥性肺炎: WBC上昇(70-80%)"), ("L02", "誤嚥性肺炎: CRP上昇"),
    ("L03", "誤嚥性肺炎: PCT上昇(細菌性)"), ("L04", "誤嚥性肺炎: CXR浸潤影(右下葉多い)"),
    ("E16", "誤嚥性肺炎: 意識障害(誤嚥リスク+敗血症)"),
    ("T01", "誤嚥性肺炎: 急性~亜急性"), ("T02", "誤嚥性肺炎: 亜急性")]:
    s2["edges"].append({"from": "D143", "to": to, "from_name": "aspiration_pneumonia", "to_name": to, "reason": reason})

n["E01"]["parent_effects"]["D143"] = {"under_37.5": 0.15, "37.5_38.0": 0.20, "38.0_39.0": 0.35, "39.0_40.0": 0.20, "over_40.0": 0.10}
n["S01"]["parent_effects"]["D143"] = {"absent": 0.25, "dry": 0.15, "productive": 0.60}
n["S04"]["parent_effects"]["D143"] = {"absent": 0.30, "on_exertion": 0.30, "at_rest": 0.40}
n["E07"]["parent_effects"]["D143"] = {"clear": 0.15, "crackles": 0.75, "wheezes": 0.05, "decreased_absent": 0.05}
n["E04"]["parent_effects"]["D143"] = {"normal_under_20": 0.25, "tachypnea_20_30": 0.50, "severe_over_30": 0.25}
n["E05"]["parent_effects"]["D143"] = {"normal_over_96": 0.35, "mild_hypoxia_93_96": 0.35, "severe_hypoxia_under_93": 0.30}
n["E02"]["parent_effects"]["D143"] = {"under_100": 0.30, "100_120": 0.45, "over_120": 0.25}
n["L01"]["parent_effects"]["D143"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.15, "high_10000_20000": 0.50, "very_high_over_20000": 0.32}
n["L02"]["parent_effects"]["D143"] = {"normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.30, "high_over_10": 0.55}
n["L03"]["parent_effects"]["D143"] = {"not_done": 0.25, "low_under_0.25": 0.10, "gray_0.25_0.5": 0.20, "high_over_0.5": 0.45}
n["L04"]["parent_effects"]["D143"] = {"normal": 0.10, "lobar_infiltrate": 0.45, "bilateral_infiltrate": 0.25, "BHL": 0.02, "pleural_effusion": 0.15, "pneumothorax": 0.03}
n["E16"]["parent_effects"]["D143"] = {"normal": 0.40, "confused": 0.35, "obtunded": 0.25}
n["T01"]["parent_effects"]["D143"] = {"under_3d": 0.30, "3d_to_1w": 0.45, "1w_to_3w": 0.20, "over_3w": 0.05}
n["T02"]["parent_effects"]["D143"] = {"sudden_hours": 0.25, "gradual_days": 0.75}
s3["full_cpts"]["D143"] = {"parents": ["R01"], "description": "誤嚥性肺炎。高齢がリスク",
    "cpt": {"18_39": 0.002, "40_64": 0.005, "65_plus": 0.015}}

# ===== D144 GBS =====
s1["variables"].append({
    "id": "D144", "name": "guillain_barre_syndrome",
    "name_ja": "ギラン・バレー症候群(GBS)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "急性上行性弛緩性麻痺。先行感染1-4週後。深部反射消失。呼吸筋麻痺リスク。CSF蛋白細胞解離"
})
for to, reason in [
    ("S52", "GBS: 上行性四肢筋力低下(bilateral, 90%+)"),
    ("S04", "GBS: 呼吸困難(呼吸筋麻痺20-30%)"), ("S06", "GBS: 筋肉痛/背部痛(50-70%)"),
    ("E02", "GBS: 頻脈(自律神経障害30-40%)"), ("E03", "GBS: 低血圧(自律神経障害)"),
    ("E01", "GBS: 通常無熱(先行感染は解熱後)"),
    ("L01", "GBS: WBC通常正常"), ("L02", "GBS: CRP通常正常"),
    ("T01", "GBS: 亜急性(数日~2週で進行)"), ("T02", "GBS: 亜急性発症")]:
    s2["edges"].append({"from": "D144", "to": to, "from_name": "guillain_barre_syndrome", "to_name": to, "reason": reason})

n["S52"]["parent_effects"]["D144"] = {"absent": 0.05, "unilateral_weakness": 0.10, "bilateral": 0.85}
n["S04"]["parent_effects"]["D144"] = {"absent": 0.60, "on_exertion": 0.20, "at_rest": 0.20}
n["S06"]["parent_effects"]["D144"] = {"absent": 0.30, "present": 0.70}
n["E02"]["parent_effects"]["D144"] = {"under_100": 0.50, "100_120": 0.35, "over_120": 0.15}
n["E03"]["parent_effects"]["D144"] = {"normal_over_90": 0.70, "hypotension_under_90": 0.30}
n["E01"]["parent_effects"]["D144"] = {"under_37.5": 0.80, "37.5_38.0": 0.12, "38.0_39.0": 0.06, "39.0_40.0": 0.02, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D144"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.80, "high_10000_20000": 0.14, "very_high_over_20000": 0.03}
n["L02"]["parent_effects"]["D144"] = {"normal_under_0.3": 0.60, "mild_0.3_3": 0.25, "moderate_3_10": 0.12, "high_over_10": 0.03}
n["T01"]["parent_effects"]["D144"] = {"under_3d": 0.10, "3d_to_1w": 0.35, "1w_to_3w": 0.45, "over_3w": 0.10}
n["T02"]["parent_effects"]["D144"] = {"sudden_hours": 0.15, "gradual_days": 0.85}
s3["full_cpts"]["D144"] = {"parents": [], "description": "GBS。先行感染後", "cpt": {"": 0.002}}

# ===== D145 Ureteral Stone =====
s1["variables"].append({
    "id": "D145", "name": "ureteral_stone",
    "name_ja": "尿管結石（腎疝痛）",
    "category": "disease", "states": ["no", "yes"], "severity": "moderate",
    "note": "突然の激烈側腹部痛(鼠径部放散)+血尿+嘔気。CT石が確定。自然排石or砕石術"
})
for to, reason in [
    ("S15", "尿管結石: 側腹部痛(90%+, 激烈, 波状)"),
    ("E11", "尿管結石: CVA叩打痛(80%+)"),
    ("S13", "尿管結石: 嘔気嘔吐(60-70%)"),
    ("L05", "尿管結石: 尿検査 血尿(80-90%)"),
    ("E01", "尿管結石: 通常無熱(感染合併なら発熱)"),
    ("E02", "尿管結石: 頻脈(疼痛で40-50%)"),
    ("L01", "尿管結石: WBC通常正常(感染なければ)"),
    ("L02", "尿管結石: CRP通常正常~軽度"),
    ("T01", "尿管結石: 超急性(数時間)"), ("T02", "尿管結石: 突然発症")]:
    s2["edges"].append({"from": "D145", "to": to, "from_name": "ureteral_stone", "to_name": to, "reason": reason})

n["S15"]["parent_effects"]["D145"] = {"absent": 0.05, "present": 0.95}
n["E11"]["parent_effects"]["D145"] = {"absent": 0.10, "present": 0.90}
n["S13"]["parent_effects"]["D145"] = {"absent": 0.25, "present": 0.75}
n["L05"]["parent_effects"]["D145"] = {"normal": 0.10, "pyuria_bacteriuria": 0.90}
n["E01"]["parent_effects"]["D145"] = {"under_37.5": 0.70, "37.5_38.0": 0.15, "38.0_39.0": 0.10, "39.0_40.0": 0.04, "over_40.0": 0.01}
n["E02"]["parent_effects"]["D145"] = {"under_100": 0.40, "100_120": 0.45, "over_120": 0.15}
n["L01"]["parent_effects"]["D145"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.70, "high_10000_20000": 0.22, "very_high_over_20000": 0.05}
n["L02"]["parent_effects"]["D145"] = {"normal_under_0.3": 0.50, "mild_0.3_3": 0.30, "moderate_3_10": 0.15, "high_over_10": 0.05}
n["T01"]["parent_effects"]["D145"] = {"under_3d": 0.80, "3d_to_1w": 0.15, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D145"] = {"sudden_hours": 0.85, "gradual_days": 0.15}
s3["full_cpts"]["D145"] = {"parents": ["R01"], "description": "尿管結石。中年男性に多い",
    "cpt": {"18_39": 0.005, "40_64": 0.008, "65_plus": 0.004}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D143: 14 edges, D144: 10 edges, D145: 10 edges")
print(f"Total: {s2['total_edges']} edges, 145 diseases")
