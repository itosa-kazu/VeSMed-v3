#!/usr/bin/env python3
"""Add D110 Toxoplasmosis (トキソプラズマ症).

Clinical basis:
  Toxoplasma gondii感染。2つの主要プレゼンテーション:
  (A) 免疫正常者: 頸部リンパ節腫脹(80-90%), 微熱, 倦怠感 → 自己限定性
  (B) 免疫不全者(HIV CD4<100等): トキソプラズマ脳炎 →
      発熱(60-80%), 頭痛(50-80%), 意識障害(30-60%), 痙攣(20-30%),
      MRI環状増強病変, 脈絡網膜炎(10-20%)
  References: UpToDate "Toxoplasmosis in HIV", Harrison's Ch.219,
              Luft BJ, Remington JS. NEJM 1992;327:1643-8
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
    "id": "D110",
    "name": "toxoplasmosis",
    "name_ja": "トキソプラズマ症（脳炎/リンパ節炎）",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "Toxoplasma gondii。免疫正常: 頸部リンパ節腫脹+微熱(自己限定)。"
           "免疫不全(HIV CD4<100): 脳炎(環状増強病変)+発熱+意識障害+痙攣。"
           "脈絡網膜炎(10-20%)。診断: IgG/IgM血清学, MRI, PCR"
})
print("step1: Added D110 toxoplasmosis")

# ── step2: D→symptom/sign/lab edges ──
# トキソプラズマ症の臨床所見:
#  免疫正常: 頸部リンパ節腫脹(80-90%), 微熱(20-40%), 倦怠感(40-60%), 筋肉痛(20-40%)
#  脳炎型: 発熱(60-80%), 頭痛(50-80%), 意識障害(30-60%), 痙攣(20-30%),
#          MRI環状増強(80-90%), 嘔気(20-30%), 脈絡網膜炎(10-20%)
#  共通: WBC正常, CRP軽度, 肝酵素軽度上昇(播種性), 亜急性経過
d_edges = [
    ("E01",  "トキソプラズマ: 発熱(免疫正常20-40%, 脳炎60-80%), 中等度"),
    ("S05",  "トキソプラズマ脳炎: 頭痛(50-80%), リンパ節型でも20-30%"),
    ("E13",  "トキソプラズマ: 頸部リンパ節腫脹(免疫正常80-90%), 全身性もあり"),
    ("S07",  "トキソプラズマ: 倦怠感(40-70%)"),
    ("S06",  "トキソプラズマ: 筋肉痛(20-40%)"),
    ("E16",  "トキソプラズマ脳炎: 意識障害(30-60%)"),
    ("S42",  "トキソプラズマ脳炎: 痙攣(20-30%)"),
    ("L46",  "トキソプラズマ脳炎: MRI環状増強病変(80-90%, 基底核に多発)"),
    ("E35",  "トキソプラズマ: 脈絡網膜炎(10-20%) → ぶどう膜炎"),
    ("L01",  "トキソプラズマ: WBC通常正常(免疫不全背景で低下もあり)"),
    ("L02",  "トキソプラズマ: CRP軽度~中等度上昇"),
    ("L11",  "トキソプラズマ: 肝酵素軽度上昇(播種性15-25%)"),
    ("E34",  "トキソプラズマ: 肝腫大(播種性10-20%)"),
    ("E14",  "トキソプラズマ: 脾腫(リンパ節型/播種性15-30%)"),
    ("T01",  "トキソプラズマ: 亜急性経過(1-3週)"),
    ("T02",  "トキソプラズマ: 緩徐発症"),
    ("L28",  "トキソプラズマ: ESR軽度上昇"),
    ("S13",  "トキソプラズマ脳炎: 嘔気嘔吐(頭蓋内圧亢進20-30%)"),
]

# R→D edges (risk factors)
r_edges = [
    ("R25", "D110", "HIV陽性: トキソプラズマ脳炎の最大リスク因子(CD4<100で好発)"),
    ("R05", "D110", "免疫不全(ステロイド/化学療法等): トキソプラズマ発症リスク上昇"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D110", "to": to_id,
        "from_name": "toxoplasmosis", "to_name": to_id,
        "reason": reason
    })

for from_id, to_id, reason in r_edges:
    s2["edges"].append({
        "from": from_id, "to": to_id,
        "from_name": from_id, "to_name": "toxoplasmosis",
        "reason": reason
    })

s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} D-edges + {len(r_edges)} R-edges = {len(d_edges)+len(r_edges)} total")
print(f"  New total_edges: {s2['total_edges']}")

# ── step3: noisy_or_params (D→symptom CPTs) ──
n = s3["noisy_or_params"]

# E01: 中等度発熱 (免疫正常20-40%, 脳炎60-80% → weighted average)
n["E01"]["parent_effects"]["D110"] = {
    "under_37.5": 0.15, "37.5_38.0": 0.25, "38.0_39.0": 0.35,
    "39.0_40.0": 0.20, "over_40.0": 0.05
}
# S05: 頭痛 (脳炎50-80%, リンパ節型20-30%)
n["S05"]["parent_effects"]["D110"] = {"absent": 0.25, "mild": 0.30, "severe": 0.45}
# E13: リンパ節腫脹 (頸部主体, 免疫正常80-90%)
n["E13"]["parent_effects"]["D110"] = {"absent": 0.30, "cervical": 0.50, "generalized": 0.20}
# S07: 倦怠感 (40-70%)
n["S07"]["parent_effects"]["D110"] = {"absent": 0.25, "mild": 0.35, "severe": 0.40}
# S06: 筋肉痛 (20-40%)
n["S06"]["parent_effects"]["D110"] = {"absent": 0.65, "present": 0.35}
# E16: 意識障害 (脳炎30-60%)
n["E16"]["parent_effects"]["D110"] = {"normal": 0.45, "confused": 0.35, "obtunded": 0.20}
# S42: 痙攣 (脳炎20-30%)
n["S42"]["parent_effects"]["D110"] = {"absent": 0.75, "present": 0.25}
# L46: 頭部MRI (脳炎: 環状増強病変80-90%, 基底核多発)
n["L46"]["parent_effects"]["D110"] = {
    "normal": 0.30, "temporal_lobe_lesion": 0.05,
    "diffuse_abnormal": 0.15, "other": 0.50
}
# E35: 眼症状 (脈絡網膜炎→ぶどう膜炎 10-20%)
n["E35"]["parent_effects"]["D110"] = {"absent": 0.80, "conjunctivitis": 0.05, "uveitis": 0.15}
# L01: WBC (通常正常, 免疫不全で低下もあり)
n["L01"]["parent_effects"]["D110"] = {
    "low_under_4000": 0.15, "normal_4000_10000": 0.60,
    "high_10000_20000": 0.20, "very_high_over_20000": 0.05
}
# L02: CRP (軽度~中等度)
n["L02"]["parent_effects"]["D110"] = {
    "normal_under_0.3": 0.15, "mild_0.3_3": 0.40,
    "moderate_3_10": 0.30, "high_over_10": 0.15
}
# L11: 肝酵素 (播種性で軽度上昇15-25%)
n["L11"]["parent_effects"]["D110"] = {"normal": 0.70, "mild_elevated": 0.25, "very_high": 0.05}
# E34: 肝腫大 (播種性10-20%)
n["E34"]["parent_effects"]["D110"] = {"absent": 0.85, "present": 0.15}
# E14: 脾腫 (15-30%)
n["E14"]["parent_effects"]["D110"] = {"absent": 0.75, "present": 0.25}
# T01: 亜急性 (1-3週)
n["T01"]["parent_effects"]["D110"] = {
    "under_3d": 0.05, "3d_to_1w": 0.20, "1w_to_3w": 0.50, "over_3w": 0.25
}
# T02: 緩徐発症
n["T02"]["parent_effects"]["D110"] = {"sudden_hours": 0.10, "gradual_days": 0.90}
# L28: ESR軽度上昇
n["L28"]["parent_effects"]["D110"] = {"normal": 0.35, "elevated": 0.50, "very_high_over_100": 0.15}
# S13: 嘔気嘔吐 (脳炎20-30%)
n["S13"]["parent_effects"]["D110"] = {"absent": 0.70, "present": 0.30}

print(f"step3: Added {len(d_edges)} noisy_or CPTs")

# ── step3: full_cpt (R→D risk factor CPT) ──
# Parents: R25 (HIV), R05 (immunosuppression)
# R25 states: no, yes  |  R05 states: no, yes
# Toxoplasmosis: HIV is the dominant risk factor
#   no HIV + no immuno: 0.002 (very rare to present as fever in immunocompetent)
#   no HIV + immuno:    0.008 (organ transplant, chemotherapy etc.)
#   HIV + no immuno:    0.015 (HIV alone is strong risk)
#   HIV + immuno:       0.030 (HIV + additional immunosuppression)
s3["full_cpts"]["D110"] = {
    "parents": ["R25", "R05"],
    "description": "トキソプラズマ症。HIV(CD4<100)が最大リスク因子",
    "cpt": {
        "no|no":  0.002,
        "no|yes": 0.008,
        "yes|no": 0.015,
        "yes|yes": 0.030
    }
}
print("step3: Added full_cpt (R25, R05 -> D110)")

# ── Save ──
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("\nAll saved. 110 diseases total.")
print("Next: python validate_bn.py && python run_test.py")
