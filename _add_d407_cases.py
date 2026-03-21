"""
D407 メニエール病 案例追加
Sources: PMC6986504, PMC11745010, PMC4003730, PMC10366631
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC6986504 - 62F classic Meniere (later + BPPV)
    {
        "id":"R1048","source":"PMC","pmcid":"PMC6986504",
        "vignette":"62歳女性。数時間続く回転性めまい発作(「物が右から左に回る」)、右耳鳴(「海の音」)、右耳閉感。嘔気あり。水平回旋性眼振。聴力検査: 右低音型感音性難聴→進行してflat型中等度感音性難聴。温度刺激検査: 右25%低下。",
        "final_diagnosis":"メニエール病",
        "expected_id":"D407","in_scope":True,
        "evidence":{
            "S59":"present",
            "S92":"episodic_with_hearing",
            "S124":"present",
            "S140":"sensorineural",
            "S125":"present",
            "S79":"present",
            "S13":"present",
            "E62":"horizontal",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Classic Meniere: vertigo+SNHL+tinnitus+aural fullness. Later developed BPPV (comorbid)."
    },
    # Case 2: PMC11745010 - 37M autoimmune Meniere
    {
        "id":"R1049","source":"PMC","pmcid":"PMC11745010",
        "vignette":"37歳男性。反復性めまい発作、悪心、左耳鳴(「ブーン」)、左難聴。脱水や塩分摂取で増悪。神経学的所見正常。VNG: 眼振なし。温度刺激検査: 左57%機能低下。聴力検査: 左低音型感音性難聴(のち両側化)。蝸電図: 両側異常(SP/AP比67%)。",
        "final_diagnosis":"メニエール病",
        "expected_id":"D407","in_scope":True,
        "evidence":{
            "S59":"present",
            "S92":"episodic_with_hearing",
            "S124":"present",
            "S140":"sensorineural",
            "S125":"present",
            "S13":"present",
            "E62":"absent",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Autoimmune Meniere possibly triggered by neurocysticercosis. Anti-HSP70+. Bilateral progression."
    },
    # Case 3: PMC4003730 - 31M post-traumatic Meniere
    {
        "id":"R1050","source":"PMC","pmcid":"PMC4003730",
        "vignette":"31歳男性。交通事故後2ヶ月で発症した右耳鳴、右耳閉感、反復性めまい。左向き水平眼振。聴力検査: 右低音域25dB閾値上昇(感音性)。4ヶ月後: 持続性耳鳴、変動する右感音性難聴、重度反復性めまい。",
        "final_diagnosis":"メニエール病",
        "expected_id":"D407","in_scope":True,
        "evidence":{
            "S59":"present",
            "S92":"episodic_with_hearing",
            "S124":"present",
            "S140":"sensorineural",
            "S125":"present",
            "S79":"present",
            "E62":"horizontal",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Post-traumatic Meniere disease. Tinnitus+fullness+SNHL+vertigo after car accident."
    },
    # Case 4: PMC10366631 - 48M bilateral Meniere with Tumarkin drop attacks
    {
        "id":"R1051","source":"PMC","pmcid":"PMC10366631",
        "vignette":"48歳男性。10年来の両側メニエール病。間欠性回転性めまい発作、耳鳴、耳閉感。最近1年でTumarkin発作(突然の転倒、意識消失なし)を14回。聴力検査: 右高度感音性難聴(語音弁別0%)、左重度感音性難聴(語音弁別70%)。vHIT正常。",
        "final_diagnosis":"メニエール病",
        "expected_id":"D407","in_scope":True,
        "evidence":{
            "S59":"present",
            "S92":"episodic_with_hearing",
            "S124":"present",
            "S140":"sensorineural",
            "S125":"present",
            "S79":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Bilateral Meniere with Tumarkin drop attacks. 10-year history. Profound SNHL right."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} Meniere cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
