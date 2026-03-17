#!/usr/bin/env python3
"""
C群分割: D109(クリプト), D110(トキソ), D23(リケッチア)

D109 クリプトコッカス → D109(髄膜炎) + D365(肺クリプトコッカス)
  R175→D109(混合だが髄膜炎主体), R179→D109

D110 トキソプラズマ → D110(脳炎) + D366(リンパ節炎)
  R182→D110(脳炎), R183→D366(肺/播種型=免疫正常)

D23 リケッチア → D23(ツツガムシ病) + D367(紅斑熱群リケッチア症)
  R31→D23, R12→D23(murine typhus=typhus group), R59,R60,R61→D367
"""
import json, copy

def load_json(p):
    with open(p,'r',encoding='utf-8') as f: return json.load(f)
def save_json(p,d):
    with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

def update_step1(s1):
    v = s1['variables']

    # D109: rename to meningitis
    for d in v:
        if isinstance(d,dict) and d.get('id') == 'D109':
            d['name'] = 'cryptococcal_meningitis'
            d['name_ja'] = 'クリプトコッカス髄膜炎'
            d['icd10'] = 'B45.1'
            d['key_features'] = '免疫不全(HIV CD4<100,移植,ステロイド)の亜急性髄膜炎。頭痛+発熱+意識障害。CSF墨汁染色/クリプトコッカス抗原陽性。髄圧上昇。'
            break
    v.append({
        "id": "D365", "name": "pulmonary_cryptococcosis", "name_ja": "肺クリプトコッカス症",
        "category": "disease", "states": ["no","yes"], "icd10": "B45.0",
        "category_sub": "fungal", "severity": "moderate",
        "key_features": "免疫不全者の肺結節/浸潤影。咳嗽+発熱。免疫正常者では無症候のことも。血清クリプトコッカス抗原陽性。",
        "diagnostic_profile": {}
    })

    # D110: rename to encephalitis
    for d in v:
        if isinstance(d,dict) and d.get('id') == 'D110':
            d['name'] = 'toxoplasma_encephalitis'
            d['name_ja'] = 'トキソプラズマ脳炎'
            d['icd10'] = 'B58.2'
            d['key_features'] = 'HIV/AIDS(CD4<100)の脳炎。頭痛+局所神経症状+痙攣+意識障害。MRIでリング状増強病変。抗トキソ治療に反応。'
            break
    v.append({
        "id": "D366", "name": "toxoplasma_lymphadenitis", "name_ja": "トキソプラズマリンパ節炎",
        "category": "disease", "states": ["no","yes"], "icd10": "B58.1",
        "category_sub": "parasitic", "severity": "low",
        "key_features": "免疫正常者の頸部リンパ節腫脹+微熱。自然軽快。肝脾腫を伴うこともある。猫接触歴。IgM抗体陽性。",
        "diagnostic_profile": {}
    })

    # D23: rename to scrub typhus
    for d in v:
        if isinstance(d,dict) and d.get('id') == 'D23':
            d['name'] = 'scrub_typhus'
            d['name_ja'] = 'ツツガムシ病'
            d['icd10'] = 'A75.3'
            d['key_features'] = '秋(9-11月)の高熱+刺し口(eschar)+皮疹+リンパ節腫脹。ダニ媒介。Weil-Felix OX-K陽性。ドキシサイクリン著効。'
            break
    v.append({
        "id": "D367", "name": "spotted_fever_rickettsiosis", "name_ja": "紅斑熱群リケッチア症",
        "category": "disease", "states": ["no","yes"], "icd10": "A77",
        "category_sub": "rickettsial", "severity": "moderate",
        "key_features": "マダニ媒介の高熱+刺し口+紅斑+血小板減少。日本紅斑熱(R.japonica)/RMSF(R.rickettsii)/地中海紅斑熱。ドキシサイクリン著効。",
        "diagnostic_profile": {}
    })

    return s1

def update_step2(s2):
    edges = s2['edges']

    # ========== D109 → D109(meningitis) + D365(pulmonary) ==========
    edges = [e for e in edges if e.get('from') != 'D109' and e.get('to') != 'D109']

    # D109 meningitis: 頭痛/意識障害/髄膜刺激/CSF中心
    mening_edges = [
        {"from": "R01", "to": "D109", "reason": "クリプトコッカス髄膜炎。免疫不全者", "from_name": "age_group", "to_name": "D109"},
        {"from": "R02", "to": "D109", "reason": "クリプトコッカス髄膜炎。やや男性多い", "from_name": "sex", "to_name": "D109"},
        {"from": "D109", "to": "E01", "reason": "クリプト髄膜炎: 発熱(70-80%)", "from_name": "crypto_mening", "to_name": "temperature"},
        {"from": "D109", "to": "S05", "reason": "クリプト髄膜炎: 頭痛(主症状, 70-90%)", "from_name": "crypto_mening", "to_name": "headache"},
        {"from": "D109", "to": "S60", "reason": "クリプト髄膜炎: 頭痛パターン(progressive)", "from_name": "crypto_mening", "to_name": "S60"},
        {"from": "D109", "to": "E16", "reason": "クリプト髄膜炎: 意識障害(30-50%)", "from_name": "crypto_mening", "to_name": "consciousness"},
        {"from": "D109", "to": "E06", "reason": "クリプト髄膜炎: 髄膜刺激徴候(30-40%)", "from_name": "crypto_mening", "to_name": "meningeal_signs"},
        {"from": "D109", "to": "S13", "reason": "クリプト髄膜炎: 嘔吐(40-50%)", "from_name": "crypto_mening", "to_name": "nausea"},
        {"from": "D109", "to": "S07", "reason": "クリプト髄膜炎: 倦怠感", "from_name": "crypto_mening", "to_name": "fatigue"},
        {"from": "D109", "to": "S17", "reason": "クリプト髄膜炎: 体重減少(慢性経過)", "from_name": "crypto_mening", "to_name": "weight_loss"},
        {"from": "D109", "to": "S46", "reason": "クリプト髄膜炎: 食欲不振", "from_name": "crypto_mening", "to_name": "anorexia"},
        {"from": "D109", "to": "L45", "reason": "クリプト髄膜炎: CSF(真菌パターン,墨汁染色+)", "from_name": "crypto_mening", "to_name": "CSF"},
        {"from": "D109", "to": "L59", "reason": "クリプト髄膜炎: 髄圧上昇", "from_name": "crypto_mening", "to_name": "CSF_pressure"},
        {"from": "D109", "to": "L01", "reason": "クリプト髄膜炎: WBC(免疫不全で低下〜正常)", "from_name": "crypto_mening", "to_name": "WBC"},
        {"from": "D109", "to": "L02", "reason": "クリプト髄膜炎: CRP上昇", "from_name": "crypto_mening", "to_name": "CRP"},
        {"from": "D109", "to": "L28", "reason": "クリプト髄膜炎: ESR上昇", "from_name": "crypto_mening", "to_name": "ESR"},
        {"from": "D109", "to": "L16", "reason": "クリプト髄膜炎: LDH上昇", "from_name": "crypto_mening", "to_name": "LDH"},
        {"from": "D109", "to": "T01", "reason": "クリプト髄膜炎: 亜急性(1-4週)", "from_name": "crypto_mening", "to_name": "fever_duration"},
        {"from": "D109", "to": "T02", "reason": "クリプト髄膜炎: 亜急性〜慢性発症", "from_name": "crypto_mening", "to_name": "onset_speed"},
        {"from": "D109", "to": "E02", "reason": "クリプト髄膜炎: 頻脈", "from_name": "crypto_mening", "to_name": "heart_rate"},
    ]

    # D365 pulmonary: 咳嗽/胸部X線中心
    pulm_edges = [
        {"from": "R01", "to": "D365", "reason": "肺クリプト。免疫不全者", "from_name": "age_group", "to_name": "D365"},
        {"from": "R02", "to": "D365", "reason": "肺クリプト。やや男性多い", "from_name": "sex", "to_name": "D365"},
        {"from": "D365", "to": "E01", "reason": "肺クリプト: 発熱(50-60%)", "from_name": "pulm_crypto", "to_name": "temperature"},
        {"from": "D365", "to": "S01", "reason": "肺クリプト: 咳嗽(50-70%)", "from_name": "pulm_crypto", "to_name": "cough"},
        {"from": "D365", "to": "S84", "reason": "肺クリプト: 乾性咳嗽主体", "from_name": "pulm_crypto", "to_name": "S84"},
        {"from": "D365", "to": "S04", "reason": "肺クリプト: 呼吸困難(30-50%)", "from_name": "pulm_crypto", "to_name": "dyspnea"},
        {"from": "D365", "to": "L04", "reason": "肺クリプト: CXR(結節/浸潤/空洞)", "from_name": "pulm_crypto", "to_name": "chest_xray"},
        {"from": "D365", "to": "E04", "reason": "肺クリプト: 頻呼吸", "from_name": "pulm_crypto", "to_name": "resp_rate"},
        {"from": "D365", "to": "E05", "reason": "肺クリプト: 低酸素", "from_name": "pulm_crypto", "to_name": "SpO2"},
        {"from": "D365", "to": "S07", "reason": "肺クリプト: 倦怠感", "from_name": "pulm_crypto", "to_name": "fatigue"},
        {"from": "D365", "to": "S17", "reason": "肺クリプト: 体重減少", "from_name": "pulm_crypto", "to_name": "weight_loss"},
        {"from": "D365", "to": "L01", "reason": "肺クリプト: WBC", "from_name": "pulm_crypto", "to_name": "WBC"},
        {"from": "D365", "to": "L02", "reason": "肺クリプト: CRP", "from_name": "pulm_crypto", "to_name": "CRP"},
        {"from": "D365", "to": "L28", "reason": "肺クリプト: ESR", "from_name": "pulm_crypto", "to_name": "ESR"},
        {"from": "D365", "to": "T01", "reason": "肺クリプト: 亜急性〜慢性", "from_name": "pulm_crypto", "to_name": "fever_duration"},
        {"from": "D365", "to": "T02", "reason": "肺クリプト: 亜急性〜慢性発症", "from_name": "pulm_crypto", "to_name": "onset_speed"},
    ]

    # ========== D110 → D110(encephalitis) + D366(lymphadenitis) ==========
    edges = [e for e in edges if e.get('from') != 'D110' and e.get('to') != 'D110']

    # D110 encephalitis: 頭痛/痙攣/意識障害/MRI
    enceph_edges = [
        {"from": "R01", "to": "D110", "reason": "トキソ脳炎。HIV CD4<100", "from_name": "age_group", "to_name": "D110"},
        {"from": "R02", "to": "D110", "reason": "トキソ脳炎。やや男性多い", "from_name": "sex", "to_name": "D110"},
        {"from": "R25", "to": "D110", "reason": "HIV陽性がトキソ脳炎の最大リスク", "from_name": "HIV", "to_name": "D110"},
        {"from": "R05", "to": "D110", "reason": "免疫抑制", "from_name": "immunosuppression", "to_name": "D110"},
        {"from": "D110", "to": "E01", "reason": "トキソ脳炎: 発熱(50-70%)", "from_name": "toxo_enceph", "to_name": "temperature"},
        {"from": "D110", "to": "S05", "reason": "トキソ脳炎: 頭痛(50-60%)", "from_name": "toxo_enceph", "to_name": "headache"},
        {"from": "D110", "to": "E16", "reason": "トキソ脳炎: 意識障害(40-50%)", "from_name": "toxo_enceph", "to_name": "consciousness"},
        {"from": "D110", "to": "S42", "reason": "トキソ脳炎: 痙攣(20-30%)", "from_name": "toxo_enceph", "to_name": "seizure"},
        {"from": "D110", "to": "S52", "reason": "トキソ脳炎: 局所神経症状(60-70%)", "from_name": "toxo_enceph", "to_name": "focal_neuro"},
        {"from": "D110", "to": "S93", "reason": "トキソ脳炎: 局所症状の側性", "from_name": "toxo_enceph", "to_name": "S93"},
        {"from": "D110", "to": "E06", "reason": "トキソ脳炎: 髄膜刺激(30%)", "from_name": "toxo_enceph", "to_name": "meningeal"},
        {"from": "D110", "to": "L46", "reason": "トキソ脳炎: MRIリング状増強", "from_name": "toxo_enceph", "to_name": "MRI"},
        {"from": "D110", "to": "L45", "reason": "トキソ脳炎: CSF(ウイルスパターン)", "from_name": "toxo_enceph", "to_name": "CSF"},
        {"from": "D110", "to": "S07", "reason": "トキソ脳炎: 倦怠感", "from_name": "toxo_enceph", "to_name": "fatigue"},
        {"from": "D110", "to": "S13", "reason": "トキソ脳炎: 嘔吐", "from_name": "toxo_enceph", "to_name": "nausea"},
        {"from": "D110", "to": "L01", "reason": "トキソ脳炎: WBC", "from_name": "toxo_enceph", "to_name": "WBC"},
        {"from": "D110", "to": "L02", "reason": "トキソ脳炎: CRP", "from_name": "toxo_enceph", "to_name": "CRP"},
        {"from": "D110", "to": "L28", "reason": "トキソ脳炎: ESR", "from_name": "toxo_enceph", "to_name": "ESR"},
        {"from": "D110", "to": "T01", "reason": "トキソ脳炎: 亜急性(1-3週)", "from_name": "toxo_enceph", "to_name": "fever_duration"},
        {"from": "D110", "to": "T02", "reason": "トキソ脳炎: 亜急性発症", "from_name": "toxo_enceph", "to_name": "onset_speed"},
    ]

    # D366 lymphadenitis: リンパ節/肝脾腫/自然軽快
    lymph_edges = [
        {"from": "R01", "to": "D366", "reason": "トキソリンパ節炎。若年成人", "from_name": "age_group", "to_name": "D366"},
        {"from": "R02", "to": "D366", "reason": "トキソリンパ節炎。男女差少ない", "from_name": "sex", "to_name": "D366"},
        {"from": "D366", "to": "E01", "reason": "トキソリンパ節炎: 微熱(50-60%)", "from_name": "toxo_lymph", "to_name": "temperature"},
        {"from": "D366", "to": "E13", "reason": "トキソリンパ節炎: リンパ節腫脹(主症状)", "from_name": "toxo_lymph", "to_name": "lymphadenopathy"},
        {"from": "D366", "to": "E46", "reason": "トキソリンパ節炎: 頸部主体", "from_name": "toxo_lymph", "to_name": "E46"},
        {"from": "D366", "to": "E34", "reason": "トキソリンパ節炎: 肝脾腫(20-30%)", "from_name": "toxo_lymph", "to_name": "hepatomegaly"},
        {"from": "D366", "to": "S07", "reason": "トキソリンパ節炎: 倦怠感", "from_name": "toxo_lymph", "to_name": "fatigue"},
        {"from": "D366", "to": "S06", "reason": "トキソリンパ節炎: 筋肉痛", "from_name": "toxo_lymph", "to_name": "myalgia"},
        {"from": "D366", "to": "S01", "reason": "トキソリンパ節炎: 咳嗽(肺浸潤時)", "from_name": "toxo_lymph", "to_name": "cough"},
        {"from": "D366", "to": "S84", "reason": "トキソリンパ節炎: 乾性咳嗽", "from_name": "toxo_lymph", "to_name": "S84"},
        {"from": "D366", "to": "L04", "reason": "トキソリンパ節炎: CXR(びまん性浸潤, 20%)", "from_name": "toxo_lymph", "to_name": "chest_xray"},
        {"from": "D366", "to": "L01", "reason": "トキソリンパ節炎: WBC(正常〜リンパ球優位)", "from_name": "toxo_lymph", "to_name": "WBC"},
        {"from": "D366", "to": "L02", "reason": "トキソリンパ節炎: CRP軽度", "from_name": "toxo_lymph", "to_name": "CRP"},
        {"from": "D366", "to": "L11", "reason": "トキソリンパ節炎: 肝酵素(肝浸潤時)", "from_name": "toxo_lymph", "to_name": "liver_enzymes"},
        {"from": "D366", "to": "L14", "reason": "トキソリンパ節炎: リンパ球優位", "from_name": "toxo_lymph", "to_name": "CBC_diff"},
        {"from": "D366", "to": "L09", "reason": "トキソリンパ節炎: 血培陰性", "from_name": "toxo_lymph", "to_name": "blood_culture"},
        {"from": "D366", "to": "L28", "reason": "トキソリンパ節炎: ESR", "from_name": "toxo_lymph", "to_name": "ESR"},
        {"from": "D366", "to": "E18", "reason": "トキソリンパ節炎: 黄疸(稀)", "from_name": "toxo_lymph", "to_name": "jaundice"},
        {"from": "D366", "to": "E35", "reason": "トキソリンパ節炎: ぶどう膜炎(眼トキソ, 10-20%)", "from_name": "toxo_lymph", "to_name": "uveitis"},
        {"from": "D366", "to": "E48", "reason": "トキソリンパ節炎: 眼所見", "from_name": "toxo_lymph", "to_name": "E48"},
        {"from": "D366", "to": "T01", "reason": "トキソリンパ節炎: 亜急性〜慢性", "from_name": "toxo_lymph", "to_name": "fever_duration"},
        {"from": "D366", "to": "T02", "reason": "トキソリンパ節炎: 亜急性発症", "from_name": "toxo_lymph", "to_name": "onset_speed"},
    ]

    # ========== D23 → D23(ツツガムシ) + D367(紅斑熱群) ==========
    edges = [e for e in edges if e.get('from') != 'D23' and e.get('to') != 'D23']

    # Common rickettsial features for both
    common = ["E01","S05","S06","S07","S08","S09","S18","E12","E17","L01","L02","L11","L14","L28","T01","T02","E02","S43","E05","S12","S84","S86","S87","S89","S90","E14","E16","E18","E25","E34","L44","S01","S14"]

    # D23 scrub typhus
    scrub_edges = [
        {"from": "R01", "to": "D23", "reason": "ツツガムシ病。全年齢", "from_name": "age_group", "to_name": "D23"},
        {"from": "R02", "to": "D23", "reason": "ツツガムシ病。男女差少ない", "from_name": "sex", "to_name": "D23"},
        {"from": "R06", "to": "D23", "reason": "ツツガムシ病。国内山間部", "from_name": "travel", "to_name": "D23"},
        {"from": "R19", "to": "D23", "reason": "ツツガムシ病。秋(9-11月)に多い", "from_name": "season", "to_name": "D23"},
        {"from": "R30", "to": "D23", "reason": "ツツガムシ病。野外活動", "from_name": "animal", "to_name": "D23"},
    ]
    for var in ["E01","S05","S06","S07","S08","S09","S18","E12","E17","L01","L02","L11","L14","L28","T01","T02","E02","S43","E05","S12","S84","S86","S87","S89","S90","E14","E16","E18","E25","E34","L44","S01","S14"]:
        scrub_edges.append({"from": "D23", "to": var, "reason": f"ツツガムシ病: {var}"})

    # D367 spotted fever
    sf_edges = [
        {"from": "R01", "to": "D367", "reason": "紅斑熱群。全年齢", "from_name": "age_group", "to_name": "D367"},
        {"from": "R02", "to": "D367", "reason": "紅斑熱群。やや男性多い", "from_name": "sex", "to_name": "D367"},
        {"from": "R06", "to": "D367", "reason": "紅斑熱群。国内/渡航", "from_name": "travel", "to_name": "D367"},
        {"from": "R19", "to": "D367", "reason": "紅斑熱群。春〜秋(4-10月)", "from_name": "season", "to_name": "D367"},
        {"from": "R30", "to": "D367", "reason": "紅斑熱群。野外活動/マダニ", "from_name": "animal", "to_name": "D367"},
    ]
    for var in ["E01","S05","S06","S07","S08","S09","S18","E12","E17","L01","L02","L11","L14","L28","T01","T02","E02","S43","E05","S12","S84","S86","S87","S89","S90","E14","E16","E18","E25","E34","L44","S01","S14"]:
        sf_edges.append({"from": "D367", "to": var, "reason": f"紅斑熱群: {var}"})

    edges.extend(mening_edges + pulm_edges + enceph_edges + lymph_edges + scrub_edges + sf_edges)
    s2['edges'] = edges
    s2['total_edges'] = len(edges)
    return s2

def update_step3(s3):
    rp = s3['root_priors']
    fc = s3['full_cpts']
    nop = s3['noisy_or_params']

    # ========== D109 → D109(meningitis) + D365(pulmonary) ==========
    rp['D109'] = {"parents": ["R02","R01"], "description": "クリプト髄膜炎。免疫不全者",
        "cpt": {"male|18_39": 0.003, "male|40_64": 0.002, "male|65_plus": 0.001, "female|18_39": 0.002, "female|40_64": 0.001, "female|65_plus": 0.001}}
    rp['D365'] = {"parents": ["R02","R01"], "description": "肺クリプト。免疫不全者",
        "cpt": {"male|18_39": 0.001, "male|40_64": 0.001, "male|65_plus": 0.001, "female|18_39": 0.001, "female|40_64": 0.001, "female|65_plus": 0.001}}
    fc['D109'] = {"parents": ["R01"], "description": "クリプトコッカス髄膜炎",
        "cpt": {"0_1":0.0001,"1_5":0.0001,"6_12":0.0001,"13_17":0.0001,"18_39":0.003,"40_64":0.002,"65_plus":0.001}}
    fc['D365'] = {"parents": ["R01"], "description": "肺クリプトコッカス症",
        "cpt": {"0_1":0.0001,"1_5":0.0001,"6_12":0.0001,"13_17":0.0001,"18_39":0.001,"40_64":0.001,"65_plus":0.001}}

    # Meningitis PE (keep most of D109, remove pulmonary specific)
    mening_pe = {
        "E01": {"under_37.5": 0.15, "37.5_38.0": 0.25, "38.0_39.0": 0.35, "39.0_40.0": 0.2, "over_40.0": 0.04, "hypothermia_under_35": 0.01},
        "E02": {"under_100": 0.5, "100_120": 0.35, "over_120": 0.15},
        "E06": {"absent": 0.45, "present": 0.55},
        "E16": {"normal": 0.4, "confused": 0.35, "obtunded": 0.25},
        "L01": {"low_under_4000": 0.3, "normal_4000_10000": 0.5, "high_10000_20000": 0.15, "very_high_over_20000": 0.05},
        "L02": {"normal_under_0.3": 0.15, "mild_0.3_3": 0.35, "moderate_3_10": 0.35, "high_over_10": 0.15},
        "L16": {"normal": 0.3, "elevated": 0.7},
        "L28": {"normal": 0.3, "elevated": 0.5, "very_high_over_100": 0.2},
        "L45": {"not_done": 0.1, "normal": 0.02, "viral_pattern": 0.05, "bacterial_pattern": 0.08, "tb_fungal_pattern": 0.75, "HSV_PCR_positive": 0.0},
        "L59": {"not_done": 0.1, "normal": 0.1, "elevated": 0.35, "very_high": 0.45},
        "S05": {"absent": 0.05, "mild": 0.2, "severe": 0.75},
        "S07": {"absent": 0.2, "mild": 0.35, "severe": 0.45},
        "S13": {"absent": 0.4, "present": 0.6},
        "S17": {"absent": 0.5, "present": 0.5},
        "S46": {"absent": 0.2, "present": 0.8},
        "S60": {"bilateral_pressing": 0.1, "unilateral_pulsating": 0.03, "periorbital_stabbing": 0.02, "thunderclap": 0.05, "progressive_with_neuro": 0.77, "electric_triggered": 0.03},
        "T01": {"under_3d": 0.05, "3d_to_1w": 0.2, "1w_to_3w": 0.45, "over_3w": 0.3},
        "T02": {"sudden": 0.01, "acute": 0.05, "subacute": 0.55, "chronic": 0.39},
    }

    # Pulmonary PE
    pulm_pe = {
        "E01": {"under_37.5": 0.3, "37.5_38.0": 0.3, "38.0_39.0": 0.25, "39.0_40.0": 0.1, "over_40.0": 0.04, "hypothermia_under_35": 0.01},
        "E04": {"normal_under_20": 0.5, "tachypnea_20_30": 0.35, "severe_over_30": 0.15},
        "E05": {"normal_over_96": 0.5, "mild_hypoxia_93_96": 0.3, "severe_hypoxia_under_93": 0.2},
        "L01": {"low_under_4000": 0.2, "normal_4000_10000": 0.55, "high_10000_20000": 0.2, "very_high_over_20000": 0.05},
        "L02": {"normal_under_0.3": 0.2, "mild_0.3_3": 0.35, "moderate_3_10": 0.3, "high_over_10": 0.15},
        "L04": {"not_done": 0.05, "normal": 0.25, "lobar_infiltrate": 0.2, "bilateral_infiltrate": 0.3, "BHL": 0.05, "pleural_effusion": 0.1, "pneumothorax": 0.05},
        "L28": {"normal": 0.35, "elevated": 0.45, "very_high_over_100": 0.2},
        "S01": {"absent": 0.35, "present": 0.65},
        "S04": {"absent": 0.45, "on_exertion": 0.35, "at_rest": 0.2},
        "S07": {"absent": 0.3, "mild": 0.35, "severe": 0.35},
        "S17": {"absent": 0.55, "present": 0.45},
        "S84": {"dry": 0.65, "productive": 0.35},
        "T01": {"under_3d": 0.03, "3d_to_1w": 0.15, "1w_to_3w": 0.4, "over_3w": 0.42},
        "T02": {"sudden": 0.01, "acute": 0.03, "subacute": 0.46, "chronic": 0.5},
    }

    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D109' in pe:
            del pe['D109']
            if var_id in mening_pe: pe['D109'] = mening_pe[var_id]
            if var_id in pulm_pe: pe['D365'] = pulm_pe[var_id]

    # ========== D110 → D110(encephalitis) + D366(lymphadenitis) ==========
    rp.pop('D110', None)  # Remove old, use full_cpts
    rp['D110'] = {"parents": ["R02","R01"], "description": "トキソ脳炎。HIV CD4<100",
        "cpt": {"male|18_39": 0.003, "male|40_64": 0.002, "male|65_plus": 0.001, "female|18_39": 0.002, "female|40_64": 0.001, "female|65_plus": 0.001}}
    rp['D366'] = {"parents": ["R02","R01"], "description": "トキソリンパ節炎。免疫正常者",
        "cpt": {"male|18_39": 0.002, "male|40_64": 0.001, "male|65_plus": 0.001, "female|18_39": 0.002, "female|40_64": 0.001, "female|65_plus": 0.001}}
    fc['D110'] = {"parents": ["R25","R05"], "description": "トキソプラズマ脳炎。HIV+免疫抑制がリスク",
        "cpt": {"no|no":0.001, "no|yes":0.005, "yes|no":0.012, "yes|yes":0.025}}
    fc['D366'] = {"parents": ["R01"], "description": "トキソプラズマリンパ節炎",
        "cpt": {"0_1":0.0001,"1_5":0.0001,"6_12":0.0001,"13_17":0.0001,"18_39":0.002,"40_64":0.001,"65_plus":0.001}}

    enceph_pe = {
        "E01": {"under_37.5": 0.2, "37.5_38.0": 0.2, "38.0_39.0": 0.35, "39.0_40.0": 0.2, "over_40.0": 0.04, "hypothermia_under_35": 0.01},
        "E06": {"absent": 0.65, "present": 0.35},
        "E16": {"normal": 0.3, "confused": 0.4, "obtunded": 0.3},
        "L01": {"low_under_4000": 0.15, "normal_4000_10000": 0.6, "high_10000_20000": 0.2, "very_high_over_20000": 0.05},
        "L02": {"normal_under_0.3": 0.2, "mild_0.3_3": 0.4, "moderate_3_10": 0.3, "high_over_10": 0.1},
        "L28": {"normal": 0.35, "elevated": 0.5, "very_high_over_100": 0.15},
        "L45": {"not_done": 0.25, "normal": 0.15, "viral_pattern": 0.45, "bacterial_pattern": 0.05, "HSV_PCR_positive": 0.0, "tb_fungal_pattern": 0.1},
        "L46": {"not_done": 0.05, "normal": 0.1, "temporal_lobe_lesion": 0.05, "diffuse_abnormal": 0.15, "other": 0.65},
        "S05": {"absent": 0.2, "mild": 0.3, "severe": 0.5},
        "S07": {"absent": 0.25, "mild": 0.35, "severe": 0.4},
        "S13": {"absent": 0.65, "present": 0.35},
        "S42": {"absent": 0.7, "present": 0.3},
        "S52": {"absent": 0.2, "present": 0.8},
        "S93": {"unilateral_weakness": 0.87, "bilateral": 0.13},
        "T01": {"under_3d": 0.05, "3d_to_1w": 0.25, "1w_to_3w": 0.5, "over_3w": 0.2},
        "T02": {"sudden": 0.01, "acute": 0.05, "subacute": 0.6, "chronic": 0.34},
    }

    lymph_pe = {
        "E01": {"under_37.5": 0.3, "37.5_38.0": 0.35, "38.0_39.0": 0.2, "39.0_40.0": 0.1, "over_40.0": 0.04, "hypothermia_under_35": 0.01},
        "E13": {"absent": 0.05, "localized": 0.7, "generalized": 0.25},
        "E18": {"absent": 0.9, "present": 0.1},
        "E34": {"absent": 0.7, "present": 0.3},
        "E35": {"absent": 0.8, "present": 0.2},
        "E46": {"cervical": 0.5, "axillary": 0.1, "inguinal": 0.05, "supraclavicular": 0.05, "mediastinal": 0.05, "generalized": 0.25},
        "E48": {"conjunctivitis": 0.25, "uveitis": 0.75},
        "L01": {"low_under_4000": 0.1, "normal_4000_10000": 0.55, "high_10000_20000": 0.3, "very_high_over_20000": 0.05},
        "L02": {"normal_under_0.3": 0.2, "mild_0.3_3": 0.45, "moderate_3_10": 0.25, "high_over_10": 0.1},
        "L04": {"not_done": 0.05, "normal": 0.6, "lobar_infiltrate": 0.05, "bilateral_infiltrate": 0.2, "BHL": 0.03, "pleural_effusion": 0.05, "pneumothorax": 0.02},
        "L09": {"not_done_or_pending": 0.15, "negative": 0.8, "gram_positive": 0.03, "gram_negative": 0.02},
        "L11": {"normal": 0.5, "mild_elevated": 0.4, "very_high": 0.1},
        "L14": {"normal": 0.25, "left_shift": 0.05, "atypical_lymphocytes": 0.15, "thrombocytopenia": 0.05, "eosinophilia": 0.05, "lymphocyte_predominant": 0.45},
        "L28": {"normal": 0.35, "elevated": 0.5, "very_high_over_100": 0.15},
        "S01": {"absent": 0.6, "present": 0.4},
        "S06": {"absent": 0.6, "present": 0.4},
        "S07": {"absent": 0.25, "mild": 0.4, "severe": 0.35},
        "S84": {"dry": 0.7, "productive": 0.3},
        "T01": {"under_3d": 0.05, "3d_to_1w": 0.2, "1w_to_3w": 0.45, "over_3w": 0.3},
        "T02": {"sudden": 0.01, "acute": 0.04, "subacute": 0.5, "chronic": 0.45},
    }

    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D110' in pe:
            del pe['D110']
            if var_id in enceph_pe: pe['D110'] = enceph_pe[var_id]
            if var_id in lymph_pe: pe['D366'] = lymph_pe[var_id]

    # ========== D23 → D23(scrub typhus) + D367(spotted fever) ==========
    # Both share most CPT values (similar clinical presentation)
    # Key differences: seasonality, SIADH(紅斑熱多い), eschar pattern

    old_d23_pe = {}
    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D23' in pe:
            old_d23_pe[var_id] = pe['D23']

    # Remove D23 from all PE, then add both
    for var_id in list(nop.keys()):
        pe = nop[var_id].get('parent_effects', {})
        if 'D23' in pe:
            del pe['D23']
            # Copy to both (almost identical clinical presentation)
            pe['D23'] = old_d23_pe[var_id]
            pe['D367'] = copy.deepcopy(old_d23_pe[var_id])

    # Tweak differences
    # D367(紅斑熱): 結膜充血多い(RMSF), 低Na多い(RMSF SIADH)
    if 'E25' in nop and 'D367' in nop['E25'].get('parent_effects',{}):
        nop['E25']['parent_effects']['D367'] = {"absent": 0.5, "present": 0.5}  # 紅斑熱: 結膜充血50%
        nop['E25']['parent_effects']['D23'] = {"absent": 0.7, "present": 0.3}   # ツツガムシ: 30%
    if 'L44' in nop and 'D367' in nop['L44'].get('parent_effects',{}):
        nop['L44']['parent_effects']['D367'] = {"normal": 0.3, "hyponatremia": 0.65, "hyperkalemia": 0.03, "other": 0.02}  # 紅斑熱: SIADH多い
        nop['L44']['parent_effects']['D23'] = {"normal": 0.5, "hyponatremia": 0.45, "hyperkalemia": 0.03, "other": 0.02}

    # D23 full_cpts: split seasonality (scrub=autumn, spotted=spring-autumn)
    rp['D23'] = {"parents": ["R02","R01"], "description": "ツツガムシ病。秋に多い",
        "cpt": {"male|18_39": 0.002, "male|40_64": 0.002, "male|65_plus": 0.002, "female|18_39": 0.002, "female|40_64": 0.002, "female|65_plus": 0.002}}
    rp['D367'] = {"parents": ["R02","R01"], "description": "紅斑熱群。春〜秋",
        "cpt": {"male|18_39": 0.002, "male|40_64": 0.002, "male|65_plus": 0.002, "female|18_39": 0.001, "female|40_64": 0.001, "female|65_plus": 0.001}}

    # Keep D23 full_cpts but halve the probabilities for each
    if 'D23' in fc:
        old_fc = fc['D23']
        # Scrub typhus: autumn dominant
        fc['D23'] = copy.deepcopy(old_fc)
        fc['D23']['description'] = "ツツガムシ病。秋、野外活動"
        for k in fc['D23']['cpt']:
            fc['D23']['cpt'][k] *= 0.6  # 60% of original
        # Spotted fever: spring-autumn
        fc['D367'] = copy.deepcopy(old_fc)
        fc['D367']['description'] = "紅斑熱群。春〜秋、マダニ"
        for k in fc['D367']['cpt']:
            fc['D367']['cpt'][k] *= 0.4  # 40% of original

    return s3

def update_cases(ts):
    for c in ts['cases']:
        cid = c.get('id','')
        exp = c.get('expected_id','')

        # D110 R183: disseminated toxo in immunocompetent → D366 (lymphadenitis/systemic type)
        if cid == 'R183' and exp == 'D110':
            c['expected_id'] = 'D366'
            c['final_diagnosis'] = 'トキソプラズマ症(播種型/免疫正常)'

        # D23 R59(RMSF), R60(JSF), R61(MSF) → D367
        if cid in ('R59','R60','R61') and exp == 'D23':
            c['expected_id'] = 'D367'
            if cid == 'R59': c['final_diagnosis'] = 'ロッキー山紅斑熱(RMSF)'
            elif cid == 'R60': c['final_diagnosis'] = '日本紅斑熱'
            elif cid == 'R61': c['final_diagnosis'] = '地中海紅斑熱'

    return ts

def validate(s3):
    nop = s3['noisy_or_params']
    for new_id, name in [('D365','PulmCrypto'), ('D366','ToxoLymph'), ('D367','SpottedFever')]:
        count = sum(1 for v in nop if new_id in nop[v].get('parent_effects', {}))
        print(f"  {new_id} ({name}): {count} parent_effects")
        assert count > 0, f"{new_id} INVISIBLE!"
    for did, name in [('D109','CryptoMening'), ('D110','ToxoEnceph'), ('D23','ScrubTyphus')]:
        count = sum(1 for v in nop if did in nop[v].get('parent_effects', {}))
        print(f"  {did} ({name}): {count} parent_effects")

if __name__ == '__main__':
    print("Loading...")
    s1 = load_json('step1_fever_v2.7.json')
    s2 = load_json('step2_fever_edges_v4.json')
    s3 = load_json('step3_fever_cpts_v2.json')
    ts = load_json('real_case_test_suite.json')

    print("Updating step1..."); s1 = update_step1(s1)
    print("Updating step2..."); s2 = update_step2(s2)
    print("Updating step3..."); s3 = update_step3(s3)
    print("Updating cases..."); ts = update_cases(ts)
    print("Validating..."); validate(s3)

    print("Saving...")
    save_json('step1_fever_v2.7.json', s1)
    save_json('step2_fever_edges_v4.json', s2)
    save_json('step3_fever_cpts_v2.json', s3)
    save_json('real_case_test_suite.json', ts)
    print("Done! D109→Meningitis+D365(Pulm), D110→Enceph+D366(Lymph), D23→Scrub+D367(Spotted)")
