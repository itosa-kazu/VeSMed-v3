#!/usr/bin/env python3
"""Add D183 Pericardial Effusion (non-infectious) + D184 Kawasaki Disease (adult) + D185 Cryoglobulinemia."""
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
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt

# D183 クリオグロブリン血症
s1["variables"].append({"id":"D183","name":"cryoglobulinemia","name_ja":"クリオグロブリン血症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"寒冷沈降免疫グロブリン。三徴:紫斑+関節痛+脱力。HCV関連が最多。腎障害(MPGN)+末梢神経障害"})
for to,reason,cpt in [
    ("E12","クリオグロブリン: 紫斑(下肢, 80-90%)",{"normal":0.08,"localized_erythema_warmth_swelling":0.02,"petechiae_purpura":0.15,"maculopapular_rash":0.02,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.65,"vesicle_bulla":0.01,"skin_necrosis":0.05}),
    ("S08","クリオグロブリン: 関節痛(70-80%)",{"absent":0.15,"present":0.85}),
    ("S07","クリオグロブリン: 倦怠感(80-90%)",{"absent":0.08,"mild":0.32,"severe":0.60}),
    ("E01","クリオグロブリン: 発熱(20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("L55","クリオグロブリン: AKI(MPGN, 30-40%)",{"normal":0.50,"mild_elevated":0.30,"high_AKI":0.20}),
    ("L05","クリオグロブリン: 尿異常(蛋白尿/血尿, 40-50%)",{"normal":0.45,"pyuria_bacteriuria":0.55}),
    ("L02","クリオグロブリン: CRP上昇",{"normal_under_0.3":0.20,"mild_0.3_3":0.30,"moderate_3_10":0.30,"high_over_10":0.20}),
    ("T01","クリオグロブリン: 慢性~亜急性",{"under_3d":0.05,"3d_to_1w":0.15,"1w_to_3w":0.30,"over_3w":0.50}),
    ("T02","クリオグロブリン: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]:
    add("D183","cryoglobulinemia",to,reason,cpt)
s3["full_cpts"]["D183"] = {"parents":[],"description":"クリオグロブリン血症。HCV関連",
    "cpt":{"":0.001}}

# D184 強直性脊椎炎(AS)
s1["variables"].append({"id":"D184","name":"ankylosing_spondylitis","name_ja":"強直性脊椎炎",
    "category":"disease","states":["no","yes"],"severity":"moderate",
    "note":"HLA-B27関連。慢性腰背部痛(朝のこわばり>30分)+仙腸関節炎。若年男性に多い。ぶどう膜炎合併"})
for to,reason,cpt in [
    ("S15","AS: 腰背部痛(定義的, 90%+)",{"absent":0.03,"present":0.97}),
    ("S08","AS: 関節痛(末梢, 30-40%)",{"absent":0.50,"present":0.50}),
    ("S27","AS: 朝のこわばり(>30分, 80%+)",{"absent":0.10,"under_30min":0.10,"over_30min":0.80}),
    ("S07","AS: 倦怠感(60-70%)",{"absent":0.25,"mild":0.45,"severe":0.30}),
    ("E01","AS: 発熱(急性増悪時, 10-20%)",{"under_37.5":0.75,"37.5_38.0":0.12,"38.0_39.0":0.08,"39.0_40.0":0.04,"over_40.0":0.01}),
    ("L02","AS: CRP上昇(50-60%)",{"normal_under_0.3":0.25,"mild_0.3_3":0.30,"moderate_3_10":0.30,"high_over_10":0.15}),
    ("T01","AS: 慢性(>3ヶ月)",{"under_3d":0.02,"3d_to_1w":0.03,"1w_to_3w":0.10,"over_3w":0.85}),
    ("T02","AS: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]:
    add("D184","ankylosing_spondylitis",to,reason,cpt)
s3["full_cpts"]["D184"] = {"parents":["R01","R02"],"description":"AS。若年男性に多い",
    "cpt":{"18_39,male":0.003,"18_39,female":0.001,"40_64,male":0.002,"40_64,female":0.0005,"65_plus,male":0.001,"65_plus,female":0.0003}}

# D185 遺伝性血管性浮腫(HAE)
s1["variables"].append({"id":"D185","name":"hereditary_angioedema","name_ja":"遺伝性血管性浮腫(HAE)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"C1-INH欠損/機能不全。反復性の顔面/四肢/消化管浮腫。喉頭浮腫は窒息リスク。蕁麻疹なし(アレルギーとの鑑別点)"})
for to,reason,cpt in [
    ("S12","HAE: 腹痛(消化管浮腫, 90%+の発作で)",{"absent":0.08,"epigastric":0.15,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.02,"diffuse":0.60}),
    ("S13","HAE: 嘔吐(消化管浮腫, 70-80%)",{"absent":0.15,"present":0.85}),
    ("S04","HAE: 呼吸困難(喉頭浮腫, 30-50%)",{"absent":0.45,"on_exertion":0.20,"at_rest":0.35}),
    ("E36","HAE: 四肢浮腫(顔面/四肢, 80%+)",{"absent":0.10,"unilateral":0.40,"bilateral":0.50}),
    ("E01","HAE: 通常無熱",{"under_37.5":0.85,"37.5_38.0":0.08,"38.0_39.0":0.05,"39.0_40.0":0.02,"over_40.0":0.00}),
    ("L01","HAE: WBC(正常~軽度上昇)",{"low_under_4000":0.05,"normal_4000_10000":0.55,"high_10000_20000":0.30,"very_high_over_20000":0.10}),
    ("T01","HAE: 急性(発作は2-5日で自然軽快)",{"under_3d":0.60,"3d_to_1w":0.30,"1w_to_3w":0.08,"over_3w":0.02}),
    ("T02","HAE: 急性",{"sudden_hours":0.70,"gradual_days":0.30}),
]:
    add("D185","hereditary_angioedema",to,reason,cpt)
s3["full_cpts"]["D185"] = {"parents":[],"description":"HAE。C1-INH欠損",
    "cpt":{"":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"D183: 9e, D184: 8e, D185: 8e. Total: {s2['total_edges']} edges, 185 diseases")
