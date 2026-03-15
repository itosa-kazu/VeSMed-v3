#!/usr/bin/env python3
"""Add D197-D201: 5 more diseases."""
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

# D197 無顆粒球症 (Agranulocytosis)
s1["variables"].append({"id":"D197","name":"agranulocytosis","name_ja":"無顆粒球症",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"好中球<500. 薬剤性(抗甲状腺薬/クロザピン等)が最多. 発熱+咽頭痛+口腔潰瘍が三徴. 敗血症リスク"})
for to,r,c in [
    ("E01","無顆粒球症: 高熱(90%+)",{"under_37.5":0.05,"37.5_38.0":0.08,"38.0_39.0":0.22,"39.0_40.0":0.35,"over_40.0":0.30}),
    ("S02","無顆粒球症: 咽頭痛(口腔/咽頭潰瘍, 70-80%)",{"absent":0.15,"present":0.85}),
    ("E08","無顆粒球症: 咽頭(潰瘍/壊死, 60-70%)",{"normal":0.20,"erythema":0.25,"exudate_or_white_patch":0.55}),
    ("S07","無顆粒球症: 倦怠感(80%+)",{"absent":0.08,"mild":0.25,"severe":0.67}),
    ("L01","無顆粒球症: WBC著減(定義的)",{"low_under_4000":0.90,"normal_4000_10000":0.08,"high_10000_20000":0.01,"very_high_over_20000":0.01}),
    ("L02","無顆粒球症: CRP上昇(感染合併)",{"normal_under_0.3":0.08,"mild_0.3_3":0.12,"moderate_3_10":0.30,"high_over_10":0.50}),
    ("S09","無顆粒球症: 悪寒戦慄(菌血症, 50-60%)",{"absent":0.35,"present":0.65}),
    ("T01","無顆粒球症: 急性",{"under_3d":0.50,"3d_to_1w":0.35,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","無顆粒球症: 急性",{"sudden_hours":0.40,"gradual_days":0.60}),
]: add("D197","agranulocytosis",to,r,c)
s3["full_cpts"]["D197"] = {"parents":[],"description":"無顆粒球症. 薬剤性","cpt":{"":0.001}}

# D198 IgA血管炎 (Henoch-Schonlein Purpura / IgA Vasculitis)
s1["variables"].append({"id":"D198","name":"IgA_vasculitis","name_ja":"IgA血管炎(HSP)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"IgA沈着性小血管炎. 四徴:触知可能紫斑(下肢)+関節痛+腹痛+腎炎. 小児に多いが成人もあり(腎障害重症化)"})
for to,r,c in [
    ("E12","IgA血管炎: 紫斑(下肢, 100%)",{"normal":0.02,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.20,"maculopapular_rash":0.02,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.65,"vesicle_bulla":0.02,"skin_necrosis":0.05}),
    ("S08","IgA血管炎: 関節痛(60-80%)",{"absent":0.15,"present":0.85}),
    ("S12","IgA血管炎: 腹痛(50-70%)",{"absent":0.25,"epigastric":0.10,"RUQ":0.03,"RLQ":0.03,"LLQ":0.03,"suprapubic":0.01,"diffuse":0.55}),
    ("L05","IgA血管炎: 尿異常(腎炎, 30-50%)",{"normal":0.45,"pyuria_bacteriuria":0.55}),
    ("E01","IgA血管炎: 発熱(20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("S14","IgA血管炎: 消化管出血(20-30%)",{"absent":0.65,"watery":0.10,"bloody":0.25}),
    ("L01","IgA血管炎: WBC(正常~軽度)",{"low_under_4000":0.05,"normal_4000_10000":0.45,"high_10000_20000":0.35,"very_high_over_20000":0.15}),
    ("T01","IgA血管炎: 急性~亜急性",{"under_3d":0.20,"3d_to_1w":0.35,"1w_to_3w":0.30,"over_3w":0.15}),
    ("T02","IgA血管炎: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D198","IgA_vasculitis",to,r,c)
s3["full_cpts"]["D198"] = {"parents":["R01"],"description":"IgA血管炎. 小児~若年成人","cpt":{"18_39":0.002,"40_64":0.001,"65_plus":0.001}}

# D199 狂犬病 (Rabies)
s1["variables"].append({"id":"D199","name":"rabies","name_ja":"狂犬病",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"狂犬病ウイルス. 動物咬傷後1-3ヶ月で発症. 狂躁型(興奮/恐水/恐風)+麻痺型. 発症後ほぼ100%致死"})
for to,r,c in [
    ("E01","狂犬病: 発熱(80-90%)",{"under_37.5":0.08,"37.5_38.0":0.12,"38.0_39.0":0.30,"39.0_40.0":0.30,"over_40.0":0.20}),
    ("E16","狂犬病: 意識障害(進行性, 80%+)",{"normal":0.10,"confused":0.40,"obtunded":0.50}),
    ("S42","狂犬病: 痙攣(恐水/恐風誘発, 50-60%)",{"absent":0.35,"present":0.65}),
    ("S07","狂犬病: 倦怠感(前駆, 70-80%)",{"absent":0.12,"mild":0.30,"severe":0.58}),
    ("S05","狂犬病: 頭痛(前駆, 50-60%)",{"absent":0.30,"mild":0.30,"severe":0.40}),
    ("E02","狂犬病: 頻脈(自律神経障害)",{"under_100":0.15,"100_120":0.35,"over_120":0.50}),
    ("E03","狂犬病: 低血圧(末期)",{"normal_over_90":0.40,"hypotension_under_90":0.60}),
    ("T01","狂犬病: 亜急性~慢性(潜伏1-3ヶ月)",{"under_3d":0.05,"3d_to_1w":0.15,"1w_to_3w":0.40,"over_3w":0.40}),
    ("T02","狂犬病: 緩徐→急速進行",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D199","rabies",to,r,c)
s3["full_cpts"]["D199"] = {"parents":[],"description":"狂犬病. 動物咬傷","cpt":{"":0.0003}}

# D200 正常圧水頭症 (NPH)
s1["variables"].append({"id":"D200","name":"NPH","name_ja":"正常圧水頭症(NPH)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"三徴:歩行障害+認知障害+尿失禁(Hakim triad). 高齢者. 治療可能な認知症. VP shuntで改善"})
for to,r,c in [
    ("E16","NPH: 認知障害(90%+)",{"normal":0.05,"confused":0.65,"obtunded":0.30}),
    ("S52","NPH: 歩行障害(磁性歩行, 90%+)",{"absent":0.05,"unilateral_weakness":0.10,"bilateral":0.85}),
    ("S05","NPH: 頭痛(30-40%)",{"absent":0.50,"mild":0.35,"severe":0.15}),
    ("T01","NPH: 慢性(数ヶ月~年)",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.10,"over_3w":0.85}),
    ("T02","NPH: 緩徐進行",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D200","NPH",to,r,c)
s3["full_cpts"]["D200"] = {"parents":["R01"],"description":"NPH. 高齢者","cpt":{"18_39":0.0002,"40_64":0.001,"65_plus":0.004}}

# D201 ウイルス性出血熱 (Viral Hemorrhagic Fever - Ebola/Marburg etc)
s1["variables"].append({"id":"D201","name":"viral_hemorrhagic_fever","name_ja":"ウイルス性出血熱",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"エボラ/マールブルグ/ラッサ/クリミア・コンゴ等. 高熱+出血傾向+多臓器不全. 致死率30-90%. 流行地渡航歴"})
for to,r,c in [
    ("E01","VHF: 高熱(100%)",{"under_37.5":0.02,"37.5_38.0":0.05,"38.0_39.0":0.18,"39.0_40.0":0.35,"over_40.0":0.40}),
    ("S44","VHF: 出血傾向(50-80%)",{"absent":0.20,"present":0.80}),
    ("S07","VHF: 倦怠感(90%+)",{"absent":0.03,"mild":0.15,"severe":0.82}),
    ("S05","VHF: 頭痛(70-80%)",{"absent":0.15,"mild":0.25,"severe":0.60}),
    ("S06","VHF: 筋肉痛(60-70%)",{"absent":0.25,"present":0.75}),
    ("S13","VHF: 嘔吐(60-70%)",{"absent":0.25,"present":0.75}),
    ("S14","VHF: 下痢(50-60%)",{"absent":0.35,"watery":0.40,"bloody":0.25}),
    ("E03","VHF: 低血圧(ショック)",{"normal_over_90":0.25,"hypotension_under_90":0.75}),
    ("E02","VHF: 頻脈",{"under_100":0.05,"100_120":0.30,"over_120":0.65}),
    ("L01","VHF: WBC(初期低下→後に上昇)",{"low_under_4000":0.30,"normal_4000_10000":0.25,"high_10000_20000":0.25,"very_high_over_20000":0.20}),
    ("L14","VHF: 血小板減少(DIC)",{"normal":0.10,"left_shift":0.05,"atypical_lymphocytes":0.02,"thrombocytopenia":0.78,"eosinophilia":0.00,"lymphocyte_predominant":0.05}),
    ("L11","VHF: 肝酵素著高",{"normal":0.05,"mild_elevated":0.15,"very_high":0.80}),
    ("T01","VHF: 急性",{"under_3d":0.20,"3d_to_1w":0.50,"1w_to_3w":0.25,"over_3w":0.05}),
    ("T02","VHF: 急性",{"sudden_hours":0.30,"gradual_days":0.70}),
]: add("D201","viral_hemorrhagic_fever",to,r,c)
s3["full_cpts"]["D201"] = {"parents":[],"description":"VHF. 流行地渡航","cpt":{"":0.0002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 201 diseases")
