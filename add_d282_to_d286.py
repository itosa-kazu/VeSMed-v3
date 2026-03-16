#!/usr/bin/env python3
"""Add D282-D286: 5 diseases."""
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

# D282 キノコ中毒 (Mushroom Poisoning)
s1["variables"].append({"id":"D282","name":"mushroom_poisoning","name_ja":"キノコ中毒",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"テングタケ→ムスカリン症状(SLUDGE)。ドクツルタケ→6h後嘔吐下痢→肝不全(24-72h)。早期vs遅発型で予後異なる"})
for to,r,c in [
    ("S13","キノコ中毒: 嘔吐(90%+)",{"absent":0.05,"present":0.95}),
    ("S14","キノコ中毒: 下痢(80%+)",{"absent":0.10,"watery":0.75,"bloody":0.15}),
    ("S12","キノコ中毒: 腹痛(70-80%)",{"absent":0.15,"epigastric":0.30,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.02,"diffuse":0.38}),
    ("L11","キノコ中毒: 肝酵素(ドクツルタケ型→著高)",{"normal":0.20,"mild_elevated":0.25,"very_high":0.55}),
    ("E16","キノコ中毒: 意識障害(重症, 30-40%)",{"normal":0.45,"confused":0.30,"obtunded":0.25}),
    ("L55","キノコ中毒: AKI(肝腎症候群)",{"normal":0.35,"mild_elevated":0.30,"high_AKI":0.35}),
    ("E02","キノコ中毒: 頻脈(脱水)",{"under_100":0.20,"100_120":0.40,"over_120":0.40}),
    ("E03","キノコ中毒: 低血圧(脱水/ショック)",{"normal_over_90":0.35,"hypotension_under_90":0.65}),
    ("T01","キノコ中毒: 急性(6-24h後)",{"under_3d":0.80,"3d_to_1w":0.15,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","キノコ中毒: 急性",{"sudden_hours":0.60,"gradual_days":0.40}),
]: add("D282","mushroom_poisoning",to,r,c)
s3["full_cpts"]["D282"] = {"parents":[],"description":"キノコ中毒","cpt":{"":0.001}}

# D283 フグ中毒 (Tetrodotoxin Poisoning)
s1["variables"].append({"id":"D283","name":"tetrodotoxin","name_ja":"フグ中毒(テトロドトキシン)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"Na+チャネル遮断→口唇/舌の痺れ→四肢麻痺→呼吸筋麻痺。摂取後20分~3時間で発症。解毒薬なし"})
for to,r,c in [
    ("S52","フグ中毒: 四肢麻痺(上行性, 60-80%)",{"absent":0.15,"unilateral_weakness":0.10,"bilateral":0.75}),
    ("S53","フグ中毒: 構音障害(口唇/舌痺れ, 80%+)",{"absent":0.10,"dysarthria":0.75,"aphasia":0.15}),
    ("S13","フグ中毒: 嘔吐(50-60%)",{"absent":0.35,"present":0.65}),
    ("S04","フグ中毒: 呼吸困難(呼吸筋麻痺, 40-60%)",{"absent":0.30,"on_exertion":0.20,"at_rest":0.50}),
    ("E03","フグ中毒: 低血圧(重症)",{"normal_over_90":0.35,"hypotension_under_90":0.65}),
    ("E16","フグ中毒: 意識(通常保たれる, 重症で消失)",{"normal":0.35,"confused":0.30,"obtunded":0.35}),
    ("T01","フグ中毒: 超急性(20分~3h)",{"under_3d":0.95,"3d_to_1w":0.04,"1w_to_3w":0.01,"over_3w":0.00}),
    ("T02","フグ中毒: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D283","tetrodotoxin",to,r,c)
s3["full_cpts"]["D283"] = {"parents":[],"description":"フグ中毒","cpt":{"":0.0005}}

# D284 マムシ咬傷 (Pit Viper Bite)
s1["variables"].append({"id":"D284","name":"pit_viper_bite","name_ja":"マムシ咬傷",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"咬傷部の激痛+腫脹+出血(DIC)+横紋筋融解+AKI。局所→全身へ進展。抗毒素血清治療"})
for to,r,c in [
    ("E12","マムシ: 咬傷部腫脹/発赤",{"normal":0.05,"localized_erythema_warmth_swelling":0.80,"petechiae_purpura":0.02,"maculopapular_rash":0.01,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.03,"vesicle_bulla":0.02,"skin_necrosis":0.05}),
    ("S44","マムシ: 出血傾向(DIC, 30-40%)",{"absent":0.55,"present":0.45}),
    ("E02","マムシ: 頻脈(疼痛/ショック)",{"under_100":0.20,"100_120":0.45,"over_120":0.35}),
    ("L17","マムシ: CK上昇(横紋筋融解)",{"normal":0.30,"elevated":0.40,"very_high":0.30}),
    ("L14","マムシ: 血小板減少(DIC)",{"normal":0.45,"left_shift":0.05,"atypical_lymphocytes":0.00,"thrombocytopenia":0.45,"eosinophilia":0.00,"lymphocyte_predominant":0.05}),
    ("L55","マムシ: AKI(横紋筋融解/DIC)",{"normal":0.45,"mild_elevated":0.30,"high_AKI":0.25}),
    ("L01","マムシ: WBC上昇(ストレス)",{"low_under_4000":0.03,"normal_4000_10000":0.20,"high_10000_20000":0.45,"very_high_over_20000":0.32}),
    ("T01","マムシ: 超急性",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","マムシ: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D284","pit_viper_bite",to,r,c)
s3["full_cpts"]["D284"] = {"parents":[],"description":"マムシ咬傷","cpt":{"":0.001}}

# D285 減圧症 (Decompression Sickness)
s1["variables"].append({"id":"D285","name":"decompression_sickness","name_ja":"減圧症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"ダイビング後の急速浮上→窒素気泡→関節痛(I型)/神経症状(II型)。高圧酸素治療"})
for to,r,c in [
    ("S08","減圧症: 関節痛(I型, 70-80%)",{"absent":0.15,"present":0.85}),
    ("S52","減圧症: 神経症状(II型, 30-40%)",{"absent":0.50,"unilateral_weakness":0.35,"bilateral":0.15}),
    ("E12","減圧症: 皮膚(marbling/cutis marmorata, 10-20%)",{"normal":0.70,"localized_erythema_warmth_swelling":0.05,"petechiae_purpura":0.05,"maculopapular_rash":0.10,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.03,"vesicle_bulla":0.01,"skin_necrosis":0.04}),
    ("S05","減圧症: 頭痛(30-40%)",{"absent":0.50,"mild":0.30,"severe":0.20}),
    ("S07","減圧症: 倦怠感(50-60%)",{"absent":0.30,"mild":0.40,"severe":0.30}),
    ("S04","減圧症: 呼吸困難(chokes, 重症, 10-20%)",{"absent":0.70,"on_exertion":0.15,"at_rest":0.15}),
    ("T01","減圧症: 超急性(浮上後24h以内)",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","減圧症: 急性",{"sudden_hours":0.75,"gradual_days":0.25}),
]: add("D285","decompression_sickness",to,r,c)
s3["full_cpts"]["D285"] = {"parents":[],"description":"減圧症","cpt":{"":0.0005}}

# D286 偶発性低体温症 → already D167. Skip.
# D286 高Ca血症 (Hypercalcemia)
s1["variables"].append({"id":"D286","name":"hypercalcemia","name_ja":"高カルシウム血症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"原発性副甲状腺機能亢進症/悪性腫瘍が二大原因。Stones/Bones/Groans/Moans/Psychic overtones"})
for to,r,c in [
    ("S13","高Ca: 嘔気/嘔吐(40-50%)",{"absent":0.45,"present":0.55}),
    ("S12","高Ca: 腹痛(便秘/膵炎, 30-40%)",{"absent":0.50,"epigastric":0.15,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.02,"diffuse":0.18}),
    ("E16","高Ca: 意識障害(Ca>14で, 30-40%)",{"normal":0.45,"confused":0.35,"obtunded":0.20}),
    ("S07","高Ca: 倦怠感(60-70%)",{"absent":0.20,"mild":0.40,"severe":0.40}),
    ("L55","高Ca: AKI(脱水/Ca腎毒性)",{"normal":0.35,"mild_elevated":0.35,"high_AKI":0.30}),
    ("E02","高Ca: 徐脈or頻脈(QT短縮/不整脈)",{"under_100":0.35,"100_120":0.40,"over_120":0.25}),
    ("L44","高Ca: 電解質異常(Ca上昇→other)",{"normal":0.15,"hyponatremia":0.05,"hyperkalemia":0.05,"other":0.75}),
    ("T01","高Ca: 急性~亜急性",{"under_3d":0.20,"3d_to_1w":0.30,"1w_to_3w":0.30,"over_3w":0.20}),
    ("T02","高Ca: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D286","hypercalcemia",to,r,c)
s3["full_cpts"]["D286"] = {"parents":["R01"],"description":"高Ca血症",
    "cpt":{"0_1":0.0002,"1_5":0.0003,"6_12":0.0003,"13_17":0.0005,"18_39":0.001,"40_64":0.002,"65_plus":0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 286 diseases")
