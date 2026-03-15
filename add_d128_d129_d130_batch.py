#!/usr/bin/env python3
"""Batch add D128 Upper Airway + D129 Hyperventilation + D130 ILD."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ============ D128 Upper Airway Obstruction ============
s1["variables"].append({
    "id": "D128", "name": "upper_airway_obstruction",
    "name_ja": "上気道閉塞（喉頭蓋炎/血管浮腫/異物）",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "喉頭蓋炎/血管浮腫/異物。吸気性喘鳴+呼吸困難+嚥下困難。緊急気道確保"
})
for to, reason in [
    ("S04", "上気道閉塞: 呼吸困難(90%+)"), ("S02", "上気道閉塞: 咽頭痛(60-80%)"),
    ("E02", "上気道閉塞: 頻脈(70-80%)"), ("E04", "上気道閉塞: 頻呼吸(60-70%)"),
    ("E05", "上気道閉塞: 低酸素"), ("E01", "上気道閉塞: 発熱(喉頭蓋炎50-70%)"),
    ("L01", "上気道閉塞: WBC上昇(喉頭蓋炎)"), ("L02", "上気道閉塞: CRP上昇(喉頭蓋炎)"),
    ("T01", "上気道閉塞: 超急性~急性"), ("T02", "上気道閉塞: 急性発症"),
    ("E16", "上気道閉塞: 意識障害(窒息)"), ("S09", "上気道閉塞: 悪寒(喉頭蓋炎)")]:
    s2["edges"].append({"from": "D128", "to": to, "from_name": "upper_airway_obstruction", "to_name": to, "reason": reason})

n["S04"]["parent_effects"]["D128"] = {"absent": 0.03, "on_exertion": 0.12, "at_rest": 0.85}
n["S02"]["parent_effects"]["D128"] = {"absent": 0.25, "present": 0.75}
n["E02"]["parent_effects"]["D128"] = {"under_100": 0.15, "100_120": 0.50, "over_120": 0.35}
n["E04"]["parent_effects"]["D128"] = {"normal_under_20": 0.15, "tachypnea_20_30": 0.50, "severe_over_30": 0.35}
n["E05"]["parent_effects"]["D128"] = {"normal_over_96": 0.30, "mild_hypoxia_93_96": 0.35, "severe_hypoxia_under_93": 0.35}
n["E01"]["parent_effects"]["D128"] = {"under_37.5": 0.30, "37.5_38.0": 0.15, "38.0_39.0": 0.25, "39.0_40.0": 0.20, "over_40.0": 0.10}
n["L01"]["parent_effects"]["D128"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.25, "high_10000_20000": 0.45, "very_high_over_20000": 0.27}
n["L02"]["parent_effects"]["D128"] = {"normal_under_0.3": 0.15, "mild_0.3_3": 0.20, "moderate_3_10": 0.30, "high_over_10": 0.35}
n["T01"]["parent_effects"]["D128"] = {"under_3d": 0.70, "3d_to_1w": 0.25, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D128"] = {"sudden_hours": 0.70, "gradual_days": 0.30}
n["E16"]["parent_effects"]["D128"] = {"normal": 0.70, "confused": 0.15, "obtunded": 0.15}
n["S09"]["parent_effects"]["D128"] = {"absent": 0.60, "present": 0.40}
s3["full_cpts"]["D128"] = {"parents": [], "description": "上気道閉塞", "cpt": {"": 0.003}}

# ============ D129 Hyperventilation Syndrome ============
s1["variables"].append({
    "id": "D129", "name": "hyperventilation_syndrome",
    "name_ja": "過換気症候群",
    "category": "disease", "states": ["no", "yes"], "severity": "low",
    "note": "心因性過換気。SpO2正常+CXR正常+呼吸性アルカローシス。除外診断"
})
for to, reason in [
    ("S04", "過換気: 呼吸困難(90%+)"), ("E04", "過換気: 頻呼吸(90%+)"),
    ("E02", "過換気: 頻脈(50-60%)"), ("S21", "過換気: 胸痛(40-60%)"),
    ("S05", "過換気: めまい(40-50%)"), ("E05", "過換気: SpO2正常(95%+)"),
    ("E01", "過換気: 無熱"), ("L01", "過換気: WBC正常"), ("L02", "過換気: CRP正常"),
    ("L04", "過換気: CXR正常"), ("T01", "過換気: 超急性"), ("T02", "過換気: 突然発症"),
    ("S07", "過換気: 倦怠感(30-40%)")]:
    s2["edges"].append({"from": "D129", "to": to, "from_name": "hyperventilation_syndrome", "to_name": to, "reason": reason})

n["S04"]["parent_effects"]["D129"] = {"absent": 0.05, "on_exertion": 0.15, "at_rest": 0.80}
n["E04"]["parent_effects"]["D129"] = {"normal_under_20": 0.05, "tachypnea_20_30": 0.65, "severe_over_30": 0.30}
n["E02"]["parent_effects"]["D129"] = {"under_100": 0.30, "100_120": 0.55, "over_120": 0.15}
n["S21"]["parent_effects"]["D129"] = {"absent": 0.40, "pleuritic": 0.10, "constant": 0.50}
n["S05"]["parent_effects"]["D129"] = {"absent": 0.40, "mild": 0.35, "severe": 0.25}
n["E05"]["parent_effects"]["D129"] = {"normal_over_96": 0.92, "mild_hypoxia_93_96": 0.07, "severe_hypoxia_under_93": 0.01}
n["E01"]["parent_effects"]["D129"] = {"under_37.5": 0.90, "37.5_38.0": 0.08, "38.0_39.0": 0.02, "39.0_40.0": 0.00, "over_40.0": 0.00}
n["L01"]["parent_effects"]["D129"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.85, "high_10000_20000": 0.10, "very_high_over_20000": 0.02}
n["L02"]["parent_effects"]["D129"] = {"normal_under_0.3": 0.75, "mild_0.3_3": 0.20, "moderate_3_10": 0.04, "high_over_10": 0.01}
n["L04"]["parent_effects"]["D129"] = {"normal": 0.90, "lobar_infiltrate": 0.02, "bilateral_infiltrate": 0.02, "BHL": 0.02, "pleural_effusion": 0.02, "pneumothorax": 0.02}
n["T01"]["parent_effects"]["D129"] = {"under_3d": 0.90, "3d_to_1w": 0.08, "1w_to_3w": 0.02, "over_3w": 0.00}
n["T02"]["parent_effects"]["D129"] = {"sudden_hours": 0.85, "gradual_days": 0.15}
n["S07"]["parent_effects"]["D129"] = {"absent": 0.50, "mild": 0.35, "severe": 0.15}
s3["full_cpts"]["D129"] = {"parents": ["R01"], "description": "過換気症候群。若年に多い",
    "cpt": {"18_39": 0.005, "40_64": 0.003, "65_plus": 0.001}}

# ============ D130 ILD ============
s1["variables"].append({
    "id": "D130", "name": "interstitial_lung_disease",
    "name_ja": "間質性肺疾患(ILD/IPF)",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "慢性進行性呼吸困難+乾性咳嗽+fine crackles。HRCT蜂巣肺/GGO。KL-6上昇"
})
for to, reason in [
    ("S04", "ILD: 労作時呼吸困難(90%+)"), ("S01", "ILD: 乾性咳嗽(70-80%)"),
    ("E07", "ILD: fine crackles(70-80%)"), ("E05", "ILD: 低酸素"),
    ("E04", "ILD: 頻呼吸(50-60%)"), ("L04", "ILD: CXR両側浸潤影"),
    ("L16", "ILD: LDH上昇(50-60%)"), ("L02", "ILD: CRP正常~軽度"),
    ("L01", "ILD: WBC通常正常"), ("E01", "ILD: 通常無熱"),
    ("S07", "ILD: 倦怠感(50-60%)"), ("S17", "ILD: 体重減少(進行期)"),
    ("T01", "ILD: 慢性(数ヶ月~)"), ("T02", "ILD: 緩徐発症")]:
    s2["edges"].append({"from": "D130", "to": to, "from_name": "interstitial_lung_disease", "to_name": to, "reason": reason})

n["S04"]["parent_effects"]["D130"] = {"absent": 0.05, "on_exertion": 0.55, "at_rest": 0.40}
n["S01"]["parent_effects"]["D130"] = {"absent": 0.20, "dry": 0.65, "productive": 0.15}
n["E07"]["parent_effects"]["D130"] = {"clear": 0.15, "crackles": 0.75, "wheezes": 0.05, "decreased_absent": 0.05}
n["E05"]["parent_effects"]["D130"] = {"normal_over_96": 0.25, "mild_hypoxia_93_96": 0.40, "severe_hypoxia_under_93": 0.35}
n["E04"]["parent_effects"]["D130"] = {"normal_under_20": 0.30, "tachypnea_20_30": 0.50, "severe_over_30": 0.20}
n["L04"]["parent_effects"]["D130"] = {"normal": 0.10, "lobar_infiltrate": 0.10, "bilateral_infiltrate": 0.60, "BHL": 0.08, "pleural_effusion": 0.08, "pneumothorax": 0.04}
n["L16"]["parent_effects"]["D130"] = {"normal": 0.40, "elevated": 0.60}
n["L02"]["parent_effects"]["D130"] = {"normal_under_0.3": 0.40, "mild_0.3_3": 0.30, "moderate_3_10": 0.20, "high_over_10": 0.10}
n["L01"]["parent_effects"]["D130"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.70, "high_10000_20000": 0.20, "very_high_over_20000": 0.05}
n["E01"]["parent_effects"]["D130"] = {"under_37.5": 0.60, "37.5_38.0": 0.20, "38.0_39.0": 0.15, "39.0_40.0": 0.04, "over_40.0": 0.01}
n["S07"]["parent_effects"]["D130"] = {"absent": 0.25, "mild": 0.35, "severe": 0.40}
n["S17"]["parent_effects"]["D130"] = {"absent": 0.70, "present": 0.30}
n["T01"]["parent_effects"]["D130"] = {"under_3d": 0.05, "3d_to_1w": 0.10, "1w_to_3w": 0.20, "over_3w": 0.65}
n["T02"]["parent_effects"]["D130"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
s3["full_cpts"]["D130"] = {"parents": [], "description": "間質性肺疾患", "cpt": {"": 0.004}}

s2["total_edges"] = len(s2["edges"])

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D128: 12 edges, D129: 13 edges, D130: 14 edges")
print(f"Total: {s2['total_edges']} edges, 130 diseases")
