#!/usr/bin/env python3
"""Add D322-D326: 5 diseases."""
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

# D322 HELLP症候群
s1["variables"].append({"id":"D322","name":"HELLP","name_ja":"HELLP症候群",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"妊娠高血圧に伴う溶血+肝酵素上昇+血小板減少。妊娠後期～産褥。右上腹部痛+嘔気+倦怠感。緊急分娩"})
for to,r,c in [
    ("S15","HELLP: 右上腹部/心窩部痛(65-90%)",{"absent":0.10,"present":0.90}),
    ("S13","HELLP: 嘔気嘔吐(50-60%)",{"absent":0.30,"present":0.70}),
    ("E38","HELLP: 高血圧(80%+)",{"normal_under_140":0.10,"elevated_140_180":0.40,"crisis_over_180":0.50}),
    ("L11","HELLP: 肝酵素上昇(定義的)",{"normal":0.03,"mild_elevated":0.25,"very_high":0.72}),
    ("S44","HELLP: 出血傾向(血小板低下, 20-30%)",{"absent":0.65,"present":0.35}),
    ("S05","HELLP: 頭痛(50-60%)",{"absent":0.30,"mild":0.25,"severe":0.45}),
    ("S07","HELLP: 倦怠感(50-60%)",{"absent":0.25,"mild":0.30,"severe":0.45}),
    ("E16","HELLP: 意識障害(重症, 10-15%)",{"normal":0.70,"confused":0.20,"obtunded":0.10}),
    ("L56","HELLP: β-hCG陽性(妊娠中)",{"not_done":0.10,"negative":0.02,"positive":0.88}),
    ("T01","HELLP: 急性",{"under_3d":0.55,"3d_to_1w":0.30,"1w_to_3w":0.12,"over_3w":0.03}),
    ("T02","HELLP: 急性",{"sudden_hours":0.40,"gradual_days":0.60}),
]: add("D322","HELLP",to,r,c)
s3["full_cpts"]["D322"] = {"parents":["R01","R02"],"description":"HELLP症候群。妊娠後期女性",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0005,"18_39,male":0.0,"18_39,female":0.002,"40_64,male":0.0,"40_64,female":0.0005,"65_plus,male":0.0,"65_plus,female":0.0}}

# D323 常位胎盤早期剥離 (Placental Abruption)
s1["variables"].append({"id":"D323","name":"placental_abruption","name_ja":"常位胎盤早期剥離",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"正常位置の胎盤が分娩前に剥離。突然の腹痛+子宮圧痛+性器出血+DIC。胎児死亡リスク高い。緊急帝王切開"})
for to,r,c in [
    ("S15","胎盤早期剥離: 腹痛/腰背部痛(80%+)",{"absent":0.08,"present":0.92}),
    ("S44","胎盤早期剥離: 性器出血/出血傾向(70-80%)",{"absent":0.15,"present":0.85}),
    ("E02","胎盤早期剥離: 頻脈(出血性ショック, 40-50%)",{"under_100":0.30,"100_120":0.35,"over_120":0.35}),
    ("E38","胎盤早期剥離: 高血圧(妊娠高血圧合併, 50%)",{"normal_under_140":0.35,"elevated_140_180":0.35,"crisis_over_180":0.30}),
    ("S13","胎盤早期剥離: 嘔気嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("L56","胎盤早期剥離: β-hCG陽性(妊娠中)",{"not_done":0.10,"negative":0.02,"positive":0.88}),
    ("L52","胎盤早期剥離: D-dimer上昇(DIC, 60%+)",{"not_done":0.15,"normal":0.10,"mildly_elevated":0.30,"very_high":0.45}),
    ("T01","胎盤早期剥離: 超急性",{"under_3d":0.85,"3d_to_1w":0.12,"1w_to_3w":0.03,"over_3w":0.00}),
    ("T02","胎盤早期剥離: 突発",{"sudden_hours":0.85,"gradual_days":0.15}),
]: add("D323","placental_abruption",to,r,c)
s3["full_cpts"]["D323"] = {"parents":["R01","R02"],"description":"常位胎盤早期剥離。妊娠後期女性",
    "cpt":{"0_1,male":0.0,"0_1,female":0.0,"1_5,male":0.0,"1_5,female":0.0,"6_12,male":0.0,"6_12,female":0.0,"13_17,male":0.0,"13_17,female":0.0003,"18_39,male":0.0,"18_39,female":0.002,"40_64,male":0.0,"40_64,female":0.0005,"65_plus,male":0.0,"65_plus,female":0.0}}

# D324 結核性髄膜炎 (Tuberculous Meningitis)
s1["variables"].append({"id":"D324","name":"TB_meningitis","name_ja":"結核性髄膜炎",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"結核菌の髄膜浸潤。亜急性経過の頭痛+発熱+意識障害+脳神経麻痺。CSF:リンパ球優位+糖低下+蛋白上昇。死亡率高い"})
for to,r,c in [
    ("S05","結核性髄膜炎: 頭痛(90%+, 進行性)",{"absent":0.05,"mild":0.10,"severe":0.85}),
    ("E01","結核性髄膜炎: 発熱(80-90%)",{"under_37.5":0.08,"37.5_38.0":0.12,"38.0_39.0":0.35,"39.0_40.0":0.30,"over_40.0":0.15}),
    ("E06","結核性髄膜炎: 項部硬直(70-80%)",{"absent":0.15,"present":0.85}),
    ("E16","結核性髄膜炎: 意識障害(50-70%)",{"normal":0.20,"confused":0.40,"obtunded":0.40}),
    ("S13","結核性髄膜炎: 嘔吐(40-50%)",{"absent":0.45,"present":0.55}),
    ("S52","結核性髄膜炎: 脳神経麻痺/局所神経症状(20-30%)",{"absent":0.60,"unilateral_weakness":0.30,"bilateral":0.10}),
    ("S07","結核性髄膜炎: 倦怠感/体重減少(60-70%)",{"absent":0.15,"mild":0.30,"severe":0.55}),
    ("L01","結核性髄膜炎: WBC軽度上昇(50-60%)",{"low_under_4000":0.05,"normal_4000_10000":0.40,"high_10000_20000":0.40,"very_high_over_20000":0.15}),
    ("L02","結核性髄膜炎: CRP上昇(70-80%)",{"normal_under_0.3":0.08,"mild_0.3_3":0.15,"moderate_3_10":0.40,"high_over_10":0.37}),
    ("T01","結核性髄膜炎: 亜急性(1-3週)",{"under_3d":0.08,"3d_to_1w":0.15,"1w_to_3w":0.45,"over_3w":0.32}),
    ("T02","結核性髄膜炎: 亜急性",{"sudden_hours":0.10,"gradual_days":0.90}),
]: add("D324","TB_meningitis",to,r,c)
s3["full_cpts"]["D324"] = {"parents":["R01"],"description":"結核性髄膜炎",
    "cpt":{"0_1":0.0005,"1_5":0.0005,"6_12":0.0003,"13_17":0.0005,"18_39":0.001,"40_64":0.001,"65_plus":0.002}}

# D325 可逆性後頭葉白質脳症(PRES)
s1["variables"].append({"id":"D325","name":"PRES","name_ja":"可逆性後頭葉白質脳症(PRES)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"高血圧/免疫抑制薬/子癇→後頭葉血管性浮腫。痙攣+頭痛+視力障害+意識障害。MRI: 後頭葉~頭頂葉白質浮腫"})
for to,r,c in [
    ("S42","PRES: 痙攣(60-75%)",{"absent":0.20,"present":0.80}),
    ("S05","PRES: 頭痛(50-60%)",{"absent":0.25,"mild":0.15,"severe":0.60}),
    ("E16","PRES: 意識障害(50-60%)",{"normal":0.25,"confused":0.40,"obtunded":0.35}),
    ("E38","PRES: 高血圧(70-80%)",{"normal_under_140":0.10,"elevated_140_180":0.30,"crisis_over_180":0.60}),
    ("S13","PRES: 嘔吐(30-40%)",{"absent":0.55,"present":0.45}),
    ("S52","PRES: 局所神経症状(視力障害含む, 30-40%)",{"absent":0.50,"unilateral_weakness":0.35,"bilateral":0.15}),
    ("L55","PRES: 腎機能障害(30-40%)",{"normal":0.45,"mild_elevated":0.30,"high_AKI":0.25}),
    ("T01","PRES: 急性~亜急性",{"under_3d":0.50,"3d_to_1w":0.30,"1w_to_3w":0.15,"over_3w":0.05}),
    ("T02","PRES: 急性",{"sudden_hours":0.45,"gradual_days":0.55}),
]: add("D325","PRES",to,r,c)
s3["full_cpts"]["D325"] = {"parents":["R01","R02"],"description":"PRES。若年女性(子癇)+高齢者",
    "cpt":{"0_1,male":0.0001,"0_1,female":0.0001,"1_5,male":0.0001,"1_5,female":0.0002,"6_12,male":0.0002,"6_12,female":0.0003,"13_17,male":0.0003,"13_17,female":0.0005,"18_39,male":0.0005,"18_39,female":0.002,"40_64,male":0.001,"40_64,female":0.002,"65_plus,male":0.001,"65_plus,female":0.001}}

# D326 腫瘍崩壊症候群(TLS)
s1["variables"].append({"id":"D326","name":"TLS","name_ja":"腫瘍崩壊症候群(TLS)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"化学療法後の大量腫瘍細胞崩壊→高K/高リン/高尿酸/低Ca→AKI+不整脈+痙攣。血液悪性腫瘍に多い"})
for to,r,c in [
    ("S13","TLS: 嘔気嘔吐(50-60%)",{"absent":0.30,"present":0.70}),
    ("L44","TLS: 高K血症(定義的, 70-80%)",{"normal":0.10,"hyponatremia":0.05,"hyperkalemia":0.75,"other":0.10}),
    ("L55","TLS: AKI(50-60%)",{"normal":0.20,"mild_elevated":0.30,"high_AKI":0.50}),
    ("S42","TLS: 痙攣(低Ca, 15-20%)",{"absent":0.75,"present":0.25}),
    ("E02","TLS: 不整脈/頻脈(高K, 30-40%)",{"under_100":0.30,"100_120":0.40,"over_120":0.30}),
    ("S07","TLS: 倦怠感(70-80%)",{"absent":0.10,"mild":0.30,"severe":0.60}),
    ("S10","TLS: 排尿減少(AKI, 30-40%)",{"absent":0.55,"present":0.45}),
    ("T01","TLS: 急性(化学療法後12-72h)",{"under_3d":0.80,"3d_to_1w":0.15,"1w_to_3w":0.04,"over_3w":0.01}),
    ("T02","TLS: 急性",{"sudden_hours":0.60,"gradual_days":0.40}),
]: add("D326","TLS",to,r,c)
s3["full_cpts"]["D326"] = {"parents":["R01"],"description":"TLS。全年齢(化学療法後)",
    "cpt":{"0_1":0.0005,"1_5":0.001,"6_12":0.001,"13_17":0.001,"18_39":0.001,"40_64":0.002,"65_plus":0.002}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 326 diseases")
