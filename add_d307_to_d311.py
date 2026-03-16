#!/usr/bin/env python3
"""Add D307-D311: 5 diseases."""
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

# D307 脊髄損傷 (Spinal Cord Injury) - too traumatic/surgical.
# D307 横断性脊髄炎 (Transverse Myelitis)
s1["variables"].append({"id":"D307","name":"transverse_myelitis","name_ja":"横断性脊髄炎",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"脊髄の急性炎症→対麻痺+膀胱直腸障害+感覚レベル。感染後/MS/NMOSD/SLE/特発性"})
for to,r,c in [
    ("S52","横断性脊髄炎: 対麻痺(80%+)",{"absent":0.05,"unilateral_weakness":0.15,"bilateral":0.80}),
    ("S15","横断性脊髄炎: 背部痛(50-60%)",{"absent":0.30,"present":0.70}),
    ("E01","横断性脊髄炎: 発熱(感染後型, 30-40%)",{"under_37.5":0.50,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.12,"over_40.0":0.03}),
    ("S04","横断性脊髄炎: 呼吸困難(高位病変, 20-30%)",{"absent":0.60,"on_exertion":0.20,"at_rest":0.20}),
    ("S07","横断性脊髄炎: 倦怠感",{"absent":0.20,"mild":0.35,"severe":0.45}),
    ("T01","横断性脊髄炎: 亜急性(数時間~数日)",{"under_3d":0.30,"3d_to_1w":0.35,"1w_to_3w":0.25,"over_3w":0.10}),
    ("T02","横断性脊髄炎: 急性~亜急性",{"sudden_hours":0.30,"gradual_days":0.70}),
]: add("D307","transverse_myelitis",to,r,c)
s3["full_cpts"]["D307"] = {"parents":["R01"],"description":"横断性脊髄炎",
    "cpt":{"0_1":0.0002,"1_5":0.0005,"6_12":0.001,"13_17":0.001,"18_39":0.002,"40_64":0.002,"65_plus":0.001}}

# D308 脊柱管狭窄症 (Spinal Stenosis) - too chronic. Better:
# D308 馬尾症候群 (Cauda Equina Syndrome)
s1["variables"].append({"id":"D308","name":"cauda_equina","name_ja":"馬尾症候群",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"馬尾神経圧迫→両下肢脱力+膀胱直腸障害+会陰部感覚低下(鞍型麻痺)。椎間板ヘルニア/腫瘍。48h以内手術"})
for to,r,c in [
    ("S52","馬尾: 両下肢脱力(70-80%)",{"absent":0.10,"unilateral_weakness":0.20,"bilateral":0.70}),
    ("S15","馬尾: 腰背部痛(90%+)",{"absent":0.05,"present":0.95}),
    ("S10","馬尾: 排尿障害(定義的, 60-80%)",{"absent":0.15,"present":0.85}),
    ("S07","馬尾: 倦怠感",{"absent":0.30,"mild":0.35,"severe":0.35}),
    ("T01","馬尾: 急性~亜急性",{"under_3d":0.35,"3d_to_1w":0.30,"1w_to_3w":0.25,"over_3w":0.10}),
    ("T02","馬尾: 急性~亜急性",{"sudden_hours":0.35,"gradual_days":0.65}),
]: add("D308","cauda_equina",to,r,c)
s3["full_cpts"]["D308"] = {"parents":["R01"],"description":"馬尾症候群",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0005,"13_17":0.001,"18_39":0.002,"40_64":0.003,"65_plus":0.003}}

# D309 脳動静脈奇形 (AVM)
s1["variables"].append({"id":"D309","name":"AVM","name_ja":"脳動静脈奇形(AVM)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"先天性脳血管奇形。頭蓋内出血/痙攣/頭痛で発症。20-40歳に多い。Spetzler-Martin分類"})
for to,r,c in [
    ("S05","AVM: 頭痛(出血時激烈, 50-60%)",{"absent":0.25,"mild":0.15,"severe":0.60}),
    ("S42","AVM: 痙攣(20-30%)",{"absent":0.65,"present":0.35}),
    ("S52","AVM: 局所神経脱落(出血時, 40-50%)",{"absent":0.40,"unilateral_weakness":0.50,"bilateral":0.10}),
    ("E16","AVM: 意識障害(出血時, 50-60%)",{"normal":0.25,"confused":0.35,"obtunded":0.40}),
    ("E38","AVM: 高血圧(交感神経亢進)",{"normal_under_140":0.30,"elevated_140_180":0.35,"crisis_over_180":0.35}),
    ("T01","AVM: 超急性(出血時)",{"under_3d":0.80,"3d_to_1w":0.15,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","AVM: 突発",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D309","AVM",to,r,c)
s3["full_cpts"]["D309"] = {"parents":["R01"],"description":"脳AVM。若年~中年",
    "cpt":{"0_1":0.0002,"1_5":0.0005,"6_12":0.001,"13_17":0.002,"18_39":0.003,"40_64":0.002,"65_plus":0.001}}

# D310 一過性脳虚血発作 (TIA)
s1["variables"].append({"id":"D310","name":"TIA","name_ja":"一過性脳虚血発作(TIA)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"一過性の局所神経症状(<24h, 多くは<1h)。脳梗塞の前駆。ABCD2スコアで脳卒中リスク評価"})
for to,r,c in [
    ("S52","TIA: 局所神経脱落(片麻痺, 定義的)",{"absent":0.05,"unilateral_weakness":0.80,"bilateral":0.15}),
    ("S53","TIA: 構音障害/失語(30-40%)",{"absent":0.50,"dysarthria":0.35,"aphasia":0.15}),
    ("S05","TIA: 頭痛(20-30%)",{"absent":0.60,"mild":0.25,"severe":0.15}),
    ("E38","TIA: 高血圧(60-70%)",{"normal_under_140":0.20,"elevated_140_180":0.45,"crisis_over_180":0.35}),
    ("E02","TIA: 頻脈(AF合併, 30-40%)",{"under_100":0.30,"100_120":0.40,"over_120":0.30}),
    ("T01","TIA: 超急性(<24h)",{"under_3d":0.90,"3d_to_1w":0.08,"1w_to_3w":0.02,"over_3w":0.00}),
    ("T02","TIA: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D310","TIA",to,r,c)
s3["full_cpts"]["D310"] = {"parents":["R01"],"description":"TIA",
    "cpt":{"0_1":0.0001,"1_5":0.0001,"6_12":0.0002,"13_17":0.0005,"18_39":0.001,"40_64":0.004,"65_plus":0.008}}

# D311 脳腫瘍(膠芽腫) (Glioblastoma)
s1["variables"].append({"id":"D311","name":"glioblastoma","name_ja":"膠芽腫(GBM)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"最も悪性の脳腫瘍。頭痛+嘔吐+局所神経症状+痙攣。中央生存期間15ヶ月"})
for to,r,c in [
    ("S05","GBM: 頭痛(進行性, 50-60%)",{"absent":0.25,"mild":0.20,"severe":0.55}),
    ("S52","GBM: 局所神経脱落(40-50%)",{"absent":0.35,"unilateral_weakness":0.50,"bilateral":0.15}),
    ("S42","GBM: 痙攣(20-40%)",{"absent":0.55,"present":0.45}),
    ("E16","GBM: 意識障害(40-50%)",{"normal":0.35,"confused":0.35,"obtunded":0.30}),
    ("S13","GBM: 嘔吐(頭蓋内圧亢進, 30-40%)",{"absent":0.55,"present":0.45}),
    ("S53","GBM: 構音障害/失語(20-30%)",{"absent":0.60,"dysarthria":0.25,"aphasia":0.15}),
    ("S07","GBM: 倦怠感",{"absent":0.15,"mild":0.35,"severe":0.50}),
    ("T01","GBM: 亜急性~慢性",{"under_3d":0.08,"3d_to_1w":0.15,"1w_to_3w":0.30,"over_3w":0.47}),
    ("T02","GBM: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D311","glioblastoma",to,r,c)
s3["full_cpts"]["D311"] = {"parents":["R01"],"description":"膠芽腫",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0003,"13_17":0.0005,"18_39":0.001,"40_64":0.003,"65_plus":0.004}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 311 diseases")
