#!/usr/bin/env python3
"""Add bronchiolitis cases for D253."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
    suite = json.load(f)
cases = [
    {"id":"R479","source":"Case Rep 2025","pmcid":"PMC12741973","vignette":"11ヶ月F 正期産. 急性呼吸窮迫+喘鳴(呼気性, びまん性)+鼻翼呼吸+肋間/肋弓下陥没. RR 57, SpO2 91%(RA), 無熱. CRP 17, WBC 10.2k, PLT 32万. CXR:びまん性気管支症候群(浸潤なし)→左気胸合併. RSV PCR陽性","final_diagnosis":"RSV細気管支炎+自然気胸","expected_id":"D253","in_scope":True,"evidence":{"S04":"at_rest","E07":"wheezes","E04":"severe_over_30","E05":"mild_hypoxia_93_96","E01":"under_37.5","L01":"high_10000_20000","T01":"under_3d","T02":"gradual_days"},"risk_factors":{"R01":"0_1","R02":"female"},"result":"","notes":"SpO2 91%. RSV+. 自然気胸合併"},
    {"id":"R480","source":"Case Rep 2021","pmcid":"PMC8655089","vignette":"40日M 正期産. 1週間の咳嗽+嘔吐+哺乳低下+呼吸困難. HR 160, RR 52, SpO2 93%, T 37.0. 持続性乾性咳嗽+大理石様皮膚. pH 7.347, pCO2 56.6, pO2 28, Hb 13.6. CXR:正常→両側びまん性肺陰影. RSV陽性→脳症合併→死亡","final_diagnosis":"RSV細気管支炎(致死的, 脳合併症)","expected_id":"D253","in_scope":True,"evidence":{"S01":"dry","S04":"at_rest","E02":"over_120","E04":"severe_over_30","E05":"mild_hypoxia_93_96","E01":"under_37.5","S13":"present","T01":"3d_to_1w","T02":"gradual_days"},"risk_factors":{"R01":"0_1","R02":"male"},"result":"","notes":"40日齢. pCO2 56.6(II型呼吸不全). 脳症→死亡"},
    {"id":"R481","source":"Case Rep 2021","pmcid":"PMC8142759","vignette":"7日M 37週 帝王切開. 発熱38.5+頻呼吸+呼吸困難+蒼白+胸郭陥没. WBC 11.9k(PMN 59.4%)→23.2k(PMN 77.7%), CRP正常→15.2. 血培:肺炎球菌serotype3. RSV A PCR陽性. CXR:両側肺野陰影","final_diagnosis":"RSV細気管支炎+肺炎球菌敗血症","expected_id":"D253","in_scope":True,"evidence":{"S04":"at_rest","E01":"38.0_39.0","L01":"high_10000_20000","L02":"high_over_10","L09":"gram_positive","T01":"under_3d","T02":"sudden_hours"},"risk_factors":{"R01":"0_1","R02":"male"},"result":"","notes":"生後7日. RSV A + 肺炎球菌敗血症. 回復"},
    {"id":"R482","source":"Case Rep 2016","pmcid":"PMC5093859","vignette":"7ヶ月F 既往なし. 3日間の発熱(自宅max 39.8)+乾性咳嗽+喘鳴→呼吸仕事量増大. HR 126, RR 50, SpO2 97%, T 37.0, BP 95/48. 頻呼吸+肋間陥没+鼻翼呼吸. CBC/CRP正常. VBG: pH 7.33, CO2 44. CXR:両側airspace disease→縦隔気腫. RSV抗原陽性+培養確認","final_diagnosis":"RSV細気管支炎+縦隔気腫","expected_id":"D253","in_scope":True,"evidence":{"S01":"dry","S04":"at_rest","E04":"tachypnea_20_30","E02":"100_120","E01":"under_37.5","L01":"normal_4000_10000","L04":"bilateral_infiltrate","T01":"under_3d","T02":"gradual_days"},"risk_factors":{"R01":"0_1","R02":"female"},"result":"","notes":"RSV抗原+培養確認. 縦隔気腫合併"},
    {"id":"R483","source":"Case Rep 2025","pmcid":"PMC12303654","vignette":"5ヶ月F 36+1週(late preterm) 7.15kg. 6日前から湿性咳嗽+透明鼻汁→重度呼吸窮迫. RR 50→55, SpO2 98%→90%低下, 無熱. 両側喘鳴+びまん性crackles. 好中球増多, CRP 0.80(正常), ABG: pH 7.44, pO2 58(低酸素). CXR:左上葉浸潤. RSV A PCR+rhinovirus共感染","final_diagnosis":"RSV細気管支炎+肺炎(rhinovirus共感染)","expected_id":"D253","in_scope":True,"evidence":{"S01":"productive","S03":"clear_rhinorrhea","S04":"at_rest","E07":"crackles","E04":"tachypnea_20_30","E05":"mild_hypoxia_93_96","E01":"under_37.5","L04":"bilateral_infiltrate","T01":"3d_to_1w","T02":"gradual_days"},"risk_factors":{"R01":"0_1","R02":"female"},"result":"","notes":"RSV A + rhinovirus共感染. late preterm"},
]
for c in cases:
    suite["cases"].append(c)
with open(os.path.join(BASE, "real_case_test_suite.json"), "w", encoding="utf-8") as f:
    json.dump(suite, f, ensure_ascii=False, indent=2)
print(f"Added {len(cases)} cases. Total: {len(suite['cases'])}")
