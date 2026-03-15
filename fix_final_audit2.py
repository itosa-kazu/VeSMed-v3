#!/usr/bin/env python3
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

# D14 IE → L22 (splenomegaly)
add("D14","IE","L22","IE: 脾腫(感染性塞栓, 30-40%)",{"absent":0.55,"present":0.45})

# D04 扁桃周囲膿瘍 → S25嚥下困難, E22口蓋垂偏位
add("D04","peritonsillar_abscess","S25","扁桃周囲膿瘍: 嚥下困難(90%+)",{"absent":0.05,"present":0.95})
add("D04","peritonsillar_abscess","E22","扁桃周囲膿瘍: 口蓋垂偏位(70-80%)",{"absent":0.15,"present":0.85})

# D148 尿管結石 → L53 troponin (通常normal)
add("D148","urolithiasis","L53","尿管結石: トロポニン(通常正常)",{"not_done":0.20,"normal":0.70,"mildly_elevated":0.08,"very_high":0.02})

# D125 pneumothorax → S49 orthopnea
add("D125","pneumothorax","S49","気胸: 起座呼吸(20-30%)",{"absent":0.65,"present":0.35})

# D67 lymphoma → L19 ANCA negative, E28 ascites, L18 ANA negative
add("D67","lymphoma","E28","リンパ腫: 腹水(進行期, 20-30%)",{"absent":0.65,"present":0.35})

# D209 骨髄線維症 → L09 gram_negative (salmonella等感染合併)
add("D209","myelofibrosis","L09","骨髄線維症: 血培(免疫不全→感染)",{"not_done_or_pending":0.15,"negative":0.40,"gram_positive":0.20,"gram_negative":0.25})

# D08 胆管炎 → E11 CVA tenderness absent, E09 soft (atypical)
add("D08","cholangitis","E09","胆管炎: 腹部(通常RUQ圧痛, 非典型では軟)",{"soft_nontender":0.15,"localized_tenderness":0.65,"peritoneal_signs":0.20})
add("D08","cholangitis","E11","胆管炎: CVA叩打痛(通常なし)",{"absent":0.70,"present":0.30})

# D99 NTM → T02
add("D99","NTM","T02","NTM: 発症(慢性~亜急性)",{"sudden_hours":0.10,"gradual_days":0.90})

# D200 NPH → S42 seizure
add("D200","NPH","S42","NPH: 痙攣(合併てんかん, 10-15%)",{"absent":0.85,"present":0.15})

# D156 TTP → E05, E04, S01, S04, E07 (influenza-triggered TTP case R316)
add("D156","TTP","E05","TTP: 低酸素(肺出血/感染合併)",{"normal_over_96":0.50,"mild_hypoxia_93_96":0.25,"severe_hypoxia_under_93":0.25})
add("D156","TTP","E04","TTP: 頻呼吸(感染合併時)",{"normal_under_20":0.40,"tachypnea_20_30":0.35,"severe_over_30":0.25})
add("D156","TTP","S01","TTP: 咳嗽(感染誘因時)",{"absent":0.55,"dry":0.30,"productive":0.15})
add("D156","TTP","S04","TTP: 呼吸困難(感染/肺合併症)",{"absent":0.45,"on_exertion":0.30,"at_rest":0.25})
add("D156","TTP","E07","TTP: 肺聴診(感染合併時)",{"clear":0.40,"crackles":0.35,"wheezes":0.10,"decreased_absent":0.15})

# D20 副鼻腔炎 → L45 (髄膜炎合併)
add("D20","sinusitis","L45","副鼻腔炎: CSF(髄膜炎合併時)",{"not_done":0.50,"normal":0.25,"viral_pattern":0.03,"bacterial_pattern":0.18,"HSV_PCR_positive":0.00,"tb_fungal_pattern":0.04})

s2["total_edges"] = len(s2["edges"])
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "w", encoding="utf-8") as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "w", encoding="utf-8") as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']}")
