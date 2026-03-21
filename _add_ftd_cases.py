import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC4755931 - 55F classic bvFTD, disinhibition, hyperorality
    {
        "id":"R1003","source":"PMC","pmcid":"PMC4755931",
        "vignette":"55歳女性。4年前からの進行性の社会的不適切行動。レストランで人種差別的発言、息子の卒業式を中断、見知らぬ人に性的冗談。甘い物への過食(12ヶ月で+25lbs)。MMSE 26/30、顔の感情認識 6/16。MRI: 著明な両側前頭・側頭葉萎縮。C9orf72陽性。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S167":"present",
            "S120":"present",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Classic bvFTD: disinhibition, hyperorality, loss of empathy. C9orf72+. Autopsy confirmed FTLD."
    },
    # Case 3: PMC10829211 - 52M bvFTD→FTD-MND
    {
        "id":"R1004","source":"PMC","pmcid":"PMC10829211",
        "vignette":"52歳男性。2ヶ月前からの人格変化+不安定歩行。繰り返しオンライン買い物、他人の物を取る、夜間の電話・罵倒、衛生不良。常に間食、易刺激性、無関心。MMSE 23/30、MoCA 19/30、FBI 47。迫害妄想あり。MRI: 両側海馬萎縮、両側側頭葉溝拡大。PET: 両側前頭前野の代謝低下。GRN変異陽性。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S104":"present",
            "S115":"present",
            "S167":"present",
            "S149":"present",
            "S106":"present",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"bvFTD progressing to FTD-MND. GRN + ErbB4 mutations. Died respiratory failure 2 years later."
    },
    # Case 9: PMC4857347 - 51F bvFTD with anxiety prodrome
    {
        "id":"R1005","source":"PMC","pmcid":"PMC4857347",
        "vignette":"51歳女性。1年前からの行動・精神症状悪化。社会的引きこもり、不適切な行動、粗暴な言葉、共感力低下。個人衛生著明に悪化。注意力低下、マルチタスク不能。検査: 病識欠如、接線的言語、保続、作話、軽度喚語困難、意味性錯語。MRI: 著明な右半球優位の前側頭葉萎縮。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S167":"present",
            "S53":"present",
            "S94":"aphasia",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"bvFTD with 30-year anxiety/OCD prodrome. Right temporal atrophy."
    },
    # Case 7: PMC11984016 - 61F FTD-ALS
    {
        "id":"R1006","source":"PMC","pmcid":"PMC11984016",
        "vignette":"61歳女性。48歳時から記憶障害(讃美歌の歌詞を忘れる)。その後、不合理な回答、焦燥、反復的言語、読書速度低下、喚語困難、易刺激性。61歳で右足脱力、近位筋力低下。MMSE 23/30、MoCA 27/30。脳CT/MRI正常。EMG: 多肢の急性/慢性脱神経、舌の線維束攣縮。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S104":"present",
            "S167":"present",
            "S53":"present",
            "S94":"aphasia",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"FTD-ALS. Cognitive onset age 48, motor onset age 61. Normal brain MRI."
    },
    # Case 11: PMC10578331 - 43M FTD-MND, apathy dominant
    {
        "id":"R1007","source":"PMC","pmcid":"PMC10578331",
        "vignette":"43歳男性。2.5年前からの進行性行動・認知変化。深い無関心、無為、意欲喪失、無言症。記憶力低下、交通事故で運転免許喪失。膀胱・腸失禁。検査: 手内在筋萎縮、下肢腱反射亢進、両側バビンスキー陽性。MMSE 18/30→14/30。MRI: 左優位海馬容量減少、第3脳室拡大。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S104":"present",
            "S115":"present",
            "S53":"present",
            "S99":"functional",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"FTD-MND with FUS G559A mutation. Progressive apathy/abulia/mutism. Bilateral Babinski."
    },
    # Case 12: PMC8772087 - 68F temporal variant FTD with OCD
    {
        "id":"R1008","source":"PMC","pmcid":"PMC8772087",
        "vignette":"68歳女性。3年前からの進行性記憶低下(名前の想起困難)。重度の強迫症状: 歩道を1日2回掃除、ゴミを収集し何度も燃やす。喚語困難。MMSE 26/30、視覚名称8/15、MAE 20/60。MRI: 両側非対称性側頭葉萎縮(右優位)、尾状核萎縮。FDG-PET: 前側頭葉低代謝。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S53":"present",
            "S94":"aphasia",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"65_plus","R02":"female"},
        "notes":"Temporal variant FTD with severe OCD. Right temporal predominant atrophy."
    },
    # Case 10: PMC6428013 - 71M FTD-MND + APS
    {
        "id":"R1009","source":"PMC","pmcid":"PMC6428013",
        "vignette":"71歳男性。2年前からの進行性筋力低下+認知機能低下。右上肢4/5、左上肢4/5、両下肢3-4/5。車椅子依存。嚥下困難、舌萎縮・線維束攣縮。記憶障害、言語減少、不適切な感情表出、無関心。K-MMSE 16。前頭遂行機能著明低下。MRI: 両側頭頂・前側頭葉の皮質萎縮。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S104":"present",
            "S115":"present",
            "S167":"present",
            "S25":"present",
            "S106":"present",
            "S53":"present",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"65_plus","R02":"male"},
        "notes":"FTD-MND in setting of antiphospholipid syndrome."
    },
    # Case 2: PMC10544695 - 23M young-onset bvFTD
    {
        "id":"R1010","source":"PMC","pmcid":"PMC10544695",
        "vignette":"23歳男性。人格変化と精神状態変化。独語・独笑、ドアの強迫的数え行為、毎日過度な入浴、同じファストフードのみ摂取。社会的引きこもり。その後反響言語、尿失禁。進行性無言症。CT: 前頭側頭葉優位の重度萎縮。初診は統合失調症と誤診。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S167":"present",
            "S115":"present",
            "S53":"present",
            "S99":"functional",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Extremely young-onset bvFTD. Misdiagnosed as schizophrenia. All genetic tests negative. Died age 26."
    },
    # Case 4: PMC9741737 - 25M extremely early-onset bvFTD
    {
        "id":"R1011","source":"PMC","pmcid":"PMC9741737",
        "vignette":"25歳男性。以前は外向的だったが内向的に変化。仕事を辞め、社会的引きこもり、共感喪失。コンピュータゲームに没頭、過食(過口性)。窃盗、器物損壊。幻視(鳥が見える)、妄想(家族に見捨てられる)。MMSE 16/30、MoCA 11/30。MRI: 著明な前頭側頭葉萎縮。FDG-PET: 重度前頭/側頭低代謝。アミロイドPET・タウPET陰性。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S167":"present",
            "S115":"present",
            "S117":"present",
            "S149":"present",
            "L46":"temporal_lobe_lesion",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"18_39","R02":"male"},
        "notes":"Extremely early-onset sporadic bvFTD. Brain biopsy confirmed neurodegeneration. Amyloid/Tau PET negative."
    },
    # Case 8: PMC10802081 - 42M FTD-ALS, C9orf72+
    {
        "id":"R1012","source":"PMC","pmcid":"PMC10802081",
        "vignette":"42歳男性。数ヶ月にわたる人格変化と奇異行動。侵入的行動増加、言語的攻撃性。脱抑制(台所の流しに排尿)、感情不安定。肉嫌悪と炭水化物渇望、飲酒増加。社会的引きこもり、過眠。幻視、無目的な反復行動。進行性無言症、嚥下困難。MoCA 5/30。SPECT: 両側頭頂葉の灌流低下。C9orf72陽性。",
        "final_diagnosis":"前頭側頭型認知症(FTD/bvFTD)",
        "expected_id":"D400","in_scope":True,
        "evidence":{
            "S150":"present",
            "S167":"present",
            "S117":"present",
            "S25":"present",
            "S53":"present",
            "S141":"chronic_progressive",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"FTD-ALS due to C9orf72. Father had bulbar ALS. Autopsy: FTLD-TDP Type C."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} FTD cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
