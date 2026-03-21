import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Classic: palpable breast mass + axillary LAD
    {
        "id":"R1041","source":"PMC","pmcid":"PMC6497072",
        "vignette":"52歳女性。2ヶ月前に右乳房に無痛性腫瘤を自覚。硬く不整形、可動性不良。右腋窩リンパ節腫脹(硬、2cm)。乳頭分泌なし。体重減少なし。",
        "final_diagnosis":"乳癌",
        "expected_id":"D405","in_scope":True,
        "evidence":{
            "S143":"present",
            "E13":"present",
            "E46":"axillary",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Classic breast cancer: painless mass + axillary LAD."
    },
    # Advanced: mass + bone metastasis + weight loss
    {
        "id":"R1042","source":"PMC","pmcid":"PMC7028263",
        "vignette":"63歳女性。左乳房腫瘤(6ヶ月前から)、最近の腰痛+体重減少(5kg/3ヶ月)。左腋窩リンパ節腫脹。ALP上昇。骨シンチ: 多発骨転移。倦怠感。",
        "final_diagnosis":"乳癌",
        "expected_id":"D405","in_scope":True,
        "evidence":{
            "S143":"present",
            "E13":"present",
            "E46":"axillary",
            "S17":"present",
            "L63":"bone",
            "L104":"moderate_elevated",
            "S07":"mild",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Advanced breast cancer with bone metastases. ALP elevated."
    },
    # Bloody nipple discharge
    {
        "id":"R1043","source":"PMC","pmcid":"PMC5400046",
        "vignette":"47歳女性。3週間前からの片側性血性乳頭分泌。触知可能な腫瘤は不明瞭。腋窩リンパ節触知せず。マンモグラフィ: 微小石灰化+不整形腫瘤影。",
        "final_diagnosis":"乳癌",
        "expected_id":"D405","in_scope":True,
        "evidence":{
            "S144":"present",
            "S148":"bloody",
            "E01":"under_37.5",
            "T01":"1w_to_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Breast cancer presenting with bloody nipple discharge. Microcalcifications on mammography."
    },
    # Male breast cancer (rare)
    {
        "id":"R1044","source":"PMC","pmcid":"PMC4404840",
        "vignette":"68歳男性。左乳房の無痛性腫瘤(数ヶ月前から増大)。硬く乳頭直下。左腋窩リンパ節腫脹。体重減少。",
        "final_diagnosis":"乳癌",
        "expected_id":"D405","in_scope":True,
        "evidence":{
            "S143":"present",
            "E13":"present",
            "E46":"axillary",
            "S17":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"Male breast cancer (<1% of all breast cancers). Subareolar mass."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} breast cancer cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
