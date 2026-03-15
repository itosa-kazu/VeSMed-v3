#!/usr/bin/env python3
"""Batch edge additions to fix FATAL cases and improve rank 4-5 cases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

def add_edge(did, dname, to, reason, cpt):
    s2["edges"].append({"from": did, "to": to, "from_name": dname, "to_name": to, "reason": reason})
    n[to]["parent_effects"][did] = cpt

# ===== FATAL fixes =====

# R398 fix: D174 AAA → needs L14, L52, L02 (hemorrhagic coagulopathy)
add_edge("D174", "ruptured_AAA", "L14", "AAA破裂: 消費性血小板減少(大量出血)",
    {"normal": 0.30, "left_shift": 0.10, "atypical_lymphocytes": 0.00, "thrombocytopenia": 0.55, "eosinophilia": 0.00, "lymphocyte_predominant": 0.05})
add_edge("D174", "ruptured_AAA", "L52", "AAA破裂: D-dimer著高(出血/消費性凝固障害)",
    {"not_done": 0.10, "normal": 0.05, "mildly_elevated": 0.15, "very_high": 0.70})
add_edge("D174", "ruptured_AAA", "L02", "AAA破裂: CRP上昇(SIRS)",
    {"normal_under_0.3": 0.10, "mild_0.3_3": 0.15, "moderate_3_10": 0.35, "high_over_10": 0.40})
add_edge("D174", "ruptured_AAA", "L01", "AAA破裂: WBC上昇(ストレス/SIRS)",
    {"low_under_4000": 0.02, "normal_4000_10000": 0.15, "high_10000_20000": 0.40, "very_high_over_20000": 0.43})
add_edge("D174", "ruptured_AAA", "L55", "AAA破裂: AKI(ショック/腎灌流低下)",
    {"normal": 0.25, "mild_elevated": 0.35, "high_AKI": 0.40})

# R387 fix: D173 varicella → needs L14, L15, L52 (disseminated varicella with DIC)
add_edge("D173", "varicella", "L14", "水痘: 血小板減少(重症/DIC合併, 20-30%)",
    {"normal": 0.60, "left_shift": 0.05, "atypical_lymphocytes": 0.05, "thrombocytopenia": 0.25, "eosinophilia": 0.00, "lymphocyte_predominant": 0.05})
add_edge("D173", "varicella", "L15", "水痘: フェリチン上昇(重症肝壊死, 稀だが極高値可)",
    {"normal": 0.55, "mild_elevated": 0.20, "very_high_over_1000": 0.15, "extreme_over_10000": 0.10})
add_edge("D173", "varicella", "L52", "水痘: D-dimer上昇(DIC合併時)",
    {"not_done": 0.20, "normal": 0.35, "mildly_elevated": 0.25, "very_high": 0.20})
add_edge("D173", "varicella", "L17", "水痘: CK上昇(横紋筋融解合併時)",
    {"normal": 0.60, "elevated": 0.25, "very_high": 0.15})
# D173 → S13 (nausea/vomiting)
add_edge("D173", "varicella", "S13", "水痘: 嘔気/嘔吐(成人30-40%)",
    {"absent": 0.55, "present": 0.45})

# R382: D171 APS → needs S12, S07 already exists, E16
add_edge("D171", "APS", "S12", "APS: 腹痛(腸管血栓/脾梗塞, 30-40%)",
    {"absent": 0.50, "epigastric": 0.10, "RUQ": 0.05, "RLQ": 0.05, "LLQ": 0.10, "suprapubic": 0.02, "diffuse": 0.18})
add_edge("D171", "APS", "S07", "APS: 倦怠感(60-70%)",
    {"absent": 0.25, "mild": 0.35, "severe": 0.40})
add_edge("D171", "APS", "L02", "APS: CRP上昇(CAPS時炎症)",
    {"normal_under_0.3": 0.20, "mild_0.3_3": 0.25, "moderate_3_10": 0.30, "high_over_10": 0.25})

# ===== Rank 4-5 improvements =====

# R278 (GBS r5): D163 Wernicke stealing → D144 GBS needs L02 edge
add_edge("D144", "GBS", "L02", "GBS: CRP上昇(感染誘因/軽度)",
    {"normal_under_0.3": 0.25, "mild_0.3_3": 0.30, "moderate_3_10": 0.30, "high_over_10": 0.15})

# R227 (airway obstruction r8): D174 AAA stealing → D128 needs more distinction
# R227's evidence: obtunded + hypotension + no fever + acute + sudden + no vomiting + no diarrhea
# Not much we can do without more D128-specific features

# R325 (AIHA r4): D156 TTP stealing → need to differentiate AIHA from TTP
# AIHA has Coombs+ (not modeled), splenomegaly (not modeled)
# Add D158 AIHA → E02 (tachycardia from anemia) - already exists

# R298 (acute liver failure r4): D166 APAP at 43% → D151 needs edges
# D151 already exists. Check its edges.
add_edge("D151", "acute_liver_failure", "L52", "劇症肝炎: D-dimer上昇(DIC合併)",
    {"not_done": 0.15, "normal": 0.10, "mildly_elevated": 0.25, "very_high": 0.50})
add_edge("D151", "acute_liver_failure", "L55", "劇症肝炎: AKI(肝腎症候群)",
    {"normal": 0.30, "mild_elevated": 0.35, "high_AKI": 0.35})

# R383 (APS r4): D24 TSS at 42.6% → APS needs E03 (hypotension)
add_edge("D171", "APS", "E03", "APS: 低血圧(CAPSショック)",
    {"normal_over_90": 0.40, "hypotension_under_90": 0.60})
add_edge("D171", "APS", "E16", "APS: 意識障害(脳血栓/CAPS)",
    {"normal": 0.40, "confused": 0.35, "obtunded": 0.25})

# R176 (パルボB19 r6): D103 (急性リウマチ熱) stealing
# Parvovirus has arthralgia but also rash → add E12 edge for D105
add_edge("D105", "parvovirus_B19", "E12", "パルボB19: 皮疹(slapped cheek/レース状, 60-70%)",
    {"normal": 0.25, "localized_erythema_warmth_swelling": 0.05, "petechiae_purpura": 0.02,
     "maculopapular_rash": 0.60, "vesicular_dermatomal": 0.01, "diffuse_erythroderma": 0.02,
     "purpura": 0.02, "vesicle_bulla": 0.01, "skin_necrosis": 0.02})

# D176 anti-NMDA → needs S13 (vomiting common prodromal)
add_edge("D176", "anti_NMDA", "S13", "抗NMDA: 嘔気/嘔吐(前駆, 30-40%)",
    {"absent": 0.55, "present": 0.45})
add_edge("D176", "anti_NMDA", "L01", "抗NMDA: WBC(正常~軽度上昇)",
    {"low_under_4000": 0.05, "normal_4000_10000": 0.50, "high_10000_20000": 0.35, "very_high_over_20000": 0.10})

s2["total_edges"] = len(s2["edges"])
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "w", encoding="utf-8") as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "w", encoding="utf-8") as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)

print(f"Added edges. Total: {s2['total_edges']}")
