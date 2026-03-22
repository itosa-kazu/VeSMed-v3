"""
D418 線維筋痛症 (Fibromyalgia) 案例追加
Sources: PMC12229245, PMC11810621, PMC8967077, PMC9653028, PMC5336631
"""
import json

data = json.load(open('real_case_test_suite.json','r',encoding='utf-8'))
cases = data if isinstance(data, list) else data.get('cases', data.get('test_cases', []))

new_cases = [
    # Case 1: PMC12229245 - 41F, most complete: pain+stiffness+headache+IBS+fatigue, 7yr
    {
        "id":"R1093","source":"PMC","pmcid":"PMC12229245",
        "vignette":"41歳女性(アフリカ系)。7年前からの広範な疼痛(頸椎・胸椎・腰椎・両肩・両股関節・骨盤)。VAS 7/10。朝のこわばり60-90分。緊張型頭痛が週2-3回。IBS症状(交代性便秘/下痢、腹部痙攣、膨満感)。認知機能低下(ブレインフォグ)。非回復性睡眠。上肢の間欠的感覚異常。FIQR 68/100。倦怠感8/10。神経学的診察は異常なし。",
        "final_diagnosis":"線維筋痛症",
        "expected_id":"D418","in_scope":True,
        "evidence":{
            "E94":"many_11_or_more",
            "S06":"present",
            "S08":"present",
            "S27":"present",
            "S07":"severe",
            "S05":"mild",
            "S12":"present",
            "S14":"present",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"Most complete presentation: widespread pain + morning stiffness 60-90min + tension headache + IBS + brain fog + fatigue 8/10. 7-year established diagnosis. All 18 tender point locations."
    },
    # Case 2: PMC11810621 - 21F, post-parvovirus, all labs normal, 14/18 tender points
    {
        "id":"R1094","source":"PMC","pmcid":"PMC11810621",
        "vignette":"21歳女性。6ヶ月前のパルボウイルスB19感染後から広範な筋骨格系疼痛。認知機能障害(ブレインフォグ)。圧痛点14/18箇所陽性。WPI 7、SS 6。CBC正常、ESR正常、CRP正常、ANA陰性、抗CCP陰性、甲状腺機能正常。",
        "final_diagnosis":"線維筋痛症",
        "expected_id":"D418","in_scope":True,
        "evidence":{
            "E94":"many_11_or_more",
            "S06":"present",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Young female, post-viral (Parvovirus B19) fibromyalgia. 14/18 tender points. All labs normal (CBC/ESR/CRP/ANA/anti-CCP/TSH). ACR 2016 criteria met."
    },
    # Case 3: PMC8967077 - 60M, 18/18 tender points, severe, 8yr history
    {
        "id":"R1095","source":"PMC","pmcid":"PMC8967077",
        "vignette":"60歳男性。8年前から線維筋痛症の診断。月2-3回のフレアー(各約7日間)。灼熱感+電撃痛が両上下肢に放散。右側の脱力。重度の倦怠感+不眠+振戦。頻尿。圧痛点18/18箇所全陽性。顔面痛スケール8/10。重度うつ(HAM-D 20)。障害年金受給中。",
        "final_diagnosis":"線維筋痛症",
        "expected_id":"D418","in_scope":True,
        "evidence":{
            "E94":"many_11_or_more",
            "S06":"present",
            "S07":"severe",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"male"},
        "notes":"Male fibromyalgia (less common). Maximum 18/18 tender points. Severe: permanent disability. 8-year history. Burning+shooting pain bilateral."
    },
    # Case 4: PMC9653028 - 44F, headache+abdominal pain+constipation, 13/18, 2yr
    {
        "id":"R1096","source":"PMC","pmcid":"PMC9653028",
        "vignette":"44歳女性。2年前からの後頭部頭痛+重度の頸部・肩・背部痛。睡眠障害(頻回覚醒、起床時疲労感)。持続する疲労。腹痛+便秘(消化器症状)。圧痛点13/18箇所。NRS 6/10。筋の過緊張(両側SCM、僧帽筋上部、棘上筋)。頸椎ROM制限。臨床検査でリウマチ性/代謝性疾患の所見なし。CBC正常範囲。",
        "final_diagnosis":"線維筋痛症",
        "expected_id":"D418","in_scope":True,
        "evidence":{
            "E94":"many_11_or_more",
            "S06":"present",
            "S05":"mild",
            "S12":"present",
            "S07":"severe",
            "T01":"over_3w",
            "T02":"chronic"
        },
        "risk_factors":{"R01":"40_64","R02":"female"},
        "notes":"FM with headache + GI symptoms (abdominal pain, constipation). 13/18 tender points. Domestic violence trigger. Normal CBC/rheumatic labs."
    },
    # Case 5: PMC5336631 - 32F, 11/18 tender points, specific labs, 1yr
    {
        "id":"R1097","source":"PMC","pmcid":"PMC5336631",
        "vignette":"32歳女性。1年前からの広範な疼痛+倦怠感+睡眠障害。圧痛点11/18箇所。WPI 9、SS 5。Hb 13.3g/dL。ESR 14mm/h(正常)。CRP 5mg/L(正常)。AST 22、ALT 18。Cr 0.49。TSH 0.707(正常)。",
        "final_diagnosis":"線維筋痛症",
        "expected_id":"D418","in_scope":True,
        "evidence":{
            "E94":"many_11_or_more",
            "S06":"present",
            "S07":"mild",
            "L02":"mild_0.3_3",
            "T01":"over_3w",
            "T02":"subacute"
        },
        "risk_factors":{"R01":"18_39","R02":"female"},
        "notes":"Borderline 11/18 tender points (ACR 1990 minimum). WPI 9, SS 5 (meets ACR 2011 modified criteria too). CRP 5mg/L=0.5mg/dL (normal-mild). ESR 14 normal."
    },
]

cases.extend(new_cases)
print(f"Added {len(new_cases)} fibromyalgia cases. Total: {len(cases)}")

with open('real_case_test_suite.json','w',encoding='utf-8') as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)
print("Saved.")
