#!/usr/bin/env python3
"""Edge audit fix for D302+ diseases with existing test cases."""
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

# R589: D312 髄膜腫 → S53 構音障害/失語 (左前頭葉腫瘍で表出性失語 25-35%)
add("D312","meningioma","S53","髄膜腫: 構音障害/失語(前頭葉/側頭葉病変, 25-35%)",
    {"absent":0.55,"dysarthria":0.25,"aphasia":0.20})

# R591: D313 脳転移 → E01 体温 (発熱は原発巣/感染で 20-30%)
add("D313","brain_metastasis","E01","脳転移: 発熱(原発巣/感染合併, 20-30%)",
    {"under_37.5":0.55,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.05})

# R592: D313 脳転移 → L11 肝酵素 (肝転移で上昇)
add("D313","brain_metastasis","L11","脳転移: 肝酵素上昇(肝転移合併, 30-40%)",
    {"normal":0.40,"mild_elevated":0.30,"very_high":0.30})

# R593: D314 急性水頭症 → E01 体温 (通常無熱, 感染性では発熱)
add("D314","acute_hydrocephalus","E01","急性水頭症: 体温(通常無熱, 感染性で上昇あり)",
    {"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.13,"39.0_40.0":0.08,"over_40.0":0.04})

# R596: D315 CVST → E38 血圧 (子癇合併で高血圧)
add("D315","CVST","E38","CVST: 高血圧(子癇/頭蓋内圧亢進, 30-40%)",
    {"normal_under_140":0.40,"elevated_140_180":0.30,"crisis_over_180":0.30})

# R597: D315 CVST → L01 WBC (感染性CVSTで上昇)
add("D315","CVST","L01","CVST: WBC上昇(感染性CVST, 30-40%)",
    {"low_under_4000":0.05,"normal_4000_10000":0.45,"high_10000_20000":0.35,"very_high_over_20000":0.15})

# R597: D315 CVST → L02 CRP (感染性CVSTで上昇)
add("D315","CVST","L02","CVST: CRP上昇(感染性CVST, 30-40%)",
    {"normal_under_0.3":0.30,"mild_0.3_3":0.25,"moderate_3_10":0.25,"high_over_10":0.20})

# R598: D316 もやもや → E38 血圧 (急性発症で高血圧)
add("D316","moyamoya","E38","もやもや: 高血圧(急性脳血管イベント, 40-50%)",
    {"normal_under_140":0.30,"elevated_140_180":0.35,"crisis_over_180":0.35})

# R599: D316 もやもや → E01 体温 (通常無熱)
add("D316","moyamoya","E01","もやもや: 体温(通常無熱)",
    {"under_37.5":0.75,"37.5_38.0":0.12,"38.0_39.0":0.08,"39.0_40.0":0.04,"over_40.0":0.01})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']} edges")
