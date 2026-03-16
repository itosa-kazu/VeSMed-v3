#!/usr/bin/env python3
"""Add D312-D316: 5 diseases."""
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

# D312 髄膜腫 (Meningioma)
s1["variables"].append({"id":"D312","name":"meningioma","name_ja":"髄膜腫",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"最も頻度の高い脳腫瘍(良性多い)。無症状~頭痛/痙攣/局所神経症状。中年女性に多い"})
for to,r,c in [
    ("S05","髄膜腫: 頭痛(40-60%)",{"absent":0.30,"mild":0.30,"severe":0.40}),
    ("S42","髄膜腫: 痙攣(25-40%)",{"absent":0.55,"present":0.45}),
    ("S52","髄膜腫: 局所神経脱落(30-40%)",{"absent":0.50,"unilateral_weakness":0.40,"bilateral":0.10}),
    ("E16","髄膜腫: 認知変化(20-30%)",{"normal":0.55,"confused":0.30,"obtunded":0.15}),
    ("S07","髄膜腫: 倦怠感",{"absent":0.35,"mild":0.40,"severe":0.25}),
    ("T01","髄膜腫: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","髄膜腫: 緩徐",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D312","meningioma",to,r,c)
s3["full_cpts"]["D312"] = {"parents":["R01","R02"],"description":"髄膜腫。中年女性",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0001,"1_5,female":0.0001,"6_12,male":0.0002,"6_12,female":0.0003,"13_17,male":0.0003,"13_17,female":0.0005,"18_39,male":0.001,"18_39,female":0.002,"40_64,male":0.002,"40_64,female":0.004,"65_plus,male":0.002,"65_plus,female":0.004}}

# D313 転移性脳腫瘍 (Brain Metastasis)
s1["variables"].append({"id":"D313","name":"brain_metastasis","name_ja":"転移性脳腫瘍",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"肺癌/乳癌/腎癌/大腸癌/黒色腫が原発巣として多い。頭痛+痙攣+局所神経症状+認知障害"})
for to,r,c in [
    ("S05","脳転移: 頭痛(40-50%)",{"absent":0.35,"mild":0.20,"severe":0.45}),
    ("S42","脳転移: 痙攣(20-35%)",{"absent":0.60,"present":0.40}),
    ("S52","脳転移: 局所神経脱落(40-50%)",{"absent":0.35,"unilateral_weakness":0.50,"bilateral":0.15}),
    ("E16","脳転移: 意識障害(30-40%)",{"normal":0.40,"confused":0.35,"obtunded":0.25}),
    ("S13","脳転移: 嘔吐(頭蓋内圧亢進, 25-35%)",{"absent":0.60,"present":0.40}),
    ("S07","脳転移: 倦怠感/体重減少",{"absent":0.10,"mild":0.30,"severe":0.60}),
    ("T01","脳転移: 亜急性~慢性",{"under_3d":0.10,"3d_to_1w":0.15,"1w_to_3w":0.30,"over_3w":0.45}),
    ("T02","脳転移: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D313","brain_metastasis",to,r,c)
s3["full_cpts"]["D313"] = {"parents":["R01"],"description":"転移性脳腫瘍",
    "cpt":{"0_1":0.0,"1_5":0.0001,"6_12":0.0002,"13_17":0.0003,"18_39":0.001,"40_64":0.004,"65_plus":0.005}}

# D314 水頭症(急性閉塞性) (Acute Obstructive Hydrocephalus)
s1["variables"].append({"id":"D314","name":"acute_hydrocephalus","name_ja":"急性閉塞性水頭症",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"脳室系閉塞→急速な頭蓋内圧亢進。頭痛+嘔吐+意識障害+上方注視麻痺。緊急脳室ドレナージ"})
for to,r,c in [
    ("S05","急性水頭症: 頭痛(激烈, 80%+)",{"absent":0.08,"mild":0.12,"severe":0.80}),
    ("S13","急性水頭症: 嘔吐(噴射性, 70-80%)",{"absent":0.15,"present":0.85}),
    ("E16","急性水頭症: 意識障害(急速進行)",{"normal":0.10,"confused":0.35,"obtunded":0.55}),
    ("E02","急性水頭症: 徐脈(Cushing反応)",{"under_100":0.55,"100_120":0.30,"over_120":0.15}),
    ("E38","急性水頭症: 高血圧(Cushing)",{"normal_under_140":0.20,"elevated_140_180":0.35,"crisis_over_180":0.45}),
    ("T01","急性水頭症: 超急性",{"under_3d":0.75,"3d_to_1w":0.18,"1w_to_3w":0.05,"over_3w":0.02}),
    ("T02","急性水頭症: 急性",{"sudden_hours":0.65,"gradual_days":0.35}),
]: add("D314","acute_hydrocephalus",to,r,c)
s3["full_cpts"]["D314"] = {"parents":["R01"],"description":"急性閉塞性水頭症",
    "cpt":{"0_1":0.002,"1_5":0.002,"6_12":0.001,"13_17":0.001,"18_39":0.001,"40_64":0.002,"65_plus":0.003}}

# D315 脳静脈洞血栓症 (Cerebral Venous Sinus Thrombosis)
s1["variables"].append({"id":"D315","name":"CVST","name_ja":"脳静脈洞血栓症(CVST)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"経口避妊薬/妊娠/脱水/感染/凝固異常。頭痛(最多)+痙攣+局所神経症状+乳頭浮腫"})
for to,r,c in [
    ("S05","CVST: 頭痛(90%+, 進行性)",{"absent":0.05,"mild":0.10,"severe":0.85}),
    ("S42","CVST: 痙攣(30-40%)",{"absent":0.55,"present":0.45}),
    ("S52","CVST: 局所神経脱落(30-40%)",{"absent":0.50,"unilateral_weakness":0.40,"bilateral":0.10}),
    ("E16","CVST: 意識障害(30-50%)",{"normal":0.35,"confused":0.35,"obtunded":0.30}),
    ("S13","CVST: 嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("L52","CVST: D-dimer上昇(80%+)",{"not_done":0.10,"normal":0.05,"mildly_elevated":0.20,"very_high":0.65}),
    ("E01","CVST: 発熱(感染性CVSTで, 20-30%)",{"under_37.5":0.55,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.05}),
    ("T01","CVST: 急性~亜急性",{"under_3d":0.30,"3d_to_1w":0.30,"1w_to_3w":0.25,"over_3w":0.15}),
    ("T02","CVST: 亜急性",{"sudden_hours":0.25,"gradual_days":0.75}),
]: add("D315","CVST",to,r,c)
s3["full_cpts"]["D315"] = {"parents":["R01","R02"],"description":"CVST。若年女性(OC/妊娠)",
    "cpt":{"0_1,male":0.0002,"0_1,female":0.0003,"1_5,male":0.0003,"1_5,female":0.0005,"6_12,male":0.0005,"6_12,female":0.001,"13_17,male":0.001,"13_17,female":0.002,"18_39,male":0.001,"18_39,female":0.003,"40_64,male":0.001,"40_64,female":0.002,"65_plus,male":0.001,"65_plus,female":0.001}}

# D316 もやもや病 (Moyamoya Disease)
s1["variables"].append({"id":"D316","name":"moyamoya","name_ja":"もやもや病",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"内頸動脈遠位部の進行性狭窄+異常血管網。日本人に多い。小児:TIA/脳梗塞、成人:脳出血"})
for to,r,c in [
    ("S52","もやもや: 局所神経脱落(TIA/梗塞/出血)",{"absent":0.15,"unilateral_weakness":0.65,"bilateral":0.20}),
    ("S05","もやもや: 頭痛(30-50%)",{"absent":0.35,"mild":0.25,"severe":0.40}),
    ("S42","もやもや: 痙攣(10-20%)",{"absent":0.75,"present":0.25}),
    ("E16","もやもや: 意識障害(出血時, 30-40%)",{"normal":0.40,"confused":0.30,"obtunded":0.30}),
    ("S53","もやもや: 構音障害/失語(30-40%)",{"absent":0.50,"dysarthria":0.35,"aphasia":0.15}),
    ("T01","もやもや: 急性(TIA/梗塞/出血)",{"under_3d":0.60,"3d_to_1w":0.25,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","もやもや: 突発~亜急性",{"sudden_hours":0.55,"gradual_days":0.45}),
]: add("D316","moyamoya",to,r,c)
s3["full_cpts"]["D316"] = {"parents":["R01"],"description":"もやもや病。日本人に多い。二峰性(小児+成人)",
    "cpt":{"0_1":0.0005,"1_5":0.002,"6_12":0.003,"13_17":0.002,"18_39":0.002,"40_64":0.003,"65_plus":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 316 diseases")
