#!/usr/bin/env python3
"""
Add new variables batch 2 - targeting Top-3 failures.
三位一体: step1 + step2 + step3 同時更新.
"""
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
added_vars = 0; added_edges = 0

def add_var(vid, name, name_ja, category, states, note=""):
    global added_vars
    if any(v["id"]==vid for v in s1["variables"]): return
    s1["variables"].append({"id":vid,"name":name,"name_ja":name_ja,
        "category":category,"states":states,"note":note})
    added_vars += 1

def add_noisy(vid, desc, leak):
    n[vid] = {"description":desc, "leak":leak, "parent_effects":{}}

def add(did, dname, to, reason, cpt):
    global added_edges
    if (did,to) in existing: return
    if to not in n: return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt
    added_edges += 1

# ============================================================
# S55 嗄声 (Hoarseness)
# D320喉頭癌(3件全滅), D128喉頭蓋炎, D320甲状腺疾患
# ============================================================
add_var("S55","hoarseness","嗄声","symptom",
    ["absent","present"],
    "喉頭癌で90%+。甲状腺疾患/喉頭蓋炎/GERD/声帯麻痺でも")
add_noisy("S55","嗄声",{"absent":0.92,"present":0.08})

add("D320","laryngeal_cancer","S55","喉頭癌: 嗄声(90%+, 最も特徴的)",{"absent":0.05,"present":0.95})
add("D128","epiglottitis","S55","喉頭蓋炎: 嗄声(muffled voice, 50-60%)",{"absent":0.35,"present":0.65})
add("D254","croup","S55","クループ: 嗄声(犬吠様咳嗽, 70-80%)",{"absent":0.15,"present":0.85})

# ============================================================
# L61 腫瘍マーカー (Tumor Markers - PSA/AFP/CEA)
# D289前立腺癌(2件), D288精巣腫瘍(2件), D287胆嚢癌(3件)
# ============================================================
add_var("L61","tumor_markers","腫瘍マーカー(PSA/AFP/CEA等)","lab",
    ["not_done","normal","elevated"],
    "PSA:前立腺癌, AFP:肝癌/精巣腫瘍, CEA:大腸癌/胆道癌, CA19-9:膵胆道癌")
add_noisy("L61","腫瘍マーカー",{"not_done":0.65,"normal":0.30,"elevated":0.05})

add("D289","prostate_cancer","L61","前立腺癌: PSA上昇(80%+)",{"not_done":0.10,"normal":0.05,"elevated":0.85})
add("D288","testicular_tumor","L61","精巣腫瘍: AFP/β-hCG/LDH上昇(70-80%)",{"not_done":0.10,"normal":0.10,"elevated":0.80})
add("D287","gallbladder_cancer","L61","胆嚢癌: CEA/CA19-9上昇(60-70%)",{"not_done":0.10,"normal":0.20,"elevated":0.70})
add("D277","lung_adenocarcinoma","L61","肺腺癌: CEA上昇(40-50%)",{"not_done":0.15,"normal":0.30,"elevated":0.55})
add("D313","brain_metastasis","L61","脳転移: 原発巣マーカー上昇(50-60%)",{"not_done":0.15,"normal":0.25,"elevated":0.60})
add("D278","mesothelioma","L61","悪性中皮腫: メソテリン上昇(40-50%)",{"not_done":0.20,"normal":0.30,"elevated":0.50})
add("D347","neuroblastoma","L61","神経芽腫: NSE上昇(70-80%)",{"not_done":0.10,"normal":0.10,"elevated":0.80})

# ============================================================
# E42 四肢末梢循環所見
# D335 PAD(3件全滅), D285減圧症
# ============================================================
add_var("E42","peripheral_circulation","四肢末梢循環所見","sign",
    ["normal","pallor_cold","cyanosis","gangrene"],
    "蒼白冷感:急性虚血/PAD。チアノーゼ:低酸素。壊疽:重症PAD/DM足")
add_noisy("E42","四肢末梢循環所見",
    {"normal":0.85,"pallor_cold":0.08,"cyanosis":0.04,"gangrene":0.03})

add("D335","PAD","E42","PAD: 蒼白冷感→壊疽(進行, 60-70%)",{"normal":0.15,"pallor_cold":0.35,"cyanosis":0.10,"gangrene":0.40})
add("D285","DCS","E42","減圧症: 蒼白/チアノーゼ(皮膚型, 20-30%)",{"normal":0.55,"pallor_cold":0.25,"cyanosis":0.15,"gangrene":0.05})
add("D172","gas_gangrene","E42","ガス壊疽: 壊疽(定義的)",{"normal":0.05,"pallor_cold":0.10,"cyanosis":0.15,"gangrene":0.70})

# ============================================================
# L62 骨盤/婦人科超音波
# D276卵巣捻転(3件全滅), D291子宮外妊娠(3件)
# ============================================================
add_var("L62","pelvic_US","骨盤超音波(経腹/経膣)","lab",
    ["not_done","normal","adnexal_mass","free_fluid","uterine_abnormal"],
    "卵巣腫瘤:卵巣捻転/嚢腫。ダグラス窩液体:子宮外妊娠破裂。子宮異常:筋腫等")
add_noisy("L62","骨盤超音波",
    {"not_done":0.55,"normal":0.35,"adnexal_mass":0.04,"free_fluid":0.04,"uterine_abnormal":0.02})

add("D276","ovarian_torsion","L62","卵巣捻転: 付属器腫瘤(90%+)",{"not_done":0.05,"normal":0.03,"adnexal_mass":0.85,"free_fluid":0.05,"uterine_abnormal":0.02})
add("D291","ectopic_pregnancy","L62","子宮外妊娠: 子宮外腫瘤+ダグラス窩液体(70-80%)",{"not_done":0.05,"normal":0.05,"adnexal_mass":0.30,"free_fluid":0.55,"uterine_abnormal":0.05})

# ============================================================
# S56 間欠性跛行 (Intermittent Claudication)
# D335 PAD(3件)
# ============================================================
add_var("S56","intermittent_claudication","間欠性跛行","symptom",
    ["absent","present"],
    "PADの典型症状。歩行→下肢痛→休息で改善。Fontaine II度")
add_noisy("S56","間欠性跛行",{"absent":0.95,"present":0.05})

add("D335","PAD","S56","PAD: 間欠性跛行(定義的症状, 70-80%)",{"absent":0.15,"present":0.85})

# ============================================================
# E43 opening snap / 拡張期雑音
# D340 僧帽弁狭窄(3件全滅)
# ============================================================
add_var("E43","diastolic_murmur","拡張期雑音/opening snap","sign",
    ["absent","present"],
    "僧帽弁狭窄: opening snap+拡張期ランブル。大動脈弁逆流: 拡張期逓減性雑音")
add_noisy("E43","拡張期雑音",{"absent":0.93,"present":0.07})

add("D340","mitral_stenosis","E43","僧帽弁狭窄: 拡張期雑音+opening snap(定義的)",{"absent":0.05,"present":0.95})
add("D350","marfan","E43","マルファン: 大動脈弁逆流→拡張期雑音(40-50%)",{"absent":0.40,"present":0.60})

# ============================================================
# S57 乳汁分泌不全/無月経 (Lactation failure / Amenorrhea)
# D345 Sheehan(3件全滅)
# ============================================================
add_var("S57","amenorrhea_agalactia","無月経/乳汁分泌不全","symptom",
    ["absent","present"],
    "Sheehan症候群: 産後乳汁分泌不全+無月経が特徴的初発症状")
add_noisy("S57","無月経/乳汁分泌不全",{"absent":0.95,"present":0.05})

add("D345","sheehan","S57","Sheehan: 無月経+乳汁分泌不全(定義的, 90%+)",{"absent":0.05,"present":0.95})
add("D332","hypopituitarism","S57","下垂体機能低下: 無月経(ゴナドトロピン低下, 60-70%)",{"absent":0.25,"present":0.75})

# ============================================================
# Save (三位一体)
# ============================================================
s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 三位一体チェック
edges_set = {(e["from"],e["to"]) for e in s2["edges"]}
enc = sum(1 for e in s2["edges"] if e["to"] in n and e["from"] not in n[e["to"]].get("parent_effects",{}))
cne = sum(1 for vid,p in n.items() if isinstance(p,dict) for did in p.get("parent_effects",{}) if (did,vid) not in edges_set)
print(f"Added {added_vars} variables, {added_edges} edges")
print(f"Total: {len([v for v in s1['variables'] if v['category']=='disease'])} diseases, {s2['total_edges']} edges")
print(f"三位一体: EDGE_NO_CPT={enc}, CPT_NO_EDGE={cne}")
