#!/usr/bin/env python3
"""Add D119 Perinephric/Renal Abscess (腎/腎周囲膿瘍).

Clinical basis:
  腎盂腎炎(D09)の重症合併症。治療反応不良の腎盂腎炎で疑う。
  発熱(66-90%), 側腹部痛(40-50%), 悪寒(40%), 排尿痛(40%)
  尿所見正常が30%(血行性播種の場合)
  WBC上昇, CRP著高, PCT上昇
  CT造影で確定。膿瘍ドレナージ+抗菌薬が治療
  リスク: 糖尿病(30-40%), 尿路結石, 尿路奇形
  References: Yen DH et al. Urology 1999
              Coelho RF et al. Int Braz J Urol 2007
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
    "id": "D119",
    "name": "perinephric_abscess",
    "name_ja": "腎/腎周囲膿瘍",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "high",
    "note": "腎盂腎炎の重症合併症。側腹部痛+発熱+CVA叩打痛。"
           "尿所見正常が30%(血行性)。CT造影で確定。DM/尿路結石がリスク"
})

d_edges = [
    ("E01",  "腎周囲膿瘍: 発熱(66-90%), 高熱が多い"),
    ("S15",  "腎周囲膿瘍: 側腹部痛(70-80%, 持続性・片側性)"),
    ("E11",  "腎周囲膿瘍: CVA叩打痛(80-90%)"),
    ("S10",  "腎周囲膿瘍: 排尿痛(30-40%, 上行性感染の場合)"),
    ("S09",  "腎周囲膿瘍: 悪寒戦慄(40-50%)"),
    ("S13",  "腎周囲膿瘍: 嘔気嘔吐(30-40%)"),
    ("L01",  "腎周囲膿瘍: WBC上昇(80-90%)"),
    ("L02",  "腎周囲膿瘍: CRP著高(>10が多い)"),
    ("L03",  "腎周囲膿瘍: PCT上昇(細菌感染)"),
    ("L05",  "腎周囲膿瘍: 尿所見 — 膿尿(70%)だが正常30%(血行性)"),
    ("L09",  "腎周囲膿瘍: 血培陽性(20-40%, グラム陰性が多い)"),
    ("L31",  "腎周囲膿瘍: 腹部CT — 膿瘍像(abscess)"),
    ("L28",  "腎周囲膿瘍: ESR上昇"),
    ("T01",  "腎周囲膿瘍: 亜急性(数日~2週)"),
    ("T02",  "腎周囲膿瘍: 亜急性発症"),
    ("S07",  "腎周囲膿瘍: 倦怠感(60-70%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({"from": "D119", "to": to_id, "from_name": "perinephric_abscess", "to_name": to_id, "reason": reason})
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

# E11 was missing from noisy_or_params despite having edges. Add it.
if "E11" not in n:
    n["E11"] = {
        "description": "CVA叩打痛。腎盂腎炎/腎周囲膿瘍で陽性。",
        "leak": {"absent": 0.95, "present": 0.05},
        "parent_effects": {
            "D09": {"absent": 0.15, "present": 0.85},
            "D42": {"absent": 0.30, "present": 0.70},
        }
    }

n["E01"]["parent_effects"]["D119"] = {"under_37.5": 0.10, "37.5_38.0": 0.10, "38.0_39.0": 0.30, "39.0_40.0": 0.35, "over_40.0": 0.15}
n["S15"]["parent_effects"]["D119"] = {"absent": 0.20, "present": 0.80}
n["E11"]["parent_effects"]["D119"] = {"absent": 0.10, "present": 0.90}
n["S10"]["parent_effects"]["D119"] = {"absent": 0.60, "present": 0.40}
n["S09"]["parent_effects"]["D119"] = {"absent": 0.50, "present": 0.50}
n["S13"]["parent_effects"]["D119"] = {"absent": 0.60, "present": 0.40}
n["L01"]["parent_effects"]["D119"] = {"low_under_4000": 0.02, "normal_4000_10000": 0.10, "high_10000_20000": 0.50, "very_high_over_20000": 0.38}
n["L02"]["parent_effects"]["D119"] = {"normal_under_0.3": 0.02, "mild_0.3_3": 0.05, "moderate_3_10": 0.20, "high_over_10": 0.73}
n["L03"]["parent_effects"]["D119"] = {"not_done": 0.25, "low_under_0.25": 0.05, "gray_0.25_0.5": 0.10, "high_over_0.5": 0.60}
n["L05"]["parent_effects"]["D119"] = {"normal": 0.30, "pyuria_bacteriuria": 0.70}
n["L09"]["parent_effects"]["D119"] = {"not_done_or_pending": 0.20, "negative": 0.40, "gram_positive": 0.10, "gram_negative": 0.30}
n["L31"]["parent_effects"]["D119"] = {"normal": 0.05, "abscess": 0.85, "mass": 0.05, "other_abnormal": 0.05}
n["L28"]["parent_effects"]["D119"] = {"normal": 0.10, "elevated": 0.50, "very_high_over_100": 0.40}
n["T01"]["parent_effects"]["D119"] = {"under_3d": 0.10, "3d_to_1w": 0.45, "1w_to_3w": 0.35, "over_3w": 0.10}
n["T02"]["parent_effects"]["D119"] = {"sudden_hours": 0.20, "gradual_days": 0.80}
n["S07"]["parent_effects"]["D119"] = {"absent": 0.25, "mild": 0.30, "severe": 0.45}

s3["full_cpts"]["D119"] = {"parents": ["R04"], "description": "腎周囲膿瘍。糖尿病がリスク",
    "cpt": {"no": 0.003, "yes": 0.008}}

for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D119: {len(d_edges)} edges. Total: {s2['total_edges']}")
