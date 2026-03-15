#!/usr/bin/env python3
"""Add D247-D251: 5 diseases to reach 251."""
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

# D247 胃癌 (Gastric Cancer)
s1["variables"].append({"id":"D247","name":"gastric_cancer","name_ja":"胃癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"心窩部痛+体重減少+貧血+嚥下困難(噴門部)。進行癌で閉塞/出血/穿孔"})
for to,r,c in [
    ("S12","胃癌: 心窩部痛(60-70%)",{"absent":0.20,"epigastric":0.65,"RUQ":0.03,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.07}),
    ("S07","胃癌: 倦怠感/体重減少(70-80%)",{"absent":0.12,"mild":0.30,"severe":0.58}),
    ("S13","胃癌: 嘔気(50-60%)",{"absent":0.35,"present":0.65}),
    ("S44","胃癌: 出血(吐血/黒色便, 20-30%)",{"absent":0.65,"present":0.35}),
    ("E01","胃癌: 通常無熱",{"under_37.5":0.75,"37.5_38.0":0.10,"38.0_39.0":0.08,"39.0_40.0":0.05,"over_40.0":0.02}),
    ("T01","胃癌: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","胃癌: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D247","gastric_cancer",to,r,c)
s3["full_cpts"]["D247"] = {"parents":["R01"],"description":"胃癌","cpt":{"18_39":0.0005,"40_64":0.003,"65_plus":0.006}}

# D248 食道癌 (Esophageal Cancer)
s1["variables"].append({"id":"D248","name":"esophageal_cancer","name_ja":"食道癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"嚥下困難(進行性)+体重減少。扁平上皮癌(飲酒+喫煙)/腺癌(Barrett食道)"})
for to,r,c in [
    ("S07","食道癌: 倦怠感/体重減少(80%+)",{"absent":0.10,"mild":0.25,"severe":0.65}),
    ("S21","食道癌: 胸痛/嚥下痛(30-40%)",{"absent":0.55,"burning":0.15,"sharp":0.10,"pressure":0.15,"tearing":0.05}),
    ("S13","食道癌: 嘔気(30-40%)",{"absent":0.55,"present":0.45}),
    ("T01","食道癌: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.15,"over_3w":0.75}),
    ("T02","食道癌: 緩徐進行",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D248","esophageal_cancer",to,r,c)
s3["full_cpts"]["D248"] = {"parents":["R01","R02"],"description":"食道癌",
    "cpt":{"18_39,male":0.0002,"18_39,female":0.0001,"40_64,male":0.002,"40_64,female":0.0005,"65_plus,male":0.004,"65_plus,female":0.001}}

# D249 慢性膵炎 (Chronic Pancreatitis)
s1["variables"].append({"id":"D249","name":"chronic_pancreatitis","name_ja":"慢性膵炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"反復性腹痛(心窩部→背部放散)+脂肪便+DM。アルコール性が最多。膵石/膵管拡張"})
for to,r,c in [
    ("S12","慢性膵炎: 心窩部痛(食後増悪, 80%+)",{"absent":0.10,"epigastric":0.60,"RUQ":0.05,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.20}),
    ("S15","慢性膵炎: 背部放散痛(50-60%)",{"absent":0.35,"present":0.65}),
    ("S13","慢性膵炎: 嘔気(40-50%)",{"absent":0.45,"present":0.55}),
    ("S07","慢性膵炎: 倦怠感/体重減少(60-70%)",{"absent":0.20,"mild":0.35,"severe":0.45}),
    ("L54","慢性膵炎: 血糖(DM合併, 30-40%)",{"hypoglycemia":0.02,"normal":0.45,"hyperglycemia":0.40,"very_high_over_500":0.13}),
    ("T01","慢性膵炎: 慢性(急性増悪で来院)",{"under_3d":0.20,"3d_to_1w":0.25,"1w_to_3w":0.25,"over_3w":0.30}),
    ("T02","慢性膵炎: 急性増悪~慢性",{"sudden_hours":0.30,"gradual_days":0.70}),
]: add("D249","chronic_pancreatitis",to,r,c)
s3["full_cpts"]["D249"] = {"parents":["R01","R02"],"description":"慢性膵炎。男性/飲酒",
    "cpt":{"18_39,male":0.002,"18_39,female":0.0005,"40_64,male":0.004,"40_64,female":0.001,"65_plus,male":0.004,"65_plus,female":0.001}}

# D250 自己免疫性肝炎(→D169で既にカバー)。代わりに：
# D250 原発性胆汁性胆管炎 (PBC)
s1["variables"].append({"id":"D250","name":"PBC","name_ja":"原発性胆汁性胆管炎(PBC)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"抗ミトコンドリア抗体(AMA)陽性。慢性進行性胆汁うっ滞→肝硬変。掻痒+黄疸+倦怠感。中年女性"})
for to,r,c in [
    ("E18","PBC: 黄疸(進行期, 40-60%)",{"absent":0.35,"present":0.65}),
    ("S07","PBC: 倦怠感(80%+)",{"absent":0.10,"mild":0.40,"severe":0.50}),
    ("L11","PBC: 肝酵素(ALP優位上昇)",{"normal":0.08,"mild_elevated":0.52,"very_high":0.40}),
    ("S12","PBC: 腹痛(RUQ, 20-30%)",{"absent":0.60,"epigastric":0.05,"RUQ":0.28,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.02}),
    ("T01","PBC: 慢性",{"under_3d":0.02,"3d_to_1w":0.05,"1w_to_3w":0.10,"over_3w":0.83}),
    ("T02","PBC: 緩徐",{"sudden_hours":0.03,"gradual_days":0.97}),
]: add("D250","PBC",to,r,c)
s3["full_cpts"]["D250"] = {"parents":["R02"],"description":"PBC。中年女性","cpt":{"male":0.0003,"female":0.002}}

# D251 肝硬変 (Liver Cirrhosis, decompensated)
s1["variables"].append({"id":"D251","name":"decompensated_cirrhosis","name_ja":"非代償性肝硬変",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"黄疸+腹水+肝性脳症+食道静脈瘤。Child-Pugh B/C。感染(SBP)/出血リスク"})
for to,r,c in [
    ("E18","肝硬変: 黄疸(90%+)",{"absent":0.05,"present":0.95}),
    ("E36","肝硬変: 浮腫/腹水(80%+)",{"absent":0.08,"unilateral":0.02,"bilateral":0.90}),
    ("E16","肝硬変: 肝性脳症(40-50%)",{"normal":0.35,"confused":0.40,"obtunded":0.25}),
    ("S07","肝硬変: 倦怠感(90%+)",{"absent":0.05,"mild":0.25,"severe":0.70}),
    ("L11","肝硬変: 肝酵素",{"normal":0.15,"mild_elevated":0.55,"very_high":0.30}),
    ("S44","肝硬変: 出血傾向(凝固障害, 40-50%)",{"absent":0.45,"present":0.55}),
    ("E01","肝硬変: 発熱(SBP/感染, 20-30%)",{"under_37.5":0.55,"37.5_38.0":0.15,"38.0_39.0":0.18,"39.0_40.0":0.10,"over_40.0":0.02}),
    ("T01","肝硬変: 慢性",{"under_3d":0.08,"3d_to_1w":0.12,"1w_to_3w":0.20,"over_3w":0.60}),
    ("T02","肝硬変: 慢性~急性増悪",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D251","decompensated_cirrhosis",to,r,c)
s3["full_cpts"]["D251"] = {"parents":["R01"],"description":"非代償性肝硬変","cpt":{"18_39":0.001,"40_64":0.003,"65_plus":0.005}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 251 diseases")
