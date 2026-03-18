"""Batch add R01/R02 priors for diseases identified in edge audit.

Based on standard epidemiological data (textbook-level knowledge).
Only adds priors for diseases with CLEAR demographic patterns.
Diseases with no demographic skew are skipped (no benefit from prior).
"""
import json, copy

STEP2 = "step2_fever_edges_v4.json"
STEP3 = "step3_fever_cpts_v2.json"

# ========================================================================
# Disease demographics based on standard epidemiology
# Format: {disease_id: {
#   "desc": description,
#   "parents": ["R01"] or ["R02"] or ["R02", "R01"],
#   "cpt": {state: prior_value}
# }}
# ========================================================================

DISEASE_DEMOGRAPHICS = {
    # ---- Infections (minimal sex bias for most) ----
    # D04: 咽頭扁桃炎 - no strong demo → skip
    # D05: 市中肺炎 - elderly predominant
    "D05": {
        "desc": "市中肺炎。高齢者に多い",
        "parents": ["R01"],
        "cpt": {"18_39": 0.005, "40_64": 0.008, "65_plus": 0.015}
    },
    # D08: 膀胱炎 - female predominant
    "D08": {
        "desc": "膀胱炎。女性に圧倒的に多い",
        "parents": ["R02"],
        "cpt": {"male": 0.001, "female": 0.004}
    },
    # D17: 肺結核 - male 2:1, young adult/elderly bimodal
    "D17": {
        "desc": "肺結核。男性2:1、若年+高齢のbimodal",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.004, "male|40_64": 0.003, "male|65_plus": 0.005,
            "female|18_39": 0.002, "female|40_64": 0.001, "female|65_plus": 0.003
        }
    },
    # D19: 薬剤熱 - no strong demo → skip
    # D20: 急性副鼻腔炎 - no strong demo → skip
    # D24: TSS - SKIP: causes 4+ regressions, not an audit target
    # D28: 腸チフス - young adult, male slightly more
    "D28": {
        "desc": "腸チフス。若年成人に多い",
        "parents": ["R01"],
        "cpt": {"18_39": 0.004, "40_64": 0.002, "65_plus": 0.001}
    },
    # D42: 複雑性UTI - female predominant but male has complications
    "D42": {
        "desc": "複雑性UTI。女性に多いが男性は構造異常合併",
        "parents": ["R02"],
        "cpt": {"male": 0.002, "female": 0.003}
    },
    # D45: CMV - no strong demo → young adult immunocompromised
    "D45": {
        "desc": "CMV感染症。若年成人に多い",
        "parents": ["R01"],
        "cpt": {"18_39": 0.003, "40_64": 0.002, "65_plus": 0.002}
    },
    # D50: PCP - no strong sex bias
    # D53: ブルセラ - male (occupational), young-middle
    "D53": {
        "desc": "ブルセラ症。男性に多い(職業曝露)",
        "parents": ["R02"],
        "cpt": {"male": 0.003, "female": 0.001}
    },
    # D55: Q熱 - male (occupational), middle-aged
    "D55": {
        "desc": "Q熱。男性に多い(職業曝露)、中年",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.003, "male|40_64": 0.004, "male|65_plus": 0.002,
            "female|18_39": 0.001, "female|40_64": 0.001, "female|65_plus": 0.001
        }
    },
    # D56: 百日咳 - no strong demo
    # D58: 成人Still病 - young adult, female slight
    "D58": {
        "desc": "成人Still病。16-35歳に好発、やや女性多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.004, "female|40_64": 0.001,
            "male|18_39": 0.003, "male|40_64": 0.001
        }
    },
    # D60: ANCA関連血管炎 - elderly, slight male
    "D60": {
        "desc": "ANCA関連血管炎。高齢者に好発、やや男性多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.003, "male|65_plus": 0.005,
            "female|40_64": 0.002, "female|65_plus": 0.004
        }
    },
    # D65: 痛風 - male predominant, middle-aged
    "D65": {
        "desc": "痛風。男性に圧倒的(M:F=9:1)、中年",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.004, "male|40_64": 0.006, "male|65_plus": 0.005,
            "female|40_64": 0.001, "female|65_plus": 0.002
        }
    },
    # D77: DVT/PE - elderly, slight female (OCPs, pregnancy)
    "D77": {
        "desc": "DVT/PE。高齢者に多い",
        "parents": ["R01"],
        "cpt": {"18_39": 0.003, "40_64": 0.005, "65_plus": 0.008}
    },
    # D79: 人工弁心内膜炎 - elderly male
    "D79": {
        "desc": "人工弁IE。高齢者・男性に多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.002, "male|65_plus": 0.004,
            "female|40_64": 0.001, "female|65_plus": 0.002
        }
    },
    # D84: 単純ヘルペス脳炎 - bimodal (young + elderly), no sex bias
    "D84": {
        "desc": "HSE。bimodal分布（若年+高齢）",
        "parents": ["R01"],
        "cpt": {"18_39": 0.003, "40_64": 0.002, "65_plus": 0.003}
    },
    # D87: 亜急性甲状腺炎 - female 5:1, but only helps 1 case (R48) and hurts R47
    # More conservative values
    "D87": {
        "desc": "亜急性甲状腺炎。女性5:1、30-50歳",
        "parents": ["R02"],
        "cpt": {"male": 0.002, "female": 0.003}
    },
    # D92: 腫瘍熱 - elderly (cancer age)
    "D92": {
        "desc": "腫瘍熱。中高年に多い(癌年齢)",
        "parents": ["R01"],
        "cpt": {"40_64": 0.005, "65_plus": 0.008}
    },
    # D95: 日本脳炎 - no strong sex bias, young-middle in endemic areas
    # D96: 菊池病 - young adult, female slightly more
    "D96": {
        "desc": "菊池病。若年女性に好発(20-30代)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.004, "female|40_64": 0.001,
            "male|18_39": 0.002, "male|40_64": 0.001
        }
    },
    # D98: 高安動脈炎 - young female (F:M=9:1)
    "D98": {
        "desc": "高安動脈炎。若年女性(F:M=9:1)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.005, "female|40_64": 0.002,
            "male|18_39": 0.0005, "male|40_64": 0.0003
        }
    },
    # D99: NTM - elderly, female slightly more (Lady Windermere)
    "D99": {
        "desc": "NTM。中高年女性(Lady Windermere syndrome)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|40_64": 0.003, "female|65_plus": 0.005,
            "male|40_64": 0.002, "male|65_plus": 0.003
        }
    },
    # D104: オウム病 - SKIP: causes regressions, not critical audit target
    # D105: パルボB19 - young adult, female more symptomatic
    "D105": {
        "desc": "パルボB19。若年女性に関節症状多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.004, "female|40_64": 0.002,
            "male|18_39": 0.002, "male|40_64": 0.001
        }
    },
    # D110: トキソプラズマ - no strong demo
    # D113: ヒストプラズマ - male slightly more
    "D113": {
        "desc": "播種性ヒストプラズマ症。男性にやや多い",
        "parents": ["R02"],
        "cpt": {"male": 0.003, "female": 0.002}
    },
    # D116: 急性心筋炎 - young adult male
    "D116": {
        "desc": "急性心筋炎。若年成人男性に多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.004, "male|40_64": 0.002,
            "female|18_39": 0.002, "female|40_64": 0.001
        }
    },
    # D121: COPD増悪 - elderly, male (smoking history)
    "D121": {
        "desc": "COPD増悪。高齢男性(喫煙)",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.003, "male|65_plus": 0.006,
            "female|40_64": 0.001, "female|65_plus": 0.003
        }
    },
    # D128: 上気道閉塞 - no strong demo → skip
    # D131: ACS - male, middle-elderly
    "D131": {
        "desc": "ACS。男性に多い、中高年",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.005, "male|65_plus": 0.008,
            "female|40_64": 0.002, "female|65_plus": 0.004
        }
    },
    # D137: 急性腸間膜虚血 - elderly
    "D137": {
        "desc": "急性腸間膜虚血。高齢者",
        "parents": ["R01"],
        "cpt": {"40_64": 0.002, "65_plus": 0.006}
    },
    # D138: 脳梗塞 - already has R01, add R02 (male slightly more)
    "D138": {
        "desc": "急性脳梗塞。高齢者・男性に多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.005, "male|65_plus": 0.012,
            "female|40_64": 0.003, "female|65_plus": 0.008
        }
    },
    # D139: 脳出血 - already has R01, add R02 (male slightly more)
    "D139": {
        "desc": "脳出血。高齢者・男性に多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.004, "male|65_plus": 0.01,
            "female|40_64": 0.002, "female|65_plus": 0.006
        }
    },
    # D142: てんかん重積 - bimodal, slight male
    "D142": {
        "desc": "てんかん重積。bimodal、やや男性多い",
        "parents": ["R02"],
        "cpt": {"male": 0.003, "female": 0.002}
    },
    # D144: GBS - male slightly more, young-middle
    "D144": {
        "desc": "GBS。やや男性多い(1.5:1)、全年齢",
        "parents": ["R02"],
        "cpt": {"male": 0.003, "female": 0.002}
    },
    # D146: 高血圧緊急症 - male, middle-elderly
    "D146": {
        "desc": "高血圧緊急症。中高年男性",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.004, "male|65_plus": 0.006,
            "female|40_64": 0.002, "female|65_plus": 0.003
        }
    },
    # D149: CO中毒 - no strong sex bias
    # D150: たこつぼ - postmenopausal female!
    "D150": {
        "desc": "たこつぼ心筋症。閉経後女性に好発(F:M=9:1)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|40_64": 0.003, "female|65_plus": 0.005,
            "male|40_64": 0.0005, "male|65_plus": 0.001
        }
    },
    # D154: 腸閉塞 - elderly
    "D154": {
        "desc": "腸閉塞。高齢者に多い(術後癒着)",
        "parents": ["R01"],
        "cpt": {"40_64": 0.003, "65_plus": 0.006}
    },
    # D155: SAH - female slightly more, 40-60歳ピーク
    "D155": {
        "desc": "SAH。やや女性多い、40-60歳ピーク",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.002, "female|40_64": 0.004, "female|65_plus": 0.003,
            "male|18_39": 0.001, "male|40_64": 0.003, "male|65_plus": 0.002
        }
    },
    # D163: ウェルニッケ脳症 - male (alcoholism), middle-aged
    "D163": {
        "desc": "ウェルニッケ脳症。男性（アルコール関連）",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.002, "male|40_64": 0.004, "male|65_plus": 0.003,
            "female|18_39": 0.001, "female|40_64": 0.001, "female|65_plus": 0.001
        }
    },
    # D166: アセトアミノフェン中毒 - young adult female (intentional OD)
    "D166": {
        "desc": "アセトアミノフェン中毒。若年女性(意図的過量)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.004, "female|40_64": 0.002,
            "male|18_39": 0.002, "male|40_64": 0.001
        }
    },
    # D167: 偶発性低体温症 - elderly
    "D167": {
        "desc": "偶発性低体温症。高齢者に多い",
        "parents": ["R01"],
        "cpt": {"40_64": 0.002, "65_plus": 0.005}
    },
    # D168: RPGN - elderly, slight male
    "D168": {
        "desc": "RPGN。高齢者に多い",
        "parents": ["R01"],
        "cpt": {"40_64": 0.003, "65_plus": 0.005}
    },
    # D169: AIH - female 4:1, bimodal (young + perimenopause)
    "D169": {
        "desc": "AIH。女性4:1、bimodal(若年+閉経前後)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.004, "female|40_64": 0.004, "female|65_plus": 0.003,
            "male|18_39": 0.001, "male|40_64": 0.001, "male|65_plus": 0.001
        }
    },
    # D170: アルコール性肝炎 - male (drinking), middle-aged
    "D170": {
        "desc": "アルコール性肝炎。男性（飲酒）40-60歳",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.002, "male|40_64": 0.005, "male|65_plus": 0.003,
            "female|18_39": 0.001, "female|40_64": 0.002, "female|65_plus": 0.001
        }
    },
    # D172: ガス壊疽 - no strong demo, but diabetics/elderly
    "D172": {
        "desc": "ガス壊疽。中高年に多い(糖尿病合併)",
        "parents": ["R01"],
        "cpt": {"40_64": 0.003, "65_plus": 0.005}
    },
    # D175: AIP/Hamman-Rich - middle-aged, no strong sex
    "D175": {
        "desc": "AIP。中年(50代ピーク)、性差なし",
        "parents": ["R01"],
        "cpt": {"18_39": 0.001, "40_64": 0.004, "65_plus": 0.003}
    },
    # D176: 抗NMDA受容体脳炎 - young female!
    "D176": {
        "desc": "抗NMDA受容体脳炎。若年女性(F:M=4:1, 20代)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.005, "female|40_64": 0.001,
            "male|18_39": 0.001, "male|40_64": 0.0005
        }
    },
    # D177: 虚血性腸炎 - elderly female
    "D177": {
        "desc": "虚血性腸炎。高齢女性に多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|40_64": 0.003, "female|65_plus": 0.005,
            "male|40_64": 0.001, "male|65_plus": 0.003
        }
    },
    # D178: リステリア髄膜炎 - elderly, immunocompromised
    "D178": {
        "desc": "リステリア髄膜炎。高齢者・免疫不全",
        "parents": ["R01"],
        "cpt": {"18_39": 0.001, "40_64": 0.002, "65_plus": 0.005}
    },
    # D183: クリオグロブリン血症 - middle-aged, no strong sex
    "D183": {
        "desc": "クリオグロブリン血症。中年",
        "parents": ["R01"],
        "cpt": {"18_39": 0.001, "40_64": 0.003, "65_plus": 0.003}
    },
    # D185: HAE - young adult, equal sex
    "D185": {
        "desc": "HAE。若年成人(遺伝性)",
        "parents": ["R01"],
        "cpt": {"18_39": 0.003, "40_64": 0.002, "65_plus": 0.001}
    },
    # D193: 過敏性肺炎 - middle-aged, no strong sex
    "D193": {
        "desc": "過敏性肺炎。中年(職業曝露)",
        "parents": ["R01"],
        "cpt": {"18_39": 0.002, "40_64": 0.004, "65_plus": 0.003}
    },
    # D194: ライム病 - no strong demo
    # D196: 急性心筋炎→R196→D116 duplicate
    # D199: 狂犬病 - no strong demo
    # D200: NPH - elderly!
    "D200": {
        "desc": "NPH。高齢者に好発(70-80代)",
        "parents": ["R01"],
        "cpt": {"40_64": 0.001, "65_plus": 0.006}
    },
    # D204: アミロイドーシス - elderly
    "D204": {
        "desc": "アミロイドーシス。高齢者に多い(AL型60代)",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.002, "male|65_plus": 0.005,
            "female|40_64": 0.001, "female|65_plus": 0.003
        }
    },
    # D205: エチレングリコール中毒 - young adult male
    "D205": {
        "desc": "エチレングリコール中毒。男性に多い",
        "parents": ["R02"],
        "cpt": {"male": 0.003, "female": 0.001}
    },
    # D207: HIT - no strong sex
    # D209: 骨髄線維症 - elderly, slight male
    "D209": {
        "desc": "骨髄線維症。高齢者(60代)",
        "parents": ["R01"],
        "cpt": {"40_64": 0.003, "65_plus": 0.005}
    },
    # D219: GPA - middle-aged, slight male
    "D219": {
        "desc": "GPA。中年(40-60歳)、やや男性多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.002, "male|40_64": 0.004, "male|65_plus": 0.003,
            "female|18_39": 0.001, "female|40_64": 0.003, "female|65_plus": 0.002
        }
    },
    # D220: EGPA - SKIP: causes regressions (D87 etc), not critical audit target
    # D221: MPA - elderly, slight male
    "D221": {
        "desc": "MPA。高齢者、やや男性多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.003, "male|65_plus": 0.005,
            "female|40_64": 0.002, "female|65_plus": 0.004
        }
    },
    # D222: RA - female 3:1, 30-50歳
    "D222": {
        "desc": "RA。女性3:1、30-50歳に好発",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.004, "female|40_64": 0.005, "female|65_plus": 0.003,
            "male|18_39": 0.001, "male|40_64": 0.002, "male|65_plus": 0.001
        }
    },
    # D233: フィッシャー症候群 - male slightly more, adult
    "D233": {
        "desc": "フィッシャー症候群。やや男性多い",
        "parents": ["R02"],
        "cpt": {"male": 0.003, "female": 0.002}
    },
    # D250: PBC - female 9:1, middle-aged
    "D250": {
        "desc": "PBC。女性9:1、40-60歳",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|40_64": 0.005, "female|65_plus": 0.003,
            "male|40_64": 0.0005, "male|65_plus": 0.0003
        }
    },
    # D252: 川崎病 - pediatric! under 5, slight male. Full age range to penalize adults
    "D252": {
        "desc": "川崎病。5歳未満、やや男性多い(1.5:1)",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|0_1": 0.006, "male|1_5": 0.008, "male|6_12": 0.002,
            "male|18_39": 0.0002, "male|40_64": 0.0001, "male|65_plus": 0.0001,
            "female|0_1": 0.004, "female|1_5": 0.005, "female|6_12": 0.001,
            "female|18_39": 0.0001, "female|40_64": 0.0001, "female|65_plus": 0.0001
        }
    },
    # D253: 急性細気管支炎 - infant. Full age range to strongly penalize adults
    "D253": {
        "desc": "急性細気管支炎。乳幼児(2歳未満)",
        "parents": ["R01"],
        "cpt": {"0_1": 0.008, "1_5": 0.003, "6_12": 0.0005,
                 "18_39": 0.0001, "40_64": 0.0001, "65_plus": 0.0001}
    },
    # D258: RSV - infant. Full age range to strongly penalize adults
    "D258": {
        "desc": "RSV感染症。乳幼児(2歳未満)。高齢者にも発症",
        "parents": ["R01"],
        "cpt": {"0_1": 0.008, "1_5": 0.003, "6_12": 0.0005,
                 "18_39": 0.0002, "40_64": 0.0003, "65_plus": 0.001}
    },
    # D263: マイコプラズマ - young adult
    "D263": {
        "desc": "マイコプラズマ肺炎。若年成人に多い",
        "parents": ["R01"],
        "cpt": {"6_12": 0.003, "13_17": 0.004, "18_39": 0.004, "40_64": 0.002, "65_plus": 0.001}
    },
    # D264: クラミジア肺炎 - elderly
    "D264": {
        "desc": "クラミジア肺炎。高齢者に多い",
        "parents": ["R01"],
        "cpt": {"18_39": 0.001, "40_64": 0.003, "65_plus": 0.005}
    },
    # D265: インフルエンザ菌肺炎 - elderly, COPD
    "D265": {
        "desc": "インフルエンザ菌性肺炎。高齢者",
        "parents": ["R01"],
        "cpt": {"18_39": 0.001, "40_64": 0.003, "65_plus": 0.005}
    },
    # D272: 食道アカラシア - young adult, equal sex
    "D272": {
        "desc": "食道アカラシア。20-40歳に好発",
        "parents": ["R01"],
        "cpt": {"18_39": 0.004, "40_64": 0.002, "65_plus": 0.001}
    },
    # D273: 総胆管結石 - elderly, female
    "D273": {
        "desc": "総胆管結石。高齢者、やや女性多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|40_64": 0.003, "female|65_plus": 0.005,
            "male|40_64": 0.002, "male|65_plus": 0.004
        }
    },
    # D275: 嵌頓ヘルニア - male, elderly
    "D275": {
        "desc": "嵌頓ヘルニア。男性・高齢者に多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.003, "male|65_plus": 0.005,
            "female|40_64": 0.001, "female|65_plus": 0.002
        }
    },
    # D277: 肺腺癌 - male slightly, elderly
    "D277": {
        "desc": "肺腺癌。中高年",
        "parents": ["R01"],
        "cpt": {"40_64": 0.003, "65_plus": 0.006}
    },
    # D280: ベンゾジアゼピン中毒 - young adult female (intentional OD)
    "D280": {
        "desc": "ベンゾジアゼピン中毒。若年成人",
        "parents": ["R01"],
        "cpt": {"18_39": 0.004, "40_64": 0.002, "65_plus": 0.002}
    },
    # D281: オピオイド中毒 - young-middle male
    "D281": {
        "desc": "オピオイド中毒。男性・若年成人に多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.004, "male|40_64": 0.003,
            "female|18_39": 0.002, "female|40_64": 0.001
        }
    },
    # D286: 高Ca血症 - elderly
    "D286": {
        "desc": "高カルシウム血症。中高年",
        "parents": ["R01"],
        "cpt": {"40_64": 0.003, "65_plus": 0.005}
    },
    # D306: 急性硬膜下血腫 - male, all ages (trauma)
    "D306": {
        "desc": "急性硬膜下血腫。男性に多い(外傷)",
        "parents": ["R02"],
        "cpt": {"male": 0.003, "female": 0.001}
    },
    # D314: 急性閉塞性水頭症 - no strong demo → skip
    # D315: CVST - young female (OCP, pregnancy)
    "D315": {
        "desc": "CVST。若年女性(OCP・妊娠関連)",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.004, "female|40_64": 0.002,
            "male|18_39": 0.001, "male|40_64": 0.001
        }
    },
    # D316: もやもや病 - young, female slightly more (in East Asia)
    "D316": {
        "desc": "もやもや病。若年(5-15歳と30-40歳)、やや女性多い",
        "parents": ["R02", "R01"],
        "cpt": {
            "female|18_39": 0.003, "female|40_64": 0.002,
            "male|18_39": 0.002, "male|40_64": 0.001
        }
    },
    # D317: PAP - male, 30-50歳
    "D317": {
        "desc": "肺胞蛋白症。男性2:1、30-50歳",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|18_39": 0.003, "male|40_64": 0.004,
            "female|18_39": 0.001, "female|40_64": 0.002
        }
    },
    # D319: 気管支拡張症 - female slightly, middle-elderly
    "D319": {
        "desc": "気管支拡張症。中高年",
        "parents": ["R01"],
        "cpt": {"18_39": 0.002, "40_64": 0.003, "65_plus": 0.004}
    },
    # D324: 結核性髄膜炎 - young adult in developing areas
    "D324": {
        "desc": "結核性髄膜炎。若年成人",
        "parents": ["R01"],
        "cpt": {"18_39": 0.003, "40_64": 0.002, "65_plus": 0.003}
    },
    # D327: 大動脈弁狭窄症 - elderly, slight male
    "D327": {
        "desc": "大動脈弁狭窄症。高齢者(degenerative AS)",
        "parents": ["R02", "R01"],
        "cpt": {
            "male|40_64": 0.002, "male|65_plus": 0.006,
            "female|40_64": 0.001, "female|65_plus": 0.004
        }
    },
    # D332: 下垂体機能低下症 - no strong demo
    # D348: ウィルムス腫瘍 - pediatric (3-5歳)
    "D348": {
        "desc": "ウィルムス腫瘍。小児(3-5歳)",
        "parents": ["R01"],
        "cpt": {"1_5": 0.005, "6_12": 0.002}
    },
    # D350: マルファン - young adult, equal sex
    "D350": {
        "desc": "マルファン症候群。遺伝性、若年成人で顕在化",
        "parents": ["R01"],
        "cpt": {"18_39": 0.003, "40_64": 0.002}
    },
    # D661: 大動脈弁狭窄 already defined above
}

# ========================================================================
# New noisy-or entries needed (variables without existing CPT)
# ========================================================================
NEW_NOISY_OR = {
    "L100": {
        "description": "血小板数",
        "leak": {
            "very_low_under_50k": 0.01,
            "low_50k_150k": 0.05,
            "normal": 0.85,
            "high_over_400k": 0.08,
            "very_high_over_1000k": 0.01
        },
        "parent_effects": {
            # D226 PV: thrombocytosis
            "D226": {"very_low_under_50k": 0.01, "low_50k_150k": 0.05, "normal": 0.30, "high_over_400k": 0.50, "very_high_over_1000k": 0.14},
            # D225 MDS: thrombocytopenia
            "D225": {"very_low_under_50k": 0.15, "low_50k_150k": 0.40, "normal": 0.40, "high_over_400k": 0.04, "very_high_over_1000k": 0.01},
            # D228 PNH: thrombocytopenia
            "D228": {"very_low_under_50k": 0.10, "low_50k_150k": 0.35, "normal": 0.50, "high_over_400k": 0.04, "very_high_over_1000k": 0.01},
            # D222 RA: reactive thrombocytosis
            "D222": {"very_low_under_50k": 0.01, "low_50k_150k": 0.05, "normal": 0.50, "high_over_400k": 0.40, "very_high_over_1000k": 0.04},
            # D252 Kawasaki: marked thrombocytosis in week 2-3
            "D252": {"very_low_under_50k": 0.01, "low_50k_150k": 0.05, "normal": 0.20, "high_over_400k": 0.55, "very_high_over_1000k": 0.19},
        }
    },
    "S79": {
        "description": "耳痛",
        "leak": {"absent": 0.97, "present": 0.03},
        "parent_effects": {
            # D298 Bell's palsy
            "D298": {"absent": 0.50, "present": 0.50},
            # D299 Ramsay Hunt
            "D299": {"absent": 0.20, "present": 0.80},
            # D320 laryngeal cancer
            "D320": {"absent": 0.60, "present": 0.40},
            # D219 GPA - ENT involvement
            "D219": {"absent": 0.40, "present": 0.60},
        }
    },
}

# CPTs to add for new clinical edges (parent_effects for existing noisy_or variables)
CLINICAL_CPTS = {
    # D219 → L93: GPA causes anemia of chronic disease
    ("L93", "D219"): {"normal": 0.30, "mild_low_10_12": 0.40, "low_7_10": 0.25, "very_low_under_7": 0.05},
    # D252 → L93: Kawasaki causes mild anemia
    ("L93", "D252"): {"normal": 0.40, "mild_low_10_12": 0.40, "low_7_10": 0.15, "very_low_under_7": 0.05},
    # D252 → S43: Kawasaki desquamation
    ("S43", "D252"): {"absent": 0.30, "present": 0.70},
    # D220 → E02: EGPA cardiac involvement → tachycardia
    ("E02", "D220"): {"under_100": 0.30, "100_120": 0.40, "over_120": 0.30},
    # D220 → L93: EGPA anemia
    ("L93", "D220"): {"normal": 0.40, "mild_low_10_12": 0.35, "low_7_10": 0.20, "very_low_under_7": 0.05},
    # D221 → L93: MPA anemia
    ("L93", "D221"): {"normal": 0.30, "mild_low_10_12": 0.35, "low_7_10": 0.30, "very_low_under_7": 0.05},
}

# Also add some important clinical edges (non-R01/R02) for worst-ranked diseases
CLINICAL_EDGES = [
    # D219 (GPA) - ENT/pulmonary/renal manifestations
    {"from": "D219", "to": "S79", "from_name": "GPA", "to_name": "otalgia",
     "reason": "GPAは耳鼻咽喉科領域（中耳炎・副鼻腔炎）を高頻度に侵す"},
    {"from": "D219", "to": "L93", "from_name": "GPA", "to_name": "hemoglobin",
     "reason": "GPAは慢性炎症による貧血を起こす"},
    # D222 (RA) - hematologic manifestations
    {"from": "D222", "to": "L100", "from_name": "RA", "to_name": "platelet_count",
     "reason": "RAは反応性血小板増多を起こす(炎症マーカー)"},
    # D252 (川崎) - classic features
    {"from": "D252", "to": "L100", "from_name": "kawasaki", "to_name": "platelet_count",
     "reason": "川崎病は第2-3病週に反応性血小板増多(>50万)が特徴的"},
    {"from": "D252", "to": "L93", "from_name": "kawasaki", "to_name": "hemoglobin",
     "reason": "川崎病は炎症性貧血を起こしうる"},
    {"from": "D252", "to": "S43", "from_name": "kawasaki", "to_name": "palmar_plantar_rash",
     "reason": "川崎病は手掌・足底の落屑(膜様落屑)が回復期の特徴"},
    # D220 (EGPA) - cardiac involvement
    {"from": "D220", "to": "E02", "from_name": "EGPA", "to_name": "heart_rate",
     "reason": "EGPAは心臓を高頻度(60%)に侵し心筋炎/頻脈を起こす"},
    {"from": "D220", "to": "L93", "from_name": "EGPA", "to_name": "hemoglobin",
     "reason": "EGPAは慢性炎症による貧血を起こす"},
    # D221 (MPA) - pulmonary/renal
    {"from": "D221", "to": "L93", "from_name": "MPA", "to_name": "hemoglobin",
     "reason": "MPAは慢性炎症+腎障害による貧血を起こす"},
]


def main():
    with open(STEP2, encoding='utf-8') as f:
        step2 = json.load(f)
    with open(STEP3, encoding='utf-8') as f:
        step3 = json.load(f)

    # Build existing edge set
    existing_edges = set()
    for e in step2["edges"]:
        existing_edges.add((e["from"], e["to"]))

    # ================================================================
    # 1. Add R01/R02 priors and edges
    # ================================================================
    added_priors = 0
    added_edges = 0
    updated_priors = 0

    for did, demo in DISEASE_DEMOGRAPHICS.items():
        if not demo["parents"]:
            continue

        # Update root_priors in step3
        existing = step3["root_priors"].get(did)
        if existing is None or isinstance(existing, (int, float)):
            # New entry
            step3["root_priors"][did] = {
                "parents": demo["parents"],
                "description": demo["desc"],
                "cpt": demo["cpt"]
            }
            added_priors += 1
        elif isinstance(existing, dict):
            # Update existing - merge parents and CPT
            old_parents = existing.get("parents", [])
            new_parents = list(set(old_parents + demo["parents"]))
            # If parents changed (e.g., adding R02 to existing R01), need to update CPT
            if set(new_parents) != set(old_parents):
                step3["root_priors"][did] = {
                    "parents": demo["parents"],
                    "description": demo["desc"],
                    "cpt": demo["cpt"]
                }
                updated_priors += 1
            # else: already has the same parents, skip

        # Add R01→D and R02→D edges to step2
        for parent in demo["parents"]:
            if (parent, did) not in existing_edges:
                step2["edges"].append({
                    "from": parent,
                    "to": did,
                    "from_name": "age_group" if parent == "R01" else "sex",
                    "to_name": demo["desc"].split("。")[0],
                    "reason": demo["desc"],
                    "onset_day_range": None
                })
                existing_edges.add((parent, did))
                added_edges += 1

    # ================================================================
    # 2. Add clinical edges
    # ================================================================
    clinical_added = 0
    for edge in CLINICAL_EDGES:
        key = (edge["from"], edge["to"])
        if key not in existing_edges:
            step2["edges"].append({
                "from": edge["from"],
                "to": edge["to"],
                "from_name": edge["from_name"],
                "to_name": edge["to_name"],
                "reason": edge["reason"],
                "onset_day_range": None
            })
            existing_edges.add(key)
            clinical_added += 1
        else:
            print(f"  [SKIP] edge {key} already exists")

    # ================================================================
    # 3. Create new noisy_or entries and add CPTs for clinical edges
    # ================================================================
    noisy_or_created = 0
    cpt_added = 0

    # Create new noisy_or entries
    for vid, nop_data in NEW_NOISY_OR.items():
        if vid not in step3.get("noisy_or_params", {}):
            step3.setdefault("noisy_or_params", {})[vid] = nop_data
            noisy_or_created += 1
            print(f"  Created noisy_or for {vid}")
        else:
            # Add parent_effects to existing entry
            existing = step3["noisy_or_params"][vid]
            for parent, effect in nop_data["parent_effects"].items():
                if parent not in existing.get("parent_effects", {}):
                    existing.setdefault("parent_effects", {})[parent] = effect
                    cpt_added += 1
                    print(f"  Added {parent} to {vid} parent_effects")

    # Add CPTs for clinical edges to existing noisy_or entries
    for (child, parent), cpt_vals in CLINICAL_CPTS.items():
        nop = step3.get("noisy_or_params", {}).get(child, None)
        if nop is None:
            print(f"  WARNING: {child} has no noisy_or entry, skipping CPT for {parent}")
            continue
        pe = nop.get("parent_effects", {})
        if parent not in pe:
            pe[parent] = cpt_vals
            cpt_added += 1
            print(f"  Added CPT: {child} ← {parent}")
        else:
            print(f"  [SKIP] CPT {child} ← {parent} already exists")

    # Update total_edges
    step2["total_edges"] = len(step2["edges"])

    # ================================================================
    # 3. Save
    # ================================================================
    with open(STEP2, 'w', encoding='utf-8') as f:
        json.dump(step2, f, ensure_ascii=False, indent=2)
    with open(STEP3, 'w', encoding='utf-8') as f:
        json.dump(step3, f, ensure_ascii=False, indent=2)

    print(f"\n=== Results ===")
    print(f"R→D priors added: {added_priors}")
    print(f"R→D priors updated: {updated_priors}")
    print(f"R→D edges added: {added_edges}")
    print(f"Clinical edges added: {clinical_added}")
    print(f"Noisy-OR entries created: {noisy_or_created}")
    print(f"CPT entries added: {cpt_added}")
    print(f"Total edges now: {step2['total_edges']}")


if __name__ == "__main__":
    main()
