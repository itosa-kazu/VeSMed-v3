#!/usr/bin/env python3
"""Add D207-D211: 5 diseases."""
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

# D207 ヘパリン起因性血小板減少症 (HIT)
s1["variables"].append({"id":"D207","name":"HIT","name_ja":"ヘパリン起因性血小板減少症(HIT)",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"ヘパリン投与5-14日後. PLT50%以上低下+血栓症(DVT/PE/動脈). 4Tスコア. アルガトロバン治療"})
for to,r,c in [
    ("L14","HIT: 血小板減少(定義的)",{"normal":0.05,"left_shift":0.02,"atypical_lymphocytes":0.00,"thrombocytopenia":0.88,"eosinophilia":0.00,"lymphocyte_predominant":0.05}),
    ("L52","HIT: D-dimer上昇(血栓)",{"not_done":0.10,"normal":0.05,"mildly_elevated":0.20,"very_high":0.65}),
    ("S04","HIT: 呼吸困難(PE, 30-40%)",{"absent":0.50,"on_exertion":0.25,"at_rest":0.25}),
    ("E36","HIT: 下肢浮腫(DVT, 30-40%)",{"absent":0.50,"unilateral":0.40,"bilateral":0.10}),
    ("E02","HIT: 頻脈(PE/血栓)",{"under_100":0.30,"100_120":0.45,"over_120":0.25}),
    ("E12","HIT: 皮膚(注射部位壊死, 10-20%)",{"normal":0.70,"localized_erythema_warmth_swelling":0.10,"petechiae_purpura":0.03,"maculopapular_rash":0.01,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.03,"vesicle_bulla":0.01,"skin_necrosis":0.10}),
    ("T01","HIT: 亜急性(ヘパリン開始5-14日後)",{"under_3d":0.10,"3d_to_1w":0.40,"1w_to_3w":0.40,"over_3w":0.10}),
    ("T02","HIT: 亜急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D207","HIT",to,r,c)
s3["full_cpts"]["D207"] = {"parents":[],"description":"HIT. ヘパリン投与後","cpt":{"":0.001}}

# D208 ITP (特発性血小板減少性紫斑病)
s1["variables"].append({"id":"D208","name":"ITP","name_ja":"特発性血小板減少性紫斑病(ITP)",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"自己免疫性血小板破壊. 出血症状(紫斑/点状出血/歯肉出血). PLT<100k. 他の原因除外で診断"})
for to,r,c in [
    ("L14","ITP: 血小板減少(定義的)",{"normal":0.03,"left_shift":0.02,"atypical_lymphocytes":0.00,"thrombocytopenia":0.90,"eosinophilia":0.00,"lymphocyte_predominant":0.05}),
    ("S44","ITP: 出血傾向(60-80%)",{"absent":0.20,"present":0.80}),
    ("E12","ITP: 紫斑/点状出血(70-80%)",{"normal":0.15,"localized_erythema_warmth_swelling":0.01,"petechiae_purpura":0.45,"maculopapular_rash":0.01,"vesicular_dermatomal":0.01,"diffuse_erythroderma":0.01,"purpura":0.30,"vesicle_bulla":0.01,"skin_necrosis":0.05}),
    ("S07","ITP: 倦怠感(30-40%)",{"absent":0.50,"mild":0.35,"severe":0.15}),
    ("E01","ITP: 通常無熱",{"under_37.5":0.80,"37.5_38.0":0.10,"38.0_39.0":0.07,"39.0_40.0":0.02,"over_40.0":0.01}),
    ("T01","ITP: 急性~慢性",{"under_3d":0.15,"3d_to_1w":0.25,"1w_to_3w":0.30,"over_3w":0.30}),
    ("T02","ITP: 亜急性",{"sudden_hours":0.20,"gradual_days":0.80}),
]: add("D208","ITP",to,r,c)
s3["full_cpts"]["D208"] = {"parents":["R02"],"description":"ITP. 女性に多い(若年)",
    "cpt":{"male":0.001,"female":0.002}}

# D209 骨髄線維症 (Myelofibrosis)
s1["variables"].append({"id":"D209","name":"myelofibrosis","name_ja":"骨髄線維症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"JAK2/CALR/MPL変異. 巨脾+貧血+leukoerythroblastic picture. 涙滴赤血球. 全身症状(倦怠感/盗汗/体重減少)"})
for to,r,c in [
    ("S07","骨髄線維症: 倦怠感(80%+)",{"absent":0.08,"mild":0.25,"severe":0.67}),
    ("E01","骨髄線維症: 発熱(20-30%)",{"under_37.5":0.60,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.08,"over_40.0":0.02}),
    ("S12","骨髄線維症: 腹痛(脾腫, LUQ, 40-50%)",{"absent":0.40,"epigastric":0.05,"RUQ":0.03,"RLQ":0.02,"LLQ":0.40,"suprapubic":0.02,"diffuse":0.08}),
    ("L01","骨髄線維症: WBC(変動: 低~著高)",{"low_under_4000":0.15,"normal_4000_10000":0.25,"high_10000_20000":0.30,"very_high_over_20000":0.30}),
    ("L16","骨髄線維症: LDH上昇(骨髄外造血)",{"normal":0.15,"elevated":0.85}),
    ("T01","骨髄線維症: 慢性",{"under_3d":0.03,"3d_to_1w":0.05,"1w_to_3w":0.12,"over_3w":0.80}),
    ("T02","骨髄線維症: 緩徐",{"sudden_hours":0.05,"gradual_days":0.95}),
]: add("D209","myelofibrosis",to,r,c)
s3["full_cpts"]["D209"] = {"parents":["R01"],"description":"骨髄線維症. 中高年",
    "cpt":{"18_39":0.0003,"40_64":0.001,"65_plus":0.002}}

# D210 ポルフィリン症 (Acute Intermittent Porphyria)
s1["variables"].append({"id":"D210","name":"acute_porphyria","name_ja":"急性間欠性ポルフィリン症",
    "category":"disease","states":["no","yes"],"severity":"high",
    "note":"ALA/PBG蓄積. 五徴:腹痛+嘔吐+便秘+頻脈+精神症状. 暗赤色尿. 薬剤/月経/絶食が誘因. 女性に多い"})
for to,r,c in [
    ("S12","ポルフィリン: 腹痛(びまん性, 90%+)",{"absent":0.03,"epigastric":0.10,"RUQ":0.03,"RLQ":0.03,"LLQ":0.03,"suprapubic":0.03,"diffuse":0.75}),
    ("S13","ポルフィリン: 嘔吐(60-70%)",{"absent":0.25,"present":0.75}),
    ("E02","ポルフィリン: 頻脈(自律神経障害, 70-80%)",{"under_100":0.12,"100_120":0.45,"over_120":0.43}),
    ("E38","ポルフィリン: 高血圧(自律神経障害, 40-50%)",{"normal_under_140":0.40,"elevated_140_180":0.35,"crisis_over_180":0.25}),
    ("E16","ポルフィリン: 精神症状/意識障害(20-30%)",{"normal":0.60,"confused":0.30,"obtunded":0.10}),
    ("S42","ポルフィリン: 痙攣(低Na, 10-20%)",{"absent":0.80,"present":0.20}),
    ("L44","ポルフィリン: 低Na血症(SIADH, 30-40%)",{"normal":0.50,"hyponatremia":0.45,"hyperkalemia":0.02,"other":0.03}),
    ("S52","ポルフィリン: 四肢脱力(神経障害, 40-50%)",{"absent":0.45,"unilateral_weakness":0.10,"bilateral":0.45}),
    ("T01","ポルフィリン: 急性(発作は数日~数週)",{"under_3d":0.35,"3d_to_1w":0.35,"1w_to_3w":0.25,"over_3w":0.05}),
    ("T02","ポルフィリン: 急性",{"sudden_hours":0.45,"gradual_days":0.55}),
]: add("D210","acute_porphyria",to,r,c)
s3["full_cpts"]["D210"] = {"parents":["R02"],"description":"急性ポルフィリン症. 女性に多い",
    "cpt":{"male":0.0003,"female":0.001}}

# D211 自己免疫性溶血性貧血(冷式) (Cold AIHA / Cold Agglutinin Disease)
# Already D158 covers AIHA broadly. Let me pick something else.
# D211 急性腎障害(Prerenal) - too generic.
# D211 偽膜性腸炎 - D38 is C.diff already. Skip.
# D211 三環系抗うつ薬中毒 (TCA Overdose)
s1["variables"].append({"id":"D211","name":"TCA_overdose","name_ja":"三環系抗うつ薬中毒",
    "category":"disease","states":["no","yes"],"severity":"critical",
    "note":"Na+チャネル遮断→QRS幅延長→不整脈. 抗コリン作用→頻脈/口渇/瞳孔散大/尿閉. 痙攣. 重炭酸Na治療"})
for to,r,c in [
    ("E16","TCA: 意識障害(昏睡, 60-70%)",{"normal":0.15,"confused":0.35,"obtunded":0.50}),
    ("E02","TCA: 頻脈(抗コリン+Na遮断, 80%+)",{"under_100":0.08,"100_120":0.30,"over_120":0.62}),
    ("S42","TCA: 痙攣(30-40%)",{"absent":0.55,"present":0.45}),
    ("E03","TCA: 低血圧(α遮断, 40-50%)",{"normal_over_90":0.45,"hypotension_under_90":0.55}),
    ("E01","TCA: 体温(高体温/抗コリン, 30-40%)",{"under_37.5":0.40,"37.5_38.0":0.15,"38.0_39.0":0.20,"39.0_40.0":0.15,"over_40.0":0.10}),
    ("T01","TCA: 超急性",{"under_3d":0.95,"3d_to_1w":0.04,"1w_to_3w":0.01,"over_3w":0.00}),
    ("T02","TCA: 突発",{"sudden_hours":0.90,"gradual_days":0.10}),
]: add("D211","TCA_overdose",to,r,c)
s3["full_cpts"]["D211"] = {"parents":[],"description":"TCA中毒","cpt":{"":0.001}}

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"5 diseases added. Total: {s2['total_edges']} edges, 211 diseases")
