#!/usr/bin/env python3
"""Add D189 Spontaneous Bacterial Peritonitis (already D56 SBP?), 
D190 Spinal Epidural Abscess (already D117?), check first.
Actually: D189 Toxic Alcohol Poisoning (methanol/ethylene glycol)
D190 SIADH
D191 Pheochromocytoma Crisis (D73 exists as 褐色細胞腫, but crisis variant)
Let me check D73... D73 is 褐色細胞腫. I can add crisis as same entity or skip.
D189: メタノール中毒 (Methanol Poisoning) - important toxicology
D190: SIADH - important endocrine
D191: 偽膜性腸炎(C.diff) - already D38? D38 is C.diff. Skip.
D191: 急性糸球体腎炎(PSGN) - post-streptococcal
"""
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
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt

# D189 メタノール中毒
s1["variables"].append({"id":"D189","name":"methanol_poisoning","name_ja":"メタノール中毒",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"メタノール→蟻酸(formate)→代謝性アシドーシス+視神経障害。AG開大+浸透圧gap。視力障害が特徴的"})
for to,reason,cpt in [
    ("E16","メタノール: 意識障害(50-70%)",{"normal":0.20,"confused":0.40,"obtunded":0.40}),
    ("S05","メタノール: 頭痛(60-70%)",{"absent":0.25,"mild":0.30,"severe":0.45}),
    ("S13","メタノール: 嘔気/嘔吐(70-80%)",{"absent":0.15,"present":0.85}),
    ("S04","メタノール: 呼吸困難(Kussmaul呼吸, アシドーシス代償)",{"absent":0.30,"on_exertion":0.20,"at_rest":0.50}),
    ("E04","メタノール: 頻呼吸(Kussmaul)",{"normal_under_20":0.15,"tachypnea_20_30":0.35,"severe_over_30":0.50}),
    ("E02","メタノール: 頻脈",{"under_100":0.25,"100_120":0.40,"over_120":0.35}),
    ("S12","メタノール: 腹痛(膵炎合併, 30-40%)",{"absent":0.55,"epigastric":0.25,"RUQ":0.03,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.12}),
    ("T01","メタノール: 超急性(12-24h後に症状出現)",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","メタノール: 急性",{"sudden_hours":0.75,"gradual_days":0.25}),
]:
    add("D189","methanol_poisoning",to,reason,cpt)
s3["full_cpts"]["D189"] = {"parents":[],"description":"メタノール中毒",
    "cpt":{"":0.001}}

# D190 SIADH
s1["variables"].append({"id":"D190","name":"SIADH","name_ja":"SIADH(抗利尿ホルモン不適切分泌症候群)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"ADH過剰→希釈性低Na血症。原因:肺疾患/CNS疾患/薬剤/悪性腫瘍。Na<120で痙攣/昏睡リスク"})
for to,reason,cpt in [
    ("L44","SIADH: 低Na血症(定義的)",{"normal":0.03,"hyponatremia":0.95,"hyperkalemia":0.01,"other":0.01}),
    ("E16","SIADH: 意識障害(Na<120で, 40-60%)",{"normal":0.30,"confused":0.40,"obtunded":0.30}),
    ("S42","SIADH: 痙攣(重度低Na, 20-30%)",{"absent":0.70,"present":0.30}),
    ("S05","SIADH: 頭痛(30-40%)",{"absent":0.50,"mild":0.30,"severe":0.20}),
    ("S13","SIADH: 嘔気(40-50%)",{"absent":0.45,"present":0.55}),
    ("S07","SIADH: 倦怠感(60-70%)",{"absent":0.25,"mild":0.40,"severe":0.35}),
    ("T01","SIADH: 亜急性~慢性",{"under_3d":0.15,"3d_to_1w":0.25,"1w_to_3w":0.35,"over_3w":0.25}),
    ("T02","SIADH: 緩徐",{"sudden_hours":0.15,"gradual_days":0.85}),
]:
    add("D190","SIADH",to,reason,cpt)
s3["full_cpts"]["D190"] = {"parents":["R01"],"description":"SIADH。高齢者に多い",
    "cpt":{"18_39":0.001,"40_64":0.002,"65_plus":0.004}}

# D191 溶連菌感染後急性糸球体腎炎 (PSGN)
s1["variables"].append({"id":"D191","name":"PSGN","name_ja":"溶連菌感染後急性糸球体腎炎(PSGN)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"GAS咽頭炎/膿痂疹の1-3週後。血尿+蛋白尿+浮腫+高血圧+AKI。補体(C3)低下が特徴。小児に多いが成人もあり"})
for to,reason,cpt in [
    ("L05","PSGN: 尿異常(血尿+蛋白尿, 100%)",{"normal":0.02,"pyuria_bacteriuria":0.98}),
    ("L55","PSGN: AKI(Cr上昇, 50-70%)",{"normal":0.25,"mild_elevated":0.40,"high_AKI":0.35}),
    ("E36","PSGN: 浮腫(顔面/下肢, 80%+)",{"absent":0.10,"unilateral":0.05,"bilateral":0.85}),
    ("E38","PSGN: 高血圧(体液過剰, 60-80%)",{"normal_under_140":0.20,"elevated_140_180":0.50,"crisis_over_180":0.30}),
    ("S05","PSGN: 頭痛(高血圧, 30-40%)",{"absent":0.50,"mild":0.30,"severe":0.20}),
    ("E01","PSGN: 発熱(先行感染の残存, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.18,"38.0_39.0":0.15,"39.0_40.0":0.05,"over_40.0":0.02}),
    ("S07","PSGN: 倦怠感",{"absent":0.20,"mild":0.45,"severe":0.35}),
    ("T01","PSGN: 亜急性(感染1-3週後)",{"under_3d":0.10,"3d_to_1w":0.25,"1w_to_3w":0.50,"over_3w":0.15}),
    ("T02","PSGN: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]:
    add("D191","PSGN",to,reason,cpt)
s3["full_cpts"]["D191"] = {"parents":["R01"],"description":"PSGN。小児~若年成人",
    "cpt":{"18_39":0.002,"40_64":0.001,"65_plus":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"D189: 9e, D190: 8e, D191: 9e. Total: {s2['total_edges']} edges, 191 diseases")
