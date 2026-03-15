#!/usr/bin/env python3
"""Add D217-D221: 5 diseases."""
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

# D217 急性動脈閉塞 (Acute Arterial Occlusion)
s1["variables"].append({"id":"D217","name":"acute_arterial_occlusion","name_ja":"急性動脈閉塞症",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"6P:Pain/Pallor/Pulselessness/Paresthesia/Paralysis/Poikilothermia。塞栓(AF/IE)か血栓。6h以内に血行再建"})
for to,r,c in [
    ("E02","急性動脈閉塞: 頻脈(AF/塞栓源)",{"under_100":0.25,"100_120":0.40,"over_120":0.35}),
    ("E03","急性動脈閉塞: 低血圧(ショック型)",{"normal_over_90":0.55,"hypotension_under_90":0.45}),
    ("L16","急性動脈閉塞: LDH上昇(虚血)",{"normal":0.25,"elevated":0.75}),
    ("L17","急性動脈閉塞: CK上昇(筋虚血)",{"normal":0.25,"elevated":0.45,"very_high":0.30}),
    ("L55","急性動脈閉塞: AKI(腎灌流低下/横紋筋融解)",{"normal":0.40,"mild_elevated":0.35,"high_AKI":0.25}),
    ("L44","急性動脈閉塞: 高K(横紋筋融解)",{"normal":0.45,"hyponatremia":0.05,"hyperkalemia":0.45,"other":0.05}),
    ("T01","急性動脈閉塞: 超急性",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","急性動脈閉塞: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D217","acute_arterial_occlusion",to,r,c)
s3["full_cpts"]["D217"] = {"parents":["R01"],"description":"急性動脈閉塞","cpt":{"18_39":0.0005,"40_64":0.001,"65_plus":0.003}}

# D218 ウィルソン病 (Wilson Disease)
s1["variables"].append({"id":"D218","name":"wilson_disease","name_ja":"ウィルソン病",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"銅代謝異常(ATP7B変異)。肝障害+神経精神症状+Kayser-Fleischer輪。急性肝不全で発症も"})
for to,r,c in [
    ("L11","ウィルソン: 肝酵素上昇",{"normal":0.10,"mild_elevated":0.40,"very_high":0.50}),
    ("E18","ウィルソン: 黄疸(溶血性/肝性)",{"absent":0.25,"present":0.75}),
    ("E16","ウィルソン: 精神神経症状(30-40%)",{"normal":0.45,"confused":0.35,"obtunded":0.20}),
    ("S07","ウィルソン: 倦怠感",{"absent":0.15,"mild":0.40,"severe":0.45}),
    ("L16","ウィルソン: LDH上昇(溶血)",{"normal":0.20,"elevated":0.80}),
    ("S53","ウィルソン: 構音障害(神経型, 30-40%)",{"absent":0.55,"dysarthria":0.35,"aphasia":0.10}),
    ("T01","ウィルソン: 急性~慢性",{"under_3d":0.15,"3d_to_1w":0.20,"1w_to_3w":0.30,"over_3w":0.35}),
    ("T02","ウィルソン: 亜急性~慢性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D218","wilson_disease",to,r,c)
s3["full_cpts"]["D218"] = {"parents":["R01"],"description":"ウィルソン病。若年","cpt":{"18_39":0.001,"40_64":0.0005,"65_plus":0.0002}}

# D219 多発血管炎性肉芽腫症 (GPA/Wegener)
s1["variables"].append({"id":"D219","name":"GPA","name_ja":"多発血管炎性肉芽腫症(GPA)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"PR3-ANCA陽性。上気道(副鼻腔炎/鞍鼻)+下気道(肺結節/肺出血)+腎(RPGN)。E/L/K triad"})
for to,r,c in [
    ("E01","GPA: 発熱(60-70%)",{"under_37.5":0.25,"37.5_38.0":0.15,"38.0_39.0":0.30,"39.0_40.0":0.20,"over_40.0":0.10}),
    ("S01","GPA: 咳嗽(肺病変, 50-60%)",{"absent":0.30,"dry":0.40,"productive":0.30}),
    ("S04","GPA: 呼吸困難(肺出血/ILD, 30-40%)",{"absent":0.50,"on_exertion":0.30,"at_rest":0.20}),
    ("L05","GPA: 尿異常(腎炎, 60-70%)",{"normal":0.25,"pyuria_bacteriuria":0.75}),
    ("L55","GPA: AKI(RPGN, 40-60%)",{"normal":0.30,"mild_elevated":0.30,"high_AKI":0.40}),
    ("S07","GPA: 倦怠感(80%+)",{"absent":0.08,"mild":0.30,"severe":0.62}),
    ("S08","GPA: 関節痛(40-50%)",{"absent":0.45,"present":0.55}),
    ("L01","GPA: WBC上昇",{"low_under_4000":0.05,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.25}),
    ("L02","GPA: CRP上昇",{"normal_under_0.3":0.05,"mild_0.3_3":0.10,"moderate_3_10":0.35,"high_over_10":0.50}),
    ("L04","GPA: CXR(肺結節/浸潤/空洞)",{"normal":0.25,"lobar_infiltrate":0.15,"bilateral_infiltrate":0.45,"BHL":0.03,"pleural_effusion":0.08,"pneumothorax":0.04}),
    ("T01","GPA: 亜急性~慢性",{"under_3d":0.08,"3d_to_1w":0.15,"1w_to_3w":0.35,"over_3w":0.42}),
    ("T02","GPA: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D219","GPA",to,r,c)
s3["full_cpts"]["D219"] = {"parents":["R01"],"description":"GPA。中高年","cpt":{"18_39":0.001,"40_64":0.002,"65_plus":0.002}}

# D220 好酸球性多発血管炎性肉芽腫症 (EGPA/Churg-Strauss)
s1["variables"].append({"id":"D220","name":"EGPA","name_ja":"好酸球性多発血管炎性肉芽腫症(EGPA)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"MPO-ANCA(40%)。喘息+好酸球増多+血管炎。心筋炎(致死的)。末梢神経障害(多発単神経炎)"})
for to,r,c in [
    ("S04","EGPA: 呼吸困難(喘息, 90%+)",{"absent":0.05,"on_exertion":0.30,"at_rest":0.65}),
    ("E07","EGPA: 肺聴診(wheezes, 喘息)",{"clear":0.05,"crackles":0.15,"wheezes":0.70,"decreased_absent":0.10}),
    ("E01","EGPA: 発熱(50-60%)",{"under_37.5":0.30,"37.5_38.0":0.15,"38.0_39.0":0.25,"39.0_40.0":0.20,"over_40.0":0.10}),
    ("L14","EGPA: 好酸球著増(定義的)",{"normal":0.05,"left_shift":0.02,"atypical_lymphocytes":0.01,"thrombocytopenia":0.02,"eosinophilia":0.85,"lymphocyte_predominant":0.05}),
    ("E12","EGPA: 紫斑/結節(皮膚血管炎, 40-50%)",{"normal":0.45,"localized_erythema_warmth_swelling":0.05,"petechiae_purpura":0.15,"maculopapular_rash":0.05,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.20,"vesicle_bulla":0.02,"skin_necrosis":0.06}),
    ("S07","EGPA: 倦怠感",{"absent":0.10,"mild":0.35,"severe":0.55}),
    ("L53","EGPA: トロポニン上昇(心筋炎, 30-40%)",{"not_done":0.15,"normal":0.30,"mildly_elevated":0.35,"very_high":0.20}),
    ("L01","EGPA: WBC上昇(好酸球優位)",{"low_under_4000":0.03,"normal_4000_10000":0.15,"high_10000_20000":0.40,"very_high_over_20000":0.42}),
    ("L02","EGPA: CRP上昇",{"normal_under_0.3":0.08,"mild_0.3_3":0.15,"moderate_3_10":0.35,"high_over_10":0.42}),
    ("T01","EGPA: 亜急性~慢性",{"under_3d":0.05,"3d_to_1w":0.15,"1w_to_3w":0.35,"over_3w":0.45}),
    ("T02","EGPA: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D220","EGPA",to,r,c)
s3["full_cpts"]["D220"] = {"parents":[],"description":"EGPA(Churg-Strauss)","cpt":{"":0.001}}

# D221 顕微鏡的多発血管炎 (MPA)
s1["variables"].append({"id":"D221","name":"MPA","name_ja":"顕微鏡的多発血管炎(MPA)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"MPO-ANCA陽性。RPGN+肺胞出血。GPA/EGPAと鑑別。肉芽腫なし"})
for to,r,c in [
    ("E01","MPA: 発熱(60-70%)",{"under_37.5":0.25,"37.5_38.0":0.15,"38.0_39.0":0.30,"39.0_40.0":0.20,"over_40.0":0.10}),
    ("L05","MPA: 尿異常(RPGN, 80%+)",{"normal":0.10,"pyuria_bacteriuria":0.90}),
    ("L55","MPA: AKI(RPGN, 70-80%)",{"normal":0.10,"mild_elevated":0.25,"high_AKI":0.65}),
    ("S04","MPA: 呼吸困難(肺胞出血, 30-40%)",{"absent":0.50,"on_exertion":0.25,"at_rest":0.25}),
    ("S07","MPA: 倦怠感(80%+)",{"absent":0.08,"mild":0.25,"severe":0.67}),
    ("S08","MPA: 関節痛(40-50%)",{"absent":0.45,"present":0.55}),
    ("S01","MPA: 咳嗽(肺出血/咳血, 30-40%)",{"absent":0.55,"dry":0.20,"productive":0.25}),
    ("L01","MPA: WBC上昇",{"low_under_4000":0.05,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.25}),
    ("L02","MPA: CRP上昇",{"normal_under_0.3":0.05,"mild_0.3_3":0.10,"moderate_3_10":0.30,"high_over_10":0.55}),
    ("T01","MPA: 亜急性",{"under_3d":0.10,"3d_to_1w":0.20,"1w_to_3w":0.40,"over_3w":0.30}),
    ("T02","MPA: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D221","MPA",to,r,c)
s3["full_cpts"]["D221"] = {"parents":["R01"],"description":"MPA","cpt":{"18_39":0.001,"40_64":0.002,"65_plus":0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 221 diseases")
