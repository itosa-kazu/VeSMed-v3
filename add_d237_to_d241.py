#!/usr/bin/env python3
"""Add D237-D241: 5 diseases."""
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
    if to not in n: return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt

# D237 腸重積症 (Intussusception, adult)
s1["variables"].append({"id":"D237","name":"intussusception","name_ja":"腸重積症(成人)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"成人は器質的先進部(腫瘍/ポリープ)が多い。間欠性腹痛+嘔吐+血便。小児のcurrant jelly stoolは稀"})
for to,r,c in [
    ("S12","腸重積: 腹痛(間欠性/疝痛様)",{"absent":0.03,"epigastric":0.05,"RUQ":0.10,"RLQ":0.15,"LLQ":0.05,"suprapubic":0.02,"diffuse":0.60}),
    ("S13","腸重積: 嘔吐(70-80%)",{"absent":0.15,"present":0.85}),
    ("S14","腸重積: 血便(30-40%)",{"absent":0.50,"watery":0.15,"bloody":0.35}),
    ("E09","腸重積: 腹部圧痛/腫瘤触知",{"soft_nontender":0.10,"localized_tenderness":0.55,"peritoneal_signs":0.35}),
    ("L01","腸重積: WBC上昇(腸管虚血時)",{"low_under_4000":0.03,"normal_4000_10000":0.30,"high_10000_20000":0.45,"very_high_over_20000":0.22}),
    ("T01","腸重積: 急性",{"under_3d":0.60,"3d_to_1w":0.25,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","腸重積: 急性",{"sudden_hours":0.55,"gradual_days":0.45}),
]: add("D237","intussusception",to,r,c)
s3["full_cpts"]["D237"] = {"parents":["R01"],"description":"成人腸重積","cpt":{"18_39":0.001,"40_64":0.001,"65_plus":0.002}}

# D238 大腸癌 (Colorectal Cancer)
s1["variables"].append({"id":"D238","name":"colorectal_cancer","name_ja":"大腸癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"血便+便通変化+体重減少+貧血。左側:狭窄症状、右側:貧血。閉塞/穿孔で緊急手術"})
for to,r,c in [
    ("S14","大腸癌: 血便(60-70%)",{"absent":0.20,"watery":0.10,"bloody":0.70}),
    ("S12","大腸癌: 腹痛(40-50%)",{"absent":0.40,"epigastric":0.03,"RUQ":0.03,"RLQ":0.20,"LLQ":0.20,"suprapubic":0.02,"diffuse":0.12}),
    ("S07","大腸癌: 倦怠感/体重減少(60-70%)",{"absent":0.20,"mild":0.35,"severe":0.45}),
    ("E01","大腸癌: 発熱(穿孔/感染時, 10-20%)",{"under_37.5":0.70,"37.5_38.0":0.12,"38.0_39.0":0.10,"39.0_40.0":0.06,"over_40.0":0.02}),
    ("L02","大腸癌: CRP上昇(腫瘍/閉塞)",{"normal_under_0.3":0.25,"mild_0.3_3":0.25,"moderate_3_10":0.30,"high_over_10":0.20}),
    ("T01","大腸癌: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","大腸癌: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D238","colorectal_cancer",to,r,c)
s3["full_cpts"]["D238"] = {"parents":["R01"],"description":"大腸癌","cpt":{"18_39":0.0005,"40_64":0.003,"65_plus":0.006}}

# D239 急性糸球体腎炎(IgA腎症急性増悪)
s1["variables"].append({"id":"D239","name":"IgA_nephropathy_flare","name_ja":"IgA腎症(急性増悪)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"IgA沈着性GN。URI後の肉眼的血尿(synpharyngitic hematuria)が特徴。慢性経過→CKD進行"})
for to,r,c in [
    ("L05","IgA腎症: 尿異常(血尿+蛋白尿, 100%)",{"normal":0.02,"pyuria_bacteriuria":0.98}),
    ("L55","IgA腎症: AKI(急性増悪時, 30-50%)",{"normal":0.35,"mild_elevated":0.35,"high_AKI":0.30}),
    ("S02","IgA腎症: 咽頭痛(先行URI, 50-60%)",{"absent":0.35,"present":0.65}),
    ("E01","IgA腎症: 発熱(先行URI, 30-40%)",{"under_37.5":0.50,"37.5_38.0":0.18,"38.0_39.0":0.18,"39.0_40.0":0.10,"over_40.0":0.04}),
    ("S15","IgA腎症: 腰背部痛(腎腫大, 20-30%)",{"absent":0.65,"present":0.35}),
    ("E38","IgA腎症: 高血圧(30-40%)",{"normal_under_140":0.50,"elevated_140_180":0.35,"crisis_over_180":0.15}),
    ("T01","IgA腎症: 急性~亜急性",{"under_3d":0.25,"3d_to_1w":0.35,"1w_to_3w":0.25,"over_3w":0.15}),
    ("T02","IgA腎症: 亜急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D239","IgA_nephropathy_flare",to,r,c)
s3["full_cpts"]["D239"] = {"parents":["R01"],"description":"IgA腎症","cpt":{"18_39":0.002,"40_64":0.001,"65_plus":0.001}}

# D240 膜性腎症 (Membranous Nephropathy) → 慢性で急性診断に不向き。代わりに：
# D240 急性間質性腎炎 (Acute Interstitial Nephritis)
s1["variables"].append({"id":"D240","name":"acute_interstitial_nephritis","name_ja":"急性間質性腎炎(AIN)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"薬剤性(70%+)/感染性/自己免疫性。三徴:発熱+皮疹+AKI(+好酸球増多)。NSAIDs/抗菌薬が原因薬"})
for to,r,c in [
    ("L55","AIN: AKI(定義的)",{"normal":0.05,"mild_elevated":0.30,"high_AKI":0.65}),
    ("E01","AIN: 発熱(50-60%)",{"under_37.5":0.30,"37.5_38.0":0.18,"38.0_39.0":0.25,"39.0_40.0":0.20,"over_40.0":0.07}),
    ("E12","AIN: 皮疹(薬疹, 25-35%)",{"normal":0.60,"localized_erythema_warmth_swelling":0.03,"petechiae_purpura":0.02,"maculopapular_rash":0.28,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.02,"purpura":0.01,"vesicle_bulla":0.01,"skin_necrosis":0.02}),
    ("L14","AIN: 好酸球増多(30-40%)",{"normal":0.50,"left_shift":0.02,"atypical_lymphocytes":0.02,"thrombocytopenia":0.01,"eosinophilia":0.40,"lymphocyte_predominant":0.05}),
    ("L05","AIN: 尿異常(白血球円柱/好酸球尿, 80%+)",{"normal":0.10,"pyuria_bacteriuria":0.90}),
    ("S08","AIN: 関節痛(薬剤アレルギー, 15-20%)",{"absent":0.75,"present":0.25}),
    ("T01","AIN: 亜急性(投薬1-3週後)",{"under_3d":0.10,"3d_to_1w":0.25,"1w_to_3w":0.45,"over_3w":0.20}),
    ("T02","AIN: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D240","acute_interstitial_nephritis",to,r,c)
s3["full_cpts"]["D240"] = {"parents":[],"description":"AIN. 薬剤性","cpt":{"":0.002}}

# D241 腎血管性高血圧 (Renovascular Hypertension)
s1["variables"].append({"id":"D241","name":"renovascular_hypertension","name_ja":"腎血管性高血圧",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"腎動脈狭窄→RAAS活性化→高血圧。動脈硬化性(高齢)/線維筋性異形成(若年女性)。治療抵抗性高血圧"})
for to,r,c in [
    ("E38","腎血管性高血圧: 高血圧(定義的, 重症)",{"normal_under_140":0.05,"elevated_140_180":0.30,"crisis_over_180":0.65}),
    ("S05","腎血管性高血圧: 頭痛(高血圧, 50-60%)",{"absent":0.30,"mild":0.35,"severe":0.35}),
    ("L55","腎血管性高血圧: AKI(ACEi開始後/両側狭窄, 20-30%)",{"normal":0.55,"mild_elevated":0.30,"high_AKI":0.15}),
    ("S04","腎血管性高血圧: 呼吸困難(flash pulmonary edema, 20-30%)",{"absent":0.60,"on_exertion":0.25,"at_rest":0.15}),
    ("T01","腎血管性高血圧: 慢性",{"under_3d":0.10,"3d_to_1w":0.15,"1w_to_3w":0.25,"over_3w":0.50}),
    ("T02","腎血管性高血圧: 慢性~急性増悪",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D241","renovascular_hypertension",to,r,c)
s3["full_cpts"]["D241"] = {"parents":["R01","R02"],"description":"腎血管性高血圧",
    "cpt":{"18_39,male":0.0005,"18_39,female":0.001,"40_64,male":0.001,"40_64,female":0.001,"65_plus,male":0.003,"65_plus,female":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 241 diseases")
