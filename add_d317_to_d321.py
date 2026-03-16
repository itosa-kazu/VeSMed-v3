#!/usr/bin/env python3
"""Add D317-D321: 5 diseases."""
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

# D317 特発性肺線維症(IPF) - already D130 covers ILD/IPF? D130 is 間質性肺疾患(ILD/IPF). Skip.
# D317 肺胞蛋白症 (Pulmonary Alveolar Proteinosis)
s1["variables"].append({"id":"D317","name":"PAP","name_ja":"肺胞蛋白症(PAP)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"サーファクタント蓄積→低酸素。自己免疫型(GM-CSF Ab)/二次性(血液疾患)/先天性。全肺洗浄が治療"})
for to,r,c in [
    ("S04","PAP: 呼吸困難(80%+)",{"absent":0.08,"on_exertion":0.42,"at_rest":0.50}),
    ("S01","PAP: 咳嗽(50-60%)",{"absent":0.30,"dry":0.45,"productive":0.25}),
    ("E05","PAP: 低酸素(60-70%)",{"normal_over_96":0.20,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.45}),
    ("L04","PAP: CXR(crazy-paving/両側GGO)",{"normal":0.05,"lobar_infiltrate":0.03,"bilateral_infiltrate":0.85,"BHL":0.02,"pleural_effusion":0.03,"pneumothorax":0.02}),
    ("S07","PAP: 倦怠感",{"absent":0.15,"mild":0.40,"severe":0.45}),
    ("E07","PAP: 肺聴診(crackles)",{"clear":0.25,"crackles":0.55,"wheezes":0.10,"decreased_absent":0.10}),
    ("T01","PAP: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.25,"over_3w":0.60}),
    ("T02","PAP: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D317","PAP",to,r,c)
s3["full_cpts"]["D317"] = {"parents":["R01","R02"],"description":"PAP。30-50歳男性に多い",
    "cpt":{"0_1,male":0.0001,"0_1,female":0.0001,"1_5,male":0.0002,"1_5,female":0.0002,"6_12,male":0.0003,"6_12,female":0.0003,"13_17,male":0.0005,"13_17,female":0.0003,"18_39,male":0.002,"18_39,female":0.001,"40_64,male":0.002,"40_64,female":0.001,"65_plus,male":0.001,"65_plus,female":0.0005}}

# D318 肺塞栓症(慢性血栓塞栓性肺高血圧) CTEPH
s1["variables"].append({"id":"D318","name":"CTEPH","name_ja":"慢性血栓塞栓性肺高血圧症(CTEPH)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"急性PEの慢性化→肺動脈リモデリング→肺高血圧。労作時呼吸困難+右心不全。肺動脈内膜摘除術"})
for to,r,c in [
    ("S04","CTEPH: 呼吸困難(進行性, 100%)",{"absent":0.02,"on_exertion":0.55,"at_rest":0.43}),
    ("E36","CTEPH: 下肢浮腫(右心不全, 40-50%)",{"absent":0.40,"unilateral":0.05,"bilateral":0.55}),
    ("E05","CTEPH: 低酸素",{"normal_over_96":0.20,"mild_hypoxia_93_96":0.40,"severe_hypoxia_under_93":0.40}),
    ("L51","CTEPH: BNP上昇(右心不全)",{"not_done":0.10,"normal":0.15,"mildly_elevated":0.35,"very_high":0.40}),
    ("S07","CTEPH: 倦怠感",{"absent":0.10,"mild":0.35,"severe":0.55}),
    ("L52","CTEPH: D-dimer(軽度上昇~正常)",{"not_done":0.15,"normal":0.30,"mildly_elevated":0.40,"very_high":0.15}),
    ("T01","CTEPH: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.15,"over_3w":0.75}),
    ("T02","CTEPH: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D318","CTEPH",to,r,c)
s3["full_cpts"]["D318"] = {"parents":["R01"],"description":"CTEPH",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0001,"13_17":0.0003,"18_39":0.001,"40_64":0.002,"65_plus":0.003}}

# D319 気管支拡張症 (Bronchiectasis)
s1["variables"].append({"id":"D319","name":"bronchiectasis","name_ja":"気管支拡張症",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"気管支の不可逆的拡張。慢性湿性咳嗽+膿性痰+反復性肺炎+喀血。CF/原発性線毛機能不全"})
for to,r,c in [
    ("S01","気管支拡張: 慢性湿性咳嗽(90%+)",{"absent":0.03,"dry":0.07,"productive":0.90}),
    ("S04","気管支拡張: 呼吸困難(40-50%)",{"absent":0.35,"on_exertion":0.40,"at_rest":0.25}),
    ("E01","気管支拡張: 発熱(増悪時, 30-40%)",{"under_37.5":0.45,"37.5_38.0":0.15,"38.0_39.0":0.22,"39.0_40.0":0.13,"over_40.0":0.05}),
    ("E07","気管支拡張: crackles+wheezes",{"clear":0.08,"crackles":0.55,"wheezes":0.25,"decreased_absent":0.12}),
    ("L04","気管支拡張: CXR(気管支壁肥厚/浸潤)",{"normal":0.10,"lobar_infiltrate":0.20,"bilateral_infiltrate":0.50,"BHL":0.02,"pleural_effusion":0.10,"pneumothorax":0.08}),
    ("S44","気管支拡張: 喀血(20-30%)",{"absent":0.65,"present":0.35}),
    ("L01","気管支拡張: WBC上昇(感染増悪時)",{"low_under_4000":0.05,"normal_4000_10000":0.30,"high_10000_20000":0.40,"very_high_over_20000":0.25}),
    ("L02","気管支拡張: CRP上昇(感染増悪時)",{"normal_under_0.3":0.10,"mild_0.3_3":0.20,"moderate_3_10":0.35,"high_over_10":0.35}),
    ("T01","気管支拡張: 慢性(増悪で急性)",{"under_3d":0.15,"3d_to_1w":0.25,"1w_to_3w":0.30,"over_3w":0.30}),
    ("T02","気管支拡張: 慢性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D319","bronchiectasis",to,r,c)
s3["full_cpts"]["D319"] = {"parents":["R01"],"description":"気管支拡張症",
    "cpt":{"0_1":0.001,"1_5":0.002,"6_12":0.002,"13_17":0.002,"18_39":0.003,"40_64":0.004,"65_plus":0.005}}

# D320 過換気症候群 → already D129. Skip.
# D320 睡眠時無呼吸症候群 → too chronic.
# D320 喉頭癌 (Laryngeal Cancer)
s1["variables"].append({"id":"D320","name":"laryngeal_cancer","name_ja":"喉頭癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"嗄声(声門型, 早期発見可能)+嚥下困難+頸部腫瘤(進行)。喫煙+飲酒がリスク。扁平上皮癌が95%"})
for to,r,c in [
    ("S02","喉頭癌: 嗄声/咽頭違和感(90%+)",{"absent":0.05,"present":0.95}),
    ("S04","喉頭癌: 呼吸困難(進行, 30-40%)",{"absent":0.50,"on_exertion":0.30,"at_rest":0.20}),
    ("S07","喉頭癌: 体重減少(40-50%)",{"absent":0.35,"mild":0.35,"severe":0.30}),
    ("S01","喉頭癌: 咳嗽(20-30%)",{"absent":0.60,"dry":0.25,"productive":0.15}),
    ("T01","喉頭癌: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.15,"over_3w":0.75}),
    ("T02","喉頭癌: 緩徐",{"sudden_hours":0.03,"gradual_days":0.97}),
]: add("D320","laryngeal_cancer",to,r,c)
s3["full_cpts"]["D320"] = {"parents":["R01","R02"],"description":"喉頭癌。男性+高齢者",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0001,"13_17,female":0.0,"18_39,male":0.0005,"18_39,female":0.0001,"40_64,male":0.003,"40_64,female":0.0005,"65_plus,male":0.005,"65_plus,female":0.001}}

# D321 甲状腺乳頭癌 (Papillary Thyroid Cancer) - too chronic/asymptomatic.
# D321 原発性アルドステロン症 (Primary Aldosteronism)
s1["variables"].append({"id":"D321","name":"primary_aldosteronism","name_ja":"原発性アルドステロン症",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"治療抵抗性高血圧の5-10%。低K血症+高血圧。アルドステロン/レニン比>200で疑い。副腎腺腫/過形成"})
for to,r,c in [
    ("E38","原発性アルドステロン症: 高血圧(定義的)",{"normal_under_140":0.03,"elevated_140_180":0.40,"crisis_over_180":0.57}),
    ("L44","原発性アルドステロン症: 低K血症→other",{"normal":0.30,"hyponatremia":0.05,"hyperkalemia":0.02,"other":0.63}),
    ("S05","原発性アルドステロン症: 頭痛(高血圧, 40-50%)",{"absent":0.40,"mild":0.35,"severe":0.25}),
    ("S07","原発性アルドステロン症: 倦怠感/筋力低下(低K, 30-40%)",{"absent":0.45,"mild":0.35,"severe":0.20}),
    ("T01","原発性アルドステロン症: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.15,"over_3w":0.75}),
    ("T02","原発性アルドステロン症: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D321","primary_aldosteronism",to,r,c)
s3["full_cpts"]["D321"] = {"parents":["R01"],"description":"原発性アルドステロン症",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0001,"13_17":0.0003,"18_39":0.001,"40_64":0.003,"65_plus":0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 321 diseases")
