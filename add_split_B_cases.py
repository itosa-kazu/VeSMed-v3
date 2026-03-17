#!/usr/bin/env python3
"""
B群分割: 6新疾患のPMC案例追加
D359 GCA: 6件, D360 CPPD: 5件, D361 PM: 5件
D362 アメーバ性肝膿瘍: 5件, D363 慢性HBV増悪: 5件, D364 iGAS: 5件
合計31件 (R762-R792)
"""
import json

def load_json(p):
    with open(p,'r',encoding='utf-8') as f: return json.load(f)
def save_json(p,d):
    with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)

new_cases = [
    # ========== D359 GCA (6件) ==========
    {
        "id": "R762", "source": "Medicine (Baltimore) 2021", "pmcid": "PMC7977053",
        "vignette": "75M. 3日の発熱38-38.5°C+下肢筋肉痛. 頭痛なし,視覚症状なし. CRP250-367, ESR70, WBC12.5-15.5K, PLT940K. 側頭動脈生検:GCA.",
        "final_diagnosis": "巨細胞動脈炎(GCA) — FUO", "expected_id": "D359", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S06": "present", "S07": "severe", "L01": "high_10000_20000", "L02": "high_over_10", "L28": "elevated", "T01": "under_3d", "T02": "acute"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R763", "source": "Cureus 2019", "pmcid": "PMC6563401",
        "vignette": "86M. 遷延する高熱40°C. 頭痛なし,顎跛行なし,視覚症状なし. ESR66, CRP55.9, フェリチン725, WBC正常. 側頭動脈生検:GCA.",
        "final_diagnosis": "巨細胞動脈炎(GCA) — 発熱のみ", "expected_id": "D359", "in_scope": True,
        "evidence": {"E01": "over_40.0", "S09": "present", "L01": "normal_4000_10000", "L02": "high_over_10", "L28": "elevated", "L15": "mild_elevated", "T01": "over_3w", "T02": "chronic"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R764", "source": "Hawaii Med J 2009", "pmcid": "PMC2659161",
        "vignette": "79F. 8ヶ月の倦怠感+微熱+7.7kg体重減少+咳嗽+股関節痛+こわばり. 頭痛なし. ESR>100, CRP18. PET-CT:大血管炎.",
        "final_diagnosis": "巨細胞動脈炎(大血管型GCA)", "expected_id": "D359", "in_scope": True,
        "evidence": {"E01": "37.5_38.0", "S01": "present", "S07": "severe", "S17": "present", "S06": "present", "S27": "present", "L02": "high_over_10", "L28": "very_high_over_100", "T01": "over_3w", "T02": "chronic"},
        "risk_factors": {"R01": "65_plus", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R765", "source": "BMJ Case Rep 2018", "pmcid": "PMC6319224",
        "vignette": "81M. 2-3週間の倦怠感+筋肉痛+咳嗽. 頭痛なし. WBC26.2K, CRP245, ESR22(正常!), ALP185. 側頭動脈生検:GCA.",
        "final_diagnosis": "巨細胞動脈炎(GCA) — ESR正常", "expected_id": "D359", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S01": "present", "S06": "present", "S07": "severe", "L01": "very_high_over_20000", "L02": "high_over_10", "L28": "normal", "L11": "mild_elevated", "T01": "1w_to_3w", "T02": "subacute"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R766", "source": "Semin Arthritis Rheum 2018", "pmcid": "PMC5806410",
        "vignette": "62M. 3週間の倦怠感+発熱38.9°C+両側鈍い頭痛+関節痛+発汗. ALP1017, AST306, ALT344, ESR97, CRP163. MRA:大動脈壁血管炎.",
        "final_diagnosis": "巨細胞動脈炎(GCA)+胆汁うっ滞性肝炎", "expected_id": "D359", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S05": "mild", "S60": "bilateral_pressing", "S07": "severe", "S08": "present", "L02": "high_over_10", "L28": "elevated", "L11": "very_high", "T01": "1w_to_3w", "T02": "subacute"},
        "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R767", "source": "Cureus 2025", "pmcid": "PMC12080050",
        "vignette": "78M. 3ヶ月のFUO+頭痛+倦怠感+9kg体重減少+Hb7.9(重度貧血). ESR113→145, CRP130, フェリチン883. 舌潰瘍. 両側生検陰性→臨床診断.",
        "final_diagnosis": "巨細胞動脈炎(GCA) — 舌潰瘍合併", "expected_id": "D359", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S05": "mild", "S07": "severe", "S17": "present", "S46": "present", "L28": "very_high_over_100", "L02": "high_over_10", "L15": "mild_elevated", "T01": "over_3w", "T02": "chronic"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },

    # ========== D360 CPPD (5件) ==========
    {
        "id": "R768", "source": "Cureus 2019", "pmcid": "PMC6684116",
        "vignette": "86M. 高熱40°C+頻脈120bpm, 敗血症疑い. 両膝痛+腫脹. 関節液:15000WBC, CPP結晶, 培養陰性. PCT0.97→1.99.",
        "final_diagnosis": "偽痛風(CPPD) — 敗血症模倣", "expected_id": "D360", "in_scope": True,
        "evidence": {"E01": "over_40.0", "S08": "present", "S23": "present", "E21": "present", "L30": "crystals", "E02": "100_120", "T01": "under_3d", "T02": "acute", "S90": "oligoarticular", "S91": "polyarticular", "E47": "polyarticular"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R769", "source": "Reumatismo 2019", "pmcid": "PMC6544428",
        "vignette": "70M. 突然の多関節炎(頚椎,肩,肘,手首,膝,足首)+発熱38°C. WBC26690, ESR120, CRP51.4mg/L. 尿酸正常. X線:軟骨石灰化. コルヒチン著効.",
        "final_diagnosis": "偽痛風(CPPD) — 多関節型", "expected_id": "D360", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S08": "present", "S23": "present", "E21": "present", "L23": "normal", "L02": "high_over_10", "L01": "very_high_over_20000", "L28": "very_high_over_100", "E02": "100_120", "T01": "under_3d", "T02": "sudden", "S90": "polyarticular_asymmetric", "S91": "polyarticular", "E47": "polyarticular"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R770", "source": "Case Rep Orthop 2018", "pmcid": "PMC5800752",
        "vignette": "71F. 左前腕+手腫脹2日, 疼痛8/10, 微熱37.8°C. WBC14200(好中球86%), ESR82, CRP25mg/L. 尿酸正常. 手首穿刺:CPP結晶.",
        "final_diagnosis": "偽痛風(CPPD) — 手首, 蜂窩織炎模倣", "expected_id": "D360", "in_scope": True,
        "evidence": {"E01": "37.5_38.0", "S08": "present", "S23": "present", "E21": "present", "L23": "normal", "L30": "crystals", "L02": "moderate_3_10", "L01": "high_10000_20000", "L28": "elevated", "E02": "under_100", "T01": "under_3d", "T02": "sudden", "S90": "monoarticular", "S91": "monoarticular", "E47": "monoarticular"},
        "risk_factors": {"R01": "65_plus", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R771", "source": "Cureus 2019", "pmcid": "PMC6935328",
        "vignette": "64M. 突然の重度右肩痛(頚部+背部放散)5日間, 大動脈解離疑い. 発熱38.1°C. WBC8500, CRP12mg/L, ESR9. 関節液:CPP結晶.",
        "final_diagnosis": "偽痛風(CPPD) — 肩, 大動脈解離模倣", "expected_id": "D360", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S08": "present", "S23": "present", "E21": "present", "L30": "crystals", "L02": "mild_0.3_3", "L01": "normal_4000_10000", "L28": "normal", "E02": "under_100", "T01": "3d_to_1w", "T02": "sudden", "S90": "monoarticular", "S91": "monoarticular", "E47": "monoarticular"},
        "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R772", "source": "Cureus 2022", "pmcid": "PMC9249022",
        "vignette": "76M. 3日の進行性頚部痛+頭痛+悪寒+発熱38.2°C, HR105. CRP119.6mg/L, ESR28. CT:歯突起石灰化(crowned dens). 入院中に両膝滑膜炎→穿刺:CPP結晶.",
        "final_diagnosis": "偽痛風(CPPD) — crowned dens+膝", "expected_id": "D360", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S08": "present", "S23": "present", "E21": "present", "L30": "crystals", "L02": "high_over_10", "L01": "high_10000_20000", "L28": "elevated", "E02": "100_120", "T01": "under_3d", "T02": "acute", "S90": "oligoarticular", "S91": "polyarticular", "E47": "polyarticular"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },

    # ========== D361 PM (5件) ==========
    {
        "id": "R773", "source": "Cureus 2023", "pmcid": "PMC10495079",
        "vignette": "61M. 3週間の進行性近位上肢筋力低下+嚥下困難. CK1521, LDH774, ESR65, ANA陰性. 皮膚所見なし. 生検:PM(anti-SRP+).",
        "final_diagnosis": "多発性筋炎(PM) — anti-SRP陽性", "expected_id": "D361", "in_scope": True,
        "evidence": {"E01": "under_37.5", "S48": "present", "S25": "present", "S07": "severe", "E12": "normal", "E20": "absent", "L17": "very_high", "L16": "elevated", "L18": "negative", "L28": "elevated", "T02": "subacute"},
        "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R774", "source": "J Community Hosp Intern Med Perspect 2016", "pmcid": "PMC4965691",
        "vignette": "64M. 2週間の進行性近位筋力低下+1週間の嚥下困難. CPK2705, ESR正常, CRP正常, ANA陰性. 皮膚所見なし.",
        "final_diagnosis": "多発性筋炎(PM)", "expected_id": "D361", "in_scope": True,
        "evidence": {"E01": "under_37.5", "S48": "present", "S25": "present", "S07": "severe", "E12": "normal", "E20": "absent", "L17": "very_high", "L18": "negative", "L28": "normal", "L02": "normal_under_0.3", "T02": "subacute"},
        "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R775", "source": "Diagnostics Basel 2023", "pmcid": "PMC10637286",
        "vignette": "41F. びまん性筋痛+上肢帯筋力低下+発熱37.8°C. CK5712, CRP147mg/L, WBC23800, ANA+, LDH上昇. 皮膚所見なし. 生検:PM(anti-OJ+).",
        "final_diagnosis": "多発性筋炎(PM) — anti-OJ陽性", "expected_id": "D361", "in_scope": True,
        "evidence": {"E01": "37.5_38.0", "S48": "present", "S06": "present", "S07": "severe", "E12": "normal", "E20": "absent", "L17": "very_high", "L16": "elevated", "L18": "positive", "L28": "elevated", "L02": "high_over_10", "T02": "acute"},
        "risk_factors": {"R01": "40_64", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R776", "source": "Case Rep Rheumatol 2022", "pmcid": "PMC9192263",
        "vignette": "53F. 1ヶ月の近位筋力低下(3/5)+嚥下困難+筋圧痛+手指圧痛. CK3261, LDH960, CRP27.1mg/L, ESR30, ANA+, Anti-Jo1 166U. CT:GGO+気管支拡張(ILD). 皮膚所見なし.",
        "final_diagnosis": "多発性筋炎(PM) — 抗ARS症候群+ILD", "expected_id": "D361", "in_scope": True,
        "evidence": {"E01": "under_37.5", "S48": "present", "S25": "present", "S06": "present", "S07": "severe", "S08": "present", "E12": "normal", "E20": "absent", "L17": "very_high", "L16": "elevated", "L18": "positive", "L28": "elevated", "L02": "mild_0.3_3", "L04": "bilateral_infiltrate", "T02": "subacute"},
        "risk_factors": {"R01": "40_64", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R777", "source": "Cureus 2022", "pmcid": "PMC9715395",
        "vignette": "58M. COVID後6ヶ月. 対称性筋力低下+筋痛+多関節痛+間欠的発熱. CK274(軽度上昇), CRP/ESR正常, ANA陰性. 皮膚所見なし.",
        "final_diagnosis": "多発性筋炎(PM) — COVID後", "expected_id": "D361", "in_scope": True,
        "evidence": {"E01": "37.5_38.0", "S48": "present", "S06": "present", "S07": "severe", "S08": "present", "E12": "normal", "E20": "absent", "L17": "elevated", "L18": "negative", "L28": "normal", "L02": "normal_under_0.3", "T01": "over_3w", "T02": "chronic"},
        "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": ""
    },

    # ========== D362 アメーバ性肝膿瘍 (5件) ==========
    {
        "id": "R778", "source": "BMC Infect Dis 2016", "pmcid": "PMC5146851",
        "vignette": "63M 農夫,スリランカ. 3週の食欲不振+体重減少→4日の発熱+悪寒+右下腹部痛. 肝腫大15cm. CT:右葉7x7cm+左葉9x8cm膿瘍. WBC14000, CRP192, ESR108. アメーバ血清陽性.",
        "final_diagnosis": "アメーバ性肝膿瘍(多発,腹膜穿破)", "expected_id": "D362", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S09": "present", "S07": "mild", "S46": "present", "S12": "present", "E34": "present", "L01": "high_10000_20000", "L02": "high_over_10", "L11": "mild_elevated", "L31": "abscess", "T01": "3d_to_1w", "S89": "RUQ"},
        "risk_factors": {"R01": "40_64", "R02": "male", "R06": "tropical_endemic"}, "result": "", "notes": ""
    },
    {
        "id": "R779", "source": "Cureus 2021", "pmcid": "PMC8489599",
        "vignette": "59F バングラデシュ渡航6週前. 2週の右上腹部痛+嘔吐+遷延する発熱. 頻脈,頻呼吸. 軽度肝腫大. CT:右葉6cm膿瘍. WBC18300, CRP127. アメーバ血清陽性(IFA 1:512).",
        "final_diagnosis": "アメーバ性肝膿瘍(右葉単発)", "expected_id": "D362", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S12": "present", "S89": "RUQ", "E34": "present", "L01": "high_10000_20000", "L02": "high_over_10", "L11": "mild_elevated", "L31": "abscess", "T01": "1w_to_3w"},
        "risk_factors": {"R01": "40_64", "R02": "female", "R06": "tropical_endemic"}, "result": "", "notes": ""
    },
    {
        "id": "R780", "source": "Iran J Parasitol 2014", "pmcid": "PMC4289874",
        "vignette": "35F 農夫,エジプト. 1ヶ月の持続熱(夜間増悪)+鈍い右上腹部痛(右肩放散)+食欲不振+嘔吐+呼吸困難. T39.4°C. CT:巨大右葉膿瘍+右膿胸. WBC16600, ESR102. 穿刺:anchovy-sauce膿+栄養体.",
        "final_diagnosis": "アメーバ性肝膿瘍(巨大,胸膜穿破)", "expected_id": "D362", "in_scope": True,
        "evidence": {"E01": "39.0_40.0", "S46": "present", "S12": "present", "S89": "RUQ", "L01": "high_10000_20000", "L11": "mild_elevated", "L31": "abscess", "T01": "over_3w"},
        "risk_factors": {"R01": "18_39", "R02": "female", "R06": "tropical_endemic"}, "result": "", "notes": ""
    },
    {
        "id": "R781", "source": "BMJ Case Rep 2013", "pmcid": "PMC3604252",
        "vignette": "74M エジプト渡航歴(3年以上前). 5週の食欲不振+体重減少+倦怠感+混乱+めまい. 無熱. CT:右葉11cm単発膿瘍. WBC22600, CRP140. 血培陰性. アメーバ血清陽性(IFA 1:512).",
        "final_diagnosis": "アメーバ性肝膿瘍(無熱,高齢)", "expected_id": "D362", "in_scope": True,
        "evidence": {"E01": "under_37.5", "S07": "severe", "S46": "present", "L01": "very_high_over_20000", "L02": "high_over_10", "L11": "mild_elevated", "L09": "negative", "L31": "abscess", "T01": "over_3w"},
        "risk_factors": {"R01": "65_plus", "R02": "male", "R06": "tropical_endemic"}, "result": "", "notes": ""
    },
    {
        "id": "R782", "source": "Int J Surg Case Rep 2021", "pmcid": "PMC8326431",
        "vignette": "23M インドネシア,未処理水飲用. 2週の呼吸困難+咳嗽+右胸痛+発熱. 黄疸+腹部膨満+下腿浮腫. 肝腫大. CT:右葉seg VII-VIII膿瘍(ガス産生)+胸膜穿破. WBC12190, AST221. アメーバ血清陽性.",
        "final_diagnosis": "アメーバ性肝膿瘍(ガス産生,胸膜穿破)", "expected_id": "D362", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "S12": "present", "S89": "RUQ", "E34": "present", "E18": "present", "L01": "high_10000_20000", "L11": "very_high", "L31": "abscess", "T01": "1w_to_3w"},
        "risk_factors": {"R01": "18_39", "R02": "male", "R06": "tropical_endemic"}, "result": "", "notes": ""
    },

    # ========== D363 慢性HBV増悪 (5件) ==========
    {
        "id": "R783", "source": "Clin Med 2016", "pmcid": "PMC4951972",
        "vignette": "72M DLBCL, R-CHOP完了2ヶ月後. 黄疸で入院. ALT988, Bil366μmol/L, INR>10. HBsAg陽転(元anti-HBc陽性のみ). HBV DNA 1.2×10^7. 肝生検:fibrosing cholestatic hepatitis.",
        "final_diagnosis": "HBV再活性化(R-CHOP後)", "expected_id": "D363", "in_scope": True,
        "evidence": {"E18": "present", "L11": "very_high", "L39": "HBV", "E01": "under_37.5", "T01": "1w_to_3w", "T02": "subacute"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R784", "source": "Clin Infect Dis 2009", "pmcid": "PMC2779698",
        "vignette": "46M HIV. ラミブジン除外に変更3ヶ月後. 1週間の発熱+嘔気嘔吐+倦怠感+腹部不快感+茶色尿. ALT2277, Bil 3.9mg/dL. HBsAg陽転, HBV DNA 1.1×10^9.",
        "final_diagnosis": "HBV再活性化(ラミブジン中止後)", "expected_id": "D363", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "E18": "present", "S07": "severe", "S13": "present", "S46": "present", "L11": "very_high", "L39": "HBV", "T01": "3d_to_1w", "T02": "acute"},
        "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": ""
    },
    {
        "id": "R785", "source": "Case Rep Gastroenterol 2012", "pmcid": "PMC3409890",
        "vignette": "78F DLBCL. Rituximab含む化療後40日. 5日間の黄疸+暗色尿. 発熱なし. AST2804, ALT2935, T-Bil 367μmol/L. HBsAg陽転(元anti-HBs陽性!). 肝性脳症→死亡.",
        "final_diagnosis": "HBV再活性化(anti-HBs陽性からの劇症化,致死)", "expected_id": "D363", "in_scope": True,
        "evidence": {"E18": "present", "L11": "very_high", "L39": "HBV", "E01": "under_37.5", "T01": "under_3d", "T02": "acute"},
        "risk_factors": {"R01": "65_plus", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R786", "source": "World J Gastroenterol 2013", "pmcid": "PMC3604245",
        "vignette": "50代F 乳癌化療後1ヶ月. 嘔気+倦怠感+脱力+黄疸. AST1414, ALT1308, HBV DNA 9.55×10^8. 意識障害+T-Bil 19.8mg/dL→肝腎症候群→死亡.",
        "final_diagnosis": "HBV再活性化(乳癌化療後,劇症肝炎)", "expected_id": "D363", "in_scope": True,
        "evidence": {"E18": "present", "S07": "severe", "S13": "present", "L11": "very_high", "L39": "HBV", "E01": "under_37.5", "T01": "1w_to_3w", "T02": "subacute"},
        "risk_factors": {"R01": "40_64", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R787", "source": "Cureus 2020", "pmcid": "PMC7296884",
        "vignette": "36M COVID-19感染中. 2日間の嘔吐後に意識障害. T35.5°C, GCS7→15. 黄疸. AST4933, ALT4758, T-Bil183.9, INR>10. HBsAg+, IgM-HBc+, HBV DNA 2490.",
        "final_diagnosis": "HBV再活性化(COVID-19誘発,肝性脳症)", "expected_id": "D363", "in_scope": True,
        "evidence": {"E01": "under_37.5", "E18": "present", "S13": "present", "E16": "obtunded", "L11": "very_high", "L39": "HBV", "T01": "under_3d", "T02": "acute"},
        "risk_factors": {"R01": "18_39", "R02": "male"}, "result": "", "notes": ""
    },

    # ========== D364 iGAS (5件) ==========
    {
        "id": "R788", "source": "Ann Intensive Care 2018", "pmcid": "PMC6141408",
        "vignette": "40F DM1. 背部痛+全身筋痛+発熱38.5°C. BP70/30. 左足首に小さな外傷(5日前). CRP320, PCT23, CK143000(!), eGFR15, Plt63k. 血培+関節液:S.pyogenes. STSS+敗血症性多関節炎.",
        "final_diagnosis": "劇症型GAS(iGAS)+STSS+敗血症性関節炎", "expected_id": "D364", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "E03": "hypotension_under_90", "S06": "present", "S07": "severe", "L02": "high_over_10", "L09": "gram_positive", "L17": "very_high", "M02": "shock", "T01": "under_3d", "T02": "acute"},
        "risk_factors": {"R01": "18_39", "R02": "female", "R14": "yes"}, "result": "", "notes": ""
    },
    {
        "id": "R789", "source": "Cureus 2024", "pmcid": "PMC11015911",
        "vignette": "41F 喘息. 1週間の倦怠感+呼吸困難+嘔吐+下痢. HR156, BP93/67, SpO2 92%, 無熱. 右5指壊死. WBC6.4→21.4K, CK2901→12772, Lac11.4. 胸水培養:S.pyogenes. 多臓器不全→人工呼吸+CRRT.",
        "final_diagnosis": "劇症型GAS(iGAS)+STSS+肺炎", "expected_id": "D364", "in_scope": True,
        "evidence": {"E01": "under_37.5", "E02": "over_120", "E12": "skin_necrosis", "S18": "present", "S13": "present", "L01": "high_10000_20000", "L17": "very_high", "M02": "shock", "T01": "3d_to_1w", "T02": "acute"},
        "risk_factors": {"R01": "18_39", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R790", "source": "J Med Case Reports 2007", "pmcid": "PMC2174498",
        "vignette": "33F 健康. 3日のインフルエンザ様症状後, 右上肢重度持続痛+嘔吐+下痢. T38.9, HR110. 右上肢非退色性紅斑→水疱→壊死進行. GCS14→7(8h後). WBC20.8→37.9K, CRP352, CK152→9367. 血培:α溶血性連鎖球菌.",
        "final_diagnosis": "劇症型GAS(iGAS)+STSS+壊死性筋膜炎", "expected_id": "D364", "in_scope": True,
        "evidence": {"E01": "38.0_39.0", "E02": "100_120", "E12": "localized_erythema_warmth_swelling", "S18": "present", "S87": "localized_pain_redness", "E16": "obtunded", "L01": "very_high_over_20000", "L02": "high_over_10", "L17": "very_high", "L09": "gram_positive", "M02": "compensated", "T01": "under_3d", "T02": "acute"},
        "risk_factors": {"R01": "18_39", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R791", "source": "Case Rep 2025", "pmcid": "PMC11745980",
        "vignette": "37F 産褥期G4P3. 2日間の発熱+嘔吐+下痢+緑色帯下+下腹部痛+乏尿+呼吸困難. HR130, SBP60, T36.5°C(低体温). WBC24.3K, CRP348, Lac12.3, Cr407. 血培:S.pyogenes. 四肢壊死→右下腿切断.",
        "final_diagnosis": "劇症型GAS(iGAS)+STSS(産褥期)", "expected_id": "D364", "in_scope": True,
        "evidence": {"E01": "under_37.5", "E02": "over_120", "E03": "hypotension_under_90", "S13": "present", "L01": "very_high_over_20000", "L02": "high_over_10", "L09": "gram_positive", "M02": "shock", "T01": "under_3d", "T02": "acute"},
        "risk_factors": {"R01": "18_39", "R02": "female"}, "result": "", "notes": ""
    },
    {
        "id": "R792", "source": "Cureus 2023", "pmcid": "PMC9839978",
        "vignette": "65M 高血圧+DM+PAD. 3日の左下肢痛+腫脹+発熱38.7→40°C. HR108, BP85/52. 左下肢炎症所見+意識障害. CRP582, Cr3.0. 血培:S.pyogenes. SOFA7→多臓器不全.",
        "final_diagnosis": "劇症型GAS(iGAS)+STSS(下肢軟部組織)", "expected_id": "D364", "in_scope": True,
        "evidence": {"E01": "39.0_40.0", "E02": "100_120", "E03": "hypotension_under_90", "E12": "localized_erythema_warmth_swelling", "S18": "present", "S87": "localized_pain_redness", "E16": "confused", "L02": "high_over_10", "L09": "gram_positive", "M02": "shock", "T01": "under_3d", "T02": "acute"},
        "risk_factors": {"R01": "65_plus", "R02": "male"}, "result": "", "notes": ""
    },
]

if __name__ == '__main__':
    ts = load_json('real_case_test_suite.json')

    # Check no duplicate IDs
    existing_ids = {c['id'] for c in ts['cases']}
    for c in new_cases:
        assert c['id'] not in existing_ids, f"Duplicate ID: {c['id']}"

    ts['cases'].extend(new_cases)
    save_json('real_case_test_suite.json', ts)
    print(f"Added {len(new_cases)} cases (R762-R792)")
    print(f"Total cases: {len(ts['cases'])}")

    # Summary by disease
    from collections import Counter
    cnt = Counter(c['expected_id'] for c in new_cases)
    for did, n in sorted(cnt.items()):
        print(f"  {did}: {n} cases")
