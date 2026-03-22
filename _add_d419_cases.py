"""
D419 コクシジオイデス症 (Coccidioidomycosis) 案例追加
Sources: PMC10501056, PMC11539121, PMC4745348, PMC12038191, PMC6069939
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC10501056 - 49M, classic: chest pain+SOB+fever+night sweats+weight loss+cough
    {
        "id":"R1098","source":"PMC","pmcid":"PMC10501056",
        "vignette":"49歳男性。カリフォルニア州コーチェラバレー在住。2-3ヶ月前にアリゾナ渡航歴。2ヶ月間の暗緑色痰を伴う湿性咳嗽。1週間前から右胸痛+呼吸困難+38.3℃の発熱+悪寒+盗汗+体重減少(1週で5ポンド)。CRP 11.3mg/dL。プロカルシトニン正常。血糖445mg/dL(新規糖尿病)。CXR: 右肺4-5cm腫瘤。CT: 右下葉6cm厚壁空洞+微小結節+少量胸水。",
        "final_diagnosis":"コクシジオイデス症",
        "expected_id":"D419","in_scope":True,
        "evidence":{
            "E01":"38.0_39.0",
            "S01":"present",
            "S04":"present",
            "S15":"present",
            "S16":"present",
            "S17":"present",
            "L02":"high_over_10",
            "L04":"lobar_infiltrate",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Classic pulmonary cocci. Coachella Valley + Arizona travel. Cavitary RLL lesion. Serology IgM/IgG+, CF 1:8. Biopsy: C. posadasii. New-onset DM."
    },
    # Case 2: PMC11539121 Case 1 - 60M, documented eosinophilia 1.70, CRP 205
    {
        "id":"R1099","source":"PMC","pmcid":"PMC11539121",
        "vignette":"60歳男性(中国人)。アリゾナ渡航歴。発熱+咳嗽+喀痰。WBC 17580/μL。好酸球1700/μL(著明増多、基準0.02-0.52)。CRP 205.67mg/L。ESR 40mm/h。インフルエンザA IgM陽性(重複感染)。CT: 左下葉浸潤影+左胸水。mNGS: C. immitis検出(981 sequences)。",
        "final_diagnosis":"コクシジオイデス症",
        "expected_id":"D419","in_scope":True,
        "evidence":{
            "E01":"38.0_39.0",
            "S01":"present",
            "L14":"eosinophilia",
            "L02":"high_over_10",
            "L01":"high_10000_20000",
            "L04":"lobar_infiltrate",
            "T01":"1w_to_3w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"KEY case: documented eosinophilia (1700/uL). CRP markedly elevated 205mg/L=20.5mg/dL. WBC 17.58k. Influenza A co-infection. mNGS diagnosed."
    },
    # Case 3: PMC4745348 - 31M, fever 103F + pleurisy + productive cough, 2 weeks
    {
        "id":"R1100","source":"PMC","pmcid":"PMC4745348",
        "vignette":"31歳男性(ヒスパニック)。テキサス州エルパソ在住。メキシコ・フアレスで解体/建設作業。2週間の発熱+湿性咳嗽+胸膜痛。再入院時39.4℃(103.0°F)。左肺底部crackles→左呼吸音消失。WBC 13000→17500/μL。新規糖尿病。CXR: 4.4cm空洞+気液面+左肺門/縦隔リンパ節腫脹+両側tree-in-bud。膿気胸合併。",
        "final_diagnosis":"コクシジオイデス症",
        "expected_id":"D419","in_scope":True,
        "evidence":{
            "E01":"39.0_40.0",
            "S01":"present",
            "S04":"present",
            "S15":"present",
            "L01":"high_10000_20000",
            "L04":"lobar_infiltrate",
            "T01":"1w_to_3w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Young Hispanic male, construction work in Mexico (dust exposure). High fever 39.4C. Cavitary lesion + pyopneumothorax. Serology ID-TP/CF+. Culture C. immitis."
    },
    # Case 4: PMC12038191 - 58M, chronic cavitary, no fever, weight loss+fatigue+dyspnea
    {
        "id":"R1101","source":"PMC","pmcid":"PMC12038191",
        "vignette":"58歳男性。テキサス州エルパソ在住。4週間の湿性咳嗽+労作時呼吸困難(NYHA III)+少量喀血+著明な体重減少+倦怠感。発熱・悪寒・関節痛・皮疹なし。るい痩(BMI 16)。HR 90、RR 24、BP 110/70、SpO2 92%(O2 2L)。右肺呼吸音著明減弱。左上肺crepitations。WBC 9970(正常)。Hb 9.4g/dL(貧血)。Plt 554000。CRP 18mg/dL。",
        "final_diagnosis":"コクシジオイデス症",
        "expected_id":"D419","in_scope":True,
        "evidence":{
            "E01":"under_37.5",
            "S01":"present",
            "S04":"present",
            "S07":"severe",
            "S17":"present",
            "L02":"high_over_10",
            "L01":"normal_4000_10000",
            "L04":"bilateral_infiltrate",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Chronic cavitary cocci. Afebrile. Cachectic BMI 16. Bilateral cavities + BPF + hydropneumothorax. SpO2 92%. CRP 18. Serology ID 1:4."
    },
    # Case 5: PMC6069939 - 25M, dyspnea+cough+chest pain, 2 months, trapped lung
    {
        "id":"R1102","source":"PMC","pmcid":"PMC6069939",
        "vignette":"25歳男性。2-3年前アリゾナで勤務、現在テキサス州ダラス在住。2ヶ月間の進行性労作時呼吸困難+乾性咳嗽+咳嗽時の右鋭い胸痛。発熱・倦怠感・盗汗・筋肉痛・関節痛・皮疹なし。軽度頻呼吸。右上肺呼吸音消失+過共鳴、右下肺濁音。CBC・代謝パネル異常なし。HIV陰性。β-Dグルカン328pg/mL(上昇)。CXR: 大量右気胸+中等量胸水。",
        "final_diagnosis":"コクシジオイデス症",
        "expected_id":"D419","in_scope":True,
        "evidence":{
            "S01":"present",
            "S04":"present",
            "S15":"present",
            "L04":"pneumothorax",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Cocci presenting as trapped lung. Arizona work history 2-3y prior. Pneumothorax + pleural effusion. No fever/myalgia/arthralgia. Serology IgG+. Culture C. immitis."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} coccidioidomycosis cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
