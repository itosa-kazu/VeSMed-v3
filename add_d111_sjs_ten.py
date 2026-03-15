#!/usr/bin/env python3
"""Add D111 SJS/TEN (スティーブンス・ジョンソン症候群/中毒性表皮壊死症).

Clinical basis:
  薬剤性(>80%): 抗てんかん薬(カルバマゼピン/フェニトイン),抗菌薬(ST合剤/βラクタム),
    アロプリノール, NSAIDs
  前駆症状(1-3日): 発熱, 倦怠感, 咽頭痛, 筋肉痛
  皮膚: 標的状紅斑→水疱/びらん→表皮壊死, Nikolsky sign陽性
    SJS: <10% BSA, SJS/TEN overlap: 10-30%, TEN: >30%
  粘膜: 口腔(90-100%), 結膜炎(80-90%), 陰部(40-60%)
  検査: WBC正常~上昇, CRP上昇, 肝酵素上昇(10-30%)
  DRESSとの鑑別: SJS/TENは好酸球増多なし, 皮膚壊死/水疱が主体
  References: Harr T, French LE. Orphanet J Rare Dis 2010;5:39 (PMC3018455)
              Dodiuk-Gad RP et al. Am J Clin Dermatol 2015;16:475-93
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
    "id": "D111",
    "name": "SJS_TEN",
    "name_ja": "スティーブンス・ジョンソン症候群/TEN",
    "category": "disease",
    "states": ["no", "yes"],
    "severity": "critical",
    "note": "薬剤性(>80%): 抗てんかん薬/抗菌薬/アロプリノール/NSAIDs。"
           "前駆: 発熱+倦怠感+咽頭痛(1-3日)→標的状紅斑→水疱/表皮壊死+粘膜びらん(口腔90%,眼80%,陰部40%)。"
           "Nikolsky sign陽性。SJS<10%BSA, TEN>30%BSA。死亡率SJS 1-5%, TEN 25-35%"
})
print("step1: Added D111 SJS/TEN")

# ── step2: D→symptom/sign/lab edges ──
d_edges = [
    ("E01",  "SJS/TEN: 発熱(80-100%), 前駆症状として出現, 中等度~高熱"),
    ("E12",  "SJS/TEN: 皮膚所見 — 標的状紅斑→水疱(vesicle_bulla)→表皮壊死(skin_necrosis), Nikolsky sign+"),
    ("E35",  "SJS/TEN: 眼症状 — 結膜炎(80-90%), 偽膜形成, 角膜びらん"),
    ("S18",  "SJS/TEN: 皮膚の訴え — 広範囲の発疹/疼痛(rash_widespread)"),
    ("S02",  "SJS/TEN: 咽頭痛/口腔粘膜びらん(90-100%), 嚥下困難"),
    ("S06",  "SJS/TEN: 筋肉痛(前駆症状, 30-50%)"),
    ("S07",  "SJS/TEN: 倦怠感(前駆症状, 60-80%)"),
    ("L01",  "SJS/TEN: WBC正常~上昇, 好中球優位"),
    ("L02",  "SJS/TEN: CRP上昇(中等度~高度)"),
    ("L11",  "SJS/TEN: 肝酵素上昇(10-30%, 重症例)"),
    ("L28",  "SJS/TEN: ESR上昇"),
    ("T01",  "SJS/TEN: 薬剤開始1-3週後に発症, 皮膚症状は3d-1w進行"),
    ("T02",  "SJS/TEN: 前駆→皮疹は数日で進行(gradual)"),
    ("S13",  "SJS/TEN: 嘔気/嘔吐(粘膜障害, 20-30%)"),
    ("S05",  "SJS/TEN: 頭痛(前駆症状, 20-30%)"),
]

# R→D edge (risk factor)
r_edges = [
    ("R08", "D111", "新規薬剤開始: SJS/TENの80%以上が薬剤性(抗てんかん薬/抗菌薬/アロプリノール)"),
]

for to_id, reason in d_edges:
    s2["edges"].append({
        "from": "D111", "to": to_id,
        "from_name": "SJS_TEN", "to_name": to_id,
        "reason": reason
    })

for from_id, to_id, reason in r_edges:
    s2["edges"].append({
        "from": from_id, "to": to_id,
        "from_name": from_id, "to_name": "SJS_TEN",
        "reason": reason
    })

s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(d_edges)} D-edges + {len(r_edges)} R-edges = {len(d_edges)+len(r_edges)} total")
print(f"  New total_edges: {s2['total_edges']}")

# ── step3: noisy_or_params (D→symptom CPTs) ──
n = s3["noisy_or_params"]

# E01: 発熱(80-100%), 中等度~高熱
n["E01"]["parent_effects"]["D111"] = {
    "under_37.5": 0.05, "37.5_38.0": 0.15, "38.0_39.0": 0.40,
    "39.0_40.0": 0.30, "over_40.0": 0.10
}
# E12: 皮膚所見 — vesicle_bulla と skin_necrosis が鍵
# 早期: maculopapular_rash/diffuse_erythroderma → 進行: vesicle_bulla → skin_necrosis
n["E12"]["parent_effects"]["D111"] = {
    "normal": 0.02, "localized_erythema_warmth_swelling": 0.03,
    "petechiae_purpura": 0.02, "maculopapular_rash": 0.10,
    "vesicular_dermatomal": 0.03, "diffuse_erythroderma": 0.10,
    "purpura": 0.05, "vesicle_bulla": 0.35, "skin_necrosis": 0.30
}
# E35: 結膜炎(80-90%)
n["E35"]["parent_effects"]["D111"] = {"absent": 0.10, "conjunctivitis": 0.80, "uveitis": 0.10}
# S18: 広範囲皮疹
n["S18"]["parent_effects"]["D111"] = {"absent": 0.05, "localized_pain_redness": 0.10, "rash_widespread": 0.85}
# S02: 咽頭痛/口腔粘膜(90-100%)
n["S02"]["parent_effects"]["D111"] = {"absent": 0.05, "present": 0.95}
# S06: 筋肉痛(30-50%)
n["S06"]["parent_effects"]["D111"] = {"absent": 0.55, "present": 0.45}
# S07: 倦怠感(60-80%)
n["S07"]["parent_effects"]["D111"] = {"absent": 0.20, "mild": 0.30, "severe": 0.50}
# L01: WBC正常~上昇
n["L01"]["parent_effects"]["D111"] = {
    "low_under_4000": 0.05, "normal_4000_10000": 0.45,
    "high_10000_20000": 0.40, "very_high_over_20000": 0.10
}
# L02: CRP中等度~高度上昇
n["L02"]["parent_effects"]["D111"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.15,
    "moderate_3_10": 0.40, "high_over_10": 0.40
}
# L11: 肝酵素(10-30%で上昇)
n["L11"]["parent_effects"]["D111"] = {"normal": 0.65, "mild_elevated": 0.25, "very_high": 0.10}
# L28: ESR上昇
n["L28"]["parent_effects"]["D111"] = {"normal": 0.20, "elevated": 0.55, "very_high_over_100": 0.25}
# T01: 薬剤開始1-3週後, 皮膚3d-1w進行
n["T01"]["parent_effects"]["D111"] = {
    "under_3d": 0.10, "3d_to_1w": 0.45, "1w_to_3w": 0.35, "over_3w": 0.10
}
# T02: 前駆→皮疹は数日
n["T02"]["parent_effects"]["D111"] = {"sudden_hours": 0.15, "gradual_days": 0.85}
# S13: 嘔気(20-30%)
n["S13"]["parent_effects"]["D111"] = {"absent": 0.70, "present": 0.30}
# S05: 頭痛(20-30%)
n["S05"]["parent_effects"]["D111"] = {"absent": 0.70, "mild": 0.20, "severe": 0.10}

print(f"step3: Added {len(d_edges)} noisy_or CPTs")

# ── step3: full_cpt (R→D risk factor CPT) ──
# R08 (new medication) states: no, yes
# SJS/TEN: >80% drug-induced
s3["full_cpts"]["D111"] = {
    "parents": ["R08"],
    "description": "SJS/TEN。80%以上が薬剤性",
    "cpt": {
        "no":  0.001,
        "yes": 0.008
    }
}
print("step3: Added full_cpt (R08 -> D111)")

# ── Save ──
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("\nAll saved. 111 diseases total.")
