"""
D411 丹毒(Erysipelas) 案例追加
Sources: PMC11257657, PMC5297528, PMC12488269
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC11257657 - 52F abdominal wall erysipelas
    {
        "id":"R1062","source":"PMC","pmcid":"PMC11257657",
        "vignette":"52歳女性。1日前からの発熱・悪寒+腹壁の発赤。倦怠感・食欲不振・体痛が皮膚変化に先行。腹壁全体+両側乳房下に広範な紅斑+圧痛。丘疹/水疱なし。体温37.3℃。WBC 14.6×10³, CRP 16.1mg/dL。抗DNase B 240(GAS確認)。",
        "final_diagnosis":"丹毒",
        "expected_id":"D411","in_scope":True,
        "evidence":{
            "S18":"present",
            "E12":"localized_erythema_warmth_swelling",
            "S87":"localized_pain_redness",
            "E01":"37.5_38.0",
            "S09":"present",
            "S07":"mild",
            "L02":"highly_elevated",
            "L01":"high",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Abdominal wall erysipelas. Umbilical piercing as portal of entry. GAS confirmed."
    },
    # Case 2: PMC5297528 - 63M facial erysipelas
    {
        "id":"R1063","source":"PMC","pmcid":"PMC5297528",
        "vignette":"63歳男性。顔面の腫脹+倦怠感。両眼瞼・頬・鼻に光沢のある紅斑性浮腫性病変。触診で熱感+圧痛。体温38.0℃、脈拍90/分。WBC 18700/μL。ASOT 380 IU/mL(上昇)。",
        "final_diagnosis":"丹毒",
        "expected_id":"D411","in_scope":True,
        "evidence":{
            "S18":"present",
            "E12":"localized_erythema_warmth_swelling",
            "S87":"localized_pain_redness",
            "E01":"38.0_39.0",
            "S07":"mild",
            "E36":"present",
            "L01":"very_high",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Facial erysipelas with secondary glomerulonephritis. WBC 18700, ASOT elevated."
    },
    # Case 3: PMC12488269 - 60F lower limb bullous erysipelas
    {
        "id":"R1064","source":"PMC","pmcid":"PMC12488269",
        "vignette":"60歳女性。左下腿の外傷後に疼痛・灼熱感+紅斑が急速に拡大。境界明瞭な紅斑性浮腫性プラーク。のち紫色変色+水疱形成。5日間で急速進行。血算・血糖正常。",
        "final_diagnosis":"丹毒",
        "expected_id":"D411","in_scope":True,
        "evidence":{
            "S18":"present",
            "E12":"localized_erythema_warmth_swelling",
            "S87":"localized_pain_redness",
            "E36":"present",
            "E01":"under_37.5",
            "T01":"3d_to_1w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Bullous erysipelas of left lower leg. Post-traumatic. Initially misdiagnosed as cellulitis."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} erysipelas cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
