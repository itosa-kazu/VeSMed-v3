#!/usr/bin/env python3
"""D276 卵巣捻転: 全172変量に臨床CPTを設定（稠密化）"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)
n = s3["noisy_or_params"]
existing = {(e["from"],e["to"]) for e in s2["edges"]}
added = 0
did = "D276"

def add(to, cpt, reason=""):
    global added
    if (did,to) in existing: return
    if to not in n: return
    s2["edges"].append({"from":did,"to":to,"from_name":"ovarian_torsion","to_name":to,
        "reason":f"D276 dense: {reason}"})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt
    added += 1

# ============================================================
# 卵巣捻転の臨床像:
# - 若年女性、突然の片側下腹部激痛+嘔気嘔吐
# - 無熱~微熱、WBC軽度上昇、CRP軽度上昇
# - 心肺/神経/関節/皮膚 → 全て正常
# - 腹部: 片側圧痛、Murphy陰性、CVA叩打痛なし
# ============================================================

# --- 陰性辺（この疾患で特に正常になる所見）---
# leak値と有意に異なる(差>0.05)もののみ

# 症状系: 卵巣捻転では起きない症状
add("S01", {"absent":0.97,"dry":0.02,"productive":0.01}, "咳嗽なし")
add("S02", {"absent":0.98,"present":0.02}, "咽頭痛なし")
add("S03", {"absent":0.98,"clear_rhinorrhea":0.01,"purulent_rhinorrhea":0.01}, "鼻汁なし")
add("S04", {"absent":0.95,"on_exertion":0.04,"at_rest":0.01}, "呼吸困難なし")
add("S05", {"absent":0.90,"mild":0.08,"severe":0.02}, "頭痛なし")
add("S06", {"absent":0.95,"present":0.05}, "筋肉痛なし")
add("S07", {"absent":0.60,"mild":0.30,"severe":0.10}, "倦怠軽度(痛みで)")
add("S08", {"absent":0.97,"present":0.03}, "関節痛なし")
add("S09", {"absent":0.85,"present":0.15}, "悪寒(感染合併時)")
add("S10", {"absent":0.95,"present":0.05}, "排尿痛なし")
add("S11", {"absent":0.90,"present":0.10}, "頻尿(骨盤圧迫で軽度)")
add("S14", {"absent":0.85,"watery":0.12,"bloody":0.03}, "下痢(腸管刺激で軽度)")
add("S15", {"absent":0.30,"present":0.70}, "側腹部痛あり(70%)")
add("S16", {"absent":0.95,"present":0.05}, "盗汗なし")
add("S17", {"absent":0.95,"present":0.05}, "体重減少なし")
add("S18", {"absent":0.98,"localized_pain_redness":0.01,"rash_widespread":0.01}, "皮膚訴えなし")
add("S21", {"absent":0.95,"burning":0.01,"sharp":0.02,"pressure":0.01,"tearing":0.01}, "胸痛なし")
add("S22", {"absent":0.90,"present":0.10}, "背部痛(放散で軽度)")
add("S44", {"absent":0.95,"present":0.05}, "出血なし")
add("S46", {"absent":0.50,"present":0.50}, "食欲不振(痛み/嘔気で)")

# 身体所見系: 卵巣捻転で正常な所見
add("E03", {"normal_over_90":0.90,"hypotension_under_90":0.10}, "血圧正常(ショックは稀)")
add("E04", {"normal_under_20":0.80,"tachypnea_20_30":0.15,"severe_over_30":0.05}, "呼吸数正常")
add("E05", {"normal_over_96":0.95,"mild_hypoxia_93_96":0.04,"severe_hypoxia_under_93":0.01}, "SpO2正常")
add("E06", {"absent":0.99,"present":0.01}, "項部硬直なし")
add("E07", {"clear":0.90,"crackles":0.05,"wheezes":0.03,"decreased_absent":0.02}, "肺清明")
add("E08", {"normal":0.95,"erythema":0.04,"exudate_or_white_patch":0.01}, "咽頭正常")
add("E10", {"negative":0.95,"positive":0.05}, "Murphy陰性")
add("E11", {"absent":0.95,"present":0.05}, "CVA叩打痛なし")
add("E12", {"normal":0.95,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.01,"maculopapular_rash":0.01,"vesicular_dermatomal":0.00,"diffuse_erythroderma":0.00,"purpura":0.00,"vesicle_bulla":0.01,"skin_necrosis":0.00}, "皮膚正常")
add("E13", {"absent":0.97,"cervical":0.02,"generalized":0.01}, "リンパ節なし")
add("E14", {"absent":0.97,"present":0.03}, "脾腫なし")
add("E15", {"absent":0.98,"pre_existing":0.01,"new":0.01}, "心雑音なし")
add("E16", {"normal":0.85,"confused":0.12,"obtunded":0.03}, "意識正常(痛みで軽度)")
add("E18", {"absent":0.98,"present":0.02}, "黄疸なし")
add("E38", {"normal_under_140":0.85,"elevated_140_180":0.12,"crisis_over_180":0.03}, "血圧正常")
add("E36", {"absent":0.97,"unilateral":0.02,"bilateral":0.01}, "下腿浮腫なし")

# 検査系: 卵巣捻転で正常な検査
add("L03", {"not_done":0.40,"low_under_0.25":0.45,"gray_0.25_0.5":0.10,"high_over_0.5":0.05}, "PCT低値")
add("L04", {"normal":0.90,"lobar_infiltrate":0.03,"bilateral_infiltrate":0.02,"BHL":0.01,"pleural_effusion":0.02,"pneumothorax":0.02}, "CXR正常")
add("L05", {"normal":0.85,"pyuria_bacteriuria":0.15}, "尿検(軽度異常あり)")
add("L09", {"not_done_or_pending":0.50,"negative":0.45,"gram_positive":0.03,"gram_negative":0.02}, "血培陰性")
add("L14", {"normal":0.60,"left_shift":0.25,"atypical_lymphocytes":0.02,"thrombocytopenia":0.05,"eosinophilia":0.02,"lymphocyte_predominant":0.06}, "末梢血(左方移動あり)")
add("L16", {"normal":0.75,"elevated":0.25}, "LDH(壊死で上昇あり)")
add("L28", {"normal":0.50,"elevated":0.40,"very_high_over_100":0.10}, "ESR(炎症で上昇)")
add("L44", {"normal":0.85,"hyponatremia":0.05,"hyperkalemia":0.03,"other":0.07}, "電解質(脱水で変動)")
add("L55", {"normal":0.90,"mild_elevated":0.08,"high_AKI":0.02}, "Cr正常")
add("L31", {"normal":0.10,"abscess":0.05,"mass":0.15,"other_abnormal":0.70}, "腹部CT(卵巣腫瘤)")

# 特殊検査: not_doneが多い
add("L10", {"not_done":0.95,"negative":0.05,"positive":0.00}, "マラリア未検査")
add("L45", {"not_done":0.95,"normal":0.05,"viral_pattern":0.00,"bacterial_pattern":0.00,"HSV_PCR_positive":0.00,"tb_fungal_pattern":0.00}, "髄液未検査")
add("L46", {"normal":0.95,"temporal_lobe_lesion":0.01,"diffuse_abnormal":0.02,"other":0.02}, "頭部MRI正常")

# 中間変量
add("M02", {"stable":0.75,"compensated":0.20,"shock":0.05}, "血行動態(痛みで頻脈)")
add("L64", {"not_done":0.50,"normal":0.45,"pre_DIC":0.04,"overt_DIC":0.01}, "DICなし")
add("L65", {"not_assessed":0.40,"absent":0.55,"mild_NYHA2":0.04,"severe_NYHA3_4":0.01}, "心不全なし")
add("L66", {"not_assessed":0.40,"normal":0.55,"hepatocellular":0.03,"cholestatic":0.01,"congestive":0.01}, "肝障害なし")
add("L67", {"not_assessed":0.50,"no_AKI":0.45,"prerenal":0.04,"renal":0.01,"postrenal":0.00}, "AKIなし")

# 新変量系: 卵巣捻転で正常
add("S52", {"absent":0.98,"unilateral_weakness":0.01,"bilateral":0.01}, "局所神経なし")
add("S53", {"absent":0.99,"dysarthria":0.01,"aphasia":0.00}, "構音障害なし")
add("S54", {"absent":0.98,"hemianopia":0.01,"central_scotoma":0.00,"visual_loss":0.01}, "視野正常")
add("S55", {"absent":0.99,"present":0.01}, "嗄声なし")
add("S58", {"absent":0.99,"present":0.01}, "飛蚊症なし")
add("S59", {"absent":0.95,"positional_brief":0.02,"continuous_rotatory":0.01,"episodic_with_hearing":0.01,"non_rotatory_disequilibrium":0.01}, "めまいなし")
add("S60", {"absent":0.95,"bilateral_pressing":0.02,"unilateral_pulsating":0.01,"periorbital_stabbing":0.01,"thunderclap":0.00,"progressive_with_neuro":0.00,"electric_triggered":0.01}, "頭痛パターンなし")
add("S42", {"absent":0.98,"present":0.02}, "痙攣なし")

# 心臓系: 正常
add("E39", {"not_done":0.60,"normal":0.35,"wall_motion_abnormal":0.02,"valvular_abnormal":0.01,"pericardial_effusion":0.01,"LVH":0.01,"dilated_chamber":0.00}, "心エコー正常")
add("E40", {"not_done":0.60,"normal":0.35,"ST_elevation":0.01,"ST_depression":0.01,"AF":0.01,"QT_prolongation":0.01,"Brugada_pattern":0.00,"RVH_strain":0.00,"LVH_pattern":0.01}, "ECG正常")
add("E43", {"absent":0.98,"present":0.02}, "拡張期雑音なし")
add("L51", {"not_done":0.50,"normal":0.45,"mildly_elevated":0.04,"very_high":0.01}, "BNP正常")
add("L53", {"not_done":0.50,"normal":0.45,"mildly_elevated":0.04,"very_high":0.01}, "トロポニン正常")

# Save
s2["total_edges"] = len(s2["edges"])
for fn,d in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fn), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# Trinity
edges_set = {(e["from"],e["to"]) for e in s2["edges"]}
enc = sum(1 for e in s2["edges"] if e["to"] in n and isinstance(n[e["to"]],dict) and e["from"] not in n[e["to"]].get("parent_effects",{}))
cne = sum(1 for vid,p in n.items() if isinstance(p,dict) for did2 in p.get("parent_effects",{}) if (did2,vid) not in edges_set)
print(f"D276: Added {added} edges. Total {s2['total_edges']}")
print(f"Trinity: EDGE_NO_CPT={enc}, CPT_NO_EDGE={cne}")
