"""
D412 脊柱管狭窄症(LSS) 案例追加
Sources: PMC6709168, PMC7610032, PMC3267447
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC6709168 - 46M LSS with bilateral claudication
    {
        "id":"R1065","source":"PMC","pmcid":"PMC6709168",
        "vignette":"46歳男性。3年来の腰痛、両側下腿痛+しびれ、神経性間欠性跛行。前脛骨筋・長母趾伸筋筋力III。膝蓋腱反射低下、アキレス腱反射消失。両側SLR陽性。会陰部感覚正常。MRI: L3/4, L4/5椎間板突出。",
        "final_diagnosis":"腰部脊柱管狭窄症",
        "expected_id":"D412","in_scope":True,
        "evidence":{
            "S56":"present",
            "S111":"present",
            "S22":"present",
            "S76":"dermatomal",
            "E53":"hyporeflexia",
            "S48":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"LSS with bilateral shank pain/numbness, neurogenic claudication 3 years. L3-5 disc protrusion."
    },
    # Case 2: PMC7610032 - 63M severe LSS with spondylolisthesis
    {
        "id":"R1066","source":"PMC","pmcid":"PMC7610032",
        "vignette":"63歳男性。2年来の慢性腰痛。50m以上の歩行/立位で両側下肢放散痛。神経学的欠損なし。MRI: L4-5低悪性度辷り症+重度中心管狭窄。",
        "final_diagnosis":"腰部脊柱管狭窄症",
        "expected_id":"D412","in_scope":True,
        "evidence":{
            "S56":"present",
            "S111":"present",
            "S22":"present",
            "S106":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Severe LSS at L4-5 with spondylolisthesis. Claudication at 50m. Declined surgery."
    },
    # Case 3: PMC3267447 - 71M tandem stenosis with cauda equina signs
    {
        "id":"R1067","source":"PMC","pmcid":"PMC3267447",
        "vignette":"71歳男性。両側下肢筋力低下(特に階段昇降時)。サドル領域のしびれ(両側)。便失禁エピソード。排尿困難。下肢反射亢進。足部の全般的感覚低下。MRI: T12-L1, L1-2, L4-5多発性脊柱管狭窄。",
        "final_diagnosis":"腰部脊柱管狭窄症",
        "expected_id":"D412","in_scope":True,
        "evidence":{
            "S22":"present",
            "S111":"present",
            "S48":"present",
            "S76":"saddle",
            "S106":"present",
            "S110":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"Tandem stenosis (cervical+lumbar). Cauda equina signs: saddle numbness, bowel incontinence, urinary difficulty."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} LSS cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
