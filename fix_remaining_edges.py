#!/usr/bin/env python3
"""Fix clinically justified missing edges from systematic audit."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]
existing = {(e["from"],e["to"]) for e in s2["edges"]}
added = 0
skipped = []
def add(did, dname, to, reason, cpt):
    global added
    if (did,to) in existing: return
    if to not in n:
        skipped.append(f"{did}→{to}: no leak")
        return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt
    added += 1

# ===== Clinically justified additions (sorted by disease) =====

# D05 pneumonia → L17 CK (rhabdomyolysis complication with pneumonia is known)
add("D05","pneumonia","L17","肺炎: CK上昇(横紋筋融解合併, Legionellaで特に)",{"normal":0.60,"elevated":0.30,"very_high":0.10})

# D11 pericarditis → E02 tachycardia (common with pericarditis)
add("D11","pericarditis","E02","心膜炎: 頻脈(50-70%)",{"under_100":0.25,"100_120":0.45,"over_120":0.30})

# D28 typhoid → E16, S09
add("D28","typhoid","E16","腸チフス: 意識障害(typhoid encephalopathy, 10-20%)",{"normal":0.70,"confused":0.22,"obtunded":0.08})
add("D28","typhoid","S09","腸チフス: 悪寒戦慄(50-60%)",{"absent":0.35,"present":0.65})

# D29 liver abscess → L03 PCT, L52 D-dimer, S05 headache
add("D29","liver_abscess","L03","肝膿瘍: PCT上昇(細菌性)",{"not_done":0.15,"low_under_0.25":0.05,"gray_0.25_0.5":0.10,"high_over_0.5":0.70})
add("D29","liver_abscess","S05","肝膿瘍: 頭痛(20-30%)",{"absent":0.65,"mild":0.25,"severe":0.10})

# D37 campylobacter → S15 flank pain (uncommon but possible)
add("D37","campylobacter","S15","カンピロ腸炎: 側腹部痛(まれ, 10-15%)",{"absent":0.80,"present":0.20})

# D57 NF → L11, S13, S14
add("D57","NF","L11","壊死性筋膜炎: 肝酵素上昇(敗血症/MOF)",{"normal":0.35,"mild_elevated":0.40,"very_high":0.25})
add("D57","NF","S13","壊死性筋膜炎: 嘔気(毒素/敗血症, 40-50%)",{"absent":0.45,"present":0.55})

# D58 Still → L16 LDH (elevated in active Still's, 60-70%)
add("D58","Still","L16","Still病: LDH上昇(活動期, 60-70%)",{"normal":0.25,"elevated":0.75})

# D67 lymphoma → E03 hypotension (advanced/B symptoms)
add("D67","lymphoma","E03","悪性リンパ腫: 低血圧(進行期/SVC症候群)",{"normal_over_90":0.70,"hypotension_under_90":0.30})

# D96 Kikuchi → S01 cough (URI-like prodrome, 15-20%)
add("D96","Kikuchi","S01","菊池病: 咳嗽(URI様前駆, 15-20%)",{"absent":0.75,"dry":0.18,"productive":0.07})

# D107 HLH → S12 abdominal pain (hepatosplenomegaly, 30-40%)
add("D107","HLH","S12","HLH: 腹痛(肝脾腫, 30-40%)",{"absent":0.50,"epigastric":0.05,"RUQ":0.15,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.25})

# D130 ILD → L15 ferritin (elevated in ILD, especially IPF)
add("D130","ILD","L15","ILD: フェリチン上昇(肺線維化/炎症)",{"normal":0.30,"mild_elevated":0.35,"very_high_over_1000":0.30,"extreme_over_10000":0.05})

# D142 seizure → L44, S52, S04, S05
add("D142","seizure","L44","てんかん: 電解質異常(誘因/結果)",{"normal":0.50,"hyponatremia":0.35,"hyperkalemia":0.10,"other":0.05})
add("D142","seizure","S52","てんかん: 局所神経脱落(Todd麻痺, 20-30%)",{"absent":0.65,"unilateral_weakness":0.30,"bilateral":0.05})
add("D142","seizure","S04","てんかん: 呼吸困難(SE後)",{"absent":0.60,"on_exertion":0.25,"at_rest":0.15})
add("D142","seizure","S05","てんかん: 頭痛(発作後, 40-50%)",{"absent":0.40,"mild":0.35,"severe":0.25})

# D145 testicular torsion → S12 (referred pain to lower abdomen)
add("D145","testicular_torsion","S12","精巣捻転: 腹痛(関連痛/下腹部, 30-40%)",{"absent":0.50,"epigastric":0.02,"RUQ":0.02,"RLQ":0.15,"LLQ":0.15,"suprapubic":0.10,"diffuse":0.06})

# D146 hypertensive emergency → L02 CRP, S12
add("D146","hypertensive_emergency","L02","高血圧緊急症: CRP上昇(臓器障害)",{"normal_under_0.3":0.30,"mild_0.3_3":0.25,"moderate_3_10":0.25,"high_over_10":0.20})

# D149 CO → S12 abdominal pain (GI symptoms 30-40%)
add("D149","CO_poisoning","S12","CO中毒: 腹痛(30-40%)",{"absent":0.50,"epigastric":0.15,"RUQ":0.05,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.25})
add("D149","CO_poisoning","S04","CO中毒: 呼吸困難(低酸素)",{"absent":0.25,"on_exertion":0.30,"at_rest":0.45})

# D153 rhabdomyolysis → S02 sore throat (URI trigger)
add("D153","rhabdomyolysis","S02","横紋筋融解: 咽頭痛(感染誘因, 20-30%)",{"absent":0.70,"present":0.30})

# D158 AIHA → S13 nausea
add("D158","AIHA","S13","AIHA: 嘔気(30-40%)",{"absent":0.55,"present":0.45})

# D161 OP → L01 WBC (already checked - may exist)
add("D161","organophosphate","L01","有機リン: WBC(ストレス応答)",{"low_under_4000":0.05,"normal_4000_10000":0.20,"high_10000_20000":0.40,"very_high_over_20000":0.35})

# D162 HUS → E12, L52
add("D162","HUS","E12","HUS: 皮膚(点状出血/紫斑, 30-40%)",{"normal":0.55,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.25,"maculopapular_rash":0.01,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.10,"vesicle_bulla":0.02,"skin_necrosis":0.03})
add("D162","HUS","L52","HUS: D-dimer上昇(TMA/DIC様)",{"not_done":0.15,"normal":0.10,"mildly_elevated":0.25,"very_high":0.50})

# D164 cSDH → E38, S13, E02
add("D164","chronic_SDH","E38","慢性SDH: 高血圧(頭蓋内圧亢進, 30-40%)",{"normal_under_140":0.50,"elevated_140_180":0.35,"crisis_over_180":0.15})
add("D164","chronic_SDH","S13","慢性SDH: 嘔吐(頭蓋内圧亢進, 40-50%)",{"absent":0.45,"present":0.55})
add("D164","chronic_SDH","E02","慢性SDH: 頻脈(Cushing response後期, 20-30%)",{"under_100":0.55,"100_120":0.30,"over_120":0.15})

# D168 RPGN → E02, E36, E38
add("D168","RPGN","E02","RPGN: 頻脈(炎症/貧血)",{"under_100":0.30,"100_120":0.45,"over_120":0.25})
add("D168","RPGN","E36","RPGN: 浮腫(体液過剰/AKI)",{"absent":0.25,"unilateral":0.05,"bilateral":0.70})
add("D168","RPGN","E38","RPGN: 高血圧(腎性, 50-60%)",{"normal_under_140":0.30,"elevated_140_180":0.40,"crisis_over_180":0.30})

# D170 alcoholic hepatitis → S44 (coagulopathy/bleeding)
add("D170","alcoholic_hepatitis","S44","アルコール性肝炎: 出血傾向(凝固障害, 30-40%)",{"absent":0.55,"present":0.45})

# D175 AIP → L02, S08
add("D175","AIP","L02","AIP: CRP上昇(炎症反応)",{"normal_under_0.3":0.08,"mild_0.3_3":0.15,"moderate_3_10":0.35,"high_over_10":0.42})

# D177 ischemic colitis → E03, L52, L55
add("D177","ischemic_colitis","E03","虚血性腸炎: 低血圧(ショック型)",{"normal_over_90":0.45,"hypotension_under_90":0.55})
add("D177","ischemic_colitis","L52","虚血性腸炎: D-dimer上昇(血栓/虚血)",{"not_done":0.15,"normal":0.15,"mildly_elevated":0.30,"very_high":0.40})
add("D177","ischemic_colitis","L55","虚血性腸炎: AKI(脱水/ショック)",{"normal":0.45,"mild_elevated":0.35,"high_AKI":0.20})

# D178 Listeria → E38, L11, L52
add("D178","listeria_meningitis","E38","リステリア: 高血圧(髄膜炎性, 30-40%)",{"normal_under_140":0.45,"elevated_140_180":0.35,"crisis_over_180":0.20})
add("D178","listeria_meningitis","L11","リステリア: 肝酵素(敗血症性, 20-30%)",{"normal":0.55,"mild_elevated":0.30,"very_high":0.15})

# D185 HAE → S14 (GI edema → diarrhea), L52
add("D185","hereditary_angioedema","S14","HAE: 下痢(消化管浮腫, 40-50%)",{"absent":0.45,"watery":0.50,"bloody":0.05})
add("D185","hereditary_angioedema","L52","HAE: D-dimer上昇(発作時, 報告あり)",{"not_done":0.20,"normal":0.25,"mildly_elevated":0.30,"very_high":0.25})

s2["total_edges"] = len(s2["edges"])
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "w", encoding="utf-8") as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "w", encoding="utf-8") as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Skipped: {len(skipped)}. Total: {s2['total_edges']}")
if skipped:
    for s in skipped:
        print(f"  SKIP: {s}")
