#!/usr/bin/env python3
"""Add D232-D236: 5 diseases."""
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

# D232 アルコール性ケトアシドーシス (AKA)
s1["variables"].append({"id":"D232","name":"alcoholic_ketoacidosis","name_ja":"アルコール性ケトアシドーシス(AKA)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"大量飲酒後の絶食→ケトアシドーシス。嘔吐+脱水+腹痛。AG開大+ケトン体。血糖は正常~低"})
for to,r,c in [
    ("S13","AKA: 嘔吐(80%+)",{"absent":0.10,"present":0.90}),
    ("S12","AKA: 腹痛(60-70%)",{"absent":0.25,"epigastric":0.30,"RUQ":0.05,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.35}),
    ("E02","AKA: 頻脈(脱水)",{"under_100":0.10,"100_120":0.40,"over_120":0.50}),
    ("E04","AKA: 頻呼吸(Kussmaul)",{"normal_under_20":0.10,"tachypnea_20_30":0.35,"severe_over_30":0.55}),
    ("E03","AKA: 低血圧(脱水)",{"normal_over_90":0.35,"hypotension_under_90":0.65}),
    ("S07","AKA: 倦怠感",{"absent":0.10,"mild":0.25,"severe":0.65}),
    ("E16","AKA: 意識障害(30-40%)",{"normal":0.45,"confused":0.35,"obtunded":0.20}),
    ("T01","AKA: 急性",{"under_3d":0.75,"3d_to_1w":0.20,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","AKA: 急性",{"sudden_hours":0.50,"gradual_days":0.50}),
]: add("D232","alcoholic_ketoacidosis",to,r,c)
s3["full_cpts"]["D232"] = {"parents":[],"description":"AKA","cpt":{"":0.002}}

# D233 急性腎皮質壊死 → 稀すぎ。代わりに：
# D233 アジソン病/副腎不全（慢性） → D72が副腎クリーゼ(急性)。慢性型を追加
# 実はD72で十分カバーされている。Skip。
# D233 フィッシャー症候群 (Miller Fisher Syndrome)
s1["variables"].append({"id":"D233","name":"miller_fisher","name_ja":"フィッシャー症候群",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"GBS亜型。三徴:眼球運動障害+運動失調+腱反射消失。抗GQ1b抗体陽性。先行感染後1-3週"})
for to,r,c in [
    ("S52","フィッシャー: 眼球運動障害/失調(三徴)",{"absent":0.05,"unilateral_weakness":0.10,"bilateral":0.85}),
    ("S05","フィッシャー: 頭痛(20-30%)",{"absent":0.60,"mild":0.25,"severe":0.15}),
    ("E16","フィッシャー: 意識障害(Bickerstaff脳幹脳炎overlap時)",{"normal":0.60,"confused":0.25,"obtunded":0.15}),
    ("S53","フィッシャー: 構音障害(球麻痺, 20-30%)",{"absent":0.65,"dysarthria":0.28,"aphasia":0.07}),
    ("E01","フィッシャー: 通常無熱",{"under_37.5":0.75,"37.5_38.0":0.12,"38.0_39.0":0.08,"39.0_40.0":0.04,"over_40.0":0.01}),
    ("T01","フィッシャー: 亜急性(先行感染1-3週後)",{"under_3d":0.10,"3d_to_1w":0.30,"1w_to_3w":0.45,"over_3w":0.15}),
    ("T02","フィッシャー: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D233","miller_fisher",to,r,c)
s3["full_cpts"]["D233"] = {"parents":[],"description":"フィッシャー症候群","cpt":{"":0.0005}}

# D234 慢性骨髄性白血病 (CML)
s1["variables"].append({"id":"D234","name":"CML","name_ja":"慢性骨髄性白血病(CML)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"Ph染色体/BCR-ABL。慢性期:著明白血球増多+脾腫+倦怠感。急性転化でblast crisis"})
for to,r,c in [
    ("L01","CML: WBC著増(定義的, 多くは>50k)",{"low_under_4000":0.02,"normal_4000_10000":0.05,"high_10000_20000":0.15,"very_high_over_20000":0.78}),
    ("S07","CML: 倦怠感(60-70%)",{"absent":0.20,"mild":0.40,"severe":0.40}),
    ("S12","CML: 腹痛(脾腫, LUQ, 40-50%)",{"absent":0.40,"epigastric":0.05,"RUQ":0.03,"RLQ":0.02,"LLQ":0.40,"suprapubic":0.02,"diffuse":0.08}),
    ("E01","CML: 発熱(blast crisis時, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.12,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.03}),
    ("L16","CML: LDH上昇(細胞回転亢進)",{"normal":0.15,"elevated":0.85}),
    ("T01","CML: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","CML: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D234","CML",to,r,c)
s3["full_cpts"]["D234"] = {"parents":["R01"],"description":"CML","cpt":{"18_39":0.001,"40_64":0.002,"65_plus":0.002}}

# D235 慢性リンパ性白血病 (CLL)
s1["variables"].append({"id":"D235","name":"CLL","name_ja":"慢性リンパ性白血病(CLL)",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"B細胞リンパ増殖。リンパ球増多+リンパ節腫脹+脾腫。高齢者。感染リスク(低γ)"})
for to,r,c in [
    ("L01","CLL: WBC著増(リンパ球優位)",{"low_under_4000":0.03,"normal_4000_10000":0.08,"high_10000_20000":0.20,"very_high_over_20000":0.69}),
    ("L14","CLL: リンパ球優位",{"normal":0.05,"left_shift":0.02,"atypical_lymphocytes":0.05,"thrombocytopenia":0.08,"eosinophilia":0.00,"lymphocyte_predominant":0.80}),
    ("S07","CLL: 倦怠感(50-60%)",{"absent":0.30,"mild":0.40,"severe":0.30}),
    ("E01","CLL: 発熱(感染合併時, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.12,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.03}),
    ("L16","CLL: LDH上昇(Richter転化時)",{"normal":0.35,"elevated":0.65}),
    ("T01","CLL: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.15,"over_3w":0.70}),
    ("T02","CLL: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D235","CLL",to,r,c)
s3["full_cpts"]["D235"] = {"parents":["R01"],"description":"CLL. 高齢者","cpt":{"18_39":0.0002,"40_64":0.001,"65_plus":0.003}}

# D236 多発性硬化症 (MS)
s1["variables"].append({"id":"D236","name":"multiple_sclerosis","name_ja":"多発性硬化症(MS)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"CNS脱髄。時間的・空間的多発。視力障害+感覚障害+運動障害+膀胱障害。若年女性に多い"})
for to,r,c in [
    ("S52","MS: 局所神経脱落(運動, 50-60%)",{"absent":0.25,"unilateral_weakness":0.55,"bilateral":0.20}),
    ("S53","MS: 構音障害(脳幹病変, 20-30%)",{"absent":0.65,"dysarthria":0.28,"aphasia":0.07}),
    ("S07","MS: 倦怠感(80%+)",{"absent":0.10,"mild":0.35,"severe":0.55}),
    ("E16","MS: 意識障害(稀, ADEM型で, 5-10%)",{"normal":0.85,"confused":0.12,"obtunded":0.03}),
    ("S04","MS: 呼吸困難(脊髄病変, 5-10%)",{"absent":0.85,"on_exertion":0.10,"at_rest":0.05}),
    ("T01","MS: 亜急性(急性増悪は数日~数週)",{"under_3d":0.10,"3d_to_1w":0.25,"1w_to_3w":0.40,"over_3w":0.25}),
    ("T02","MS: 亜急性",{"sudden_hours":0.15,"gradual_days":0.85}),
]: add("D236","multiple_sclerosis",to,r,c)
s3["full_cpts"]["D236"] = {"parents":["R01","R02"],"description":"MS. 若年女性に多い",
    "cpt":{"18_39,male":0.001,"18_39,female":0.003,"40_64,male":0.0005,"40_64,female":0.001,"65_plus,male":0.0002,"65_plus,female":0.0005}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 236 diseases")
