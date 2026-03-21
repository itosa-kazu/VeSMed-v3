"""
D413 インスリノーマ 案例追加
Sources: PMC5622836, PMC4953241, PMC9733155, PMC9835887, PMC8479877
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC5622836 - 50F consciousness/coma dominant, 5-year history
    {
        "id":"R1068","source":"PMC","pmcid":"PMC5622836",
        "vignette":"50歳女性。5年間の再発性低血糖発作。視覚障害+意識障害が進行し低血糖性昏睡に至る。空腹時に誘発。空腹時血糖26mg/dL。",
        "final_diagnosis":"インスリノーマ",
        "expected_id":"D413","in_scope":True,
        "evidence":{
            "L54":"hypoglycemia",
            "E16":"obtunded",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Classic insulinoma: 5-year recurrent hypoglycemia → coma. Fasting glucose 26 mg/dL. 1.5cm pancreatic tail tumor."
    },
    # Case 2: PMC4953241 - 34M seizure dominant
    {
        "id":"R1069","source":"PMC","pmcid":"PMC4953241",
        "vignette":"34歳男性(農業従事者)。低血糖による全般性強直間代発作。長時間の労作・空腹後に誘発される低血糖発作とけいれん。72時間絶食試験で血糖43mg/dL。膵尾部に15mm腫瘤(10年間安定)。",
        "final_diagnosis":"インスリノーマ",
        "expected_id":"D413","in_scope":True,
        "evidence":{
            "L54":"hypoglycemia",
            "S42":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Insulinoma with seizure-dominant presentation. 10-year stable tumor. Triggered by exertion/fasting."
    },
    # Case 3: PMC9733155 - 36F weight gain + Whipple triad
    {
        "id":"R1070","source":"PMC","pmcid":"PMC9733155",
        "vignette":"36歳女性。18kg(40ポンド)の体重増加。Whipple三徴(低血糖症状+血糖低下+ブドウ糖投与で改善)。空腹時血糖49mg/dL。72時間絶食で26時間後に血糖36mg/dLに低下。",
        "final_diagnosis":"インスリノーマ",
        "expected_id":"D413","in_scope":True,
        "evidence":{
            "L54":"hypoglycemia",
            "S120":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Insulinoma with prominent weight gain (40 lbs) due to defensive eating. Unusual duodenal location."
    },
    # Case 4: PMC9835887 - 60sF confusion + diplopia + recurrent
    {
        "id":"R1071","source":"PMC","pmcid":"PMC9835887",
        "vignette":"60代女性。再発性の混乱+複視+運動失調+不随意運動+転倒。エピソードの健忘。血糖1.9mmol/L(34mg/dL)。低血糖時にインスリン不適切高値(23.65mIU/L)。",
        "final_diagnosis":"インスリノーマ",
        "expected_id":"D413","in_scope":True,
        "evidence":{
            "L54":"hypoglycemia",
            "E16":"confused",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Insulinoma with neuroglycopenic dominant presentation. Confusion + diplopia + ataxia. CT negative, MRI found 16mm lesion."
    },
    # Case 5: PMC8479877 - 54M sweating + confusion + aggression
    {
        "id":"R1072","source":"PMC","pmcid":"PMC8479877",
        "vignette":"54歳男性。混乱+夢遊病(特に早朝03:00-08:00)+全身脱力+発汗+攻撃的行動。低血糖時に交感神経症状なし(低血糖非自覚)。血糖22-61mg/dL。HbA1c 5.3%。",
        "final_diagnosis":"インスリノーマ",
        "expected_id":"D413","in_scope":True,
        "evidence":{
            "L54":"hypoglycemia",
            "E16":"confused",
            "S45":"excessive",
            "S07":"severe",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Insulinoma in DM2 patient. Sweating + confusion + aggression. Glucose 22-61 mg/dL. Pancreatic tail 12mm tumor."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} insulinoma cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
