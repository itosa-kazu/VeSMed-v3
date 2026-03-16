#!/usr/bin/env python3
"""Edge audit fix for 350-disease model. Add clinically justified missing edges."""
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

# D78 熱中症 → L20 D-dimer (DIC合併で上昇)
# L20 is D-dimer in old format, check if it maps to L52
# Actually L20 may not be in noisy_or. Skip if not present.

# D81 SBP → L11 肝酵素 (肝硬変背景で上昇)
add("D81","SBP","L11","SBP: 肝硬変背景で肝酵素上昇",{"normal":0.15,"mild_elevated":0.45,"very_high":0.40})
# D81 SBP → T01, T02
add("D81","SBP","T01","SBP: 急性(数日)",{"under_3d":0.40,"3d_to_1w":0.35,"1w_to_3w":0.20,"over_3w":0.05})
add("D81","SBP","T02","SBP: 急性~亜急性",{"sudden_hours":0.30,"gradual_days":0.70})

# D127 胸水 → E15 心雑音 (弁膜症性胸水で)
# E15 might not be in noisy_or for all states. Skip complex ones.

# D140 DKA → S01 咳嗽 (Kussmaul呼吸で咳嗽は稀, skip - not clinically justified)
# D140 DKA → E05 SpO2 (通常正常, but can be low in severe cases)
add("D140","DKA","E05","DKA: SpO2(通常正常, 重症で低下あり)",{"normal_over_96":0.75,"mild_hypoxia_93_96":0.18,"severe_hypoxia_under_93":0.07})

# D258 RSV → L02 CRP (上昇)
add("D258","RSV","L02","RSV: CRP上昇(感染で)",{"normal_under_0.3":0.15,"mild_0.3_3":0.30,"moderate_3_10":0.35,"high_over_10":0.20})
# D258 RSV → S03 鼻汁 (RSV: 鼻汁は非常に多い)
add("D258","RSV","S03","RSV: 鼻汁(90%+)",{"absent":0.05,"rhinorrhea":0.60,"nasal_congestion":0.35})
# D258 RSV → E02 心拍数 (発熱/呼吸困難で頻脈)
add("D258","RSV","E02","RSV: 頻脈(発熱/呼吸困難)",{"under_100":0.20,"100_120":0.35,"over_120":0.45})
# D258 RSV → L04 CXR (過膨張+浸潤影)
add("D258","RSV","L04","RSV: CXR(過膨張/浸潤)",{"normal":0.15,"lobar_infiltrate":0.15,"bilateral_infiltrate":0.55,"BHL":0.02,"pleural_effusion":0.08,"pneumothorax":0.05})

# D263 マイコプラズマ → E04 呼吸数 / E05 SpO2
add("D263","mycoplasma","E05","マイコプラズマ: SpO2(通常正常~軽度低下)",{"normal_over_96":0.55,"mild_hypoxia_93_96":0.30,"severe_hypoxia_under_93":0.15})
add("D263","mycoplasma","E04","マイコプラズマ: 呼吸数上昇(肺炎)",{"normal":0.40,"mildly_elevated":0.35,"tachypnea":0.25})

# D264 クラミジア肺炎 → S04 呼吸困難 / E05 SpO2 / E04 呼吸数
add("D264","chlamydia_pneumoniae","S04","クラミジア肺炎: 呼吸困難(30-40%)",{"absent":0.50,"on_exertion":0.35,"at_rest":0.15})
add("D264","chlamydia_pneumoniae","E05","クラミジア肺炎: SpO2(軽度低下あり)",{"normal_over_96":0.50,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.15})
add("D264","chlamydia_pneumoniae","E04","クラミジア肺炎: 呼吸数上昇",{"normal":0.40,"mildly_elevated":0.40,"tachypnea":0.20})
add("D264","chlamydia_pneumoniae","E02","クラミジア肺炎: 頻脈(発熱/呼吸困難)",{"under_100":0.30,"100_120":0.40,"over_120":0.30})

# D265 インフルエンザ菌性肺炎 → S03 鼻汁
add("D265","H_influenzae","S03","H.flu肺炎: 鼻汁(上気道症状, 40-50%)",{"absent":0.40,"rhinorrhea":0.35,"nasal_congestion":0.25})

# D277 肺腺癌 → E05 SpO2 / E07 肺聴診 / E04 呼吸数
add("D277","lung_adenocarcinoma","E05","肺腺癌: SpO2低下(進行例)",{"normal_over_96":0.35,"mild_hypoxia_93_96":0.35,"severe_hypoxia_under_93":0.30})
add("D277","lung_adenocarcinoma","E07","肺腺癌: 肺聴診(減弱/crackles)",{"clear":0.20,"crackles":0.30,"wheezes":0.15,"decreased_absent":0.35})
add("D277","lung_adenocarcinoma","E36","肺腺癌: 下肢浮腫(SVC症候群/悪液質)",{"absent":0.60,"unilateral":0.10,"bilateral":0.30})
add("D277","lung_adenocarcinoma","L52","肺腺癌: D-dimer上昇(癌関連凝固亢進)",{"not_done":0.15,"normal":0.15,"mildly_elevated":0.40,"very_high":0.30})

# D278 悪性胸膜中皮腫 → E07 肺聴診 / E01 発熱 / E02 心拍数 / L02 CRP
add("D278","mesothelioma","E07","悪性中皮腫: 肺聴診(呼吸音減弱, 胸水)",{"clear":0.08,"crackles":0.12,"wheezes":0.05,"decreased_absent":0.75})
add("D278","mesothelioma","E01","悪性中皮腫: 発熱(20-30%)",{"under_37.5":0.55,"37.5_38.0":0.15,"38.0_39.0":0.15,"39.0_40.0":0.10,"over_40.0":0.05})
add("D278","mesothelioma","E02","悪性中皮腫: 頻脈(呼吸不全)",{"under_100":0.30,"100_120":0.40,"over_120":0.30})
add("D278","mesothelioma","L02","悪性中皮腫: CRP上昇(炎症/腫瘍)",{"normal_under_0.3":0.10,"mild_0.3_3":0.20,"moderate_3_10":0.40,"high_over_10":0.30})
add("D278","mesothelioma","E36","悪性中皮腫: 下肢浮腫(悪液質)",{"absent":0.55,"unilateral":0.10,"bilateral":0.35})

# D285 減圧症 → E01 体温 (通常正常)
add("D285","DCS","E01","減圧症: 体温(通常正常~低体温)",{"under_37.5":0.70,"37.5_38.0":0.15,"38.0_39.0":0.10,"39.0_40.0":0.04,"over_40.0":0.01})

# D295 群発頭痛 → S03 鼻汁 (自律神経症状)
add("D295","cluster_headache","S03","群発頭痛: 鼻汁/鼻閉(自律神経症状, 70-80%)",{"absent":0.15,"rhinorrhea":0.50,"nasal_congestion":0.35})

# D316 もやもや → E02 心拍数 (急性発症で頻脈)
add("D316","moyamoya","E02","もやもや: 頻脈(急性発症時)",{"under_100":0.30,"100_120":0.40,"over_120":0.30})

# D276 卵巣捻転 → L02 CRP (軽度上昇)
add("D276","ovarian_torsion","L02","卵巣捻転: CRP軽度上昇(炎症)",{"normal_under_0.3":0.25,"mild_0.3_3":0.35,"moderate_3_10":0.30,"high_over_10":0.10})

s2["total_edges"] = len(s2["edges"])
for fname, data in [("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']} edges")
