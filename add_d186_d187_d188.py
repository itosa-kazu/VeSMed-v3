#!/usr/bin/env python3
"""Add D186 Cholangiocarcinoma + D187 Renal Infarction + D188 Splenic Infarction."""
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

# D186 腎梗塞 (Renal Infarction)
s1["variables"].append({"id":"D186","name":"renal_infarction","name_ja":"腎梗塞",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"腎動脈塞栓/血栓→側腹部痛+LDH著高+AKI。AF/IE/大動脈解離が塞栓源。虫垂炎/腎盂腎炎と誤診多い"})
for to,reason,cpt in [
    ("S15","腎梗塞: 側腹部痛/腰背部痛(突然, 90%+)",{"absent":0.05,"present":0.95}),
    ("S12","腎梗塞: 腹痛(側腹部, 70-80%)",{"absent":0.15,"epigastric":0.05,"RUQ":0.15,"RLQ":0.15,"LLQ":0.15,"suprapubic":0.05,"diffuse":0.30}),
    ("S13","腎梗塞: 嘔気/嘔吐(50-60%)",{"absent":0.35,"present":0.65}),
    ("E01","腎梗塞: 発熱(30-40%)",{"under_37.5":0.50,"37.5_38.0":0.20,"38.0_39.0":0.18,"39.0_40.0":0.10,"over_40.0":0.02}),
    ("L16","腎梗塞: LDH著高(90%+, 鑑別の鍵)",{"normal":0.05,"elevated":0.95}),
    ("L55","腎梗塞: AKI(60-70%)",{"normal":0.25,"mild_elevated":0.40,"high_AKI":0.35}),
    ("L01","腎梗塞: WBC上昇(50-60%)",{"low_under_4000":0.03,"normal_4000_10000":0.30,"high_10000_20000":0.45,"very_high_over_20000":0.22}),
    ("L02","腎梗塞: CRP上昇",{"normal_under_0.3":0.10,"mild_0.3_3":0.20,"moderate_3_10":0.40,"high_over_10":0.30}),
    ("T01","腎梗塞: 急性",{"under_3d":0.75,"3d_to_1w":0.20,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","腎梗塞: 突発",{"sudden_hours":0.80,"gradual_days":0.20}),
]:
    add("D186","renal_infarction",to,reason,cpt)
s3["full_cpts"]["D186"] = {"parents":["R01"],"description":"腎梗塞。AF/IE/解離が塞栓源",
    "cpt":{"18_39":0.001,"40_64":0.002,"65_plus":0.003}}

# D187 脾梗塞 (Splenic Infarction)
s1["variables"].append({"id":"D187","name":"splenic_infarction","name_ja":"脾梗塞",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"脾動脈塞栓→左上腹部痛/左肩放散痛(Kehr sign)。IE/AF/血液疾患が原因。LDH上昇"})
for to,reason,cpt in [
    ("S12","脾梗塞: 左上腹部痛/LUQ(90%+)",{"absent":0.05,"epigastric":0.05,"RUQ":0.02,"RLQ":0.02,"LLQ":0.75,"suprapubic":0.01,"diffuse":0.10}),
    ("E01","脾梗塞: 発熱(40-60%)",{"under_37.5":0.35,"37.5_38.0":0.20,"38.0_39.0":0.25,"39.0_40.0":0.15,"over_40.0":0.05}),
    ("L16","脾梗塞: LDH上昇(80%+)",{"normal":0.12,"elevated":0.88}),
    ("L01","脾梗塞: WBC上昇(白血球増多, 50-60%)",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.27}),
    ("L02","脾梗塞: CRP上昇",{"normal_under_0.3":0.08,"mild_0.3_3":0.15,"moderate_3_10":0.40,"high_over_10":0.37}),
    ("S13","脾梗塞: 嘔気(30-40%)",{"absent":0.55,"present":0.45}),
    ("T01","脾梗塞: 急性",{"under_3d":0.70,"3d_to_1w":0.22,"1w_to_3w":0.06,"over_3w":0.02}),
    ("T02","脾梗塞: 急性~亜急性",{"sudden_hours":0.65,"gradual_days":0.35}),
]:
    add("D187","splenic_infarction",to,reason,cpt)
s3["full_cpts"]["D187"] = {"parents":[],"description":"脾梗塞。IE/AF/血液疾患",
    "cpt":{"":0.001}}

# D188 好酸球性肺炎 (Eosinophilic Pneumonia)
s1["variables"].append({"id":"D188","name":"eosinophilic_pneumonia","name_ja":"好酸球性肺炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"急性(AEP):数日で呼吸不全、喫煙開始が誘因。慢性(CEP):数週~月、末梢浸潤(photonegative of PE)。BAL好酸球>25%"})
for to,reason,cpt in [
    ("S04","好酸球性肺炎: 呼吸困難(90%+)",{"absent":0.05,"on_exertion":0.20,"at_rest":0.75}),
    ("S01","好酸球性肺炎: 咳嗽(80%+)",{"absent":0.10,"dry":0.55,"productive":0.35}),
    ("E01","好酸球性肺炎: 発熱(70-80%)",{"under_37.5":0.15,"37.5_38.0":0.15,"38.0_39.0":0.35,"39.0_40.0":0.25,"over_40.0":0.10}),
    ("E07","好酸球性肺炎: 肺聴診(crackles)",{"clear":0.15,"crackles":0.65,"wheezes":0.15,"decreased_absent":0.05}),
    ("L04","好酸球性肺炎: CXR(両側浸潤/末梢優位)",{"normal":0.05,"lobar_infiltrate":0.05,"bilateral_infiltrate":0.80,"BHL":0.02,"pleural_effusion":0.06,"pneumothorax":0.02}),
    ("E04","好酸球性肺炎: 頻呼吸",{"normal_under_20":0.10,"tachypnea_20_30":0.40,"severe_over_30":0.50}),
    ("E05","好酸球性肺炎: 低酸素",{"normal_over_96":0.10,"mild_hypoxia_93_96":0.30,"severe_hypoxia_under_93":0.60}),
    ("L14","好酸球性肺炎: 末梢血好酸球増多(CEPで80%+, AEPでは初期正常→後に上昇)",
        {"normal":0.25,"left_shift":0.02,"atypical_lymphocytes":0.01,"thrombocytopenia":0.01,"eosinophilia":0.65,"lymphocyte_predominant":0.06}),
    ("L01","好酸球性肺炎: WBC上昇(好酸球優位)",{"low_under_4000":0.03,"normal_4000_10000":0.20,"high_10000_20000":0.45,"very_high_over_20000":0.32}),
    ("T01","好酸球性肺炎: AEP急性/CEP亜急性",{"under_3d":0.25,"3d_to_1w":0.30,"1w_to_3w":0.25,"over_3w":0.20}),
    ("T02","好酸球性肺炎: 亜急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]:
    add("D188","eosinophilic_pneumonia",to,reason,cpt)
s3["full_cpts"]["D188"] = {"parents":[],"description":"好酸球性肺炎。AEP/CEP",
    "cpt":{"":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"D186: 10e, D187: 8e, D188: 11e. Total: {s2['total_edges']} edges, 188 diseases")
