#!/usr/bin/env python3
"""Add D272-D276: 5 diseases."""
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

# D272 食道アカラシア (Achalasia)
s1["variables"].append({"id":"D272","name":"achalasia","name_ja":"食道アカラシア",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"LES弛緩不全+食道蠕動消失。嚥下困難(固形+液体)+regurgitation+体重減少+胸痛"})
for to,r,c in [
    ("S21","アカラシア: 胸痛(食道痙攣, 30-40%)",{"absent":0.50,"burning":0.20,"sharp":0.10,"pressure":0.15,"tearing":0.05}),
    ("S13","アカラシア: 嘔吐/逆流(60-70%)",{"absent":0.25,"present":0.75}),
    ("S07","アカラシア: 体重減少(50-60%)",{"absent":0.30,"mild":0.40,"severe":0.30}),
    ("S01","アカラシア: 咳嗽(夜間誤嚥, 20-30%)",{"absent":0.65,"dry":0.25,"productive":0.10}),
    ("T01","アカラシア: 慢性",{"under_3d":0.03,"3d_to_1w":0.05,"1w_to_3w":0.15,"over_3w":0.77}),
    ("T02","アカラシア: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D272","achalasia",to,r,c)
s3["full_cpts"]["D272"] = {"parents":["R01"],"description":"アカラシア",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0003,"13_17":0.0005,"18_39":0.001,"40_64":0.001,"65_plus":0.001}}

# D273 総胆管結石 (Choledocholithiasis)
s1["variables"].append({"id":"D273","name":"choledocholithiasis","name_ja":"総胆管結石",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"胆石がCBDに嵌頓。疝痛様RUQ痛+黄疸+発熱(Charcot三徴は胆管炎合併時)。ERCP治療"})
for to,r,c in [
    ("S12","CBD結石: RUQ痛(80%+)",{"absent":0.08,"epigastric":0.10,"RUQ":0.70,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.07}),
    ("E18","CBD結石: 黄疸(60-70%)",{"absent":0.25,"present":0.75}),
    ("S13","CBD結石: 嘔気/嘔吐(50-60%)",{"absent":0.35,"present":0.65}),
    ("E01","CBD結石: 発熱(胆管炎合併時, 30-40%)",{"under_37.5":0.45,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.15,"over_40.0":0.05}),
    ("L11","CBD結石: 肝酵素上昇(胆汁うっ滞)",{"normal":0.10,"mild_elevated":0.40,"very_high":0.50}),
    ("L01","CBD結石: WBC上昇(胆管炎時)",{"low_under_4000":0.03,"normal_4000_10000":0.30,"high_10000_20000":0.40,"very_high_over_20000":0.27}),
    ("L02","CBD結石: CRP上昇",{"normal_under_0.3":0.15,"mild_0.3_3":0.15,"moderate_3_10":0.35,"high_over_10":0.35}),
    ("E10","CBD結石: Murphy徴候(胆嚢炎合併時)",{"negative":0.40,"positive":0.60}),
    ("T01","CBD結石: 急性",{"under_3d":0.50,"3d_to_1w":0.30,"1w_to_3w":0.15,"over_3w":0.05}),
    ("T02","CBD結石: 急性",{"sudden_hours":0.50,"gradual_days":0.50}),
]: add("D273","choledocholithiasis",to,r,c)
s3["full_cpts"]["D273"] = {"parents":["R01"],"description":"総胆管結石",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0003,"13_17":0.0005,"18_39":0.002,"40_64":0.004,"65_plus":0.006}}

# D274 胆石症 (Cholelithiasis/Biliary Colic)
s1["variables"].append({"id":"D274","name":"biliary_colic","name_ja":"胆石発作(胆石疝痛)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"胆石嵌頓→RUQ疝痛(食後30分~数時間)。発熱なし(胆嚢炎との鑑別)。Murphy陰性"})
for to,r,c in [
    ("S12","胆石: RUQ痛(90%+)",{"absent":0.03,"epigastric":0.08,"RUQ":0.80,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.04}),
    ("S13","胆石: 嘔気/嘔吐(60-70%)",{"absent":0.25,"present":0.75}),
    ("E01","胆石: 無熱(胆嚢炎なし)",{"under_37.5":0.80,"37.5_38.0":0.10,"38.0_39.0":0.07,"39.0_40.0":0.02,"over_40.0":0.01}),
    ("E10","胆石: Murphy陰性(胆嚢炎なし)",{"negative":0.75,"positive":0.25}),
    ("L01","胆石: WBC正常",{"low_under_4000":0.05,"normal_4000_10000":0.60,"high_10000_20000":0.28,"very_high_over_20000":0.07}),
    ("T01","胆石: 急性(発作は30分~数時間)",{"under_3d":0.70,"3d_to_1w":0.20,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","胆石: 突発(食後)",{"sudden_hours":0.70,"gradual_days":0.30}),
]: add("D274","biliary_colic",to,r,c)
s3["full_cpts"]["D274"] = {"parents":["R01","R02"],"description":"胆石発作。F>M, 4F(Fat/Female/Forty/Fertile)",
    "cpt":{"0_1,male":0.0001,"0_1,female":0.0001,"1_5,male":0.0002,"1_5,female":0.0002,"6_12,male":0.0003,"6_12,female":0.0005,"13_17,male":0.0005,"13_17,female":0.001,"18_39,male":0.002,"18_39,female":0.004,"40_64,male":0.003,"40_64,female":0.006,"65_plus,male":0.004,"65_plus,female":0.007}}

# D275 急性膵炎(胆石性) - D86 already covers acute pancreatitis.
# Better: D275 腹壁ヘルニア嵌頓 (Incarcerated Hernia)
s1["variables"].append({"id":"D275","name":"incarcerated_hernia","name_ja":"嵌頓ヘルニア",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"鼠径/大腿/臍/腹壁瘢痕ヘルニアが還納不能。腸閉塞→絞扼→壊死。緊急手術"})
for to,r,c in [
    ("S12","嵌頓ヘルニア: 腹痛(局所→びまん性)",{"absent":0.03,"epigastric":0.03,"RUQ":0.03,"RLQ":0.25,"LLQ":0.10,"suprapubic":0.10,"diffuse":0.46}),
    ("S13","嵌頓ヘルニア: 嘔吐(腸閉塞, 70-80%)",{"absent":0.15,"present":0.85}),
    ("E09","嵌頓ヘルニア: 腹部(圧痛+膨満+腹膜刺激)",{"soft_nontender":0.05,"localized_tenderness":0.35,"peritoneal_signs":0.60}),
    ("E01","嵌頓ヘルニア: 発熱(絞扼時, 30-40%)",{"under_37.5":0.50,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.12,"over_40.0":0.03}),
    ("E02","嵌頓ヘルニア: 頻脈(ショック)",{"under_100":0.20,"100_120":0.40,"over_120":0.40}),
    ("L01","嵌頓ヘルニア: WBC上昇(絞扼時)",{"low_under_4000":0.03,"normal_4000_10000":0.20,"high_10000_20000":0.45,"very_high_over_20000":0.32}),
    ("L02","嵌頓ヘルニア: CRP上昇",{"normal_under_0.3":0.08,"mild_0.3_3":0.15,"moderate_3_10":0.35,"high_over_10":0.42}),
    ("T01","嵌頓ヘルニア: 急性",{"under_3d":0.75,"3d_to_1w":0.20,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","嵌頓ヘルニア: 急性",{"sudden_hours":0.55,"gradual_days":0.45}),
]: add("D275","incarcerated_hernia",to,r,c)
s3["full_cpts"]["D275"] = {"parents":["R01"],"description":"嵌頓ヘルニア",
    "cpt":{"0_1":0.003,"1_5":0.002,"6_12":0.001,"13_17":0.001,"18_39":0.002,"40_64":0.003,"65_plus":0.005}}

# D276 卵巣捻転 (Ovarian Torsion)
s1["variables"].append({"id":"D276","name":"ovarian_torsion","name_ja":"卵巣捻転",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"卵巣/卵管が靭帯軸で捻転→血流途絶→壊死。突然のLLQ/RLQ痛+嘔吐。緊急手術"})
for to,r,c in [
    ("S12","卵巣捻転: 下腹部痛(突然, 片側性)",{"absent":0.02,"epigastric":0.02,"RUQ":0.05,"RLQ":0.40,"LLQ":0.40,"suprapubic":0.05,"diffuse":0.06}),
    ("S13","卵巣捻転: 嘔吐(70-80%)",{"absent":0.15,"present":0.85}),
    ("E01","卵巣捻転: 発熱(壊死時, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("E02","卵巣捻転: 頻脈(疼痛)",{"under_100":0.20,"100_120":0.45,"over_120":0.35}),
    ("L01","卵巣捻転: WBC(正常~軽度上昇)",{"low_under_4000":0.05,"normal_4000_10000":0.40,"high_10000_20000":0.40,"very_high_over_20000":0.15}),
    ("T01","卵巣捻転: 超急性",{"under_3d":0.85,"3d_to_1w":0.12,"1w_to_3w":0.02,"over_3w":0.01}),
    ("T02","卵巣捻転: 突発",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D276","ovarian_torsion",to,r,c)
s3["full_cpts"]["D276"] = {"parents":["R01","R02"],"description":"卵巣捻転。女性のみ",
    "cpt":{"0_1,male":0.0,"0_1,female":0.001,"1_5,male":0.0,"1_5,female":0.001,"6_12,male":0.0,"6_12,female":0.002,"13_17,male":0.0,"13_17,female":0.003,"18_39,male":0.0,"18_39,female":0.003,"40_64,male":0.0,"40_64,female":0.002,"65_plus,male":0.0,"65_plus,female":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 276 diseases")
