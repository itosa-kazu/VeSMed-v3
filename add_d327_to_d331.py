#!/usr/bin/env python3
"""Add D327-D331: 5 diseases."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]
existing = {(e["from"],e["to"]) for e in s2["edges"]}
def add(did, dname, to, reason, cpt):
    if (did,to) in existing: return
    if to not in n: return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt

# D327 大動脈弁狭窄症 (Aortic Stenosis)
s1["variables"].append({"id":"D327","name":"aortic_stenosis","name_ja":"大動脈弁狭窄症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"大動脈弁石灰化→狭窄。三徴:狭心症+失神+心不全。収縮期駆出性雑音(頸部放散)。高齢者に多い"})
for to,r,c in [
    ("S04","大動脈弁狭窄: 呼吸困難(心不全, 50-60%)",{"absent":0.25,"on_exertion":0.50,"at_rest":0.25}),
    ("S05","大動脈弁狭窄: 失神/めまい(30-40%)",{"absent":0.45,"mild":0.30,"severe":0.25}),
    ("S07","大動脈弁狭窄: 倦怠感(40-50%)",{"absent":0.30,"mild":0.40,"severe":0.30}),
    ("E36","大動脈弁狭窄: 下肢浮腫(心不全, 30-40%)",{"absent":0.50,"unilateral":0.05,"bilateral":0.45}),
    ("L51","大動脈弁狭窄: BNP上昇(心不全時)",{"not_done":0.15,"normal":0.20,"mildly_elevated":0.35,"very_high":0.30}),
    ("E02","大動脈弁狭窄: 徐脈~正常",{"under_100":0.60,"100_120":0.30,"over_120":0.10}),
    ("T01","大動脈弁狭窄: 慢性(急性増悪あり)",{"under_3d":0.10,"3d_to_1w":0.15,"1w_to_3w":0.20,"over_3w":0.55}),
    ("T02","大動脈弁狭窄: 緩徐",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D327","aortic_stenosis",to,r,c)
s3["full_cpts"]["D327"] = {"parents":["R01"],"description":"大動脈弁狭窄症。高齢者",
    "cpt":{"0_1":0.0002,"1_5":0.0002,"6_12":0.0003,"13_17":0.0005,"18_39":0.001,"40_64":0.003,"65_plus":0.008}}

# D328 ARDS (急性呼吸窮迫症候群)
s1["variables"].append({"id":"D328","name":"ARDS","name_ja":"急性呼吸窮迫症候群(ARDS)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"肺胞上皮/内皮障害→非心原性肺水腫。敗血症/肺炎/外傷/膵炎が原因。P/F比≤300。Berlin分類"})
for to,r,c in [
    ("S04","ARDS: 呼吸困難(定義的, 100%)",{"absent":0.01,"on_exertion":0.09,"at_rest":0.90}),
    ("E05","ARDS: 重度低酸素(定義的)",{"normal_over_96":0.02,"mild_hypoxia_93_96":0.15,"severe_hypoxia_under_93":0.83}),
    ("E02","ARDS: 頻脈(80%+)",{"under_100":0.10,"100_120":0.30,"over_120":0.60}),
    ("E01","ARDS: 発熱(原因疾患, 70-80%)",{"under_37.5":0.15,"37.5_38.0":0.10,"38.0_39.0":0.25,"39.0_40.0":0.30,"over_40.0":0.20}),
    ("L04","ARDS: CXR(両側浸潤影, 定義的)",{"normal":0.01,"lobar_infiltrate":0.04,"bilateral_infiltrate":0.90,"BHL":0.01,"pleural_effusion":0.03,"pneumothorax":0.01}),
    ("E07","ARDS: 肺聴診(crackles)",{"clear":0.05,"crackles":0.75,"wheezes":0.10,"decreased_absent":0.10}),
    ("L01","ARDS: WBC上昇(感染原因)",{"low_under_4000":0.08,"normal_4000_10000":0.15,"high_10000_20000":0.40,"very_high_over_20000":0.37}),
    ("L02","ARDS: CRP高度上昇",{"normal_under_0.3":0.03,"mild_0.3_3":0.07,"moderate_3_10":0.25,"high_over_10":0.65}),
    ("T01","ARDS: 急性(72h以内)",{"under_3d":0.65,"3d_to_1w":0.25,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","ARDS: 急性",{"sudden_hours":0.55,"gradual_days":0.45}),
]: add("D328","ARDS",to,r,c)
s3["full_cpts"]["D328"] = {"parents":["R01"],"description":"ARDS",
    "cpt":{"0_1":0.001,"1_5":0.001,"6_12":0.0005,"13_17":0.001,"18_39":0.002,"40_64":0.003,"65_plus":0.004}}

# D329 骨髄炎 (Osteomyelitis)
s1["variables"].append({"id":"D329","name":"osteomyelitis","name_ja":"骨髄炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"骨の細菌感染。小児:血行性(長管骨骨幹端)、成人:開放骨折/糖尿病性足部。発熱+局所疼痛+腫脹。黄色ブドウ球菌が最多"})
for to,r,c in [
    ("E01","骨髄炎: 発熱(60-70%)",{"under_37.5":0.20,"37.5_38.0":0.15,"38.0_39.0":0.30,"39.0_40.0":0.25,"over_40.0":0.10}),
    ("S15","骨髄炎: 局所骨痛(90%+)",{"absent":0.05,"present":0.95}),
    ("L01","骨髄炎: WBC上昇(60-70%)",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.27}),
    ("L02","骨髄炎: CRP/ESR上昇(90%+)",{"normal_under_0.3":0.05,"mild_0.3_3":0.10,"moderate_3_10":0.35,"high_over_10":0.50}),
    ("S07","骨髄炎: 倦怠感(40-50%)",{"absent":0.35,"mild":0.35,"severe":0.30}),
    ("T01","骨髄炎: 亜急性~慢性",{"under_3d":0.15,"3d_to_1w":0.25,"1w_to_3w":0.30,"over_3w":0.30}),
    ("T02","骨髄炎: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D329","osteomyelitis",to,r,c)
s3["full_cpts"]["D329"] = {"parents":["R01"],"description":"骨髄炎。小児+高齢者/糖尿病",
    "cpt":{"0_1":0.001,"1_5":0.002,"6_12":0.002,"13_17":0.001,"18_39":0.001,"40_64":0.002,"65_plus":0.003}}

# D330 横紋筋融解症 (Rhabdomyolysis)
s1["variables"].append({"id":"D330","name":"rhabdomyolysis","name_ja":"横紋筋融解症",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"骨格筋壊死→CK大量放出→ミオグロビン尿→AKI。外傷/圧挫/薬剤/過度運動/横紋筋/感染が原因。茶褐色尿が特徴的"})
for to,r,c in [
    ("S15","横紋筋融解: 筋痛/腰背部痛(80%+)",{"absent":0.10,"present":0.90}),
    ("S07","横紋筋融解: 倦怠感/筋力低下(70-80%)",{"absent":0.10,"mild":0.25,"severe":0.65}),
    ("L55","横紋筋融解: AKI(30-50%)",{"normal":0.30,"mild_elevated":0.30,"high_AKI":0.40}),
    ("L11","横紋筋融解: AST上昇(CK連動, 80%+)",{"normal":0.05,"mild_elevated":0.20,"very_high":0.75}),
    ("S13","横紋筋融解: 嘔気嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("E01","横紋筋融解: 発熱(30-40%)",{"under_37.5":0.50,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.12,"over_40.0":0.03}),
    ("E02","横紋筋融解: 頻脈(脱水/ショック, 40-50%)",{"under_100":0.35,"100_120":0.35,"over_120":0.30}),
    ("L44","横紋筋融解: 高K血症(30-40%)",{"normal":0.40,"hyponatremia":0.05,"hyperkalemia":0.45,"other":0.10}),
    ("T01","横紋筋融解: 急性",{"under_3d":0.55,"3d_to_1w":0.30,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","横紋筋融解: 急性",{"sudden_hours":0.45,"gradual_days":0.55}),
]: add("D330","rhabdomyolysis",to,r,c)
s3["full_cpts"]["D330"] = {"parents":["R01"],"description":"横紋筋融解症",
    "cpt":{"0_1":0.0003,"1_5":0.0005,"6_12":0.001,"13_17":0.002,"18_39":0.003,"40_64":0.002,"65_plus":0.002}}

# D331 脂肪塞栓症候群 (Fat Embolism Syndrome)
s1["variables"].append({"id":"D331","name":"fat_embolism","name_ja":"脂肪塞栓症候群",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"長管骨骨折後12-72hに発症。古典的三徴:呼吸困難+意識障害+点状出血。低酸素+肺浸潤+血小板減少"})
for to,r,c in [
    ("S04","脂肪塞栓: 呼吸困難(95%+)",{"absent":0.03,"on_exertion":0.12,"at_rest":0.85}),
    ("E05","脂肪塞栓: 低酸素(90%+)",{"normal_over_96":0.05,"mild_hypoxia_93_96":0.20,"severe_hypoxia_under_93":0.75}),
    ("E16","脂肪塞栓: 意識障害(60-80%)",{"normal":0.15,"confused":0.40,"obtunded":0.45}),
    ("S44","脂肪塞栓: 点状出血(20-50%)",{"absent":0.50,"present":0.50}),
    ("E02","脂肪塞栓: 頻脈(80%+)",{"under_100":0.10,"100_120":0.30,"over_120":0.60}),
    ("E01","脂肪塞栓: 発熱(50-60%)",{"under_37.5":0.30,"37.5_38.0":0.15,"38.0_39.0":0.25,"39.0_40.0":0.20,"over_40.0":0.10}),
    ("L04","脂肪塞栓: CXR(両側浸潤/snow storm)",{"normal":0.10,"lobar_infiltrate":0.05,"bilateral_infiltrate":0.75,"BHL":0.02,"pleural_effusion":0.05,"pneumothorax":0.03}),
    ("T01","脂肪塞栓: 急性(外傷後12-72h)",{"under_3d":0.80,"3d_to_1w":0.15,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","脂肪塞栓: 急性",{"sudden_hours":0.60,"gradual_days":0.40}),
]: add("D331","fat_embolism",to,r,c)
s3["full_cpts"]["D331"] = {"parents":["R01"],"description":"脂肪塞栓症候群。長管骨骨折後",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0005,"13_17":0.002,"18_39":0.003,"40_64":0.002,"65_plus":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 331 diseases")
