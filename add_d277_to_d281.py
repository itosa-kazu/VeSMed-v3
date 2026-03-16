#!/usr/bin/env python3
"""Add D277-D281: 5 diseases."""
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

# D277 肺腺癌 (Lung Adenocarcinoma)
s1["variables"].append({"id":"D277","name":"lung_adenocarcinoma","name_ja":"肺腺癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"非喫煙者にも多い。咳嗽+体重減少+呼吸困難+胸痛。末梢発生が多い。胸水合併"})
for to,r,c in [
    ("S01","肺腺癌: 咳嗽(60-70%)",{"absent":0.20,"dry":0.45,"productive":0.35}),
    ("S04","肺腺癌: 呼吸困難(40-50%)",{"absent":0.40,"on_exertion":0.40,"at_rest":0.20}),
    ("S07","肺腺癌: 体重減少(50-60%)",{"absent":0.25,"mild":0.35,"severe":0.40}),
    ("S21","肺腺癌: 胸痛(30-40%)",{"absent":0.55,"burning":0.03,"sharp":0.20,"pressure":0.15,"tearing":0.07}),
    ("E01","肺腺癌: 発熱(閉塞性肺炎合併, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.12,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.03}),
    ("L04","肺腺癌: CXR(腫瘤/浸潤/胸水)",{"normal":0.08,"lobar_infiltrate":0.20,"bilateral_infiltrate":0.15,"BHL":0.05,"pleural_effusion":0.45,"pneumothorax":0.07}),
    ("L02","肺腺癌: CRP上昇",{"normal_under_0.3":0.20,"mild_0.3_3":0.25,"moderate_3_10":0.30,"high_over_10":0.25}),
    ("T01","肺腺癌: 慢性",{"under_3d":0.05,"3d_to_1w":0.08,"1w_to_3w":0.20,"over_3w":0.67}),
    ("T02","肺腺癌: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D277","lung_adenocarcinoma",to,r,c)
s3["full_cpts"]["D277"] = {"parents":["R01"],"description":"肺腺癌",
    "cpt":{"0_1":0.0001,"1_5":0.0001,"6_12":0.0001,"13_17":0.0002,"18_39":0.001,"40_64":0.004,"65_plus":0.006}}

# D278 肺扁平上皮癌 (Lung SCC) - too similar to D277, pick something else
# D278 癌性胸膜炎 (Malignant Pleural Effusion) - already D127 is 胸水(非感染性)
# D278 肺小細胞癌 (SCLC) - also lung cancer
# D278 悪性胸膜中皮腫 (Malignant Mesothelioma) - different enough
s1["variables"].append({"id":"D278","name":"mesothelioma","name_ja":"悪性胸膜中皮腫",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"アスベスト曝露歴。胸痛(持続性)+呼吸困難+大量胸水+体重減少。予後不良(中央値12ヶ月)"})
for to,r,c in [
    ("S04","中皮腫: 呼吸困難(70-80%)",{"absent":0.12,"on_exertion":0.40,"at_rest":0.48}),
    ("S21","中皮腫: 胸痛(持続性, 60-70%)",{"absent":0.25,"burning":0.05,"sharp":0.25,"pressure":0.35,"tearing":0.10}),
    ("S07","中皮腫: 体重減少(60-70%)",{"absent":0.20,"mild":0.30,"severe":0.50}),
    ("S01","中皮腫: 咳嗽(30-40%)",{"absent":0.55,"dry":0.30,"productive":0.15}),
    ("L04","中皮腫: CXR(大量片側胸水)",{"normal":0.05,"lobar_infiltrate":0.05,"bilateral_infiltrate":0.08,"BHL":0.02,"pleural_effusion":0.75,"pneumothorax":0.05}),
    ("E05","中皮腫: 低酸素(胸水)",{"normal_over_96":0.25,"mild_hypoxia_93_96":0.40,"severe_hypoxia_under_93":0.35}),
    ("T01","中皮腫: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.20,"over_3w":0.70}),
    ("T02","中皮腫: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D278","mesothelioma",to,r,c)
s3["full_cpts"]["D278"] = {"parents":["R01","R02"],"description":"中皮腫。男性+高齢者",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0,"18_39,male":0.0002,"18_39,female":0.0001,"40_64,male":0.001,"40_64,female":0.0003,"65_plus,male":0.003,"65_plus,female":0.001}}

# D279 睡眠時無呼吸症候群 → 慢性すぎて急性診断に不向き。
# D279 急性喉頭蓋炎 → already D128 上気道閉塞 covers epiglottitis.
# D279 縦隔炎 (Mediastinitis)
s1["variables"].append({"id":"D279","name":"mediastinitis","name_ja":"縦隔炎",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"食道穿孔/歯原性/術後。激しい胸痛+発熱+頸部腫脹+敗血症。死亡率20-40%"})
for to,r,c in [
    ("S21","縦隔炎: 胸痛(激烈, 90%+)",{"absent":0.03,"burning":0.03,"sharp":0.30,"pressure":0.50,"tearing":0.14}),
    ("E01","縦隔炎: 高熱(90%+)",{"under_37.5":0.05,"37.5_38.0":0.08,"38.0_39.0":0.22,"39.0_40.0":0.35,"over_40.0":0.30}),
    ("E02","縦隔炎: 頻脈(敗血症)",{"under_100":0.05,"100_120":0.25,"over_120":0.70}),
    ("E03","縦隔炎: 低血圧(敗血症性ショック)",{"normal_over_90":0.25,"hypotension_under_90":0.75}),
    ("S04","縦隔炎: 呼吸困難(60-70%)",{"absent":0.20,"on_exertion":0.25,"at_rest":0.55}),
    ("L01","縦隔炎: WBC著増",{"low_under_4000":0.03,"normal_4000_10000":0.07,"high_10000_20000":0.30,"very_high_over_20000":0.60}),
    ("L02","縦隔炎: CRP著高",{"normal_under_0.3":0.02,"mild_0.3_3":0.03,"moderate_3_10":0.15,"high_over_10":0.80}),
    ("S02","縦隔炎: 咽頭痛/嚥下困難(40-50%)",{"absent":0.45,"present":0.55}),
    ("T01","縦隔炎: 急性",{"under_3d":0.50,"3d_to_1w":0.35,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","縦隔炎: 急性",{"sudden_hours":0.40,"gradual_days":0.60}),
]: add("D279","mediastinitis",to,r,c)
s3["full_cpts"]["D279"] = {"parents":[],"description":"縦隔炎","cpt":{"":0.001}}

# D280 ベンゾジアゼピン中毒 (Benzodiazepine Overdose)
s1["variables"].append({"id":"D280","name":"benzodiazepine_OD","name_ja":"ベンゾジアゼピン中毒",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"中枢神経抑制→意識障害+呼吸抑制。混合(アルコール/オピオイド)でリスク増大。フルマゼニル拮抗"})
for to,r,c in [
    ("E16","BZD: 意識障害(90%+)",{"normal":0.05,"confused":0.35,"obtunded":0.60}),
    ("E02","BZD: 徐脈(呼吸抑制)",{"under_100":0.55,"100_120":0.30,"over_120":0.15}),
    ("E03","BZD: 低血圧(中枢抑制)",{"normal_over_90":0.40,"hypotension_under_90":0.60}),
    ("E04","BZD: 呼吸抑制(徐呼吸)",{"normal_under_20":0.40,"tachypnea_20_30":0.30,"severe_over_30":0.30}),
    ("E05","BZD: 低酸素(呼吸抑制)",{"normal_over_96":0.20,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.45}),
    ("T01","BZD: 超急性",{"under_3d":0.95,"3d_to_1w":0.04,"1w_to_3w":0.01,"over_3w":0.00}),
    ("T02","BZD: 突発",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D280","benzodiazepine_OD",to,r,c)
s3["full_cpts"]["D280"] = {"parents":[],"description":"BZD中毒","cpt":{"":0.002}}

# D281 オピオイド中毒 (Opioid Overdose)
s1["variables"].append({"id":"D281","name":"opioid_OD","name_ja":"オピオイド中毒",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"三徴:意識障害+呼吸抑制+縮瞳。ヘロイン/フェンタニル/処方オピオイド。ナロキソン拮抗"})
for to,r,c in [
    ("E16","オピオイド: 意識障害(定義的)",{"normal":0.03,"confused":0.20,"obtunded":0.77}),
    ("E02","オピオイド: 徐脈",{"under_100":0.65,"100_120":0.25,"over_120":0.10}),
    ("E03","オピオイド: 低血圧",{"normal_over_90":0.30,"hypotension_under_90":0.70}),
    ("E04","オピオイド: 呼吸抑制(徐呼吸/無呼吸)",{"normal_under_20":0.50,"tachypnea_20_30":0.25,"severe_over_30":0.25}),
    ("E05","オピオイド: 低酸素",{"normal_over_96":0.10,"mild_hypoxia_93_96":0.25,"severe_hypoxia_under_93":0.65}),
    ("E01","オピオイド: 低体温(中枢抑制)",{"under_37.5":0.70,"37.5_38.0":0.12,"38.0_39.0":0.10,"39.0_40.0":0.06,"over_40.0":0.02}),
    ("S13","オピオイド: 嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("T01","オピオイド: 超急性",{"under_3d":0.95,"3d_to_1w":0.04,"1w_to_3w":0.01,"over_3w":0.00}),
    ("T02","オピオイド: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D281","opioid_OD",to,r,c)
s3["full_cpts"]["D281"] = {"parents":[],"description":"オピオイド中毒","cpt":{"":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 281 diseases")
