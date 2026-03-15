#!/usr/bin/env python3
"""Add D115 Disseminated Gonococcal Infection (播種性淋菌感染症/DGI).

Clinical basis:
  Neisseria gonorrhoeae菌血症。性活動活発な若年成人(15-35歳, 女性>男性)。
  2型: (1)関節炎-皮膚炎症候群(60%): 遊走性多関節痛+腱鞘炎+皮疹(膿疱/点状出血)
       (2)化膿性関節炎(40%): 単関節の敗血症性関節炎
  発熱(60-80%), 多関節痛(80-90%), 皮膚病変(50-75%), 腱鞘炎(60-70%)
  WBC軽度上昇, CRP軽度~中等度, 血培陽性10-30%, 関節液培養20-50%
  References: Rice PA. NEJM 2005;353:1109-15, Barbee LA et al. MMWR 2023
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
    "id": "D115",
    "name": "disseminated_gonococcal_infection",
    "name_ja": "播種性淋菌感染症（DGI）",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "high",
    "note": "淋菌菌血症。関節炎-皮膚炎症候群(遊走性多関節痛+膿疱性皮疹+腱鞘炎)が特徴的。"
           "若年性活動活発な成人、女性に多い。診断: 血培/関節液培養/NAAT"
})
print("step1: Added D115")

# step2
d_edges = [
    ("E01",  "DGI: 発熱(60-80%), 中等度~高熱"),
    ("S08",  "DGI: 多関節痛(80-90%, 遊走性, 膝/手首/足首)"),
    ("S23",  "DGI: 関節腫脹(60-70%, 多関節型が多い)"),
    ("E21",  "DGI: 関節発赤・熱感(50-60%)"),
    ("E12",  "DGI: 皮膚(50-75%) — 膿疱/点状出血, 四肢遠位に多い"),
    ("S18",  "DGI: 皮膚の訴え(50-70%, 発疹)"),
    ("S10",  "DGI: 排尿時痛(30-50%, 原発巣の尿道炎/子宮頸管炎)"),
    ("L01",  "DGI: WBC軽度上昇"),
    ("L02",  "DGI: CRP軽度~中等度上昇"),
    ("L09",  "DGI: 血培陽性(10-30%, グラム陰性双球菌)"),
    ("L30",  "DGI: 関節液 — 炎症性~敗血症性(WBC高値, 培養20-50%陽性)"),
    ("L28",  "DGI: ESR軽度上昇"),
    ("T01",  "DGI: 急性~亜急性(3日~1週)"),
    ("T02",  "DGI: 亜急性発症(数日)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D115", "to": to_id,
        "from_name": "disseminated_gonococcal_infection", "to_name": to_id,
        "reason": reason
    })
s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} edges (total: {s2['total_edges']})")

# step3
n = s3["noisy_or_params"]

n["E01"]["parent_effects"]["D115"] = {
    "under_37.5": 0.15, "37.5_38.0": 0.20, "38.0_39.0": 0.35,
    "39.0_40.0": 0.25, "over_40.0": 0.05
}
n["S08"]["parent_effects"]["D115"] = {"absent": 0.10, "present": 0.90}
n["S23"]["parent_effects"]["D115"] = {"absent": 0.30, "monoarticular": 0.25, "polyarticular": 0.45}
n["E21"]["parent_effects"]["D115"] = {"absent": 0.40, "monoarticular": 0.25, "polyarticular": 0.35}
n["E12"]["parent_effects"]["D115"] = {
    "normal": 0.30, "localized_erythema_warmth_swelling": 0.05,
    "petechiae_purpura": 0.25, "maculopapular_rash": 0.15,
    "vesicular_dermatomal": 0.05, "diffuse_erythroderma": 0.02,
    "purpura": 0.10, "vesicle_bulla": 0.05, "skin_necrosis": 0.03
}
n["S18"]["parent_effects"]["D115"] = {"absent": 0.30, "localized_pain_redness": 0.25, "rash_widespread": 0.45}
n["S10"]["parent_effects"]["D115"] = {"absent": 0.55, "present": 0.45}
n["L01"]["parent_effects"]["D115"] = {
    "low_under_4000": 0.05, "normal_4000_10000": 0.35,
    "high_10000_20000": 0.45, "very_high_over_20000": 0.15
}
n["L02"]["parent_effects"]["D115"] = {
    "normal_under_0.3": 0.10, "mild_0.3_3": 0.35,
    "moderate_3_10": 0.35, "high_over_10": 0.20
}
n["L09"]["parent_effects"]["D115"] = {
    "not_done_or_pending": 0.20, "negative": 0.50,
    "gram_positive": 0.02, "gram_negative": 0.28
}
n["L30"]["parent_effects"]["D115"] = {
    "not_done": 0.30, "inflammatory": 0.30, "septic": 0.35, "crystals": 0.05
}
n["L28"]["parent_effects"]["D115"] = {"normal": 0.30, "elevated": 0.55, "very_high_over_100": 0.15}
n["T01"]["parent_effects"]["D115"] = {
    "under_3d": 0.15, "3d_to_1w": 0.55, "1w_to_3w": 0.25, "over_3w": 0.05
}
n["T02"]["parent_effects"]["D115"] = {"sudden_hours": 0.20, "gradual_days": 0.80}

print(f"step3: Added {len(d_edges)} CPTs")

s3["full_cpts"]["D115"] = {
    "parents": ["R01"],
    "description": "DGI。15-35歳の性活動活発な成人に好発",
    "cpt": {"18_39": 0.005, "40_64": 0.002, "65_plus": 0.001}
}
print("step3: Added full_cpt")

for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved. 115 diseases, {s2['total_edges']} edges.")
