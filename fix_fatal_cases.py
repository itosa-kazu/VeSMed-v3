#!/usr/bin/env python3
"""Fix FATAL cases by adding missing edges."""
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

# R600 FATAL: D322 HELLP → L14 血小板減少(定義的)
add("D322","HELLP","L14","HELLP: 血小板減少(定義的, <100k)",
    {"normal":0.05,"left_shift":0.05,"atypical_lymphocytes":0.02,"thrombocytopenia":0.80,"eosinophilia":0.02,"lymphocyte_predominant":0.06})
# D322 HELLP → L16 LDH上昇(溶血, 定義的)
add("D322","HELLP","L16","HELLP: LDH上昇(溶血, 定義的)",
    {"normal":0.05,"elevated":0.95})
# D322 HELLP → S12 心窩部/右上腹部痛(65-90%)
add("D322","HELLP","S12","HELLP: 心窩部/右上腹部痛(65-90%)",
    {"absent":0.10,"epigastric":0.40,"RUQ":0.40,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.02,"diffuse":0.04})

# R608 FATAL: D324 TB meningitis → L45 CSF pattern
add("D324","TB_meningitis","L45","結核性髄膜炎: 髄液(リンパ球優位+糖低下+蛋白上昇)",
    {"not_done":0.05,"normal":0.03,"viral_pattern":0.07,"bacterial_pattern":0.10,"HSV_PCR_positive":0.01,"tb_fungal_pattern":0.74})
# D324 TB → L44 低Na(SIADH合併で30-40%)
add("D324","TB_meningitis","L44","結核性髄膜炎: 低Na血症(SIADH, 30-40%)",
    {"normal":0.45,"hyponatremia":0.45,"hyperkalemia":0.03,"other":0.07})

# R623 FATAL: D319 気管支拡張 → E05 SpO2 (増悪時低下)
add("D319","bronchiectasis","E05","気管支拡張: SpO2低下(増悪/大量喀血時)",
    {"normal_over_96":0.30,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.35})
# D319 → E02 頻脈 (感染増悪時)
add("D319","bronchiectasis","E02","気管支拡張: 頻脈(感染増悪/喀血時)",
    {"under_100":0.30,"100_120":0.35,"over_120":0.35})

# R658 FATAL: D336 ADPKD → E05 SpO2 (出血性ショック時)
add("D336","ADPKD","E05","ADPKD: SpO2低下(出血性ショック/腎不全)",
    {"normal_over_96":0.40,"mild_hypoxia_93_96":0.30,"severe_hypoxia_under_93":0.30})
# D336 → E02 頻脈 (出血/感染)
add("D336","ADPKD","E02","ADPKD: 頻脈(出血/感染合併時)",
    {"under_100":0.30,"100_120":0.35,"over_120":0.35})
# D336 → S04 呼吸困難 (腎不全→肺水腫/貧血)
add("D336","ADPKD","S04","ADPKD: 呼吸困難(腎不全→肺水腫/重度貧血)",
    {"absent":0.35,"on_exertion":0.35,"at_rest":0.30})
# D336 → E16 意識障害 (尿毒症/出血性ショック)
add("D336","ADPKD","E16","ADPKD: 意識障害(尿毒症/出血性ショック)",
    {"normal":0.50,"confused":0.30,"obtunded":0.20})
# D336 → S13 嘔気 (尿毒症)
add("D336","ADPKD","S13","ADPKD: 嘔気嘔吐(尿毒症, 40-50%)",
    {"absent":0.40,"present":0.60})
# D336 → L01 WBC (UTI合併)
add("D336","ADPKD","L01","ADPKD: WBC上昇(UTI/嚢胞感染, 30-40%)",
    {"low_under_4000":0.05,"normal_4000_10000":0.40,"high_10000_20000":0.35,"very_high_over_20000":0.20})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']} edges")
