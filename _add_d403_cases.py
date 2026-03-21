import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 4: PMC10589413 - 58F unrepaired TOF, dyspnea NYHA III
    {
        "id":"R1027","source":"PMC","pmcid":"PMC10589413",
        "vignette":"58歳女性。4週間前からの呼吸困難悪化(NYHA III)、チアノーゼ。SpO2 80%。口唇・粘膜チアノーゼ、ばち指、5/6全収縮期雑音、肝腫大。CXR: 右大動脈弓。心エコー: RA拡大、RVH、VSD 21mm、大動脈騎乗、RVOT勾配75mmHg。CT: 肺動脈低形成。Hgb 16.1。",
        "final_diagnosis":"ファロー四徴症(TOF)",
        "expected_id":"D403","in_scope":True,
        "evidence":{
            "E42":"cyanosis",
            "E05":"severe_hypoxia_under_93",
            "E15":"new",
            "S04":"at_rest",
            "E95":"cyanosis",
            "E55":"clubbing",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"58F unrepaired TOF with right aortic arch. NYHA III. SpO2 80%."
    },
    # Case 2: PMC9641611 - 8M unrepaired TOF, incidental
    {
        "id":"R1028","source":"PMC","pmcid":"PMC9641611",
        "vignette":"8歳男児。口唇裂修復のため来院。中心性チアノーゼ、SpO2 80-85%、全収縮期雑音3/6、ばち指。CXR: ブーツ型心(coeur en sabot)。心エコーでTOF確認。Hgb 12.9。",
        "final_diagnosis":"ファロー四徴症(TOF)",
        "expected_id":"D403","in_scope":True,
        "evidence":{
            "E42":"cyanosis",
            "E05":"severe_hypoxia_under_93",
            "E15":"new",
            "E95":"cyanosis",
            "E55":"clubbing",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"6_12","R02":"male"},
        "notes":"8M unrepaired TOF. Incidental finding during cleft lip evaluation. Boot-shaped heart."
    },
    # Case 7: PMC8114129 - 30M unrepaired TOF, dyspnea
    {
        "id":"R1029","source":"PMC","pmcid":"PMC8114129",
        "vignette":"30歳男性。チアノーゼと労作時呼吸困難(NYHA III)。SpO2 86%。心エコー/CT: 大きいVSD 30mm、大動脈洞拡大56mm、上行大動脈43mm、中等度AR、PV狭窄(勾配98mmHg)。",
        "final_diagnosis":"ファロー四徴症(TOF)",
        "expected_id":"D403","in_scope":True,
        "evidence":{
            "E42":"cyanosis",
            "E05":"severe_hypoxia_under_93",
            "E15":"new",
            "S04":"on_exertion",
            "E95":"cyanosis",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"30M unrepaired TOF with aortic root disease. VSD 30mm, PV gradient 98mmHg."
    },
    # Case 8: PMC10976810 - 3M TOF with brain abscesses
    {
        "id":"R1030","source":"PMC","pmcid":"PMC10976810",
        "vignette":"3歳男児。痙攣、脱力感、倦怠感、泣き声でチアノーゼ悪化。SpO2 55%。ばち指(grade 3)、過動性心尖拍動、左胸骨縁上部に駆出性収縮期雑音。CT頭部: 多発性リング状増強病変(脳膿瘍)、最大42×41×36mm。Hgb 14.9-17.9。",
        "final_diagnosis":"ファロー四徴症(TOF)",
        "expected_id":"D403","in_scope":True,
        "evidence":{
            "E42":"cyanosis",
            "E05":"severe_hypoxia_under_93",
            "E15":"new",
            "E55":"clubbing",
            "S42":"present",
            "S07":"severe",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"1_5","R02":"male"},
        "notes":"3M TOF complicated by multiple brain abscesses. SpO2 55%. Hgb 17.9."
    },
    # Case 9: PMC10757113 - 24F pregnant with unrepaired TOF
    {
        "id":"R1031","source":"PMC","pmcid":"PMC10757113",
        "vignette":"24歳女性、妊娠31週。運動耐容能低下、呼吸困難、動悸。著明な中心性チアノーゼ、ばち指、全収縮期雑音+スリル、SpO2 78-80%。CXR: ブーツ型心、肺血管減少。心エコー: 4つの古典的特徴全て、RV壁14.6mm、大きいVSD。",
        "final_diagnosis":"ファロー四徴症(TOF)",
        "expected_id":"D403","in_scope":True,
        "evidence":{
            "E42":"cyanosis",
            "E05":"severe_hypoxia_under_93",
            "E15":"new",
            "S04":"on_exertion",
            "E95":"cyanosis",
            "E55":"clubbing",
            "E40":"RVH_strain",
            "R15":"yes",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"24F pregnant with unrepaired TOF. SpO2 78-80%. Boot-shaped heart on CXR."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} TOF cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
