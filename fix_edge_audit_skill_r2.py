#!/usr/bin/env python3
"""
Edge audit round 2 via /edge-audit skill.
Step 3 clinical judgment applied to MEDIUM + selected LOW priority pairs.
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

# === MEDIUM (rank 6-10) ===

# D286 高Ca → E03 血圧: 高Caで高血圧(教科書的, 30-40%)
add("D286","hypercalcemia","E03","高Ca: 高血圧→低血圧(脱水時)",
    {"normal_over_90":0.80,"hypotension_under_90":0.20})

# === LOW (rank 11+) — 臨床的に妥当なもののみ ===

# D323 胎盤早期剥離 → M02 ショック(3件, 教科書的)
add("D323","placental_abruption","M02","胎盤早期剥離: 出血性ショック(30-40%)",
    {"stable":0.30,"compensated":0.40,"shock":0.30})

# D128 喉頭蓋炎 → S13 嘔気(嚥下困難→嘔気, 20-30%)
add("D128","epiglottitis","S13","喉頭蓋炎: 嘔気(嚥下困難, 20-30%)",
    {"absent":0.65,"present":0.35})

# D340 僧帽弁狭窄 → S01 咳嗽(肺うっ血→咳嗽, 40-50%)
add("D340","mitral_stenosis","S01","僧帽弁狭窄: 咳嗽(肺うっ血, 40-50%)",
    {"absent":0.40,"dry":0.40,"productive":0.20})
# D340 → E38 血圧(高血圧合併, 40-50%)
add("D340","mitral_stenosis","E38","僧帽弁狭窄: 高血圧(合併, 40-50%)",
    {"normal_under_140":0.35,"elevated_140_180":0.40,"crisis_over_180":0.25})
# D340 → E05 SpO2(肺うっ血→低酸素, 30-40%)
add("D340","mitral_stenosis","E05","僧帽弁狭窄: SpO2低下(肺うっ血, 30-40%)",
    {"normal_over_96":0.40,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.25})
# D340 → L11 肝酵素(うっ血肝, 20-30%)
add("D340","mitral_stenosis","L11","僧帽弁狭窄: 肝酵素上昇(うっ血肝, 20-30%)",
    {"normal":0.55,"mild_elevated":0.30,"very_high":0.15})

# D334 IgG4 → S13 嘔気(膵炎, 30-40%)
add("D334","IgG4_RD","S13","IgG4: 嘔気嘔吐(膵炎, 30-40%)",
    {"absent":0.55,"present":0.45})
# D334 → L01 WBC(炎症, 30-40%)
add("D334","IgG4_RD","L01","IgG4: WBC上昇(炎症, 30-40%)",
    {"low_under_4000":0.05,"normal_4000_10000":0.40,"high_10000_20000":0.40,"very_high_over_20000":0.15})
# D334 → L02 CRP(炎症, 40-50%)
add("D334","IgG4_RD","L02","IgG4: CRP上昇(炎症, 40-50%)",
    {"normal_under_0.3":0.15,"mild_0.3_3":0.25,"moderate_3_10":0.35,"high_over_10":0.25})

# D287 胆嚢癌 → L01 WBC(閉塞性胆管炎, 40-50%)
add("D287","gallbladder_cancer","L01","胆嚢癌: WBC上昇(閉塞性胆管炎, 40-50%)",
    {"low_under_4000":0.05,"normal_4000_10000":0.30,"high_10000_20000":0.40,"very_high_over_20000":0.25})
# D287 → L02 CRP(同上)
add("D287","gallbladder_cancer","L02","胆嚢癌: CRP上昇(閉塞性胆管炎, 40-50%)",
    {"normal_under_0.3":0.10,"mild_0.3_3":0.20,"moderate_3_10":0.35,"high_over_10":0.35})
# D287 → S15 腹痛(右上腹部痛, 60-70%)
add("D287","gallbladder_cancer","S15","胆嚢癌: 右上腹部/腰背部痛(60-70%)",
    {"absent":0.20,"present":0.80})

# D345 Sheehan → E36 浮腫(甲状腺低下→粘液水腫, 30-40%)
add("D345","sheehan","E36","Sheehan: 浮腫(甲状腺低下→粘液水腫, 30-40%)",
    {"absent":0.45,"unilateral":0.05,"bilateral":0.50})
# D345 → L55 Cr(副腎不全→腎前性, 15-20%)
add("D345","sheehan","L55","Sheehan: Cr上昇(副腎不全→腎前性AKI, 15-20%)",
    {"normal":0.65,"mild_elevated":0.25,"high_AKI":0.10})

# D343 たこつぼ → L01 WBC(ストレス反応→白血球上昇, 40-50%)
add("D343","takotsubo","L01","たこつぼ: WBC上昇(カテコラミンストレス, 40-50%)",
    {"low_under_4000":0.03,"normal_4000_10000":0.35,"high_10000_20000":0.40,"very_high_over_20000":0.22})

# D335 PAD → L55 Cr(DM/CKD背景, 40-50%)
add("D335","PAD","L55","PAD: Cr上昇(DM/CKD背景, 40-50%)",
    {"normal":0.30,"mild_elevated":0.35,"high_AKI":0.35})
# D335 → E02 心拍数(急性虚血/疼痛, 20-30%)
add("D335","PAD","E02","PAD: 頻脈(急性虚血/疼痛, 20-30%)",
    {"under_100":0.45,"100_120":0.30,"over_120":0.25})

# D295 群発頭痛 → S13 嘔気(30-40%)
add("D295","cluster_headache","S13","群発頭痛: 嘔気(30-40%)",
    {"absent":0.55,"present":0.45})

# D301 NMOSD → S07 倦怠感(慢性疾患, 40-50%)
add("D301","NMOSD","S07","NMOSD: 倦怠感(慢性消耗, 40-50%)",
    {"absent":0.35,"mild":0.35,"severe":0.30})

# D290 膀胱癌 → L55 Cr(尿路閉塞→腎後性AKI, 20-30%)
add("D290","bladder_cancer","L55","膀胱癌: Cr上昇(尿路閉塞→腎後性AKI, 20-30%)",
    {"normal":0.50,"mild_elevated":0.30,"high_AKI":0.20})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Judgment summary
no_pairs = [
    "D286→L17(高Ca→CK, 原発巣固有)", "D286→L53(高Ca→トロポニン, 稀)",
    "D340→L01(MS→WBC, 因果なし)", "D345→L11(Sheehan→肝酵素, 因果弱)",
    "D343→L11(たこつぼ→肝酵素, 稀)",
]
skip_pairs = ["D265→S03(S03未実装)", "D295→S03(S03未実装)"]
print(f"Added {added} edges. Total: {s2['total_edges']} edges")
print(f"\nJudgment: YES={added}, NO={len(no_pairs)}, SKIP={len(skip_pairs)}")
print(f"NO: {', '.join(no_pairs)}")
print(f"SKIP: {', '.join(skip_pairs)}")
