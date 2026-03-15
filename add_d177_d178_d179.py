#!/usr/bin/env python3
"""Add D177 Pheochromocytoma Crisis + D178 Cholangiocarcinoma + D179 Amoebic Liver Abscess.
Actually D29 already covers 肝膿瘍（細菌性/アメーバ性）. Let me pick different ones.
D177: 褐色細胞腫クリーゼ (already D73 褐色細胞腫 exists? Let me check)
Actually D73 is 褐色細胞腫. Skip.
D177: 急性膵炎(重症) - D86 is 急性膵炎. Could add severe variant but that's same disease.
D177: 虚血性腸炎 (Ischemic Colitis) - important GI diagnosis
D178: リステリア髄膜炎 - important meningitis differential
D179: 薬剤性肝障害(DILI) - very common
"""
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
    if (did, to) in existing:
        return
    s2["edges"].append({"from": did, "to": to, "from_name": dname, "to_name": to, "reason": reason})
    existing.add((did, to))
    n[to]["parent_effects"][did] = cpt

# ===== D177 虚血性腸炎 (Ischemic Colitis) =====
s1["variables"].append({
    "id": "D177", "name": "ischemic_colitis",
    "name_ja": "虚血性腸炎",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "大腸の一過性虚血。左下腹部痛+血性下痢。高齢者+動脈硬化。多くは保存的治療で改善。壊疽型は手術要"
})
for to, reason, cpt in [
    ("S12","虚血性腸炎: 腹痛(左下腹部が典型, 90%+)",{"absent":0.03,"epigastric":0.02,"RUQ":0.02,"RLQ":0.05,"LLQ":0.55,"suprapubic":0.03,"diffuse":0.30}),
    ("S14","虚血性腸炎: 血性下痢(70-80%)",{"absent":0.10,"watery":0.15,"bloody":0.75}),
    ("S13","虚血性腸炎: 嘔気/嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("E01","虚血性腸炎: 発熱(20-30%)",{"under_37.5":0.60,"37.5_38.0":0.18,"38.0_39.0":0.15,"39.0_40.0":0.05,"over_40.0":0.02}),
    ("E02","虚血性腸炎: 頻脈(脱水/ショック)",{"under_100":0.30,"100_120":0.45,"over_120":0.25}),
    ("L01","虚血性腸炎: WBC上昇(50-60%)",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.27}),
    ("L02","虚血性腸炎: CRP上昇",{"normal_under_0.3":0.10,"mild_0.3_3":0.20,"moderate_3_10":0.40,"high_over_10":0.30}),
    ("L16","虚血性腸炎: LDH上昇(組織虚血)",{"normal":0.30,"elevated":0.70}),
    ("T01","虚血性腸炎: 急性",{"under_3d":0.65,"3d_to_1w":0.25,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","虚血性腸炎: 急性",{"sudden_hours":0.60,"gradual_days":0.40}),
]:
    add("D177","ischemic_colitis",to,reason,cpt)
s3["full_cpts"]["D177"] = {"parents":["R01"],"description":"虚血性腸炎。高齢者に多い",
    "cpt":{"18_39":0.001,"40_64":0.002,"65_plus":0.005}}

# ===== D178 リステリア髄膜炎 =====
s1["variables"].append({
    "id": "D178", "name": "listeria_meningitis",
    "name_ja": "リステリア髄膜炎",
    "category": "disease", "states": ["no", "yes"], "severity": "critical",
    "note": "Listeria monocytogenes。高齢者/免疫不全/妊婦/新生児。菱脳幹脳炎(rhombencephalitis)。アンピシリンが治療"
})
for to, reason, cpt in [
    ("E01","リステリア: 発熱(90%+)",{"under_37.5":0.08,"37.5_38.0":0.10,"38.0_39.0":0.25,"39.0_40.0":0.35,"over_40.0":0.22}),
    ("E06","リステリア: 項部硬直(60-70%)",{"absent":0.25,"present":0.75}),
    ("E16","リステリア: 意識障害(50-70%)",{"normal":0.20,"confused":0.40,"obtunded":0.40}),
    ("S05","リステリア: 頭痛(70-80%)",{"absent":0.15,"mild":0.25,"severe":0.60}),
    ("S13","リステリア: 嘔吐(50-60%)",{"absent":0.35,"present":0.65}),
    ("S52","リステリア: 局所神経脱落(脳幹脳炎, 30-40%)",{"absent":0.55,"unilateral_weakness":0.35,"bilateral":0.10}),
    ("S42","リステリア: 痙攣(20-30%)",{"absent":0.70,"present":0.30}),
    ("L01","リステリア: WBC上昇",{"low_under_4000":0.05,"normal_4000_10000":0.20,"high_10000_20000":0.45,"very_high_over_20000":0.30}),
    ("L02","リステリア: CRP上昇",{"normal_under_0.3":0.03,"mild_0.3_3":0.07,"moderate_3_10":0.25,"high_over_10":0.65}),
    ("T01","リステリア: 急性~亜急性",{"under_3d":0.35,"3d_to_1w":0.40,"1w_to_3w":0.20,"over_3w":0.05}),
    ("T02","リステリア: 亜急性",{"sudden_hours":0.25,"gradual_days":0.75}),
]:
    add("D178","listeria_meningitis",to,reason,cpt)
s3["full_cpts"]["D178"] = {"parents":["R01"],"description":"リステリア髄膜炎。高齢者/免疫不全",
    "cpt":{"18_39":0.0005,"40_64":0.001,"65_plus":0.003}}

# ===== D179 薬剤性肝障害 (DILI) =====
s1["variables"].append({
    "id": "D179", "name": "DILI",
    "name_ja": "薬剤性肝障害(DILI)",
    "category": "disease", "states": ["no", "yes"], "severity": "high",
    "note": "薬剤による肝細胞障害/胆汁うっ滞/混合型。原因薬剤中止が治療。重症はALF進展リスク。R値で分類"
})
for to, reason, cpt in [
    ("L11","DILI: 肝酵素上昇(定義的)",{"normal":0.02,"mild_elevated":0.28,"very_high":0.70}),
    ("E18","DILI: 黄疸(胆汁うっ滞型/重症, 40-60%)",{"absent":0.35,"present":0.65}),
    ("S07","DILI: 倦怠感(60-70%)",{"absent":0.25,"mild":0.40,"severe":0.35}),
    ("S13","DILI: 嘔気(40-50%)",{"absent":0.45,"present":0.55}),
    ("S12","DILI: 腹痛(RUQ, 20-30%)",{"absent":0.60,"epigastric":0.05,"RUQ":0.30,"RLQ":0.01,"LLQ":0.01,"suprapubic":0.01,"diffuse":0.02}),
    ("E01","DILI: 発熱(薬剤アレルギー型, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("L01","DILI: WBC(好酸球増多型もあり)",{"low_under_4000":0.05,"normal_4000_10000":0.50,"high_10000_20000":0.35,"very_high_over_20000":0.10}),
    ("T01","DILI: 急性~亜急性(投薬開始数日~数週後)",{"under_3d":0.15,"3d_to_1w":0.30,"1w_to_3w":0.35,"over_3w":0.20}),
    ("T02","DILI: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]:
    add("D179","DILI",to,reason,cpt)
s3["full_cpts"]["D179"] = {"parents":[],"description":"DILI。薬剤性肝障害",
    "cpt":{"":0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"D177 虚血性腸炎: 10 edges, D178 リステリア髄膜炎: 11 edges, D179 DILI: 9 edges")
print(f"Total: {s2['total_edges']} edges, 179 diseases")
