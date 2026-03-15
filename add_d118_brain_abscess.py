#!/usr/bin/env python3
"""Add D118 Brain Abscess (脳膿瘍).

Clinical basis:
  古典的3徴(発熱+頭痛+局所神経症状)は14%のみ!
  頭痛(69-70%), 発熱(45-60%), 局所神経障害(50-65%),
  痙攣(25-35%), 嘔気嘔吐(40-50%), 意識障害(30-50%)
  WBC上昇(53%), CRP/ESR上昇, 血培陽性16%
  CT/MRI: 環状増強病変+周囲浮腫
  起炎菌: Streptococcus, Staphylococcus, グラム陰性桿菌
  感染源: 副鼻腔(30-50%), 心内膜炎, 歯原性, 外傷/手術後
  References: Brouwer MC et al. NEJM 2014;371:447
              BMC Infect Dis 2021 PMC8667431 (57例レトロ)
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
    "id": "D118",
    "name": "brain_abscess",
    "name_ja": "脳膿瘍",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "古典的3徴(発熱+頭痛+局所神経症状)は14%のみ。頭痛が最多(70%)。"
           "CT/MRI環状増強病変。副鼻腔/歯原性/心内膜炎が感染源。"
           "Streptococcus/Staphylococcus。緊急手術/ドレナージが必要"
})

d_edges = [
    ("E01",  "脳膿瘍: 発熱(45-60%, 古典的3徴の一部だが半数以下)"),
    ("S05",  "脳膿瘍: 頭痛(69-70%, 最多症状, 進行性)"),
    ("E16",  "脳膿瘍: 意識障害(30-50%, mass effectによる)"),
    ("S42",  "脳膿瘍: 痙攣(25-35%)"),
    ("S13",  "脳膿瘍: 嘔気嘔吐(40-50%, 頭蓋内圧亢進)"),
    ("E06",  "脳膿瘍: 項部硬直(20-30%, 髄膜刺激)"),
    ("L46",  "脳膿瘍: 頭部MRI/CT — 環状増強病変+浮腫(other)"),
    ("L01",  "脳膿瘍: WBC上昇(53%)"),
    ("L02",  "脳膿瘍: CRP上昇(中等度~高度)"),
    ("L28",  "脳膿瘍: ESR上昇"),
    ("L03",  "脳膿瘍: プロカルシトニン上昇(細菌感染)"),
    ("L09",  "脳膿瘍: 血培陽性(16%, 低い)"),
    ("T01",  "脳膿瘍: 亜急性(数日~数週)"),
    ("T02",  "脳膿瘍: 亜急性発症(日単位で進行)"),
    ("S07",  "脳膿瘍: 倦怠感(40-60%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D118", "to": to_id,
        "from_name": "brain_abscess", "to_name": to_id,
        "reason": reason
    })
s2["total_edges"] = len(s2["edges"])

n = s3["noisy_or_params"]

n["E01"]["parent_effects"]["D118"] = {
    "under_37.5": 0.30, "37.5_38.0": 0.20, "38.0_39.0": 0.25,
    "39.0_40.0": 0.15, "over_40.0": 0.10
}
n["S05"]["parent_effects"]["D118"] = {"absent": 0.25, "mild": 0.25, "severe": 0.50}
n["E16"]["parent_effects"]["D118"] = {"normal": 0.50, "confused": 0.30, "obtunded": 0.20}
n["S42"]["parent_effects"]["D118"] = {"absent": 0.65, "present": 0.35}
n["S13"]["parent_effects"]["D118"] = {"absent": 0.50, "present": 0.50}
n["E06"]["parent_effects"]["D118"] = {"absent": 0.70, "present": 0.30}
n["L46"]["parent_effects"]["D118"] = {
    "normal": 0.05, "temporal_lobe_lesion": 0.10,
    "diffuse_abnormal": 0.10, "other": 0.75
}
n["L01"]["parent_effects"]["D118"] = {
    "low_under_4000": 0.05, "normal_4000_10000": 0.40,
    "high_10000_20000": 0.40, "very_high_over_20000": 0.15
}
n["L02"]["parent_effects"]["D118"] = {
    "normal_under_0.3": 0.10, "mild_0.3_3": 0.15,
    "moderate_3_10": 0.35, "high_over_10": 0.40
}
n["L28"]["parent_effects"]["D118"] = {"normal": 0.15, "elevated": 0.50, "very_high_over_100": 0.35}
n["L03"]["parent_effects"]["D118"] = {
    "not_done": 0.30, "low_under_0.25": 0.10,
    "gray_0.25_0.5": 0.20, "high_over_0.5": 0.40
}
n["L09"]["parent_effects"]["D118"] = {
    "not_done_or_pending": 0.20, "negative": 0.55,
    "gram_positive": 0.15, "gram_negative": 0.10
}
n["T01"]["parent_effects"]["D118"] = {
    "under_3d": 0.10, "3d_to_1w": 0.35, "1w_to_3w": 0.40, "over_3w": 0.15
}
n["T02"]["parent_effects"]["D118"] = {"sudden_hours": 0.15, "gradual_days": 0.85}
n["S07"]["parent_effects"]["D118"] = {"absent": 0.35, "mild": 0.30, "severe": 0.35}

s3["full_cpts"]["D118"] = {
    "parents": [],
    "description": "脳膿瘍。副鼻腔/歯原性/心内膜炎由来",
    "cpt": {"": 0.003}
}

for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D118 brain_abscess: {len(d_edges)} edges. Total: {s2['total_edges']}")
