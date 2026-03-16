#!/usr/bin/env python3
"""Add D292-D296: 5 diseases."""
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

# D292 子宮筋腫 (Uterine Fibroids / Leiomyoma) - too chronic. Better:
# D292 前置胎盤/常位胎盤早期剥離 - obstetric, too specific
# D292 急性前庭神経炎 (Acute Vestibular Neuritis)
s1["variables"].append({"id":"D292","name":"vestibular_neuritis","name_ja":"急性前庭神経炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"突然の回転性めまい+嘔吐+歩行障害。聴力正常(メニエールとの鑑別)。ウイルス感染先行。1-2週で改善"})
for to,r,c in [
    ("S13","前庭神経炎: 嘔吐(80%+)",{"absent":0.10,"present":0.90}),
    ("S05","前庭神経炎: 頭痛(20-30%)",{"absent":0.60,"mild":0.25,"severe":0.15}),
    ("E16","前庭神経炎: めまい(回転性, 定義的)",{"normal":0.05,"confused":0.70,"obtunded":0.25}),
    ("E02","前庭神経炎: 頻脈(自律神経反応)",{"under_100":0.30,"100_120":0.45,"over_120":0.25}),
    ("E01","前庭神経炎: 通常無熱",{"under_37.5":0.70,"37.5_38.0":0.15,"38.0_39.0":0.10,"39.0_40.0":0.04,"over_40.0":0.01}),
    ("T01","前庭神経炎: 急性(突然発症)",{"under_3d":0.50,"3d_to_1w":0.35,"1w_to_3w":0.13,"over_3w":0.02}),
    ("T02","前庭神経炎: 突発",{"sudden_hours":0.80,"gradual_days":0.20}),
]: add("D292","vestibular_neuritis",to,r,c)
s3["full_cpts"]["D292"] = {"parents":["R01"],"description":"前庭神経炎",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0005,"13_17":0.001,"18_39":0.003,"40_64":0.003,"65_plus":0.002}}

# D293 良性発作性頭位めまい症 (BPPV)
s1["variables"].append({"id":"D293","name":"BPPV","name_ja":"良性発作性頭位めまい症(BPPV)",
    "category":"disease","states":["no","yes"],"severity":"low",
    "note":"頭位変換で誘発される短時間(30秒)の回転性めまい+嘔気。後半規管型が最多。Dix-Hallpike陽性"})
for to,r,c in [
    ("S13","BPPV: 嘔気(50-60%)",{"absent":0.35,"present":0.65}),
    ("S05","BPPV: 頭痛(20-30%)",{"absent":0.65,"mild":0.25,"severe":0.10}),
    ("E01","BPPV: 無熱",{"under_37.5":0.90,"37.5_38.0":0.05,"38.0_39.0":0.03,"39.0_40.0":0.01,"over_40.0":0.01}),
    ("T01","BPPV: 急性~反復性",{"under_3d":0.35,"3d_to_1w":0.30,"1w_to_3w":0.20,"over_3w":0.15}),
    ("T02","BPPV: 突発(頭位変換で)",{"sudden_hours":0.75,"gradual_days":0.25}),
]: add("D293","BPPV",to,r,c)
s3["full_cpts"]["D293"] = {"parents":["R01"],"description":"BPPV",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0005,"13_17":0.001,"18_39":0.003,"40_64":0.005,"65_plus":0.008}}

# D294 片頭痛 (Migraine)
s1["variables"].append({"id":"D294","name":"migraine","name_ja":"片頭痛",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"片側性拍動性頭痛+嘔気/嘔吐+光過敏/音過敏。前兆(aura)あり/なし。4-72時間持続"})
for to,r,c in [
    ("S05","片頭痛: 頭痛(定義的, 片側拍動性)",{"absent":0.02,"mild":0.10,"severe":0.88}),
    ("S13","片頭痛: 嘔気/嘔吐(70-80%)",{"absent":0.15,"present":0.85}),
    ("E01","片頭痛: 通常無熱",{"under_37.5":0.85,"37.5_38.0":0.08,"38.0_39.0":0.05,"39.0_40.0":0.01,"over_40.0":0.01}),
    ("E02","片頭痛: 頻脈(自律神経症状)",{"under_100":0.35,"100_120":0.40,"over_120":0.25}),
    ("T01","片頭痛: 急性(4-72h)",{"under_3d":0.65,"3d_to_1w":0.25,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","片頭痛: 急性",{"sudden_hours":0.50,"gradual_days":0.50}),
]: add("D294","migraine",to,r,c)
s3["full_cpts"]["D294"] = {"parents":["R01","R02"],"description":"片頭痛。若年女性に多い",
    "cpt":{"0_1,male":0.0001,"0_1,female":0.0002,"1_5,male":0.001,"1_5,female":0.002,"6_12,male":0.003,"6_12,female":0.005,"13_17,male":0.005,"13_17,female":0.010,"18_39,male":0.005,"18_39,female":0.012,"40_64,male":0.004,"40_64,female":0.008,"65_plus,male":0.002,"65_plus,female":0.004}}

# D295 群発頭痛 (Cluster Headache)
s1["variables"].append({"id":"D295","name":"cluster_headache","name_ja":"群発頭痛",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"片眼窩周囲の激烈頭痛+流涙+鼻閉/鼻漏+発汗。15-180分持続。群発期(数週~数月)+寛解期。男性に多い"})
for to,r,c in [
    ("S05","群発頭痛: 激烈頭痛(片側眼窩周囲, 定義的)",{"absent":0.02,"mild":0.03,"severe":0.95}),
    ("S03","群発頭痛: 鼻閉/鼻漏(自律神経症状, 60-70%)",{"absent":0.25,"clear_rhinorrhea":0.60,"purulent_rhinorrhea":0.15}),
    ("E02","群発頭痛: 頻脈(激痛)",{"under_100":0.20,"100_120":0.45,"over_120":0.35}),
    ("E01","群発頭痛: 無熱",{"under_37.5":0.90,"37.5_38.0":0.05,"38.0_39.0":0.03,"39.0_40.0":0.01,"over_40.0":0.01}),
    ("T01","群発頭痛: 急性(15-180分の発作)",{"under_3d":0.60,"3d_to_1w":0.25,"1w_to_3w":0.10,"over_3w":0.05}),
    ("T02","群発頭痛: 突発",{"sudden_hours":0.80,"gradual_days":0.20}),
]: add("D295","cluster_headache",to,r,c)
s3["full_cpts"]["D295"] = {"parents":["R01","R02"],"description":"群発頭痛。男性に多い(M:F=3:1)",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0003,"6_12,female":0.0001,"13_17,male":0.001,"13_17,female":0.0003,"18_39,male":0.003,"18_39,female":0.001,"40_64,male":0.003,"40_64,female":0.001,"65_plus,male":0.001,"65_plus,female":0.0003}}

# D296 緊張型頭痛 (Tension-Type Headache)
s1["variables"].append({"id":"D296","name":"tension_headache","name_ja":"緊張型頭痛",
    "category":"disease","states":["no","yes"],"severity":"low",
    "note":"両側性の圧迫感/締め付け感。嘔気なし(片頭痛との鑑別)。日常動作で増悪しない。最も頻度が高い頭痛"})
for to,r,c in [
    ("S05","緊張型: 頭痛(両側性圧迫感, 定義的)",{"absent":0.02,"mild":0.45,"severe":0.53}),
    ("S07","緊張型: 倦怠感(40-50%)",{"absent":0.40,"mild":0.40,"severe":0.20}),
    ("E01","緊張型: 無熱",{"under_37.5":0.92,"37.5_38.0":0.04,"38.0_39.0":0.03,"39.0_40.0":0.01,"over_40.0":0.00}),
    ("T01","緊張型: 急性~慢性(30分~7日)",{"under_3d":0.40,"3d_to_1w":0.30,"1w_to_3w":0.15,"over_3w":0.15}),
    ("T02","緊張型: 緩徐",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D296","tension_headache",to,r,c)
s3["full_cpts"]["D296"] = {"parents":["R01","R02"],"description":"緊張型頭痛。最頻度",
    "cpt":{"0_1,male":0.0001,"0_1,female":0.0001,"1_5,male":0.001,"1_5,female":0.001,"6_12,male":0.003,"6_12,female":0.004,"13_17,male":0.005,"13_17,female":0.008,"18_39,male":0.008,"18_39,female":0.012,"40_64,male":0.006,"40_64,female":0.010,"65_plus,male":0.004,"65_plus,female":0.006}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 296 diseases")
