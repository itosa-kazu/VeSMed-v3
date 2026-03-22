"""
D416 大腿骨頸部骨折 (Femoral Neck Fracture) 案例追加
Sources: PMC9568747, PMC12508903, PMC11934235, PMC8076929, PMC5534680
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC9568747 - 94F, classic displaced, external rotation + shortening + ecchymosis
    {
        "id":"R1083","source":"PMC","pmcid":"PMC9568747",
        "vignette":"94歳女性。立位からの転倒後、左股関節の激痛。左下肢の運動不能・荷重不能。左下肢短縮+外旋変形。左大腿外側に皮下出血。左下肢の感覚は保たれている。股関節可動域は疼痛で著明に制限。",
        "final_diagnosis":"大腿骨頸部骨折",
        "expected_id":"D416","in_scope":True,
        "evidence":{
            "S28":"present",
            "S08":"present",
            "S48":"present",
            "S106":"present",
            "S06":"present",
            "T01":"under_3d",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Classic displaced subcapital fracture. External rotation + LLD + ecchymosis. Low-energy fall from standing. Concomitant pubic rami fractures."
    },
    # Case 2: PMC12508903 - 72M, displaced Garden IV, initially missed on X-ray
    {
        "id":"R1084","source":"PMC","pmcid":"PMC12508903",
        "vignette":"72歳男性。転倒受傷後の左股関節痛と腰痛。左下肢への荷重不能。VAS 7/10。バイタルサイン安定。遠位神経血管所見は正常。脚長差約3cm。",
        "final_diagnosis":"大腿骨頸部骨折",
        "expected_id":"D416","in_scope":True,
        "evidence":{
            "S28":"present",
            "S08":"present",
            "S48":"present",
            "S106":"present",
            "S111":"present",
            "T01":"under_3d",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"Displaced Garden IV, initially missed on first X-ray. Repeat imaging 6 days later confirmed displaced femoral neck fracture. LLD 3cm. Also had lower back pain (referred)."
    },
    # Case 3: PMC11934235 - 90F, bilateral fractures, severe delirium (AMT 0/10)
    {
        "id":"R1085","source":"PMC","pmcid":"PMC11934235",
        "vignette":"90歳女性。自宅で転倒し床で発見される。左下肢痛と右股関節痛。右股関節部に小さな皮下出血。意識混濁が著明(AMT 0/10)。骨粗鬆症、心房細動(アスピリン内服)、CKD3期の既往。普段は歩行器使用で独居。",
        "final_diagnosis":"大腿骨頸部骨折",
        "expected_id":"D416","in_scope":True,
        "evidence":{
            "S28":"present",
            "S08":"present",
            "S48":"present",
            "S106":"present",
            "E16":"confused",
            "T01":"under_3d",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Bilateral simultaneous proximal femoral fractures (right extracapsular + left intracapsular). Severe delirium AMT 0/10. Hb dropped to 65g/L intraop. Osteoporosis. Cognition returned to baseline by 3 months."
    },
    # Case 4: PMC8076929 - 97F, non-displaced Garden II, mild dementia
    {
        "id":"R1086","source":"PMC","pmcid":"PMC8076929",
        "vignette":"97歳女性。右股関節痛を主訴に受診。BMI 14.8(31.6kg/146cm)。重度僧帽弁閉鎖不全症、軽度認知症、L3圧迫骨折の既往。",
        "final_diagnosis":"大腿骨頸部骨折",
        "expected_id":"D416","in_scope":True,
        "evidence":{
            "S28":"present",
            "S08":"present",
            "E16":"confused",
            "T01":"under_3d",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Non-displaced Garden type II intracapsular fracture. Extremely elderly (97yo), low BMI (14.8). Baseline mild dementia. Prior L3 compression fracture (osteoporosis)."
    },
    # Case 5: PMC5534680 - 77F, occult fracture (X-ray/CT negative, MRI positive)
    {
        "id":"R1087","source":"PMC","pmcid":"PMC5534680",
        "vignette":"77歳女性。立位からの転倒後、持続する右股関節痛。単純X線およびCTで骨折所見なし。MRI(T1冠状断)で右大腿骨頸部に浮腫を認め不顕性骨折と確定。",
        "final_diagnosis":"大腿骨頸部骨折",
        "expected_id":"D416","in_scope":True,
        "evidence":{
            "S28":"present",
            "S08":"present",
            "T01":"under_3d",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Occult non-displaced femoral neck fracture. X-ray and CT negative. Only MRI showed edema at femoral neck. 2-10% of hip fractures are occult (StatPearls)."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} femoral neck fracture cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
