#!/usr/bin/env python3
"""Add D222-D226: 5 diseases."""
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

# D222 関節リウマチ (RA)
s1["variables"].append({"id":"D222","name":"rheumatoid_arthritis","name_ja":"関節リウマチ(RA)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"対称性多関節炎(MCP/PIP/手関節). 朝のこわばり>1h. RF/抗CCP陽性. ILD/血管炎が腺外症状"})
for to,r,c in [
    ("S08","RA: 関節痛(100%)",{"absent":0.02,"present":0.98}),
    ("S27","RA: 朝のこわばり(>30min, 80%+)",{"absent":0.05,"under_30min":0.10,"over_30min":0.85}),
    ("S07","RA: 倦怠感(60-70%)",{"absent":0.20,"mild":0.45,"severe":0.35}),
    ("E01","RA: 発熱(急性増悪時, 10-20%)",{"under_37.5":0.70,"37.5_38.0":0.12,"38.0_39.0":0.10,"39.0_40.0":0.06,"over_40.0":0.02}),
    ("L02","RA: CRP上昇(活動期, 60-70%)",{"normal_under_0.3":0.20,"mild_0.3_3":0.25,"moderate_3_10":0.30,"high_over_10":0.25}),
    ("L28","RA: ESR上昇(活動期, 70-80%)",{"normal":0.15,"elevated":0.85}),
    ("L01","RA: WBC(正常~軽度上昇)",{"low_under_4000":0.05,"normal_4000_10000":0.50,"high_10000_20000":0.35,"very_high_over_20000":0.10}),
    ("T01","RA: 慢性(急性増悪で来院)",{"under_3d":0.05,"3d_to_1w":0.15,"1w_to_3w":0.30,"over_3w":0.50}),
    ("T02","RA: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D222","rheumatoid_arthritis",to,r,c)
s3["full_cpts"]["D222"] = {"parents":["R02"],"description":"RA. 女性に多い(F:M=3:1)","cpt":{"male":0.002,"female":0.006}}

# D223 混合性結合組織病 (MCTD)
s1["variables"].append({"id":"D223","name":"MCTD","name_ja":"混合性結合組織病(MCTD)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"SLE+SSc+PM重複。抗U1-RNP抗体陽性。レイノー+手指腫脹+多関節炎+肺高血圧"})
for to,r,c in [
    ("S08","MCTD: 関節痛(80-90%)",{"absent":0.08,"present":0.92}),
    ("S07","MCTD: 倦怠感(80%+)",{"absent":0.10,"mild":0.35,"severe":0.55}),
    ("S06","MCTD: 筋肉痛(60-70%)",{"absent":0.25,"present":0.75}),
    ("E01","MCTD: 発熱(30-40%)",{"under_37.5":0.50,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.12,"over_40.0":0.03}),
    ("S04","MCTD: 呼吸困難(肺高血圧/ILD, 30-40%)",{"absent":0.50,"on_exertion":0.35,"at_rest":0.15}),
    ("E36","MCTD: 手指腫脹/浮腫(sausage fingers, 60-70%)",{"absent":0.25,"unilateral":0.10,"bilateral":0.65}),
    ("L02","MCTD: CRP上昇",{"normal_under_0.3":0.20,"mild_0.3_3":0.30,"moderate_3_10":0.30,"high_over_10":0.20}),
    ("T01","MCTD: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.20,"over_3w":0.70}),
    ("T02","MCTD: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D223","MCTD",to,r,c)
s3["full_cpts"]["D223"] = {"parents":["R02"],"description":"MCTD. 女性に多い","cpt":{"male":0.0003,"female":0.001}}

# D224 重症筋無力症 (MG, non-crisis) → D165はcrisis. 慢性MGは急性診断に不向き。Skip.
# D224 成人T細胞白血病/リンパ腫 (ATLL)
s1["variables"].append({"id":"D224","name":"ATLL","name_ja":"成人T細胞白血病/リンパ腫(ATLL)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"HTLV-1。急性型:高Ca血症+皮疹+リンパ節腫脹+肝脾腫+日和見感染。九州/沖縄/カリブに多い"})
for to,r,c in [
    ("E01","ATLL: 発熱(日和見感染, 60-70%)",{"under_37.5":0.20,"37.5_38.0":0.15,"38.0_39.0":0.25,"39.0_40.0":0.25,"over_40.0":0.15}),
    ("E12","ATLL: 皮疹(紅斑/丘疹/結節, 50-60%)",{"normal":0.35,"localized_erythema_warmth_swelling":0.05,"petechiae_purpura":0.05,"maculopapular_rash":0.30,"vesicular_dermatomal":0.02,"diffuse_erythroderma":0.10,"purpura":0.05,"vesicle_bulla":0.03,"skin_necrosis":0.05}),
    ("S07","ATLL: 倦怠感(80%+)",{"absent":0.08,"mild":0.25,"severe":0.67}),
    ("L01","ATLL: WBC(著増, 異常リンパ球flower cell)",{"low_under_4000":0.05,"normal_4000_10000":0.10,"high_10000_20000":0.25,"very_high_over_20000":0.60}),
    ("L44","ATLL: 高Ca血症(急性型80%+)",{"normal":0.15,"hyponatremia":0.03,"hyperkalemia":0.02,"other":0.80}),
    ("L16","ATLL: LDH上昇(腫瘍量反映)",{"normal":0.10,"elevated":0.90}),
    ("L11","ATLL: 肝酵素上昇(肝浸潤)",{"normal":0.30,"mild_elevated":0.40,"very_high":0.30}),
    ("T01","ATLL: 急性~亜急性",{"under_3d":0.15,"3d_to_1w":0.25,"1w_to_3w":0.30,"over_3w":0.30}),
    ("T02","ATLL: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D224","ATLL",to,r,c)
s3["full_cpts"]["D224"] = {"parents":["R01"],"description":"ATLL. HTLV-1. 中高年","cpt":{"18_39":0.0003,"40_64":0.001,"65_plus":0.002}}

# D225 骨髄異形成症候群 (MDS)
s1["variables"].append({"id":"D225","name":"MDS","name_ja":"骨髄異形成症候群(MDS)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"無効造血→汎血球減少。高齢者。倦怠感+感染+出血。芽球増加でAML転化リスク"})
for to,r,c in [
    ("S07","MDS: 倦怠感(貧血, 80%+)",{"absent":0.08,"mild":0.30,"severe":0.62}),
    ("E01","MDS: 発熱(感染合併, 30-40%)",{"under_37.5":0.50,"37.5_38.0":0.15,"38.0_39.0":0.18,"39.0_40.0":0.12,"over_40.0":0.05}),
    ("S44","MDS: 出血傾向(血小板減少, 30-40%)",{"absent":0.55,"present":0.45}),
    ("L01","MDS: WBC(低~正常)",{"low_under_4000":0.50,"normal_4000_10000":0.35,"high_10000_20000":0.10,"very_high_over_20000":0.05}),
    ("L14","MDS: 汎血球減少(dysplasia)",{"normal":0.10,"left_shift":0.10,"atypical_lymphocytes":0.05,"thrombocytopenia":0.65,"eosinophilia":0.02,"lymphocyte_predominant":0.08}),
    ("L16","MDS: LDH上昇(無効造血)",{"normal":0.30,"elevated":0.70}),
    ("T01","MDS: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","MDS: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D225","MDS",to,r,c)
s3["full_cpts"]["D225"] = {"parents":["R01"],"description":"MDS. 高齢者","cpt":{"18_39":0.0003,"40_64":0.001,"65_plus":0.003}}

# D226 真性多血症 (PV)
s1["variables"].append({"id":"D226","name":"polycythemia_vera","name_ja":"真性多血症(PV)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"JAK2 V617F(95%+)。赤血球増多→血栓症リスク。頭痛/めまい/掻痒(入浴後)/脾腫/血栓"})
for to,r,c in [
    ("S05","PV: 頭痛(40-50%)",{"absent":0.40,"mild":0.35,"severe":0.25}),
    ("S07","PV: 倦怠感(50-60%)",{"absent":0.30,"mild":0.40,"severe":0.30}),
    ("E38","PV: 高血圧(血液粘度上昇, 30-40%)",{"normal_under_140":0.50,"elevated_140_180":0.35,"crisis_over_180":0.15}),
    ("E12","PV: 皮膚(plethora/紅潮, 40-50%)",{"normal":0.45,"localized_erythema_warmth_swelling":0.05,"petechiae_purpura":0.05,"maculopapular_rash":0.02,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.35,"purpura":0.03,"vesicle_bulla":0.01,"skin_necrosis":0.03}),
    ("L16","PV: LDH上昇(細胞回転亢進)",{"normal":0.25,"elevated":0.75}),
    ("T01","PV: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","PV: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D226","polycythemia_vera",to,r,c)
s3["full_cpts"]["D226"] = {"parents":["R01"],"description":"PV. 中高年","cpt":{"18_39":0.0003,"40_64":0.001,"65_plus":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 226 diseases")
