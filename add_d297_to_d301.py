#!/usr/bin/env python3
"""Add D297-D301: 5 diseases. 300 disease milestone!"""
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

# D297 三叉神経痛 (Trigeminal Neuralgia)
s1["variables"].append({"id":"D297","name":"trigeminal_neuralgia","name_ja":"三叉神経痛",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"電撃様の片側顔面痛(V2/V3領域)。トリガーポイント(洗顔/咀嚼/風)で誘発。発作間は無痛"})
for to,r,c in [
    ("S05","三叉神経痛: 顔面痛(電撃様, 定義的)",{"absent":0.02,"mild":0.08,"severe":0.90}),
    ("E01","三叉神経痛: 無熱",{"under_37.5":0.95,"37.5_38.0":0.03,"38.0_39.0":0.01,"39.0_40.0":0.005,"over_40.0":0.005}),
    ("T01","三叉神経痛: 急性~慢性(発作性)",{"under_3d":0.25,"3d_to_1w":0.25,"1w_to_3w":0.25,"over_3w":0.25}),
    ("T02","三叉神経痛: 突発(電撃様)",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D297","trigeminal_neuralgia",to,r,c)
s3["full_cpts"]["D297"] = {"parents":["R01"],"description":"三叉神経痛",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0001,"13_17":0.0003,"18_39":0.001,"40_64":0.003,"65_plus":0.004}}

# D298 顔面神経麻痺 (Bell Palsy)
s1["variables"].append({"id":"D298","name":"bell_palsy","name_ja":"顔面神経麻痺(Bell麻痺)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"急性片側末梢性顔面神経麻痺。前額皺寄せ不可(中枢性との鑑別)。耳後部痛先行。HSV-1再活性化説"})
for to,r,c in [
    ("S52","Bell: 顔面麻痺(片側性)",{"absent":0.03,"unilateral_weakness":0.90,"bilateral":0.07}),
    ("S05","Bell: 耳後部痛/顔面痛(50-60%)",{"absent":0.35,"mild":0.35,"severe":0.30}),
    ("E01","Bell: 通常無熱",{"under_37.5":0.80,"37.5_38.0":0.10,"38.0_39.0":0.07,"39.0_40.0":0.02,"over_40.0":0.01}),
    ("T01","Bell: 急性(24-72hでピーク)",{"under_3d":0.55,"3d_to_1w":0.30,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","Bell: 急性",{"sudden_hours":0.60,"gradual_days":0.40}),
]: add("D298","bell_palsy",to,r,c)
s3["full_cpts"]["D298"] = {"parents":["R01"],"description":"Bell麻痺",
    "cpt":{"0_1":0.0002,"1_5":0.0005,"6_12":0.001,"13_17":0.001,"18_39":0.002,"40_64":0.003,"65_plus":0.003}}

# D299 Ramsay Hunt症候群 (already D04 covers 帯状疱疹 broadly? D04 is 扁桃周囲膿瘍)
# D04 is actually 帯状疱疹. No wait, let me check. D04 is peritonsillar abscess.
# D46 is 百日咳. Where is 帯状疱疹? Let me check... it should be one of the early diseases.
# Herpes zoster is a separate entity from peritonsillar abscess. Let me add Ramsay Hunt.
s1["variables"].append({"id":"D299","name":"ramsay_hunt","name_ja":"Ramsay Hunt症候群",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"VZV再活性化→耳介帯状疱疹+顔面神経麻痺+聴覚障害(三徴)。Bell麻痺より予後不良"})
for to,r,c in [
    ("S52","Ramsay Hunt: 顔面神経麻痺(片側)",{"absent":0.05,"unilateral_weakness":0.90,"bilateral":0.05}),
    ("E12","Ramsay Hunt: 耳介水疱(帯状疱疹)",{"normal":0.05,"localized_erythema_warmth_swelling":0.05,"petechiae_purpura":0.01,"maculopapular_rash":0.03,"vesicular_dermatomal":0.80,"diffuse_erythroderma":0.01,"purpura":0.01,"vesicle_bulla":0.02,"skin_necrosis":0.02}),
    ("S05","Ramsay Hunt: 耳痛(80%+)",{"absent":0.10,"mild":0.20,"severe":0.70}),
    ("E01","Ramsay Hunt: 発熱(30-40%)",{"under_37.5":0.50,"37.5_38.0":0.18,"38.0_39.0":0.18,"39.0_40.0":0.10,"over_40.0":0.04}),
    ("S07","Ramsay Hunt: 倦怠感",{"absent":0.25,"mild":0.40,"severe":0.35}),
    ("T01","Ramsay Hunt: 急性",{"under_3d":0.30,"3d_to_1w":0.40,"1w_to_3w":0.25,"over_3w":0.05}),
    ("T02","Ramsay Hunt: 急性",{"sudden_hours":0.30,"gradual_days":0.70}),
]: add("D299","ramsay_hunt",to,r,c)
s3["full_cpts"]["D299"] = {"parents":["R01"],"description":"Ramsay Hunt症候群",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0003,"13_17":0.0005,"18_39":0.001,"40_64":0.002,"65_plus":0.003}}

# D300 クロイツフェルト・ヤコブ病 (CJD)
s1["variables"].append({"id":"D300","name":"CJD","name_ja":"クロイツフェルト・ヤコブ病(CJD)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"プリオン病。急速進行性認知症+ミオクローヌス+小脳失調+錐体路/錐体外路徴候。MRI DWI高信号。致死的"})
for to,r,c in [
    ("E16","CJD: 急速進行性認知症(定義的)",{"normal":0.03,"confused":0.35,"obtunded":0.62}),
    ("S42","CJD: ミオクローヌス(70-80%)",{"absent":0.15,"present":0.85}),
    ("S52","CJD: 運動障害(失調/錐体路, 60-70%)",{"absent":0.20,"unilateral_weakness":0.20,"bilateral":0.60}),
    ("S53","CJD: 構音障害(50-60%)",{"absent":0.30,"dysarthria":0.55,"aphasia":0.15}),
    ("S07","CJD: 全身衰弱",{"absent":0.05,"mild":0.15,"severe":0.80}),
    ("T01","CJD: 亜急性~急性(数週~数月で急速進行)",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.25,"over_3w":0.65}),
    ("T02","CJD: 亜急性",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D300","CJD",to,r,c)
s3["full_cpts"]["D300"] = {"parents":["R01"],"description":"CJD。中高年",
    "cpt":{"0_1":0.0,"1_5":0.0,"6_12":0.0,"13_17":0.0001,"18_39":0.0002,"40_64":0.001,"65_plus":0.002}}

# D301 視神経脊髄炎 (NMOSD / Devic Disease)
s1["variables"].append({"id":"D301","name":"NMOSD","name_ja":"視神経脊髄炎(NMOSD)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"AQP4抗体陽性。重度視神経炎(失明)+横断性脊髄炎(対麻痺/四肢麻痺)。MSとの鑑別重要。女性に多い"})
for to,r,c in [
    ("S52","NMOSD: 対麻痺/四肢麻痺(横断性脊髄炎)",{"absent":0.10,"unilateral_weakness":0.15,"bilateral":0.75}),
    ("S04","NMOSD: 呼吸困難(頸髄病変時, 20-30%)",{"absent":0.60,"on_exertion":0.20,"at_rest":0.20}),
    ("S13","NMOSD: 嘔吐(area postrema症候群, 30-40%)",{"absent":0.55,"present":0.45}),
    ("S05","NMOSD: 頭痛(20-30%)",{"absent":0.60,"mild":0.25,"severe":0.15}),
    ("E01","NMOSD: 発熱(稀)",{"under_37.5":0.80,"37.5_38.0":0.10,"38.0_39.0":0.07,"39.0_40.0":0.02,"over_40.0":0.01}),
    ("T01","NMOSD: 亜急性(数日~数週)",{"under_3d":0.15,"3d_to_1w":0.30,"1w_to_3w":0.40,"over_3w":0.15}),
    ("T02","NMOSD: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D301","NMOSD",to,r,c)
s3["full_cpts"]["D301"] = {"parents":["R01","R02"],"description":"NMOSD。若年~中年女性に多い",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0001,"1_5,female":0.0002,"6_12,male":0.0002,"6_12,female":0.0005,"13_17,male":0.0003,"13_17,female":0.001,"18_39,male":0.0005,"18_39,female":0.002,"40_64,male":0.0003,"40_64,female":0.001,"65_plus,male":0.0002,"65_plus,female":0.0005}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 301 diseases")
