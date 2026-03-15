#!/usr/bin/env python3
"""Add D257-D261: 5 diseases."""
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

# D257 壊死性腸炎 (NEC - Necrotizing Enterocolitis)
s1["variables"].append({"id":"D257","name":"NEC","name_ja":"壊死性腸炎(NEC)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"早産児・低出生体重児に多い。腹部膨満+血便+胆汁性嘔吐+敗血症。X線:腸管壁内気腫(pneumatosis)"})
for to,r,c in [
    ("S12","NEC: 腹部膨満+圧痛",{"absent":0.05,"epigastric":0.03,"RUQ":0.03,"RLQ":0.03,"LLQ":0.03,"suprapubic":0.03,"diffuse":0.80}),
    ("S14","NEC: 血便(50-70%)",{"absent":0.25,"watery":0.15,"bloody":0.60}),
    ("S13","NEC: 胆汁性嘔吐(70-80%)",{"absent":0.15,"present":0.85}),
    ("E01","NEC: 発熱/低体温(不安定)",{"under_37.5":0.35,"37.5_38.0":0.15,"38.0_39.0":0.25,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("E03","NEC: 低血圧(敗血症)",{"normal_over_90":0.30,"hypotension_under_90":0.70}),
    ("E02","NEC: 頻脈/徐脈",{"under_100":0.20,"100_120":0.30,"over_120":0.50}),
    ("L01","NEC: WBC(低下or上昇)",{"low_under_4000":0.25,"normal_4000_10000":0.20,"high_10000_20000":0.30,"very_high_over_20000":0.25}),
    ("L14","NEC: 血小板減少(DIC合併)",{"normal":0.30,"left_shift":0.05,"atypical_lymphocytes":0.00,"thrombocytopenia":0.60,"eosinophilia":0.00,"lymphocyte_predominant":0.05}),
    ("L02","NEC: CRP上昇",{"normal_under_0.3":0.10,"mild_0.3_3":0.15,"moderate_3_10":0.30,"high_over_10":0.45}),
    ("T01","NEC: 急性",{"under_3d":0.60,"3d_to_1w":0.30,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","NEC: 急性",{"sudden_hours":0.45,"gradual_days":0.55}),
]: add("D257","NEC",to,r,c)
s3["full_cpts"]["D257"] = {"parents":["R01"],"description":"NEC。早産児",
    "cpt":{"0_1":0.008,"1_5":0.001,"6_12":0.0002,"13_17":0.0001,"18_39":0.0001,"40_64":0.0001,"65_plus":0.0001}}

# D258 溶連菌感染後急性糸球体腎炎 → already D191 PSGN. Skip.
# D258 先天性心疾患(VSD) → too chronic for acute diagnosis.
# D258 RSウイルス感染症 (RSV infection, broader than bronchiolitis)
s1["variables"].append({"id":"D258","name":"RSV_infection","name_ja":"RSウイルス感染症",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"乳幼児の上下気道感染。鼻汁→咳嗽→喘鳴。成人/高齢者でも重症化。冬季流行"})
for to,r,c in [
    ("S01","RSV: 咳嗽(90%+)",{"absent":0.05,"dry":0.35,"productive":0.60}),
    ("S03","RSV: 鼻汁(80%+)",{"absent":0.10,"clear_rhinorrhea":0.65,"purulent_rhinorrhea":0.25}),
    ("E01","RSV: 発熱(60-70%)",{"under_37.5":0.20,"37.5_38.0":0.20,"38.0_39.0":0.35,"39.0_40.0":0.18,"over_40.0":0.07}),
    ("S04","RSV: 呼吸困難(40-60%)",{"absent":0.30,"on_exertion":0.30,"at_rest":0.40}),
    ("E07","RSV: 肺聴診(wheezes)",{"clear":0.15,"crackles":0.25,"wheezes":0.50,"decreased_absent":0.10}),
    ("E04","RSV: 多呼吸",{"normal_under_20":0.20,"tachypnea_20_30":0.40,"severe_over_30":0.40}),
    ("E05","RSV: SpO2低下",{"normal_over_96":0.35,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.30}),
    ("L01","RSV: WBC(正常~軽度)",{"low_under_4000":0.05,"normal_4000_10000":0.50,"high_10000_20000":0.35,"very_high_over_20000":0.10}),
    ("T01","RSV: 急性",{"under_3d":0.25,"3d_to_1w":0.50,"1w_to_3w":0.20,"over_3w":0.05}),
    ("T02","RSV: 急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D258","RSV_infection",to,r,c)
s3["full_cpts"]["D258"] = {"parents":["R01"],"description":"RSV感染症",
    "cpt":{"0_1":0.012,"1_5":0.008,"6_12":0.003,"13_17":0.002,"18_39":0.002,"40_64":0.002,"65_plus":0.004}}

# D259 手足口病 (Hand-Foot-Mouth Disease)
s1["variables"].append({"id":"D259","name":"HFMD","name_ja":"手足口病",
    "category":"disease","states":["no","yes"],"severity":"low",
    "note":"コクサッキーA16/エンテロウイルス71。口腔内水疱+手掌/足底水疱。発熱は軽度。EV71は重症化(脳炎/肺水腫)"})
for to,r,c in [
    ("E12","手足口病: 水疱(手掌/足底/口腔)",{"normal":0.03,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.01,"maculopapular_rash":0.10,"vesicular_dermatomal":0.02,"diffuse_erythroderma":0.01,"purpura":0.01,"vesicle_bulla":0.78,"skin_necrosis":0.02}),
    ("E01","手足口病: 発熱(軽度, 60-70%)",{"under_37.5":0.20,"37.5_38.0":0.25,"38.0_39.0":0.35,"39.0_40.0":0.15,"over_40.0":0.05}),
    ("S02","手足口病: 咽頭痛(口腔内水疱, 60-70%)",{"absent":0.25,"present":0.75}),
    ("S43","手足口病: 手掌/足底発疹(定義的)",{"absent":0.05,"present":0.95}),
    ("S07","手足口病: 倦怠感(40-50%)",{"absent":0.40,"mild":0.40,"severe":0.20}),
    ("S13","手足口病: 嘔気(20-30%)",{"absent":0.65,"present":0.35}),
    ("L01","手足口病: WBC(正常)",{"low_under_4000":0.10,"normal_4000_10000":0.60,"high_10000_20000":0.25,"very_high_over_20000":0.05}),
    ("T01","手足口病: 急性",{"under_3d":0.30,"3d_to_1w":0.50,"1w_to_3w":0.18,"over_3w":0.02}),
    ("T02","手足口病: 急性",{"sudden_hours":0.25,"gradual_days":0.75}),
]: add("D259","HFMD",to,r,c)
s3["full_cpts"]["D259"] = {"parents":["R01"],"description":"手足口病。乳幼児",
    "cpt":{"0_1":0.008,"1_5":0.010,"6_12":0.004,"13_17":0.002,"18_39":0.001,"40_64":0.0005,"65_plus":0.0003}}

# D260 ヘルパンギーナ (Herpangina)
s1["variables"].append({"id":"D260","name":"herpangina","name_ja":"ヘルパンギーナ",
    "category":"disease","states":["no","yes"],"severity":"low",
    "note":"コクサッキーA群。夏季。高熱+咽頭痛+口蓋弓/軟口蓋の小水疱。1-5歳に多い"})
for to,r,c in [
    ("E01","ヘルパンギーナ: 高熱(90%+)",{"under_37.5":0.05,"37.5_38.0":0.08,"38.0_39.0":0.25,"39.0_40.0":0.35,"over_40.0":0.27}),
    ("S02","ヘルパンギーナ: 咽頭痛(90%+)",{"absent":0.05,"present":0.95}),
    ("E08","ヘルパンギーナ: 口蓋弓水疱(特徴的)",{"normal":0.03,"erythema":0.10,"exudate_or_white_patch":0.87}),
    ("S07","ヘルパンギーナ: 倦怠感",{"absent":0.20,"mild":0.45,"severe":0.35}),
    ("S13","ヘルパンギーナ: 嘔吐(脱水, 30-40%)",{"absent":0.55,"present":0.45}),
    ("L01","ヘルパンギーナ: WBC(正常)",{"low_under_4000":0.10,"normal_4000_10000":0.55,"high_10000_20000":0.30,"very_high_over_20000":0.05}),
    ("T01","ヘルパンギーナ: 急性(2-4日)",{"under_3d":0.50,"3d_to_1w":0.40,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","ヘルパンギーナ: 急性",{"sudden_hours":0.40,"gradual_days":0.60}),
]: add("D260","herpangina",to,r,c)
s3["full_cpts"]["D260"] = {"parents":["R01"],"description":"ヘルパンギーナ。1-5歳",
    "cpt":{"0_1":0.006,"1_5":0.010,"6_12":0.003,"13_17":0.001,"18_39":0.001,"40_64":0.0005,"65_plus":0.0003}}

# D261 突発性発疹 (Exanthem Subitum / Roseola)
s1["variables"].append({"id":"D261","name":"roseola","name_ja":"突発性発疹(ロゼオラ)",
    "category":"disease","states":["no","yes"],"severity":"low",
    "note":"HHV-6/7。6ヶ月~2歳。3-5日の高熱→解熱と同時に体幹の淡い紅斑性発疹。熱性痙攣合併あり"})
for to,r,c in [
    ("E01","突発性発疹: 高熱3-5日(定義的)",{"under_37.5":0.03,"37.5_38.0":0.05,"38.0_39.0":0.20,"39.0_40.0":0.40,"over_40.0":0.32}),
    ("E12","突発性発疹: 解熱後の紅斑(体幹)",{"normal":0.15,"localized_erythema_warmth_swelling":0.03,"petechiae_purpura":0.01,"maculopapular_rash":0.70,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.05,"purpura":0.01,"vesicle_bulla":0.01,"skin_necrosis":0.03}),
    ("S42","突発性発疹: 熱性痙攣合併(10-15%)",{"absent":0.85,"present":0.15}),
    ("S14","突発性発疹: 下痢(30-40%)",{"absent":0.55,"watery":0.40,"bloody":0.05}),
    ("S09","突発性発疹: 易刺激性",{"absent":0.30,"present":0.70}),
    ("L01","突発性発疹: WBC(解熱期にリンパ球優位)",{"low_under_4000":0.15,"normal_4000_10000":0.45,"high_10000_20000":0.30,"very_high_over_20000":0.10}),
    ("T01","突発性発疹: 急性(3-5日高熱→解熱)",{"under_3d":0.20,"3d_to_1w":0.60,"1w_to_3w":0.18,"over_3w":0.02}),
    ("T02","突発性発疹: 急性",{"sudden_hours":0.30,"gradual_days":0.70}),
]: add("D261","roseola",to,r,c)
s3["full_cpts"]["D261"] = {"parents":["R01"],"description":"突発性発疹。6月~2歳",
    "cpt":{"0_1":0.012,"1_5":0.006,"6_12":0.001,"13_17":0.0003,"18_39":0.0001,"40_64":0.0001,"65_plus":0.0001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 261 diseases")
