#!/usr/bin/env python3
"""Add D342-D346: 5 diseases."""
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

# D342 QT延長症候群 (Long QT Syndrome)
s1["variables"].append({"id":"D342","name":"LQTS","name_ja":"QT延長症候群",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"先天性(KCNQ1/KCNH2/SCN5A変異)or薬剤性。QTc延長→TdP→失神/突然死。運動/精神的ストレス/睡眠中に発作"})
for to,r,c in [
    ("S42","LQTS: 失神/痙攣(TdP, 40-50%)",{"absent":0.40,"present":0.60}),
    ("E16","LQTS: 意識消失(TdP, 40-50%)",{"normal":0.35,"confused":0.25,"obtunded":0.40}),
    ("E02","LQTS: 不整脈(TdP/VF)",{"under_100":0.25,"100_120":0.20,"over_120":0.55}),
    ("T01","LQTS: 突発(発作)",{"under_3d":0.85,"3d_to_1w":0.10,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","LQTS: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D342","LQTS",to,r,c)
s3["full_cpts"]["D342"] = {"parents":["R01","R02"],"description":"QT延長症候群。若年女性にやや多い",
    "cpt":{"0_1,male":0.0005,"0_1,female":0.0005,"1_5,male":0.001,"1_5,female":0.001,"6_12,male":0.001,"6_12,female":0.002,"13_17,male":0.001,"13_17,female":0.002,"18_39,male":0.001,"18_39,female":0.002,"40_64,male":0.001,"40_64,female":0.001,"65_plus,male":0.0005,"65_plus,female":0.0005}}

# D343 たこつぼ心筋症 (Takotsubo Cardiomyopathy)
s1["variables"].append({"id":"D343","name":"takotsubo","name_ja":"たこつぼ心筋症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"精神的/身体的ストレス→左室心尖部無動(ballooning)。閉経後女性。AMIに酷似するが冠動脈正常。トロポニン軽度上昇"})
for to,r,c in [
    ("S04","たこつぼ: 呼吸困難(50-60%)",{"absent":0.25,"on_exertion":0.30,"at_rest":0.45}),
    ("S15","たこつぼ: 胸痛(70-80%)",{"absent":0.15,"present":0.85}),
    ("E02","たこつぼ: 頻脈(50-60%)",{"under_100":0.25,"100_120":0.40,"over_120":0.35}),
    ("E38","たこつぼ: 血圧低下~正常",{"normal_under_140":0.55,"elevated_140_180":0.30,"crisis_over_180":0.15}),
    ("L51","たこつぼ: BNP上昇(80%+)",{"not_done":0.10,"normal":0.05,"mildly_elevated":0.30,"very_high":0.55}),
    ("S07","たこつぼ: 倦怠感(40-50%)",{"absent":0.35,"mild":0.35,"severe":0.30}),
    ("T01","たこつぼ: 急性",{"under_3d":0.70,"3d_to_1w":0.20,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","たこつぼ: 突発",{"sudden_hours":0.75,"gradual_days":0.25}),
]: add("D343","takotsubo",to,r,c)
s3["full_cpts"]["D343"] = {"parents":["R01","R02"],"description":"たこつぼ心筋症。閉経後女性",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0001,"18_39,male":0.0003,"18_39,female":0.0005,"40_64,male":0.0005,"40_64,female":0.002,"65_plus,male":0.001,"65_plus,female":0.004}}

# D344 収縮性心膜炎 (Constrictive Pericarditis)
s1["variables"].append({"id":"D344","name":"constrictive_pericarditis","name_ja":"収縮性心膜炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"心膜肥厚/石灰化→心室拡張障害。結核/術後/放射線/特発性。右心不全症状:頸静脈怒張+肝腫大+腹水+浮腫。Kussmaul徴候"})
for to,r,c in [
    ("E36","収縮性心膜炎: 下肢浮腫(右心不全, 70-80%)",{"absent":0.15,"unilateral":0.05,"bilateral":0.80}),
    ("S04","収縮性心膜炎: 呼吸困難(60-70%)",{"absent":0.20,"on_exertion":0.50,"at_rest":0.30}),
    ("S07","収縮性心膜炎: 倦怠感(60-70%)",{"absent":0.15,"mild":0.35,"severe":0.50}),
    ("S15","収縮性心膜炎: 腹部膨満/腹痛(腹水, 40-50%)",{"absent":0.40,"present":0.60}),
    ("L51","収縮性心膜炎: BNP上昇(軽度~中等度)",{"not_done":0.15,"normal":0.20,"mildly_elevated":0.45,"very_high":0.20}),
    ("L11","収縮性心膜炎: 肝酵素上昇(うっ血肝, 30-40%)",{"normal":0.45,"mild_elevated":0.35,"very_high":0.20}),
    ("T01","収縮性心膜炎: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.15,"over_3w":0.75}),
    ("T02","収縮性心膜炎: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D344","constrictive_pericarditis",to,r,c)
s3["full_cpts"]["D344"] = {"parents":["R01"],"description":"収縮性心膜炎",
    "cpt":{"0_1":0.0001,"1_5":0.0001,"6_12":0.0002,"13_17":0.0003,"18_39":0.001,"40_64":0.002,"65_plus":0.002}}

# D345 Sheehan症候群
s1["variables"].append({"id":"D345","name":"sheehan","name_ja":"Sheehan症候群",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"分娩時大量出血→下垂体壊死→汎下垂体機能低下。乳汁分泌不全+無月経+倦怠感+低血圧+低Na。産後数日~数週で発症"})
for to,r,c in [
    ("S07","Sheehan: 倦怠感(80%+)",{"absent":0.05,"mild":0.20,"severe":0.75}),
    ("E38","Sheehan: 低血圧(副腎不全, 60-70%)",{"normal_under_140":0.85,"elevated_140_180":0.12,"crisis_over_180":0.03}),
    ("L44","Sheehan: 低Na血症(40-50%)",{"normal":0.35,"hyponatremia":0.55,"hyperkalemia":0.02,"other":0.08}),
    ("S13","Sheehan: 嘔気嘔吐(副腎不全, 30-40%)",{"absent":0.55,"present":0.45}),
    ("E16","Sheehan: 意識障害(低Na/低血糖, 20-30%)",{"normal":0.55,"confused":0.30,"obtunded":0.15}),
    ("E01","Sheehan: 低体温(甲状腺低下)",{"under_37.5":0.75,"37.5_38.0":0.15,"38.0_39.0":0.08,"39.0_40.0":0.02,"over_40.0":0.00}),
    ("L56","Sheehan: β-hCG(産後で低下)",{"not_done":0.20,"negative":0.60,"positive":0.20}),
    ("T01","Sheehan: 亜急性~慢性(産後)",{"under_3d":0.10,"3d_to_1w":0.20,"1w_to_3w":0.30,"over_3w":0.40}),
    ("T02","Sheehan: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D345","sheehan",to,r,c)
s3["full_cpts"]["D345"] = {"parents":["R01","R02"],"description":"Sheehan症候群。産後女性のみ",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0001,"18_39,male":0.0,"18_39,female":0.001,"40_64,male":0.0,"40_64,female":0.0005,"65_plus,male":0.0,"65_plus,female":0.0}}

# D346 肥大型心筋症 (HCM/HOCM)
s1["variables"].append({"id":"D346","name":"HCM","name_ja":"肥大型心筋症(HCM)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"心室中隔の非対称性肥大。閉塞性(HOCM)は流出路狭窄→失神。若年突然死の原因。労作時呼吸困難+胸痛+失神+動悸"})
for to,r,c in [
    ("S04","HCM: 呼吸困難(50-60%)",{"absent":0.25,"on_exertion":0.50,"at_rest":0.25}),
    ("S15","HCM: 胸痛(30-40%)",{"absent":0.50,"present":0.50}),
    ("S42","HCM: 失神(15-25%)",{"absent":0.70,"present":0.30}),
    ("E02","HCM: 動悸/不整脈(30-40%)",{"under_100":0.35,"100_120":0.35,"over_120":0.30}),
    ("S07","HCM: 倦怠感(40-50%)",{"absent":0.35,"mild":0.40,"severe":0.25}),
    ("L51","HCM: BNP上昇(拡張障害)",{"not_done":0.15,"normal":0.25,"mildly_elevated":0.40,"very_high":0.20}),
    ("T01","HCM: 慢性(急性イベントあり)",{"under_3d":0.15,"3d_to_1w":0.15,"1w_to_3w":0.15,"over_3w":0.55}),
    ("T02","HCM: 緩徐(失神は突発)",{"sudden_hours":0.25,"gradual_days":0.75}),
]: add("D346","HCM",to,r,c)
s3["full_cpts"]["D346"] = {"parents":["R01"],"description":"HCM。全年齢。若年突然死",
    "cpt":{"0_1":0.0003,"1_5":0.0005,"6_12":0.001,"13_17":0.002,"18_39":0.002,"40_64":0.002,"65_plus":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 346 diseases")
