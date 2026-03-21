"""
D409 急性中耳炎(AOM) 案例追加
Sources: PMC7804088 (COVID-19 otitis media case series, Cases 1/3/5/8)
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC7804088 Case1 - 38M bilateral AOM with effusion
    {
        "id":"R1055","source":"PMC","pmcid":"PMC7804088",
        "vignette":"38歳男性。4日前からの難聴+耳閉感。慢性の非産生性咳嗽、軽度呼吸困難。耳鏡: 両側鼓膜膨隆+膿性貯留液。",
        "final_diagnosis":"急性中耳炎",
        "expected_id":"D409","in_scope":True,
        "evidence":{
            "S79":"present",
            "S124":"present",
            "S140":"conductive",
            "S01":"present",
            "E01":"under_37.5",
            "T01":"3d_to_1w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Bilateral AOM with purulent effusion. No fever. Cough (COVID context)."
    },
    # Case 2: PMC7804088 Case3 - 35F AOM with red TM
    {
        "id":"R1056","source":"PMC","pmcid":"PMC7804088",
        "vignette":"35歳女性。2週間前からの咳嗽+進行性呼吸困難。入院中に片側性耳痛+難聴を発症。耳鏡: 鼓膜著明発赤。",
        "final_diagnosis":"急性中耳炎",
        "expected_id":"D409","in_scope":True,
        "evidence":{
            "S79":"present",
            "S124":"present",
            "S140":"conductive",
            "S01":"present",
            "E01":"under_37.5",
            "T01":"1w_to_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"AOM developing during hospitalization for pneumonia. Red TM."
    },
    # Case 3: PMC7804088 Case5 - 22F AOM with bulging TM
    {
        "id":"R1057","source":"PMC","pmcid":"PMC7804088",
        "vignette":"22歳女性。7日前からの非産生性咳嗽。24時間前から左耳痛、耳閉感、難聴、ポップ音。耳鏡: 鼓膜可動性低下+膨隆+充血+膿性貯留液。聴力検査: 伝音性難聴+軽度感音性難聴。",
        "final_diagnosis":"急性中耳炎",
        "expected_id":"D409","in_scope":True,
        "evidence":{
            "S79":"present",
            "S124":"present",
            "S140":"conductive",
            "S01":"present",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"AOM with bulging TM and purulent effusion. Conductive + mild SNHL on audiometry."
    },
    # Case 4: PMC7804088 Case8 - 45F AOM with TM perforation
    {
        "id":"R1058","source":"PMC","pmcid":"PMC7804088",
        "vignette":"45歳女性。4日前からの重度耳痛、耳閉感、難聴。軽度咳嗽。耳鏡: 鼓膜中央穿孔+膿性耳漏。",
        "final_diagnosis":"急性中耳炎",
        "expected_id":"D409","in_scope":True,
        "evidence":{
            "S79":"present",
            "S124":"present",
            "S140":"conductive",
            "S01":"present",
            "E01":"under_37.5",
            "T01":"3d_to_1w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"AOM with spontaneous TM perforation and purulent otorrhea."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} AOM cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
