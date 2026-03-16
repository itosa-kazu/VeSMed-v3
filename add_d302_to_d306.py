#!/usr/bin/env python3
"""Add D302-D306: 5 diseases."""
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

# D302 進行性核上性麻痺 (PSP)
s1["variables"].append({"id":"D302","name":"PSP","name_ja":"進行性核上性麻痺(PSP)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"垂直注視麻痺(下方)+早期転倒+軸性固縮+認知症。パーキンソニズムだがL-DOPA無効"})
for to,r,c in [
    ("S52","PSP: 歩行障害/転倒(90%+)",{"absent":0.05,"unilateral_weakness":0.15,"bilateral":0.80}),
    ("E16","PSP: 認知機能低下(50-70%)",{"normal":0.20,"confused":0.55,"obtunded":0.25}),
    ("S53","PSP: 構音障害(60-70%)",{"absent":0.25,"dysarthria":0.60,"aphasia":0.15}),
    ("S07","PSP: 倦怠感",{"absent":0.10,"mild":0.35,"severe":0.55}),
    ("T01","PSP: 慢性",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.10,"over_3w":0.85}),
    ("T02","PSP: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D302","PSP",to,r,c)
s3["full_cpts"]["D302"] = {"parents":["R01"],"description":"PSP",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.0,"18_39":0.0001,"40_64":0.001,"65_plus":0.002}}

# D303 パーキンソン病 (Parkinson Disease)
s1["variables"].append({"id":"D303","name":"parkinson_disease","name_ja":"パーキンソン病",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"四徴:安静時振戦+固縮+無動+姿勢反射障害。片側発症→両側進展。L-DOPA有効"})
for to,r,c in [
    ("S52","パーキンソン: 運動障害(定義的)",{"absent":0.03,"unilateral_weakness":0.50,"bilateral":0.47}),
    ("S53","パーキンソン: 構音障害(40-50%)",{"absent":0.45,"dysarthria":0.45,"aphasia":0.10}),
    ("E16","パーキンソン: 認知症(進行期, 30-40%)",{"normal":0.50,"confused":0.35,"obtunded":0.15}),
    ("S07","パーキンソン: 倦怠感",{"absent":0.15,"mild":0.40,"severe":0.45}),
    ("T01","パーキンソン: 慢性",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.10,"over_3w":0.85}),
    ("T02","パーキンソン: 緩徐",{"sudden_hours":0.03,"gradual_days":0.97}),
]: add("D303","parkinson_disease",to,r,c)
s3["full_cpts"]["D303"] = {"parents":["R01"],"description":"パーキンソン病",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.0001,"18_39":0.0005,"40_64":0.003,"65_plus":0.008}}

# D304 レビー小体型認知症 (DLB)
s1["variables"].append({"id":"D304","name":"DLB","name_ja":"レビー小体型認知症(DLB)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"変動する認知障害+幻視+パーキンソニズム+REM睡眠行動障害。抗精神病薬過敏に注意"})
for to,r,c in [
    ("E16","DLB: 変動する認知障害(定義的)",{"normal":0.05,"confused":0.60,"obtunded":0.35}),
    ("S52","DLB: パーキンソニズム(60-70%)",{"absent":0.25,"unilateral_weakness":0.30,"bilateral":0.45}),
    ("S42","DLB: 失神/転倒(30-40%)",{"absent":0.55,"present":0.45}),
    ("S07","DLB: 倦怠感",{"absent":0.10,"mild":0.35,"severe":0.55}),
    ("T01","DLB: 慢性",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.10,"over_3w":0.85}),
    ("T02","DLB: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D304","DLB",to,r,c)
s3["full_cpts"]["D304"] = {"parents":["R01"],"description":"DLB",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.0,"18_39":0.0001,"40_64":0.001,"65_plus":0.004}}

# D305 急性硬膜外血腫 (Acute Epidural Hematoma)
s1["variables"].append({"id":"D305","name":"acute_epidural_hematoma","name_ja":"急性硬膜外血腫",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"側頭骨骨折→中硬膜動脈損傷→レンズ状血腫。意識清明期(lucid interval)→急速悪化。緊急開頭"})
for to,r,c in [
    ("E16","急性硬膜外: 意識障害(lucid interval後)",{"normal":0.10,"confused":0.30,"obtunded":0.60}),
    ("S05","急性硬膜外: 頭痛(70-80%)",{"absent":0.15,"mild":0.20,"severe":0.65}),
    ("S13","急性硬膜外: 嘔吐(50-60%)",{"absent":0.35,"present":0.65}),
    ("S52","急性硬膜外: 片麻痺(対側, 50-60%)",{"absent":0.30,"unilateral_weakness":0.60,"bilateral":0.10}),
    ("S42","急性硬膜外: 痙攣(20-30%)",{"absent":0.70,"present":0.30}),
    ("E02","急性硬膜外: 徐脈(Cushing反応)",{"under_100":0.55,"100_120":0.30,"over_120":0.15}),
    ("E38","急性硬膜外: 高血圧(Cushing反応)",{"normal_under_140":0.25,"elevated_140_180":0.35,"crisis_over_180":0.40}),
    ("T01","急性硬膜外: 超急性",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","急性硬膜外: 突発",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D305","acute_epidural_hematoma",to,r,c)
s3["full_cpts"]["D305"] = {"parents":["R01"],"description":"急性硬膜外血腫",
    "cpt":{"0_1":0.001,"1_5":0.001,"6_12":0.002,"13_17":0.003,"18_39":0.003,"40_64":0.002,"65_plus":0.002}}

# D306 急性硬膜下血腫 (Acute Subdural Hematoma)
s1["variables"].append({"id":"D306","name":"acute_subdural_hematoma","name_ja":"急性硬膜下血腫",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"架橋静脈断裂→三日月状血腫。高齢者/抗凝固薬/外傷。意識障害進行性。死亡率40-60%"})
for to,r,c in [
    ("E16","急性硬膜下: 意識障害(80%+)",{"normal":0.05,"confused":0.30,"obtunded":0.65}),
    ("S05","急性硬膜下: 頭痛(60-70%)",{"absent":0.20,"mild":0.20,"severe":0.60}),
    ("S52","急性硬膜下: 片麻痺(対側, 50-60%)",{"absent":0.30,"unilateral_weakness":0.55,"bilateral":0.15}),
    ("S42","急性硬膜下: 痙攣(15-20%)",{"absent":0.80,"present":0.20}),
    ("S13","急性硬膜下: 嘔吐(40-50%)",{"absent":0.45,"present":0.55}),
    ("E02","急性硬膜下: 徐脈(Cushing)",{"under_100":0.45,"100_120":0.35,"over_120":0.20}),
    ("E38","急性硬膜下: 高血圧(Cushing)",{"normal_under_140":0.30,"elevated_140_180":0.35,"crisis_over_180":0.35}),
    ("T01","急性硬膜下: 超急性",{"under_3d":0.80,"3d_to_1w":0.15,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","急性硬膜下: 突発~亜急性",{"sudden_hours":0.70,"gradual_days":0.30}),
]: add("D306","acute_subdural_hematoma",to,r,c)
s3["full_cpts"]["D306"] = {"parents":["R01"],"description":"急性硬膜下血腫。高齢者+抗凝固",
    "cpt":{"0_1":0.0005,"1_5":0.0005,"6_12":0.001,"13_17":0.002,"18_39":0.002,"40_64":0.003,"65_plus":0.005}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 306 diseases")
