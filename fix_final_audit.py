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

# D53 ブルセラ → L45 CSF, E16, E06, S02
add("D53","brucella","L45","ブルセラ: CSF(リンパ球優位)",{"not_done":0.30,"normal":0.15,"viral_pattern":0.40,"bacterial_pattern":0.10,"HSV_PCR_positive":0.00,"tb_fungal_pattern":0.05})
add("D53","brucella","E16","ブルセラ: 意識障害(神経ブルセラ)",{"normal":0.65,"confused":0.25,"obtunded":0.10})
add("D53","brucella","E06","ブルセラ: 項部硬直(髄膜炎)",{"absent":0.60,"present":0.40})
add("D53","brucella","S02","ブルセラ: 咽頭痛(20-30%)",{"absent":0.65,"present":0.35})

# D50 ニューモシスチス → L01 WBC
add("D50","PCP","L01","PCP: WBC(HIV+で低値, HIV-で上昇)",{"low_under_4000":0.20,"normal_4000_10000":0.30,"high_10000_20000":0.35,"very_high_over_20000":0.15})

# D21 肛門周囲膿瘍 → S09
add("D21","perianal_abscess","S09","肛門周囲膿瘍: 悪寒戦慄(菌血症)",{"absent":0.40,"present":0.60})

# D85 歯原性感染 → S04, T02, E02, E03, E16, E04, T01
add("D85","odontogenic","S04","歯原性感染: 呼吸困難(Ludwig angina→気道)",{"absent":0.50,"on_exertion":0.25,"at_rest":0.25})
add("D85","odontogenic","E02","歯原性感染: 頻脈(敗血症)",{"under_100":0.25,"100_120":0.45,"over_120":0.30})
add("D85","odontogenic","E03","歯原性感染: 血圧(通常正常)",{"normal_over_90":0.70,"hypotension_under_90":0.30})
add("D85","odontogenic","E16","歯原性感染: 意識(通常正常)",{"normal":0.75,"confused":0.18,"obtunded":0.07})
add("D85","odontogenic","E04","歯原性感染: 頻呼吸(気道閉塞時)",{"normal_under_20":0.40,"tachypnea_20_30":0.40,"severe_over_30":0.20})
add("D85","odontogenic","T01","歯原性感染: 急性",{"under_3d":0.40,"3d_to_1w":0.35,"1w_to_3w":0.20,"over_3w":0.05})
add("D85","odontogenic","T02","歯原性感染: 急性",{"sudden_hours":0.30,"gradual_days":0.70})

# D110 トキソプラズマ → L45, E06
add("D110","toxoplasmosis","L45","トキソプラズマ: CSF(リンパ球優位)",{"not_done":0.25,"normal":0.15,"viral_pattern":0.45,"bacterial_pattern":0.05,"HSV_PCR_positive":0.00,"tb_fungal_pattern":0.10})
add("D110","toxoplasmosis","E06","トキソプラズマ: 項部硬直(脳炎)",{"absent":0.60,"present":0.40})

# D121 心タンポナーデ → E16
add("D121","tamponade","E16","心タンポナーデ: 意識障害(ショック)",{"normal":0.35,"confused":0.35,"obtunded":0.30})

# D77 DVT/PE → T02
add("D77","DVT_PE","T02","PE: 発症(突発~亜急性)",{"sudden_hours":0.55,"gradual_days":0.45})

# D143 誤嚥性肺炎 → S13
add("D143","aspiration_pneumonia","S13","誤嚥性肺炎: 嘔吐(誤嚥のリスク因子)",{"absent":0.30,"present":0.70})

# D38 C.diff → E03, T02
add("D38","C_diff","E03","C.diff: 血圧(通常正常)",{"normal_over_90":0.70,"hypotension_under_90":0.30})
add("D38","C_diff","T02","C.diff: 発症(亜急性)",{"sudden_hours":0.15,"gradual_days":0.85})

# D202 シェーグレン → L01
add("D202","sjogren","L01","シェーグレン: WBC低下(リンパ球減少)",{"low_under_4000":0.30,"normal_4000_10000":0.45,"high_10000_20000":0.20,"very_high_over_20000":0.05})

# D208 ITP → S21 chest pain (ITP+ACS case)
add("D208","ITP","S21","ITP: 胸痛(冠動脈血栓合併時)",{"absent":0.80,"burning":0.02,"sharp":0.05,"pressure":0.10,"tearing":0.03})

# D14 IE → L11
add("D14","IE","L11","IE: 肝酵素(肝梗塞/うっ血肝)",{"normal":0.45,"mild_elevated":0.40,"very_high":0.15})

s2["total_edges"] = len(s2["edges"])
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "w", encoding="utf-8") as f:
    json.dump(s2, f, ensure_ascii=False, indent=2)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "w", encoding="utf-8") as f:
    json.dump(s3, f, ensure_ascii=False, indent=2)
print(f"Added {added} edges. Total: {s2['total_edges']}")
