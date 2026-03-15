#!/usr/bin/env python3
"""Add AIP 5 cases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)

cases = [
    {"id":"R390","source":"Cureus 2023","pmcid":"PMC10015610","vignette":"25M 溶接工. 数日増悪の湿性咳嗽+2日間の発熱+6-7日の食欲不振. T 39.0, HR 116, RR 38, BP 98/70, SpO2 84%(RA)→96%(高流量O2). WBC 10.3k, PLT 60k, CRP 102, ESR 110, AST 84, ALT 98, D-dimer 581. HRCT:両側多巣GGO+斑状浸潤+牽引性気管支拡張. Echo:EF 47%(心筋炎合併). BiPAP→Day9退院","final_diagnosis":"急性間質性肺炎(AIP/Hamman-Rich)+心筋炎","expected_id":"D175","in_scope":True,"evidence":{"S01":"productive","S04":"at_rest","E01":"39.0_40.0","E02":"100_120","E03":"hypotension_under_90","E04":"severe_over_30","E05":"severe_hypoxia_under_93","E07":"crackles","L04":"bilateral_infiltrate","L01":"high_10000_20000","L02":"high_over_10","L52":"very_high","T01":"under_3d","T02":"gradual_days"},"risk_factors":{"R01":"18_39","R02":"male"},"result":"","notes":"SpO2 84%. CRP 102. EF 47%(心筋炎). Day9退院"},
    {"id":"R391","source":"Cureus 2020","pmcid":"PMC7500727","vignette":"77F CAD+大動脈弁狭窄. 2週前からURI様症状(間欠微熱+非湿性咳嗽+呼吸困難). 初回:T 99.8F, HR 80, RR 18, SpO2 97%(3L). 3日後再入院:T 99.0F, HR 92, RR 24, SpO2 88%(NRB!). WBC 8.9→22.2k, CRP 93.26, PaO2 52.7. CT:両側GGO→進行性両側肺胞陰影+小葉間隔壁肥厚. BAL:好中球43%. 挿管→hospice→死亡","final_diagnosis":"急性間質性肺炎(AIP)","expected_id":"D175","in_scope":True,"evidence":{"S01":"dry","S04":"at_rest","E01":"37.5_38.0","E02":"under_100","E04":"tachypnea_20_30","E05":"severe_hypoxia_under_93","E07":"crackles","L04":"bilateral_infiltrate","L01":"very_high_over_20000","L02":"high_over_10","T01":"1w_to_3w","T02":"gradual_days"},"risk_factors":{"R01":"65_plus","R02":"female"},"result":"","notes":"PaO2 52.7. WBC 22.2k. BAL好中球43%. 死亡"},
    {"id":"R392","source":"Resp Med CME 2011","pmcid":"PMC3114546","vignette":"77F DM1+PMR+高血圧. 3日前の咽頭痛+倦怠感→入院48h後に突然の呼吸困難+低酸素. P/F 89(重症ARDS!). 初回CXR正常→48h後急速な両側浸潤. HRCT:びまん性GGO+牽引性気管支拡張. Day19 VATS生検:DAD(滲出+器質化混合). mPSL 60mg q6h→35日後死亡(敗血症+AKI)","final_diagnosis":"急性間質性肺炎(AIP, 生検確認DAD)","expected_id":"D175","in_scope":True,"evidence":{"S07":"severe","S04":"at_rest","E01":"under_37.5","E07":"crackles","L04":"bilateral_infiltrate","T01":"under_3d","T02":"sudden_hours"},"risk_factors":{"R01":"65_plus","R02":"female"},"result":"","notes":"P/F 89. 初回CXR正常→48h後ARDS. VATS生検DAD確認. Day35死亡"},
    {"id":"R393","source":"JCPSP 2016","pmcid":"PMC5081432","vignette":"45F 5日間の湿性咳嗽(大量粘液痰)+呼吸困難+胸膜痛+高熱. 6ヶ月のdry eyes/mouth. 頻呼吸, SpO2 92%(RA). 白血球増多+軽度貧血. 抗SSA/SSB陽性(Sjogren). ABG:I型呼吸不全. HRCT:両側GGO+牽引性気管支拡張(下葉). 気管支生検:DAD. 挿管1週→mPSL→3週で完全回復","final_diagnosis":"急性間質性肺炎(AIP, Sjogren続発)","expected_id":"D175","in_scope":True,"evidence":{"S01":"productive","S04":"at_rest","E01":"39.0_40.0","E05":"mild_hypoxia_93_96","E07":"crackles","L04":"bilateral_infiltrate","L01":"high_10000_20000","S08":"present","T01":"3d_to_1w","T02":"gradual_days"},"risk_factors":{"R01":"40_64","R02":"female"},"result":"","notes":"Sjogren合併. DAD生検確認. 3週で完全回復"},
    {"id":"R394","source":"BMC Pulm Med 2014","pmcid":"PMC4013083","vignette":"28F 非喫煙+既往なし. 咳嗽+軽度呼吸困難+発熱. T 38.0, HR 100, RR 25, BP 103/63. チアノーゼ. ABG:PaO2 53→Day4 PaO2 32(!), pH 7.47→7.19. HRCT:両側びまん性GGO→悪化. Day5経気管支生検:DAD(滲出期). mPSL 500mg→挿管8週→Day62死亡. 剖検:DAD線維化期","final_diagnosis":"急性間質性肺炎(AIP, 生検+剖検確認DAD)","expected_id":"D175","in_scope":True,"evidence":{"S01":"dry","S04":"at_rest","E01":"37.5_38.0","E02":"100_120","E04":"tachypnea_20_30","E07":"crackles","L04":"bilateral_infiltrate","T01":"under_3d","T02":"gradual_days"},"risk_factors":{"R01":"18_39","R02":"female"},"result":"","notes":"PaO2 53→32. チアノーゼ. Day62死亡. 剖検DAD確認"},
]

for c in cases:
    suite["cases"].append(c)
with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added {len(cases)} AIP cases (R390-R394). Total: {len(suite['cases'])}")
