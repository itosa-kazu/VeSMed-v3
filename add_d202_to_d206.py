#!/usr/bin/env python3
"""Add D202-D206: 5 diseases."""
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

# D202 シェーグレン症候群
s1["variables"].append({"id":"D202","name":"sjogren_syndrome","name_ja":"シェーグレン症候群",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"乾燥症候群(sicca). 乾燥性角結膜炎+口腔乾燥+関節痛. 腺外症状:ILD/腎/神経. 抗SSA/SSB抗体"})
for to,r,c in [
    ("S08","シェーグレン: 関節痛(50-60%)",{"absent":0.35,"present":0.65}),
    ("S07","シェーグレン: 倦怠感(70-80%)",{"absent":0.15,"mild":0.40,"severe":0.45}),
    ("E01","シェーグレン: 発熱(腺外症状時, 15-20%)",{"under_37.5":0.75,"37.5_38.0":0.10,"38.0_39.0":0.10,"39.0_40.0":0.04,"over_40.0":0.01}),
    ("S01","シェーグレン: 咳嗽(ILD合併, 20-30%)",{"absent":0.65,"dry":0.28,"productive":0.07}),
    ("L02","シェーグレン: CRP(通常正常~軽度)",{"normal_under_0.3":0.35,"mild_0.3_3":0.30,"moderate_3_10":0.25,"high_over_10":0.10}),
    ("L05","シェーグレン: 尿異常(間質性腎炎, 10-20%)",{"normal":0.80,"pyuria_bacteriuria":0.20}),
    ("T01","シェーグレン: 慢性",{"under_3d":0.03,"3d_to_1w":0.05,"1w_to_3w":0.12,"over_3w":0.80}),
    ("T02","シェーグレン: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D202","sjogren_syndrome",to,r,c)
s3["full_cpts"]["D202"] = {"parents":["R02"],"description":"シェーグレン. 女性に多い(F:M=9:1)",
    "cpt":{"male":0.0003,"female":0.003}}

# D203 全身性強皮症 (Systemic Sclerosis)
s1["variables"].append({"id":"D203","name":"systemic_sclerosis","name_ja":"全身性強皮症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"皮膚硬化+レイノー現象+ILD+肺高血圧+腎クリーゼ. 抗Scl-70/抗セントロメア抗体"})
for to,r,c in [
    ("S04","強皮症: 呼吸困難(ILD, 40-60%)",{"absent":0.35,"on_exertion":0.40,"at_rest":0.25}),
    ("S07","強皮症: 倦怠感(70-80%)",{"absent":0.15,"mild":0.40,"severe":0.45}),
    ("S08","強皮症: 関節痛(40-50%)",{"absent":0.45,"present":0.55}),
    ("E38","強皮症: 高血圧(腎クリーゼ, 10-20%)",{"normal_under_140":0.60,"elevated_140_180":0.25,"crisis_over_180":0.15}),
    ("L04","強皮症: CXR(ILD, 40-60%)",{"normal":0.40,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.45,"BHL":0.02,"pleural_effusion":0.08,"pneumothorax":0.03}),
    ("L55","強皮症: AKI(腎クリーゼ, 5-10%)",{"normal":0.80,"mild_elevated":0.12,"high_AKI":0.08}),
    ("T01","強皮症: 慢性",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.10,"over_3w":0.85}),
    ("T02","強皮症: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D203","systemic_sclerosis",to,r,c)
s3["full_cpts"]["D203"] = {"parents":["R02"],"description":"強皮症. 女性に多い(F:M=4:1)",
    "cpt":{"male":0.0003,"female":0.001}}

# D204 急性HIV感染症(既にD44があるが確認) → D44は急性HIV. スキップ。
# D204 多系統萎縮症ではない → 急性でないから除外
# D204 アミロイドーシス
s1["variables"].append({"id":"D204","name":"amyloidosis","name_ja":"アミロイドーシス",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"異常蛋白沈着. AL型(形質細胞)/AA型(炎症性). 心不全+腎症候群+神経障害+肝腫大+巨舌"})
for to,r,c in [
    ("S04","アミロイドーシス: 呼吸困難(心不全, 40-50%)",{"absent":0.40,"on_exertion":0.40,"at_rest":0.20}),
    ("S07","アミロイドーシス: 倦怠感(80%+)",{"absent":0.08,"mild":0.30,"severe":0.62}),
    ("E36","アミロイドーシス: 浮腫(ネフローゼ/心不全, 50-60%)",{"absent":0.30,"unilateral":0.05,"bilateral":0.65}),
    ("L05","アミロイドーシス: 尿異常(蛋白尿, 60-70%)",{"normal":0.25,"pyuria_bacteriuria":0.75}),
    ("L55","アミロイドーシス: AKI(腎アミロイド, 30-40%)",{"normal":0.40,"mild_elevated":0.35,"high_AKI":0.25}),
    ("L51","アミロイドーシス: BNP上昇(心アミロイド, 50-60%)",{"not_done":0.15,"normal":0.15,"mildly_elevated":0.30,"very_high":0.40}),
    ("L53","アミロイドーシス: トロポニン上昇(心, 40-50%)",{"not_done":0.15,"normal":0.25,"mildly_elevated":0.40,"very_high":0.20}),
    ("T01","アミロイドーシス: 慢性",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.10,"over_3w":0.85}),
    ("T02","アミロイドーシス: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D204","amyloidosis",to,r,c)
s3["full_cpts"]["D204"] = {"parents":["R01"],"description":"アミロイドーシス. 中高年",
    "cpt":{"18_39":0.0005,"40_64":0.001,"65_plus":0.002}}

# D205 エチレングリコール中毒
s1["variables"].append({"id":"D205","name":"ethylene_glycol_poisoning","name_ja":"エチレングリコール中毒",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"不凍液. 代謝性アシドーシス(AG開大)+浸透圧gap+AKI(蓚酸カルシウム結晶). メタノールと鑑別"})
for to,r,c in [
    ("E16","エチレングリコール: 意識障害(酩酊→昏睡)",{"normal":0.15,"confused":0.40,"obtunded":0.45}),
    ("S13","エチレングリコール: 嘔気/嘔吐(70-80%)",{"absent":0.15,"present":0.85}),
    ("E04","エチレングリコール: 頻呼吸(Kussmaul, アシドーシス代償)",{"normal_under_20":0.10,"tachypnea_20_30":0.35,"severe_over_30":0.55}),
    ("L55","エチレングリコール: AKI(蓚酸腎, Stage II-III)",{"normal":0.10,"mild_elevated":0.25,"high_AKI":0.65}),
    ("E02","エチレングリコール: 頻脈",{"under_100":0.20,"100_120":0.40,"over_120":0.40}),
    ("S42","エチレングリコール: 痙攣(低Ca, 20-30%)",{"absent":0.70,"present":0.30}),
    ("T01","エチレングリコール: 超急性",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","エチレングリコール: 急性",{"sudden_hours":0.80,"gradual_days":0.20}),
]: add("D205","ethylene_glycol_poisoning",to,r,c)
s3["full_cpts"]["D205"] = {"parents":[],"description":"エチレングリコール中毒","cpt":{"":0.0005}}

# D206 肥大型心筋症 (HCM)
s1["variables"].append({"id":"D206","name":"HCM","name_ja":"肥大型心筋症(HCM)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"非対称性中隔肥大. 労作時呼吸困難+失神+胸痛+突然死リスク. LVOT obstruction. 若年突然死の原因"})
for to,r,c in [
    ("S04","HCM: 呼吸困難(労作時, 60-70%)",{"absent":0.20,"on_exertion":0.60,"at_rest":0.20}),
    ("S21","HCM: 胸痛(40-50%)",{"absent":0.45,"burning":0.05,"sharp":0.10,"pressure":0.35,"tearing":0.05}),
    ("E02","HCM: 頻脈/不整脈(30-40%)",{"under_100":0.40,"100_120":0.35,"over_120":0.25}),
    ("E03","HCM: 低血圧(LVOT閉塞時)",{"normal_over_90":0.60,"hypotension_under_90":0.40}),
    ("L53","HCM: トロポニン上昇(心筋障害, 20-30%)",{"not_done":0.15,"normal":0.40,"mildly_elevated":0.35,"very_high":0.10}),
    ("L51","HCM: BNP上昇(拡張障害, 50-60%)",{"not_done":0.15,"normal":0.20,"mildly_elevated":0.40,"very_high":0.25}),
    ("T01","HCM: 慢性(急性増悪で来院)",{"under_3d":0.25,"3d_to_1w":0.25,"1w_to_3w":0.25,"over_3w":0.25}),
    ("T02","HCM: 急性~慢性",{"sudden_hours":0.35,"gradual_days":0.65}),
]: add("D206","HCM",to,r,c)
s3["full_cpts"]["D206"] = {"parents":["R01"],"description":"HCM. 若年~中年",
    "cpt":{"18_39":0.002,"40_64":0.002,"65_plus":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 206 diseases")
