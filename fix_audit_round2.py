#!/usr/bin/env python3
"""Edge audit round 2: fix clinically justified missing edges."""
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

# === RANK 4-5 fixes (Top-3 targets) ===
add("D89","malignant_hyperthermia","L11","悪性高熱: 肝酵素(横紋筋融解/肝障害)",{"normal":0.20,"mild_elevated":0.40,"very_high":0.40})
add("D192","APL","S01","APL: 咳嗽(感染合併)",{"absent":0.55,"dry":0.30,"productive":0.15})
add("D194","lyme_disease","L11","ライム: 肝酵素上昇(ライム肝炎, 30-40%)",{"normal":0.50,"mild_elevated":0.30,"very_high":0.20})

# === RANK 2-3 fixes (Top-1 targets, clinically justified only) ===
# D91 chikungunya → E03 hypotension
add("D91","chikungunya","E03","チクングニア: 低血圧(重症, 10-20%)",{"normal_over_90":0.75,"hypotension_under_90":0.25})

# D57 NF → S14 diarrhea (GI involvement/toxin)
add("D57","NF","S14","壊死性筋膜炎: 下痢(毒素/敗血症, 15-20%)",{"absent":0.75,"watery":0.20,"bloody":0.05})

# D78 cellulitis → E04, T02
add("D78","cellulitis","E04","蜂窩織炎: 頻呼吸(重症/敗血症)",{"normal_under_20":0.50,"tachypnea_20_30":0.35,"severe_over_30":0.15})

# D75 DVT/PE → E04, E05, L52
add("D75","DVT_PE","E04","PE: 頻呼吸(60-80%)",{"normal_under_20":0.15,"tachypnea_20_30":0.45,"severe_over_30":0.40})
add("D75","DVT_PE","E05","PE: 低酸素(60-70%)",{"normal_over_96":0.20,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.45})
add("D75","DVT_PE","L52","PE: D-dimer著高(95%+)",{"not_done":0.05,"normal":0.03,"mildly_elevated":0.07,"very_high":0.85})

# D64 reactive arthritis → S27, S43
add("D64","reactive_arthritis","S27","反応性関節炎: 朝のこわばり(50-60%)",{"absent":0.30,"under_30min":0.30,"over_30min":0.40})
add("D64","reactive_arthritis","S43","反応性関節炎: 手掌足底皮疹(keratoderma, 15-20%)",{"absent":0.75,"present":0.25})

# D82 hospital meningitis → E12, S09
add("D82","hospital_meningitis","E12","院内髄膜炎: 皮膚(創部発赤/感染)",{"normal":0.50,"localized_erythema_warmth_swelling":0.40,"petechiae_purpura":0.02,"maculopapular_rash":0.01,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.02,"vesicle_bulla":0.01,"skin_necrosis":0.02})
add("D82","hospital_meningitis","S09","院内髄膜炎: 悪寒戦慄(菌血症)",{"absent":0.30,"present":0.70})

# D107 HLH → S04, S06
add("D107","HLH","S04","HLH: 呼吸困難(肺浸潤/胸水, 20-30%)",{"absent":0.60,"on_exertion":0.25,"at_rest":0.15})
add("D107","HLH","S06","HLH: 筋肉痛(20-30%)",{"absent":0.65,"present":0.35})

# D114 histoplasmosis → E12, L15, S01
add("D114","histoplasmosis","E12","ヒストプラズマ: 皮疹(播種性, 30-40%)",{"normal":0.55,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.03,"maculopapular_rash":0.25,"vesicular_dermatomal":0.02,"diffuse_erythroderma":0.02,"purpura":0.05,"vesicle_bulla":0.02,"skin_necrosis":0.04})
add("D114","histoplasmosis","L15","ヒストプラズマ: フェリチン上昇(播種性)",{"normal":0.30,"mild_elevated":0.35,"very_high_over_1000":0.25,"extreme_over_10000":0.10})
add("D114","histoplasmosis","S01","ヒストプラズマ: 咳嗽(肺型, 60-70%)",{"absent":0.25,"dry":0.45,"productive":0.30})

# D124 COPD exac → L15 ferritin (inflammation)
add("D124","COPD_exacerbation","L15","COPD増悪: フェリチン(炎症性上昇)",{"normal":0.35,"mild_elevated":0.35,"very_high_over_1000":0.25,"extreme_over_10000":0.05})

# D135 tension pneumothorax → S04, S05
add("D135","tension_pneumothorax","S04","緊張性気胸: 呼吸困難(100%)",{"absent":0.02,"on_exertion":0.08,"at_rest":0.90})
add("D135","tension_pneumothorax","S05","緊張性気胸: 頭痛(低酸素, 20-30%)",{"absent":0.65,"mild":0.25,"severe":0.10})

# D136 peptic ulcer perforation → L03 PCT, S04
add("D136","peptic_ulcer_perf","L03","消化性潰瘍穿孔: PCT上昇(腹膜炎/敗血症)",{"not_done":0.15,"low_under_0.25":0.10,"gray_0.25_0.5":0.15,"high_over_0.5":0.60})
add("D136","peptic_ulcer_perf","S04","消化性潰瘍穿孔: 呼吸困難(腹痛→呼吸制限)",{"absent":0.45,"on_exertion":0.30,"at_rest":0.25})

# D152 DIC → S13, S14
add("D152","DIC","S13","DIC: 嘔気(基礎疾患/臓器不全, 40-50%)",{"absent":0.45,"present":0.55})
add("D152","DIC","S14","DIC: 下痢(基礎疾患, 20-30%)",{"absent":0.65,"watery":0.25,"bloody":0.10})

# D158 AIHA → S01 (cough from anemia/HF)
add("D158","AIHA","S01","AIHA: 咳嗽(重度貧血/うっ血, 15-20%)",{"absent":0.75,"dry":0.18,"productive":0.07})

# D160 tetanus → E38 hypertension (autonomic)
add("D160","tetanus","E38","破傷風: 高血圧(自律神経障害)",{"normal_under_140":0.25,"elevated_140_180":0.40,"crisis_over_180":0.35})

# D171 APS → S14 (GI thrombosis → diarrhea)
add("D171","APS","S14","APS: 下痢(腸管血栓, 20-30%)",{"absent":0.65,"watery":0.25,"bloody":0.10})

# D183 cryoglobulinemia → L11, L14, S12, S14
add("D183","cryoglobulinemia","L11","クリオグロブリン: 肝酵素(HCV肝炎合併)",{"normal":0.35,"mild_elevated":0.45,"very_high":0.20})
add("D183","cryoglobulinemia","L14","クリオグロブリン: 血小板減少(20-30%)",{"normal":0.55,"left_shift":0.05,"atypical_lymphocytes":0.02,"thrombocytopenia":0.30,"eosinophilia":0.01,"lymphocyte_predominant":0.07})
add("D183","cryoglobulinemia","S12","クリオグロブリン: 腹痛(腸管血管炎, 20-30%)",{"absent":0.60,"epigastric":0.10,"RUQ":0.05,"RLQ":0.03,"LLQ":0.03,"suprapubic":0.02,"diffuse":0.17})
add("D183","cryoglobulinemia","S14","クリオグロブリン: 下痢(腸管血管炎, 15-20%)",{"absent":0.75,"watery":0.20,"bloody":0.05})

# D192 APL → E05
add("D192","APL","E05","APL: 低酸素(肺出血/感染)",{"normal_over_96":0.40,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.25})

# D193 HP → L02 CRP
add("D193","hypersensitivity_pneumonitis","L02","過敏性肺炎: CRP上昇(急性型)",{"normal_under_0.3":0.08,"mild_0.3_3":0.12,"moderate_3_10":0.35,"high_over_10":0.45})

# D195 drug pneumonitis → L02 CRP
add("D195","drug_induced_pneumonitis","L02","薬剤性肺炎: CRP上昇",{"normal_under_0.3":0.10,"mild_0.3_3":0.15,"moderate_3_10":0.35,"high_over_10":0.40})

s2["total_edges"] = len(s2["edges"])
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "w", encoding="utf-8") as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "w", encoding="utf-8") as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']}")
