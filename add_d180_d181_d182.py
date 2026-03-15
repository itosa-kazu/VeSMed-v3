#!/usr/bin/env python3
"""Add D180 Sigmoid Volvulus + D181 Adenovirus infection + D182 Scarlet Fever."""
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
    if (did, to) in existing: return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did, to))
    n[to]["parent_effects"][did] = cpt

# D180 S状結腸捻転
s1["variables"].append({"id":"D180","name":"sigmoid_volvulus","name_ja":"S状結腸捻転",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"S状結腸の軸捻転→閉塞→虚血。高齢者/施設入所者/便秘歴。腹部膨満+便秘+嘔吐。X線coffee bean sign"})
for to,reason,cpt in [
    ("S12","S状結腸捻転: 腹痛(LLQ~びまん性)",{"absent":0.05,"epigastric":0.03,"RUQ":0.02,"RLQ":0.05,"LLQ":0.40,"suprapubic":0.05,"diffuse":0.40}),
    ("S13","S状結腸捻転: 嘔吐(50-70%)",{"absent":0.30,"present":0.70}),
    ("E09","S状結腸捻転: 腹部膨満+圧痛",{"soft_nontender":0.05,"localized_tenderness":0.40,"peritoneal_signs":0.55}),
    ("E01","S状結腸捻転: 発熱(壊疽/穿孔時, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("E02","S状結腸捻転: 頻脈(脱水/ショック)",{"under_100":0.25,"100_120":0.45,"over_120":0.30}),
    ("L01","S状結腸捻転: WBC上昇(壊疽時)",{"low_under_4000":0.03,"normal_4000_10000":0.30,"high_10000_20000":0.45,"very_high_over_20000":0.22}),
    ("T01","S状結腸捻転: 急性~亜急性",{"under_3d":0.55,"3d_to_1w":0.30,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","S状結腸捻転: 急性",{"sudden_hours":0.45,"gradual_days":0.55}),
]:
    add("D180","sigmoid_volvulus",to,reason,cpt)
s3["full_cpts"]["D180"] = {"parents":["R01"],"description":"S状結腸捻転。高齢者",
    "cpt":{"18_39":0.001,"40_64":0.002,"65_plus":0.005}}

# D181 アデノウイルス感染症
s1["variables"].append({"id":"D181","name":"adenovirus","name_ja":"アデノウイルス感染症",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"咽頭結膜熱(プール熱)/気道感染/胃腸炎/出血性膀胱炎。高熱+咽頭炎+結膜炎が三徴"})
for to,reason,cpt in [
    ("E01","アデノウイルス: 高熱(90%+, 39-40℃, 5-7日持続)",{"under_37.5":0.05,"37.5_38.0":0.08,"38.0_39.0":0.25,"39.0_40.0":0.40,"over_40.0":0.22}),
    ("S02","アデノウイルス: 咽頭痛(咽頭炎, 80%+)",{"absent":0.12,"present":0.88}),
    ("E08","アデノウイルス: 咽頭所見(発赤/白苔)",{"normal":0.10,"erythema":0.60,"exudate_or_white_patch":0.30}),
    ("S01","アデノウイルス: 咳嗽(50-60%)",{"absent":0.35,"dry":0.40,"productive":0.25}),
    ("S14","アデノウイルス: 下痢(胃腸炎型, 30-40%)",{"absent":0.55,"watery":0.40,"bloody":0.05}),
    ("S05","アデノウイルス: 頭痛(40-50%)",{"absent":0.45,"mild":0.35,"severe":0.20}),
    ("L01","アデノウイルス: WBC(正常~やや上昇)",{"low_under_4000":0.10,"normal_4000_10000":0.50,"high_10000_20000":0.30,"very_high_over_20000":0.10}),
    ("L02","アデノウイルス: CRP上昇(細菌様の上昇あり)",{"normal_under_0.3":0.10,"mild_0.3_3":0.25,"moderate_3_10":0.35,"high_over_10":0.30}),
    ("T01","アデノウイルス: 急性(5-7日)",{"under_3d":0.25,"3d_to_1w":0.55,"1w_to_3w":0.18,"over_3w":0.02}),
    ("T02","アデノウイルス: 急性",{"sudden_hours":0.35,"gradual_days":0.65}),
]:
    add("D181","adenovirus",to,reason,cpt)
s3["full_cpts"]["D181"] = {"parents":[],"description":"アデノウイルス感染症",
    "cpt":{"":0.005}}

# D182 猩紅熱(Scarlet Fever)
s1["variables"].append({"id":"D182","name":"scarlet_fever","name_ja":"猩紅熱",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"GAS咽頭炎+発疹(sandpaper rash)+苺舌。発熱+咽頭痛+全身性粗い紅斑。ペニシリン治療"})
for to,reason,cpt in [
    ("E01","猩紅熱: 高熱(90%+)",{"under_37.5":0.05,"37.5_38.0":0.10,"38.0_39.0":0.30,"39.0_40.0":0.35,"over_40.0":0.20}),
    ("S02","猩紅熱: 咽頭痛(GAS咽頭炎, 95%+)",{"absent":0.03,"present":0.97}),
    ("E08","猩紅熱: 咽頭(発赤/白苔)",{"normal":0.03,"erythema":0.35,"exudate_or_white_patch":0.62}),
    ("E12","猩紅熱: 皮疹(sandpaper rash, 全身性粗い紅斑)",{"normal":0.03,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.01,"maculopapular_rash":0.10,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.80,"purpura":0.01,"vesicle_bulla":0.01,"skin_necrosis":0.01}),
    ("S05","猩紅熱: 頭痛(50-60%)",{"absent":0.35,"mild":0.40,"severe":0.25}),
    ("S07","猩紅熱: 倦怠感(70-80%)",{"absent":0.15,"mild":0.45,"severe":0.40}),
    ("S13","猩紅熱: 嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("L01","猩紅熱: WBC上昇(好中球)",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.50,"very_high_over_20000":0.22}),
    ("L07","猩紅熱: 迅速溶連菌検査陽性",{"negative":0.10,"positive":0.90}),
    ("T01","猩紅熱: 急性",{"under_3d":0.50,"3d_to_1w":0.40,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","猩紅熱: 急性",{"sudden_hours":0.40,"gradual_days":0.60}),
]:
    add("D182","scarlet_fever",to,reason,cpt)
s3["full_cpts"]["D182"] = {"parents":[],"description":"猩紅熱。GAS咽頭炎+発疹",
    "cpt":{"":0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"D180: 8e, D181: 10e, D182: 11e. Total: {s2['total_edges']} edges, 182 diseases")
