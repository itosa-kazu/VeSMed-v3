"""
D410 尋常性乾癬 案例追加
Sources: PMC6143714, PMC6120403, PMC8419559
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC6143714 - 60F moderate plaque psoriasis with pruritus
    {
        "id":"R1059","source":"PMC","pmcid":"PMC6143714",
        "vignette":"60歳女性。中等度の汎発性尋常性乾癬(BSA 10%)。境界明瞭な紅斑性鱗屑プラーク。掻痒感あり、疼痛なし。軽度変形性関節症の既往あるが関節腫脹なし。PASI 7.2。",
        "final_diagnosis":"尋常性乾癬",
        "expected_id":"D410","in_scope":True,
        "evidence":{
            "S18":"present",
            "E12":"maculopapular_rash",
            "S96":"generalized",
            "S87":"rash_widespread",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Moderate plaque psoriasis. BSA 10%, PASI 7.2. Pruritus without pain."
    },
    # Case 2: PMC6120403 - 65F psoriasis exacerbation on limbs + scalp
    {
        "id":"R1060","source":"PMC","pmcid":"PMC6120403",
        "vignette":"65歳女性。1週間前からの四肢に多発する搔痒性紅斑鱗屑性プラーク。頭皮+耳後部にも乾癬様鱗屑。発熱・体重減少・盗汗なし。既知の頭皮乾癬の増悪。",
        "final_diagnosis":"尋常性乾癬",
        "expected_id":"D410","in_scope":True,
        "evidence":{
            "S18":"present",
            "E12":"maculopapular_rash",
            "S96":"localized",
            "S87":"rash_widespread",
            "S75":"extremities_centrifugal",
            "E01":"under_37.5",
            "T01":"3d_to_1w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Psoriasis exacerbation during PD-1 therapy. Scalp + limbs."
    },
    # Case 3: PMC8419559 - 35M PsA with dactylitis + scalp patch
    {
        "id":"R1061","source":"PMC","pmcid":"PMC8419559",
        "vignette":"35歳男性。5日前からの右示指・環指+右第4趾の有痛性腫脹。手掌腫脹あり。頭皮に3×2.5cmの鱗屑を伴う乾癬パッチ。爪変化なし。HLA-B27陰性、RF陰性、炎症マーカー正常。",
        "final_diagnosis":"尋常性乾癬",
        "expected_id":"D410","in_scope":True,
        "evidence":{
            "S18":"present",
            "E12":"maculopapular_rash",
            "S08":"present",
            "S90":"oligoarticular",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Psoriatic arthritis with dactylitis. Scalp psoriatic patch. CASPAR score 4."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} psoriasis cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
