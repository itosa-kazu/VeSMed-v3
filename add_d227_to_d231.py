#!/usr/bin/env python3
"""Add D227-D231: 5 diseases."""
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

# D227 胸腺腫 (Thymoma)
s1["variables"].append({"id":"D227","name":"thymoma","name_ja":"胸腺腫",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"前縦隔腫瘍。MG合併(30-50%)。赤芽球癆/低γグロブリン血症/SLE/重症筋無力症"})
for to,r,c in [
    ("S04","胸腺腫: 呼吸困難(圧迫/MG, 30-40%)",{"absent":0.50,"on_exertion":0.30,"at_rest":0.20}),
    ("S21","胸腺腫: 胸痛(圧迫, 20-30%)",{"absent":0.65,"burning":0.03,"sharp":0.15,"pressure":0.12,"tearing":0.05}),
    ("S01","胸腺腫: 咳嗽(圧迫, 20-30%)",{"absent":0.65,"dry":0.25,"productive":0.10}),
    ("S07","胸腺腫: 倦怠感(40-50%)",{"absent":0.40,"mild":0.35,"severe":0.25}),
    ("L04","胸腺腫: CXR(前縦隔腫瘤)",{"normal":0.15,"lobar_infiltrate":0.02,"bilateral_infiltrate":0.05,"BHL":0.10,"pleural_effusion":0.08,"pneumothorax":0.60}),
    ("T01","胸腺腫: 慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.20,"over_3w":0.65}),
    ("T02","胸腺腫: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D227","thymoma",to,r,c)
s3["full_cpts"]["D227"] = {"parents":["R01"],"description":"胸腺腫","cpt":{"18_39":0.0005,"40_64":0.001,"65_plus":0.001}}

# D228 発作性夜間ヘモグロビン尿症 (PNH)
s1["variables"].append({"id":"D228","name":"PNH","name_ja":"発作性夜間ヘモグロビン尿症(PNH)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"GPI-AP欠損→補体介在性溶血+血栓+骨髄不全。暗色尿(朝)+貧血+血栓。エクリズマブ治療"})
for to,r,c in [
    ("S07","PNH: 倦怠感(貧血, 80%+)",{"absent":0.08,"mild":0.25,"severe":0.67}),
    ("E18","PNH: 黄疸(溶血, 40-50%)",{"absent":0.45,"present":0.55}),
    ("L16","PNH: LDH上昇(溶血, 90%+)",{"normal":0.05,"elevated":0.95}),
    ("S12","PNH: 腹痛(腸間膜血栓, 30-40%)",{"absent":0.50,"epigastric":0.10,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.02,"diffuse":0.23}),
    ("S04","PNH: 呼吸困難(貧血/PE, 30-40%)",{"absent":0.50,"on_exertion":0.35,"at_rest":0.15}),
    ("L52","PNH: D-dimer上昇(血栓, 50-60%)",{"not_done":0.15,"normal":0.10,"mildly_elevated":0.25,"very_high":0.50}),
    ("T01","PNH: 慢性(急性増悪も)",{"under_3d":0.15,"3d_to_1w":0.25,"1w_to_3w":0.30,"over_3w":0.30}),
    ("T02","PNH: 亜急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D228","PNH",to,r,c)
s3["full_cpts"]["D228"] = {"parents":[],"description":"PNH","cpt":{"":0.0005}}

# D229 自己免疫性膵炎 (AIP/IgG4関連)
s1["variables"].append({"id":"D229","name":"autoimmune_pancreatitis","name_ja":"自己免疫性膵炎(AIP)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"IgG4関連(1型)/非IgG4(2型)。閉塞性黄疸+膵腫大+IgG4高値。膵癌との鑑別重要。ステロイド著効"})
for to,r,c in [
    ("E18","AIP: 閉塞性黄疸(60-70%)",{"absent":0.25,"present":0.75}),
    ("S12","AIP: 腹痛(心窩部, 40-50%)",{"absent":0.40,"epigastric":0.40,"RUQ":0.10,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.05}),
    ("S07","AIP: 倦怠感(50-60%)",{"absent":0.30,"mild":0.40,"severe":0.30}),
    ("L11","AIP: 肝酵素上昇(胆汁うっ滞)",{"normal":0.20,"mild_elevated":0.50,"very_high":0.30}),
    ("E01","AIP: 通常無熱",{"under_37.5":0.75,"37.5_38.0":0.12,"38.0_39.0":0.08,"39.0_40.0":0.04,"over_40.0":0.01}),
    ("T01","AIP: 亜急性~慢性",{"under_3d":0.05,"3d_to_1w":0.10,"1w_to_3w":0.30,"over_3w":0.55}),
    ("T02","AIP: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D229","autoimmune_pancreatitis",to,r,c)
s3["full_cpts"]["D229"] = {"parents":["R01","R02"],"description":"AIP. 中高年男性に多い",
    "cpt":{"18_39,male":0.0005,"18_39,female":0.0002,"40_64,male":0.002,"40_64,female":0.0005,"65_plus,male":0.002,"65_plus,female":0.0005}}

# D230 膵癌 (Pancreatic Cancer)
s1["variables"].append({"id":"D230","name":"pancreatic_cancer","name_ja":"膵癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"無痛性閉塞性黄疸(膵頭部)+体重減少+背部痛+新規DM。5年生存率<10%"})
for to,r,c in [
    ("E18","膵癌: 黄疸(膵頭部, 70-80%)",{"absent":0.15,"present":0.85}),
    ("S12","膵癌: 腹痛(心窩部/背部, 60-70%)",{"absent":0.20,"epigastric":0.45,"RUQ":0.10,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.20}),
    ("S15","膵癌: 背部痛(40-50%)",{"absent":0.45,"present":0.55}),
    ("S07","膵癌: 倦怠感/体重減少(80%+)",{"absent":0.08,"mild":0.25,"severe":0.67}),
    ("L11","膵癌: 肝酵素上昇(胆汁うっ滞)",{"normal":0.15,"mild_elevated":0.45,"very_high":0.40}),
    ("L54","膵癌: 血糖(新規DM, 30-40%)",{"hypoglycemia":0.02,"normal":0.40,"hyperglycemia":0.45,"very_high_over_500":0.13}),
    ("L52","膵癌: D-dimer上昇(Trousseau, 40-50%)",{"not_done":0.15,"normal":0.15,"mildly_elevated":0.30,"very_high":0.40}),
    ("T01","膵癌: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.20,"over_3w":0.70}),
    ("T02","膵癌: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D230","pancreatic_cancer",to,r,c)
s3["full_cpts"]["D230"] = {"parents":["R01"],"description":"膵癌. 中高年","cpt":{"18_39":0.0003,"40_64":0.002,"65_plus":0.004}}

# D231 胆管癌 (Cholangiocarcinoma)
s1["variables"].append({"id":"D231","name":"cholangiocarcinoma","name_ja":"胆管癌",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"肝内/肝門部/遠位胆管。閉塞性黄疸+体重減少+腹痛。PSC/肝吸虫がリスク"})
for to,r,c in [
    ("E18","胆管癌: 黄疸(80%+)",{"absent":0.10,"present":0.90}),
    ("S12","胆管癌: 腹痛(RUQ/心窩部, 40-50%)",{"absent":0.40,"epigastric":0.15,"RUQ":0.35,"RLQ":0.02,"LLQ":0.02,"suprapubic":0.01,"diffuse":0.05}),
    ("S07","胆管癌: 倦怠感/体重減少(70-80%)",{"absent":0.12,"mild":0.30,"severe":0.58}),
    ("L11","胆管癌: 肝酵素上昇(胆汁うっ滞)",{"normal":0.05,"mild_elevated":0.35,"very_high":0.60}),
    ("E01","胆管癌: 発熱(胆管炎合併, 20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("L01","胆管癌: WBC上昇(胆管炎時)",{"low_under_4000":0.05,"normal_4000_10000":0.40,"high_10000_20000":0.35,"very_high_over_20000":0.20}),
    ("T01","胆管癌: 慢性",{"under_3d":0.03,"3d_to_1w":0.07,"1w_to_3w":0.20,"over_3w":0.70}),
    ("T02","胆管癌: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D231","cholangiocarcinoma",to,r,c)
s3["full_cpts"]["D231"] = {"parents":["R01"],"description":"胆管癌","cpt":{"18_39":0.0002,"40_64":0.001,"65_plus":0.003}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 231 diseases")
