"""
D417 結核性腹膜炎 (Tuberculous Peritonitis) 案例追加
Sources: PMC2267201, PMC11441176, PMC6807046, PMC3970332, PMC3700482
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC2267201 - 73F, fever 39.6C, ascites, weight loss 10kg/3mo, CRP 15.68, fatal
    {
        "id":"R1088","source":"PMC","pmcid":"PMC2267201",
        "vignette":"73歳女性。原発性胆汁性肝硬変の既往。3ヶ月間の腹痛+嘔吐+10kg体重減少。39.6℃の発熱。腹部膨満(大量腹水)。下肢浮腫。WBC 5200(好中球81%)。CRP 15.68mg/dL。Alb 1.7g/dL。腹水蛋白4.6g/dL(滲出性)。",
        "final_diagnosis":"結核性腹膜炎",
        "expected_id":"D417","in_scope":True,
        "evidence":{
            "E01":"39.0_40.0",
            "S12":"present",
            "S89":"diffuse",
            "E28":"present",
            "S17":"present",
            "S07":"severe",
            "S46":"present",
            "L02":"high_over_10",
            "L01":"normal_4000_10000",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"TB peritonitis in elderly PBC patient. Ascitic fluid culture M.tuberculosis+. CRP 15.68mg/dL. Died day 5 (MOF)."
    },
    # Case 2: PMC11441176 - 41M, no fever, weight loss 15kg/4mo, ascites, CRP 82mg/L
    {
        "id":"R1089","source":"PMC","pmcid":"PMC11441176",
        "vignette":"41歳男性。4ヶ月間の腹部膨満+腹痛+15kgの体重減少(62→47kg)。発熱なし。全腹部のびまん性圧痛。両下肢浮腫。リンパ節腫大/臓器腫大なし。WBC正常。CRP 82mg/L。ESR 70mm/h。Alb 2.6g/dL。",
        "final_diagnosis":"結核性腹膜炎",
        "expected_id":"D417","in_scope":True,
        "evidence":{
            "E01":"under_37.5",
            "S12":"present",
            "S89":"diffuse",
            "E28":"present",
            "S17":"present",
            "S46":"present",
            "L02":"moderate_3_10",
            "L01":"normal_4000_10000",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Afebrile TB peritonitis. Massive weight loss 15kg/4mo. Peritoneal pseudocyst 203x266x248mm. Biopsy: caseous granuloma. CRP 82mg/L=8.2mg/dL."
    },
    # Case 3: PMC6807046 - 21F, night sweats, diarrhea, weight loss 8kg/1mo, ascites, fever
    {
        "id":"R1090","source":"PMC","pmcid":"PMC6807046",
        "vignette":"21歳女性。10日間の腹部膨満+腹痛+下痢+悪心。1ヶ月で8kgの体重減少。発熱+盗汗あり。びまん性腹水。腹膜肥厚+omental cake(CT)。Hb 11.5g/dL。CA-125 563U/mL。",
        "final_diagnosis":"結核性腹膜炎",
        "expected_id":"D417","in_scope":True,
        "evidence":{
            "E01":"38.0_39.0",
            "S12":"present",
            "S89":"diffuse",
            "E28":"present",
            "S17":"present",
            "S16":"present",
            "S14":"present",
            "T01":"1w_to_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Young female with classic TB constitutional symptoms: fever+night sweats+weight loss+diarrhea. Omental biopsy: caseous granuloma. MTB DNA+."
    },
    # Case 4: PMC3970332 - 25F, high fever up to 40C, ascites, anorexia, fatal
    {
        "id":"R1091","source":"PMC","pmcid":"PMC3970332",
        "vignette":"25歳女性。2週間のびまん性腹痛。3週間以上の間欠的高熱(最高40.0℃)。食欲不振+めまい+発汗。腹部膨満+びまん性圧痛(特に下腹部)。大量腹水。Hb 7.9g/dL。Plt 112000。CRP 21.6。CA-125 669U/mL。腹水: リンパ球優位。",
        "final_diagnosis":"結核性腹膜炎",
        "expected_id":"D417","in_scope":True,
        "evidence":{
            "E01":"39.0_40.0",
            "S12":"present",
            "S89":"diffuse",
            "E28":"present",
            "S46":"present",
            "S07":"severe",
            "L02":"moderate_3_10",
            "T01":"1w_to_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Severe TB peritonitis mimicking peritoneal carcinomatosis. Fever up to 40C. Omental cake on CT. Tissue culture M.tuberculosis+. Died day 12 (ARDS/MOF)."
    },
    # Case 5: PMC3700482 - 46M, no fever, no pain, anorexia+weight loss, ascites, lymphadenopathy
    {
        "id":"R1092","source":"PMC","pmcid":"PMC3700482",
        "vignette":"46歳男性(モロッコ出身)。4-6ヶ月間の食欲不振+体重減少+消化不良+しゃっくり。発熱なし。腹痛なし。腹部膨満(腹水)。両側鼠径部+腋窩リンパ節腫脹(硬、無痛性)。Hb 10.6g/dL。CRP 3.4-4.3mg/dL。ESR 42mm/h。ツベルクリン反応8mm陽性。腹水蛋白65.3g/L(高蛋白)。SAAG 0.4。腹水WBCリンパ球優位(80%)。",
        "final_diagnosis":"結核性腹膜炎",
        "expected_id":"D417","in_scope":True,
        "evidence":{
            "E01":"under_37.5",
            "E28":"present",
            "S17":"present",
            "S46":"present",
            "E13":"present",
            "S07":"mild",
            "L02":"moderate_3_10",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Afebrile, painless TB peritonitis. Moroccan immigrant. Inguinal+axillary lymphadenopathy. Ascitic fluid: high protein, SAAG 0.4, 80% lymphocytes. Laparoscopic biopsy: caseous granuloma."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} TB peritonitis cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
