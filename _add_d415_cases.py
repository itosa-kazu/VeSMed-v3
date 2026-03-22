"""
D415 絨毛膜羊膜炎 (Chorioamnionitis) 案例追加
Sources: PMC10208626, PMC9711999, PMC11528179, PMC3484970, PMC10171218
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC10208626 - 26F 39w, severe (septic shock), C.perfringens, PROM
    {
        "id":"R1078","source":"PMC","pmcid":"PMC10208626",
        "vignette":"26歳初産婦。妊娠39週。破水2時間後に38.0℃の発熱+悪寒戦慄。分娩後に敗血症性ショック(血圧88/54、脈拍130)。WBC 18.6×10³/μL。CRP 187mg/L。血液培養: Clostridium perfringens。胎盤病理で急性好中球浸潤。",
        "final_diagnosis":"絨毛膜羊膜炎",
        "expected_id":"D415","in_scope":True,
        "evidence":{
            "E01":"38.0_39.0",
            "E02":"over_120",
            "S09":"present",
            "L01":"high_10000_20000",
            "L02":"high_over_10",
            "R15":"yes",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Severe chorioamnionitis → septic shock (C. perfringens). PROM-triggered. WBC 18.6k, CRP 187mg/L."
    },
    # Case 2: PMC9711999 - 31F 39w, classic presentation, prolonged ROM 3d
    {
        "id":"R1079","source":"PMC","pmcid":"PMC9711999",
        "vignette":"31歳初産婦。妊娠39週。3日前から膣漏液(前期破水)。入院後38.0℃に上昇、母体脈拍140/分。胎児心拍170bpm(頻脈)。WBC 18.9×10³/μL。CRP 53mg/L。厚いメコニウム。胎盤培養: AmpC Klebsiella。",
        "final_diagnosis":"絨毛膜羊膜炎",
        "expected_id":"D415","in_scope":True,
        "evidence":{
            "E01":"38.0_39.0",
            "E02":"over_120",
            "L01":"high_10000_20000",
            "L02":"moderate_3_10",
            "R15":"yes",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Classic chorioamnionitis. Prolonged ROM 3 days. Maternal+fetal tachycardia. AmpC Klebsiella."
    },
    # Case 3: PMC11528179 - 27F 27+3w, preterm, Listeria, intact membranes
    {
        "id":"R1080","source":"PMC","pmcid":"PMC11528179",
        "vignette":"27歳経産婦(IVF妊娠)。妊娠27週3日。6日間の発熱+全身痛。体温39.4℃。胎動減少。軽度腹部圧痛。破水なし。WBC 8.19×10³/μL(正常)。CRP 69mg/L。羊水穿刺: WBC>2000、グルコース<11mg/dL。羊水培養: Listeria monocytogenes。",
        "final_diagnosis":"絨毛膜羊膜炎",
        "expected_id":"D415","in_scope":True,
        "evidence":{
            "E01":"39.0_40.0",
            "L01":"normal_4000_10000",
            "L02":"moderate_3_10",
            "S12":"present",
            "R15":"yes",
            "T01":"3d_to_1w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Preterm Listeria chorioamnionitis. Intact membranes (hematogenous). Normal WBC! CRP 69. 6-day fever."
    },
    # Case 4: PMC3484970 - 21F 38w, Fusobacterium, intact membranes, abdominal cramps
    {
        "id":"R1081","source":"PMC","pmcid":"PMC3484970",
        "vignette":"21歳初産婦。妊娠38週。38.0℃の発熱+母体頻脈。胎児心拍170bpm。腹部痙攣+腰痛。子宮圧痛なし。WBC 19500(左方移動)。羊水穿刺で膿性悪臭羊水。培養: Fusobacterium nucleatum。分娩中に敗血症性ショックに進行。",
        "final_diagnosis":"絨毛膜羊膜炎",
        "expected_id":"D415","in_scope":True,
        "evidence":{
            "E01":"38.0_39.0",
            "E02":"100_120",
            "L01":"high_10000_20000",
            "S12":"present",
            "S89":"suprapubic",
            "S128":"present",
            "R15":"yes",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Fusobacterium chorioamnionitis. Intact membranes. Foul-smelling amniotic fluid. Progressed to septic shock."
    },
    # Case 5: PMC10171218 - 26F 36+6w, Listeria, chills, near-term
    {
        "id":"R1082","source":"PMC","pmcid":"PMC10171218",
        "vignette":"26歳初産婦。妊娠36週6日。37.7℃→38.4℃の発熱+悪寒+咳嗽。胎児心拍175bpm(頻脈)。不規則子宮収縮。WBC 16810/μL。CRP 102.7mg/L。胎盤培養: Listeria monocytogenes+E.coli+Bacteroides。病理で急性絨毛膜羊膜炎+微小膿瘍。",
        "final_diagnosis":"絨毛膜羊膜炎",
        "expected_id":"D415","in_scope":True,
        "evidence":{
            "E01":"38.0_39.0",
            "S09":"present",
            "L01":"high_10000_20000",
            "L02":"high_over_10",
            "R15":"yes",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Listeria chorioamnionitis near-term. Chills, leukocytosis, CRP 103. Polymicrobial. Placental microabscesses."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} chorioamnionitis cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
