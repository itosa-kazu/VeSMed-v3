#!/usr/bin/env python3
"""Add D114 Multiple Myeloma (多発性骨髄腫).

Clinical basis:
  形質細胞腫瘍。ピーク65-70歳、男女比1.5:1。
  CRAB: Calcium↑(28%), Renal failure(20-50%), Anemia(70%), Bone lesions(80%)
  FUOとして: 繰り返す感染(免疫不全)+腫瘍熱, 発熱(10-20%が初発症状)
  骨痛(腰/肋骨, 58-70%), 倦怠感(>80%), 体重減少(24%)
  ESR著明上昇(>100が多い, 診断的手がかり)
  References: Kyle RA et al. Mayo Clin Proc 2003;78:21-33
              Rajkumar SV. Am J Hematol 2022;97:1086
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# ── step1 ──
s1["variables"].append({
    "id": "D114",
    "name": "multiple_myeloma",
    "name_ja": "多発性骨髄腫",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "high",
    "note": "形質細胞腫瘍。高齢者のFUO。CRAB(Ca↑/腎不全/貧血/骨病変)。"
           "骨痛(58-70%)+倦怠感+体重減少。ESR著明上昇(>100)が診断手がかり。"
           "繰り返す感染(免疫不全)。診断: 血清蛋白電気泳動/骨髄生検"
})
print("step1: Added D114 multiple_myeloma")

# ── step2 ──
d_edges = [
    ("E01",  "骨髄腫: 発熱(10-20%が初発, 感染合併or腫瘍熱), 通常微熱"),
    ("S07",  "骨髄腫: 倦怠感(>80%, 貧血+腫瘍負荷)"),
    ("S17",  "骨髄腫: 体重減少(24%)"),
    ("S08",  "骨髄腫: 骨痛→関節痛(58-70%, 腰椎/肋骨/骨盤が多い)"),
    ("S15",  "骨髄腫: 腰背部痛(40-50%, 椎体圧迫骨折)"),
    ("L01",  "骨髄腫: WBC通常正常, 進行期で低下(免疫不全)"),
    ("L02",  "骨髄腫: CRP軽度~中等度上昇(IL-6関連)"),
    ("L28",  "骨髄腫: ESR著明上昇(>100mm/hが多い, M蛋白によるrouleaux)"),
    ("L16",  "骨髄腫: LDH上昇(腫瘍負荷)"),
    ("L11",  "骨髄腫: 肝酵素通常正常"),
    ("L44",  "骨髄腫: 電解質異常(高Ca血症28% → other)"),
    ("L14",  "骨髄腫: 血小板減少(進行期, 骨髄浸潤)"),
    ("T01",  "骨髄腫: 慢性経過(数ヶ月~)"),
    ("T02",  "骨髄腫: 緩徐発症"),
    ("E16",  "骨髄腫: 意識障害(高Ca血症による, 5-10%)"),
    ("S13",  "骨髄腫: 嘔気(高Ca血症/腎不全, 15-20%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D114", "to": to_id,
        "from_name": "multiple_myeloma", "to_name": to_id,
        "reason": reason
    })
s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} edges")

# ── step3: noisy_or_params ──
n = s3["noisy_or_params"]

# E01: 微熱主体(10-20%が初発)
n["E01"]["parent_effects"]["D114"] = {
    "under_37.5": 0.40, "37.5_38.0": 0.30, "38.0_39.0": 0.20,
    "39.0_40.0": 0.08, "over_40.0": 0.02
}
# S07: 倦怠感(>80%)
n["S07"]["parent_effects"]["D114"] = {"absent": 0.10, "mild": 0.25, "severe": 0.65}
# S17: 体重減少(24%)
n["S17"]["parent_effects"]["D114"] = {"absent": 0.75, "present": 0.25}
# S08: 骨痛→関節痛(58-70%)
n["S08"]["parent_effects"]["D114"] = {"absent": 0.35, "present": 0.65}
# S15: 腰背部痛(40-50%)
n["S15"]["parent_effects"]["D114"] = {"absent": 0.50, "present": 0.50}
# L01: WBC通常正常~低下
n["L01"]["parent_effects"]["D114"] = {
    "low_under_4000": 0.25, "normal_4000_10000": 0.55,
    "high_10000_20000": 0.15, "very_high_over_20000": 0.05
}
# L02: CRP軽度~中等度
n["L02"]["parent_effects"]["D114"] = {
    "normal_under_0.3": 0.15, "mild_0.3_3": 0.30,
    "moderate_3_10": 0.35, "high_over_10": 0.20
}
# L28: ESR著明上昇(>100が多い!) — 骨髄腫の最大手がかり
n["L28"]["parent_effects"]["D114"] = {"normal": 0.05, "elevated": 0.25, "very_high_over_100": 0.70}
# L16: LDH上昇
n["L16"]["parent_effects"]["D114"] = {"normal": 0.40, "elevated": 0.60}
# L11: 肝酵素通常正常
n["L11"]["parent_effects"]["D114"] = {"normal": 0.85, "mild_elevated": 0.12, "very_high": 0.03}
# L44: 高Ca血症(28%)
n["L44"]["parent_effects"]["D114"] = {
    "normal": 0.65, "hyponatremia": 0.05, "hyperkalemia": 0.02, "other": 0.28
}
# L14: 血小板減少(進行期)
n["L14"]["parent_effects"]["D114"] = {
    "normal": 0.55, "left_shift": 0.05, "atypical_lymphocytes": 0.02,
    "thrombocytopenia": 0.35, "eosinophilia": 0.03
}
# T01: 慢性
n["T01"]["parent_effects"]["D114"] = {
    "under_3d": 0.02, "3d_to_1w": 0.03, "1w_to_3w": 0.15, "over_3w": 0.80
}
# T02: 緩徐
n["T02"]["parent_effects"]["D114"] = {"sudden_hours": 0.05, "gradual_days": 0.95}
# E16: 意識障害(高Ca)
n["E16"]["parent_effects"]["D114"] = {"normal": 0.88, "confused": 0.10, "obtunded": 0.02}
# S13: 嘔気
n["S13"]["parent_effects"]["D114"] = {"absent": 0.80, "present": 0.20}

print(f"step3: Added {len(d_edges)} noisy_or CPTs")

# ── full_cpt: 高齢者に好発 ──
s3["full_cpts"]["D114"] = {
    "parents": ["R01"],
    "description": "多発性骨髄腫。65-70歳ピーク",
    "cpt": {
        "18_39": 0.001,
        "40_64": 0.003,
        "65_plus": 0.008
    }
}
print("step3: Added full_cpt (R01 -> D114)")

# ── Save ──
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nAll saved. 114 diseases, {s2['total_edges']} edges.")
