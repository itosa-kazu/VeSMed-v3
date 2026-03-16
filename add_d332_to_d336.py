#!/usr/bin/env python3
"""Add D332-D336: 5 diseases."""
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

# D332 下垂体機能低下症 (Hypopituitarism)
s1["variables"].append({"id":"D332","name":"hypopituitarism","name_ja":"下垂体機能低下症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"下垂体前葉ホルモン欠損。副腎不全+甲状腺低下+性腺低下。倦怠感+低血圧+低Na+低血糖。Sheehan症候群/腫瘍/術後"})
for to,r,c in [
    ("S07","下垂体機能低下: 倦怠感(80%+)",{"absent":0.05,"mild":0.25,"severe":0.70}),
    ("E38","下垂体機能低下: 低血圧(副腎不全, 60-70%)",{"normal_under_140":0.80,"elevated_140_180":0.15,"crisis_over_180":0.05}),
    ("L44","下垂体機能低下: 低Na血症(40-50%)",{"normal":0.40,"hyponatremia":0.50,"hyperkalemia":0.02,"other":0.08}),
    ("S13","下垂体機能低下: 嘔気嘔吐(副腎クリーゼ, 30-40%)",{"absent":0.55,"present":0.45}),
    ("E16","下垂体機能低下: 意識障害(副腎クリーゼ/粘液水腫, 20-30%)",{"normal":0.55,"confused":0.30,"obtunded":0.15}),
    ("S05","下垂体機能低下: 頭痛(腫瘍性, 30-40%)",{"absent":0.50,"mild":0.30,"severe":0.20}),
    ("E01","下垂体機能低下: 低体温(甲状腺低下)",{"under_37.5":0.70,"37.5_38.0":0.15,"38.0_39.0":0.10,"39.0_40.0":0.04,"over_40.0":0.01}),
    ("T01","下垂体機能低下: 慢性(急性増悪あり)",{"under_3d":0.10,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.60}),
    ("T02","下垂体機能低下: 緩徐",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D332","hypopituitarism",to,r,c)
s3["full_cpts"]["D332"] = {"parents":["R01","R02"],"description":"下垂体機能低下症",
    "cpt":{"0_1,male":0.0002,"0_1,female":0.0002,"1_5,male":0.0003,"1_5,female":0.0003,"6_12,male":0.0003,"6_12,female":0.0003,"13_17,male":0.0005,"13_17,female":0.0005,"18_39,male":0.001,"18_39,female":0.002,"40_64,male":0.001,"40_64,female":0.002,"65_plus,male":0.001,"65_plus,female":0.001}}

# D333 先端巨大症 (Acromegaly)
s1["variables"].append({"id":"D333","name":"acromegaly","name_ja":"先端巨大症",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"GH産生下垂体腺腫。末端肥大+顔貌変化+発汗過多+関節痛+頭痛。IGF-1高値+OGTT GH抑制不良"})
for to,r,c in [
    ("S05","先端巨大症: 頭痛(60-70%)",{"absent":0.20,"mild":0.40,"severe":0.40}),
    ("S07","先端巨大症: 倦怠感/関節痛(50-60%)",{"absent":0.25,"mild":0.35,"severe":0.40}),
    ("E38","先端巨大症: 高血圧(30-40%)",{"normal_under_140":0.45,"elevated_140_180":0.35,"crisis_over_180":0.20}),
    ("E02","先端巨大症: 心肥大→不整脈(20-30%)",{"under_100":0.50,"100_120":0.35,"over_120":0.15}),
    ("S04","先端巨大症: 睡眠時無呼吸(30-40%)",{"absent":0.50,"on_exertion":0.30,"at_rest":0.20}),
    ("T01","先端巨大症: 慢性",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.05,"over_3w":0.90}),
    ("T02","先端巨大症: 緩徐",{"sudden_hours":0.03,"gradual_days":0.97}),
]: add("D333","acromegaly",to,r,c)
s3["full_cpts"]["D333"] = {"parents":["R01"],"description":"先端巨大症。30-50歳",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0001,"13_17":0.0003,"18_39":0.001,"40_64":0.001,"65_plus":0.0005}}

# D334 IgG4関連疾患 (IgG4-Related Disease)
s1["variables"].append({"id":"D334","name":"IgG4_RD","name_ja":"IgG4関連疾患",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"IgG4陽性形質細胞浸潤→臓器腫大/線維化。自己免疫性膵炎/唾液腺腫大/後腹膜線維症/胆管狭窄。高齢男性に多い"})
for to,r,c in [
    ("S15","IgG4: 腹痛(膵炎/後腹膜, 50-60%)",{"absent":0.30,"present":0.70}),
    ("L11","IgG4: 肝胆道酵素上昇(胆管狭窄, 40-50%)",{"normal":0.35,"mild_elevated":0.35,"very_high":0.30}),
    ("S07","IgG4: 倦怠感/体重減少(40-50%)",{"absent":0.35,"mild":0.35,"severe":0.30}),
    ("E36","IgG4: 浮腫(腎障害/後腹膜, 20-30%)",{"absent":0.60,"unilateral":0.10,"bilateral":0.30}),
    ("L55","IgG4: 腎機能障害(腎病変, 20-30%)",{"normal":0.55,"mild_elevated":0.30,"high_AKI":0.15}),
    ("T01","IgG4: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.15,"over_3w":0.75}),
    ("T02","IgG4: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D334","IgG4_RD",to,r,c)
s3["full_cpts"]["D334"] = {"parents":["R01","R02"],"description":"IgG4関連疾患。中高年男性",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0001,"13_17,female":0.0001,"18_39,male":0.0005,"18_39,female":0.0003,"40_64,male":0.002,"40_64,female":0.001,"65_plus,male":0.003,"65_plus,female":0.001}}

# D335 閉塞性動脈硬化症 (PAD/ASO)
s1["variables"].append({"id":"D335","name":"PAD","name_ja":"閉塞性動脈硬化症(PAD)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"動脈硬化→下肢動脈閉塞。間欠性跛行(Fontaine II)→安静時痛(III)→壊疽(IV)。ABI<0.9。糖尿病/喫煙がリスク"})
for to,r,c in [
    ("S15","PAD: 下肢痛(間欠性跛行~安静時痛, 80%+)",{"absent":0.10,"present":0.90}),
    ("S07","PAD: 倦怠感/冷感(40-50%)",{"absent":0.35,"mild":0.40,"severe":0.25}),
    ("S04","PAD: 労作時症状(40-50%)",{"absent":0.40,"on_exertion":0.45,"at_rest":0.15}),
    ("E38","PAD: 高血圧(動脈硬化, 60-70%)",{"normal_under_140":0.20,"elevated_140_180":0.50,"crisis_over_180":0.30}),
    ("T01","PAD: 慢性(急性増悪あり)",{"under_3d":0.08,"3d_to_1w":0.12,"1w_to_3w":0.15,"over_3w":0.65}),
    ("T02","PAD: 緩徐(急性閉塞は突発)",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D335","PAD",to,r,c)
s3["full_cpts"]["D335"] = {"parents":["R01","R02"],"description":"PAD。高齢男性+糖尿病/喫煙",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0,"18_39,male":0.001,"18_39,female":0.0003,"40_64,male":0.004,"40_64,female":0.002,"65_plus,male":0.008,"65_plus,female":0.004}}

# D336 多発性嚢胞腎 (ADPKD)
s1["variables"].append({"id":"D336","name":"ADPKD","name_ja":"多発性嚢胞腎(ADPKD)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"常染色体優性遺伝。両側腎嚢胞→腎肥大→腎不全。側腹部痛+血尿+高血圧+腎不全。肝嚢胞/脳動脈瘤合併"})
for to,r,c in [
    ("S15","ADPKD: 側腹部痛(60-70%)",{"absent":0.20,"present":0.80}),
    ("E38","ADPKD: 高血圧(60-70%)",{"normal_under_140":0.20,"elevated_140_180":0.45,"crisis_over_180":0.35}),
    ("L55","ADPKD: 腎機能障害(進行性, 50-60%)",{"normal":0.25,"mild_elevated":0.35,"high_AKI":0.40}),
    ("S44","ADPKD: 血尿(30-50%)",{"absent":0.45,"present":0.55}),
    ("S07","ADPKD: 倦怠感(40-50%)",{"absent":0.35,"mild":0.35,"severe":0.30}),
    ("S05","ADPKD: 頭痛(高血圧/脳動脈瘤, 20-30%)",{"absent":0.55,"mild":0.25,"severe":0.20}),
    ("T01","ADPKD: 慢性(急性増悪あり)",{"under_3d":0.08,"3d_to_1w":0.12,"1w_to_3w":0.15,"over_3w":0.65}),
    ("T02","ADPKD: 緩徐",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D336","ADPKD",to,r,c)
s3["full_cpts"]["D336"] = {"parents":["R01"],"description":"ADPKD。30-50歳で発症",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0003,"13_17":0.0005,"18_39":0.002,"40_64":0.003,"65_plus":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 336 diseases")
