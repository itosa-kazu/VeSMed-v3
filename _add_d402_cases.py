import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC3158371 - 60M SCLC with SIADH, heavy smoker
    {
        "id":"R1020","source":"PMC","pmcid":"PMC3158371",
        "vignette":"60歳男性。80pack-year喫煙歴。慢性低Na血症、その後悪心・嘔吐・倦怠感。Na 119mEq/L、血漿浸透圧249、尿Na 105、尿浸透圧680。CXR正常。CT: 左肺尖2cm結節+6.2×4cm縦隔腫瘤(左肺門へ進展)+肝転移。気管支鏡でSCLC確認。",
        "final_diagnosis":"小細胞肺癌(SCLC)",
        "expected_id":"D402","in_scope":True,
        "evidence":{
            "S07":"severe",
            "S13":"present",
            "L44":"hyponatremia",
            "L04":"BHL",
            "L63":"multiple",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"SCLC with SIADH + oncogenic osteomalacia. 80 pack-year smoker. Died 1.5 months."
    },
    # Case 3: PMC6995698 - 70F SCLC with SIADH + ectopic Cushing
    {
        "id":"R1021","source":"PMC","pmcid":"PMC6995698",
        "vignette":"70歳女性。40pack-year喫煙歴。2ヶ月前からの頭痛と全身倦怠感。水牛肩、中心性肥満、両下肢圧痕性浮腫。Na 129、K 2.4、血漿浸透圧267、尿浸透圧633。ACTH 253pg/mL、コルチゾール30.3。CXR: 右上肺野腫瘤。CT: 右上葉腫瘍+縦隔リンパ節腫脹。",
        "final_diagnosis":"小細胞肺癌(SCLC)",
        "expected_id":"D402","in_scope":True,
        "evidence":{
            "S05":"severe",
            "S07":"severe",
            "E36":"present",
            "L44":"hyponatremia",
            "L04":"BHL",
            "E13":"present",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"SCLC with dual paraneoplastic: SIADH + ectopic ACTH Cushing. 40 pack-year."
    },
    # Case 7: PMC6663210 - 66M SCLC with Lambert-Eaton
    {
        "id":"R1022","source":"PMC","pmcid":"PMC6663210",
        "vignette":"66歳男性。50pack-year喫煙歴。1年前からの歩行不安定、両下肢感覚異常。悪液質、遠位対称性しびれ、近位筋力低下、Romberg陽性、下肢腱反射消失、左頸部リンパ節(硬)、体重6kg減少。Na 128。CXR: 右傍気管影。CT: 右上葉68mm腫瘤+右肺門45mmリンパ節(SVC圧迫)。EMG: 脱髄性多発神経障害+反復刺激で増大。",
        "final_diagnosis":"小細胞肺癌(SCLC)",
        "expected_id":"D402","in_scope":True,
        "evidence":{
            "S17":"present",
            "S106":"present",
            "E13":"present",
            "E46":"cervical",
            "L44":"hyponatremia",
            "L04":"BHL",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"SCLC with Lambert-Eaton myasthenic syndrome. 50 pack-year. SVC compression."
    },
    # Case 10: PMC9199995 - 71M SCLC Pancoast/Horner
    {
        "id":"R1023","source":"PMC","pmcid":"PMC9199995",
        "vignette":"71歳男性。55pack-year喫煙歴。3ヶ月前からの間欠的咳嗽、2ヶ月前からの嗄声、左頸部・鎖骨上の有痛性腫脹、左肩痛(上肢放散)。ばち指、鎖骨上リンパ節(硬、可動性不良)、手内筋萎縮・筋力低下(C8-T1)、Horner症候群(眼瞼下垂+縮瞳)。CXR: 左肺尖部腫瘤+中等度胸水。CT: 5.4×5.2×4.4cm左上葉腫瘤。",
        "final_diagnosis":"小細胞肺癌(SCLC)",
        "expected_id":"D402","in_scope":True,
        "evidence":{
            "S01":"present",
            "S55":"present",
            "S17":"present",
            "E13":"present",
            "E46":"supraclavicular",
            "L04":"pleural_effusion",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"SCLC with Pancoast syndrome + Horner syndrome. 55 pack-year."
    },
    # Case 14: PMC5961507 - 70M SCLC, cough, ProGRP extremely elevated
    {
        "id":"R1024","source":"PMC","pmcid":"PMC5961507",
        "vignette":"70歳男性。2ヶ月前からの咳嗽。CXR: 上肺野浸潤影。CT: 右上葉腫瘤+胸水。肝転移。胸水細胞診でSCLC。ProGRP 36,700pg/mL(著明高値)、NSE 306ng/mL。",
        "final_diagnosis":"小細胞肺癌(SCLC)",
        "expected_id":"D402","in_scope":True,
        "evidence":{
            "S01":"present",
            "L04":"pleural_effusion",
            "L63":"liver",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"SCLC with liver metastasis. Extremely elevated ProGRP/NSE."
    },
    # Case 2: PMC8943389 - 67M Stage I SCLC with SIADH only
    {
        "id":"R1025","source":"PMC","pmcid":"PMC8943389",
        "vignette":"67歳男性。悪心と食欲不振。Na 112mEq/L(121から低下)。血漿浸透圧240、尿浸透圧468、尿Na 75。CT: 右下葉13mm結節、PET陽性。リンパ節腫脹なし。脳MRI陰性。",
        "final_diagnosis":"小細胞肺癌(SCLC)",
        "expected_id":"D402","in_scope":True,
        "evidence":{
            "S13":"present",
            "S46":"present",
            "L44":"hyponatremia",
            "L04":"normal",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"Very early stage SCLC (T1bN0M0) presenting only with SIADH. Na 112."
    },
    # Case 16: PMC2886876 - 82M SCLC, hemoptysis, heavy smoker
    {
        "id":"R1026","source":"PMC","pmcid":"PMC2886876",
        "vignette":"82歳男性。60年間の1日30本喫煙歴。2週間前からの血痰混じりの咳嗽。呼吸音清明、リンパ節腫脹なし。軽度正球性貧血。CXR: 右上葉腫瘤。CT: 3.7cm分葉状右上葉腫瘤、気管支包囲、縦隔浸潤、リンパ節腫大。",
        "final_diagnosis":"小細胞肺癌(SCLC)",
        "expected_id":"D402","in_scope":True,
        "evidence":{
            "S01":"present",
            "S16":"present",
            "L04":"lobar_infiltrate",
            "E01":"under_37.5",
            "T01":"1w_to_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"SCLC + synchronous NSCLC. 82M, 60-year heavy smoker. Hemoptysis presentation."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} SCLC cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
