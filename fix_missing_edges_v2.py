#!/usr/bin/env python3
"""Fix missing edges found by systematic audit."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]

added = 0
existing = {(e["from"],e["to"]) for e in s2["edges"]}
def add(did, dname, to, reason, cpt):
    global added
    if (did, to) in existing:
        return
    s2["edges"].append({"from": did, "to": to, "from_name": dname, "to_name": to, "reason": reason})
    existing.add((did, to))
    n[to]["parent_effects"][did] = cpt
    added += 1

# Rank 4 fixes
add("D151","acute_liver_failure","E02","劇症肝炎: 頻脈",{"under_100":0.20,"100_120":0.40,"over_120":0.40})
add("D151","acute_liver_failure","E03","劇症肝炎: 低血圧",{"normal_over_90":0.35,"hypotension_under_90":0.65})
add("D151","acute_liver_failure","E04","劇症肝炎: 頻呼吸",{"normal_under_20":0.25,"tachypnea_20_30":0.45,"severe_over_30":0.30})
add("D151","acute_liver_failure","L54","劇症肝炎: 低血糖",{"hypoglycemia":0.40,"normal":0.45,"hyperglycemia":0.12,"very_high_over_500":0.03})
add("D158","AIHA","E16","AIHA: 意識障害",{"normal":0.60,"confused":0.30,"obtunded":0.10})
add("D158","AIHA","S05","AIHA: 頭痛",{"absent":0.45,"mild":0.35,"severe":0.20})
add("D166","acetaminophen_OD","E38","APAP: 血圧",{"normal_under_140":0.60,"elevated_140_180":0.30,"crisis_over_180":0.10})
add("D149","CO_poisoning","S53","CO中毒: 構音障害",{"absent":0.55,"dysarthria":0.35,"aphasia":0.10})
add("D110","toxoplasmosis","E18","トキソプラズマ: 黄疸",{"absent":0.80,"present":0.20})

# Rank 5 fixes
add("D144","GBS","E16","GBS: 意識障害",{"normal":0.75,"confused":0.18,"obtunded":0.07})
add("D144","GBS","S05","GBS: 頭痛",{"absent":0.70,"mild":0.22,"severe":0.08})
add("D146","hypertensive_emergency","S42","高血圧緊急症: 痙攣",{"absent":0.80,"present":0.20})
add("D146","hypertensive_emergency","S52","高血圧緊急症: 局所神経脱落",{"absent":0.65,"unilateral_weakness":0.30,"bilateral":0.05})
add("D161","organophosphate","L11","有機リン: 肝酵素",{"normal":0.40,"mild_elevated":0.40,"very_high":0.20})
add("D161","organophosphate","S12","有機リン: 腹痛",{"absent":0.30,"epigastric":0.35,"RUQ":0.05,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.25})
add("D169","AIH","S13","AIH: 嘔気",{"absent":0.55,"present":0.45})
add("D175","AIP","S07","AIP: 倦怠感",{"absent":0.20,"mild":0.40,"severe":0.40})
add("D87","subacute_thyroiditis","S01","亜急性甲状腺炎: 咳嗽",{"absent":0.65,"dry":0.25,"productive":0.10})

# Rank 6-30 fixes
add("D170","alcoholic_hepatitis","E03","アルコール性肝炎: 低血圧",{"normal_over_90":0.50,"hypotension_under_90":0.50})
add("D170","alcoholic_hepatitis","L16","アルコール性肝炎: LDH",{"normal":0.25,"elevated":0.75})
add("D170","alcoholic_hepatitis","L55","アルコール性肝炎: AKI",{"normal":0.45,"mild_elevated":0.30,"high_AKI":0.25})
add("D169","AIH","S04","AIH: 呼吸困難",{"absent":0.75,"on_exertion":0.18,"at_rest":0.07})
add("D165","myasthenic_crisis","E05","MGクリーゼ: 低酸素",{"normal_over_96":0.10,"mild_hypoxia_93_96":0.30,"severe_hypoxia_under_93":0.60})
add("D165","myasthenic_crisis","E38","MGクリーゼ: 血圧",{"normal_under_140":0.50,"elevated_140_180":0.35,"crisis_over_180":0.15})
add("D163","wernicke","L17","ウェルニッケ: CK",{"normal":0.60,"elevated":0.30,"very_high":0.10})
add("D163","wernicke","L53","ウェルニッケ: トロポニン",{"not_done":0.20,"normal":0.55,"mildly_elevated":0.20,"very_high":0.05})
add("D172","gas_gangrene","S13","ガス壊疽: 嘔気",{"absent":0.55,"present":0.45})
add("D172","gas_gangrene","S14","ガス壊疽: 下痢",{"absent":0.65,"watery":0.30,"bloody":0.05})
add("D171","APS","L01","APS: WBC",{"low_under_4000":0.05,"normal_4000_10000":0.25,"high_10000_20000":0.40,"very_high_over_20000":0.30})
add("D171","APS","E38","APS: 高血圧",{"normal_under_140":0.35,"elevated_140_180":0.35,"crisis_over_180":0.30})
add("D171","APS","S13","APS: 嘔吐",{"absent":0.50,"present":0.50})

s2["total_edges"] = len(s2["edges"])
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "w", encoding="utf-8") as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "w", encoding="utf-8") as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print(f"Added {added} new edges. Total: {s2['total_edges']}")
