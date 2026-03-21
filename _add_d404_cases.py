import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC8543963 - 3y Sri Lankan boy
    {
        "id":"R1032","source":"PMC","pmcid":"PMC8543963",
        "vignette":"3歳男児。進行性の歩行困難、動揺性歩行、筋緊張低下、発達遅延。両側腓腹筋肥大、Gower徴候陽性、下肢筋力grade 4。CK 12,395 U/L。MLPA: ジストロフィン遺伝子exon 45-79ヘミ接合性欠失。心エコー/ECG正常。",
        "final_diagnosis":"Duchenne型筋ジストロフィー(DMD)",
        "expected_id":"D404","in_scope":True,
        "evidence":{
            "S48":"present",
            "L17":"very_high",
            "S106":"present",
            "S137":"waddling",
            "E81":"flaccid",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"1_5","R02":"male"},
        "notes":"DMD with contiguous gene deletion. CK 12,395. Gower's sign positive."
    },
    # Case 4: PMC10998125 - 8y Chinese boy
    {
        "id":"R1033","source":"PMC","pmcid":"PMC10998125",
        "vignette":"8歳男児。幼児期からの尖足歩行、アヒル様歩行、頻回の転倒。両側腓腹筋仮性肥大(硬化)、腱反射減弱、近位筋力低下(下肢grade III+、上肢grade IV)。CK 31,406 U/L(正常50-310)。ALT 401.6、AST 645.2、LDH 2,180.6。EMG: 筋原性。ECG: 洞性頻脈。",
        "final_diagnosis":"Duchenne型筋ジストロフィー(DMD)",
        "expected_id":"D404","in_scope":True,
        "evidence":{
            "S48":"present",
            "L17":"very_high",
            "S106":"present",
            "S137":"waddling",
            "E53":"hyporeflexia",
            "L11":"very_high",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"6_12","R02":"male"},
        "notes":"DMD. CK 31,406. Novel exon 35 deletion. AST/ALT elevated from muscle origin."
    },
    # Case 3: PMC7752564 - 11y Tanzanian boy
    {
        "id":"R1034","source":"PMC","pmcid":"PMC7752564",
        "vignette":"11歳男児。6年以上の全身脱力。成績不良、頻回転倒、同級生についていけない。動揺性歩行、腰椎前弯、尖足歩行、近位下肢筋力低下、腓腹筋肥大、扁平足、Gower徴候陽性、軽度筋萎縮。CK 20,232 U/L。ALT 206、AST 192.4、LDH 645。筋生検: 広範な筋線維脱落→脂肪置換+線維化。心エコー/ECG正常。",
        "final_diagnosis":"Duchenne型筋ジストロフィー(DMD)",
        "expected_id":"D404","in_scope":True,
        "evidence":{
            "S48":"present",
            "L17":"very_high",
            "S106":"present",
            "S137":"waddling",
            "E53":"hyporeflexia",
            "L11":"mild_elevated",
            "S07":"severe",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"6_12","R02":"male"},
        "notes":"DMD. CK 20,232. Biopsy confirmed. Maternal uncle with same symptoms."
    },
    # Case 2: PMC5787973 - 12y Indian boy
    {
        "id":"R1035","source":"PMC","pmcid":"PMC5787973",
        "vignette":"12歳男児。頻回の転倒、易疲労性、筋力低下、階段昇降困難。近位筋力低下(上肢+下肢)、腓腹筋仮性肥大、ハムストリング拘縮、Gower徴候陽性。CK 7,342 U/L。LDH 595、ALT 124。EMG: 筋原性。筋生検: ジストロフィン陰性(DYS1/DYS2/DYS3)。母方叔父が同疾患で若年死。",
        "final_diagnosis":"Duchenne型筋ジストロフィー(DMD)",
        "expected_id":"D404","in_scope":True,
        "evidence":{
            "S48":"present",
            "L17":"very_high",
            "S106":"present",
            "S137":"waddling",
            "S07":"mild",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"6_12","R02":"male"},
        "notes":"DMD. CK 7,342. Dystrophin-negative on biopsy. X-linked family history."
    },
    # Case 5: PMC9130841 - 1y boy incidental DMD during pneumonia
    {
        "id":"R1036","source":"PMC","pmcid":"PMC9130841",
        "vignette":"1歳男児。4日間の咳嗽+発熱で入院(気管支肺炎)。入院時に腓腹筋肥大、対称性近位筋力低下、深部腱反射低下、発達遅延(立位保持のみ、歩行不能)を発見。CK 3,906 U/L(正常0-195)。遺伝子検査: exon 43のナンセンス変異c.6283C>T (p.R2095X)。",
        "final_diagnosis":"Duchenne型筋ジストロフィー(DMD)",
        "expected_id":"D404","in_scope":True,
        "evidence":{
            "S48":"present",
            "L17":"very_high",
            "E53":"hyporeflexia",
            "E81":"flaccid",
            "E01":"under_37.5",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"0_1","R02":"male"},
        "notes":"DMD discovered incidentally during bronchopneumonia admission. 1y. Unable to walk."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} DMD cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
