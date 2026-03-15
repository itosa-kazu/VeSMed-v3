#!/usr/bin/env python3
"""Add D117 Spinal Epidural Abscess (脊椎硬膜外膿瘍).

Clinical basis:
  ER見逃し率56%(全疾患中最高)。4段階進行:
  Stage 1: 背部痛+発熱+圧痛
  Stage 2: 放散痛+項部硬直+反射亢進
  Stage 3: 感覚鈍麻+筋力低下+膀胱直腸障害
  Stage 4: 麻痺
  古典的3徴(背部痛+発熱+神経症状)は8-15%のみ。
  起炎菌: S.aureus 62%, M.tuberculosis
  リスク: 糖尿病, IVDU, 免疫不全, 脊椎手術後
  検査: WBC上昇, CRP著高, ESR著高(>90%), 血培陽性(60%)
  MRIが診断gold standard
  References: Darouiche RO. NEJM 2006;355:2012
              AHRQ Diagnostic Errors Systematic Review 2022
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# step1
s1["variables"].append({
    "id": "D117",
    "name": "spinal_epidural_abscess",
    "name_ja": "脊椎硬膜外膿瘍",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "ER見逃し率56%。背部痛+発熱(初期)+神経症状(進行期)。"
           "古典的3徴は8-15%のみ。S.aureus 62%。糖尿病/IVDU/免疫不全がリスク。"
           "ESR/CRP著高。血培陽性60%。MRIで確定。緊急手術が必要"
})
print("step1: Added D117 spinal_epidural_abscess")

# step2
d_edges = [
    ("E01",  "硬膜外膿瘍: 発熱(50-70%, Stage 1で出現, 進行後は消退もあり)"),
    ("S22",  "硬膜外膿瘍: 背部痛(90-95%, 最も早い症状, 限局性+圧痛)"),
    ("S15",  "硬膜外膿瘍: 側腹部痛/腰背部痛(50-70%, 放散痛Stage 2)"),
    ("E06",  "硬膜外膿瘍: 項部硬直(20-30%, Stage 2, 頸椎病変で多い)"),
    ("S06",  "硬膜外膿瘍: 筋肉痛/圧痛(30-40%, 傍脊柱筋)"),
    ("E16",  "硬膜外膿瘍: 意識障害(10-20%, 敗血症合併時)"),
    ("L01",  "硬膜外膿瘍: WBC上昇(60-80%)"),
    ("L02",  "硬膜外膿瘍: CRP著高(80-95%)"),
    ("L28",  "硬膜外膿瘍: ESR著高(>90%, 平均70-100mm/h)"),
    ("L03",  "硬膜外膿瘍: プロカルシトニン上昇(細菌感染)"),
    ("L09",  "硬膜外膿瘍: 血培陽性(50-60%, グラム陽性=S.aureus)"),
    ("T01",  "硬膜外膿瘍: 急性(数日)~亜急性(1-2週)"),
    ("T02",  "硬膜外膿瘍: 急性~亜急性発症"),
    ("S09",  "硬膜外膿瘍: 悪寒戦慄(菌血症, 30-40%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D117", "to": to_id,
        "from_name": "spinal_epidural_abscess", "to_name": to_id,
        "reason": reason
    })
s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} edges (total: {s2['total_edges']})")

# step3
n = s3["noisy_or_params"]

n["E01"]["parent_effects"]["D117"] = {
    "under_37.5": 0.20, "37.5_38.0": 0.20, "38.0_39.0": 0.30,
    "39.0_40.0": 0.20, "over_40.0": 0.10
}
n["S22"]["parent_effects"]["D117"] = {"absent": 0.05, "present": 0.95}
n["S15"]["parent_effects"]["D117"] = {"absent": 0.30, "present": 0.70}
n["E06"]["parent_effects"]["D117"] = {"absent": 0.70, "present": 0.30}
n["S06"]["parent_effects"]["D117"] = {"absent": 0.60, "present": 0.40}
n["E16"]["parent_effects"]["D117"] = {"normal": 0.80, "confused": 0.15, "obtunded": 0.05}
n["L01"]["parent_effects"]["D117"] = {
    "low_under_4000": 0.03, "normal_4000_10000": 0.20,
    "high_10000_20000": 0.50, "very_high_over_20000": 0.27
}
n["L02"]["parent_effects"]["D117"] = {
    "normal_under_0.3": 0.02, "mild_0.3_3": 0.05,
    "moderate_3_10": 0.25, "high_over_10": 0.68
}
n["L28"]["parent_effects"]["D117"] = {"normal": 0.05, "elevated": 0.30, "very_high_over_100": 0.65}
n["L03"]["parent_effects"]["D117"] = {
    "not_done": 0.30, "low_under_0.25": 0.05,
    "gray_0.25_0.5": 0.15, "high_over_0.5": 0.50
}
n["L09"]["parent_effects"]["D117"] = {
    "not_done_or_pending": 0.15, "negative": 0.25,
    "gram_positive": 0.50, "gram_negative": 0.10
}
n["T01"]["parent_effects"]["D117"] = {
    "under_3d": 0.15, "3d_to_1w": 0.45, "1w_to_3w": 0.30, "over_3w": 0.10
}
n["T02"]["parent_effects"]["D117"] = {"sudden_hours": 0.25, "gradual_days": 0.75}
n["S09"]["parent_effects"]["D117"] = {"absent": 0.60, "present": 0.40}

print(f"step3: Added {len(d_edges)} CPTs")

# full_cpt: 糖尿病+免疫不全がリスク
s3["full_cpts"]["D117"] = {
    "parents": ["R04", "R05"],
    "description": "脊椎硬膜外膿瘍。糖尿病/免疫不全がリスク",
    "cpt": {
        "no|no": 0.002,
        "no|yes": 0.006,
        "yes|no": 0.005,
        "yes|yes": 0.012
    }
}

for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved. 117 diseases, {s2['total_edges']} edges.")
