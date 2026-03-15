#!/usr/bin/env python3
"""Batch add D131 ACS (急性冠症候群) + D132 Aortic Dissection (大動脈解離).

D131 ACS:
  胸痛(80-95%, 圧迫感/絞扼感, 左腕/顎に放散), 呼吸困難(50-60%),
  冷汗(40-60%), 嘔気(30-40%), 動悸
  頻脈, 低血圧(重症で), トロポニン上昇, CK上昇
  ECGでST変化。リスク: 高齢/DM/喫煙/高血圧/心疾患既往

D132 大動脈解離:
  胸痛(90%+, 引き裂かれるような, 突然発症, 最初から最大),
  背部痛(50-70%), 血圧左右差(>20mmHg)
  頻脈, 高血圧(Type B), 低血圧(Type A合併症)
  D-dimer上昇, WBC上昇, CRP上昇
  CT造影で確定。リスク: 高血圧/Marfan/大動脈二尖弁
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

# ============ D131 ACS ============
s1["variables"].append({
    "id": "D131", "name": "acute_coronary_syndrome",
    "name_ja": "急性冠症候群（ACS/心筋梗塞）",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "STEMI/NSTEMI/不安定狭心症。胸痛(圧迫感)+冷汗+呼吸困難。"
           "トロポニン/CK上昇。ECG ST変化。緊急PCI"
})
for to, reason in [
    ("S21", "ACS: 胸痛(80-95%, 圧迫感/絞扼感, 左腕/顎放散)"),
    ("S04", "ACS: 呼吸困難(50-60%, 心不全合併)"),
    ("S13", "ACS: 嘔気嘔吐(30-40%, 特に下壁MI)"),
    ("S35", "ACS: 動悸(20-30%)"),
    ("E02", "ACS: 頻脈(40-60%)"),
    ("E03", "ACS: 低血圧(重症/右室梗塞で20-30%)"),
    ("E05", "ACS: 低酸素(心不全合併で)"),
    ("E07", "ACS: 肺聴診 crackles(心不全合併30-40%)"),
    ("L17", "ACS: CK上昇(60-80%, 発症6-12h後)"),
    ("L51", "ACS: BNP上昇(心不全合併で)"),
    ("L01", "ACS: WBC軽度上昇(ストレス反応)"),
    ("L02", "ACS: CRP軽度上昇"),
    ("E01", "ACS: 通常無熱(梗塞後微熱もあり)"),
    ("T01", "ACS: 超急性(数分~数時間)"),
    ("T02", "ACS: 突然発症"),
    ("S07", "ACS: 倦怠感(30-40%)"),
    ("E37", "ACS: JVD(右室梗塞/心不全で)"),
    ("E36", "ACS: 下腿浮腫(心不全合併で)"),
]:
    s2["edges"].append({"from": "D131", "to": to, "from_name": "acute_coronary_syndrome", "to_name": to, "reason": reason})

n["S21"]["parent_effects"]["D131"] = {"absent": 0.05, "pleuritic": 0.05, "constant": 0.90}
n["S04"]["parent_effects"]["D131"] = {"absent": 0.35, "on_exertion": 0.30, "at_rest": 0.35}
n["S13"]["parent_effects"]["D131"] = {"absent": 0.60, "present": 0.40}
n["S35"]["parent_effects"]["D131"] = {"absent": 0.70, "present": 0.30}
n["E02"]["parent_effects"]["D131"] = {"under_100": 0.35, "100_120": 0.45, "over_120": 0.20}
n["E03"]["parent_effects"]["D131"] = {"normal_over_90": 0.70, "hypotension_under_90": 0.30}
n["E05"]["parent_effects"]["D131"] = {"normal_over_96": 0.55, "mild_hypoxia_93_96": 0.30, "severe_hypoxia_under_93": 0.15}
n["E07"]["parent_effects"]["D131"] = {"clear": 0.55, "crackles": 0.35, "wheezes": 0.05, "decreased_absent": 0.05}
n["L17"]["parent_effects"]["D131"] = {"normal": 0.25, "elevated": 0.50, "very_high": 0.25}
n["L51"]["parent_effects"]["D131"] = {"not_done": 0.20, "normal": 0.25, "mildly_elevated": 0.30, "very_high": 0.25}
n["L01"]["parent_effects"]["D131"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.45, "high_10000_20000": 0.40, "very_high_over_20000": 0.12}
n["L02"]["parent_effects"]["D131"] = {"normal_under_0.3": 0.25, "mild_0.3_3": 0.40, "moderate_3_10": 0.25, "high_over_10": 0.10}
n["E01"]["parent_effects"]["D131"] = {"under_37.5": 0.70, "37.5_38.0": 0.20, "38.0_39.0": 0.08, "39.0_40.0": 0.02, "over_40.0": 0.00}
n["T01"]["parent_effects"]["D131"] = {"under_3d": 0.80, "3d_to_1w": 0.15, "1w_to_3w": 0.04, "over_3w": 0.01}
n["T02"]["parent_effects"]["D131"] = {"sudden_hours": 0.80, "gradual_days": 0.20}
n["S07"]["parent_effects"]["D131"] = {"absent": 0.45, "mild": 0.30, "severe": 0.25}
n["E37"]["parent_effects"]["D131"] = {"absent": 0.75, "present": 0.25}
n["E36"]["parent_effects"]["D131"] = {"absent": 0.70, "unilateral": 0.05, "bilateral": 0.25}

s3["full_cpts"]["D131"] = {
    "parents": ["R44", "R01"],
    "description": "ACS。心疾患既往+高齢がリスク",
    "cpt": {
        "no|18_39": 0.002, "no|40_64": 0.005, "no|65_plus": 0.010,
        "yes|18_39": 0.008, "yes|40_64": 0.020, "yes|65_plus": 0.040,
    }
}

# ============ D132 Aortic Dissection ============
s1["variables"].append({
    "id": "D132", "name": "aortic_dissection",
    "name_ja": "急性大動脈解離",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "胸痛(引き裂かれるような, 突然, 最初から最大)+背部痛。血圧左右差。"
           "CT造影で確定。Type A: 緊急手術。Type B: 降圧管理"
})
for to, reason in [
    ("S21", "大動脈解離: 胸痛(90%+, 引き裂かれるような, 突然最大)"),
    ("S22", "大動脈解離: 背部痛(50-70%, Type Bで多い)"),
    ("S04", "大動脈解離: 呼吸困難(30-40%)"),
    ("E02", "大動脈解離: 頻脈(40-50%)"),
    ("E03", "大動脈解離: 低血圧/ショック(Type A 20-30%)"),
    ("E33", "大動脈解離: 脈拍左右差/血管雑音(30-40%, 特徴的)"),
    ("E16", "大動脈解離: 意識障害(脳灌流低下10-15%)"),
    ("L01", "大動脈解離: WBC上昇(ストレス反応)"),
    ("L02", "大動脈解離: CRP上昇"),
    ("L16", "大動脈解離: LDH上昇"),
    ("E01", "大動脈解離: 通常無熱"),
    ("T01", "大動脈解離: 超急性(数分~数時間)"),
    ("T02", "大動脈解離: 突然発症(最初から最大)"),
    ("S13", "大動脈解離: 嘔気(20-30%)"),
    ("E15", "大動脈解離: 心雑音(大動脈弁閉鎖不全, Type Aで)"),
]:
    s2["edges"].append({"from": "D132", "to": to, "from_name": "aortic_dissection", "to_name": to, "reason": reason})

n["S21"]["parent_effects"]["D132"] = {"absent": 0.05, "pleuritic": 0.10, "constant": 0.85}
n["S22"]["parent_effects"]["D132"] = {"absent": 0.30, "present": 0.70}
n["S04"]["parent_effects"]["D132"] = {"absent": 0.55, "on_exertion": 0.15, "at_rest": 0.30}
n["E02"]["parent_effects"]["D132"] = {"under_100": 0.35, "100_120": 0.40, "over_120": 0.25}
n["E03"]["parent_effects"]["D132"] = {"normal_over_90": 0.65, "hypotension_under_90": 0.35}
n["E33"]["parent_effects"]["D132"] = {"absent": 0.55, "present": 0.45}
n["E16"]["parent_effects"]["D132"] = {"normal": 0.80, "confused": 0.12, "obtunded": 0.08}
n["L01"]["parent_effects"]["D132"] = {"low_under_4000": 0.02, "normal_4000_10000": 0.30, "high_10000_20000": 0.50, "very_high_over_20000": 0.18}
n["L02"]["parent_effects"]["D132"] = {"normal_under_0.3": 0.10, "mild_0.3_3": 0.25, "moderate_3_10": 0.40, "high_over_10": 0.25}
n["L16"]["parent_effects"]["D132"] = {"normal": 0.35, "elevated": 0.65}
n["E01"]["parent_effects"]["D132"] = {"under_37.5": 0.75, "37.5_38.0": 0.15, "38.0_39.0": 0.08, "39.0_40.0": 0.02, "over_40.0": 0.00}
n["T01"]["parent_effects"]["D132"] = {"under_3d": 0.85, "3d_to_1w": 0.12, "1w_to_3w": 0.02, "over_3w": 0.01}
n["T02"]["parent_effects"]["D132"] = {"sudden_hours": 0.90, "gradual_days": 0.10}
n["S13"]["parent_effects"]["D132"] = {"absent": 0.70, "present": 0.30}
n["E15"]["parent_effects"]["D132"] = {"absent": 0.65, "pre_existing": 0.05, "new": 0.30}

s3["full_cpts"]["D132"] = {
    "parents": ["R01"],
    "description": "大動脈解離。高血圧+高齢がリスク",
    "cpt": {"18_39": 0.001, "40_64": 0.003, "65_plus": 0.005}
}

s2["total_edges"] = len(s2["edges"])

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D131 ACS: 18 edges")
print(f"D132 Aortic Dissection: 15 edges")
print(f"Total: {s2['total_edges']} edges, 132 diseases")
