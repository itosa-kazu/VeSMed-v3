#!/usr/bin/env python3
"""
B群 Batch1: D61 PMR/GCA分割 + D65 痛風/偽痛風分割

D61 PMR/GCA → D61(PMR) + D359(GCA)
  - R129(GCA) → D359
  - 差別化: PMR=肩骨盤帯筋痛+朝のこわばり, GCA=側頭部頭痛+視力障害+大血管炎

D65 痛風/偽痛風 → D65(痛風) + D360(偽痛風/CPPD)
  - R134(偽痛風) → D360
  - 差別化: 痛風=中年男性+尿酸高+第1MTP, 偽痛風=高齢者+尿酸正常+膝
"""

import json
import copy

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# STEP 1: Variables / Disease Definitions
# ============================================================
def update_step1(s1):
    variables = s1['variables']

    # --- D61: Rename to PMR only ---
    for v in variables:
        if isinstance(v, dict) and v.get('id') == 'D61':
            v['name'] = 'polymyalgia_rheumatica'
            v['name_ja'] = 'リウマチ性多発筋痛症(PMR)'
            v['icd10'] = 'M35.3'
            v['key_features'] = '50歳以上の発熱+肩・骨盤帯の著明な筋痛+朝のこわばり(>30分)+ESR著増。PSL低用量で劇的改善。'
            break

    # --- D359: GCA (巨細胞動脈炎) ---
    d359 = {
        "id": "D359",
        "name": "giant_cell_arteritis",
        "name_ja": "巨細胞動脈炎(GCA)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "M31.6",
        "category_sub": "autoimmune",
        "severity": "high",
        "key_features": "50歳以上の新規頭痛+側頭動脈圧痛+顎跛行+視力障害→緊急。ESR著増+CRP著増。大血管型はFUO。",
        "diagnostic_profile": {}
    }

    # --- D65: Rename to gout only ---
    for v in variables:
        if isinstance(v, dict) and v.get('id') == 'D65':
            v['name'] = 'gout'
            v['name_ja'] = '痛風発作'
            v['icd10'] = 'M10'
            v['key_features'] = '急性の単関節腫脹+発赤+激痛+発熱。第1MTP好発。中年男性。血清尿酸高値。関節液に尿酸ナトリウム結晶。'
            break

    # --- D360: 偽痛風(CPPD) ---
    d360 = {
        "id": "D360",
        "name": "pseudogout_CPPD",
        "name_ja": "偽痛風(CPPD発作)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "M11",
        "category_sub": "crystal",
        "severity": "low",
        "key_features": "高齢者の急性単関節炎。膝好発。X線で軟骨石灰化。関節液にピロリン酸カルシウム結晶。尿酸正常。",
        "diagnostic_profile": {}
    }

    # Insert new diseases at end of disease list
    variables.append(d359)
    variables.append(d360)

    return s1

# ============================================================
# STEP 2: Edges
# ============================================================
def update_step2(s2):
    edges = s2['edges']

    # --- Remove all D61 edges ---
    edges = [e for e in edges if e.get('from') != 'D61' and e.get('to') != 'D61']

    # --- D61 (PMR) edges: 肩骨盤帯筋痛中心 ---
    pmr_edges = [
        {"from": "R01", "to": "D61", "reason": "50歳以上に多い(PMR)", "from_name": "age_group", "to_name": "PMR"},
        {"from": "R02", "to": "D61", "reason": "PMR。高齢女性2:1", "from_name": "sex", "to_name": "D61"},
        {"from": "D61", "to": "E01", "reason": "発熱(微熱〜中等度)", "from_name": "PMR", "to_name": "temperature",
         "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D61", "to": "S06", "reason": "肩・骨盤帯の著明な筋痛(PMR主症状)", "from_name": "PMR", "to_name": "myalgia",
         "onset_day_range": {"earliest": 0, "typical": 1, "latest": 7}},
        {"from": "D61", "to": "S27", "reason": "朝のこわばり>30分(PMR特異的)", "from_name": "PMR", "to_name": "morning_stiffness",
         "onset_day_range": {"earliest": 0, "typical": 1, "latest": 7}},
        {"from": "D61", "to": "S07", "reason": "全身倦怠感", "from_name": "PMR", "to_name": "fatigue",
         "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D61", "to": "L28", "reason": "ESR著増(>50が多い, >100も)", "from_name": "PMR", "to_name": "ESR",
         "onset_day_range": {"earliest": 0, "typical": 3, "latest": 7}},
        {"from": "D61", "to": "L02", "reason": "CRP著増", "from_name": "PMR", "to_name": "CRP",
         "onset_day_range": {"earliest": 0, "typical": 3, "latest": 7}},
        {"from": "D61", "to": "T01", "reason": "PMR慢性経過(週〜月単位)", "from_name": "PMR", "to_name": "fever_duration",
         "onset_day_range": {"earliest": 7, "typical": 21, "latest": 120}},
        {"from": "D61", "to": "L01", "reason": "白血球軽度上昇", "from_name": "PMR", "to_name": "WBC"},
        {"from": "D61", "to": "S17", "reason": "体重減少(慢性炎症)", "from_name": "PMR", "to_name": "weight_loss"},
        {"from": "D61", "to": "S46", "reason": "食欲不振", "from_name": "PMR", "to_name": "anorexia"},
        {"from": "D61", "to": "S09", "reason": "悪寒(全身炎症)", "from_name": "PMR", "to_name": "chills"},
        {"from": "D61", "to": "L15", "reason": "フェリチン上昇(炎症)", "from_name": "PMR", "to_name": "ferritin"},
        {"from": "D61", "to": "S145", "reason": "朝のこわばり>30分(PMR特異的所見)", "from_name": "PMR", "to_name": "S145"},
        {"from": "D61", "to": "S146", "reason": "活動で改善(炎症性パターン)", "from_name": "PMR", "to_name": "S146"},
    ]

    # --- D359 (GCA) edges: 頭痛・視力障害中心 ---
    gca_edges = [
        {"from": "R01", "to": "D359", "reason": "50歳以上(GCAは70歳以上にピーク)", "from_name": "age_group", "to_name": "GCA"},
        {"from": "R02", "to": "D359", "reason": "GCA。高齢女性3:1", "from_name": "sex", "to_name": "D359"},
        {"from": "D359", "to": "E01", "reason": "発熱(GCA: 中等度〜高熱, FUOの原因)", "from_name": "GCA", "to_name": "temperature",
         "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D359", "to": "S05", "reason": "新規頭痛(GCA主症状, 側頭部)", "from_name": "GCA", "to_name": "headache",
         "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D359", "to": "S60", "reason": "側頭部頭痛(GCA 70-80%)", "from_name": "GCA", "to_name": "S60"},
        {"from": "D359", "to": "S06", "reason": "筋痛(GCA合併PMR 40-60%)", "from_name": "GCA", "to_name": "myalgia",
         "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D359", "to": "S27", "reason": "朝のこわばり(GCA合併PMR時)", "from_name": "GCA", "to_name": "morning_stiffness",
         "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D359", "to": "S07", "reason": "全身倦怠感", "from_name": "GCA", "to_name": "fatigue",
         "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D359", "to": "L28", "reason": "ESR著増(>100が多い)", "from_name": "GCA", "to_name": "ESR",
         "onset_day_range": {"earliest": 0, "typical": 3, "latest": 7}},
        {"from": "D359", "to": "L02", "reason": "CRP著増", "from_name": "GCA", "to_name": "CRP",
         "onset_day_range": {"earliest": 0, "typical": 3, "latest": 7}},
        {"from": "D359", "to": "T01", "reason": "GCA慢性経過(週〜月単位)", "from_name": "GCA", "to_name": "fever_duration",
         "onset_day_range": {"earliest": 7, "typical": 21, "latest": 120}},
        {"from": "D359", "to": "L01", "reason": "白血球軽度上昇", "from_name": "GCA", "to_name": "WBC"},
        {"from": "D359", "to": "S17", "reason": "体重減少(慢性炎症)", "from_name": "GCA", "to_name": "weight_loss"},
        {"from": "D359", "to": "S46", "reason": "食欲不振", "from_name": "GCA", "to_name": "anorexia"},
        {"from": "D359", "to": "S09", "reason": "悪寒", "from_name": "GCA", "to_name": "chills"},
        {"from": "D359", "to": "L11", "reason": "肝酵素軽度上昇(GCA 30%)", "from_name": "GCA", "to_name": "AST_ALT"},
        {"from": "D359", "to": "L15", "reason": "フェリチン著増(GCAで高い)", "from_name": "GCA", "to_name": "ferritin"},
        {"from": "D359", "to": "S01", "reason": "咳嗽(大血管型GCA)", "from_name": "GCA", "to_name": "cough"},
        {"from": "D359", "to": "S84", "reason": "乾性咳嗽(大血管型GCA)", "from_name": "GCA", "to_name": "S84"},
        {"from": "D359", "to": "S145", "reason": "朝のこわばり(GCA合併PMR時)", "from_name": "GCA", "to_name": "S145"},
        {"from": "D359", "to": "S146", "reason": "活動で改善(炎症性パターン)", "from_name": "GCA", "to_name": "S146"},
    ]

    # --- Remove all D65 edges ---
    edges = [e for e in edges if e.get('from') != 'D65' and e.get('to') != 'D65']

    # --- D65 (痛風) edges ---
    gout_edges = [
        {"from": "R01", "to": "D65", "reason": "痛風。中年男性に多い", "from_name": "age_group", "to_name": "gout"},
        {"from": "R02", "to": "D65", "reason": "痛風。男性9:1", "from_name": "sex", "to_name": "D65"},
        {"from": "D65", "to": "E01", "reason": "発熱(急性発作時)", "from_name": "gout", "to_name": "temperature",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D65", "to": "S23", "reason": "関節腫脹(単関節, 第1MTP好発)", "from_name": "gout", "to_name": "joint_swelling",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D65", "to": "E21", "reason": "関節の発赤・熱感", "from_name": "gout", "to_name": "joint_redness_warmth",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D65", "to": "S08", "reason": "関節痛(激痛)", "from_name": "gout", "to_name": "arthralgia",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D65", "to": "L23", "reason": "尿酸高値(痛風特異的)", "from_name": "gout", "to_name": "uric_acid",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D65", "to": "L30", "reason": "関節液:尿酸ナトリウム結晶", "from_name": "gout", "to_name": "joint_fluid",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D65", "to": "L02", "reason": "CRP上昇", "from_name": "gout", "to_name": "CRP",
         "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D65", "to": "L01", "reason": "白血球上昇(急性発作時)", "from_name": "gout", "to_name": "WBC"},
        {"from": "D65", "to": "T01", "reason": "発作は数日で自然軽快", "from_name": "gout", "to_name": "fever_duration"},
        {"from": "D65", "to": "T02", "reason": "急性発症", "from_name": "gout", "to_name": "onset_speed"},
        {"from": "D65", "to": "E02", "reason": "頻脈(急性発作時の疼痛)", "from_name": "gout", "to_name": "heart_rate"},
        {"from": "D65", "to": "L28", "reason": "ESR上昇(急性炎症)", "from_name": "gout", "to_name": "ESR"},
        {"from": "D65", "to": "S90", "reason": "関節痛の分布(単関節)", "from_name": "gout", "to_name": "S90"},
        {"from": "D65", "to": "S91", "reason": "関節腫脹の分布(単関節)", "from_name": "gout", "to_name": "S91"},
        {"from": "D65", "to": "E47", "reason": "関節炎症の分布(単関節)", "from_name": "gout", "to_name": "E47"},
    ]

    # --- D360 (偽痛風/CPPD) edges ---
    cppd_edges = [
        {"from": "R01", "to": "D360", "reason": "偽痛風。高齢者(60歳以上)に多い", "from_name": "age_group", "to_name": "CPPD"},
        {"from": "R02", "to": "D360", "reason": "偽痛風。男女差少ない(やや女性多い)", "from_name": "sex", "to_name": "D360"},
        {"from": "D360", "to": "E01", "reason": "発熱(急性発作時)", "from_name": "CPPD", "to_name": "temperature",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D360", "to": "S23", "reason": "関節腫脹(単関節, 膝好発)", "from_name": "CPPD", "to_name": "joint_swelling",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D360", "to": "E21", "reason": "関節の発赤・熱感", "from_name": "CPPD", "to_name": "joint_redness_warmth",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D360", "to": "S08", "reason": "関節痛(激痛)", "from_name": "CPPD", "to_name": "arthralgia",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D360", "to": "L23", "reason": "尿酸正常(痛風との鑑別点)", "from_name": "CPPD", "to_name": "uric_acid",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D360", "to": "L30", "reason": "関節液:ピロリン酸カルシウム結晶", "from_name": "CPPD", "to_name": "joint_fluid",
         "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D360", "to": "L02", "reason": "CRP上昇", "from_name": "CPPD", "to_name": "CRP",
         "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D360", "to": "L01", "reason": "白血球上昇(急性発作時)", "from_name": "CPPD", "to_name": "WBC"},
        {"from": "D360", "to": "T01", "reason": "発作は数日〜1週で軽快", "from_name": "CPPD", "to_name": "fever_duration"},
        {"from": "D360", "to": "T02", "reason": "急性発症", "from_name": "CPPD", "to_name": "onset_speed"},
        {"from": "D360", "to": "E02", "reason": "頻脈(疼痛)", "from_name": "CPPD", "to_name": "heart_rate"},
        {"from": "D360", "to": "L28", "reason": "ESR上昇", "from_name": "CPPD", "to_name": "ESR"},
        {"from": "D360", "to": "S90", "reason": "関節痛の分布(単関節)", "from_name": "CPPD", "to_name": "S90"},
        {"from": "D360", "to": "S91", "reason": "関節腫脹の分布(単関節)", "from_name": "CPPD", "to_name": "S91"},
        {"from": "D360", "to": "E47", "reason": "関節炎症の分布(単関節)", "from_name": "CPPD", "to_name": "E47"},
    ]

    edges.extend(pmr_edges)
    edges.extend(gca_edges)
    edges.extend(gout_edges)
    edges.extend(cppd_edges)

    s2['edges'] = edges
    s2['total_edges'] = len(edges)
    return s2

# ============================================================
# STEP 3: CPTs
# ============================================================
def update_step3(s3):
    rp = s3['root_priors']
    fc = s3['full_cpts']
    nop = s3['noisy_or_params']

    # ========================================
    # D61 PMR/GCA → D61 PMR + D359 GCA
    # ========================================

    # (A) root_priors: 分割
    # PMR: 70% of combined, more female, peak 65+
    rp['D61'] = {
        "parents": ["R02", "R01"],
        "description": "PMR。50歳以上の高齢女性2:1。GCAの3倍多い",
        "cpt": {
            "male|40_64": 0.0015,
            "male|65_plus": 0.003,
            "female|40_64": 0.002,
            "female|65_plus": 0.006
        }
    }
    # GCA: 30% of combined, even more female, peak 70+
    rp['D359'] = {
        "parents": ["R02", "R01"],
        "description": "GCA。70歳以上にピーク。女性3:1",
        "cpt": {
            "male|40_64": 0.0005,
            "male|65_plus": 0.001,
            "female|40_64": 0.001,
            "female|65_plus": 0.003
        }
    }

    # (B) full_cpts
    fc['D61'] = {
        "parents": ["R01"],
        "description": "リウマチ性多発筋痛症(PMR)",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.0005, "40_64": 0.003, "65_plus": 0.01
        }
    }
    fc['D359'] = {
        "parents": ["R01"],
        "description": "巨細胞動脈炎(GCA)",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.0003, "40_64": 0.002, "65_plus": 0.005
        }
    }

    # (C) noisy_or_params - D61 not in noisy_or_params as a disease entry, skip

    # (D) ★最重要★ parent_effects
    # D61 currently in: E01, L01, L02, L11, L15, L28, S01, S05, S06, S07, S09, S17, S27, S46, T01, S60, S84, S145, S146

    # PMR (D61) parent_effects - 筋痛/こわばり中心、頭痛弱い
    pmr_pe = {
        "E01":  {"under_37.5": 0.1, "37.5_38.0": 0.35, "38.0_39.0": 0.4, "39.0_40.0": 0.12, "over_40.0": 0.02, "hypothermia_under_35": 0.01},
        "L01":  {"low_under_4000": 0.03, "normal_4000_10000": 0.45, "high_10000_20000": 0.4, "very_high_over_20000": 0.12},
        "L02":  {"normal_under_0.3": 0.02, "mild_0.3_3": 0.05, "moderate_3_10": 0.23, "high_over_10": 0.7},
        "L15":  {"normal": 0.35, "mild_elevated": 0.5, "very_high_over_1000": 0.13, "extreme_over_10000": 0.02},
        "L28":  {"normal": 0.03, "elevated": 0.27, "very_high_over_100": 0.7},
        "S06":  {"absent": 0.02, "present": 0.98},    # PMR主症状
        "S07":  {"absent": 0.1, "mild": 0.3, "severe": 0.6},
        "S09":  {"absent": 0.6, "present": 0.4},
        "S17":  {"absent": 0.4, "present": 0.6},
        "S27":  {"absent": 0.03, "present": 0.97},    # PMR主症状
        "S46":  {"absent": 0.35, "present": 0.65},
        "T01":  {"under_3d": 0.02, "3d_to_1w": 0.03, "1w_to_3w": 0.15, "over_3w": 0.8},
        "S05":  {"absent": 0.7, "mild": 0.2, "severe": 0.1},  # PMR: 頭痛は稀
        "S145": {"under_30min": 0.05, "over_30min": 0.55, "over_1hour": 0.4},  # PMR特異
        "S146": {"improves_with_activity": 0.65, "worsens_with_activity": 0.15, "no_change": 0.2},
    }

    # GCA (D359) parent_effects - 頭痛/視力/大血管炎中心
    gca_pe = {
        "E01":  {"under_37.5": 0.05, "37.5_38.0": 0.15, "38.0_39.0": 0.35, "39.0_40.0": 0.35, "over_40.0": 0.09, "hypothermia_under_35": 0.01},
        "L01":  {"low_under_4000": 0.03, "normal_4000_10000": 0.35, "high_10000_20000": 0.5, "very_high_over_20000": 0.12},
        "L02":  {"normal_under_0.3": 0.01, "mild_0.3_3": 0.02, "moderate_3_10": 0.12, "high_over_10": 0.85},
        "L11":  {"normal": 0.6, "mild_elevated": 0.35, "very_high": 0.05},  # GCA肝酵素30%
        "L15":  {"normal": 0.15, "mild_elevated": 0.4, "very_high_over_1000": 0.35, "extreme_over_10000": 0.1},  # GCAフェリチン著増
        "L28":  {"normal": 0.02, "elevated": 0.13, "very_high_over_100": 0.85},  # GCA ESR著増
        "S01":  {"absent": 0.8, "present": 0.2},     # 大血管型GCAで咳嗽
        "S05":  {"absent": 0.15, "mild": 0.2, "severe": 0.65},  # GCA主症状:頭痛
        "S06":  {"absent": 0.45, "present": 0.55},    # GCA:PMR合併40-60%
        "S07":  {"absent": 0.1, "mild": 0.25, "severe": 0.65},
        "S09":  {"absent": 0.5, "present": 0.5},
        "S17":  {"absent": 0.3, "present": 0.7},
        "S27":  {"absent": 0.45, "present": 0.55},    # GCA:PMR合併時のみ
        "S46":  {"absent": 0.25, "present": 0.75},
        "T01":  {"under_3d": 0.02, "3d_to_1w": 0.03, "1w_to_3w": 0.2, "over_3w": 0.75},
        "S60":  {"bilateral_pressing": 0.7, "unilateral_pulsating": 0.15, "periorbital_stabbing": 0.03, "thunderclap": 0.02, "progressive_with_neuro": 0.08, "electric_triggered": 0.02},
        "S84":  {"dry": 0.85, "productive": 0.15},
        "S145": {"under_30min": 0.2, "over_30min": 0.5, "over_1hour": 0.3},
        "S146": {"improves_with_activity": 0.5, "worsens_with_activity": 0.25, "no_change": 0.25},
    }

    # Update parent_effects: remove D61, add D61(PMR) + D359(GCA)
    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D61' in pe:
            del pe['D61']
            if var_id in pmr_pe:
                pe['D61'] = pmr_pe[var_id]
            if var_id in gca_pe:
                pe['D359'] = gca_pe[var_id]

    # ========================================
    # D65 痛風/偽痛風 → D65 痛風 + D360 偽痛風
    # ========================================

    # (A) root_priors
    # 痛風: 中年男性9:1
    rp['D65'] = {
        "parents": ["R02", "R01"],
        "description": "痛風。中年男性9:1",
        "cpt": {
            "male|18_39": 0.003,
            "male|40_64": 0.01,
            "male|65_plus": 0.007,
            "female|18_39": 0.0003,
            "female|40_64": 0.0008,
            "female|65_plus": 0.002
        }
    }
    # 偽痛風: 高齢者、男女差少ない
    rp['D360'] = {
        "parents": ["R02", "R01"],
        "description": "偽痛風(CPPD)。高齢者に多い。男女差少ない",
        "cpt": {
            "male|18_39": 0.0001,
            "male|40_64": 0.001,
            "male|65_plus": 0.004,
            "female|18_39": 0.0001,
            "female|40_64": 0.001,
            "female|65_plus": 0.005
        }
    }

    # (B) full_cpts
    fc['D65'] = {
        "parents": ["R01"],
        "description": "痛風発作",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.002, "40_64": 0.006, "65_plus": 0.005
        }
    }
    fc['D360'] = {
        "parents": ["R01"],
        "description": "偽痛風(CPPD発作)",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.0002, "40_64": 0.001, "65_plus": 0.004
        }
    }

    # (D) parent_effects
    # D65 currently in: E01, E02, E21, L01, L02, L23, L28, L30, S08, S23, T01, T02, S90, S91, E47

    # 痛風 (D65): 尿酸高値が特異的
    gout_pe = {
        "E01":  {"under_37.5": 0.05, "37.5_38.0": 0.25, "38.0_39.0": 0.4, "39.0_40.0": 0.25, "over_40.0": 0.04, "hypothermia_under_35": 0.01},
        "E02":  {"under_100": 0.3, "100_120": 0.45, "over_120": 0.25},
        "E21":  {"absent": 0.05, "present": 0.95},
        "L01":  {"low_under_4000": 0.03, "normal_4000_10000": 0.35, "high_10000_20000": 0.5, "very_high_over_20000": 0.12},
        "L02":  {"normal_under_0.3": 0.1, "mild_0.3_3": 0.3, "moderate_3_10": 0.4, "high_over_10": 0.2},
        "L23":  {"not_done": 0.05, "normal": 0.1, "elevated": 0.85},  # 痛風: 尿酸高値85%
        "L28":  {"normal": 0.15, "elevated": 0.85},
        "L30":  {"not_done": 0.1, "inflammatory": 0.05, "septic": 0.03, "crystals": 0.82},  # 痛風: 結晶82%
        "S08":  {"absent": 0.02, "present": 0.98},
        "S23":  {"absent": 0.05, "present": 0.95},
        "T01":  {"under_3d": 0.6, "3d_to_1w": 0.3, "1w_to_3w": 0.08, "over_3w": 0.02},
        "T02":  {"sudden": 0.1, "acute": 0.4, "subacute": 0.4, "chronic": 0.1},
        "S90":  {"monoarticular": 0.75, "oligoarticular": 0.15, "polyarticular_symmetric": 0.02, "polyarticular_asymmetric": 0.05, "migratory": 0.03},
        "S91":  {"monoarticular": 0.95, "polyarticular": 0.05},
        "E47":  {"monoarticular": 0.95, "polyarticular": 0.05},
    }

    # 偽痛風 (D360): 尿酸正常が特異的
    cppd_pe = {
        "E01":  {"under_37.5": 0.1, "37.5_38.0": 0.35, "38.0_39.0": 0.35, "39.0_40.0": 0.15, "over_40.0": 0.04, "hypothermia_under_35": 0.01},
        "E02":  {"under_100": 0.4, "100_120": 0.4, "over_120": 0.2},
        "E21":  {"absent": 0.08, "present": 0.92},
        "L01":  {"low_under_4000": 0.03, "normal_4000_10000": 0.4, "high_10000_20000": 0.45, "very_high_over_20000": 0.12},
        "L02":  {"normal_under_0.3": 0.05, "mild_0.3_3": 0.15, "moderate_3_10": 0.4, "high_over_10": 0.4},  # CPPD: CRPやや高め
        "L23":  {"not_done": 0.05, "normal": 0.8, "elevated": 0.15},   # 偽痛風: 尿酸正常80%
        "L28":  {"normal": 0.1, "elevated": 0.9},
        "L30":  {"not_done": 0.1, "inflammatory": 0.1, "septic": 0.05, "crystals": 0.75},  # CPPD結晶
        "S08":  {"absent": 0.03, "present": 0.97},
        "S23":  {"absent": 0.05, "present": 0.95},
        "T01":  {"under_3d": 0.4, "3d_to_1w": 0.4, "1w_to_3w": 0.15, "over_3w": 0.05},  # CPPD: やや遷延
        "T02":  {"sudden": 0.05, "acute": 0.3, "subacute": 0.5, "chronic": 0.15},
        "S90":  {"monoarticular": 0.7, "oligoarticular": 0.2, "polyarticular_symmetric": 0.03, "polyarticular_asymmetric": 0.05, "migratory": 0.02},
        "S91":  {"monoarticular": 0.9, "polyarticular": 0.1},
        "E47":  {"monoarticular": 0.9, "polyarticular": 0.1},
    }

    # Update parent_effects: remove D65, add D65(gout) + D360(CPPD)
    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D65' in pe:
            del pe['D65']
            if var_id in gout_pe:
                pe['D65'] = gout_pe[var_id]
            if var_id in cppd_pe:
                pe['D360'] = cppd_pe[var_id]

    return s3

# ============================================================
# TEST CASES: 案例再マッピング
# ============================================================
def update_cases(ts):
    cases = ts['cases']
    for c in cases:
        cid = c.get('id', '')
        exp = c.get('expected_id', '')

        # R129: GCA → D359
        if cid == 'R129' and exp == 'D61':
            c['expected_id'] = 'D359'
            c['final_diagnosis'] = '巨細胞動脈炎(大血管型GCA)'

        # R134: 偽痛風 → D360
        if cid == 'R134' and exp == 'D65':
            c['expected_id'] = 'D360'
            c['final_diagnosis'] = '偽痛風(CPPD発作)'

    return ts

# ============================================================
# Validation
# ============================================================
def validate(s3):
    nop = s3['noisy_or_params']
    for new_id, name in [('D359', 'GCA'), ('D360', 'CPPD')]:
        count = sum(1 for v in nop if new_id in nop[v].get('parent_effects', {}))
        print(f"  {new_id} ({name}): {count} parent_effects entries")
        assert count > 0, f"{new_id} has 0 parent_effects — will be INVISIBLE!"

    # Check D61 and D65 still have parent_effects
    for did, name in [('D61', 'PMR'), ('D65', 'Gout')]:
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

    print("Updating step1 (disease definitions)...")
    s1 = update_step1(s1)

    print("Updating step2 (edges)...")
    s2 = update_step2(s2)

    print("Updating step3 (CPTs)...")
    s3 = update_step3(s3)

    print("Updating test cases...")
    ts = update_cases(ts)

    print("Validating...")
    validate(s3)

    print("Saving files...")
    save_json('step1_fever_v2.7.json', s1)
    save_json('step2_fever_edges_v4.json', s2)
    save_json('step3_fever_cpts_v2.json', s3)
    save_json('real_case_test_suite.json', ts)

    print("Done! D61→PMR+D359(GCA), D65→Gout+D360(CPPD)")
