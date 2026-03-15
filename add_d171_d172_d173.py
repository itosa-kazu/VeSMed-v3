#!/usr/bin/env python3
"""Add D171 APS + D172 Acute Mesenteric Ischemia (already D37?) + D173 Adrenal insufficiency.
Actually D37 is 急性腸間膜虚血. Let me check and pick different diseases.
D171: 抗リン脂質抗体症候群 (APS)
D172: 関節リウマチ (RA) - very common, important differential
D173: ガス壊疽 (Gas gangrene)
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

# ===== D171 抗リン脂質抗体症候群 (APS) =====
s1["variables"].append({
    "id": "D171", "name": "antiphospholipid_syndrome",
    "name_ja": "抗リン脂質抗体症候群(APS)",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "動静脈血栓+流産。catastrophic APS(CAPS)は多臓器血栓→MOF。aPL/LAC/抗β2GP1抗体陽性。SLE合併多い"
})
for to, reason in [
    ("L52", "APS: D-dimer上昇(血栓症, 80%+)"),
    ("L14", "APS: 血小板減少(20-40%)"),
    ("S52", "APS: 局所神経脱落(脳梗塞, 20-30%)"),
    ("S04", "APS: 呼吸困難(PE, 30-40%)"),
    ("E36", "APS: 下肢浮腫(DVT, 30-40%)"),
    ("E12", "APS: 皮膚(網状皮斑/紫斑, 30-50%)"),
    ("E01", "APS: 発熱(CAPS, 30-40%)"),
    ("E02", "APS: 頻脈(PE/血栓)"),
    ("L55", "APS: AKI(腎血栓, CAPS)"),
    ("T01", "APS: 急性~亜急性"),
    ("T02", "APS: 急性~亜急性")]:
    s2["edges"].append({"from": "D171", "to": to, "from_name": "APS", "to_name": to, "reason": reason})

n["L52"]["parent_effects"]["D171"] = {"not_done": 0.10, "normal": 0.05, "mildly_elevated": 0.20, "very_high": 0.65}
n["L14"]["parent_effects"]["D171"] = {"normal": 0.55, "left_shift": 0.05, "atypical_lymphocytes": 0.00, "thrombocytopenia": 0.35, "eosinophilia": 0.00, "lymphocyte_predominant": 0.05}
n["S52"]["parent_effects"]["D171"] = {"absent": 0.60, "unilateral_weakness": 0.35, "bilateral": 0.05}
n["S04"]["parent_effects"]["D171"] = {"absent": 0.50, "on_exertion": 0.30, "at_rest": 0.20}
n["E36"]["parent_effects"]["D171"] = {"absent": 0.55, "unilateral": 0.35, "bilateral": 0.10}
n["E12"]["parent_effects"]["D171"] = {
    "normal": 0.45, "localized_erythema_warmth_swelling": 0.05, "petechiae_purpura": 0.10,
    "maculopapular_rash": 0.02, "vesicular_dermatomal": 0.01, "diffuse_erythroderma": 0.01,
    "purpura": 0.15, "vesicle_bulla": 0.01, "skin_necrosis": 0.20
}
n["E01"]["parent_effects"]["D171"] = {"under_37.5": 0.50, "37.5_38.0": 0.15, "38.0_39.0": 0.20, "39.0_40.0": 0.12, "over_40.0": 0.03}
n["E02"]["parent_effects"]["D171"] = {"under_100": 0.25, "100_120": 0.45, "over_120": 0.30}
n["L55"]["parent_effects"]["D171"] = {"normal": 0.50, "mild_elevated": 0.30, "high_AKI": 0.20}
n["T01"]["parent_effects"]["D171"] = {"under_3d": 0.35, "3d_to_1w": 0.35, "1w_to_3w": 0.20, "over_3w": 0.10}
n["T02"]["parent_effects"]["D171"] = {"sudden_hours": 0.40, "gradual_days": 0.60}
s3["full_cpts"]["D171"] = {"parents": ["R02"], "description": "APS。女性に多い(F:M≈5:1)",
    "cpt": {"male": 0.0005, "female": 0.002}}

# ===== D172 ガス壊疽 (Gas Gangrene / Clostridial Myonecrosis) =====
s1["variables"].append({
    "id": "D172", "name": "gas_gangrene",
    "name_ja": "ガス壊疽",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "Clostridium perfringens等による筋壊死。外傷/手術後。激痛+浮腫+捻髪音(皮下気腫)+毒素性ショック。数時間で致死的"
})
for to, reason in [
    ("E01", "ガス壊疽: 発熱(80-90%)"),
    ("E02", "ガス壊疽: 頻脈(毒素性ショック)"),
    ("E03", "ガス壊疽: 低血圧(毒素性ショック)"),
    ("E12", "ガス壊疽: 皮膚(壊死/水疱/暗赤色変色)"),
    ("E16", "ガス壊疽: 意識障害(毒素性)"),
    ("S07", "ガス壊疽: 全身脱力"),
    ("L01", "ガス壊疽: WBC上昇(重度感染)"),
    ("L02", "ガス壊疽: CRP著高"),
    ("L17", "ガス壊疽: CK上昇(筋壊死)"),
    ("T01", "ガス壊疽: 超急性(6-24時間)"),
    ("T02", "ガス壊疽: 超急性")]:
    s2["edges"].append({"from": "D172", "to": to, "from_name": "gas_gangrene", "to_name": to, "reason": reason})

n["E01"]["parent_effects"]["D172"] = {"under_37.5": 0.08, "37.5_38.0": 0.10, "38.0_39.0": 0.25, "39.0_40.0": 0.35, "over_40.0": 0.22}
n["E02"]["parent_effects"]["D172"] = {"under_100": 0.05, "100_120": 0.30, "over_120": 0.65}
n["E03"]["parent_effects"]["D172"] = {"normal_over_90": 0.20, "hypotension_under_90": 0.80}
n["E12"]["parent_effects"]["D172"] = {
    "normal": 0.05, "localized_erythema_warmth_swelling": 0.10, "petechiae_purpura": 0.03,
    "maculopapular_rash": 0.01, "vesicular_dermatomal": 0.01, "diffuse_erythroderma": 0.01,
    "purpura": 0.04, "vesicle_bulla": 0.25, "skin_necrosis": 0.50
}
n["E16"]["parent_effects"]["D172"] = {"normal": 0.25, "confused": 0.40, "obtunded": 0.35}
n["S07"]["parent_effects"]["D172"] = {"absent": 0.05, "mild": 0.20, "severe": 0.75}
n["L01"]["parent_effects"]["D172"] = {"low_under_4000": 0.05, "normal_4000_10000": 0.10, "high_10000_20000": 0.35, "very_high_over_20000": 0.50}
n["L02"]["parent_effects"]["D172"] = {"normal_under_0.3": 0.02, "mild_0.3_3": 0.05, "moderate_3_10": 0.18, "high_over_10": 0.75}
n["L17"]["parent_effects"]["D172"] = {"normal": 0.10, "elevated": 0.40, "very_high": 0.50}
n["T01"]["parent_effects"]["D172"] = {"under_3d": 0.85, "3d_to_1w": 0.12, "1w_to_3w": 0.02, "over_3w": 0.01}
n["T02"]["parent_effects"]["D172"] = {"sudden_hours": 0.85, "gradual_days": 0.15}
s3["full_cpts"]["D172"] = {"parents": [], "description": "ガス壊疽。外傷/手術後",
    "cpt": {"": 0.001}}

# ===== D173 水痘 (Varicella) =====
s1["variables"].append({
    "id": "D173", "name": "varicella",
    "name_ja": "水痘",
    "category": "disease", "states": ["no", "yes"], "severity": "moderate",
    "note": "VZV初感染。発熱+全身性水疱性発疹(各段階混在:紅斑→丘疹→水疱→痂皮)。成人は重症化リスク(肺炎/脳炎)"
})
for to, reason in [
    ("E01", "水痘: 発熱(90%+)"),
    ("E12", "水痘: 水疱性発疹(全身, 各段階混在)"),
    ("S05", "水痘: 頭痛(50-60%)"),
    ("S07", "水痘: 倦怠感(80%+)"),
    ("S01", "水痘: 咳嗽(成人水痘肺炎, 20-30%)"),
    ("L01", "水痘: WBC(正常~軽度)"),
    ("L11", "水痘: 肝酵素(軽度上昇, 成人30-40%)"),
    ("T01", "水痘: 急性"),
    ("T02", "水痘: 急性")]:
    s2["edges"].append({"from": "D173", "to": to, "from_name": "varicella", "to_name": to, "reason": reason})

n["E01"]["parent_effects"]["D173"] = {"under_37.5": 0.08, "37.5_38.0": 0.15, "38.0_39.0": 0.35, "39.0_40.0": 0.30, "over_40.0": 0.12}
n["E12"]["parent_effects"]["D173"] = {
    "normal": 0.02, "localized_erythema_warmth_swelling": 0.01, "petechiae_purpura": 0.01,
    "maculopapular_rash": 0.05, "vesicular_dermatomal": 0.05, "diffuse_erythroderma": 0.01,
    "purpura": 0.01, "vesicle_bulla": 0.82, "skin_necrosis": 0.02
}
n["S05"]["parent_effects"]["D173"] = {"absent": 0.35, "mild": 0.40, "severe": 0.25}
n["S07"]["parent_effects"]["D173"] = {"absent": 0.10, "mild": 0.50, "severe": 0.40}
n["S01"]["parent_effects"]["D173"] = {"absent": 0.65, "dry": 0.25, "productive": 0.10}
n["L01"]["parent_effects"]["D173"] = {"low_under_4000": 0.15, "normal_4000_10000": 0.55, "high_10000_20000": 0.25, "very_high_over_20000": 0.05}
n["L11"]["parent_effects"]["D173"] = {"normal": 0.55, "mild_elevated": 0.35, "very_high": 0.10}
n["T01"]["parent_effects"]["D173"] = {"under_3d": 0.30, "3d_to_1w": 0.50, "1w_to_3w": 0.18, "over_3w": 0.02}
n["T02"]["parent_effects"]["D173"] = {"sudden_hours": 0.30, "gradual_days": 0.70}
s3["full_cpts"]["D173"] = {"parents": [], "description": "水痘。成人は重症化リスク",
    "cpt": {"": 0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D171 APS: 11 edges, D172 Gas gangrene: 11 edges, D173 Varicella: 9 edges")
print(f"Total: {s2['total_edges']} edges, 173 diseases")
