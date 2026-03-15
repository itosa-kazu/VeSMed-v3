#!/usr/bin/env python3
"""Add D267-D271: 5 diseases."""
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

# D267 モラクセラ肺炎 (Moraxella catarrhalis Pneumonia)
s1["variables"].append({"id":"D267","name":"moraxella_pneumonia","name_ja":"モラクセラ肺炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"COPD/高齢者に多い第3の市中肺炎菌。湿性咳嗽+膿性痰。βラクタマーゼ産生"})
for to,r,c in [
    ("S01","モラクセラ: 湿性咳嗽",{"absent":0.08,"dry":0.15,"productive":0.77}),
    ("E01","モラクセラ: 発熱(70-80%)",{"under_37.5":0.15,"37.5_38.0":0.15,"38.0_39.0":0.35,"39.0_40.0":0.25,"over_40.0":0.10}),
    ("E07","モラクセラ: crackles",{"clear":0.10,"crackles":0.70,"wheezes":0.12,"decreased_absent":0.08}),
    ("L04","モラクセラ: CXR(斑状浸潤)",{"normal":0.08,"lobar_infiltrate":0.30,"bilateral_infiltrate":0.45,"BHL":0.02,"pleural_effusion":0.10,"pneumothorax":0.05}),
    ("S04","モラクセラ: 呼吸困難",{"absent":0.25,"on_exertion":0.35,"at_rest":0.40}),
    ("E04","モラクセラ: 頻呼吸",{"normal_under_20":0.15,"tachypnea_20_30":0.40,"severe_over_30":0.45}),
    ("L01","モラクセラ: WBC上昇",{"low_under_4000":0.05,"normal_4000_10000":0.20,"high_10000_20000":0.45,"very_high_over_20000":0.30}),
    ("L02","モラクセラ: CRP上昇",{"normal_under_0.3":0.05,"mild_0.3_3":0.10,"moderate_3_10":0.30,"high_over_10":0.55}),
    ("T01","モラクセラ: 急性",{"under_3d":0.35,"3d_to_1w":0.40,"1w_to_3w":0.20,"over_3w":0.05}),
    ("T02","モラクセラ: 急性",{"sudden_hours":0.25,"gradual_days":0.75}),
]: add("D267","moraxella_pneumonia",to,r,c)
s3["full_cpts"]["D267"] = {"parents":["R01"],"description":"モラクセラ肺炎",
    "cpt":{"0_1":0.002,"1_5":0.002,"6_12":0.001,"13_17":0.001,"18_39":0.002,"40_64":0.003,"65_plus":0.005}}

# D268 CMV肺炎 → already D41 CMV exists. Needs differentiation.
# D268 サイトメガロウイルス肺炎 is a specific presentation of D41.
# Better: D268 ノロウイルス胃腸炎 (Norovirus Gastroenteritis)
s1["variables"].append({"id":"D268","name":"norovirus","name_ja":"ノロウイルス胃腸炎",
    "category":"disease","states":["no","yes"],"severity":"low",
    "note":"冬季流行。突然の嘔吐+水様下痢。高度感染性(10-100粒子で感染)。自然軽快(1-3日)"})
for to,r,c in [
    ("S13","ノロ: 嘔吐(90%+)",{"absent":0.05,"present":0.95}),
    ("S14","ノロ: 水様下痢(70-80%)",{"absent":0.10,"watery":0.85,"bloody":0.05}),
    ("S12","ノロ: 腹痛(50-60%)",{"absent":0.30,"epigastric":0.25,"RUQ":0.02,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.02,"diffuse":0.37}),
    ("E01","ノロ: 発熱(軽度, 40-50%)",{"under_37.5":0.35,"37.5_38.0":0.25,"38.0_39.0":0.25,"39.0_40.0":0.12,"over_40.0":0.03}),
    ("S07","ノロ: 倦怠感(50-60%)",{"absent":0.30,"mild":0.45,"severe":0.25}),
    ("S05","ノロ: 頭痛(30-40%)",{"absent":0.50,"mild":0.35,"severe":0.15}),
    ("T01","ノロ: 急性(1-3日)",{"under_3d":0.70,"3d_to_1w":0.25,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","ノロ: 突発",{"sudden_hours":0.65,"gradual_days":0.35}),
]: add("D268","norovirus",to,r,c)
s3["full_cpts"]["D268"] = {"parents":[],"description":"ノロウイルス胃腸炎","cpt":{"":0.008}}

# D269 ロタウイルス胃腸炎 (Rotavirus)
s1["variables"].append({"id":"D269","name":"rotavirus","name_ja":"ロタウイルス胃腸炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"乳幼児(6ヶ月~2歳)。白色水様便が特徴。嘔吐→下痢→脱水。ワクチンで減少"})
for to,r,c in [
    ("S14","ロタ: 白色水様便(特徴的)",{"absent":0.05,"watery":0.90,"bloody":0.05}),
    ("S13","ロタ: 嘔吐(80-90%)",{"absent":0.08,"present":0.92}),
    ("E01","ロタ: 発熱(60-70%)",{"under_37.5":0.20,"37.5_38.0":0.15,"38.0_39.0":0.35,"39.0_40.0":0.22,"over_40.0":0.08}),
    ("S12","ロタ: 腹痛",{"absent":0.30,"epigastric":0.10,"RUQ":0.02,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.02,"diffuse":0.52}),
    ("E02","ロタ: 頻脈(脱水)",{"under_100":0.15,"100_120":0.40,"over_120":0.45}),
    ("E03","ロタ: 低血圧(重度脱水)",{"normal_over_90":0.50,"hypotension_under_90":0.50}),
    ("L01","ロタ: WBC(正常~軽度)",{"low_under_4000":0.05,"normal_4000_10000":0.50,"high_10000_20000":0.35,"very_high_over_20000":0.10}),
    ("T01","ロタ: 急性(3-8日)",{"under_3d":0.20,"3d_to_1w":0.60,"1w_to_3w":0.18,"over_3w":0.02}),
    ("T02","ロタ: 急性",{"sudden_hours":0.40,"gradual_days":0.60}),
]: add("D269","rotavirus",to,r,c)
s3["full_cpts"]["D269"] = {"parents":["R01"],"description":"ロタウイルス胃腸炎。乳幼児",
    "cpt":{"0_1":0.010,"1_5":0.008,"6_12":0.003,"13_17":0.001,"18_39":0.001,"40_64":0.001,"65_plus":0.002}}

# D270 アスピリン喘息 (AERD / Aspirin-Exacerbated Respiratory Disease)
s1["variables"].append({"id":"D270","name":"AERD","name_ja":"アスピリン喘息(NSAIDs不耐症)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"NSAIDs服用→30分~2時間で喘息発作+鼻閉+結膜充血。鼻ポリープ合併。Samter triad"})
for to,r,c in [
    ("S04","AERD: 呼吸困難(急性発作, 90%+)",{"absent":0.03,"on_exertion":0.12,"at_rest":0.85}),
    ("E07","AERD: wheezes(90%+)",{"clear":0.03,"crackles":0.05,"wheezes":0.85,"decreased_absent":0.07}),
    ("S03","AERD: 鼻閉(60-70%)",{"absent":0.20,"clear_rhinorrhea":0.50,"purulent_rhinorrhea":0.30}),
    ("E04","AERD: 頻呼吸",{"normal_under_20":0.05,"tachypnea_20_30":0.30,"severe_over_30":0.65}),
    ("E05","AERD: SpO2低下",{"normal_over_96":0.10,"mild_hypoxia_93_96":0.30,"severe_hypoxia_under_93":0.60}),
    ("E02","AERD: 頻脈",{"under_100":0.10,"100_120":0.35,"over_120":0.55}),
    ("T01","AERD: 超急性(NSAIDs後30分~2h)",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","AERD: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D270","AERD",to,r,c)
s3["full_cpts"]["D270"] = {"parents":["R01"],"description":"AERD","cpt":{"0_1":0.0001,"1_5":0.0003,"6_12":0.001,"13_17":0.001,"18_39":0.002,"40_64":0.002,"65_plus":0.001}}

# D271 好酸球性食道炎 (Eosinophilic Esophagitis)
s1["variables"].append({"id":"D271","name":"eosinophilic_esophagitis","name_ja":"好酸球性食道炎(EoE)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"食道好酸球浸潤→嚥下困難+食物つかえ感+胸痛。若年男性+アトピー素因に多い。PPIで改善しない"})
for to,r,c in [
    ("S21","EoE: 胸痛/嚥下痛(40-50%)",{"absent":0.45,"burning":0.25,"sharp":0.15,"pressure":0.10,"tearing":0.05}),
    ("S13","EoE: 嘔気(30-40%)",{"absent":0.55,"present":0.45}),
    ("S07","EoE: 倦怠感(20-30%)",{"absent":0.60,"mild":0.30,"severe":0.10}),
    ("L14","EoE: 末梢血好酸球増多(40-50%)",{"normal":0.45,"left_shift":0.02,"atypical_lymphocytes":0.01,"thrombocytopenia":0.01,"eosinophilia":0.45,"lymphocyte_predominant":0.06}),
    ("T01","EoE: 慢性(反復性)",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.25,"over_3w":0.60}),
    ("T02","EoE: 慢性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D271","eosinophilic_esophagitis",to,r,c)
s3["full_cpts"]["D271"] = {"parents":["R01","R02"],"description":"EoE。若年男性",
    "cpt":{"0_1,male":0.001,"0_1,female":0.0005,"1_5,male":0.002,"1_5,female":0.001,"6_12,male":0.003,"6_12,female":0.001,"13_17,male":0.003,"13_17,female":0.001,"18_39,male":0.004,"18_39,female":0.001,"40_64,male":0.003,"40_64,female":0.001,"65_plus,male":0.002,"65_plus,female":0.0005}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 271 diseases")
