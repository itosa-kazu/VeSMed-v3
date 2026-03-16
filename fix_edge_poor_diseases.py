#!/usr/bin/env python3
"""Add missing clinically necessary edges to edge-poor new diseases (≤10 edges)."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]
existing = {(e["from"],e["to"]) for e in s2["edges"]}
added = 0
def add(did, dname, to, reason, cpt):
    global added
    if (did,to) in existing: return
    if to not in n: return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt
    added += 1

# === D262 膿痂疹(5→10辺) ===
add("D262","impetigo","L02","膿痂疹: CRP軽度上昇(20-30%)",{"normal_under_0.3":0.40,"mild_0.3_3":0.35,"moderate_3_10":0.20,"high_over_10":0.05})
add("D262","impetigo","E02","膿痂疹: 通常正常バイタル",{"under_100":0.80,"100_120":0.15,"over_120":0.05})
add("D262","impetigo","S07","膿痂疹: 倦怠感(軽度, 20-30%)",{"absent":0.60,"mild":0.30,"severe":0.10})
add("D262","impetigo","L02","膿痂疹: CRP",{"normal_under_0.3":0.40,"mild_0.3_3":0.35,"moderate_3_10":0.20,"high_over_10":0.05})

# === D293 BPPV(5→10辺) ===
add("D293","BPPV","E02","BPPV: 通常正常バイタル",{"under_100":0.85,"100_120":0.12,"over_120":0.03})
add("D293","BPPV","E16","BPPV: 意識正常(めまいだが意識清明)",{"normal":0.95,"confused":0.04,"obtunded":0.01})
add("D293","BPPV","S07","BPPV: 不安/倦怠(20-30%)",{"absent":0.60,"mild":0.30,"severe":0.10})
add("D293","BPPV","L01","BPPV: WBC正常",{"low_under_4000":0.03,"normal_4000_10000":0.90,"high_10000_20000":0.06,"very_high_over_20000":0.01})
add("D293","BPPV","L02","BPPV: CRP正常",{"normal_under_0.3":0.85,"mild_0.3_3":0.10,"moderate_3_10":0.04,"high_over_10":0.01})

# === D296 緊張型頭痛(5→10辺) ===
add("D296","TTH","E02","TTH: 通常正常バイタル",{"under_100":0.90,"100_120":0.08,"over_120":0.02})
add("D296","TTH","E16","TTH: 意識正常",{"normal":0.98,"confused":0.02,"obtunded":0.00})
add("D296","TTH","S13","TTH: 嘔気なし(片頭痛との鑑別)",{"absent":0.90,"present":0.10})
add("D296","TTH","E38","TTH: 血圧正常",{"normal_under_140":0.85,"elevated_140_180":0.12,"crisis_over_180":0.03})
add("D296","TTH","L01","TTH: WBC正常",{"low_under_4000":0.03,"normal_4000_10000":0.90,"high_10000_20000":0.06,"very_high_over_20000":0.01})

# === D297 三叉神経痛(5→10辺) ===
add("D297","TN","E02","三叉神経痛: 通常正常バイタル",{"under_100":0.85,"100_120":0.12,"over_120":0.03})
add("D297","TN","E16","三叉神経痛: 意識正常",{"normal":0.98,"confused":0.02,"obtunded":0.00})
add("D297","TN","S13","三叉神経痛: 嘔気(発作で20-30%)",{"absent":0.65,"present":0.35})
add("D297","TN","L01","三叉神経痛: WBC正常",{"low_under_4000":0.03,"normal_4000_10000":0.90,"high_10000_20000":0.06,"very_high_over_20000":0.01})
add("D297","TN","S07","三叉神経痛: 倦怠感(慢性痛で, 30-40%)",{"absent":0.50,"mild":0.35,"severe":0.15})

# === D339 網膜剥離(5→10辺) ===
add("D339","RD","E01","網膜剥離: 通常無熱",{"under_37.5":0.90,"37.5_38.0":0.05,"38.0_39.0":0.03,"39.0_40.0":0.01,"over_40.0":0.01})
add("D339","RD","E02","網膜剥離: 通常正常バイタル",{"under_100":0.85,"100_120":0.12,"over_120":0.03})
add("D339","RD","E16","網膜剥離: 意識正常",{"normal":0.98,"confused":0.02,"obtunded":0.00})
add("D339","RD","S13","網膜剥離: 嘔気(不安で, 10-15%)",{"absent":0.85,"present":0.15})
add("D339","RD","L01","網膜剥離: WBC正常",{"low_under_4000":0.03,"normal_4000_10000":0.90,"high_10000_20000":0.06,"very_high_over_20000":0.01})

# === D302 PSP(6→12辺) ===
add("D302","PSP","E01","PSP: 通常無熱",{"under_37.5":0.85,"37.5_38.0":0.08,"38.0_39.0":0.05,"39.0_40.0":0.02,"over_40.0":0.00})
add("D302","PSP","E02","PSP: 通常正常バイタル",{"under_100":0.85,"100_120":0.12,"over_120":0.03})
add("D302","PSP","S42","PSP: 転倒(定義的だが痙攣ではない)",{"absent":0.90,"present":0.10})
add("D302","PSP","L01","PSP: WBC正常",{"low_under_4000":0.05,"normal_4000_10000":0.85,"high_10000_20000":0.08,"very_high_over_20000":0.02})
add("D302","PSP","L02","PSP: CRP正常",{"normal_under_0.3":0.80,"mild_0.3_3":0.12,"moderate_3_10":0.06,"high_over_10":0.02})
add("D302","PSP","S05","PSP: 頭痛(稀, 10-15%)",{"absent":0.80,"mild":0.15,"severe":0.05})

# === D303 パーキンソン(7→12辺) ===
add("D303","PD","E01","PD: 通常無熱",{"under_37.5":0.90,"37.5_38.0":0.05,"38.0_39.0":0.03,"39.0_40.0":0.01,"over_40.0":0.01})
add("D303","PD","E02","PD: 通常正常バイタル",{"under_100":0.80,"100_120":0.15,"over_120":0.05})
add("D303","PD","S42","PD: 転倒(進行期, 30-40%)",{"absent":0.55,"present":0.45})
add("D303","PD","L01","PD: WBC正常",{"low_under_4000":0.05,"normal_4000_10000":0.85,"high_10000_20000":0.08,"very_high_over_20000":0.02})
add("D303","PD","S05","PD: 頭痛(稀)",{"absent":0.85,"mild":0.12,"severe":0.03})

# === D304 DLB(7→12辺) ===
add("D304","DLB","E01","DLB: 通常無熱",{"under_37.5":0.85,"37.5_38.0":0.08,"38.0_39.0":0.05,"39.0_40.0":0.02,"over_40.0":0.00})
add("D304","DLB","E02","DLB: 通常正常(自律神経障害で起立性低血圧あり)",{"under_100":0.65,"100_120":0.25,"over_120":0.10})
add("D304","DLB","L01","DLB: WBC正常",{"low_under_4000":0.05,"normal_4000_10000":0.85,"high_10000_20000":0.08,"very_high_over_20000":0.02})
add("D304","DLB","S05","DLB: 頭痛(稀)",{"absent":0.85,"mild":0.12,"severe":0.03})
add("D304","DLB","L02","DLB: CRP正常",{"normal_under_0.3":0.80,"mild_0.3_3":0.12,"moderate_3_10":0.06,"high_over_10":0.02})

# === D294 片頭痛(8→12辺) ===
add("D294","migraine","E02","片頭痛: 通常正常バイタル",{"under_100":0.75,"100_120":0.18,"over_120":0.07})
add("D294","migraine","E16","片頭痛: 意識正常",{"normal":0.95,"confused":0.04,"obtunded":0.01})
add("D294","migraine","L01","片頭痛: WBC正常",{"low_under_4000":0.03,"normal_4000_10000":0.90,"high_10000_20000":0.06,"very_high_over_20000":0.01})
add("D294","migraine","L02","片頭痛: CRP正常",{"normal_under_0.3":0.85,"mild_0.3_3":0.10,"moderate_3_10":0.04,"high_over_10":0.01})

# === D295 群発頭痛(7→11辺) ===
add("D295","cluster","E02","群発頭痛: 発作時頻脈(交感亢進, 30-40%)",{"under_100":0.45,"100_120":0.35,"over_120":0.20})
add("D295","cluster","E16","群発頭痛: 意識正常",{"normal":0.95,"confused":0.04,"obtunded":0.01})
add("D295","cluster","L01","群発頭痛: WBC正常",{"low_under_4000":0.03,"normal_4000_10000":0.90,"high_10000_20000":0.06,"very_high_over_20000":0.01})
add("D295","cluster","L02","群発頭痛: CRP正常",{"normal_under_0.3":0.85,"mild_0.3_3":0.10,"moderate_3_10":0.04,"high_over_10":0.01})

# === D271 EoE(6→10辺) ===
add("D271","EoE","E01","EoE: 通常無熱",{"under_37.5":0.90,"37.5_38.0":0.05,"38.0_39.0":0.03,"39.0_40.0":0.01,"over_40.0":0.01})
add("D271","EoE","E02","EoE: 通常正常バイタル",{"under_100":0.85,"100_120":0.12,"over_120":0.03})
add("D271","EoE","S25","EoE: 嚥下困難(定義的, 70-80%)",{"absent":0.15,"present":0.85})
add("D271","EoE","L01","EoE: WBC正常~好酸球上昇",{"low_under_4000":0.03,"normal_4000_10000":0.60,"high_10000_20000":0.30,"very_high_over_20000":0.07})

# === D272 食道アカラシア(7→11辺) ===
add("D272","achalasia","E01","アカラシア: 通常無熱",{"under_37.5":0.85,"37.5_38.0":0.08,"38.0_39.0":0.05,"39.0_40.0":0.02,"over_40.0":0.00})
add("D272","achalasia","E02","アカラシア: 通常正常バイタル",{"under_100":0.80,"100_120":0.15,"over_120":0.05})
add("D272","achalasia","S25","アカラシア: 嚥下困難(定義的, 90%+)",{"absent":0.05,"present":0.95})
add("D272","achalasia","L01","アカラシア: WBC正常",{"low_under_4000":0.03,"normal_4000_10000":0.90,"high_10000_20000":0.06,"very_high_over_20000":0.01})

# === D298 Bell麻痺(7→11辺) ===
add("D298","bell_palsy","E02","Bell麻痺: 通常正常バイタル",{"under_100":0.85,"100_120":0.12,"over_120":0.03})
add("D298","bell_palsy","L01","Bell麻痺: WBC正常",{"low_under_4000":0.05,"normal_4000_10000":0.85,"high_10000_20000":0.08,"very_high_over_20000":0.02})
add("D298","bell_palsy","L02","Bell麻痺: CRP正常~軽度上昇",{"normal_under_0.3":0.60,"mild_0.3_3":0.25,"moderate_3_10":0.12,"high_over_10":0.03})
add("D298","bell_palsy","E16","Bell麻痺: 意識正常",{"normal":0.98,"confused":0.02,"obtunded":0.00})

# === D299 Ramsay Hunt(7→11辺) ===
add("D299","ramsay_hunt","E02","Ramsay Hunt: 通常正常バイタル",{"under_100":0.80,"100_120":0.15,"over_120":0.05})
add("D299","ramsay_hunt","L01","Ramsay Hunt: WBC正常~軽度上昇",{"low_under_4000":0.05,"normal_4000_10000":0.70,"high_10000_20000":0.20,"very_high_over_20000":0.05})
add("D299","ramsay_hunt","L02","Ramsay Hunt: CRP軽度上昇",{"normal_under_0.3":0.35,"mild_0.3_3":0.35,"moderate_3_10":0.25,"high_over_10":0.05})
add("D299","ramsay_hunt","E16","Ramsay Hunt: 意識正常",{"normal":0.95,"confused":0.04,"obtunded":0.01})

# === D300 CJD(7→11辺) ===
add("D300","CJD","E01","CJD: 通常無熱",{"under_37.5":0.85,"37.5_38.0":0.08,"38.0_39.0":0.05,"39.0_40.0":0.02,"over_40.0":0.00})
add("D300","CJD","E02","CJD: 通常正常バイタル",{"under_100":0.75,"100_120":0.18,"over_120":0.07})
add("D300","CJD","S42","CJD: ミオクローヌス/痙攣(60-70%)",{"absent":0.25,"present":0.75})
add("D300","CJD","L01","CJD: WBC正常",{"low_under_4000":0.05,"normal_4000_10000":0.85,"high_10000_20000":0.08,"very_high_over_20000":0.02})

s2["total_edges"] = len(s2["edges"])
# Trinity
edges_set = {(e["from"],e["to"]) for e in s2["edges"]}
enc = sum(1 for e in s2["edges"] if e["to"] in n and isinstance(n[e["to"]],dict) and e["from"] not in n[e["to"]].get("parent_effects",{}))
cne = sum(1 for vid,p in n.items() if isinstance(p,dict) for did in p.get("parent_effects",{}) if (did,vid) not in edges_set)
for fn,d in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fn), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total {s2['total_edges']}")
print(f"Trinity: EDGE_NO_CPT={enc}, CPT_NO_EDGE={cne}")
