#!/usr/bin/env python3
"""Add D262-D266: 5 diseases."""
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

# D262 伝染性膿痂疹 (Impetigo)
s1["variables"].append({"id":"D262","name":"impetigo","name_ja":"伝染性膿痂疹(とびひ)",
    "category":"disease","states":["no","yes"],"severity":"low",
    "note":"GAS/S.aureus。蜂蜜色痂皮(非水疱型)/水疱(水疱型)。小児に多い。PSGN合併リスク"})
for to,r,c in [
    ("E12","膿痂疹: 皮疹(痂皮/水疱)",{"normal":0.02,"localized_erythema_warmth_swelling":0.10,"petechiae_purpura":0.01,"maculopapular_rash":0.05,"vesicular_dermatomal":0.02,"diffuse_erythroderma":0.01,"purpura":0.01,"vesicle_bulla":0.70,"skin_necrosis":0.08}),
    ("E01","膿痂疹: 発熱(軽度, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.18,"38.0_39.0":0.15,"39.0_40.0":0.05,"over_40.0":0.02}),
    ("L01","膿痂疹: WBC(正常~軽度)",{"low_under_4000":0.03,"normal_4000_10000":0.55,"high_10000_20000":0.32,"very_high_over_20000":0.10}),
    ("T01","膿痂疹: 急性~亜急性",{"under_3d":0.15,"3d_to_1w":0.40,"1w_to_3w":0.35,"over_3w":0.10}),
    ("T02","膿痂疹: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D262","impetigo",to,r,c)
s3["full_cpts"]["D262"] = {"parents":["R01"],"description":"膿痂疹",
    "cpt":{"0_1":0.005,"1_5":0.008,"6_12":0.005,"13_17":0.002,"18_39":0.001,"40_64":0.0005,"65_plus":0.0005}}

# D263 溶連菌咽頭炎 (GAS Pharyngitis) - D09 already covers 急性咽頭扁桃炎.
# But GAS-specific is different. Actually D09 is generic pharyngitis. Let's add GAS-specific.
# Actually let me pick something else. D09 covers this.
# D263 百日咳 - already D46. Skip.
# D263 アデノウイルス咽頭結膜熱(プール熱) → D181 is adenovirus. Skip.
# D263 マイコプラズマ肺炎 → already covered in D05 community pneumonia? No, D05 is generic.
# D263 マイコプラズマ肺炎 (Mycoplasma Pneumonia)
s1["variables"].append({"id":"D263","name":"mycoplasma_pneumonia","name_ja":"マイコプラズマ肺炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"若年成人/学童に多い。乾性咳嗽(頑固)+微熱+倦怠感。聴診所見乏しい(walking pneumonia)。CXR:斑状浸潤"})
for to,r,c in [
    ("S01","マイコプラズマ: 頑固な乾性咳嗽(90%+)",{"absent":0.03,"dry":0.80,"productive":0.17}),
    ("E01","マイコプラズマ: 発熱(中等度, 80%+)",{"under_37.5":0.08,"37.5_38.0":0.15,"38.0_39.0":0.40,"39.0_40.0":0.28,"over_40.0":0.09}),
    ("S07","マイコプラズマ: 倦怠感(60-70%)",{"absent":0.20,"mild":0.45,"severe":0.35}),
    ("S05","マイコプラズマ: 頭痛(40-50%)",{"absent":0.40,"mild":0.35,"severe":0.25}),
    ("E07","マイコプラズマ: 肺聴診(所見乏しいことが多い)",{"clear":0.35,"crackles":0.40,"wheezes":0.15,"decreased_absent":0.10}),
    ("L04","マイコプラズマ: CXR(斑状浸潤/GGO)",{"normal":0.10,"lobar_infiltrate":0.15,"bilateral_infiltrate":0.60,"BHL":0.02,"pleural_effusion":0.08,"pneumothorax":0.05}),
    ("L01","マイコプラズマ: WBC(正常~軽度)",{"low_under_4000":0.05,"normal_4000_10000":0.50,"high_10000_20000":0.35,"very_high_over_20000":0.10}),
    ("L02","マイコプラズマ: CRP上昇(中等度)",{"normal_under_0.3":0.08,"mild_0.3_3":0.20,"moderate_3_10":0.40,"high_over_10":0.32}),
    ("S02","マイコプラズマ: 咽頭痛(30-40%)",{"absent":0.55,"present":0.45}),
    ("S04","マイコプラズマ: 呼吸困難(20-30%)",{"absent":0.60,"on_exertion":0.25,"at_rest":0.15}),
    ("T01","マイコプラズマ: 急性~亜急性(1-3週)",{"under_3d":0.10,"3d_to_1w":0.30,"1w_to_3w":0.45,"over_3w":0.15}),
    ("T02","マイコプラズマ: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D263","mycoplasma_pneumonia",to,r,c)
s3["full_cpts"]["D263"] = {"parents":["R01"],"description":"マイコプラズマ肺炎。若年成人/学童",
    "cpt":{"0_1":0.002,"1_5":0.004,"6_12":0.008,"13_17":0.006,"18_39":0.005,"40_64":0.003,"65_plus":0.002}}

# D264 クラミジア肺炎 (Chlamydia pneumoniae)
s1["variables"].append({"id":"D264","name":"chlamydia_pneumonia","name_ja":"クラミジア肺炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"C. pneumoniae。嗄声+咽頭痛→遷延性咳嗽。マイコプラズマと類似だが嗄声が特徴的"})
for to,r,c in [
    ("S01","クラミジア肺炎: 咳嗽(遷延性, 80%+)",{"absent":0.05,"dry":0.60,"productive":0.35}),
    ("E01","クラミジア肺炎: 発熱(60-70%)",{"under_37.5":0.20,"37.5_38.0":0.20,"38.0_39.0":0.35,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("S02","クラミジア肺炎: 咽頭痛(嗄声, 40-50%)",{"absent":0.40,"present":0.60}),
    ("E07","クラミジア肺炎: 肺聴診(crackles)",{"clear":0.25,"crackles":0.50,"wheezes":0.15,"decreased_absent":0.10}),
    ("L04","クラミジア肺炎: CXR(両側浸潤/斑状)",{"normal":0.10,"lobar_infiltrate":0.15,"bilateral_infiltrate":0.60,"BHL":0.02,"pleural_effusion":0.08,"pneumothorax":0.05}),
    ("S07","クラミジア肺炎: 倦怠感",{"absent":0.20,"mild":0.45,"severe":0.35}),
    ("L01","クラミジア肺炎: WBC(正常)",{"low_under_4000":0.05,"normal_4000_10000":0.55,"high_10000_20000":0.30,"very_high_over_20000":0.10}),
    ("L02","クラミジア肺炎: CRP上昇",{"normal_under_0.3":0.10,"mild_0.3_3":0.25,"moderate_3_10":0.35,"high_over_10":0.30}),
    ("T01","クラミジア肺炎: 亜急性(2-4週)",{"under_3d":0.05,"3d_to_1w":0.20,"1w_to_3w":0.50,"over_3w":0.25}),
    ("T02","クラミジア肺炎: 亜急性",{"sudden_hours":0.08,"gradual_days":0.92}),
]: add("D264","chlamydia_pneumonia",to,r,c)
s3["full_cpts"]["D264"] = {"parents":["R01"],"description":"クラミジア肺炎",
    "cpt":{"0_1":0.001,"1_5":0.002,"6_12":0.004,"13_17":0.003,"18_39":0.003,"40_64":0.003,"65_plus":0.004}}

# D265 インフルエンザ菌性肺炎 (H. influenzae Pneumonia)
s1["variables"].append({"id":"D265","name":"h_influenzae_pneumonia","name_ja":"インフルエンザ菌性肺炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"COPD/高齢者に多い。急性発症の発熱+湿性咳嗽+膿性痰。グラム陰性短桿菌"})
for to,r,c in [
    ("S01","H.flu肺炎: 湿性咳嗽(80%+)",{"absent":0.05,"dry":0.15,"productive":0.80}),
    ("E01","H.flu肺炎: 高熱(80%+)",{"under_37.5":0.08,"37.5_38.0":0.10,"38.0_39.0":0.30,"39.0_40.0":0.32,"over_40.0":0.20}),
    ("E07","H.flu肺炎: crackles",{"clear":0.05,"crackles":0.75,"wheezes":0.10,"decreased_absent":0.10}),
    ("L04","H.flu肺炎: CXR(肺葉浸潤)",{"normal":0.05,"lobar_infiltrate":0.50,"bilateral_infiltrate":0.30,"BHL":0.01,"pleural_effusion":0.10,"pneumothorax":0.04}),
    ("S04","H.flu肺炎: 呼吸困難(60-70%)",{"absent":0.20,"on_exertion":0.35,"at_rest":0.45}),
    ("E04","H.flu肺炎: 頻呼吸",{"normal_under_20":0.10,"tachypnea_20_30":0.40,"severe_over_30":0.50}),
    ("E05","H.flu肺炎: 低酸素",{"normal_over_96":0.20,"mild_hypoxia_93_96":0.40,"severe_hypoxia_under_93":0.40}),
    ("L01","H.flu肺炎: WBC上昇",{"low_under_4000":0.05,"normal_4000_10000":0.15,"high_10000_20000":0.45,"very_high_over_20000":0.35}),
    ("L02","H.flu肺炎: CRP著高",{"normal_under_0.3":0.03,"mild_0.3_3":0.07,"moderate_3_10":0.25,"high_over_10":0.65}),
    ("L09","H.flu肺炎: 血培(グラム陰性)",{"not_done_or_pending":0.15,"negative":0.45,"gram_positive":0.05,"gram_negative":0.35}),
    ("E02","H.flu肺炎: 頻脈",{"under_100":0.10,"100_120":0.40,"over_120":0.50}),
    ("T01","H.flu肺炎: 急性",{"under_3d":0.40,"3d_to_1w":0.40,"1w_to_3w":0.15,"over_3w":0.05}),
    ("T02","H.flu肺炎: 急性",{"sudden_hours":0.30,"gradual_days":0.70}),
]: add("D265","h_influenzae_pneumonia",to,r,c)
s3["full_cpts"]["D265"] = {"parents":["R01"],"description":"インフルエンザ菌性肺炎。高齢者/COPD",
    "cpt":{"0_1":0.002,"1_5":0.002,"6_12":0.001,"13_17":0.001,"18_39":0.002,"40_64":0.003,"65_plus":0.006}}

# D266 肺炎球菌性肺炎 (Pneumococcal Pneumonia)
s1["variables"].append({"id":"D266","name":"pneumococcal_pneumonia","name_ja":"肺炎球菌性肺炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"S. pneumoniae。市中肺炎の最多原因菌。突然の高熱+悪寒戦慄+膿性痰+胸膜痛。典型的大葉性肺炎"})
for to,r,c in [
    ("S01","肺炎球菌: 膿性痰(70-80%)",{"absent":0.08,"dry":0.12,"productive":0.80}),
    ("E01","肺炎球菌: 高熱+悪寒(90%+)",{"under_37.5":0.03,"37.5_38.0":0.07,"38.0_39.0":0.25,"39.0_40.0":0.35,"over_40.0":0.30}),
    ("S09","肺炎球菌: 悪寒戦慄(70-80%)",{"absent":0.15,"present":0.85}),
    ("E07","肺炎球菌: crackles(限局性)",{"clear":0.05,"crackles":0.80,"wheezes":0.05,"decreased_absent":0.10}),
    ("L04","肺炎球菌: CXR(大葉性浸潤)",{"normal":0.03,"lobar_infiltrate":0.65,"bilateral_infiltrate":0.15,"BHL":0.01,"pleural_effusion":0.12,"pneumothorax":0.04}),
    ("S04","肺炎球菌: 呼吸困難",{"absent":0.15,"on_exertion":0.35,"at_rest":0.50}),
    ("E04","肺炎球菌: 頻呼吸",{"normal_under_20":0.08,"tachypnea_20_30":0.37,"severe_over_30":0.55}),
    ("E05","肺炎球菌: 低酸素",{"normal_over_96":0.15,"mild_hypoxia_93_96":0.40,"severe_hypoxia_under_93":0.45}),
    ("L01","肺炎球菌: WBC著増(好中球左方移動)",{"low_under_4000":0.05,"normal_4000_10000":0.10,"high_10000_20000":0.40,"very_high_over_20000":0.45}),
    ("L02","肺炎球菌: CRP著高",{"normal_under_0.3":0.02,"mild_0.3_3":0.05,"moderate_3_10":0.20,"high_over_10":0.73}),
    ("L03","肺炎球菌: PCT上昇(細菌性)",{"not_done":0.15,"low_under_0.25":0.05,"gray_0.25_0.5":0.10,"high_over_0.5":0.70}),
    ("L09","肺炎球菌: 血培(グラム陽性球菌)",{"not_done_or_pending":0.10,"negative":0.45,"gram_positive":0.40,"gram_negative":0.05}),
    ("E02","肺炎球菌: 頻脈",{"under_100":0.05,"100_120":0.35,"over_120":0.60}),
    ("S21","肺炎球菌: 胸膜痛(30-40%)",{"absent":0.50,"burning":0.03,"sharp":0.35,"pressure":0.08,"tearing":0.04}),
    ("T01","肺炎球菌: 急性",{"under_3d":0.45,"3d_to_1w":0.40,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","肺炎球菌: 急性",{"sudden_hours":0.45,"gradual_days":0.55}),
]: add("D266","pneumococcal_pneumonia",to,r,c)
s3["full_cpts"]["D266"] = {"parents":["R01"],"description":"肺炎球菌性肺炎",
    "cpt":{"0_1":0.004,"1_5":0.003,"6_12":0.002,"13_17":0.002,"18_39":0.004,"40_64":0.005,"65_plus":0.008}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 266 diseases")
