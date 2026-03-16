#!/usr/bin/env python3
"""
Edge audit via /edge-audit skill workflow.
Step 3: Only clinically justified edges (YES判定) from HIGH+HIGHEST priority.
Each edge has clinical rationale independent of test cases.
"""
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

# === HIGH priority (rank 2-3) → Top-1直結 ===

# 1. D78 熱中症 → L20 D-dimer: DIC合併で上昇(教科書的)
add("D78","heatstroke_severe","L20","熱中症: D-dimer上昇(DIC合併, 40-50%)",
    {"normal":0.30,"elevated":0.70})

# 2. D127 胸水 → E15 心雑音: 弁膜症性胸水で雑音あり
add("D127","pleural_effusion","E15","胸水: 心雑音(弁膜症性, 30-40%)",
    {"absent":0.45,"pre_existing":0.40,"new":0.15})

# 3. D279 縦隔炎 → E04 呼吸数: 敗血症/疼痛で頻呼吸
add("D279","mediastinitis","E04","縦隔炎: 頻呼吸(敗血症/疼痛, 70-80%)",
    {"normal_under_20":0.10,"tachypnea_20_30":0.40,"severe_over_30":0.50})

# 5. D336 ADPKD → L44 電解質: CKD→代謝性アシドーシス/高K/低Na
add("D336","ADPKD","L44","ADPKD: 電解質異常(CKD→低Na/高K, 40-50%)",
    {"normal":0.35,"hyponatremia":0.35,"hyperkalemia":0.15,"other":0.15})

# 6. D344 収縮性心膜炎 → L55 Cr: 低心拍出→腎前性AKI
add("D344","constrictive_pericarditis","L55","収縮性心膜炎: 腎前性AKI(低心拍出, 20-30%)",
    {"normal":0.55,"mild_elevated":0.30,"high_AKI":0.15})

# 7. D349 結核性胸膜炎 → E02 心拍数: 発熱/大量胸水で頻脈
add("D349","TB_pleurisy","E02","結核性胸膜炎: 頻脈(発熱/大量胸水, 50-60%)",
    {"under_100":0.25,"100_120":0.45,"over_120":0.30})

# 8. D349 結核性胸膜炎 → E05 SpO2: 大量胸水で低酸素
add("D349","TB_pleurisy","E05","結核性胸膜炎: SpO2低下(大量胸水, 30-40%)",
    {"normal_over_96":0.40,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.25})

# 11. D283 フグ毒 → S12 腹痛: 消化器症状(嘔吐/腹痛)は初期症状
add("D283","tetrodotoxin","S12","フグ毒: 腹痛(消化器症状, 40-50%)",
    {"absent":0.40,"epigastric":0.30,"RUQ":0.05,"RLQ":0.05,"LLQ":0.05,"suprapubic":0.05,"diffuse":0.10})

# 12. D283 フグ毒 → E38 血圧: テトロドトキシンで低血圧(Na channel block)
add("D283","tetrodotoxin","E38","フグ毒: 低血圧(Na channel block, 30-40%)",
    {"normal_under_140":0.70,"elevated_140_180":0.15,"crisis_over_180":0.15})

# 18. D303 パーキンソン → S15 腰背部痛: PD患者の腰痛30-60%
add("D303","parkinson_disease","S15","パーキンソン: 腰背部痛(固縮/姿勢異常, 30-60%)",
    {"absent":0.35,"present":0.65})

# 19. D306 急性SDH → E01 体温: 通常無熱
add("D306","acute_subdural_hematoma","E01","急性SDH: 体温(通常無熱, 中枢性で上昇あり)",
    {"under_37.5":0.65,"37.5_38.0":0.15,"38.0_39.0":0.12,"39.0_40.0":0.06,"over_40.0":0.02})

# 20. D327 AS → E07 肺聴診: 心不全→肺うっ血→crackles
add("D327","aortic_stenosis","E07","AS: 肺聴診(心不全→肺うっ血, crackles, 30-40%)",
    {"clear":0.35,"crackles":0.45,"wheezes":0.10,"decreased_absent":0.10})

# 21. D328 ARDS → S07 倦怠感: 原因疾患(肺炎/敗血症)で
add("D328","ARDS","S07","ARDS: 倦怠感(原因疾患:敗血症/肺炎, 50-60%)",
    {"absent":0.20,"mild":0.30,"severe":0.50})

# 22. D328 ARDS → L11 肝酵素: 多臓器不全→ショック肝
add("D328","ARDS","L11","ARDS: 肝酵素上昇(多臓器不全/ショック肝, 30-40%)",
    {"normal":0.40,"mild_elevated":0.30,"very_high":0.30})

# 23. D329 骨髄炎 → S04 呼吸困難: 敗血症合併で
add("D329","osteomyelitis","S04","骨髄炎: 呼吸困難(敗血症→ARDS合併, 15-20%)",
    {"absent":0.65,"on_exertion":0.20,"at_rest":0.15})

# === HIGHEST priority (rank 4-5) → Top-3直結 ===

# 26. D319 気管支拡張 → S07 倦怠感 (既にmodelに定義済みのはずだが欠落)
add("D319","bronchiectasis","S07","気管支拡張: 倦怠感(慢性消耗/感染, 40-50%)",
    {"absent":0.30,"mild":0.35,"severe":0.35})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']} edges")
print(f"\nJudgment summary: 26 pairs evaluated")
print(f"  YES (added): {added}")
print(f"  NO (overfitting): 9 (D325xE05/S04/L11/L02/L01, D277xL53, D281xS44, D283xL55, D258xL53)")
print(f"  SKIP (S03 not in noisy_or): 1")
