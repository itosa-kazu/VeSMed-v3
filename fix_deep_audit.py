#!/usr/bin/env python3
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

add("D195","drug_pneumonitis","E04","薬剤性肺炎: 頻呼吸",{"normal_under_20":0.10,"tachypnea_20_30":0.35,"severe_over_30":0.55})
add("D195","drug_pneumonitis","L55","薬剤性肺炎: AKI",{"normal":0.50,"mild_elevated":0.25,"high_AKI":0.25})
add("D207","HIT","S12","HIT: 腹痛",{"absent":0.45,"epigastric":0.05,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.02,"diffuse":0.33})
add("D207","HIT","E01","HIT: 発熱",{"under_37.5":0.40,"37.5_38.0":0.15,"38.0_39.0":0.25,"39.0_40.0":0.15,"over_40.0":0.05})
add("D207","HIT","E03","HIT: 低血圧",{"normal_over_90":0.45,"hypotension_under_90":0.55})
add("D207","HIT","L53","HIT: トロポニン",{"not_done":0.15,"normal":0.35,"mildly_elevated":0.35,"very_high":0.15})
add("D146","hypertensive_emergency","S12","高血圧緊急症: 腹痛",{"absent":0.55,"epigastric":0.10,"RUQ":0.05,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.25})
add("D250","PBC","L14","PBC: 汎血球減少",{"normal":0.40,"left_shift":0.05,"atypical_lymphocytes":0.02,"thrombocytopenia":0.45,"eosinophilia":0.01,"lymphocyte_predominant":0.07})
add("D250","PBC","L01","PBC: WBC低下",{"low_under_4000":0.40,"normal_4000_10000":0.40,"high_10000_20000":0.15,"very_high_over_20000":0.05})
add("D234","CML","S08","CML: 関節痛",{"absent":0.60,"present":0.40})
add("D234","CML","E18","CML: 黄疸",{"absent":0.65,"present":0.35})
add("D234","CML","E12","CML: 皮疹",{"normal":0.55,"localized_erythema_warmth_swelling":0.05,"petechiae_purpura":0.05,"maculopapular_rash":0.10,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.02,"purpura":0.05,"vesicle_bulla":0.12,"skin_necrosis":0.05})
add("D234","CML","E36","CML: 浮腫",{"absent":0.55,"unilateral":0.10,"bilateral":0.35})
add("D199","rabies","S13","狂犬病: 嘔吐",{"absent":0.35,"present":0.65})
add("D209","myelofibrosis","L14","骨髄線維症: 血小板減少",{"normal":0.15,"left_shift":0.10,"atypical_lymphocytes":0.03,"thrombocytopenia":0.60,"eosinophilia":0.02,"lymphocyte_predominant":0.10})
add("D209","myelofibrosis","S15","骨髄線維症: 背部痛",{"absent":0.55,"present":0.45})
add("D209","myelofibrosis","S14","骨髄線維症: 下痢",{"absent":0.65,"watery":0.30,"bloody":0.05})
add("D246","EHEC","E03","EHEC: 低血圧",{"normal_over_90":0.50,"hypotension_under_90":0.50})
add("D246","EHEC","L14","EHEC: 血小板減少",{"normal":0.55,"left_shift":0.05,"atypical_lymphocytes":0.00,"thrombocytopenia":0.35,"eosinophilia":0.00,"lymphocyte_predominant":0.05})
add("D246","EHEC","E16","EHEC: 意識障害",{"normal":0.60,"confused":0.25,"obtunded":0.15})
add("D246","EHEC","S42","EHEC: 痙攣",{"absent":0.75,"present":0.25})
add("D203","systemic_sclerosis","E36","強皮症: 浮腫",{"absent":0.25,"unilateral":0.10,"bilateral":0.65})
add("D232","AKA","L54","AKA: 低血糖",{"hypoglycemia":0.40,"normal":0.40,"hyperglycemia":0.15,"very_high_over_500":0.05})
add("D232","AKA","L11","AKA: 肝酵素",{"normal":0.25,"mild_elevated":0.50,"very_high":0.25})
add("D232","AKA","L01","AKA: WBC",{"low_under_4000":0.05,"normal_4000_10000":0.20,"high_10000_20000":0.45,"very_high_over_20000":0.30})
add("D232","AKA","L17","AKA: CK",{"normal":0.35,"elevated":0.35,"very_high":0.30})
add("D232","AKA","E01","AKA: 体温",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02})
add("D232","AKA","L55","AKA: AKI",{"normal":0.30,"mild_elevated":0.35,"high_AKI":0.35})
add("D202","sjogren","L28","シェーグレン: ESR",{"normal":0.15,"elevated":0.85})
add("D202","sjogren","E02","シェーグレン: 頻脈",{"under_100":0.40,"100_120":0.40,"over_120":0.20})
add("D205","EG","L44","EG: 電解質",{"normal":0.25,"hyponatremia":0.05,"hyperkalemia":0.10,"other":0.60})
add("D205","EG","E03","EG: 低血圧",{"normal_over_90":0.35,"hypotension_under_90":0.65})
add("D197","agranulocytosis","S12","無顆粒球症: 腹痛",{"absent":0.40,"epigastric":0.05,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.02,"diffuse":0.38})
add("D249","chronic_pancreatitis","L02","慢性膵炎: CRP",{"normal_under_0.3":0.15,"mild_0.3_3":0.20,"moderate_3_10":0.35,"high_over_10":0.30})
add("D249","chronic_pancreatitis","L01","慢性膵炎: WBC",{"low_under_4000":0.03,"normal_4000_10000":0.25,"high_10000_20000":0.45,"very_high_over_20000":0.27})
add("D249","chronic_pancreatitis","S04","慢性膵炎: 呼吸困難",{"absent":0.55,"on_exertion":0.25,"at_rest":0.20})
add("D138","acute_stroke","L51","脳梗塞: BNP",{"not_done":0.15,"normal":0.25,"mildly_elevated":0.35,"very_high":0.25})
add("D20","sinusitis","E16","副鼻腔炎: 意識障害",{"normal":0.80,"confused":0.15,"obtunded":0.05})
add("D208","ITP","L53","ITP: トロポニン",{"not_done":0.20,"normal":0.50,"mildly_elevated":0.25,"very_high":0.05})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']}")
