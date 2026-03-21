"""
D414 低カリウム性周期性四肢麻痺 (HypoPP) 案例追加
Sources: PMC3254894, PMC5614135, PMC4259161, PMC11110751, PMC9596356
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC3254894 Case 2 - 15M classic adolescent, myalgia, areflexia, SCN4A
    {
        "id":"R1073","source":"PMC","pmcid":"PMC3254894",
        "vignette":"15歳男性。起床時の下肢脱力→運動後に上肢も脱力。下肢筋痛。上肢III/V、下肢II/V、左右対称。深部腱反射消失。感覚障害・筋萎縮なし。血清K 2.3mmol/L。心電図正常。",
        "final_diagnosis":"低カリウム性周期性四肢麻痺",
        "expected_id":"D414","in_scope":True,
        "evidence":{
            "L108":"hypo_2.5_3.5",
            "S48":"present",
            "E53":"areflexia",
            "S06":"present",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"13_17","R02":"male"},
        "notes":"Primary HypoPP type 2 (SCN4A R672H). Classic teen male. LL>UL weakness, absent DTR, myalgia."
    },
    # Case 2: PMC5614135 - 9M pediatric, fatigue prodrome, CACNA1S de novo
    {
        "id":"R1074","source":"PMC","pmcid":"PMC5614135",
        "vignette":"9歳男性。インフルエンザ様疾患後、4ヶ月の持続性疲労+全身痛。その後突然の四肢麻痺発作。下肢2/5、上肢4/5。発作時腱反射低下+筋緊張低下。発作間欠期は正常。血清K 2.0mmol/L。",
        "final_diagnosis":"低カリウム性周期性四肢麻痺",
        "expected_id":"D414","in_scope":True,
        "evidence":{
            "L108":"severe_hypo_under_2.5",
            "S48":"present",
            "E53":"hyporeflexia",
            "S07":"severe",
            "S06":"present",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"6_12","R02":"male"},
        "notes":"Primary HypoPP type 1 (CACNA1S de novo). Pediatric. Severe fatigue prodrome + acute paralysis."
    },
    # Case 3: PMC4259161 - 43M adult, 20-year history, palpitations, familial
    {
        "id":"R1075","source":"PMC","pmcid":"PMC4259161",
        "vignette":"43歳男性。20年以上の周期性四肢麻痺発作歴。今回は動悸+右大腿から始まる筋力低下が四肢に拡大。4-6時間で回復。肉体労働・ストレスで誘発。血清K 1.89mmol/L(発作時)。発作間欠期K正常(3.63-3.74)。家族歴陽性(叔父2名+弟+甥)。",
        "final_diagnosis":"低カリウム性周期性四肢麻痺",
        "expected_id":"D414","in_scope":True,
        "evidence":{
            "L108":"severe_hypo_under_2.5",
            "S48":"present",
            "S35":"present",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Primary HypoPP type 1 (CACNA1S R528C). 20-year history, familial. Palpitations + limb paralysis."
    },
    # Case 4: PMC11110751 Case 3 - 28F pregnancy, hypoactive reflexes
    {
        "id":"R1076","source":"PMC","pmcid":"PMC11110751",
        "vignette":"28歳女性(妊婦)。3日間の下肢脱力。先行する嘔吐。下肢2/5、上肢4/5。腱反射低下。血清K 2.3mmol/L。",
        "final_diagnosis":"低カリウム性周期性四肢麻痺",
        "expected_id":"D414","in_scope":True,
        "evidence":{
            "L108":"hypo_2.5_3.5",
            "S48":"present",
            "E53":"hyporeflexia",
            "S106":"present",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Primary HypoPP in pregnancy. Female presentation. LL>UL weakness, hypoactive reflexes."
    },
    # Case 5: PMC9596356 - 16M cardiac dominant, QTc prolongation
    {
        "id":"R1077","source":"PMC","pmcid":"PMC9596356",
        "vignette":"16歳男性。高炭水化物食後に進行性筋力低下。3年間で3回の失神エピソード。血清K 2.7mmol/L。心電図: U波著明+QTc 574ms+ST低下。甲状腺機能正常。",
        "final_diagnosis":"低カリウム性周期性四肢麻痺",
        "expected_id":"D414","in_scope":True,
        "evidence":{
            "L108":"hypo_2.5_3.5",
            "S48":"present",
            "S35":"present",
            "E01":"under_37.5",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"13_17","R02":"male"},
        "notes":"Primary HypoPP with cardiac involvement. QTc 574ms, U waves. Carb-triggered. Gene panel negative."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} HypoPP cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
