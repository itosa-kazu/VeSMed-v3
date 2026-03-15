#!/usr/bin/env python3
"""Add D152 DIC + D153 Rhabdomyolysis + D154 Bowel Obstruction."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D152 DIC =====
s1["variables"].append({
    "id": "D152", "name": "DIC",
    "name_ja": "播種性血管内凝固症候群(DIC)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "敗血症/悪性腫瘍/外傷等が基礎疾患。出血+臓器不全。PLT低下+PT延長+D-dimer著高+フィブリノゲン低下"
})
for to, reason in [
    ("S44", "DIC: 出血傾向(紫斑/歯肉出血/消化管出血, 60-80%)"),
    ("E12", "DIC: 皮膚(紫斑/点状出血, 50-70%)"),
    ("E01", "DIC: 発熱(基礎疾患による, 60-70%)"),
    ("E02", "DIC: 頻脈(ショック/敗血症)"), ("E03", "DIC: 低血圧(ショック)"),
    ("E16", "DIC: 意識障害(臓器不全)"),
    ("L01", "DIC: WBC(基礎疾患による)"), ("L02", "DIC: CRP上昇(敗血症)"),
    ("L52", "DIC: D-dimer著高"), ("L14", "DIC: 血小板減少"),
    ("T01", "DIC: 急性"), ("T02", "DIC: 急性~亜急性")]:
    s2["edges"].append({"from": "D152", "to": to, "from_name": "DIC", "to_name": to, "reason": reason})

n["S44"]["parent_effects"]["D152"] = {"absent": 0.20, "present": 0.80}
n["E12"]["parent_effects"]["D152"] = {
    "normal": 0.25, "localized_erythema_warmth_swelling": 0.03, "petechiae_purpura": 0.30,
    "maculopapular_rash": 0.02, "vesicular_dermatomal": 0.02, "diffuse_erythroderma": 0.03,
    "purpura": 0.25, "vesicle_bulla": 0.05, "skin_necrosis": 0.05
}
n["E01"]["parent_effects"]["D152"] = {"under_37.5": 0.20, "37.5_38.0": 0.15, "38.0_39.0": 0.30, "39.0_40.0": 0.25, "over_40.0": 0.10}
n["E02"]["parent_effects"]["D152"] = {"under_100": 0.10, "100_120": 0.40, "over_120": 0.50}
n["E03"]["parent_effects"]["D152"] = {"normal_over_90": 0.40, "hypotension_under_90": 0.60}
n["E16"]["parent_effects"]["D152"] = {"normal": 0.30, "confused": 0.35, "obtunded": 0.35}
n["L01"]["parent_effects"]["D152"] = {"low_under_4000": 0.15, "normal_4000_10000": 0.20, "high_10000_20000": 0.35, "very_high_over_20000": 0.30}
n["L02"]["parent_effects"]["D152"] = {"normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.25, "high_over_10": 0.60}
n["L52"]["parent_effects"]["D152"] = {"not_done": 0.10, "normal": 0.03, "mildly_elevated": 0.12, "very_high": 0.75}
n["L14"]["parent_effects"]["D152"] = {"normal": 0.05, "left_shift": 0.10, "atypical_lymphocytes": 0.02, "thrombocytopenia": 0.80, "eosinophilia": 0.03}
n["T01"]["parent_effects"]["D152"] = {"under_3d": 0.60, "3d_to_1w": 0.30, "1w_to_3w": 0.08, "over_3w": 0.02}
n["T02"]["parent_effects"]["D152"] = {"sudden_hours": 0.50, "gradual_days": 0.50}
s3["full_cpts"]["D152"] = {"parents": [], "description": "DIC。敗血症/悪性腫瘍が基礎", "cpt": {"": 0.003}}

# ===== D153 Rhabdomyolysis =====
s1["variables"].append({
    "id": "D153", "name": "rhabdomyolysis",
    "name_ja": "横紋筋融解症",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "筋肉痛+暗色尿(ミオグロビン尿)+CK著高(>10000)。原因:外傷/圧挫/過度運動/薬剤/感染。AKIリスク"
})
for to, reason in [
    ("S06", "横紋筋融解: 筋肉痛(70-80%)"), ("L17", "横紋筋融解: CK著高(>10000, 定義的)"),
    ("S07", "横紋筋融解: 全身脱力(60-70%)"), ("S13", "横紋筋融解: 嘔気(30-40%)"),
    ("E01", "横紋筋融解: 発熱(感染性なら)"), ("E02", "横紋筋融解: 頻脈(脱水)"),
    ("L01", "横紋筋融解: WBC上昇(ストレス/感染)"), ("L02", "横紋筋融解: CRP上昇"),
    ("L16", "横紋筋融解: LDH上昇"), ("L44", "横紋筋融解: 高K血症"),
    ("T01", "横紋筋融解: 急性"), ("T02", "横紋筋融解: 急性~亜急性")]:
    s2["edges"].append({"from": "D153", "to": to, "from_name": "rhabdomyolysis", "to_name": to, "reason": reason})

n["S06"]["parent_effects"]["D153"] = {"absent": 0.15, "present": 0.85}
n["L17"]["parent_effects"]["D153"] = {"normal": 0.02, "elevated": 0.08, "very_high": 0.90}
n["S07"]["parent_effects"]["D153"] = {"absent": 0.15, "mild": 0.25, "severe": 0.60}
n["S13"]["parent_effects"]["D153"] = {"absent": 0.55, "present": 0.45}
n["E01"]["parent_effects"]["D153"] = {"under_37.5": 0.45, "37.5_38.0": 0.20, "38.0_39.0": 0.20, "39.0_40.0": 0.12, "over_40.0": 0.03}
n["E02"]["parent_effects"]["D153"] = {"under_100": 0.30, "100_120": 0.45, "over_120": 0.25}
n["L01"]["parent_effects"]["D153"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.35, "high_10000_20000": 0.40, "very_high_over_20000": 0.22}
n["L02"]["parent_effects"]["D153"] = {"normal_under_0.3": 0.15, "mild_0.3_3": 0.25, "moderate_3_10": 0.35, "high_over_10": 0.25}
n["L16"]["parent_effects"]["D153"] = {"normal": 0.10, "elevated": 0.90}
n["L44"]["parent_effects"]["D153"] = {"normal": 0.35, "hyponatremia": 0.05, "hyperkalemia": 0.55, "other": 0.05}
n["T01"]["parent_effects"]["D153"] = {"under_3d": 0.65, "3d_to_1w": 0.25, "1w_to_3w": 0.08, "over_3w": 0.02}
n["T02"]["parent_effects"]["D153"] = {"sudden_hours": 0.45, "gradual_days": 0.55}
s3["full_cpts"]["D153"] = {"parents": [], "description": "横紋筋融解症", "cpt": {"": 0.003}}

# ===== D154 Bowel Obstruction =====
s1["variables"].append({
    "id": "D154", "name": "bowel_obstruction",
    "name_ja": "腸閉塞（イレウス）",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "腹痛(疝痛様)+嘔吐+腹部膨満+排ガス停止。手術既往(癒着)/ヘルニア/腫瘍が原因。絞扼性は緊急手術"
})
for to, reason in [
    ("S12", "腸閉塞: 腹痛(疝痛様, 90%+)"), ("S13", "腸閉塞: 嘔吐(80-90%)"),
    ("E09", "腸閉塞: 腹部触診(膨満+圧痛, 絞扼性で腹膜刺激)"),
    ("E01", "腸閉塞: 発熱(絞扼性/感染で30-40%)"),
    ("E02", "腸閉塞: 頻脈(脱水/ショック)"),
    ("E03", "腸閉塞: 低血圧(脱水/絞扼性ショック)"),
    ("L01", "腸閉塞: WBC上昇(絞扼性/感染)"), ("L02", "腸閉塞: CRP上昇(絞扼性)"),
    ("T01", "腸閉塞: 急性~亜急性"), ("T02", "腸閉塞: 急性~亜急性")]:
    s2["edges"].append({"from": "D154", "to": to, "from_name": "bowel_obstruction", "to_name": to, "reason": reason})

n["S12"]["parent_effects"]["D154"] = {"absent": 0.03, "epigastric": 0.10, "RUQ": 0.05, "RLQ": 0.10, "LLQ": 0.05, "suprapubic": 0.02, "diffuse": 0.65}
n["S13"]["parent_effects"]["D154"] = {"absent": 0.08, "present": 0.92}
n["E09"]["parent_effects"]["D154"] = {"soft_nontender": 0.10, "localized_tenderness": 0.45, "peritoneal_signs": 0.45}
n["E01"]["parent_effects"]["D154"] = {"under_37.5": 0.50, "37.5_38.0": 0.20, "38.0_39.0": 0.18, "39.0_40.0": 0.10, "over_40.0": 0.02}
n["E02"]["parent_effects"]["D154"] = {"under_100": 0.20, "100_120": 0.45, "over_120": 0.35}
n["E03"]["parent_effects"]["D154"] = {"normal_over_90": 0.55, "hypotension_under_90": 0.45}
n["L01"]["parent_effects"]["D154"] = {"low_under_4000": 0.03, "normal_4000_10000": 0.25, "high_10000_20000": 0.45, "very_high_over_20000": 0.27}
n["L02"]["parent_effects"]["D154"] = {"normal_under_0.3": 0.10, "mild_0.3_3": 0.20, "moderate_3_10": 0.35, "high_over_10": 0.35}
n["T01"]["parent_effects"]["D154"] = {"under_3d": 0.55, "3d_to_1w": 0.30, "1w_to_3w": 0.12, "over_3w": 0.03}
n["T02"]["parent_effects"]["D154"] = {"sudden_hours": 0.40, "gradual_days": 0.60}
s3["full_cpts"]["D154"] = {"parents": ["R01"], "description": "腸閉塞。高齢+手術既往がリスク",
    "cpt": {"18_39": 0.003, "40_64": 0.005, "65_plus": 0.008}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D152 DIC: 12 edges, D153 Rhabdo: 12 edges, D154 Obstruction: 10 edges")
print(f"Total: {s2['total_edges']} edges, 154 diseases")
