#!/usr/bin/env python3
"""Add D252-D256: 5 diseases following add-diseases skill workflow."""
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

# D252 川崎病 (Kawasaki Disease)
s1["variables"].append({"id":"D252","name":"kawasaki_disease","name_ja":"川崎病",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"5日以上の発熱+5主要症状のうち4つ: 両側結膜充血/口唇紅潮・苺舌/多形性発疹/四肢末端変化/非化膿性頸部リンパ節腫脹。冠動脈瘤リスク"})
for to,r,c in [
    ("E01","川崎: 高熱5日以上(定義的)",{"under_37.5":0.02,"37.5_38.0":0.03,"38.0_39.0":0.20,"39.0_40.0":0.40,"over_40.0":0.35}),
    ("E12","川崎: 多形性発疹(紅斑+丘疹)",{"normal":0.08,"localized_erythema_warmth_swelling":0.05,"petechiae_purpura":0.02,"maculopapular_rash":0.60,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.15,"purpura":0.02,"vesicle_bulla":0.02,"skin_necrosis":0.05}),
    ("E02","川崎: 頻脈(高熱)",{"under_100":0.05,"100_120":0.35,"over_120":0.60}),
    ("S09","川崎: 易刺激性(特徴的)",{"absent":0.20,"present":0.80}),
    ("S08","川崎: 関節痛(30-40%)",{"absent":0.55,"present":0.45}),
    ("L01","川崎: WBC上昇(好中球優位)",{"low_under_4000":0.02,"normal_4000_10000":0.10,"high_10000_20000":0.45,"very_high_over_20000":0.43}),
    ("L02","川崎: CRP著高",{"normal_under_0.3":0.02,"mild_0.3_3":0.05,"moderate_3_10":0.25,"high_over_10":0.68}),
    ("L14","川崎: 血小板増多(回復期400k+)",{"normal":0.30,"left_shift":0.05,"atypical_lymphocytes":0.02,"thrombocytopenia":0.08,"eosinophilia":0.00,"lymphocyte_predominant":0.55}),
    ("L11","川崎: 肝酵素上昇(30-40%)",{"normal":0.50,"mild_elevated":0.35,"very_high":0.15}),
    ("S13","川崎: 嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("S14","川崎: 下痢(20-30%)",{"absent":0.65,"watery":0.30,"bloody":0.05}),
    ("T01","川崎: 急性(5日以上の発熱)",{"under_3d":0.05,"3d_to_1w":0.40,"1w_to_3w":0.45,"over_3w":0.10}),
    ("T02","川崎: 急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D252","kawasaki_disease",to,r,c)
s3["full_cpts"]["D252"] = {"parents":["R01"],"description":"川崎病。乳幼児に圧倒的に多い",
    "cpt":{"0_1":0.008,"1_5":0.010,"6_12":0.003,"13_17":0.001,"18_39":0.0005,"40_64":0.0002,"65_plus":0.0001}}

# D253 急性細気管支炎 (Acute Bronchiolitis)
s1["variables"].append({"id":"D253","name":"acute_bronchiolitis","name_ja":"急性細気管支炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"RSV等。2歳未満の乳児。鼻汁→咳嗽→喘鳴→呼吸困難。多呼吸+陥没呼吸+SpO2低下"})
for to,r,c in [
    ("S01","細気管支炎: 咳嗽(90%+)",{"absent":0.05,"dry":0.40,"productive":0.55}),
    ("S04","細気管支炎: 呼吸困難(60-80%)",{"absent":0.10,"on_exertion":0.25,"at_rest":0.65}),
    ("E07","細気管支炎: 肺聴診(wheezes+crackles)",{"clear":0.05,"crackles":0.30,"wheezes":0.55,"decreased_absent":0.10}),
    ("E04","細気管支炎: 多呼吸",{"normal_under_20":0.10,"tachypnea_20_30":0.35,"severe_over_30":0.55}),
    ("E05","細気管支炎: SpO2低下(40-60%)",{"normal_over_96":0.30,"mild_hypoxia_93_96":0.40,"severe_hypoxia_under_93":0.30}),
    ("E01","細気管支炎: 発熱(50-70%)",{"under_37.5":0.25,"37.5_38.0":0.20,"38.0_39.0":0.30,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("S03","細気管支炎: 鼻汁(前駆, 80%+)",{"absent":0.10,"clear_rhinorrhea":0.70,"purulent_rhinorrhea":0.20}),
    ("E02","細気管支炎: 頻脈",{"under_100":0.10,"100_120":0.35,"over_120":0.55}),
    ("L01","細気管支炎: WBC(正常~軽度上昇)",{"low_under_4000":0.05,"normal_4000_10000":0.50,"high_10000_20000":0.35,"very_high_over_20000":0.10}),
    ("T01","細気管支炎: 急性",{"under_3d":0.30,"3d_to_1w":0.50,"1w_to_3w":0.18,"over_3w":0.02}),
    ("T02","細気管支炎: 急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D253","acute_bronchiolitis",to,r,c)
s3["full_cpts"]["D253"] = {"parents":["R01"],"description":"細気管支炎。2歳未満",
    "cpt":{"0_1":0.015,"1_5":0.005,"6_12":0.001,"13_17":0.0003,"18_39":0.0001,"40_64":0.0001,"65_plus":0.0001}}

# D254 クループ (Croup / Acute Laryngotracheitis)
s1["variables"].append({"id":"D254","name":"croup","name_ja":"クループ(急性喉頭気管炎)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"パラインフルエンザ等。6ヶ月~3歳。犬吠様咳嗽+嗄声+吸気性喘鳴。夜間増悪。Westleyスコア"})
for to,r,c in [
    ("S01","クループ: 犬吠様咳嗽(90%+)",{"absent":0.03,"dry":0.90,"productive":0.07}),
    ("S04","クループ: 呼吸困難(50-70%)",{"absent":0.20,"on_exertion":0.30,"at_rest":0.50}),
    ("E01","クループ: 発熱(50-70%)",{"under_37.5":0.20,"37.5_38.0":0.20,"38.0_39.0":0.35,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("E04","クループ: 多呼吸(中等度以上)",{"normal_under_20":0.25,"tachypnea_20_30":0.40,"severe_over_30":0.35}),
    ("S03","クループ: 鼻汁(前駆URI)",{"absent":0.20,"clear_rhinorrhea":0.60,"purulent_rhinorrhea":0.20}),
    ("E02","クループ: 頻脈",{"under_100":0.15,"100_120":0.45,"over_120":0.40}),
    ("L01","クループ: WBC(正常~軽度)",{"low_under_4000":0.05,"normal_4000_10000":0.55,"high_10000_20000":0.30,"very_high_over_20000":0.10}),
    ("L04","クループ: CXR(steeple sign/正常)",{"normal":0.60,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.05,"BHL":0.01,"pleural_effusion":0.02,"pneumothorax":0.30}),
    ("T01","クループ: 急性(2-5日)",{"under_3d":0.40,"3d_to_1w":0.45,"1w_to_3w":0.13,"over_3w":0.02}),
    ("T02","クループ: 急性",{"sudden_hours":0.35,"gradual_days":0.65}),
]: add("D254","croup",to,r,c)
s3["full_cpts"]["D254"] = {"parents":["R01"],"description":"クループ。6月~3歳",
    "cpt":{"0_1":0.010,"1_5":0.008,"6_12":0.002,"13_17":0.0005,"18_39":0.0001,"40_64":0.0001,"65_plus":0.0001}}

# D255 熱性痙攣 (Febrile Seizure)
s1["variables"].append({"id":"D255","name":"febrile_seizure","name_ja":"熱性痙攣",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"6ヶ月~5歳。発熱時の全身性強直間代痙攣(<15分)。単純型/複雑型。良性だが初回は髄膜炎除外必要"})
for to,r,c in [
    ("S42","熱性痙攣: 痙攣(定義的)",{"absent":0.02,"present":0.98}),
    ("E01","熱性痙攣: 高熱(定義的, 38℃以上)",{"under_37.5":0.02,"37.5_38.0":0.05,"38.0_39.0":0.25,"39.0_40.0":0.40,"over_40.0":0.28}),
    ("E16","熱性痙攣: 意識(発作後一過性傾眠, 通常30分以内回復)",{"normal":0.40,"confused":0.45,"obtunded":0.15}),
    ("E02","熱性痙攣: 頻脈(発熱)",{"under_100":0.05,"100_120":0.35,"over_120":0.60}),
    ("S03","熱性痙攣: 鼻汁(URI先行, 60-70%)",{"absent":0.25,"clear_rhinorrhea":0.55,"purulent_rhinorrhea":0.20}),
    ("S01","熱性痙攣: 咳嗽(URI先行)",{"absent":0.35,"dry":0.40,"productive":0.25}),
    ("L01","熱性痙攣: WBC(感染による上昇)",{"low_under_4000":0.05,"normal_4000_10000":0.30,"high_10000_20000":0.40,"very_high_over_20000":0.25}),
    ("T01","熱性痙攣: 急性",{"under_3d":0.70,"3d_to_1w":0.25,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","熱性痙攣: 急性(発熱初日に多い)",{"sudden_hours":0.65,"gradual_days":0.35}),
]: add("D255","febrile_seizure",to,r,c)
s3["full_cpts"]["D255"] = {"parents":["R01"],"description":"熱性痙攣。6月~5歳",
    "cpt":{"0_1":0.010,"1_5":0.012,"6_12":0.002,"13_17":0.0005,"18_39":0.0001,"40_64":0.0001,"65_plus":0.0001}}

# D256 腸回転異常症/中腸軸捻転 (Midgut Volvulus)
s1["variables"].append({"id":"D256","name":"midgut_volvulus","name_ja":"腸回転異常症(中腸軸捻転)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"先天性腸回転異常→Ladd靭帯/中腸軸捻転。新生児~乳児に多い。胆汁性嘔吐+腹部膨満+血便。緊急手術"})
for to,r,c in [
    ("S13","中腸軸捻転: 胆汁性嘔吐(90%+)",{"absent":0.05,"present":0.95}),
    ("S12","中腸軸捻転: 腹痛/腹部膨満",{"absent":0.10,"epigastric":0.05,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.05,"diffuse":0.65}),
    ("S14","中腸軸捻転: 血便(腸管虚血, 30-50%)",{"absent":0.40,"watery":0.15,"bloody":0.45}),
    ("E03","中腸軸捻転: 低血圧(ショック)",{"normal_over_90":0.30,"hypotension_under_90":0.70}),
    ("E02","中腸軸捻転: 頻脈",{"under_100":0.05,"100_120":0.30,"over_120":0.65}),
    ("L01","中腸軸捻転: WBC上昇(壊死時)",{"low_under_4000":0.05,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.25}),
    ("L16","中腸軸捻転: LDH上昇(腸管虚血)",{"normal":0.20,"elevated":0.80}),
    ("T01","中腸軸捻転: 超急性",{"under_3d":0.85,"3d_to_1w":0.12,"1w_to_3w":0.02,"over_3w":0.01}),
    ("T02","中腸軸捻転: 急性",{"sudden_hours":0.75,"gradual_days":0.25}),
]: add("D256","midgut_volvulus",to,r,c)
s3["full_cpts"]["D256"] = {"parents":["R01"],"description":"中腸軸捻転。新生児~乳児",
    "cpt":{"0_1":0.005,"1_5":0.002,"6_12":0.0005,"13_17":0.0002,"18_39":0.0001,"40_64":0.0001,"65_plus":0.0001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 256 diseases")
