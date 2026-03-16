#!/usr/bin/env python3
"""Edge audit round 2 - deeper pass on remaining missing edges."""
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

# avg_r=4: D325 PRES → E02/L54/E36
add("D325","PRES","E02","PRES: 頻脈(痙攣/高血圧クリーゼ, 30-40%)",{"under_100":0.30,"100_120":0.35,"over_120":0.35})
add("D325","PRES","L54","PRES: 血糖(DM合併で高血糖あり)",{"normal":0.50,"hyperglycemia":0.35,"hypoglycemia":0.05,"very_high_over_500":0.10})
add("D325","PRES","E36","PRES: 浮腫(腎障害/子癇, 20-30%)",{"absent":0.55,"unilateral":0.05,"bilateral":0.40})

# avg_r=4: D321 アルドステロン → S15 腰背部痛(副腎腫瘤)
add("D321","primary_aldosteronism","S15","アルドステロン症: 腰背部痛(副腎腫瘤/低K性筋痛, 20-30%)",{"absent":0.60,"present":0.40})

# avg_r=5: D319 気管支拡張 → S07 (already has it? check)
# avg_r=5: D305 EDH → E01 体温
add("D305","acute_epidural_hematoma","E01","急性EDH: 体温(通常正常)",{"under_37.5":0.70,"37.5_38.0":0.15,"38.0_39.0":0.10,"39.0_40.0":0.04,"over_40.0":0.01})

# avg_r=6: D317 PAP → E01 体温(通常無熱)
add("D317","PAP","E01","PAP: 体温(通常無熱)",{"under_37.5":0.75,"37.5_38.0":0.12,"38.0_39.0":0.08,"39.0_40.0":0.04,"over_40.0":0.01})

# avg_r=7: D331 脂肪塞栓 → E07 肺聴診
add("D331","fat_embolism","E07","脂肪塞栓: 肺聴診(ラ音/水泡音, 50-60%)",{"clear":0.20,"crackles":0.55,"wheezes":0.10,"decreased_absent":0.15})
# D331 → L01 WBC
add("D331","fat_embolism","L01","脂肪塞栓: WBC上昇(炎症反応, 40-50%)",{"low_under_4000":0.05,"normal_4000_10000":0.30,"high_10000_20000":0.40,"very_high_over_20000":0.25})

# avg_r=8: D304 DLB → S53 構音障害
add("D304","DLB","S53","DLB: 構音障害/失語(30-40%)",{"absent":0.50,"dysarthria":0.35,"aphasia":0.15})

# avg_r=8: D344 収縮性心膜炎 → E02 心拍数
add("D344","constrictive_pericarditis","E02","収縮性心膜炎: 徐脈~頻脈(40-50%)",{"under_100":0.40,"100_120":0.35,"over_120":0.25})

# avg_r=9: D315 CVST → E06 項部硬直(SAH様, 20-30%)
add("D315","CVST","E06","CVST: 項部硬直(出血合併/頭蓋内圧, 20-30%)",{"absent":0.65,"present":0.35})

# avg_r=10: D347 神経芽腫 → E02 頻脈
add("D347","neuroblastoma","E02","神経芽腫: 頻脈(カテコラミン/貧血/発熱, 30-40%)",{"under_100":0.35,"100_120":0.35,"over_120":0.30})

# avg_r=15: D321 → S52 局所神経症状(低K性四肢脱力)
add("D321","primary_aldosteronism","S52","アルドステロン症: 四肢脱力(低K, 20-30%)",{"absent":0.55,"unilateral_weakness":0.15,"bilateral":0.30})
# D321 → L11 肝酵素(横紋筋融解合併→AST上昇)
add("D321","primary_aldosteronism","L11","アルドステロン症: AST上昇(横紋筋融解合併, 15-20%)",{"normal":0.65,"mild_elevated":0.20,"very_high":0.15})

# avg_r=21: D323 胎盤早期剥離 → L16 LDH / L55 Cr
add("D323","placental_abruption","L16","胎盤早期剥離: LDH上昇(溶血/DIC, 30-40%)",{"normal":0.40,"elevated":0.60})
add("D323","placental_abruption","L55","胎盤早期剥離: AKI(出血性ショック/DIC, 20-30%)",{"normal":0.55,"mild_elevated":0.25,"high_AKI":0.20})

# avg_r=22: D342 LQTS → S13 嘔気 / E38 BP / L44 電解質
add("D342","LQTS","S13","LQTS: 嘔気嘔吐(TdP後, 20-30%)",{"absent":0.65,"present":0.35})
add("D342","LQTS","E38","LQTS: 血圧(TdP時低下~正常)",{"normal_under_140":0.60,"elevated_140_180":0.25,"crisis_over_180":0.15})
add("D342","LQTS","L44","LQTS: 電解質異常(低K/低Mgで誘発, 30-40%)",{"normal":0.45,"hyponatremia":0.10,"hyperkalemia":0.05,"other":0.40})

# avg_r=26: D279 縦隔炎 → S01/E05/E16
add("D279","mediastinitis","S01","縦隔炎: 咳嗽(20-30%)",{"absent":0.60,"dry":0.25,"productive":0.15})
add("D279","mediastinitis","E05","縦隔炎: SpO2低下(呼吸障害, 30-40%)",{"normal_over_96":0.35,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.30})
add("D279","mediastinitis","E16","縦隔炎: 意識障害(敗血症, 20-30%)",{"normal":0.50,"confused":0.30,"obtunded":0.20})

# avg_r=26: D285 減圧症 → E16 意識障害
add("D285","DCS","E16","減圧症: 意識障害(脳型, 20-30%)",{"normal":0.50,"confused":0.30,"obtunded":0.20})
# D285 → E02 頻脈
add("D285","DCS","E02","減圧症: 頻脈(ショック/疼痛, 30-40%)",{"under_100":0.35,"100_120":0.35,"over_120":0.30})
# D285 → L01 WBC
add("D285","DCS","L01","減圧症: WBC上昇(ストレス反応, 30-40%)",{"low_under_4000":0.05,"normal_4000_10000":0.40,"high_10000_20000":0.35,"very_high_over_20000":0.20})

# avg_r=33: D321 → S42 痙攣(低K→VT→失神)
add("D321","primary_aldosteronism","S42","アルドステロン症: 失神/痙攣(低K→VT/VF, 10-20%)",{"absent":0.75,"present":0.25})
# D321 → E16 意識障害
add("D321","primary_aldosteronism","E16","アルドステロン症: 意識障害(低K→VT→心停止, 10-15%)",{"normal":0.70,"confused":0.15,"obtunded":0.15})

# D345 Sheehan → S42 痙攣(低Na/低血糖→痙攣)
add("D345","sheehan","S42","Sheehan: 痙攣(低Na/低血糖→痙攣, 15-20%)",{"absent":0.70,"present":0.30})

# D348 ウィルムス → S13 嘔吐
add("D348","wilms_tumor","S13","ウィルムス: 嘔気嘔吐(腹部圧迫, 20-30%)",{"absent":0.60,"present":0.40})
# D348 → L04 CXR(肺転移)
add("D348","wilms_tumor","L04","ウィルムス: CXR(肺転移, 15-20%)",{"normal":0.65,"lobar_infiltrate":0.10,"bilateral_infiltrate":0.10,"BHL":0.02,"pleural_effusion":0.08,"pneumothorax":0.05})
# D348 → L44 電解質(Na/Ca低下)
add("D348","wilms_tumor","L44","ウィルムス: 電解質異常(Na/Ca低下, 15-20%)",{"normal":0.60,"hyponatremia":0.25,"hyperkalemia":0.05,"other":0.10})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']} edges")
