#!/usr/bin/env python3
"""Add D174 Aortic Aneurysm Rupture + D175 Acute Cholecystitis (acalculous) + D176 Adrenal Crisis (already D72?)."""
# Check: D72 is already 副腎クリーゼ. Let me pick different diseases.
# D174: 腹部大動脈瘤破裂 (Ruptured AAA)
# D175: 無石胆嚢炎 (already D76?)
# Check existing: D76 is 無石胆嚢炎. Skip.
# D175: シェーグレン症候群 (Sjogren's) - autoimmune
# D176: 強直性脊椎炎 (Ankylosing Spondylitis) - autoimmune
# Actually let me pick more impactful diseases:
# D174: 腹部大動脈瘤破裂 - surgical emergency
# D175: 急性間質性肺炎 (AIP/Hamman-Rich) - respiratory emergency
# D176: 抗NMDA受容体脳炎 - important neuro diagnosis
"""Add D174 Ruptured AAA + D175 AIP + D176 Anti-NMDA Receptor Encephalitis."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D174 腹部大動脈瘤破裂 (Ruptured AAA) =====
s1["variables"].append({
    "id": "D174", "name": "ruptured_AAA",
    "name_ja": "腹部大動脈瘤破裂",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "突然の腹痛/背部痛+ショック+拍動性腹部腫瘤。高齢男性+喫煙+高血圧がリスク。緊急手術。死亡率50-80%"
})
for to, reason in [
    ("S12", "AAA破裂: 腹痛(突然, びまん性/腰背部, 90%+)"),
    ("S15", "AAA破裂: 腰背部痛(後腹膜出血, 70-80%)"),
    ("E03", "AAA破裂: 低血圧/ショック(出血, 80%+)"),
    ("E02", "AAA破裂: 頻脈(出血)"),
    ("E16", "AAA破裂: 意識障害(ショック)"),
    ("E09", "AAA破裂: 腹部(膨満+圧痛)"),
    ("S44", "AAA破裂: 出血傾向(消費性)"),
    ("T01", "AAA破裂: 超急性"),
    ("T02", "AAA破裂: 突発")]:
    s2["edges"].append({"from": "D174", "to": to, "from_name": "ruptured_AAA", "to_name": to, "reason": reason})

n["S12"]["parent_effects"]["D174"] = {"absent": 0.05, "epigastric": 0.10, "RUQ": 0.03, "RLQ": 0.03, "LLQ": 0.03, "suprapubic": 0.01, "diffuse": 0.75}
n["S15"]["parent_effects"]["D174"] = {"absent": 0.15, "present": 0.85}
n["E03"]["parent_effects"]["D174"] = {"normal_over_90": 0.10, "hypotension_under_90": 0.90}
n["E02"]["parent_effects"]["D174"] = {"under_100": 0.05, "100_120": 0.30, "over_120": 0.65}
n["E16"]["parent_effects"]["D174"] = {"normal": 0.30, "confused": 0.35, "obtunded": 0.35}
n["E09"]["parent_effects"]["D174"] = {"soft_nontender": 0.05, "localized_tenderness": 0.30, "peritoneal_signs": 0.65}
n["S44"]["parent_effects"]["D174"] = {"absent": 0.50, "present": 0.50}
n["T01"]["parent_effects"]["D174"] = {"under_3d": 0.95, "3d_to_1w": 0.04, "1w_to_3w": 0.01, "over_3w": 0.00}
n["T02"]["parent_effects"]["D174"] = {"sudden_hours": 0.95, "gradual_days": 0.05}
s3["full_cpts"]["D174"] = {"parents": ["R01", "R02"], "description": "AAA破裂。高齢男性に多い",
    "cpt": {"18_39,male": 0.0001, "18_39,female": 0.00005,
            "40_64,male": 0.001, "40_64,female": 0.0003,
            "65_plus,male": 0.004, "65_plus,female": 0.001}}

# ===== D175 急性間質性肺炎 (AIP / Hamman-Rich) =====
s1["variables"].append({
    "id": "D175", "name": "acute_interstitial_pneumonia",
    "name_ja": "急性間質性肺炎(AIP/Hamman-Rich)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "特発性の急速進行性間質性肺炎→DAD(diffuse alveolar damage)→ARDS。前駆:URI様症状→1-2週で呼吸不全。50-70%死亡"
})
for to, reason in [
    ("S04", "AIP: 呼吸困難(急速進行, 100%)"),
    ("S01", "AIP: 咳嗽(乾性, 80%+)"),
    ("E01", "AIP: 発熱(前駆URI症状, 50-60%)"),
    ("E07", "AIP: 肺聴診(crackles両側)"),
    ("E04", "AIP: 頻呼吸"),
    ("E05", "AIP: 低酸素(重度)"),
    ("L04", "AIP: CXR(両側浸潤)"),
    ("E02", "AIP: 頻脈"),
    ("L01", "AIP: WBC(正常~軽度上昇)"),
    ("T01", "AIP: 急性(1-3週)"),
    ("T02", "AIP: 亜急性")]:
    s2["edges"].append({"from": "D175", "to": to, "from_name": "AIP", "to_name": to, "reason": reason})

n["S04"]["parent_effects"]["D175"] = {"absent": 0.02, "on_exertion": 0.15, "at_rest": 0.83}
n["S01"]["parent_effects"]["D175"] = {"absent": 0.10, "dry": 0.75, "productive": 0.15}
n["E01"]["parent_effects"]["D175"] = {"under_37.5": 0.35, "37.5_38.0": 0.20, "38.0_39.0": 0.25, "39.0_40.0": 0.15, "over_40.0": 0.05}
n["E07"]["parent_effects"]["D175"] = {"clear": 0.05, "crackles": 0.80, "wheezes": 0.10, "decreased_absent": 0.05}
n["E04"]["parent_effects"]["D175"] = {"normal_under_20": 0.05, "tachypnea_20_30": 0.35, "severe_over_30": 0.60}
n["E05"]["parent_effects"]["D175"] = {"normal_over_96": 0.05, "mild_hypoxia_93_96": 0.20, "severe_hypoxia_under_93": 0.75}
n["L04"]["parent_effects"]["D175"] = {"normal": 0.03, "lobar_infiltrate": 0.02, "bilateral_infiltrate": 0.90, "BHL": 0.01, "pleural_effusion": 0.02, "pneumothorax": 0.02}
n["E02"]["parent_effects"]["D175"] = {"under_100": 0.05, "100_120": 0.35, "over_120": 0.60}
n["L01"]["parent_effects"]["D175"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.40, "high_10000_20000": 0.40, "very_high_over_20000": 0.15}
n["T01"]["parent_effects"]["D175"] = {"under_3d": 0.15, "3d_to_1w": 0.35, "1w_to_3w": 0.40, "over_3w": 0.10}
n["T02"]["parent_effects"]["D175"] = {"sudden_hours": 0.20, "gradual_days": 0.80}
s3["full_cpts"]["D175"] = {"parents": [], "description": "AIP。特発性、年齢問わず",
    "cpt": {"": 0.001}}

# ===== D176 抗NMDA受容体脳炎 =====
s1["variables"].append({
    "id": "D176", "name": "anti_NMDA_receptor_encephalitis",
    "name_ja": "抗NMDA受容体脳炎",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "若年女性に多い。前駆:発熱/頭痛→精神症状(幻覚/興奮)→痙攣→意識障害→不随意運動→自律神経障害。卵巣奇形腫が30-50%"
})
for to, reason in [
    ("E16", "抗NMDA: 意識障害(80-90%)"),
    ("S42", "抗NMDA: 痙攣(70-80%)"),
    ("S05", "抗NMDA: 頭痛(前駆, 50-60%)"),
    ("E01", "抗NMDA: 発熱(前駆/自律神経障害, 60-70%)"),
    ("E02", "抗NMDA: 頻脈(自律神経障害)"),
    ("S53", "抗NMDA: 構音障害/失語(50-60%)"),
    ("S07", "抗NMDA: 全身脱力"),
    ("T01", "抗NMDA: 亜急性(1-3週)"),
    ("T02", "抗NMDA: 亜急性")]:
    s2["edges"].append({"from": "D176", "to": to, "from_name": "anti_NMDA", "to_name": to, "reason": reason})

n["E16"]["parent_effects"]["D176"] = {"normal": 0.08, "confused": 0.45, "obtunded": 0.47}
n["S42"]["parent_effects"]["D176"] = {"absent": 0.15, "present": 0.85}
n["S05"]["parent_effects"]["D176"] = {"absent": 0.30, "mild": 0.35, "severe": 0.35}
n["E01"]["parent_effects"]["D176"] = {"under_37.5": 0.25, "37.5_38.0": 0.20, "38.0_39.0": 0.30, "39.0_40.0": 0.18, "over_40.0": 0.07}
n["E02"]["parent_effects"]["D176"] = {"under_100": 0.15, "100_120": 0.40, "over_120": 0.45}
n["S53"]["parent_effects"]["D176"] = {"absent": 0.30, "dysarthria": 0.35, "aphasia": 0.35}
n["S07"]["parent_effects"]["D176"] = {"absent": 0.15, "mild": 0.35, "severe": 0.50}
n["T01"]["parent_effects"]["D176"] = {"under_3d": 0.10, "3d_to_1w": 0.30, "1w_to_3w": 0.45, "over_3w": 0.15}
n["T02"]["parent_effects"]["D176"] = {"sudden_hours": 0.15, "gradual_days": 0.85}
s3["full_cpts"]["D176"] = {"parents": ["R01", "R02"], "description": "抗NMDA受容体脳炎。若年女性に多い",
    "cpt": {"18_39,male": 0.0005, "18_39,female": 0.002,
            "40_64,male": 0.0003, "40_64,female": 0.001,
            "65_plus,male": 0.0001, "65_plus,female": 0.0003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D174 rAAA: 9 edges, D175 AIP: 11 edges, D176 anti-NMDA: 9 edges")
print(f"Total: {s2['total_edges']} edges, 176 diseases")
