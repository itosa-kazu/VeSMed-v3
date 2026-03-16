#!/usr/bin/env python3
"""Add D347-D350: 4 diseases to reach 350."""
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

# D347 神経芽腫 (Neuroblastoma)
s1["variables"].append({"id":"D347","name":"neuroblastoma","name_ja":"神経芽腫",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"小児固形腫瘍で最多(副腎髄質/交感神経節)。腹部腫瘤+発熱+骨痛+眼周囲出血(パンダの目)。尿中VMA/HVA高値"})
for to,r,c in [
    ("S15","神経芽腫: 腹部腫瘤/腹痛(60-70%)",{"absent":0.20,"present":0.80}),
    ("E01","神経芽腫: 発熱(30-40%)",{"under_37.5":0.45,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.15,"over_40.0":0.05}),
    ("S07","神経芽腫: 倦怠感/体重減少(50-60%)",{"absent":0.25,"mild":0.30,"severe":0.45}),
    ("E38","神経芽腫: 高血圧(カテコラミン産生, 20-30%)",{"normal_under_140":0.55,"elevated_140_180":0.30,"crisis_over_180":0.15}),
    ("S44","神経芽腫: 出血傾向(骨髄浸潤, 15-20%)",{"absent":0.75,"present":0.25}),
    ("L01","神経芽腫: WBC変動",{"low_under_4000":0.10,"normal_4000_10000":0.35,"high_10000_20000":0.35,"very_high_over_20000":0.20}),
    ("T01","神経芽腫: 亜急性~慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.30,"over_3w":0.55}),
    ("T02","神経芽腫: 緩徐",{"sudden_hours":0.08,"gradual_days":0.92}),
]: add("D347","neuroblastoma",to,r,c)
s3["full_cpts"]["D347"] = {"parents":["R01"],"description":"神経芽腫。小児(特に5歳以下)",
    "cpt":{"0_1":0.005,"1_5":0.004,"6_12":0.001,"13_17":0.0003,"18_39":0.0001,"40_64":0.0001,"65_plus":0.0001}}

# D348 ウィルムス腫瘍 (Wilms Tumor/Nephroblastoma)
s1["variables"].append({"id":"D348","name":"wilms_tumor","name_ja":"ウィルムス腫瘍",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"小児腎腫瘍で最多(3-5歳)。腹部腫瘤(無症状で発見多い)+血尿+腹痛+高血圧。WAGR症候群/Beckwith-Wiedemann"})
for to,r,c in [
    ("S15","ウィルムス: 腹部腫瘤/腹痛(80%+)",{"absent":0.10,"present":0.90}),
    ("S44","ウィルムス: 血尿(20-25%)",{"absent":0.70,"present":0.30}),
    ("E38","ウィルムス: 高血圧(レニン産生, 25-30%)",{"normal_under_140":0.55,"elevated_140_180":0.30,"crisis_over_180":0.15}),
    ("E01","ウィルムス: 発熱(20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("S07","ウィルムス: 倦怠感(30-40%)",{"absent":0.45,"mild":0.30,"severe":0.25}),
    ("T01","ウィルムス: 亜急性~慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.25,"over_3w":0.60}),
    ("T02","ウィルムス: 緩徐",{"sudden_hours":0.08,"gradual_days":0.92}),
]: add("D348","wilms_tumor",to,r,c)
s3["full_cpts"]["D348"] = {"parents":["R01"],"description":"ウィルムス腫瘍。3-5歳",
    "cpt":{"0_1":0.001,"1_5":0.005,"6_12":0.001,"13_17":0.0002,"18_39":0.0001,"40_64":0.0,"65_plus":0.0}}

# D349 結核性胸膜炎 (Tuberculous Pleurisy)
s1["variables"].append({"id":"D349","name":"TB_pleurisy","name_ja":"結核性胸膜炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"結核菌の胸膜浸潤。若年者。片側性胸水+発熱+胸痛+咳嗽。胸水:リンパ球優位+ADA高値+蛋白高い(滲出性)"})
for to,r,c in [
    ("E01","結核性胸膜炎: 発熱(80-90%)",{"under_37.5":0.08,"37.5_38.0":0.12,"38.0_39.0":0.35,"39.0_40.0":0.30,"over_40.0":0.15}),
    ("S15","結核性胸膜炎: 胸痛(胸膜痛, 70-80%)",{"absent":0.15,"present":0.85}),
    ("S01","結核性胸膜炎: 咳嗽(50-60%)",{"absent":0.30,"dry":0.50,"productive":0.20}),
    ("S04","結核性胸膜炎: 呼吸困難(大量胸水, 40-50%)",{"absent":0.35,"on_exertion":0.40,"at_rest":0.25}),
    ("E07","結核性胸膜炎: 肺聴診(減弱/消失)",{"clear":0.10,"crackles":0.15,"wheezes":0.05,"decreased_absent":0.70}),
    ("L04","結核性胸膜炎: CXR(胸水)",{"normal":0.03,"lobar_infiltrate":0.05,"bilateral_infiltrate":0.07,"BHL":0.02,"pleural_effusion":0.80,"pneumothorax":0.03}),
    ("S07","結核性胸膜炎: 倦怠感/体重減少(60-70%)",{"absent":0.15,"mild":0.30,"severe":0.55}),
    ("L02","結核性胸膜炎: CRP上昇(70-80%)",{"normal_under_0.3":0.08,"mild_0.3_3":0.12,"moderate_3_10":0.40,"high_over_10":0.40}),
    ("L01","結核性胸膜炎: WBC正常~軽度上昇",{"low_under_4000":0.05,"normal_4000_10000":0.45,"high_10000_20000":0.35,"very_high_over_20000":0.15}),
    ("T01","結核性胸膜炎: 亜急性(1-3週)",{"under_3d":0.05,"3d_to_1w":0.15,"1w_to_3w":0.40,"over_3w":0.40}),
    ("T02","結核性胸膜炎: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D349","TB_pleurisy",to,r,c)
s3["full_cpts"]["D349"] = {"parents":["R01"],"description":"結核性胸膜炎。若年者~中年",
    "cpt":{"0_1":0.0002,"1_5":0.0003,"6_12":0.0005,"13_17":0.001,"18_39":0.002,"40_64":0.001,"65_plus":0.001}}

# D350 マルファン症候群 (Marfan Syndrome)
s1["variables"].append({"id":"D350","name":"marfan","name_ja":"マルファン症候群",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"FBN1変異→結合組織障害。高身長+くも状指+水晶体偏位+大動脈基部拡張→解離。僧帽弁逸脱。Ghent基準で診断"})
for to,r,c in [
    ("S15","マルファン: 胸痛/背部痛(大動脈拡張/解離, 30-40%)",{"absent":0.50,"present":0.50}),
    ("S04","マルファン: 呼吸困難(僧帽弁逸脱/気胸, 20-30%)",{"absent":0.55,"on_exertion":0.30,"at_rest":0.15}),
    ("S07","マルファン: 倦怠感/関節痛(30-40%)",{"absent":0.45,"mild":0.35,"severe":0.20}),
    ("E02","マルファン: 動悸/頻脈(MVP, 20-30%)",{"under_100":0.45,"100_120":0.35,"over_120":0.20}),
    ("T01","マルファン: 慢性(急性合併症あり)",{"under_3d":0.10,"3d_to_1w":0.10,"1w_to_3w":0.15,"over_3w":0.65}),
    ("T02","マルファン: 慢性(解離は突発)",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D350","marfan",to,r,c)
s3["full_cpts"]["D350"] = {"parents":["R01"],"description":"マルファン症候群。先天性。10-30歳で発症",
    "cpt":{"0_1":0.001,"1_5":0.002,"6_12":0.003,"13_17":0.003,"18_39":0.002,"40_64":0.001,"65_plus":0.0005}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"4 diseases added. Total: {s2['total_edges']} edges, 350 diseases")
