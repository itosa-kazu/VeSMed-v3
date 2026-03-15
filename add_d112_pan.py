#!/usr/bin/env python3
"""Add D112 Polyarteritis Nodosa (結節性多発動脈炎/PAN).

Clinical basis:
  中型血管炎。男女比2:1, 40-60歳ピーク。肺を除く全臓器を侵す。
  全身症状: 発熱(52%), 体重減少(44%), 倦怠感(60-80%), 筋肉痛(70%)
  皮膚: livedo reticularis/紫斑/皮膚壊死/結節(44%)
  筋骨格: 関節痛(30%), 筋痛(70%)
  消化器: 腹痛(33%), 消化管出血
  腎臓: 高血圧(30%), 腎不全
  神経: 多発性単神経炎(50-75%)
  精巣痛(18-25%)
  検査: ESR↑(90%), CRP↑, WBC軽度↑, ANCA通常陰性
  HBV関連(歴史的に10-30%, 現在は稀)
  References: Hernández-Rodríguez J et al. Medicine 2004;83:292
              Korean PAN study: Kor J Int Med 2000 (PMC2729876)
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# ── step1: add disease node ──
s1["variables"].append({
    "id": "D112",
    "name": "polyarteritis_nodosa",
    "name_ja": "結節性多発動脈炎（PAN）",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "中型血管炎。肺を除く全臓器を侵す。発熱+体重減少+筋痛+紫斑/皮膚壊死+腹痛+末梢神経障害。"
           "ESR著明上昇, ANCA通常陰性。HBV関連あり。診断: 血管造影(微小動脈瘤)+生検"
})
print("step1: Added D112 polyarteritis_nodosa")

# ── step2: D→symptom/sign/lab edges ──
d_edges = [
    ("E01",  "PAN: 発熱(52%), 通常微熱~中等度"),
    ("S06",  "PAN: 筋肉痛(70%, 圧痛を伴うことが多い, 特に下腿)"),
    ("S07",  "PAN: 倦怠感(60-80%)"),
    ("S08",  "PAN: 関節痛(30%, 非破壊性)"),
    ("S17",  "PAN: 体重減少(44%, 数kg/月)"),
    ("E12",  "PAN: 皮膚所見(44%) — livedo reticularis/紫斑/皮膚壊死/皮下結節"),
    ("S12",  "PAN: 腹痛(33%, 腸間膜血管炎による虚血性腸炎)"),
    ("L01",  "PAN: WBC正常~軽度上昇"),
    ("L02",  "PAN: CRP上昇(中等度~高度)"),
    ("L28",  "PAN: ESR著明上昇(90%, 平均60-80mm/h)"),
    ("L11",  "PAN: 肝酵素上昇(HBV関連, 10-20%)"),
    ("L19",  "PAN: ANCA通常陰性(80%), p-ANCA陽性が20%程度"),
    ("T01",  "PAN: 慢性経過(数週~数ヶ月)"),
    ("T02",  "PAN: 緩徐発症"),
    ("S13",  "PAN: 嘔気(消化器血管炎, 20-30%)"),
    ("S44",  "PAN: 出血傾向 — 紫斑/消化管出血(15-20%)"),
    ("S15",  "PAN: 側腹部痛(腎梗塞/腎動脈瘤, 15-25%)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D112", "to": to_id,
        "from_name": "polyarteritis_nodosa", "to_name": to_id,
        "reason": reason
    })

s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} edges")
print(f"  New total_edges: {s2['total_edges']}")

# ── step3: noisy_or_params ──
n = s3["noisy_or_params"]

# E01: 発熱(52%), 微熱~中等度
n["E01"]["parent_effects"]["D112"] = {
    "under_37.5": 0.30, "37.5_38.0": 0.30, "38.0_39.0": 0.25,
    "39.0_40.0": 0.10, "over_40.0": 0.05
}
# S06: 筋肉痛(70%)
n["S06"]["parent_effects"]["D112"] = {"absent": 0.30, "present": 0.70}
# S07: 倦怠感(60-80%)
n["S07"]["parent_effects"]["D112"] = {"absent": 0.15, "mild": 0.30, "severe": 0.55}
# S08: 関節痛(30%)
n["S08"]["parent_effects"]["D112"] = {"absent": 0.70, "present": 0.30}
# S17: 体重減少(44%)
n["S17"]["parent_effects"]["D112"] = {"absent": 0.55, "present": 0.45}
# E12: 皮膚(44%) — 紫斑/皮膚壊死が特徴的
n["E12"]["parent_effects"]["D112"] = {
    "normal": 0.50, "localized_erythema_warmth_swelling": 0.05,
    "petechiae_purpura": 0.10, "maculopapular_rash": 0.05,
    "vesicular_dermatomal": 0.02, "diffuse_erythroderma": 0.03,
    "purpura": 0.10, "vesicle_bulla": 0.05, "skin_necrosis": 0.10
}
# S12: 腹痛(33%, diffuse)
n["S12"]["parent_effects"]["D112"] = {
    "absent": 0.65, "epigastric": 0.05, "RUQ": 0.03,
    "RLQ": 0.03, "LLQ": 0.02, "suprapubic": 0.02, "diffuse": 0.20
}
# L01: WBC正常~軽度上昇
n["L01"]["parent_effects"]["D112"] = {
    "low_under_4000": 0.05, "normal_4000_10000": 0.45,
    "high_10000_20000": 0.40, "very_high_over_20000": 0.10
}
# L02: CRP中等度~高度
n["L02"]["parent_effects"]["D112"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.10,
    "moderate_3_10": 0.40, "high_over_10": 0.45
}
# L28: ESR著明上昇(90%)
n["L28"]["parent_effects"]["D112"] = {"normal": 0.10, "elevated": 0.45, "very_high_over_100": 0.45}
# L11: 肝酵素(HBV関連10-20%)
n["L11"]["parent_effects"]["D112"] = {"normal": 0.75, "mild_elevated": 0.20, "very_high": 0.05}
# L19: ANCA(通常陰性80%, p-ANCA 20%)
n["L19"]["parent_effects"]["D112"] = {"negative": 0.80, "c_ANCA": 0.02, "p_ANCA": 0.18}
# T01: 慢性(数週~数ヶ月)
n["T01"]["parent_effects"]["D112"] = {
    "under_3d": 0.02, "3d_to_1w": 0.08, "1w_to_3w": 0.30, "over_3w": 0.60
}
# T02: 緩徐
n["T02"]["parent_effects"]["D112"] = {"sudden_hours": 0.05, "gradual_days": 0.95}
# S13: 嘔気(20-30%)
n["S13"]["parent_effects"]["D112"] = {"absent": 0.70, "present": 0.30}
# S44: 出血傾向(15-20%)
n["S44"]["parent_effects"]["D112"] = {"absent": 0.80, "present": 0.20}
# S15: 側腹部痛(15-25%)
n["S15"]["parent_effects"]["D112"] = {"absent": 0.75, "present": 0.25}

print(f"step3: Added {len(d_edges)} noisy_or CPTs")

# ── step3: full_cpt (no specific risk factor parents, use empty like D60) ──
s3["full_cpts"]["D112"] = {
    "parents": [],
    "description": "結節性多発動脈炎。中型血管炎。40-60歳男性に好発",
    "cpt": {
        "": 0.003
    }
}
print("step3: Added full_cpt for D112")

# ── Save ──
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("\nAll saved. 112 diseases total.")
