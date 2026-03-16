#!/usr/bin/env python3
"""
Add 8 new variables + fix R15(妊娠) noisy_or.
E39 心エコー所見, E40 ECG所見, L57 ADAMTS13, L58 IGF-1,
S54 視野障害, L59 髄液開放圧, L60 尿中VMA/HVA, E41 ABI
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
added_vars = 0
added_edges = 0

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
# E39 心エコー所見
# ============================================================
add_var("E39","echocardiography","心エコー所見","sign",
    ["not_done","normal","wall_motion_abnormal","valvular_abnormal",
     "pericardial_effusion","LVH","dilated_chamber"],
    "心エコー: 壁運動異常(ACS/心筋炎/たこつぼ)/弁膜症/心嚢液/LVH/腔拡大")
add_noisy("E39","心エコー所見",
    {"not_done":0.30,"normal":0.50,"wall_motion_abnormal":0.05,
     "valvular_abnormal":0.05,"pericardial_effusion":0.03,"LVH":0.04,"dilated_chamber":0.03})

# 心エコー edges
add("D131","ACS","E39","ACS: 壁運動異常(80%+)",{"not_done":0.05,"normal":0.05,"wall_motion_abnormal":0.80,"valvular_abnormal":0.02,"pericardial_effusion":0.02,"LVH":0.03,"dilated_chamber":0.03})
add("D116","acute_myocarditis","E39","心筋炎: 壁運動異常+EF低下(60-70%)",{"not_done":0.05,"normal":0.10,"wall_motion_abnormal":0.65,"valvular_abnormal":0.03,"pericardial_effusion":0.10,"LVH":0.02,"dilated_chamber":0.05})
add("D134","acute_pericarditis","E39","心膜炎: 心嚢液(50-60%)",{"not_done":0.05,"normal":0.20,"wall_motion_abnormal":0.05,"valvular_abnormal":0.03,"pericardial_effusion":0.60,"LVH":0.03,"dilated_chamber":0.04})
add("D124","cardiac_tamponade","E39","心タンポナーデ: 心嚢液(定義的)",{"not_done":0.03,"normal":0.02,"wall_motion_abnormal":0.03,"valvular_abnormal":0.02,"pericardial_effusion":0.85,"LVH":0.02,"dilated_chamber":0.03})
add("D120","ADHF","E39","心不全: 腔拡大/壁運動異常(70-80%)",{"not_done":0.05,"normal":0.05,"wall_motion_abnormal":0.30,"valvular_abnormal":0.10,"pericardial_effusion":0.05,"LVH":0.15,"dilated_chamber":0.30})
add("D327","aortic_stenosis","E39","AS: 弁膜症(定義的)+LVH",{"not_done":0.05,"normal":0.03,"wall_motion_abnormal":0.05,"valvular_abnormal":0.55,"pericardial_effusion":0.02,"LVH":0.25,"dilated_chamber":0.05})
add("D340","mitral_stenosis","E39","MS: 弁膜症(定義的)",{"not_done":0.05,"normal":0.03,"wall_motion_abnormal":0.05,"valvular_abnormal":0.70,"pericardial_effusion":0.02,"LVH":0.05,"dilated_chamber":0.10})
add("D343","takotsubo","E39","たこつぼ: apical ballooning(定義的)",{"not_done":0.05,"normal":0.03,"wall_motion_abnormal":0.80,"valvular_abnormal":0.03,"pericardial_effusion":0.02,"LVH":0.03,"dilated_chamber":0.04})
add("D344","constrictive_pericarditis","E39","収縮性心膜炎: 心膜肥厚+中隔バウンス",{"not_done":0.05,"normal":0.05,"wall_motion_abnormal":0.10,"valvular_abnormal":0.05,"pericardial_effusion":0.15,"LVH":0.05,"dilated_chamber":0.55})
add("D346","HCM","E39","HCM: LVH+SAM(定義的)",{"not_done":0.05,"normal":0.03,"wall_motion_abnormal":0.05,"valvular_abnormal":0.10,"pericardial_effusion":0.02,"LVH":0.65,"dilated_chamber":0.10})
add("D150","takotsubo_old","E39","たこつぼ(旧): apical ballooning",{"not_done":0.05,"normal":0.03,"wall_motion_abnormal":0.80,"valvular_abnormal":0.03,"pericardial_effusion":0.02,"LVH":0.03,"dilated_chamber":0.04})
add("D345","sheehan","E39","Sheehan: 心嚢液(甲状腺低下, 30-40%)",{"not_done":0.10,"normal":0.35,"wall_motion_abnormal":0.10,"valvular_abnormal":0.03,"pericardial_effusion":0.35,"LVH":0.03,"dilated_chamber":0.04})

# ============================================================
# E40 ECG所見
# ============================================================
add_var("E40","ECG","ECG所見","sign",
    ["not_done","normal","ST_elevation","ST_depression","AF",
     "QT_prolongation","Brugada_pattern","RVH_strain","LVH_pattern"],
    "ECG: ST変化/AF/QT延長/Brugada/右室負荷/左室肥大")
add_noisy("E40","ECG所見",
    {"not_done":0.15,"normal":0.55,"ST_elevation":0.05,"ST_depression":0.05,
     "AF":0.05,"QT_prolongation":0.03,"Brugada_pattern":0.01,"RVH_strain":0.05,"LVH_pattern":0.06})

add("D131","ACS","E40","ACS: ST上昇/低下(80%+)",{"not_done":0.03,"normal":0.05,"ST_elevation":0.45,"ST_depression":0.35,"AF":0.03,"QT_prolongation":0.03,"Brugada_pattern":0.01,"RVH_strain":0.02,"LVH_pattern":0.03})
add("D134","acute_pericarditis","E40","心膜炎: びまん性ST上昇(80%+)",{"not_done":0.03,"normal":0.05,"ST_elevation":0.75,"ST_depression":0.03,"AF":0.05,"QT_prolongation":0.03,"Brugada_pattern":0.01,"RVH_strain":0.02,"LVH_pattern":0.03})
add("D116","acute_myocarditis","E40","心筋炎: ST-T変化(70-80%)",{"not_done":0.03,"normal":0.08,"ST_elevation":0.35,"ST_depression":0.25,"AF":0.10,"QT_prolongation":0.05,"Brugada_pattern":0.01,"RVH_strain":0.03,"LVH_pattern":0.10})
add("D341","brugada","E40","Brugada: coved型ST上昇V1-V3(定義的)",{"not_done":0.03,"normal":0.02,"ST_elevation":0.05,"ST_depression":0.02,"AF":0.03,"QT_prolongation":0.02,"Brugada_pattern":0.80,"RVH_strain":0.01,"LVH_pattern":0.02})
add("D342","LQTS","E40","LQTS: QT延長(定義的)",{"not_done":0.03,"normal":0.02,"ST_elevation":0.02,"ST_depression":0.05,"AF":0.03,"QT_prolongation":0.80,"Brugada_pattern":0.01,"RVH_strain":0.02,"LVH_pattern":0.02})
add("D343","takotsubo","E40","たこつぼ: ST上昇→T波逆転(80%+)",{"not_done":0.03,"normal":0.05,"ST_elevation":0.40,"ST_depression":0.30,"AF":0.05,"QT_prolongation":0.05,"Brugada_pattern":0.01,"RVH_strain":0.03,"LVH_pattern":0.08})
add("D327","aortic_stenosis","E40","AS: LVH pattern(60-70%)",{"not_done":0.05,"normal":0.10,"ST_elevation":0.03,"ST_depression":0.10,"AF":0.05,"QT_prolongation":0.03,"Brugada_pattern":0.01,"RVH_strain":0.03,"LVH_pattern":0.60})
add("D340","mitral_stenosis","E40","MS: AF(40-50%)+左房負荷",{"not_done":0.05,"normal":0.10,"ST_elevation":0.03,"ST_depression":0.05,"AF":0.55,"QT_prolongation":0.03,"Brugada_pattern":0.01,"RVH_strain":0.10,"LVH_pattern":0.08})
add("D346","HCM","E40","HCM: LVH+ST-T変化(80%+)",{"not_done":0.03,"normal":0.05,"ST_elevation":0.03,"ST_depression":0.20,"AF":0.05,"QT_prolongation":0.03,"Brugada_pattern":0.01,"RVH_strain":0.02,"LVH_pattern":0.58})
add("D125","arrhythmia","E40","不整脈: AF/SVT/VT(定義的)",{"not_done":0.03,"normal":0.05,"ST_elevation":0.03,"ST_depression":0.10,"AF":0.55,"QT_prolongation":0.05,"Brugada_pattern":0.02,"RVH_strain":0.07,"LVH_pattern":0.10})
add("D318","CTEPH","E40","CTEPH: 右室負荷(70-80%)",{"not_done":0.05,"normal":0.08,"ST_elevation":0.02,"ST_depression":0.05,"AF":0.05,"QT_prolongation":0.02,"Brugada_pattern":0.01,"RVH_strain":0.65,"LVH_pattern":0.07})

# ============================================================
# L57 ADAMTS13活性
# ============================================================
add_var("L57","ADAMTS13","ADAMTS13活性","lab",
    ["not_done","normal","low","very_low_under_10"],
    "TTP鑑別の決め手。<10%→TTP, 正常→HUS/DIC/HELLP")
add_noisy("L57","ADAMTS13活性",
    {"not_done":0.70,"normal":0.25,"low":0.03,"very_low_under_10":0.02})

add("D156","TTP","L57","TTP: ADAMTS13<10%(定義的)",{"not_done":0.10,"normal":0.03,"low":0.07,"very_low_under_10":0.80})
add("D162","HUS","L57","HUS: ADAMTS13正常(定義的鑑別)",{"not_done":0.15,"normal":0.70,"low":0.10,"very_low_under_10":0.05})
add("D152","DIC","L57","DIC: ADAMTS13正常~軽度低下",{"not_done":0.15,"normal":0.55,"low":0.25,"very_low_under_10":0.05})
add("D322","HELLP","L57","HELLP: ADAMTS13正常~軽度低下",{"not_done":0.15,"normal":0.50,"low":0.30,"very_low_under_10":0.05})

# ============================================================
# L58 IGF-1/GH
# ============================================================
add_var("L58","IGF1_GH","IGF-1/GH","lab",
    ["not_done","normal","elevated","low"],
    "先端巨大症でIGF-1/GH上昇、下垂体機能低下で低下")
add_noisy("L58","IGF-1/GH",
    {"not_done":0.75,"normal":0.20,"elevated":0.03,"low":0.02})

add("D333","acromegaly","L58","先端巨大症: IGF-1/GH上昇(定義的)",{"not_done":0.05,"normal":0.03,"elevated":0.90,"low":0.02})
add("D332","hypopituitarism","L58","下垂体機能低下: GH/IGF-1低下(50-60%)",{"not_done":0.15,"normal":0.20,"elevated":0.02,"low":0.63})

# ============================================================
# S54 視野障害
# ============================================================
add_var("S54","visual_field_defect","視野障害","symptom",
    ["absent","hemianopia","central_scotoma","visual_loss"],
    "両耳側半盲(下垂体腫瘍)/中心暗点(視神経炎)/視力消失(網膜剥離/CRAO)")
add_noisy("S54","視野障害",
    {"absent":0.90,"hemianopia":0.03,"central_scotoma":0.03,"visual_loss":0.04})

add("D333","acromegaly","S54","先端巨大症: 両耳側半盲(視交叉圧迫, 30-40%)",{"absent":0.50,"hemianopia":0.35,"central_scotoma":0.05,"visual_loss":0.10})
add("D332","hypopituitarism","S54","下垂体機能低下: 視野障害(腫瘍性, 20-30%)",{"absent":0.60,"hemianopia":0.25,"central_scotoma":0.05,"visual_loss":0.10})
add("D301","NMOSD","S54","NMOSD: 視神経炎→中心暗点/視力消失(70-80%)",{"absent":0.15,"hemianopia":0.05,"central_scotoma":0.30,"visual_loss":0.50})
add("D312","meningioma","S54","髄膜腫: 視野障害(鞍上部/蝶形骨, 20-30%)",{"absent":0.60,"hemianopia":0.20,"central_scotoma":0.05,"visual_loss":0.15})
add("D311","glioblastoma","S54","GBM: 視野障害(後頭葉, 15-20%)",{"absent":0.70,"hemianopia":0.15,"central_scotoma":0.05,"visual_loss":0.10})
add("D339","retinal_detachment","S54","網膜剥離: 視野欠損→視力消失(定義的)",{"absent":0.05,"hemianopia":0.10,"central_scotoma":0.10,"visual_loss":0.75})
add("D325","PRES","S54","PRES: 視力障害(30-40%)",{"absent":0.50,"hemianopia":0.10,"central_scotoma":0.10,"visual_loss":0.30})

# ============================================================
# L59 髄液開放圧
# ============================================================
add_var("L59","CSF_opening_pressure","髄液開放圧","lab",
    ["not_done","normal","elevated","very_high"],
    "正常<20cmH2O。髄膜炎/水頭症で上昇。NPHでは正常~軽度上昇")
add_noisy("L59","髄液開放圧",
    {"not_done":0.60,"normal":0.30,"elevated":0.07,"very_high":0.03})

add("D13","meningitis","L59","髄膜炎: 髄液圧上昇(80%+)",{"not_done":0.10,"normal":0.05,"elevated":0.40,"very_high":0.45})
add("D324","TB_meningitis","L59","結核性髄膜炎: 髄液圧上昇(70-80%)",{"not_done":0.10,"normal":0.10,"elevated":0.45,"very_high":0.35})
add("D314","acute_hydrocephalus","L59","急性水頭症: 髄液圧著明上昇(定義的)",{"not_done":0.10,"normal":0.03,"elevated":0.17,"very_high":0.70})
add("D315","CVST","L59","CVST: 髄液圧上昇(80%+)",{"not_done":0.10,"normal":0.05,"elevated":0.40,"very_high":0.45})
add("D200","NPH","L59","NPH: 髄液圧正常~軽度上昇(定義的)",{"not_done":0.10,"normal":0.55,"elevated":0.30,"very_high":0.05})
add("D109","cryptococcosis","L59","クリプトコッカス: 髄液圧上昇(60-70%)",{"not_done":0.10,"normal":0.15,"elevated":0.40,"very_high":0.35})

# ============================================================
# L60 尿中VMA/HVA
# ============================================================
add_var("L60","urine_VMA_HVA","尿中VMA/HVA","lab",
    ["not_done","normal","elevated"],
    "神経芽腫/褐色細胞腫のスクリーニング")
add_noisy("L60","尿中VMA/HVA",
    {"not_done":0.85,"normal":0.13,"elevated":0.02})

add("D347","neuroblastoma","L60","神経芽腫: VMA/HVA上昇(90%+)",{"not_done":0.05,"normal":0.03,"elevated":0.92})
add("D196","pheochromocytoma","L60","褐色細胞腫: VMA上昇(80%+)",{"not_done":0.05,"normal":0.08,"elevated":0.87})

# ============================================================
# E41 ABI (Ankle-Brachial Index)
# ============================================================
add_var("E41","ABI","ABI(足関節上腕血圧比)","sign",
    ["not_done","normal_over_0.9","low_under_0.9"],
    "PAD: ABI<0.9で診断。<0.4は重症")
add_noisy("E41","ABI",
    {"not_done":0.70,"normal_over_0.9":0.25,"low_under_0.9":0.05})

add("D335","PAD","E41","PAD: ABI<0.9(定義的)",{"not_done":0.05,"normal_over_0.9":0.05,"low_under_0.9":0.90})

# ============================================================
# R15 妊娠 → noisy_or修復
# ============================================================
if "R15" not in n:
    add_noisy("R15","妊娠",{"no":0.95,"yes":0.05})
    # 妊娠関連疾患
    add("D322","HELLP","R15","HELLP: 妊娠中(定義的)",{"no":0.02,"yes":0.98})
    add("D323","placental_abruption","R15","胎盤早期剥離: 妊娠中(定義的)",{"no":0.02,"yes":0.98})
    add("D291","ectopic_pregnancy","R15","子宮外妊娠: 妊娠(定義的)",{"no":0.02,"yes":0.98})
    add("D345","sheehan","R15","Sheehan: 産後(妊娠関連)",{"no":0.30,"yes":0.70})
    add("D325","PRES","R15","PRES: 子癇関連(30-40%)",{"no":0.55,"yes":0.45})
    # 非妊娠性疾患にも(negative direction)
    add("D156","TTP","R15","TTP: 非妊娠性(通常)",{"no":0.85,"yes":0.15})
    add("D152","DIC","R15","DIC: 非妊娠性(通常)",{"no":0.80,"yes":0.20})

# ============================================================
# Save
# ============================================================
s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {added_vars} new variables, {added_edges} new edges")
print(f"Total: {len([v for v in s1['variables'] if v['category']=='disease'])} diseases, {s2['total_edges']} edges")
print(f"\nNew variables: E39(心エコー), E40(ECG), L57(ADAMTS13), L58(IGF-1), S54(視野障害), L59(髄液圧), L60(VMA/HVA), E41(ABI)")
print(f"Fixed: R15(妊娠) noisy_or")
