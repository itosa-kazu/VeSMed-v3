#!/usr/bin/env python3
"""Add D287-D291: 5 diseases."""
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

# D287 胆嚢癌 (Gallbladder Cancer)
s1["variables"].append({"id":"D287","name":"gallbladder_cancer","name_ja":"胆嚢癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"胆石合併が多い。RUQ痛+黄疸+体重減少。早期は無症状。進行で胆管浸潤→閉塞性黄疸"})
for to,r,c in [
    ("S12","胆嚢癌: RUQ痛(60-70%)",{"absent":0.20,"epigastric":0.08,"RUQ":0.60,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.07}),
    ("E18","胆嚢癌: 黄疸(40-50%)",{"absent":0.40,"present":0.60}),
    ("S07","胆嚢癌: 体重減少(50-60%)",{"absent":0.25,"mild":0.35,"severe":0.40}),
    ("S13","胆嚢癌: 嘔気(30-40%)",{"absent":0.55,"present":0.45}),
    ("L11","胆嚢癌: 肝酵素上昇(胆管浸潤)",{"normal":0.25,"mild_elevated":0.40,"very_high":0.35}),
    ("E01","胆嚢癌: 発熱(胆管炎合併, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.12,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.03}),
    ("T01","胆嚢癌: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","胆嚢癌: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D287","gallbladder_cancer",to,r,c)
s3["full_cpts"]["D287"] = {"parents":["R01","R02"],"description":"胆嚢癌。女性+高齢者",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0,"18_39,male":0.0002,"18_39,female":0.0003,"40_64,male":0.001,"40_64,female":0.002,"65_plus,male":0.002,"65_plus,female":0.004}}

# D288 精巣腫瘍 (Testicular Cancer)
s1["variables"].append({"id":"D288","name":"testicular_cancer","name_ja":"精巣腫瘍",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"若年男性(15-35歳)。無痛性陰嚢腫大。セミノーマ/非セミノーマ。LDH/AFP/hCG上昇"})
for to,r,c in [
    ("S07","精巣腫瘍: 倦怠感(30-40%)",{"absent":0.50,"mild":0.35,"severe":0.15}),
    ("S15","精巣腫瘍: 腰背部痛(後腹膜転移, 20-30%)",{"absent":0.65,"present":0.35}),
    ("S04","精巣腫瘍: 呼吸困難(肺転移, 10-20%)",{"absent":0.75,"on_exertion":0.15,"at_rest":0.10}),
    ("L16","精巣腫瘍: LDH上昇(腫瘍マーカー, 50-60%)",{"normal":0.30,"elevated":0.70}),
    ("T01","精巣腫瘍: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","精巣腫瘍: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D288","testicular_cancer",to,r,c)
s3["full_cpts"]["D288"] = {"parents":["R01","R02"],"description":"精巣腫瘍。若年男性のみ",
    "cpt":{"0_1,male":0.0001,"0_1,female":0.0,"1_5,male":0.0002,"1_5,female":0.0,"6_12,male":0.0003,"6_12,female":0.0,"13_17,male":0.001,"13_17,female":0.0,"18_39,male":0.003,"18_39,female":0.0,"40_64,male":0.001,"40_64,female":0.0,"65_plus,male":0.0005,"65_plus,female":0.0}}

# D289 前立腺癌 (Prostate Cancer)
s1["variables"].append({"id":"D289","name":"prostate_cancer","name_ja":"前立腺癌",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"高齢男性。初期無症状→進行で排尿障害+血尿+骨転移痛。PSA上昇"})
for to,r,c in [
    ("S10","前立腺癌: 排尿障害(30-40%)",{"absent":0.50,"present":0.50}),
    ("S15","前立腺癌: 骨転移痛(20-30%)",{"absent":0.60,"present":0.40}),
    ("S07","前立腺癌: 倦怠感(30-40%)",{"absent":0.50,"mild":0.35,"severe":0.15}),
    ("L16","前立腺癌: LDH上昇(転移時)",{"normal":0.40,"elevated":0.60}),
    ("T01","前立腺癌: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.15,"over_3w":0.75}),
    ("T02","前立腺癌: 緩徐",{"sudden_hours":0.03,"gradual_days":0.97}),
]: add("D289","prostate_cancer",to,r,c)
s3["full_cpts"]["D289"] = {"parents":["R01","R02"],"description":"前立腺癌。高齢男性のみ",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0,"18_39,male":0.0002,"18_39,female":0.0,"40_64,male":0.002,"40_64,female":0.0,"65_plus,male":0.006,"65_plus,female":0.0}}

# D290 膀胱癌 (Bladder Cancer)
s1["variables"].append({"id":"D290","name":"bladder_cancer","name_ja":"膀胱癌",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"無痛性肉眼的血尿が初発症状(80%+)。喫煙がリスク。高齢男性に多い"})
for to,r,c in [
    ("S10","膀胱癌: 排尿障害(30-40%)",{"absent":0.55,"present":0.45}),
    ("S15","膀胱癌: 側腹部痛(水腎症, 10-20%)",{"absent":0.75,"present":0.25}),
    ("S07","膀胱癌: 倦怠感",{"absent":0.45,"mild":0.35,"severe":0.20}),
    ("L05","膀胱癌: 尿異常(血尿, 80%+)",{"normal":0.08,"pyuria_bacteriuria":0.92}),
    ("T01","膀胱癌: 慢性",{"under_3d":0.10,"3d_to_1w":0.15,"1w_to_3w":0.25,"over_3w":0.50}),
    ("T02","膀胱癌: 慢性~間欠",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D290","bladder_cancer",to,r,c)
s3["full_cpts"]["D290"] = {"parents":["R01","R02"],"description":"膀胱癌。高齢男性",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0001,"13_17,female":0.0001,"18_39,male":0.0005,"18_39,female":0.0002,"40_64,male":0.002,"40_64,female":0.0005,"65_plus,male":0.005,"65_plus,female":0.001}}

# D291 腎細胞癌 → already D75 covers 腎細胞癌? Check. D75 is DVT/PE. D48 is 腫瘍全般.
# Actually D81 is 腎細胞癌. Skip.
# D291 子宮外妊娠 (Ectopic Pregnancy)
s1["variables"].append({"id":"D291","name":"ectopic_pregnancy","name_ja":"子宮外妊娠",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"妊娠可能年齢女性。下腹部痛+性器出血+無月経。破裂で出血性ショック。緊急手術"})
for to,r,c in [
    ("S12","子宮外妊娠: 下腹部痛(90%+)",{"absent":0.03,"epigastric":0.02,"RUQ":0.05,"RLQ":0.35,"LLQ":0.35,"suprapubic":0.10,"diffuse":0.10}),
    ("S44","子宮外妊娠: 性器出血(60-70%)",{"absent":0.25,"present":0.75}),
    ("E03","子宮外妊娠: 低血圧(破裂時ショック)",{"normal_over_90":0.30,"hypotension_under_90":0.70}),
    ("E02","子宮外妊娠: 頻脈(出血)",{"under_100":0.15,"100_120":0.35,"over_120":0.50}),
    ("E16","子宮外妊娠: 意識障害(ショック時)",{"normal":0.40,"confused":0.35,"obtunded":0.25}),
    ("S13","子宮外妊娠: 嘔気(30-40%)",{"absent":0.55,"present":0.45}),
    ("T01","子宮外妊娠: 急性",{"under_3d":0.65,"3d_to_1w":0.25,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","子宮外妊娠: 急性~突発(破裂時)",{"sudden_hours":0.65,"gradual_days":0.35}),
]: add("D291","ectopic_pregnancy",to,r,c)
s3["full_cpts"]["D291"] = {"parents":["R01","R02"],"description":"子宮外妊娠。妊娠可能年齢女性のみ",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.001,"18_39,male":0.0,"18_39,female":0.005,"40_64,male":0.0,"40_64,female":0.001,"65_plus,male":0.0,"65_plus,female":0.0}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 291 diseases")
