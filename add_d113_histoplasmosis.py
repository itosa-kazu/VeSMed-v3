#!/usr/bin/env python3
"""Add D113 Disseminated Histoplasmosis (播種性ヒストプラズマ症).

Clinical basis:
  Histoplasma capsulatum。Ohio/Mississippi valley, 中南米, 東南アジアに流行。
  免疫不全(HIV CD4<150, 臓器移植)で播種性を呈する。
  発熱(95%), 体重減少(70%), 肝脾腫(60-80%), 汎血球減少(50-70%),
  リンパ節腫脹(30-50%), 咳嗽(40-60%), 皮膚病変(10-20% HIV),
  LDH著明上昇, フェリチン上昇
  References: Wheat LJ et al. Medicine 1990;69:361
              Adenis A et al. Curr Opin Infect Dis 2014;27:466
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
    "id": "D113",
    "name": "disseminated_histoplasmosis",
    "name_ja": "播種性ヒストプラズマ症",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "Histoplasma capsulatum。免疫不全(HIV CD4<150)で播種性。"
           "発熱+体重減少+肝脾腫+汎血球減少+LDH/フェリチン著明上昇。"
           "CXR: 粟粒影/びまん性浸潤影。流行地渡航歴。診断: 尿/血清抗原, 骨髄培養"
})
print("step1: Added D113 disseminated_histoplasmosis")

# ── step2 ──
d_edges = [
    ("E01",  "ヒストプラズマ播種性: 発熱(95%), 中等度~高熱, 持続性"),
    ("S17",  "ヒストプラズマ播種性: 体重減少(70%)"),
    ("E34",  "ヒストプラズマ播種性: 肝腫大(60-80%)"),
    ("E14",  "ヒストプラズマ播種性: 脾腫(60-80%)"),
    ("E13",  "ヒストプラズマ播種性: リンパ節腫脹(30-50%, 全身性が多い)"),
    ("S01",  "ヒストプラズマ播種性: 咳嗽(40-60%, 肺病変)"),
    ("S04",  "ヒストプラズマ播種性: 呼吸困難(20-40%, 肺病変重症時)"),
    ("L01",  "ヒストプラズマ播種性: WBC低下(汎血球減少50-70%)"),
    ("L14",  "ヒストプラズマ播種性: 血小板減少(汎血球減少の一部)"),
    ("L16",  "ヒストプラズマ播種性: LDH著明上昇(80-90%, 診断的)"),
    ("L15",  "ヒストプラズマ播種性: フェリチン上昇(60-80%, >500が多い)"),
    ("L11",  "ヒストプラズマ播種性: 肝酵素上昇(40-60%, 肝浸潤)"),
    ("L02",  "ヒストプラズマ播種性: CRP上昇(中等度~高度)"),
    ("L28",  "ヒストプラズマ播種性: ESR上昇"),
    ("L04",  "ヒストプラズマ播種性: CXR異常(粟粒影/びまん性浸潤影50-70%)"),
    ("S07",  "ヒストプラズマ播種性: 倦怠感(80-90%)"),
    ("E12",  "ヒストプラズマ播種性: 皮膚病変(10-20% HIV, 丘疹/潰瘍/紫斑)"),
    ("T01",  "ヒストプラズマ播種性: 亜急性~慢性(数週~数ヶ月)"),
    ("T02",  "ヒストプラズマ播種性: 緩徐発症"),
    ("S13",  "ヒストプラズマ播種性: 嘔気/下痢(消化管浸潤20-30%)"),
]

r_edges = [
    ("R25", "D113", "HIV陽性: ヒストプラズマ播種性の最大リスク(CD4<150)"),
    ("R05", "D113", "免疫不全(臓器移植/ステロイド): ヒストプラズマ播種性リスク"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D113", "to": to_id,
        "from_name": "disseminated_histoplasmosis", "to_name": to_id,
        "reason": reason
    })
for from_id, to_id, reason in r_edges:
    s2["edges"].append({
        "from": from_id, "to": to_id,
        "from_name": from_id, "to_name": "disseminated_histoplasmosis",
        "reason": reason
    })
s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} D-edges + {len(r_edges)} R-edges")

# ── step3: noisy_or_params ──
n = s3["noisy_or_params"]

# E01: 高熱(95%), 持続性
n["E01"]["parent_effects"]["D113"] = {
    "under_37.5": 0.05, "37.5_38.0": 0.10, "38.0_39.0": 0.35,
    "39.0_40.0": 0.35, "over_40.0": 0.15
}
# S17: 体重減少(70%)
n["S17"]["parent_effects"]["D113"] = {"absent": 0.30, "present": 0.70}
# E34: 肝腫大(60-80%)
n["E34"]["parent_effects"]["D113"] = {"absent": 0.25, "present": 0.75}
# E14: 脾腫(60-80%)
n["E14"]["parent_effects"]["D113"] = {"absent": 0.25, "present": 0.75}
# E13: リンパ節(30-50%, 全身性)
n["E13"]["parent_effects"]["D113"] = {"absent": 0.50, "cervical": 0.10, "generalized": 0.40}
# S01: 咳嗽(40-60%)
n["S01"]["parent_effects"]["D113"] = {"absent": 0.45, "dry": 0.30, "productive": 0.25}
# S04: 呼吸困難(20-40%)
n["S04"]["parent_effects"]["D113"] = {"absent": 0.60, "on_exertion": 0.25, "at_rest": 0.15}
# L01: WBC低下(汎血球減少)
n["L01"]["parent_effects"]["D113"] = {
    "low_under_4000": 0.50, "normal_4000_10000": 0.35,
    "high_10000_20000": 0.10, "very_high_over_20000": 0.05
}
# L14: 血小板減少
n["L14"]["parent_effects"]["D113"] = {
    "normal": 0.35, "left_shift": 0.05, "atypical_lymphocytes": 0.05,
    "thrombocytopenia": 0.50, "eosinophilia": 0.05
}
# L16: LDH著明上昇(80-90%)
n["L16"]["parent_effects"]["D113"] = {"normal": 0.10, "elevated": 0.90}
# L15: フェリチン上昇(60-80%)
n["L15"]["parent_effects"]["D113"] = {
    "normal": 0.15, "mild_elevated": 0.25,
    "very_high_over_1000": 0.40, "extreme_over_10000": 0.20
}
# L11: 肝酵素(40-60%上昇)
n["L11"]["parent_effects"]["D113"] = {"normal": 0.40, "mild_elevated": 0.45, "very_high": 0.15}
# L02: CRP中等度~高度
n["L02"]["parent_effects"]["D113"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.15,
    "moderate_3_10": 0.40, "high_over_10": 0.40
}
# L28: ESR上昇
n["L28"]["parent_effects"]["D113"] = {"normal": 0.10, "elevated": 0.50, "very_high_over_100": 0.40}
# L04: CXR(粟粒影/びまん性浸潤)
n["L04"]["parent_effects"]["D113"] = {
    "normal": 0.30, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.40,
    "BHL": 0.10, "pleural_effusion": 0.15
}
# S07: 倦怠感(80-90%)
n["S07"]["parent_effects"]["D113"] = {"absent": 0.10, "mild": 0.25, "severe": 0.65}
# E12: 皮膚(10-20%, HIV)
n["E12"]["parent_effects"]["D113"] = {
    "normal": 0.75, "localized_erythema_warmth_swelling": 0.03,
    "petechiae_purpura": 0.05, "maculopapular_rash": 0.07,
    "vesicular_dermatomal": 0.02, "diffuse_erythroderma": 0.02,
    "purpura": 0.03, "vesicle_bulla": 0.01, "skin_necrosis": 0.02
}
# T01: 亜急性~慢性
n["T01"]["parent_effects"]["D113"] = {
    "under_3d": 0.02, "3d_to_1w": 0.08, "1w_to_3w": 0.35, "over_3w": 0.55
}
# T02: 緩徐
n["T02"]["parent_effects"]["D113"] = {"sudden_hours": 0.05, "gradual_days": 0.95}
# S13: GI症状(20-30%)
n["S13"]["parent_effects"]["D113"] = {"absent": 0.70, "present": 0.30}

print(f"step3: Added {len(d_edges)} noisy_or CPTs")

# ── full_cpt ──
s3["full_cpts"]["D113"] = {
    "parents": ["R25", "R05"],
    "description": "播種性ヒストプラズマ症。HIV/免疫不全が主要リスク",
    "cpt": {
        "no|no":  0.001,
        "no|yes": 0.005,
        "yes|no": 0.010,
        "yes|yes": 0.020
    }
}
print("step3: Added full_cpt (R25, R05 -> D113)")

# ── Save ──
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nAll saved. 113 diseases, {s2['total_edges']} edges.")
