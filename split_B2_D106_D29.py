#!/usr/bin/env python3
"""
B群 Batch2: D106 DM/PM分割 + D29 肝膿瘍分割

D106 炎症性筋疾患 → D106(皮膚筋炎/DM) + D361(多発性筋炎/PM)
  - R168,R169,R170,R180(全DM) → D106残留
  - 差別化: DM=皮膚所見(heliotrope/Gottron)+光線過敏, PM=皮膚所見なし+純筋炎

D29 肝膿瘍 → D29(細菌性肝膿瘍) + D362(アメーバ性肝膿瘍)
  - R53,R76(細菌性) → D29残留
  - 差別化: 細菌性=DM+胆道+多発+培養陽性, アメーバ=渡航歴+右葉単発+血清抗体
"""

import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# STEP 1
# ============================================================
def update_step1(s1):
    variables = s1['variables']

    # D106: Rename to DM
    for v in variables:
        if isinstance(v, dict) and v.get('id') == 'D106':
            v['name'] = 'dermatomyositis'
            v['name_ja'] = '皮膚筋炎(DM)'
            v['icd10'] = 'M33.1'
            v['key_features'] = 'Heliotrope疹+Gottron丘疹+近位筋力低下+CK著増。悪性腫瘍合併15-30%。間質性肺炎合併20-40%。'
            break

    # D361: PM
    d361 = {
        "id": "D361",
        "name": "polymyositis",
        "name_ja": "多発性筋炎(PM)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "M33.2",
        "category_sub": "autoimmune",
        "severity": "high",
        "key_features": "皮膚所見なしの近位筋力低下+CK著増。嚥下困難30-40%。間質性肺炎20-30%。悪性腫瘍合併注意。",
        "diagnostic_profile": {}
    }

    # D29: Rename to bacterial
    for v in variables:
        if isinstance(v, dict) and v.get('id') == 'D29':
            v['name'] = 'pyogenic_liver_abscess'
            v['name_ja'] = '細菌性肝膿瘍'
            v['icd10'] = 'K75.0'
            v['key_features'] = '発熱+右上腹部痛+肝腫大。糖尿病・胆道疾患がリスク。血培Klebsiella/E.coli。CT多発膿瘍。'
            break

    # D362: Amebic
    d362 = {
        "id": "D362",
        "name": "amebic_liver_abscess",
        "name_ja": "アメーバ性肝膿瘍",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "A06.4",
        "category_sub": "deep_abscess",
        "severity": "high",
        "key_features": "発熱+右上腹部痛+肝腫大。熱帯渡航歴。右葉単発の大きな膿瘍。血清アメーバ抗体陽性。血培陰性。",
        "diagnostic_profile": {}
    }

    variables.append(d361)
    variables.append(d362)
    return s1

# ============================================================
# STEP 2
# ============================================================
def update_step2(s2):
    edges = s2['edges']

    # --- Remove all D106 edges ---
    edges = [e for e in edges if e.get('from') != 'D106' and e.get('to') != 'D106']

    # --- D106 (DM) edges: 皮膚所見中心 ---
    dm_edges = [
        {"from": "R01", "to": "D106", "reason": "DM。中年女性2:1", "from_name": "age_group", "to_name": "DM"},
        {"from": "R02", "to": "D106", "reason": "DM。女性2:1", "from_name": "sex", "to_name": "D106"},
        {"from": "D106", "to": "E01", "reason": "発熱(20-50%)", "from_name": "DM", "to_name": "temperature"},
        {"from": "D106", "to": "E12", "reason": "DM皮膚所見(heliotrope/Gottron)(DM特異的)", "from_name": "DM", "to_name": "skin_findings"},
        {"from": "D106", "to": "E20", "reason": "DM heliotrope疹(蝶形紅斑類似)(DM特異的)", "from_name": "DM", "to_name": "butterfly_rash"},
        {"from": "D106", "to": "S30", "reason": "光線過敏(DM 40-50%)(DM特異的)", "from_name": "DM", "to_name": "photosensitivity"},
        {"from": "D106", "to": "S48", "reason": "近位筋力低下(>90%)", "from_name": "DM", "to_name": "proximal_weakness"},
        {"from": "D106", "to": "L17", "reason": "CK著増(通常5-50倍)", "from_name": "DM", "to_name": "CK"},
        {"from": "D106", "to": "S25", "reason": "嚥下困難(30-40%)", "from_name": "DM", "to_name": "dysphagia"},
        {"from": "D106", "to": "S06", "reason": "筋肉痛(50-70%)", "from_name": "DM", "to_name": "myalgia"},
        {"from": "D106", "to": "S07", "reason": "倦怠感(60-80%)", "from_name": "DM", "to_name": "fatigue"},
        {"from": "D106", "to": "S08", "reason": "関節痛(20-50%)", "from_name": "DM", "to_name": "arthralgia"},
        {"from": "D106", "to": "L04", "reason": "間質性肺炎(DM 30-50%)", "from_name": "DM", "to_name": "chest_xray"},
        {"from": "D106", "to": "L02", "reason": "CRP上昇(50-70%)", "from_name": "DM", "to_name": "CRP"},
        {"from": "D106", "to": "L28", "reason": "ESR上昇(50-70%)", "from_name": "DM", "to_name": "ESR"},
        {"from": "D106", "to": "L16", "reason": "LDH上昇(筋原性)", "from_name": "DM", "to_name": "LDH"},
        {"from": "D106", "to": "L18", "reason": "ANA陽性(60-80%)", "from_name": "DM", "to_name": "ANA"},
        {"from": "D106", "to": "S17", "reason": "体重減少(30-50%)", "from_name": "DM", "to_name": "weight_loss"},
        {"from": "D106", "to": "T01", "reason": "亜急性〜慢性経過", "from_name": "DM", "to_name": "fever_duration"},
        {"from": "D106", "to": "T02", "reason": "緩徐発症", "from_name": "DM", "to_name": "onset_speed"},
        {"from": "D106", "to": "S90", "reason": "関節痛の分布(多関節対称性)", "from_name": "DM", "to_name": "S90"},
    ]

    # --- D361 (PM) edges: 皮膚所見なし、筋炎のみ ---
    pm_edges = [
        {"from": "R01", "to": "D361", "reason": "PM。中年〜高齢、女性やや多い", "from_name": "age_group", "to_name": "PM"},
        {"from": "R02", "to": "D361", "reason": "PM。女性やや多い(1.5:1)", "from_name": "sex", "to_name": "D361"},
        {"from": "D361", "to": "E01", "reason": "発熱(20-40%)", "from_name": "PM", "to_name": "temperature"},
        {"from": "D361", "to": "S48", "reason": "近位筋力低下(>95%)(PM主症状)", "from_name": "PM", "to_name": "proximal_weakness"},
        {"from": "D361", "to": "L17", "reason": "CK著増(通常5-50倍)", "from_name": "PM", "to_name": "CK"},
        {"from": "D361", "to": "S25", "reason": "嚥下困難(30-40%)", "from_name": "PM", "to_name": "dysphagia"},
        {"from": "D361", "to": "S06", "reason": "筋肉痛(60-80%)", "from_name": "PM", "to_name": "myalgia"},
        {"from": "D361", "to": "S07", "reason": "倦怠感(60-80%)", "from_name": "PM", "to_name": "fatigue"},
        {"from": "D361", "to": "S08", "reason": "関節痛(20-40%)", "from_name": "PM", "to_name": "arthralgia"},
        {"from": "D361", "to": "L04", "reason": "間質性肺炎(PM 20-30%)", "from_name": "PM", "to_name": "chest_xray"},
        {"from": "D361", "to": "L02", "reason": "CRP上昇", "from_name": "PM", "to_name": "CRP"},
        {"from": "D361", "to": "L28", "reason": "ESR上昇", "from_name": "PM", "to_name": "ESR"},
        {"from": "D361", "to": "L16", "reason": "LDH上昇(筋原性)", "from_name": "PM", "to_name": "LDH"},
        {"from": "D361", "to": "L18", "reason": "ANA陽性(40-60%,DMより低い)", "from_name": "PM", "to_name": "ANA"},
        {"from": "D361", "to": "S17", "reason": "体重減少", "from_name": "PM", "to_name": "weight_loss"},
        {"from": "D361", "to": "T01", "reason": "亜急性〜慢性経過", "from_name": "PM", "to_name": "fever_duration"},
        {"from": "D361", "to": "T02", "reason": "緩徐発症", "from_name": "PM", "to_name": "onset_speed"},
        {"from": "D361", "to": "S90", "reason": "関節痛の分布", "from_name": "PM", "to_name": "S90"},
    ]

    # --- Remove all D29 edges ---
    edges = [e for e in edges if e.get('from') != 'D29' and e.get('to') != 'D29']

    # --- D29 (細菌性肝膿瘍) edges ---
    bact_edges = [
        {"from": "R01", "to": "D29", "reason": "細菌性肝膿瘍。中年男性", "from_name": "age_group", "to_name": "D29"},
        {"from": "R02", "to": "D29", "reason": "細菌性肝膿瘍。男性2:1", "from_name": "sex", "to_name": "D29"},
        {"from": "R04", "to": "D29", "reason": "糖尿病は細菌性肝膿瘍の主リスク因子", "from_name": "diabetes", "to_name": "D29"},
        {"from": "D29", "to": "E01", "reason": "高熱(弛張熱パターン)", "from_name": "bacterial_abscess", "to_name": "temperature",
         "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D29", "to": "S09", "reason": "悪寒戦慄(細菌血症)", "from_name": "bacterial_abscess", "to_name": "rigors",
         "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D29", "to": "S12", "reason": "右上腹部痛", "from_name": "bacterial_abscess", "to_name": "abdominal_distension",
         "onset_day_range": {"earliest": 0, "typical": 1, "latest": 5}},
        {"from": "D29", "to": "E34", "reason": "肝腫大", "from_name": "bacterial_abscess", "to_name": "hepatomegaly",
         "onset_day_range": {"earliest": 2, "typical": 5, "latest": 14}},
        {"from": "D29", "to": "E18", "reason": "黄疸(胆管圧迫, 細菌性で多い)", "from_name": "bacterial_abscess", "to_name": "jaundice",
         "onset_day_range": {"earliest": 3, "typical": 7, "latest": 14}},
        {"from": "D29", "to": "L02", "reason": "CRP著増", "from_name": "bacterial_abscess", "to_name": "CRP"},
        {"from": "D29", "to": "L01", "reason": "白血球増多", "from_name": "bacterial_abscess", "to_name": "WBC"},
        {"from": "D29", "to": "L11", "reason": "肝酵素上昇", "from_name": "bacterial_abscess", "to_name": "liver_enzymes"},
        {"from": "D29", "to": "L31", "reason": "CT:膿瘍像(多発が多い)", "from_name": "bacterial_abscess", "to_name": "CT_abdomen"},
        {"from": "D29", "to": "L09", "reason": "血培陽性(Klebsiella/E.coli 50-60%)", "from_name": "bacterial_abscess", "to_name": "blood_culture"},
        {"from": "D29", "to": "S07", "reason": "倦怠感", "from_name": "bacterial_abscess", "to_name": "fatigue"},
        {"from": "D29", "to": "S46", "reason": "食欲不振", "from_name": "bacterial_abscess", "to_name": "anorexia"},
        {"from": "D29", "to": "T01", "reason": "亜急性経過(1-3週)", "from_name": "bacterial_abscess", "to_name": "fever_duration"},
        {"from": "D29", "to": "E02", "reason": "頻脈(全身感染)", "from_name": "bacterial_abscess", "to_name": "heart_rate"},
        {"from": "D29", "to": "L14", "reason": "血小板減少(重症時)", "from_name": "bacterial_abscess", "to_name": "CBC_diff"},
        {"from": "D29", "to": "L20", "reason": "D-dimer上昇", "from_name": "bacterial_abscess", "to_name": "D_dimer"},
        {"from": "D29", "to": "L03", "reason": "PCT上昇(細菌性)", "from_name": "bacterial_abscess", "to_name": "PCT"},
        {"from": "D29", "to": "S05", "reason": "頭痛", "from_name": "bacterial_abscess", "to_name": "headache"},
        {"from": "D29", "to": "L66", "reason": "肝細胞型障害パターン", "from_name": "bacterial_abscess", "to_name": "L66"},
        {"from": "D29", "to": "S89", "reason": "右上腹部痛", "from_name": "bacterial_abscess", "to_name": "S89"},
    ]

    # --- D362 (アメーバ性肝膿瘍) edges ---
    amebic_edges = [
        {"from": "R01", "to": "D362", "reason": "アメーバ性肝膿瘍。20-40歳男性に多い", "from_name": "age_group", "to_name": "D362"},
        {"from": "R02", "to": "D362", "reason": "アメーバ性肝膿瘍。男性10:1", "from_name": "sex", "to_name": "D362"},
        {"from": "R06", "to": "D362", "reason": "熱帯渡航歴(アメーバ感染の主リスク)", "from_name": "travel_tropical", "to_name": "D362"},
        {"from": "D362", "to": "E01", "reason": "高熱(弛張熱)", "from_name": "amebic_abscess", "to_name": "temperature",
         "onset_day_range": {"earliest": 0, "typical": 3, "latest": 7}},
        {"from": "D362", "to": "S09", "reason": "悪寒戦慄", "from_name": "amebic_abscess", "to_name": "rigors"},
        {"from": "D362", "to": "S12", "reason": "右上腹部痛(右肩放散)", "from_name": "amebic_abscess", "to_name": "abdominal_distension"},
        {"from": "D362", "to": "E34", "reason": "肝腫大(右葉単発大膿瘍)", "from_name": "amebic_abscess", "to_name": "hepatomegaly"},
        {"from": "D362", "to": "E18", "reason": "黄疸(稀, <10%)", "from_name": "amebic_abscess", "to_name": "jaundice"},
        {"from": "D362", "to": "L02", "reason": "CRP著増", "from_name": "amebic_abscess", "to_name": "CRP"},
        {"from": "D362", "to": "L01", "reason": "白血球増多", "from_name": "amebic_abscess", "to_name": "WBC"},
        {"from": "D362", "to": "L11", "reason": "肝酵素軽度上昇(細菌性より低い)", "from_name": "amebic_abscess", "to_name": "liver_enzymes"},
        {"from": "D362", "to": "L31", "reason": "CT:右葉単発大膿瘍", "from_name": "amebic_abscess", "to_name": "CT_abdomen"},
        {"from": "D362", "to": "L09", "reason": "血培陰性(アメーバ性の特徴)", "from_name": "amebic_abscess", "to_name": "blood_culture"},
        {"from": "D362", "to": "S07", "reason": "倦怠感", "from_name": "amebic_abscess", "to_name": "fatigue"},
        {"from": "D362", "to": "S46", "reason": "食欲不振", "from_name": "amebic_abscess", "to_name": "anorexia"},
        {"from": "D362", "to": "T01", "reason": "亜急性〜慢性(1-4週)", "from_name": "amebic_abscess", "to_name": "fever_duration"},
        {"from": "D362", "to": "E02", "reason": "頻脈", "from_name": "amebic_abscess", "to_name": "heart_rate"},
        {"from": "D362", "to": "L14", "reason": "白血球左方移動", "from_name": "amebic_abscess", "to_name": "CBC_diff"},
        {"from": "D362", "to": "L03", "reason": "PCT軽度上昇(細菌性より低い)", "from_name": "amebic_abscess", "to_name": "PCT"},
        {"from": "D362", "to": "L66", "reason": "肝細胞型障害パターン(軽度)", "from_name": "amebic_abscess", "to_name": "L66"},
        {"from": "D362", "to": "S89", "reason": "右上腹部痛", "from_name": "amebic_abscess", "to_name": "S89"},
        {"from": "D362", "to": "S05", "reason": "頭痛", "from_name": "amebic_abscess", "to_name": "headache"},
    ]

    edges.extend(dm_edges)
    edges.extend(pm_edges)
    edges.extend(bact_edges)
    edges.extend(amebic_edges)

    s2['edges'] = edges
    s2['total_edges'] = len(edges)
    return s2

# ============================================================
# STEP 3
# ============================================================
def update_step3(s3):
    rp = s3['root_priors']
    fc = s3['full_cpts']
    nop = s3['noisy_or_params']

    # ========================================
    # D106 DM/PM → D106(DM) + D361(PM)
    # ========================================

    # (A) root_priors: DM 60%, PM 40% of combined
    rp['D106'] = {
        "parents": ["R02", "R01"],
        "description": "皮膚筋炎(DM)。中年女性2:1",
        "cpt": {
            "male|18_39": 0.0006,
            "male|40_64": 0.002,
            "male|65_plus": 0.0012,
            "female|18_39": 0.0012,
            "female|40_64": 0.004,
            "female|65_plus": 0.002
        }
    }
    rp['D361'] = {
        "parents": ["R02", "R01"],
        "description": "多発性筋炎(PM)。中年〜高齢、女性やや多い",
        "cpt": {
            "male|18_39": 0.0004,
            "male|40_64": 0.001,
            "male|65_plus": 0.0008,
            "female|18_39": 0.0008,
            "female|40_64": 0.002,
            "female|65_plus": 0.001
        }
    }

    # (B) full_cpts - D106 had none, add basic ones
    fc['D106'] = {
        "parents": ["R01"],
        "description": "皮膚筋炎(DM)",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.001, "40_64": 0.003, "65_plus": 0.002
        }
    }
    fc['D361'] = {
        "parents": ["R01"],
        "description": "多発性筋炎(PM)",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.0005, "40_64": 0.002, "65_plus": 0.0015
        }
    }

    # (D) parent_effects
    # DM (D106): 皮膚所見が特異的
    dm_pe = {
        "E01":  {"under_37.5": 0.5, "37.5_38.0": 0.25, "38.0_39.0": 0.15, "39.0_40.0": 0.07, "over_40.0": 0.02, "hypothermia_under_35": 0.01},
        "E12":  {"maculopapular_rash": 0.4, "petechiae_purpura": 0.01, "diffuse_erythroderma": 0.15, "normal": 0.43, "vesicular_dermatomal": 0.01},  # DM: 皮疹多い
        "E20":  {"absent": 0.6, "present": 0.4},     # DM: heliotrope 40%
        "L02":  {"normal_under_0.3": 0.25, "mild_0.3_3": 0.35, "moderate_3_10": 0.3, "high_over_10": 0.1},
        "L04":  {"not_done": 0.05, "normal": 0.45, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.35, "BHL": 0.01, "pleural_effusion": 0.05, "pneumothorax": 0.04},  # DM: ILD 30-50%
        "L16":  {"normal": 0.15, "elevated": 0.85},
        "L17":  {"normal": 0.03, "elevated": 0.27, "very_high": 0.7},
        "L18":  {"not_done": 0.05, "negative": 0.25, "positive": 0.7},  # DM: ANA 60-80%
        "L28":  {"normal": 0.3, "elevated": 0.5, "very_high_over_100": 0.2},
        "S06":  {"absent": 0.35, "present": 0.65},
        "S07":  {"absent": 0.2, "mild": 0.35, "severe": 0.45},
        "S08":  {"absent": 0.55, "present": 0.45},
        "S17":  {"absent": 0.55, "present": 0.45},
        "S25":  {"absent": 0.6, "present": 0.4},
        "S30":  {"absent": 0.5, "present": 0.5},     # DM: 光線過敏 40-50%
        "T01":  {"under_3d": 0.02, "3d_to_1w": 0.08, "1w_to_3w": 0.3, "over_3w": 0.6},
        "T02":  {"sudden": 0.005, "acute": 0.02, "subacute": 0.54, "chronic": 0.435},
        "S48":  {"absent": 0.05, "present": 0.95},
        "S90":  {"monoarticular": 0.1, "oligoarticular": 0.15, "polyarticular_symmetric": 0.5, "polyarticular_asymmetric": 0.15, "migratory": 0.1},
    }

    # PM (D361): 皮膚所見なし
    pm_pe = {
        "E01":  {"under_37.5": 0.55, "37.5_38.0": 0.2, "38.0_39.0": 0.15, "39.0_40.0": 0.07, "over_40.0": 0.02, "hypothermia_under_35": 0.01},
        "E12":  {"maculopapular_rash": 0.02, "petechiae_purpura": 0.01, "diffuse_erythroderma": 0.01, "normal": 0.95, "vesicular_dermatomal": 0.01},  # PM: 皮疹なし
        "E20":  {"absent": 0.98, "present": 0.02},    # PM: heliotropeなし
        "L02":  {"normal_under_0.3": 0.3, "mild_0.3_3": 0.35, "moderate_3_10": 0.25, "high_over_10": 0.1},
        "L04":  {"not_done": 0.05, "normal": 0.6, "lobar_infiltrate": 0.04, "bilateral_infiltrate": 0.22, "BHL": 0.01, "pleural_effusion": 0.04, "pneumothorax": 0.04},  # PM: ILD 20-30%
        "L16":  {"normal": 0.2, "elevated": 0.8},
        "L17":  {"normal": 0.03, "elevated": 0.3, "very_high": 0.67},
        "L18":  {"not_done": 0.05, "negative": 0.45, "positive": 0.5},  # PM: ANA 40-60%
        "L28":  {"normal": 0.35, "elevated": 0.45, "very_high_over_100": 0.2},
        "S06":  {"absent": 0.25, "present": 0.75},    # PM: 筋痛多い
        "S07":  {"absent": 0.2, "mild": 0.35, "severe": 0.45},
        "S08":  {"absent": 0.65, "present": 0.35},
        "S17":  {"absent": 0.6, "present": 0.4},
        "S25":  {"absent": 0.6, "present": 0.4},
        "S30":  {"absent": 0.95, "present": 0.05},    # PM: 光線過敏なし
        "T01":  {"under_3d": 0.02, "3d_to_1w": 0.05, "1w_to_3w": 0.25, "over_3w": 0.68},
        "T02":  {"sudden": 0.005, "acute": 0.02, "subacute": 0.5, "chronic": 0.475},
        "S48":  {"absent": 0.03, "present": 0.97},    # PM: 筋力低下がさらに多い
        "S90":  {"monoarticular": 0.15, "oligoarticular": 0.15, "polyarticular_symmetric": 0.4, "polyarticular_asymmetric": 0.15, "migratory": 0.15},
    }

    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D106' in pe:
            del pe['D106']
            if var_id in dm_pe:
                pe['D106'] = dm_pe[var_id]
            if var_id in pm_pe:
                pe['D361'] = pm_pe[var_id]

    # ========================================
    # D29 肝膿瘍 → D29(細菌性) + D362(アメーバ性)
    # ========================================

    # (A) root_priors
    rp['D29'] = {
        "parents": ["R02", "R01"],
        "description": "細菌性肝膿瘍。中年男性、DM合併多い",
        "cpt": {
            "male|18_39": 0.0015,
            "male|40_64": 0.005,
            "male|65_plus": 0.003,
            "female|18_39": 0.0008,
            "female|40_64": 0.002,
            "female|65_plus": 0.0015
        }
    }
    rp['D362'] = {
        "parents": ["R02", "R01"],
        "description": "アメーバ性肝膿瘍。若年男性+渡航歴",
        "cpt": {
            "male|18_39": 0.001,
            "male|40_64": 0.001,
            "male|65_plus": 0.0005,
            "female|18_39": 0.0001,
            "female|40_64": 0.0001,
            "female|65_plus": 0.0001
        }
    }

    # (B) full_cpts
    fc['D29'] = {
        "parents": ["R04"],
        "description": "細菌性肝膿瘍。糖尿病がリスク",
        "cpt": {
            "no": 0.004,
            "yes": 0.015
        }
    }
    fc['D362'] = {
        "parents": ["R06"],
        "description": "アメーバ性肝膿瘍。渡航歴がリスク",
        "cpt": {
            "no": 0.001,
            "yes": 0.015
        }
    }

    # (D) parent_effects
    # 細菌性 (D29): 血培陽性、多発膿瘍、黄疸多い
    bact_pe = {
        "E01":  {"under_37.5": 0.02, "37.5_38.0": 0.03, "38.0_39.0": 0.15, "39.0_40.0": 0.5, "over_40.0": 0.3, "hypothermia_under_35": 0.0},
        "E02":  {"under_100": 0.3, "100_120": 0.45, "over_120": 0.25},
        "E18":  {"absent": 0.45, "present": 0.55},    # 細菌性: 黄疸多い
        "E34":  {"absent": 0.3, "present": 0.7},
        "L01":  {"low_under_4000": 0.03, "normal_4000_10000": 0.12, "high_10000_20000": 0.55, "very_high_over_20000": 0.3},
        "L02":  {"normal_under_0.3": 0.02, "mild_0.3_3": 0.05, "moderate_3_10": 0.23, "high_over_10": 0.7},
        "L03":  {"not_done": 0.15, "low_under_0.25": 0.03, "gray_0.25_0.5": 0.07, "high_over_0.5": 0.75},  # 細菌性: PCT高い
        "L09":  {"not_done_or_pending": 0.1, "negative": 0.3, "gram_positive": 0.15, "gram_negative": 0.45},  # 細菌性: 培養陽性60%
        "L11":  {"normal": 0.1, "mild_elevated": 0.45, "very_high": 0.45},  # 細菌性: 肝酵素高い
        "L14":  {"normal": 0.35, "left_shift": 0.38, "atypical_lymphocytes": 0.03, "thrombocytopenia": 0.17, "eosinophilia": 0.03, "lymphocyte_predominant": 0.04},
        "L20":  {"not_done": 0.05, "normal": 0.35, "elevated": 0.6},
        "L31":  {"not_done": 0.05, "normal": 0.04, "abscess": 0.82, "mass": 0.04, "other_abnormal": 0.05},
        "S05":  {"absent": 0.65, "mild": 0.25, "severe": 0.1},
        "S07":  {"absent": 0.2, "mild": 0.35, "severe": 0.45},
        "S09":  {"absent": 0.1, "present": 0.9},
        "S12":  {"absent": 0.1, "present": 0.9},
        "S46":  {"absent": 0.2, "present": 0.8},
        "T01":  {"under_3d": 0.1, "3d_to_1w": 0.35, "1w_to_3w": 0.4, "over_3w": 0.15},
        "L66":  {"not_assessed": 0.05, "normal": 0.08, "hepatocellular": 0.55, "cholestatic": 0.27, "congestive": 0.05},
        "S89":  {"epigastric": 0.06, "RUQ": 0.78, "RLQ": 0.02, "LLQ": 0.02, "suprapubic": 0.01, "diffuse": 0.11},
    }

    # アメーバ性 (D362): 血培陰性、右葉単発、黄疸少ない
    amebic_pe = {
        "E01":  {"under_37.5": 0.02, "37.5_38.0": 0.05, "38.0_39.0": 0.2, "39.0_40.0": 0.5, "over_40.0": 0.23, "hypothermia_under_35": 0.0},
        "E02":  {"under_100": 0.35, "100_120": 0.4, "over_120": 0.25},
        "E18":  {"absent": 0.85, "present": 0.15},    # アメーバ: 黄疸稀<15%
        "E34":  {"absent": 0.2, "present": 0.8},      # アメーバ: 肝腫大多い
        "L01":  {"low_under_4000": 0.02, "normal_4000_10000": 0.2, "high_10000_20000": 0.55, "very_high_over_20000": 0.23},
        "L02":  {"normal_under_0.3": 0.02, "mild_0.3_3": 0.08, "moderate_3_10": 0.35, "high_over_10": 0.55},
        "L03":  {"not_done": 0.15, "low_under_0.25": 0.15, "gray_0.25_0.5": 0.3, "high_over_0.5": 0.4},  # アメーバ: PCT低め
        "L09":  {"not_done_or_pending": 0.1, "negative": 0.8, "gram_positive": 0.05, "gram_negative": 0.05},  # アメーバ: 血培陰性80%
        "L11":  {"normal": 0.25, "mild_elevated": 0.55, "very_high": 0.2},  # アメーバ: 肝酵素軽度
        "L14":  {"normal": 0.4, "left_shift": 0.35, "atypical_lymphocytes": 0.05, "thrombocytopenia": 0.1, "eosinophilia": 0.05, "lymphocyte_predominant": 0.05},
        "L20":  {"not_done": 0.05, "normal": 0.45, "elevated": 0.5},
        "L31":  {"not_done": 0.05, "normal": 0.03, "abscess": 0.85, "mass": 0.03, "other_abnormal": 0.04},
        "S05":  {"absent": 0.6, "mild": 0.28, "severe": 0.12},
        "S07":  {"absent": 0.2, "mild": 0.35, "severe": 0.45},
        "S09":  {"absent": 0.2, "present": 0.8},
        "S12":  {"absent": 0.08, "present": 0.92},
        "S46":  {"absent": 0.25, "present": 0.75},
        "T01":  {"under_3d": 0.05, "3d_to_1w": 0.2, "1w_to_3w": 0.45, "over_3w": 0.3},  # アメーバ: やや遷延
        "L66":  {"not_assessed": 0.05, "normal": 0.15, "hepatocellular": 0.55, "cholestatic": 0.15, "congestive": 0.1},
        "S89":  {"epigastric": 0.04, "RUQ": 0.82, "RLQ": 0.02, "LLQ": 0.01, "suprapubic": 0.01, "diffuse": 0.1},
    }

    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D29' in pe:
            del pe['D29']
            if var_id in bact_pe:
                pe['D29'] = bact_pe[var_id]
            if var_id in amebic_pe:
                pe['D362'] = amebic_pe[var_id]

    return s3

# ============================================================
# TEST CASES
# ============================================================
def update_cases(ts):
    # D106: all 4 cases are DM → stay D106
    # D29: both cases are bacterial → stay D29
    # No remapping needed for this batch!
    return ts

# ============================================================
# Validation
# ============================================================
def validate(s3):
    nop = s3['noisy_or_params']
    for new_id, name in [('D361', 'PM'), ('D362', 'Amebic')]:
        count = sum(1 for v in nop if new_id in nop[v].get('parent_effects', {}))
        print(f"  {new_id} ({name}): {count} parent_effects entries")
        assert count > 0, f"{new_id} has 0 parent_effects — will be INVISIBLE!"

    for did, name in [('D106', 'DM'), ('D29', 'Bacterial')]:
        count = sum(1 for v in nop if did in nop[v].get('parent_effects', {}))
        print(f"  {did} ({name}): {count} parent_effects entries")
        assert count > 0, f"{did} has 0 parent_effects!"

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("Loading files...")
    s1 = load_json('step1_fever_v2.7.json')
    s2 = load_json('step2_fever_edges_v4.json')
    s3 = load_json('step3_fever_cpts_v2.json')
    ts = load_json('real_case_test_suite.json')

    print("Updating step1...")
    s1 = update_step1(s1)
    print("Updating step2...")
    s2 = update_step2(s2)
    print("Updating step3...")
    s3 = update_step3(s3)
    print("Updating test cases...")
    ts = update_cases(ts)

    print("Validating...")
    validate(s3)

    print("Saving...")
    save_json('step1_fever_v2.7.json', s1)
    save_json('step2_fever_edges_v4.json', s2)
    save_json('step3_fever_cpts_v2.json', s3)
    save_json('real_case_test_suite.json', ts)

    print("Done! D106→DM+D361(PM), D29→Bacterial+D362(Amebic)")
