#!/usr/bin/env python3
"""Add 9 test cases for D128/D129/D130."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

new_cases = [
    # D128 Upper Airway x3
    {"id": "R225", "source": "Cureus 2024", "pmcid": "PMC11408896",
     "vignette": "44M DM/喫煙者. 数日咽頭痛->急性呼吸困難+吸気性喘鳴+流涎+前傾姿勢. 前夜39.4度. HR 121, RR 32, SpO2 95%. WBC 21k. 側面頸部X線thumb sign+. 鼻咽頭鏡:喉頭蓋腫大",
     "final_diagnosis": "急性喉頭蓋炎", "expected_id": "D128", "in_scope": True,
     "evidence": {"S04": "at_rest", "S02": "present", "E02": "over_120", "E04": "severe_over_30",
                  "E05": "mild_hypoxia_93_96", "E01": "39.0_40.0", "L01": "very_high_over_20000",
                  "S09": "present", "T01": "under_3d", "T02": "gradual_days"},
     "risk_factors": {"R01": "40_64", "R02": "male", "R04": "yes"}, "result": "", "notes": "喉頭蓋炎. thumb sign. WBC 21k"},
    {"id": "R226", "source": "BMJ Case Rep 2021", "pmcid": "PMC7846295",
     "vignette": "48M 6年間反復歴. 炭酸飲料2h後に進行性呼吸困難. 蕁麻疹なし. ステロイド/抗ヒスタミン無効. 喉頭鏡:披裂喉頭蓋ヒダ浮腫. C1-INH 8%. 緊急気管切開",
     "final_diagnosis": "遺伝性血管浮腫(HAE Type 1)", "expected_id": "D128", "in_scope": True,
     "evidence": {"S04": "at_rest", "E04": "severe_over_30", "E01": "under_37.5",
                  "T01": "under_3d", "T02": "sudden_hours"},
     "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": "HAE. C1-INH 8%. ステロイド無効"},
    {"id": "R227", "source": "Case Rep Emerg Med 2016", "pmcid": "PMC4781940",
     "vignette": "48M 食品窒息->院外心停止. CPR 15分+除細動ROSC. HR 98, BP 98/65, SpO2 100%(FiO2 40%). 気管支鏡:左主気管支に肉片+骨片",
     "final_diagnosis": "異物気道閉塞(窒息性心停止)", "expected_id": "D128", "in_scope": True,
     "evidence": {"E16": "obtunded", "E03": "hypotension_under_90", "E01": "under_37.5",
                  "T01": "under_3d", "T02": "sudden_hours"},
     "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": "異物窒息->心停止->ROSC"},
    # D129 Hyperventilation x3
    {"id": "R228", "source": "Cureus 2021", "pmcid": "PMC7920229",
     "vignette": "33M COVID ICU勤務医. 30分の急性呼吸困難+胸痛+不安. HR 110, RR 28, SpO2 98%. ABG pH 7.52 pCO2 20. トロポニン陰性, CXR正常",
     "final_diagnosis": "過換気症候群", "expected_id": "D129", "in_scope": True,
     "evidence": {"S04": "at_rest", "S21": "constant", "E02": "100_120", "E04": "tachypnea_20_30",
                  "E05": "normal_over_96", "E01": "under_37.5", "L02": "normal_under_0.3",
                  "L04": "normal", "T01": "under_3d", "T02": "sudden_hours"},
     "risk_factors": {"R01": "18_39", "R02": "male"}, "result": "", "notes": "SpO2 98%正常+pH 7.52"},
    {"id": "R229", "source": "Neth J Med 2011", "pmcid": "PMC3047286",
     "vignette": "51M 既往なし. ストレス後の急性呼吸困難+めまい+嘔気+発汗. HR 75, RR 25, SpO2 98%. ABG pH 7.51 pCO2 25.5, 乳酸7.5. CT-PA正常",
     "final_diagnosis": "パニック発作(過換気)", "expected_id": "D129", "in_scope": True,
     "evidence": {"S04": "at_rest", "S05": "mild", "E04": "tachypnea_20_30",
                  "E05": "normal_over_96", "E01": "under_37.5",
                  "T01": "under_3d", "T02": "sudden_hours"},
     "risk_factors": {"R01": "40_64", "R02": "male"}, "result": "", "notes": "乳酸7.5は過換気による"},
    {"id": "R230", "source": "BMC Neurol 2023", "pmcid": "PMC10216786",
     "vignette": "22M 運動選手. 急性過換気+四肢しびれ+テタニー. ABG pH 7.57 pCO2 19.2. P 0.2mmol/L, CK 44913. MRI/NCS正常",
     "final_diagnosis": "パニック発作+過換気(低P+横紋筋融解)", "expected_id": "D129", "in_scope": True,
     "evidence": {"S04": "at_rest", "E04": "tachypnea_20_30",
                  "E05": "normal_over_96", "E01": "under_37.5",
                  "T01": "under_3d", "T02": "sudden_hours"},
     "risk_factors": {"R01": "18_39", "R02": "male"}, "result": "", "notes": "pH 7.57 pCO2 19.2 CK 44913"},
    # D130 ILD x3
    {"id": "R231", "source": "Cureus 2022", "pmcid": "PMC8712254",
     "vignette": "55F 乳癌EC化学療法中. 乾性咳嗽+労作時呼吸困難. T 36.4, HR 113, SpO2 90%. WBC 3600, CRP 3.77, LDH 348. HRCT:両側GGO上葉優位",
     "final_diagnosis": "薬剤性ILD(EC化学療法)", "expected_id": "D130", "in_scope": True,
     "evidence": {"S04": "on_exertion", "S01": "dry", "E02": "100_120", "E05": "mild_hypoxia_93_96",
                  "E01": "under_37.5", "L01": "low_under_4000", "L02": "moderate_3_10",
                  "L16": "elevated", "L04": "bilateral_infiltrate",
                  "T01": "1w_to_3w", "T02": "gradual_days"},
     "risk_factors": {"R01": "40_64", "R02": "female"}, "result": "", "notes": "薬剤性ILD. WBC 3600"},
    {"id": "R232", "source": "Cureus 2021", "pmcid": "PMC8555926",
     "vignette": "61F COVID後. 6ヶ月の進行性呼吸困難+脱力. RR 27, SpO2 90%. CRP 3.75, LDH 756, フェリチン1568. ANA 1:320. HRCT:末梢consolidation+嚢胞",
     "final_diagnosis": "LIP+MCTD", "expected_id": "D130", "in_scope": True,
     "evidence": {"S04": "on_exertion", "S01": "dry", "S07": "severe",
                  "E04": "tachypnea_20_30", "E05": "mild_hypoxia_93_96",
                  "E01": "under_37.5", "L02": "moderate_3_10", "L16": "elevated",
                  "L04": "bilateral_infiltrate", "L15": "very_high_over_1000",
                  "T01": "over_3w", "T02": "gradual_days"},
     "risk_factors": {"R01": "40_64", "R02": "female"}, "result": "", "notes": "LIP+MCTD. LDH 756"},
    {"id": "R233", "source": "Respir Med Case Rep 2021", "pmcid": "PMC8112992",
     "vignette": "74F 元喫煙. 20年来乾性咳嗽+労作時呼吸困難. Fine crackles. SpO2 91%(歩行時). WBC 7250, CRP 0.2, KL-6 661. HRCT:蜂巣肺+GGO右肺優位",
     "final_diagnosis": "IPF(UIP, 非対称性)", "expected_id": "D130", "in_scope": True,
     "evidence": {"S04": "on_exertion", "S01": "dry", "E07": "crackles",
                  "E05": "mild_hypoxia_93_96", "E01": "under_37.5",
                  "L01": "normal_4000_10000", "L02": "normal_under_0.3",
                  "L04": "bilateral_infiltrate",
                  "T01": "over_3w", "T02": "gradual_days"},
     "risk_factors": {"R01": "65_plus", "R02": "female", "R45": "former"}, "result": "", "notes": "20年IPF. KL-6 661"},
]

for c in new_cases:
    suite["cases"].append(c)

with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_cases)} cases. Total: {len(suite['cases'])}")
