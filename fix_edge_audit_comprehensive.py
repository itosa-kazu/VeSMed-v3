#!/usr/bin/env python3
"""Comprehensive edge audit for 350-disease model with 712 cases."""
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

# D322 HELLP → E02 頻脈 (ショック/DIC)
add("D322","HELLP","E02","HELLP: 頻脈(出血/DIC/ショック, 30-40%)",{"under_100":0.35,"100_120":0.35,"over_120":0.30})
# D322 HELLP → L55 腎機能 (AKI合併 20-30%)
add("D322","HELLP","L55","HELLP: AKI(20-30%)",{"normal":0.50,"mild_elevated":0.25,"high_AKI":0.25})
# D322 HELLP → L01 WBC (上昇 40-50%)
add("D322","HELLP","L01","HELLP: WBC上昇(炎症/ストレス, 40-50%)",{"low_under_4000":0.03,"normal_4000_10000":0.35,"high_10000_20000":0.40,"very_high_over_20000":0.22})

# D323 胎盤早期剥離 → S12 腹痛部位
add("D323","placental_abruption","S12","胎盤早期剥離: 下腹部/恥骨上痛(80%+)",{"absent":0.08,"epigastric":0.05,"RUQ":0.02,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.40,"diffuse":0.35})
# D323 → L14 血小板減少 (DIC)
add("D323","placental_abruption","L14","胎盤早期剥離: 血小板減少(DIC, 30-40%)",{"normal":0.40,"left_shift":0.10,"atypical_lymphocytes":0.02,"thrombocytopenia":0.40,"eosinophilia":0.02,"lymphocyte_predominant":0.06})
# D323 → L01 WBC
add("D323","placental_abruption","L01","胎盤早期剥離: WBC上昇(ストレス/感染)",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.27})

# D326 TLS → L23 尿酸 (定義的)
add("D326","TLS","L23","TLS: 尿酸上昇(定義的, 80%+)",{"normal":0.05,"elevated":0.95})
# D326 TLS → L16 LDH (上昇 80%+)
add("D326","TLS","L16","TLS: LDH上昇(腫瘍崩壊, 80%+)",{"normal":0.05,"elevated":0.95})
# D326 TLS → L01 WBC
add("D326","TLS","L01","TLS: WBC変動(白血病/リンパ腫背景)",{"low_under_4000":0.10,"normal_4000_10000":0.20,"high_10000_20000":0.30,"very_high_over_20000":0.40})
# D326 TLS → L11 肝酵素 (腫瘍崩壊で上昇)
add("D326","TLS","L11","TLS: 肝酵素上昇(腫瘍崩壊, 40-50%)",{"normal":0.30,"mild_elevated":0.30,"very_high":0.40})

# D321 原発性アルドステロン → E02 (不整脈/VT/低K)
add("D321","primary_aldosteronism","E02","アルドステロン症: 不整脈/頻脈(低K→VT, 20-30%)",{"under_100":0.40,"100_120":0.30,"over_120":0.30})

# D306 急性SDH → S44 出血
add("D306","acute_subdural_hematoma","S44","急性SDH: 出血(頭蓋内出血, 定義的)",{"absent":0.20,"present":0.80})

# D327 AS → S13 嘔気 (失神/低灌流で)
add("D327","aortic_stenosis","S13","AS: 嘔気(失神/低灌流時, 20-30%)",{"absent":0.65,"present":0.35})
# D327 AS → S42 失神 (三徴の一つ)
add("D327","aortic_stenosis","S42","AS: 失神(三徴の一つ, 15-30%)",{"absent":0.60,"present":0.40})

# D328 ARDS → S01 咳嗽 (原因疾患で)
add("D328","ARDS","S01","ARDS: 咳嗽(原因疾患:肺炎等, 50-60%)",{"absent":0.30,"dry":0.25,"productive":0.45})

# D333 先端巨大症 → S13 嘔吐 (腫瘍圧迫/頭蓋内圧)
add("D333","acromegaly","S13","先端巨大症: 嘔気嘔吐(腫瘤効果/頭蓋内圧, 20-30%)",{"absent":0.65,"present":0.35})
# D333 → S52 局所神経症状 (視野障害/脳神経圧迫)
add("D333","acromegaly","S52","先端巨大症: 視野障害/局所神経症状(視交叉圧迫, 30-40%)",{"absent":0.50,"unilateral_weakness":0.35,"bilateral":0.15})

# D345 Sheehan → S44 出血歴 (定義的)
add("D345","sheehan","S44","Sheehan: 産後出血(定義的)",{"absent":0.10,"present":0.90})
# D345 → E02 頻脈 (副腎不全/ショック)
add("D345","sheehan","E02","Sheehan: 頻脈(副腎不全/ショック, 40-50%)",{"under_100":0.30,"100_120":0.35,"over_120":0.35})

# D348 ウィルムス → S04 呼吸困難 (心不全/肺転移)
add("D348","wilms_tumor","S04","ウィルムス: 呼吸困難(心不全/肺転移, 20-30%)",{"absent":0.55,"on_exertion":0.25,"at_rest":0.20})
# D348 → E02 頻脈 (高血圧/心不全)
add("D348","wilms_tumor","E02","ウィルムス: 頻脈(高血圧性心不全, 30-40%)",{"under_100":0.30,"100_120":0.35,"over_120":0.35})
# D348 → L11 肝酵素 (肝うっ血/転移)
add("D348","wilms_tumor","L11","ウィルムス: 肝酵素上昇(肝うっ血/転移, 20-30%)",{"normal":0.55,"mild_elevated":0.30,"very_high":0.15})
# D348 → E38 高血圧 (レニン産生)
add("D348","wilms_tumor","E38","ウィルムス: 高血圧(レニン産生, 25-30%)",{"normal_under_140":0.55,"elevated_140_180":0.30,"crisis_over_180":0.15})

# D341 Brugada → E05 SpO2
add("D341","brugada","E05","Brugada: SpO2(VF後に低下あり)",{"normal_over_96":0.60,"mild_hypoxia_93_96":0.25,"severe_hypoxia_under_93":0.15})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']} edges")
