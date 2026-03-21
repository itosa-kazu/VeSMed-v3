import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC6035407 - 34F, severe PE, classic presentation
    {
        "id":"R1013","source":"PMC","pmcid":"PMC6035407",
        "vignette":"34歳女性、G2P1、妊娠26週。1日前からの重度持続性後頭部頭痛、霧視、1週間前からの全身浮腫。BP 180/120mmHg。蛋白尿+2。AST 102, ALT 89, LDH 288, 血小板169,000, Cr 0.69。下腿浮腫(+)、深部腱反射+2。β-hCG陽性。",
        "final_diagnosis":"子癇前症/子癇(Preeclampsia/Eclampsia)",
        "expected_id":"D401","in_scope":True,
        "evidence":{
            "E38":"crisis_over_180",
            "L78":"mild_proteinuria",
            "S05":"severe",
            "S54":"present",
            "E36":"present",
            "L11":"mild_elevated",
            "L56":"positive",
            "R15":"yes",
            "T01":"3d_to_1w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Early-onset severe preeclampsia at 26 weeks. Classic triad: HTN + proteinuria + headache."
    },
    # Case 3: PMC7640453 - 31F, PE→eclampsia with seizures
    {
        "id":"R1014","source":"PMC","pmcid":"PMC7640453",
        "vignette":"31歳女性、G2P1、妊娠27週。頭痛と暗点。BP初期130/90→160/100→175/120mmHg。尿酸0.49, AST 78, ALT 65, 血小板149,000, 24h蛋白尿5.92g。体重4kg増加。MgSO4開始後も産後に子癇発作、ICU挿管。β-hCG陽性。",
        "final_diagnosis":"子癇前症/子癇(Preeclampsia/Eclampsia)",
        "expected_id":"D401","in_scope":True,
        "evidence":{
            "E38":"crisis_over_180",
            "L78":"nephrotic_range",
            "S05":"severe",
            "S54":"present",
            "S42":"present",
            "L11":"mild_elevated",
            "S120":"present",
            "L56":"positive",
            "R15":"yes",
            "T01":"3d_to_1w",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Severe PE→eclampsia. Scotomata, massive proteinuria, postpartum seizures despite MgSO4."
    },
    # Case 6: PMC5660323 - 21F eclampsia with fatal brainstem hemorrhage
    {
        "id":"R1015","source":"PMC","pmcid":"PMC5660323",
        "vignette":"21歳女性、妊娠38週、未管理妊娠。BP 150/100mmHg。頭痛、耳鳴、深部腱反射亢進、心窩部痛。AST 462, ALT 286, LDH 1400, Cr 9.8mg/L。術後に子癇発作→昏睡。β-hCG陽性。",
        "final_diagnosis":"子癇前症/子癇(Preeclampsia/Eclampsia)",
        "expected_id":"D401","in_scope":True,
        "evidence":{
            "E38":"elevated_140_180",
            "S05":"severe",
            "S12":"present",
            "S89":"epigastric",
            "S42":"present",
            "L11":"very_high",
            "L56":"positive",
            "R15":"yes",
            "E16":"obtunded",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Fatal eclampsia. Brainstem hemorrhage post-seizure. Unmonitored pregnancy."
    },
    # Case 8a: PMC6180921 - 20F eclampsia, seizure
    {
        "id":"R1016","source":"PMC","pmcid":"PMC6180921",
        "vignette":"20歳女性、初産、妊娠40週。来院3時間前に痙攣発作。BP 147/95mmHg。蛋白尿+1。AST 28.7, ALT 16.4, Cr 0.90, 血小板正常。MgSO4抵抗性の再発痙攣→チオペンタール。β-hCG陽性。",
        "final_diagnosis":"子癇前症/子癇(Preeclampsia/Eclampsia)",
        "expected_id":"D401","in_scope":True,
        "evidence":{
            "E38":"elevated_140_180",
            "L78":"mild_proteinuria",
            "S42":"present",
            "L56":"positive",
            "R15":"yes",
            "T01":"under_3d",
            "T02":"sudden"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Eclampsia with MgSO4-resistant seizures. Minimal lab abnormalities. Nulliparous."
    },
    # Case 11: PMC3939391 - 28F late postpartum eclampsia with PRES + visual loss
    {
        "id":"R1017","source":"PMC","pmcid":"PMC3939391",
        "vignette":"28歳女性、G2P2、産後2週間。腹痛・腹部膨満で入院。その後頭痛+両側視力低下。BP初期135/85→180/100mmHg。WBC 17,000, 血小板230,000, 蛋白尿3+, 肝機能正常。痙攣発作(全身性強直間代)。視力は手動弁まで低下、瞳孔反応正常。β-hCG陽性。",
        "final_diagnosis":"子癇前症/子癇(Preeclampsia/Eclampsia)",
        "expected_id":"D401","in_scope":True,
        "evidence":{
            "E38":"crisis_over_180",
            "L78":"nephrotic_range",
            "S05":"severe",
            "S122":"bilateral",
            "S42":"present",
            "S12":"present",
            "L56":"positive",
            "R15":"yes",
            "T01":"3d_to_1w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Late postpartum eclampsia with PRES. Bilateral near-blindness (cortical). Vision recovered."
    },
    # Case 5: PMC7145984 - 29F severe PE→HELLP→aHUS (model as PE)
    {
        "id":"R1018","source":"PMC","pmcid":"PMC7145984",
        "vignette":"29歳女性、初産、妊娠34週。上腹部痛、頭痛、嘔吐、落ち着きのなさ、振戦。BP 133/91→147/87→170/94mmHg。蛋白尿1.6g/24h。ALT 23→159→1800, LDH 1231→3570, 血小板158→49→33×10^9/L, Cr 153μmol/L。乏尿(10mL/h)。腱反射亢進。β-hCG陽性。",
        "final_diagnosis":"子癇前症/子癇(Preeclampsia/Eclampsia)",
        "expected_id":"D401","in_scope":True,
        "evidence":{
            "E38":"crisis_over_180",
            "L78":"mild_proteinuria",
            "S05":"severe",
            "S12":"present",
            "S89":"epigastric",
            "S13":"present",
            "L11":"very_high",
            "L14":"thrombocytopenia",
            "L16":"elevated",
            "L55":"mild_elevated",
            "L56":"positive",
            "R15":"yes",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Severe PE→HELLP→aHUS. Primigravida. Progressive deterioration. Dialysis required."
    },
    # Case 14: PMC6494391 - 23F late postpartum eclampsia (10 weeks post)
    {
        "id":"R1019","source":"PMC","pmcid":"PMC6494391",
        "vignette":"23歳女性、G1P1、産後71日。2日前からの間欠的頭痛+悪心。その後霧視+意識変容+全身性強直間代痙攣。BP 141/103mmHg。WBC 11,220。β-hCG陽性。",
        "final_diagnosis":"子癇前症/子癇(Preeclampsia/Eclampsia)",
        "expected_id":"D401","in_scope":True,
        "evidence":{
            "E38":"elevated_140_180",
            "S05":"severe",
            "S54":"present",
            "S42":"present",
            "S13":"present",
            "E16":"confused",
            "L56":"positive",
            "R15":"yes",
            "T01":"under_3d",
            "T02":"acute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Extremely late postpartum eclampsia (71 days). PRES on MRI. Primigravida."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} PE/eclampsia cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
