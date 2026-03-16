#!/usr/bin/env python3
"""Add D337-D341: 5 diseases."""
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

# D337 肥厚性幽門狭窄症 (Hypertrophic Pyloric Stenosis)
s1["variables"].append({"id":"D337","name":"pyloric_stenosis","name_ja":"肥厚性幽門狭窄症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"生後2-8週の乳児。幽門筋肥厚→噴射状嘔吐→脱水+低Cl性代謝性アルカローシス。オリーブ状腫瘤触知。Ramstedt手術"})
for to,r,c in [
    ("S13","肥厚性幽門狭窄: 噴射状嘔吐(定義的, 100%)",{"absent":0.02,"present":0.98}),
    ("E02","肥厚性幽門狭窄: 頻脈(脱水, 50-60%)",{"under_100":0.25,"100_120":0.35,"over_120":0.40}),
    ("L44","肥厚性幽門狭窄: 低Cl性アルカローシス→other",{"normal":0.15,"hyponatremia":0.10,"hyperkalemia":0.03,"other":0.72}),
    ("S07","肥厚性幽門狭窄: 体重減少(60-70%)",{"absent":0.20,"mild":0.30,"severe":0.50}),
    ("E01","肥厚性幽門狭窄: 通常無熱",{"under_37.5":0.80,"37.5_38.0":0.12,"38.0_39.0":0.06,"39.0_40.0":0.02,"over_40.0":0.00}),
    ("T01","肥厚性幽門狭窄: 亜急性(1-3週)",{"under_3d":0.10,"3d_to_1w":0.25,"1w_to_3w":0.45,"over_3w":0.20}),
    ("T02","肥厚性幽門狭窄: 漸進性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D337","pyloric_stenosis",to,r,c)
s3["full_cpts"]["D337"] = {"parents":["R01","R02"],"description":"肥厚性幽門狭窄。生後2-8週男児",
    "cpt":{"0_1,male":0.01,"0_1,female":0.003,"1_5,male":0.0001,"1_5,female":0.0001,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0,"18_39,male":0.0,"18_39,female":0.0,"40_64,male":0.0,"40_64,female":0.0,"65_plus,male":0.0,"65_plus,female":0.0}}

# D338 腸重積症 (Intussusception)
s1["variables"].append({"id":"D338","name":"intussusception","name_ja":"腸重積症",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"腸管が自身に陥入。小児(3ヶ月-6歳)に多い。間欠的腹痛+嘔吐+血便(イチゴゼリー状)。腹部エコーでtarget sign"})
for to,r,c in [
    ("S15","腸重積: 間欠的腹痛(90%+)",{"absent":0.05,"present":0.95}),
    ("S13","腸重積: 嘔吐(80%+)",{"absent":0.10,"present":0.90}),
    ("S44","腸重積: 血便(イチゴゼリー, 50-60%)",{"absent":0.30,"present":0.70}),
    ("E02","腸重積: 頻脈(痛み/脱水, 40-50%)",{"under_100":0.30,"100_120":0.35,"over_120":0.35}),
    ("S07","腸重積: ぐったり(50-60%)",{"absent":0.25,"mild":0.25,"severe":0.50}),
    ("E01","腸重積: 発熱(30-40%)",{"under_37.5":0.50,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.12,"over_40.0":0.03}),
    ("T01","腸重積: 急性",{"under_3d":0.75,"3d_to_1w":0.20,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","腸重積: 急性",{"sudden_hours":0.65,"gradual_days":0.35}),
]: add("D338","intussusception",to,r,c)
s3["full_cpts"]["D338"] = {"parents":["R01"],"description":"腸重積。3ヶ月-6歳に多い",
    "cpt":{"0_1":0.008,"1_5":0.005,"6_12":0.001,"13_17":0.0003,"18_39":0.0002,"40_64":0.0003,"65_plus":0.0005}}

# D339 網膜剥離 (Retinal Detachment)
s1["variables"].append({"id":"D339","name":"retinal_detachment","name_ja":"網膜剥離",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"網膜が色素上皮から剥離。飛蚊症→光視症→視野欠損→視力低下。裂孔原性(最多)/牽引性/滲出性。緊急手術"})
for to,r,c in [
    ("S05","網膜剥離: 視覚異常(頭痛として, 20-30%)",{"absent":0.60,"mild":0.30,"severe":0.10}),
    ("S07","網膜剥離: 不安/倦怠感",{"absent":0.50,"mild":0.35,"severe":0.15}),
    ("T01","網膜剥離: 急性~亜急性",{"under_3d":0.40,"3d_to_1w":0.30,"1w_to_3w":0.20,"over_3w":0.10}),
    ("T02","網膜剥離: 急性",{"sudden_hours":0.55,"gradual_days":0.45}),
]: add("D339","retinal_detachment",to,r,c)
s3["full_cpts"]["D339"] = {"parents":["R01"],"description":"網膜剥離。中高年",
    "cpt":{"0_1":0.0001,"1_5":0.0002,"6_12":0.0005,"13_17":0.001,"18_39":0.002,"40_64":0.003,"65_plus":0.003}}

# D340 僧帽弁狭窄症 (Mitral Stenosis)
s1["variables"].append({"id":"D340","name":"mitral_stenosis","name_ja":"僧帽弁狭窄症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"リウマチ熱後遺症が最多。左房拡大→心房細動→肺うっ血→呼吸困難。拡張期ランブル+opening snap。左房血栓→脳塞栓"})
for to,r,c in [
    ("S04","僧帽弁狭窄: 呼吸困難(80%+)",{"absent":0.08,"on_exertion":0.52,"at_rest":0.40}),
    ("E02","僧帽弁狭窄: AF→頻脈(40-50%)",{"under_100":0.25,"100_120":0.35,"over_120":0.40}),
    ("S07","僧帽弁狭窄: 倦怠感(50-60%)",{"absent":0.25,"mild":0.35,"severe":0.40}),
    ("E07","僧帽弁狭窄: 肺聴診(crackles, 肺うっ血)",{"clear":0.20,"crackles":0.55,"wheezes":0.15,"decreased_absent":0.10}),
    ("L51","僧帽弁狭窄: BNP上昇",{"not_done":0.15,"normal":0.15,"mildly_elevated":0.35,"very_high":0.35}),
    ("S44","僧帽弁狭窄: 喀血(10-20%)",{"absent":0.80,"present":0.20}),
    ("E36","僧帽弁狭窄: 下肢浮腫(右心不全, 30-40%)",{"absent":0.50,"unilateral":0.05,"bilateral":0.45}),
    ("T01","僧帽弁狭窄: 慢性",{"under_3d":0.08,"3d_to_1w":0.12,"1w_to_3w":0.15,"over_3w":0.65}),
    ("T02","僧帽弁狭窄: 緩徐",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D340","mitral_stenosis",to,r,c)
s3["full_cpts"]["D340"] = {"parents":["R01","R02"],"description":"僧帽弁狭窄症。リウマチ熱後。女性に多い",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0001,"6_12,female":0.0002,"13_17,male":0.0003,"13_17,female":0.0005,"18_39,male":0.001,"18_39,female":0.002,"40_64,male":0.001,"40_64,female":0.003,"65_plus,male":0.001,"65_plus,female":0.002}}

# D341 Brugada症候群
s1["variables"].append({"id":"D341","name":"brugada","name_ja":"Brugada症候群",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"SCN5A変異→coved型ST上昇(V1-V3)。失神/心室細動/突然死。30-50歳男性、東南アジアに多い。ICD適応"})
for to,r,c in [
    ("S42","Brugada: 失神/痙攣(VF→, 30-40%)",{"absent":0.50,"present":0.50}),
    ("E16","Brugada: 意識消失(VF, 30-40%)",{"normal":0.45,"confused":0.25,"obtunded":0.30}),
    ("E02","Brugada: 不整脈(VT/VF)",{"under_100":0.30,"100_120":0.20,"over_120":0.50}),
    ("E01","Brugada: 発熱で増悪(20-30%)",{"under_37.5":0.55,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.05}),
    ("T01","Brugada: 突発(失神/VF)",{"under_3d":0.85,"3d_to_1w":0.10,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","Brugada: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D341","brugada",to,r,c)
s3["full_cpts"]["D341"] = {"parents":["R01","R02"],"description":"Brugada症候群。30-50歳男性",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0001,"6_12,female":0.0,"13_17,male":0.0005,"13_17,female":0.0001,"18_39,male":0.002,"18_39,female":0.0003,"40_64,male":0.002,"40_64,female":0.0003,"65_plus,male":0.001,"65_plus,female":0.0001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 341 diseases")
