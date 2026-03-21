import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 5: PMC12657040 - 30F inflammatory breast cancer
    {
        "id":"R1045","source":"PMC","pmcid":"PMC12657040",
        "vignette":"30歳女性。6ヶ月前からの急速増大する有痛性左乳房腫瘤。紅斑、間欠的発熱。8×10cm硬い非可動性腫瘤、不整形、発赤皮膚、乳頭陥凹。CT: 13×8.5cm混合腫瘤。CA15-3 204.61(著明高値)、ALP 210、LDH 870。腋窩リンパ節腫脹。",
        "final_diagnosis":"乳癌",
        "expected_id":"D405","in_scope":True,
        "evidence":{
            "S143":"present",
            "S129":"present",
            "E13":"present",
            "E46":"axillary",
            "L104":"mild_elevated",
            "E01":"37.5_38.0",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Inflammatory breast cancer. Young woman. CA15-3 204, LDH 870. Rapid growth."
    },
    # Case 7: PMC12977319 - 51F de novo bone metastasis
    {
        "id":"R1046","source":"PMC","pmcid":"PMC12977319",
        "vignette":"51歳女性。腰痛で受診。腰椎MRI: L2/L3/S1/S3椎体に骨転移を示唆する異常信号。乳房US: 1.5cm病変。生検: IDC grade 2、ER100%、PR85%。",
        "final_diagnosis":"乳癌",
        "expected_id":"D405","in_scope":True,
        "evidence":{
            "S143":"present",
            "L63":"bone",
            "S07":"mild",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"De novo metastatic breast cancer. Presented with low back pain → bone mets found."
    },
    # Case 4: PMC6505228 - 63M male breast cancer + pleural effusion
    {
        "id":"R1047","source":"PMC","pmcid":"PMC6505228",
        "vignette":"63歳男性。進行性呼吸困難。幼少期からの右乳房腫瘤が最近急速増大。尿閉/頻尿。1年で15ポンド体重減少。4cm硬い固定性右乳房腫瘤、皮膚肥厚・陥凹。右腋窩リンパ節腫脹。CXR: 右肺完全白濁(大量胸水)。CT: 6-7cm右乳房腫瘤+腋窩リンパ節+大量胸水+左肺結節。",
        "final_diagnosis":"乳癌",
        "expected_id":"D405","in_scope":True,
        "evidence":{
            "S143":"present",
            "S04":"at_rest",
            "E13":"present",
            "E46":"axillary",
            "S17":"present",
            "L63":"multiple",
            "L04":"pleural_effusion",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Male breast cancer, metastatic. Pleural effusion + lung mets. Synchronous prostate cancer."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} extra breast cancer cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
