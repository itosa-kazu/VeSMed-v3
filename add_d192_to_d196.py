#!/usr/bin/env python3
"""Add D192 APL + D193 HP + D194 Lyme + D195 Drug Pneumonitis + D196 Diphtheria."""
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

# D192 APL
s1["variables"].append({"id":"D192","name":"APL","name_ja":"急性前骨髄球性白血病(APL)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"AML-M3. DIC高率合併(80%+). ATRA+ATO治療"})
for to,r,c in [
    ("L14","APL: 血小板減少/DIC",{"normal":0.05,"left_shift":0.05,"atypical_lymphocytes":0.00,"thrombocytopenia":0.85,"eosinophilia":0.00,"lymphocyte_predominant":0.05}),
    ("S44","APL: 出血傾向(DIC)",{"absent":0.15,"present":0.85}),
    ("L52","APL: D-dimer著高",{"not_done":0.10,"normal":0.03,"mildly_elevated":0.07,"very_high":0.80}),
    ("E12","APL: 紫斑",{"normal":0.15,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.30,"maculopapular_rash":0.01,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.35,"vesicle_bulla":0.02,"skin_necrosis":0.13}),
    ("E01","APL: 発熱",{"under_37.5":0.30,"37.5_38.0":0.15,"38.0_39.0":0.25,"39.0_40.0":0.20,"over_40.0":0.10}),
    ("S07","APL: 倦怠感",{"absent":0.08,"mild":0.30,"severe":0.62}),
    ("L01","APL: WBC",{"low_under_4000":0.25,"normal_4000_10000":0.25,"high_10000_20000":0.25,"very_high_over_20000":0.25}),
    ("L16","APL: LDH",{"normal":0.15,"elevated":0.85}),
    ("T01","APL: 急性",{"under_3d":0.25,"3d_to_1w":0.40,"1w_to_3w":0.25,"over_3w":0.10}),
    ("T02","APL: 亜急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D192","APL",to,r,c)
s3["full_cpts"]["D192"] = {"parents":[],"description":"APL","cpt":{"":0.001}}

# D193 過敏性肺炎
s1["variables"].append({"id":"D193","name":"hypersensitivity_pneumonitis","name_ja":"過敏性肺炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"抗原吸入->肺アレルギー. 農夫肺/鳥飼い肺"})
for to,r,c in [
    ("S04","過敏性肺炎: 呼吸困難",{"absent":0.05,"on_exertion":0.25,"at_rest":0.70}),
    ("S01","過敏性肺炎: 咳嗽",{"absent":0.10,"dry":0.60,"productive":0.30}),
    ("E01","過敏性肺炎: 発熱",{"under_37.5":0.15,"37.5_38.0":0.15,"38.0_39.0":0.35,"39.0_40.0":0.25,"over_40.0":0.10}),
    ("E07","過敏性肺炎: crackles",{"clear":0.10,"crackles":0.75,"wheezes":0.10,"decreased_absent":0.05}),
    ("E04","過敏性肺炎: 頻呼吸",{"normal_under_20":0.10,"tachypnea_20_30":0.45,"severe_over_30":0.45}),
    ("E05","過敏性肺炎: 低酸素",{"normal_over_96":0.15,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.50}),
    ("L04","過敏性肺炎: CXR",{"normal":0.08,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.80,"BHL":0.03,"pleural_effusion":0.03,"pneumothorax":0.04}),
    ("S07","過敏性肺炎: 倦怠感",{"absent":0.15,"mild":0.40,"severe":0.45}),
    ("L01","過敏性肺炎: WBC",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.27}),
    ("T01","過敏性肺炎: 急性",{"under_3d":0.50,"3d_to_1w":0.25,"1w_to_3w":0.15,"over_3w":0.10}),
    ("T02","過敏性肺炎: 急性",{"sudden_hours":0.55,"gradual_days":0.45}),
]: add("D193","hypersensitivity_pneumonitis",to,r,c)
s3["full_cpts"]["D193"] = {"parents":[],"description":"過敏性肺炎","cpt":{"":0.002}}

# D194 ライム病
s1["variables"].append({"id":"D194","name":"lyme_disease","name_ja":"ライム病",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"Borrelia burgdorferi. ダニ->遊走性紅斑->関節炎/神経/心"})
for to,r,c in [
    ("E12","ライム: 遊走性紅斑",{"normal":0.15,"localized_erythema_warmth_swelling":0.10,"petechiae_purpura":0.01,"maculopapular_rash":0.65,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.02,"purpura":0.01,"vesicle_bulla":0.01,"skin_necrosis":0.04}),
    ("E01","ライム: 発熱",{"under_37.5":0.25,"37.5_38.0":0.20,"38.0_39.0":0.30,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("S08","ライム: 関節痛",{"absent":0.35,"present":0.65}),
    ("S05","ライム: 頭痛",{"absent":0.35,"mild":0.35,"severe":0.30}),
    ("S07","ライム: 倦怠感",{"absent":0.15,"mild":0.40,"severe":0.45}),
    ("S06","ライム: 筋肉痛",{"absent":0.45,"present":0.55}),
    ("E06","ライム: 項部硬直(神経ライム)",{"absent":0.80,"present":0.20}),
    ("L01","ライム: WBC",{"low_under_4000":0.05,"normal_4000_10000":0.55,"high_10000_20000":0.30,"very_high_over_20000":0.10}),
    ("T01","ライム: 亜急性",{"under_3d":0.10,"3d_to_1w":0.25,"1w_to_3w":0.40,"over_3w":0.25}),
    ("T02","ライム: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D194","lyme_disease",to,r,c)
s3["full_cpts"]["D194"] = {"parents":[],"description":"ライム病","cpt":{"":0.001}}

# D195 薬剤性肺炎
s1["variables"].append({"id":"D195","name":"drug_induced_pneumonitis","name_ja":"薬剤性肺炎",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"MTX/アミオダロン/CPI等->間質性肺炎"})
for to,r,c in [
    ("S04","薬剤性肺炎: 呼吸困難",{"absent":0.05,"on_exertion":0.30,"at_rest":0.65}),
    ("S01","薬剤性肺炎: 咳嗽",{"absent":0.10,"dry":0.65,"productive":0.25}),
    ("E01","薬剤性肺炎: 発熱",{"under_37.5":0.35,"37.5_38.0":0.15,"38.0_39.0":0.25,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("E07","薬剤性肺炎: crackles",{"clear":0.15,"crackles":0.70,"wheezes":0.10,"decreased_absent":0.05}),
    ("E05","薬剤性肺炎: 低酸素",{"normal_over_96":0.15,"mild_hypoxia_93_96":0.40,"severe_hypoxia_under_93":0.45}),
    ("L04","薬剤性肺炎: CXR",{"normal":0.08,"lobar_infiltrate":0.05,"bilateral_infiltrate":0.75,"BHL":0.02,"pleural_effusion":0.06,"pneumothorax":0.04}),
    ("L14","薬剤性肺炎: 好酸球増多",{"normal":0.40,"left_shift":0.02,"atypical_lymphocytes":0.02,"thrombocytopenia":0.01,"eosinophilia":0.50,"lymphocyte_predominant":0.05}),
    ("L01","薬剤性肺炎: WBC",{"low_under_4000":0.05,"normal_4000_10000":0.35,"high_10000_20000":0.40,"very_high_over_20000":0.20}),
    ("T01","薬剤性肺炎: 亜急性",{"under_3d":0.10,"3d_to_1w":0.25,"1w_to_3w":0.35,"over_3w":0.30}),
    ("T02","薬剤性肺炎: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D195","drug_induced_pneumonitis",to,r,c)
s3["full_cpts"]["D195"] = {"parents":[],"description":"薬剤性肺炎","cpt":{"":0.002}}

# D196 ジフテリア
s1["variables"].append({"id":"D196","name":"diphtheria","name_ja":"ジフテリア",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"C.diphtheriae. 偽膜+bull neck. 心筋炎/神経麻痺が致死的"})
for to,r,c in [
    ("S02","ジフテリア: 咽頭痛",{"absent":0.05,"present":0.95}),
    ("E08","ジフテリア: 白苔/偽膜",{"normal":0.03,"erythema":0.10,"exudate_or_white_patch":0.87}),
    ("E01","ジフテリア: 発熱",{"under_37.5":0.10,"37.5_38.0":0.20,"38.0_39.0":0.40,"39.0_40.0":0.22,"over_40.0":0.08}),
    ("S04","ジフテリア: 呼吸困難(気道閉塞)",{"absent":0.40,"on_exertion":0.25,"at_rest":0.35}),
    ("S07","ジフテリア: 倦怠感",{"absent":0.10,"mild":0.35,"severe":0.55}),
    ("E02","ジフテリア: 頻脈(心筋炎)",{"under_100":0.30,"100_120":0.40,"over_120":0.30}),
    ("L01","ジフテリア: WBC",{"low_under_4000":0.05,"normal_4000_10000":0.30,"high_10000_20000":0.45,"very_high_over_20000":0.20}),
    ("T01","ジフテリア: 急性",{"under_3d":0.30,"3d_to_1w":0.50,"1w_to_3w":0.15,"over_3w":0.05}),
    ("T02","ジフテリア: 急性",{"sudden_hours":0.25,"gradual_days":0.75}),
]: add("D196","diphtheria",to,r,c)
s3["full_cpts"]["D196"] = {"parents":[],"description":"ジフテリア","cpt":{"":0.0005}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 196 diseases")
