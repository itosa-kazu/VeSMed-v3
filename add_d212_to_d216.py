#!/usr/bin/env python3
"""Add D212-D216: 5 diseases."""
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

# D212 高浸透圧高血糖症候群 → already D157 HHS. Skip.
# D212 拘束型心筋症 (Restrictive Cardiomyopathy)
s1["variables"].append({"id":"D212","name":"restrictive_cardiomyopathy","name_ja":"拘束型心筋症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"心室壁硬化→拡張障害→うっ血性心不全。アミロイドーシス/サルコイドーシス/ヘモクロマトーシス等が原因"})
for to,r,c in [
    ("S04","拘束型心筋症: 呼吸困難(80%+)",{"absent":0.10,"on_exertion":0.50,"at_rest":0.40}),
    ("E36","拘束型心筋症: 浮腫(右心不全, 60-70%)",{"absent":0.20,"unilateral":0.05,"bilateral":0.75}),
    ("L51","拘束型心筋症: BNP上昇(心不全, 80%+)",{"not_done":0.10,"normal":0.05,"mildly_elevated":0.30,"very_high":0.55}),
    ("S07","拘束型心筋症: 倦怠感(80%+)",{"absent":0.08,"mild":0.30,"severe":0.62}),
    ("E02","拘束型心筋症: 頻脈/不整脈(AF多い)",{"under_100":0.25,"100_120":0.40,"over_120":0.35}),
    ("L04","拘束型心筋症: CXR(うっ血/胸水)",{"normal":0.20,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.25,"BHL":0.02,"pleural_effusion":0.48,"pneumothorax":0.03}),
    ("T01","拘束型心筋症: 慢性",{"under_3d":0.10,"3d_to_1w":0.15,"1w_to_3w":0.25,"over_3w":0.50}),
    ("T02","拘束型心筋症: 緩徐",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D212","restrictive_cardiomyopathy",to,r,c)
s3["full_cpts"]["D212"] = {"parents":["R01"],"description":"拘束型心筋症","cpt":{"18_39":0.0005,"40_64":0.001,"65_plus":0.002}}

# D213 収縮性心膜炎 (Constrictive Pericarditis)
s1["variables"].append({"id":"D213","name":"constrictive_pericarditis","name_ja":"収縮性心膜炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"心膜肥厚/石灰化→心室充満障害→右心不全優位。結核/手術後/放射線後。Kussmaul sign"})
for to,r,c in [
    ("S04","収縮性心膜炎: 呼吸困難(80%+)",{"absent":0.10,"on_exertion":0.55,"at_rest":0.35}),
    ("E36","収縮性心膜炎: 浮腫(右心不全, 70-80%)",{"absent":0.15,"unilateral":0.05,"bilateral":0.80}),
    ("S07","収縮性心膜炎: 倦怠感(70-80%)",{"absent":0.12,"mild":0.35,"severe":0.53}),
    ("L51","収縮性心膜炎: BNP上昇(心不全, 70%+)",{"not_done":0.10,"normal":0.10,"mildly_elevated":0.40,"very_high":0.40}),
    ("L04","収縮性心膜炎: CXR(心膜石灰化/胸水)",{"normal":0.25,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.15,"BHL":0.02,"pleural_effusion":0.53,"pneumothorax":0.03}),
    ("L11","収縮性心膜炎: 肝酵素(うっ血肝, 30-40%)",{"normal":0.50,"mild_elevated":0.35,"very_high":0.15}),
    ("T01","収縮性心膜炎: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","収縮性心膜炎: 緩徐",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D213","constrictive_pericarditis",to,r,c)
s3["full_cpts"]["D213"] = {"parents":[],"description":"収縮性心膜炎","cpt":{"":0.001}}

# D214 肺動脈性肺高血圧症 (PAH)
s1["variables"].append({"id":"D214","name":"PAH","name_ja":"肺動脈性肺高血圧症(PAH)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"肺動脈圧上昇→右心不全。特発性/CTD関連/先天性心疾患後。労作時呼吸困難+失神+胸痛"})
for to,r,c in [
    ("S04","PAH: 呼吸困難(労作時, 100%)",{"absent":0.02,"on_exertion":0.58,"at_rest":0.40}),
    ("E36","PAH: 浮腫(右心不全, 40-50%)",{"absent":0.40,"unilateral":0.05,"bilateral":0.55}),
    ("S21","PAH: 胸痛(労作時, 30-40%)",{"absent":0.55,"burning":0.03,"sharp":0.10,"pressure":0.28,"tearing":0.04}),
    ("S07","PAH: 倦怠感(70-80%)",{"absent":0.15,"mild":0.35,"severe":0.50}),
    ("E02","PAH: 頻脈(右心不全代償)",{"under_100":0.20,"100_120":0.45,"over_120":0.35}),
    ("L51","PAH: BNP上昇(右心不全, 80%+)",{"not_done":0.10,"normal":0.05,"mildly_elevated":0.30,"very_high":0.55}),
    ("E05","PAH: 低酸素(40-50%)",{"normal_over_96":0.35,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.30}),
    ("T01","PAH: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","PAH: 緩徐",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D214","PAH",to,r,c)
s3["full_cpts"]["D214"] = {"parents":["R02"],"description":"PAH。女性に多い","cpt":{"male":0.0005,"female":0.001}}

# D215 急性大動脈弁閉鎖不全症 (Acute Aortic Regurgitation)
s1["variables"].append({"id":"D215","name":"acute_aortic_regurgitation","name_ja":"急性大動脈弁閉鎖不全症",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"IE/大動脈解離/外傷→急性AR→急性左心不全→肺水腫。慢性ARと異なり代償なし→緊急手術"})
for to,r,c in [
    ("S04","急性AR: 呼吸困難(肺水腫, 100%)",{"absent":0.02,"on_exertion":0.10,"at_rest":0.88}),
    ("E02","急性AR: 頻脈(代償, 90%+)",{"under_100":0.05,"100_120":0.30,"over_120":0.65}),
    ("E03","急性AR: 低血圧(心拍出量低下)",{"normal_over_90":0.20,"hypotension_under_90":0.80}),
    ("E07","急性AR: 肺聴診(crackles/肺水腫)",{"clear":0.05,"crackles":0.80,"wheezes":0.10,"decreased_absent":0.05}),
    ("L04","急性AR: CXR(肺うっ血/肺水腫)",{"normal":0.05,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.70,"BHL":0.01,"pleural_effusion":0.20,"pneumothorax":0.02}),
    ("L51","急性AR: BNP著高(急性心不全)",{"not_done":0.05,"normal":0.03,"mildly_elevated":0.12,"very_high":0.80}),
    ("E01","急性AR: 発熱(IE原因時, 30-50%)",{"under_37.5":0.40,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("T01","急性AR: 超急性",{"under_3d":0.80,"3d_to_1w":0.15,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","急性AR: 突発",{"sudden_hours":0.80,"gradual_days":0.20}),
]: add("D215","acute_aortic_regurgitation",to,r,c)
s3["full_cpts"]["D215"] = {"parents":["R01"],"description":"急性AR","cpt":{"18_39":0.0005,"40_64":0.001,"65_plus":0.002}}

# D216 僧帽弁狭窄症 → 慢性すぎて急性診断に不向き。代わりに：
# D216 急性僧帽弁閉鎖不全(Acute MR) - 腱索断裂/IE/MI後
s1["variables"].append({"id":"D216","name":"acute_mitral_regurgitation","name_ja":"急性僧帽弁閉鎖不全症",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"腱索断裂(IE/MIなど)→急性肺水腫→心原性ショック。緊急手術"})
for to,r,c in [
    ("S04","急性MR: 呼吸困難(肺水腫, 100%)",{"absent":0.02,"on_exertion":0.08,"at_rest":0.90}),
    ("E02","急性MR: 頻脈(90%+)",{"under_100":0.05,"100_120":0.30,"over_120":0.65}),
    ("E03","急性MR: 低血圧(心原性ショック)",{"normal_over_90":0.15,"hypotension_under_90":0.85}),
    ("E07","急性MR: 肺聴診(crackles+収縮期雑音)",{"clear":0.03,"crackles":0.82,"wheezes":0.10,"decreased_absent":0.05}),
    ("L04","急性MR: CXR(肺水腫/胸水)",{"normal":0.05,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.65,"BHL":0.01,"pleural_effusion":0.25,"pneumothorax":0.02}),
    ("L51","急性MR: BNP著高",{"not_done":0.05,"normal":0.02,"mildly_elevated":0.10,"very_high":0.83}),
    ("L53","急性MR: トロポニン上昇(MI原因時)",{"not_done":0.10,"normal":0.25,"mildly_elevated":0.35,"very_high":0.30}),
    ("T01","急性MR: 超急性",{"under_3d":0.85,"3d_to_1w":0.12,"1w_to_3w":0.02,"over_3w":0.01}),
    ("T02","急性MR: 突発",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D216","acute_mitral_regurgitation",to,r,c)
s3["full_cpts"]["D216"] = {"parents":["R01"],"description":"急性MR","cpt":{"18_39":0.0003,"40_64":0.001,"65_plus":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 216 diseases")
