#!/usr/bin/env python3
"""Add D242-D246: 5 diseases."""
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

# D242 胃潰瘍/十二指腸潰瘍 (Peptic Ulcer, non-perforated)
s1["variables"].append({"id":"D242","name":"peptic_ulcer","name_ja":"消化性潰瘍(非穿孔性)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"H.pylori/NSAIDs。心窩部痛(食後増悪=胃/空腹時増悪=十二指腸)。出血(吐血/黒色便)リスク"})
for to,r,c in [
    ("S12","消化性潰瘍: 心窩部痛(90%+)",{"absent":0.03,"epigastric":0.80,"RUQ":0.05,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.07}),
    ("S13","消化性潰瘍: 嘔気(50-60%)",{"absent":0.35,"present":0.65}),
    ("S44","消化性潰瘍: 出血(吐血/黒色便, 15-20%)",{"absent":0.75,"present":0.25}),
    ("E01","消化性潰瘍: 通常無熱",{"under_37.5":0.85,"37.5_38.0":0.08,"38.0_39.0":0.05,"39.0_40.0":0.01,"over_40.0":0.01}),
    ("L01","消化性潰瘍: WBC(出血時上昇)",{"low_under_4000":0.05,"normal_4000_10000":0.55,"high_10000_20000":0.30,"very_high_over_20000":0.10}),
    ("T01","消化性潰瘍: 急性~慢性",{"under_3d":0.20,"3d_to_1w":0.25,"1w_to_3w":0.25,"over_3w":0.30}),
    ("T02","消化性潰瘍: 亜急性",{"sudden_hours":0.25,"gradual_days":0.75}),
]: add("D242","peptic_ulcer",to,r,c)
s3["full_cpts"]["D242"] = {"parents":["R01"],"description":"消化性潰瘍","cpt":{"18_39":0.005,"40_64":0.006,"65_plus":0.008}}

# D243 逆流性食道炎 (already D133 GERD exists? check)
# D133 is GERD. Skip.
# D243 食道静脈瘤破裂 (Esophageal Variceal Bleeding)
s1["variables"].append({"id":"D243","name":"variceal_bleeding","name_ja":"食道静脈瘤破裂",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"肝硬変門脈圧亢進→食道/胃静脈瘤破裂→大量吐血。致死率20-30%。EVL/TIPS/SBT"})
for to,r,c in [
    ("S44","静脈瘤破裂: 大量吐血(100%)",{"absent":0.02,"present":0.98}),
    ("E03","静脈瘤破裂: 低血圧(出血性ショック)",{"normal_over_90":0.15,"hypotension_under_90":0.85}),
    ("E02","静脈瘤破裂: 頻脈(出血)",{"under_100":0.05,"100_120":0.25,"over_120":0.70}),
    ("E16","静脈瘤破裂: 意識障害(肝性脳症+ショック)",{"normal":0.20,"confused":0.40,"obtunded":0.40}),
    ("L11","静脈瘤破裂: 肝酵素(肝硬変baseline)",{"normal":0.20,"mild_elevated":0.50,"very_high":0.30}),
    ("E18","静脈瘤破裂: 黄疸(肝硬変)",{"absent":0.30,"present":0.70}),
    ("T01","静脈瘤破裂: 超急性",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","静脈瘤破裂: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D243","variceal_bleeding",to,r,c)
s3["full_cpts"]["D243"] = {"parents":["R01"],"description":"食道静脈瘤破裂","cpt":{"18_39":0.001,"40_64":0.003,"65_plus":0.005}}

# D244 Mallory-Weiss症候群
s1["variables"].append({"id":"D244","name":"mallory_weiss","name_ja":"マロリー・ワイス症候群",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"嘔吐→食道胃接合部裂傷→吐血。アルコール/妊娠悪阻が原因。多くは自然止血"})
for to,r,c in [
    ("S44","Mallory-Weiss: 吐血(定義的)",{"absent":0.05,"present":0.95}),
    ("S13","Mallory-Weiss: 嘔吐(先行, 90%+)",{"absent":0.05,"present":0.95}),
    ("S12","Mallory-Weiss: 心窩部痛(50-60%)",{"absent":0.30,"epigastric":0.55,"RUQ":0.03,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.07}),
    ("E02","Mallory-Weiss: 頻脈(出血時)",{"under_100":0.35,"100_120":0.40,"over_120":0.25}),
    ("T01","Mallory-Weiss: 超急性",{"under_3d":0.85,"3d_to_1w":0.12,"1w_to_3w":0.02,"over_3w":0.01}),
    ("T02","Mallory-Weiss: 突発",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D244","mallory_weiss",to,r,c)
s3["full_cpts"]["D244"] = {"parents":[],"description":"Mallory-Weiss","cpt":{"":0.003}}

# D245 急性胃粘膜病変 (AGML)
s1["variables"].append({"id":"D245","name":"AGML","name_ja":"急性胃粘膜病変(AGML)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"ストレス/NSAIDs/アルコール→急性びらん/出血。心窩部痛+嘔気+吐血/黒色便"})
for to,r,c in [
    ("S12","AGML: 心窩部痛(80%+)",{"absent":0.10,"epigastric":0.70,"RUQ":0.03,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.12}),
    ("S13","AGML: 嘔気/嘔吐(60-70%)",{"absent":0.25,"present":0.75}),
    ("S44","AGML: 出血(30-40%)",{"absent":0.55,"present":0.45}),
    ("E01","AGML: 通常無熱",{"under_37.5":0.80,"37.5_38.0":0.10,"38.0_39.0":0.07,"39.0_40.0":0.02,"over_40.0":0.01}),
    ("T01","AGML: 急性",{"under_3d":0.65,"3d_to_1w":0.25,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","AGML: 急性",{"sudden_hours":0.55,"gradual_days":0.45}),
]: add("D245","AGML",to,r,c)
s3["full_cpts"]["D245"] = {"parents":[],"description":"AGML","cpt":{"":0.005}}

# D246 腸管出血性大腸菌感染症 (EHEC/O157)
s1["variables"].append({"id":"D246","name":"EHEC","name_ja":"腸管出血性大腸菌感染症(EHEC/O157)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"志賀毒素産生性大腸菌(O157:H7等)。水様便→血性下痢。HUS合併リスク(5-10%)。抗菌薬禁忌論争"})
for to,r,c in [
    ("S14","EHEC: 血性下痢(90%+)",{"absent":0.03,"watery":0.07,"bloody":0.90}),
    ("S12","EHEC: 腹痛(びまん性/疝痛様, 90%+)",{"absent":0.03,"epigastric":0.05,"RUQ":0.05,"RLQ":0.10,"LLQ":0.10,"suprapubic":0.02,"diffuse":0.65}),
    ("S13","EHEC: 嘔吐(50-60%)",{"absent":0.35,"present":0.65}),
    ("E01","EHEC: 発熱(30-40%, 軽度)",{"under_37.5":0.45,"37.5_38.0":0.20,"38.0_39.0":0.20,"39.0_40.0":0.12,"over_40.0":0.03}),
    ("L01","EHEC: WBC上昇(50-60%)",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.27}),
    ("L02","EHEC: CRP上昇",{"normal_under_0.3":0.10,"mild_0.3_3":0.20,"moderate_3_10":0.40,"high_over_10":0.30}),
    ("T01","EHEC: 急性(食品摂取3-8日後)",{"under_3d":0.30,"3d_to_1w":0.50,"1w_to_3w":0.18,"over_3w":0.02}),
    ("T02","EHEC: 急性",{"sudden_hours":0.30,"gradual_days":0.70}),
]: add("D246","EHEC",to,r,c)
s3["full_cpts"]["D246"] = {"parents":[],"description":"EHEC/O157","cpt":{"":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 246 diseases")
