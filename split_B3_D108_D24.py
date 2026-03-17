#!/usr/bin/env python3
"""
B群 Batch3: D108 HBV分割 + D24 TSS分割

D108 B型肝炎 → D108(急性HBV) + D363(慢性HBV増悪/再活性化)
  - R173,R174,R181(全急性) → D108残留
  - 差別化: 急性=若年+IgM-HBc(+)+前駆症状, 慢性増悪=既知キャリア+免疫抑制契機

D24 TSS → D24(黄色ブドウ球菌TSS) + D364(劇症型GAS/iGAS)
  - R88(TSS) → D24残留, R91(iGAS) → D364
  - 差別化: TSS=びまん性紅皮+タンポン+消化器, iGAS=局所壊死+創傷+急速進行
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

    # D108: Rename to acute HBV
    for v in variables:
        if isinstance(v, dict) and v.get('id') == 'D108':
            v['name'] = 'acute_hepatitis_B'
            v['name_ja'] = '急性B型肝炎'
            v['icd10'] = 'B16'
            v['key_features'] = 'HBV急性感染。前駆期(倦怠感+関節痛)→黄疸期(黄疸+AST/ALT著増)。IgM-HBc陽性。若年成人。'
            break

    # D363: 慢性HBV増悪
    d363 = {
        "id": "D363",
        "name": "chronic_hepatitis_B_flare",
        "name_ja": "慢性B型肝炎増悪(再活性化)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "B18.1",
        "category_sub": "viral_hepatitis",
        "severity": "high",
        "key_features": "既知HBVキャリアの急性増悪。免疫抑制剤/化学療法が契機。HBV-DNA急上昇+肝酵素著増。劇症化リスク。",
        "diagnostic_profile": {}
    }

    # D24: Rename to Staph TSS
    for v in variables:
        if isinstance(v, dict) and v.get('id') == 'D24':
            v['name'] = 'staphylococcal_TSS'
            v['name_ja'] = '黄色ブドウ球菌性TSS'
            v['icd10'] = 'A48.3'
            v['key_features'] = '高熱+びまん性紅皮症+ショック+多臓器不全。タンポン/創傷。消化器症状(嘔吐下痢)。落屑(7-14日目)。'
            break

    # D364: iGAS
    d364 = {
        "id": "D364",
        "name": "invasive_group_A_strep",
        "name_ja": "劇症型溶血性レンサ球菌感染症(iGAS)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "A48.0",
        "category_sub": "bacterial",
        "severity": "critical",
        "key_features": "急速進行性の軟部組織感染→壊死性筋膜炎+ショック+多臓器不全。局所疼痛が激烈。創傷/水痘が侵入門戸。",
        "diagnostic_profile": {}
    }

    variables.append(d363)
    variables.append(d364)
    return s1

# ============================================================
# STEP 2
# ============================================================
def update_step2(s2):
    edges = s2['edges']

    # --- Remove all D108 edges ---
    edges = [e for e in edges if e.get('from') != 'D108' and e.get('to') != 'D108']

    # --- D108 (急性HBV) edges ---
    acute_hbv_edges = [
        {"from": "R01", "to": "D108", "reason": "急性HBV。若年成人に多い", "from_name": "age_group", "to_name": "D108"},
        {"from": "R02", "to": "D108", "reason": "急性HBV。男性やや多い", "from_name": "sex", "to_name": "D108"},
        {"from": "D108", "to": "E01", "reason": "急性HBV: 前駆期発熱(30-50%)", "from_name": "acute_HBV", "to_name": "temperature"},
        {"from": "D108", "to": "S07", "reason": "急性HBV: 倦怠感(90%+)", "from_name": "acute_HBV", "to_name": "fatigue"},
        {"from": "D108", "to": "S46", "reason": "急性HBV: 食欲不振(80%+)", "from_name": "acute_HBV", "to_name": "anorexia"},
        {"from": "D108", "to": "S13", "reason": "急性HBV: 嘔気嘔吐(60-80%)", "from_name": "acute_HBV", "to_name": "nausea"},
        {"from": "D108", "to": "E18", "reason": "急性HBV: 黄疸(50-70%)", "from_name": "acute_HBV", "to_name": "jaundice"},
        {"from": "D108", "to": "S12", "reason": "急性HBV: 右上腹部痛(40-60%)", "from_name": "acute_HBV", "to_name": "abd_distension"},
        {"from": "D108", "to": "E34", "reason": "急性HBV: 肝腫大(30-50%)", "from_name": "acute_HBV", "to_name": "hepatomegaly"},
        {"from": "D108", "to": "S08", "reason": "急性HBV: 関節痛(前駆期10-30%,免疫複合体)", "from_name": "acute_HBV", "to_name": "arthralgia"},
        {"from": "D108", "to": "L11", "reason": "急性HBV: AST/ALT著増(>1000)", "from_name": "acute_HBV", "to_name": "liver_enzymes"},
        {"from": "D108", "to": "L01", "reason": "急性HBV: WBC正常〜軽度低下", "from_name": "acute_HBV", "to_name": "WBC"},
        {"from": "D108", "to": "L02", "reason": "急性HBV: CRP軽度上昇", "from_name": "acute_HBV", "to_name": "CRP"},
        {"from": "D108", "to": "L39", "reason": "急性HBV: HBsAg+IgM-HBc陽性", "from_name": "acute_HBV", "to_name": "hepatitis_serology"},
        {"from": "D108", "to": "T01", "reason": "急性HBV: 亜急性(前駆1-4週→黄疸期)", "from_name": "acute_HBV", "to_name": "fever_duration"},
        {"from": "D108", "to": "T02", "reason": "急性HBV: 緩徐発症", "from_name": "acute_HBV", "to_name": "onset_speed"},
        {"from": "D108", "to": "S17", "reason": "急性HBV: 体重減少(30-40%)", "from_name": "acute_HBV", "to_name": "weight_loss"},
        {"from": "D108", "to": "E12", "reason": "急性HBV: 蕁麻疹/血管炎(10-20%)", "from_name": "acute_HBV", "to_name": "skin"},
        {"from": "D108", "to": "S09", "reason": "急性HBV: 悪寒", "from_name": "acute_HBV", "to_name": "chills"},
        {"from": "D108", "to": "L66", "reason": "急性HBV: 肝細胞型", "from_name": "acute_HBV", "to_name": "L66"},
        {"from": "D108", "to": "S89", "reason": "急性HBV: 右上腹部痛", "from_name": "acute_HBV", "to_name": "S89"},
        {"from": "D108", "to": "S90", "reason": "急性HBV: 関節痛の分布", "from_name": "acute_HBV", "to_name": "S90"},
        {"from": "D108", "to": "E50", "reason": "急性HBV: 下腿浮腫", "from_name": "acute_HBV", "to_name": "E50"},
        {"from": "D108", "to": "E36", "reason": "急性HBV: 浮腫(10-20%)", "from_name": "acute_HBV", "to_name": "E36"},
    ]

    # --- D363 (慢性HBV増悪) edges ---
    chronic_hbv_edges = [
        {"from": "R01", "to": "D363", "reason": "慢性HBV増悪。中年に多い(キャリア)", "from_name": "age_group", "to_name": "D363"},
        {"from": "R02", "to": "D363", "reason": "慢性HBV増悪。男性やや多い", "from_name": "sex", "to_name": "D363"},
        {"from": "D363", "to": "E01", "reason": "慢性HBV増悪: 発熱(20-30%)", "from_name": "chronic_HBV_flare", "to_name": "temperature"},
        {"from": "D363", "to": "S07", "reason": "慢性HBV増悪: 倦怠感(80%+)", "from_name": "chronic_HBV_flare", "to_name": "fatigue"},
        {"from": "D363", "to": "S46", "reason": "慢性HBV増悪: 食欲不振(70%+)", "from_name": "chronic_HBV_flare", "to_name": "anorexia"},
        {"from": "D363", "to": "S13", "reason": "慢性HBV増悪: 嘔気(50-60%)", "from_name": "chronic_HBV_flare", "to_name": "nausea"},
        {"from": "D363", "to": "E18", "reason": "慢性HBV増悪: 黄疸(40-60%)", "from_name": "chronic_HBV_flare", "to_name": "jaundice"},
        {"from": "D363", "to": "S12", "reason": "慢性HBV増悪: 腹部膨満(40-50%)", "from_name": "chronic_HBV_flare", "to_name": "abd_distension"},
        {"from": "D363", "to": "E34", "reason": "慢性HBV増悪: 肝腫大/脾腫(40-60%)", "from_name": "chronic_HBV_flare", "to_name": "hepatomegaly"},
        {"from": "D363", "to": "L11", "reason": "慢性HBV増悪: AST/ALT著増(500-2000)", "from_name": "chronic_HBV_flare", "to_name": "liver_enzymes"},
        {"from": "D363", "to": "L01", "reason": "慢性HBV増悪: WBC正常〜低下", "from_name": "chronic_HBV_flare", "to_name": "WBC"},
        {"from": "D363", "to": "L02", "reason": "慢性HBV増悪: CRP軽度上昇", "from_name": "chronic_HBV_flare", "to_name": "CRP"},
        {"from": "D363", "to": "L39", "reason": "慢性HBV増悪: HBsAg+, HBV-DNA急上昇", "from_name": "chronic_HBV_flare", "to_name": "hepatitis_serology"},
        {"from": "D363", "to": "T01", "reason": "慢性HBV増悪: 亜急性〜慢性", "from_name": "chronic_HBV_flare", "to_name": "fever_duration"},
        {"from": "D363", "to": "T02", "reason": "慢性HBV増悪: 亜急性発症", "from_name": "chronic_HBV_flare", "to_name": "onset_speed"},
        {"from": "D363", "to": "S17", "reason": "慢性HBV増悪: 体重減少(20-30%)", "from_name": "chronic_HBV_flare", "to_name": "weight_loss"},
        {"from": "D363", "to": "L66", "reason": "慢性HBV増悪: 肝細胞型", "from_name": "chronic_HBV_flare", "to_name": "L66"},
        {"from": "D363", "to": "S89", "reason": "慢性HBV増悪: 右上腹部痛", "from_name": "chronic_HBV_flare", "to_name": "S89"},
        {"from": "D363", "to": "S09", "reason": "慢性HBV増悪: 悪寒", "from_name": "chronic_HBV_flare", "to_name": "chills"},
        {"from": "D363", "to": "E36", "reason": "慢性HBV増悪: 浮腫(慢性肝障害)", "from_name": "chronic_HBV_flare", "to_name": "E36"},
        {"from": "D363", "to": "E50", "reason": "慢性HBV増悪: 下腿浮腫", "from_name": "chronic_HBV_flare", "to_name": "E50"},
    ]

    # --- Remove all D24 edges ---
    edges = [e for e in edges if e.get('from') != 'D24' and e.get('to') != 'D24']

    # --- D24 (黄ブ菌TSS) edges ---
    tss_edges = [
        {"from": "R01", "to": "D24", "reason": "黄ブ菌TSS。若年女性(menstrual TSS)", "from_name": "age_group", "to_name": "D24"},
        {"from": "R02", "to": "D24", "reason": "黄ブ菌TSS。女性やや多い(menstrual)", "from_name": "sex", "to_name": "D24"},
        {"from": "R20", "to": "D24", "reason": "タンポン使用は黄ブ菌TSS主リスク", "from_name": "tampon", "to_name": "D24"},
        {"from": "R14", "to": "D24", "reason": "創傷(術後・火傷)もTSSリスク", "from_name": "wound", "to_name": "D24"},
        {"from": "D24", "to": "E01", "reason": "TSS: 高熱>38.9°C", "from_name": "TSS", "to_name": "temperature"},
        {"from": "D24", "to": "E02", "reason": "TSS: ショック性頻脈", "from_name": "TSS", "to_name": "heart_rate"},
        {"from": "D24", "to": "E03", "reason": "TSS: ショック性低血圧", "from_name": "TSS", "to_name": "blood_pressure"},
        {"from": "D24", "to": "E12", "reason": "TSS: びまん性紅皮症(sunburn-like, TSS特異的)", "from_name": "TSS", "to_name": "skin_exam"},
        {"from": "D24", "to": "E16", "reason": "TSS: ショック→意識障害", "from_name": "TSS", "to_name": "consciousness"},
        {"from": "D24", "to": "S13", "reason": "TSS: 嘔吐(70%+, TSS特異的)", "from_name": "TSS", "to_name": "vomiting"},
        {"from": "D24", "to": "S14", "reason": "TSS: 水様性下痢(60%+, TSS特異的)", "from_name": "TSS", "to_name": "diarrhea"},
        {"from": "D24", "to": "S06", "reason": "TSS: 筋肉痛(激烈)", "from_name": "TSS", "to_name": "myalgia"},
        {"from": "D24", "to": "S09", "reason": "TSS: 悪寒戦慄", "from_name": "TSS", "to_name": "rigors"},
        {"from": "D24", "to": "S18", "reason": "TSS: 皮膚症状(紅皮)", "from_name": "TSS", "to_name": "skin_complaint"},
        {"from": "D24", "to": "E25", "reason": "TSS: 結膜充血(TSS診断基準)", "from_name": "TSS", "to_name": "conj_injection"},
        {"from": "D24", "to": "L01", "reason": "TSS: WBC著増", "from_name": "TSS", "to_name": "WBC"},
        {"from": "D24", "to": "L02", "reason": "TSS: CRP著増", "from_name": "TSS", "to_name": "CRP"},
        {"from": "D24", "to": "L03", "reason": "TSS: PCT著増", "from_name": "TSS", "to_name": "PCT"},
        {"from": "D24", "to": "L09", "reason": "TSS: 血培(Staph aureus 30-50%)", "from_name": "TSS", "to_name": "blood_culture"},
        {"from": "D24", "to": "L11", "reason": "TSS: 肝酵素上昇(多臓器障害)", "from_name": "TSS", "to_name": "liver_enzymes"},
        {"from": "D24", "to": "L14", "reason": "TSS: 血小板減少(DIC)", "from_name": "TSS", "to_name": "CBC_diff"},
        {"from": "D24", "to": "L17", "reason": "TSS: CK上昇(筋炎)", "from_name": "TSS", "to_name": "CK"},
        {"from": "D24", "to": "T01", "reason": "TSS: 急性経過(数日)", "from_name": "TSS", "to_name": "fever_duration"},
        {"from": "D24", "to": "T02", "reason": "TSS: 急速発症", "from_name": "TSS", "to_name": "onset_speed"},
        {"from": "D24", "to": "M02", "reason": "TSS: ショック(80-90%)", "from_name": "TSS", "to_name": "hemodynamic"},
        {"from": "D24", "to": "E04", "reason": "TSS: 頻呼吸(ARDS)", "from_name": "TSS", "to_name": "resp_rate"},
        {"from": "D24", "to": "E05", "reason": "TSS: 低酸素(ARDS)", "from_name": "TSS", "to_name": "spo2"},
        {"from": "D24", "to": "E37", "reason": "TSS: 敗血症性心不全(JVD)", "from_name": "TSS", "to_name": "JVD"},
        {"from": "D24", "to": "L51", "reason": "TSS: BNP上昇", "from_name": "TSS", "to_name": "BNP"},
        {"from": "D24", "to": "L52", "reason": "TSS: D-dimer上昇(DIC)", "from_name": "TSS", "to_name": "D_dimer"},
        {"from": "D24", "to": "L54", "reason": "TSS: 血糖変動", "from_name": "TSS", "to_name": "glucose"},
        {"from": "D24", "to": "L55", "reason": "TSS: AKI(ショック)", "from_name": "TSS", "to_name": "creatinine"},
        {"from": "D24", "to": "L64", "reason": "TSS: DIC(30-40%)", "from_name": "TSS", "to_name": "DIC_score"},
        {"from": "D24", "to": "S86", "reason": "TSS: 水様性下痢", "from_name": "TSS", "to_name": "S86"},
        {"from": "D24", "to": "S87", "reason": "TSS: びまん性皮疹", "from_name": "TSS", "to_name": "S87"},
    ]

    # --- D364 (iGAS) edges ---
    igas_edges = [
        {"from": "R01", "to": "D364", "reason": "iGAS。全年齢だが高齢・DM・免疫不全にリスク", "from_name": "age_group", "to_name": "D364"},
        {"from": "R02", "to": "D364", "reason": "iGAS。男女差少ない", "from_name": "sex", "to_name": "D364"},
        {"from": "R14", "to": "D364", "reason": "創傷・水痘がiGASの侵入門戸", "from_name": "wound", "to_name": "D364"},
        {"from": "D364", "to": "E01", "reason": "iGAS: 高熱", "from_name": "iGAS", "to_name": "temperature"},
        {"from": "D364", "to": "E02", "reason": "iGAS: ショック性頻脈", "from_name": "iGAS", "to_name": "heart_rate"},
        {"from": "D364", "to": "E03", "reason": "iGAS: ショック性低血圧", "from_name": "iGAS", "to_name": "blood_pressure"},
        {"from": "D364", "to": "E12", "reason": "iGAS: 局所発赤腫脹→壊死(TSS型紅皮ではない)", "from_name": "iGAS", "to_name": "skin_exam"},
        {"from": "D364", "to": "S18", "reason": "iGAS: 局所激痛(壊死性筋膜炎)", "from_name": "iGAS", "to_name": "skin_complaint"},
        {"from": "D364", "to": "S06", "reason": "iGAS: 筋肉痛(激烈,壊死性)", "from_name": "iGAS", "to_name": "myalgia"},
        {"from": "D364", "to": "S09", "reason": "iGAS: 悪寒戦慄", "from_name": "iGAS", "to_name": "rigors"},
        {"from": "D364", "to": "E16", "reason": "iGAS: ショック→意識障害", "from_name": "iGAS", "to_name": "consciousness"},
        {"from": "D364", "to": "L01", "reason": "iGAS: WBC著増(左方移動)", "from_name": "iGAS", "to_name": "WBC"},
        {"from": "D364", "to": "L02", "reason": "iGAS: CRP著増", "from_name": "iGAS", "to_name": "CRP"},
        {"from": "D364", "to": "L03", "reason": "iGAS: PCT著増", "from_name": "iGAS", "to_name": "PCT"},
        {"from": "D364", "to": "L09", "reason": "iGAS: 血培GAS陽性(60-70%)", "from_name": "iGAS", "to_name": "blood_culture"},
        {"from": "D364", "to": "L11", "reason": "iGAS: 肝酵素上昇(多臓器障害)", "from_name": "iGAS", "to_name": "liver_enzymes"},
        {"from": "D364", "to": "L14", "reason": "iGAS: 血小板減少(DIC)", "from_name": "iGAS", "to_name": "CBC_diff"},
        {"from": "D364", "to": "L17", "reason": "iGAS: CK著増(横紋筋融解)", "from_name": "iGAS", "to_name": "CK"},
        {"from": "D364", "to": "T01", "reason": "iGAS: 急性経過(数日)", "from_name": "iGAS", "to_name": "fever_duration"},
        {"from": "D364", "to": "T02", "reason": "iGAS: 電撃的発症", "from_name": "iGAS", "to_name": "onset_speed"},
        {"from": "D364", "to": "M02", "reason": "iGAS: ショック(70-80%)", "from_name": "iGAS", "to_name": "hemodynamic"},
        {"from": "D364", "to": "E04", "reason": "iGAS: 頻呼吸", "from_name": "iGAS", "to_name": "resp_rate"},
        {"from": "D364", "to": "E05", "reason": "iGAS: 低酸素", "from_name": "iGAS", "to_name": "spo2"},
        {"from": "D364", "to": "L52", "reason": "iGAS: D-dimer上昇(DIC)", "from_name": "iGAS", "to_name": "D_dimer"},
        {"from": "D364", "to": "L55", "reason": "iGAS: AKI", "from_name": "iGAS", "to_name": "creatinine"},
        {"from": "D364", "to": "L64", "reason": "iGAS: DIC(40-50%)", "from_name": "iGAS", "to_name": "DIC_score"},
        {"from": "D364", "to": "S87", "reason": "iGAS: 局所疼痛・発赤", "from_name": "iGAS", "to_name": "S87"},
    ]

    edges.extend(acute_hbv_edges)
    edges.extend(chronic_hbv_edges)
    edges.extend(tss_edges)
    edges.extend(igas_edges)

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
    # D108 → D108(急性HBV) + D363(慢性増悪)
    # ========================================

    rp['D108'] = {
        "parents": ["R02", "R01"],
        "description": "急性HBV。若年成人に多い",
        "cpt": {
            "male|18_39": 0.004,
            "male|40_64": 0.002,
            "male|65_plus": 0.001,
            "female|18_39": 0.003,
            "female|40_64": 0.001,
            "female|65_plus": 0.0005
        }
    }
    rp['D363'] = {
        "parents": ["R02", "R01"],
        "description": "慢性HBV増悪。中年キャリアに多い",
        "cpt": {
            "male|18_39": 0.001,
            "male|40_64": 0.002,
            "male|65_plus": 0.001,
            "female|18_39": 0.0005,
            "female|40_64": 0.001,
            "female|65_plus": 0.0005
        }
    }

    # full_cpts - D108 had none
    fc['D108'] = {
        "parents": ["R01"],
        "description": "急性B型肝炎",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.003, "40_64": 0.002, "65_plus": 0.001
        }
    }
    fc['D363'] = {
        "parents": ["R01"],
        "description": "慢性B型肝炎増悪",
        "cpt": {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001, "13_17": 0.0001,
            "18_39": 0.001, "40_64": 0.002, "65_plus": 0.001
        }
    }

    # parent_effects
    acute_hbv_pe = {
        "E01":  {"under_37.5": 0.4, "37.5_38.0": 0.3, "38.0_39.0": 0.2, "39.0_40.0": 0.07, "over_40.0": 0.02, "hypothermia_under_35": 0.01},
        "E12":  {"maculopapular_rash": 0.1, "petechiae_purpura": 0.02, "diffuse_erythroderma": 0.05, "normal": 0.82, "vesicular_dermatomal": 0.01},
        "E18":  {"absent": 0.35, "present": 0.65},  # 急性: 黄疸多い
        "E34":  {"absent": 0.55, "present": 0.45},
        "L01":  {"low_under_4000": 0.25, "normal_4000_10000": 0.6, "high_10000_20000": 0.12, "very_high_over_20000": 0.03},
        "L02":  {"normal_under_0.3": 0.3, "mild_0.3_3": 0.45, "moderate_3_10": 0.2, "high_over_10": 0.05},
        "L11":  {"normal": 0.02, "mild_elevated": 0.05, "very_high": 0.93},  # 急性: AST/ALT著増
        "L39":  {"not_done": 0.05, "negative": 0.01, "HAV_IgM": 0.01, "HBV": 0.92, "HCV": 0.01},
        "S07":  {"absent": 0.05, "mild": 0.25, "severe": 0.7},
        "S08":  {"absent": 0.7, "present": 0.3},  # 急性: 関節痛多め(免疫複合体)
        "S09":  {"absent": 0.5, "present": 0.5},
        "S12":  {"absent": 0.45, "present": 0.55},
        "S13":  {"absent": 0.25, "present": 0.75},
        "S17":  {"absent": 0.6, "present": 0.4},
        "S46":  {"absent": 0.1, "present": 0.9},
        "T01":  {"under_3d": 0.05, "3d_to_1w": 0.2, "1w_to_3w": 0.5, "over_3w": 0.25},
        "T02":  {"sudden": 0.01, "acute": 0.04, "subacute": 0.55, "chronic": 0.4},
        "E36":  {"absent": 0.85, "present": 0.15},
        "L66":  {"not_assessed": 0.05, "normal": 0.03, "hepatocellular": 0.85, "cholestatic": 0.05, "congestive": 0.02},
        "S89":  {"epigastric": 0.18, "RUQ": 0.73, "RLQ": 0.02, "LLQ": 0.02, "suprapubic": 0.02, "diffuse": 0.03},
        "S90":  {"monoarticular": 0.1, "oligoarticular": 0.2, "polyarticular_symmetric": 0.5, "polyarticular_asymmetric": 0.1, "migratory": 0.1},
        "E50":  {"unilateral": 0.15, "bilateral": 0.85},
    }

    chronic_hbv_pe = {
        "E01":  {"under_37.5": 0.55, "37.5_38.0": 0.25, "38.0_39.0": 0.12, "39.0_40.0": 0.05, "over_40.0": 0.02, "hypothermia_under_35": 0.01},
        "E18":  {"absent": 0.5, "present": 0.5},  # 慢性増悪: 黄疸やや少ない
        "E34":  {"absent": 0.4, "present": 0.6},  # 慢性: 肝脾腫多い
        "L01":  {"low_under_4000": 0.2, "normal_4000_10000": 0.6, "high_10000_20000": 0.15, "very_high_over_20000": 0.05},
        "L02":  {"normal_under_0.3": 0.35, "mild_0.3_3": 0.4, "moderate_3_10": 0.2, "high_over_10": 0.05},
        "L11":  {"normal": 0.03, "mild_elevated": 0.15, "very_high": 0.82},  # 慢性増悪: 著増だが急性よりやや低い
        "L39":  {"not_done": 0.05, "negative": 0.02, "HAV_IgM": 0.01, "HBV": 0.9, "HCV": 0.02},
        "S07":  {"absent": 0.1, "mild": 0.35, "severe": 0.55},
        "S09":  {"absent": 0.6, "present": 0.4},
        "S12":  {"absent": 0.4, "present": 0.6},
        "S13":  {"absent": 0.4, "present": 0.6},
        "S17":  {"absent": 0.55, "present": 0.45},
        "S46":  {"absent": 0.2, "present": 0.8},
        "T01":  {"under_3d": 0.03, "3d_to_1w": 0.15, "1w_to_3w": 0.45, "over_3w": 0.37},  # 慢性: やや遷延
        "T02":  {"sudden": 0.01, "acute": 0.05, "subacute": 0.5, "chronic": 0.44},
        "E36":  {"absent": 0.7, "present": 0.3},  # 慢性: 浮腫多い
        "L66":  {"not_assessed": 0.05, "normal": 0.05, "hepatocellular": 0.75, "cholestatic": 0.1, "congestive": 0.05},
        "S89":  {"epigastric": 0.18, "RUQ": 0.7, "RLQ": 0.02, "LLQ": 0.02, "suprapubic": 0.02, "diffuse": 0.06},
        "E50":  {"unilateral": 0.1, "bilateral": 0.9},
    }

    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D108' in pe:
            del pe['D108']
            if var_id in acute_hbv_pe:
                pe['D108'] = acute_hbv_pe[var_id]
            if var_id in chronic_hbv_pe:
                pe['D363'] = chronic_hbv_pe[var_id]

    # ========================================
    # D24 → D24(黄ブ菌TSS) + D364(iGAS)
    # ========================================

    rp['D24'] = {
        "parents": ["R02", "R01"],
        "description": "黄ブ菌TSS。若年女性(menstrual TSS)",
        "cpt": {
            "male|18_39": 0.001,
            "male|40_64": 0.001,
            "male|65_plus": 0.001,
            "female|18_39": 0.003,
            "female|40_64": 0.002,
            "female|65_plus": 0.001
        }
    }
    rp['D364'] = {
        "parents": ["R02", "R01"],
        "description": "iGAS。全年齢、男女差少ない",
        "cpt": {
            "male|18_39": 0.002,
            "male|40_64": 0.002,
            "male|65_plus": 0.002,
            "female|18_39": 0.001,
            "female|40_64": 0.001,
            "female|65_plus": 0.001
        }
    }

    fc['D24'] = {
        "parents": ["R14", "R20"],
        "description": "黄ブ菌TSS。創傷+タンポンがリスク",
        "cpt": {
            "no|no": 0.0003,
            "no|yes": 0.005,
            "yes|no": 0.002,
            "yes|yes": 0.008
        }
    }
    fc['D364'] = {
        "parents": ["R14"],
        "description": "iGAS。創傷が侵入門戸",
        "cpt": {
            "no": 0.001,
            "yes": 0.005
        }
    }

    # TSS (D24): びまん性紅皮+消化器症状が特異的
    tss_pe = {
        "E01":  {"under_37.5": 0.01, "37.5_38.0": 0.03, "38.0_39.0": 0.1, "39.0_40.0": 0.36, "over_40.0": 0.5, "hypothermia_under_35": 0.0},
        "E02":  {"under_100": 0.08, "100_120": 0.27, "over_120": 0.65},
        "E03":  {"hypotension_under_90": 0.85, "normal_over_90": 0.15},
        "E04":  {"normal_under_20": 0.15, "tachypnea_20_30": 0.4, "severe_over_30": 0.45},
        "E05":  {"normal_over_96": 0.35, "mild_hypoxia_93_96": 0.3, "severe_hypoxia_under_93": 0.35},
        "E12":  {"normal": 0.03, "localized_erythema_warmth_swelling": 0.03, "petechiae_purpura": 0.05, "maculopapular_rash": 0.02, "vesicular_dermatomal": 0.01, "diffuse_erythroderma": 0.83, "skin_necrosis": 0.02, "purpura": 0.0, "vesicle_bulla": 0.01},  # TSS: びまん性紅皮83%
        "E16":  {"normal": 0.3, "confused": 0.4, "obtunded": 0.3},
        "E25":  {"absent": 0.45, "present": 0.55},  # TSS: 結膜充血55%
        "L01":  {"low_under_4000": 0.05, "normal_4000_10000": 0.1, "high_10000_20000": 0.35, "very_high_over_20000": 0.5},
        "L02":  {"normal_under_0.3": 0.02, "mild_0.3_3": 0.03, "moderate_3_10": 0.15, "high_over_10": 0.8},
        "L03":  {"not_done": 0.1, "low_under_0.25": 0.05, "gray_0.25_0.5": 0.1, "high_over_0.5": 0.75},
        "L09":  {"not_done_or_pending": 0.1, "negative": 0.4, "gram_positive": 0.45, "gram_negative": 0.05},  # TSS: 血培陽性は50%程度(毒素性)
        "L11":  {"normal": 0.1, "mild_elevated": 0.5, "very_high": 0.4},
        "L14":  {"normal": 0.2, "left_shift": 0.34, "atypical_lymphocytes": 0.02, "thrombocytopenia": 0.38, "eosinophilia": 0.03, "lymphocyte_predominant": 0.03},
        "L17":  {"normal": 0.35, "elevated": 0.45, "very_high": 0.2},
        "S06":  {"absent": 0.25, "present": 0.75},
        "S09":  {"absent": 0.25, "present": 0.75},
        "S13":  {"absent": 0.2, "present": 0.8},    # TSS: 嘔吐多い(TSS特異的)
        "S14":  {"absent": 0.3, "present": 0.7},    # TSS: 下痢多い(TSS特異的)
        "S18":  {"absent": 0.15, "present": 0.85},
        "T01":  {"under_3d": 0.7, "3d_to_1w": 0.25, "1w_to_3w": 0.04, "over_3w": 0.01},
        "T02":  {"sudden": 0.15, "acute": 0.83, "subacute": 0.01, "chronic": 0.01},
        "M02":  {"stable": 0.05, "compensated": 0.1, "shock": 0.85},
        "E37":  {"absent": 0.85, "present": 0.15},
        "L51":  {"not_done": 0.4, "normal": 0.2, "mildly_elevated": 0.25, "very_high": 0.15},
        "L52":  {"not_done": 0.2, "normal": 0.1, "mildly_elevated": 0.35, "very_high": 0.35},
        "L54":  {"hypoglycemia": 0.15, "normal": 0.35, "hyperglycemia": 0.35, "very_high_over_500": 0.15},
        "L55":  {"normal": 0.35, "mild_elevated": 0.35, "high_AKI": 0.3},
        "L64":  {"not_done": 0.1, "normal": 0.3, "pre_DIC": 0.3, "overt_DIC": 0.3},
        "S86":  {"watery": 0.85, "bloody": 0.15},
        "S87":  {"localized_pain_redness": 0.2, "rash_widespread": 0.8},  # TSS: びまん性
    }

    # iGAS (D364): 局所壊死+ショック、消化器症状少ない
    igas_pe = {
        "E01":  {"under_37.5": 0.01, "37.5_38.0": 0.05, "38.0_39.0": 0.2, "39.0_40.0": 0.45, "over_40.0": 0.29, "hypothermia_under_35": 0.0},
        "E02":  {"under_100": 0.12, "100_120": 0.33, "over_120": 0.55},
        "E03":  {"hypotension_under_90": 0.75, "normal_over_90": 0.25},
        "E04":  {"normal_under_20": 0.2, "tachypnea_20_30": 0.4, "severe_over_30": 0.4},
        "E05":  {"normal_over_96": 0.4, "mild_hypoxia_93_96": 0.3, "severe_hypoxia_under_93": 0.3},
        "E12":  {"normal": 0.05, "localized_erythema_warmth_swelling": 0.55, "petechiae_purpura": 0.05, "maculopapular_rash": 0.02, "vesicular_dermatomal": 0.01, "diffuse_erythroderma": 0.15, "skin_necrosis": 0.15, "purpura": 0.01, "vesicle_bulla": 0.01},  # iGAS: 局所炎症55%
        "E16":  {"normal": 0.3, "confused": 0.35, "obtunded": 0.35},
        "L01":  {"low_under_4000": 0.08, "normal_4000_10000": 0.12, "high_10000_20000": 0.35, "very_high_over_20000": 0.45},
        "L02":  {"normal_under_0.3": 0.02, "mild_0.3_3": 0.03, "moderate_3_10": 0.1, "high_over_10": 0.85},
        "L03":  {"not_done": 0.1, "low_under_0.25": 0.03, "gray_0.25_0.5": 0.07, "high_over_0.5": 0.8},
        "L09":  {"not_done_or_pending": 0.1, "negative": 0.15, "gram_positive": 0.7, "gram_negative": 0.05},  # iGAS: 血培GAS陽性70%
        "L11":  {"normal": 0.1, "mild_elevated": 0.45, "very_high": 0.45},
        "L14":  {"normal": 0.15, "left_shift": 0.4, "atypical_lymphocytes": 0.02, "thrombocytopenia": 0.35, "eosinophilia": 0.03, "lymphocyte_predominant": 0.05},
        "L17":  {"normal": 0.2, "elevated": 0.35, "very_high": 0.45},  # iGAS: CK著増(横紋筋融解)
        "S06":  {"absent": 0.15, "present": 0.85},  # iGAS: 局所筋痛激烈
        "S09":  {"absent": 0.2, "present": 0.8},
        "S18":  {"absent": 0.1, "present": 0.9},  # iGAS: 局所皮膚症状
        "T01":  {"under_3d": 0.75, "3d_to_1w": 0.2, "1w_to_3w": 0.04, "over_3w": 0.01},
        "T02":  {"sudden": 0.2, "acute": 0.78, "subacute": 0.01, "chronic": 0.01},
        "M02":  {"stable": 0.1, "compensated": 0.2, "shock": 0.7},
        "L52":  {"not_done": 0.2, "normal": 0.08, "mildly_elevated": 0.3, "very_high": 0.42},
        "L55":  {"normal": 0.3, "mild_elevated": 0.35, "high_AKI": 0.35},
        "L64":  {"not_done": 0.1, "normal": 0.2, "pre_DIC": 0.3, "overt_DIC": 0.4},  # iGAS: DIC多い
        "S87":  {"localized_pain_redness": 0.8, "rash_widespread": 0.2},  # iGAS: 局所
    }

    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D24' in pe:
            del pe['D24']
            if var_id in tss_pe:
                pe['D24'] = tss_pe[var_id]
            if var_id in igas_pe:
                pe['D364'] = igas_pe[var_id]

    return s3

# ============================================================
# TEST CASES
# ============================================================
def update_cases(ts):
    for c in ts['cases']:
        cid = c.get('id', '')
        exp = c.get('expected_id', '')

        # R91: iGAS → D364
        if cid == 'R91' and exp == 'D24':
            c['expected_id'] = 'D364'
            c['final_diagnosis'] = '劇症型溶血性レンサ球菌感染症(iGAS)'

        # D108 cases: all acute → stay D108
        # R88: Staph TSS → stay D24

    return ts

# ============================================================
# Validation
# ============================================================
def validate(s3):
    nop = s3['noisy_or_params']
    for new_id, name in [('D363', 'Chronic HBV'), ('D364', 'iGAS')]:
        count = sum(1 for v in nop if new_id in nop[v].get('parent_effects', {}))
        print(f"  {new_id} ({name}): {count} parent_effects entries")
        assert count > 0, f"{new_id} has 0 parent_effects — will be INVISIBLE!"

    for did, name in [('D108', 'Acute HBV'), ('D24', 'TSS')]:
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

    print("Done! D108→Acute HBV+D363(Chronic), D24→TSS+D364(iGAS)")
