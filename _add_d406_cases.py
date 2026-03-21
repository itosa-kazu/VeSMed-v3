import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC7145698 - 45F ABPA as recurrent pneumonia
    {
        "id":"R1037","source":"PMC","pmcid":"PMC7145698",
        "vignette":"45歳女性。長年の喘息歴。繰り返す「肺炎」で抗菌薬治療歴。慢性産生性咳嗽(濃厚な茶色痰)、喘鳴、呼吸困難、微熱。総IgE>3000IU/mL、末梢好酸球2,500/μL、Aspergillus特異的IgE強陽性。CXR: 右上葉移動性浸潤影。CT: 中枢性気管支拡張症+粘液栓(finger-in-glove sign)。",
        "final_diagnosis":"アレルギー性気管支肺アスペルギルス症(ABPA)",
        "expected_id":"D406","in_scope":True,
        "evidence":{
            "S01":"present",
            "S84":"productive",
            "S04":"on_exertion",
            "E07":"wheezes",
            "L14":"eosinophilia",
            "L04":"lobar_infiltrate",
            "E01":"37.5_38.0",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"ABPA Stage III. Misdiagnosed as recurrent pneumonia. IgE >3000, eosinophilia."
    },
    # Case 5: PMC6700758 - 35M ABPA mimicking TB
    {
        "id":"R1038","source":"PMC","pmcid":"PMC6700758",
        "vignette":"35歳男性。喘息歴あり。上葉浸潤影で肺結核として治療されるも改善せず。慢性咳嗽(茶色痰)、微熱、呼吸困難、3ヶ月で5kg体重減少。総IgE 2800IU/mL、好酸球2,000/μL、Aspergillus皮膚試験陽性、喀痰AFB複数回陰性。CXR: 両側上葉陰影。CT: 中枢性気管支拡張症+粘液栓、空洞なし。",
        "final_diagnosis":"アレルギー性気管支肺アスペルギルス症(ABPA)",
        "expected_id":"D406","in_scope":True,
        "evidence":{
            "S01":"present",
            "S84":"productive",
            "S04":"on_exertion",
            "S17":"present",
            "L14":"eosinophilia",
            "L04":"bilateral_infiltrate",
            "E01":"37.5_38.0",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"ABPA misdiagnosed as TB. Weight loss, bilateral upper lobe infiltrates. AFB negative."
    },
    # Case 3: Based on PMC4921692 - 28F ABPA-CB steroid-dependent
    {
        "id":"R1039","source":"PMC","pmcid":"PMC4921692",
        "vignette":"28歳女性。小児期発症の喘息、ステロイド依存性。濃厚な粘液栓の喀出を伴う咳嗽、反復する発熱+呼吸困難エピソード、軽度喀血。総IgE 4200IU/mL、好酸球4,000/μL、Aspergillus fumigatus皮膚プリック試験陽性、特異的IgG沈降抗体陽性。CXR: 反復性上葉浸潤影。CT: 中枢性気管支拡張症+粘液栓(toothpaste/finger-in-glove)。",
        "final_diagnosis":"アレルギー性気管支肺アスペルギルス症(ABPA)",
        "expected_id":"D406","in_scope":True,
        "evidence":{
            "S01":"present",
            "S84":"productive",
            "S04":"at_rest",
            "E07":"wheezes",
            "S34":"present",
            "L14":"eosinophilia",
            "L04":"lobar_infiltrate",
            "E01":"38.0_39.0",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"ABPA-CB Stage IV. Steroid-dependent asthma. Hemoptysis. IgE 4200."
    },
    # Case 4: 19M newly diagnosed ABPA
    {
        "id":"R1040","source":"PMC","pmcid":"PMC3960790",
        "vignette":"19歳男性。12歳からの喘息。気管支拡張薬に反応しない喘鳴悪化、産生性咳嗽、微熱、軽度体重減少。総IgE 8500IU/mL、好酸球6,000/μL、Aspergillus特異的IgEおよびIgG強陽性。CT: 両側中枢性気管支拡張症(上葉優位)、粘液栓、右中葉に移動性浸潤影。",
        "final_diagnosis":"アレルギー性気管支肺アスペルギルス症(ABPA)",
        "expected_id":"D406","in_scope":True,
        "evidence":{
            "S01":"present",
            "S84":"productive",
            "E07":"wheezes",
            "S17":"present",
            "L14":"eosinophilia",
            "L04":"bilateral_infiltrate",
            "E01":"37.5_38.0",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Newly diagnosed ABPA. IgE 8500 (extremely elevated). Refractory asthma."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} ABPA cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
