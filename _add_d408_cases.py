"""
D408 突発性難聴(SSNHL) 案例追加
Sources: PMC4582458, PMC8524121, PMC11666207
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC4582458 - 57F SSNHL + positional vertigo (light cupula)
    {
        "id":"R1052","source":"PMC","pmcid":"PMC4582458",
        "vignette":"57歳女性。突然の左難聴+耳鳴。同日、頭位変換で増悪する回転性めまい。鼓膜正常。聴力検査: 左平均99dB(高度感音性難聴)。自発眼振なし。Head impulse test陰性。温度刺激検査正常。脳MRI正常。",
        "final_diagnosis":"突発性難聴",
        "expected_id":"D408","in_scope":True,
        "evidence":{
            "S124":"present",
            "S140":"sensorineural",
            "S125":"present",
            "S59":"present",
            "S79":"present",
            "E62":"absent",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"SSNHL with persistent positional vertigo (light cupula). Profound left SNHL 99dB."
    },
    # Case 2: PMC8524121 - 75F sequential bilateral SSNHL
    {
        "id":"R1053","source":"PMC","pmcid":"PMC8524121",
        "vignette":"75歳女性。高血圧/脂質異常症。7日前からのめまい(非回転性ふらつき)+悪心。その後、突然の左難聴を発症。聴力検査: 左高度感音性難聴。自発眼振なし。MRI正常。",
        "final_diagnosis":"突発性難聴",
        "expected_id":"D408","in_scope":True,
        "evidence":{
            "S124":"present",
            "S140":"sensorineural",
            "S59":"present",
            "S92":"non_rotatory_disequilibrium",
            "S13":"present",
            "E62":"absent",
            "E01":"under_37.5",
            "T01":"3d_to_1w",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Sequential bilateral SSNHL. Left first, then right 37 days later. HTN/HLD comorbid."
    },
    # Case 3: PMC11666207 - 49M classic SSNHL without vertigo
    {
        "id":"R1054","source":"PMC","pmcid":"PMC11666207",
        "vignette":"49歳男性。15日前の朝、起床時に左耳の聴力低下+セミのような耳鳴に気づく。ヘッドホン使用時に左の音量明らかに低下。めまいなし。聴力検査: 左90dB flat型高度感音性難聴。",
        "final_diagnosis":"突発性難聴",
        "expected_id":"D408","in_scope":True,
        "evidence":{
            "S124":"present",
            "S140":"sensorineural",
            "S125":"present",
            "S79":"present",
            "S59":"absent",
            "E01":"under_37.5",
            "T01":"1w_to_3w",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Classic SSNHL: sudden hearing loss + tinnitus, noticed upon waking. No vertigo. 90dB flat loss."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} SSNHL cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
