#!/usr/bin/env python3
"""
Add DIC score and heart failure grade as observable lab/sign variables.
L63方式: 中間層ではなく観測可能な検査所見として実装。
三位一体: step1 + step2 + step3 同時更新。
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
added_edges = 0

def add(did, dname, to, reason, cpt):
    global added_edges
    if (did,to) in existing: return
    if to not in n: return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt
    added_edges += 1

# ============================================================
# L64 DICスコア (ISTH overt DIC score)
# 観測可能: PLT + PT + D-dimer + フィブリノゲンから算出
# ============================================================
s1["variables"].append({
    "id": "L64", "name": "DIC_score", "name_ja": "DICスコア(ISTH基準)",
    "category": "lab",
    "states": ["not_done", "normal", "pre_DIC", "overt_DIC"],
    "note": "ISTH overt DIC score: PLT+PT+D-dimer+フィブリノゲンから算出。≥5=overt DIC"
})
n["L64"] = {
    "description": "DICスコア(ISTH基準)",
    "leak": {"not_done": 0.60, "normal": 0.35, "pre_DIC": 0.03, "overt_DIC": 0.02},
    "parent_effects": {}
}

# DIC自体
add("D152","DIC","L64","DIC: overt DIC(定義的)",
    {"not_done":0.05,"normal":0.03,"pre_DIC":0.12,"overt_DIC":0.80})
# DICを起こしやすい疾患
add("D322","HELLP","L64","HELLP: DIC合併(20-40%)",
    {"not_done":0.10,"normal":0.30,"pre_DIC":0.30,"overt_DIC":0.30})
add("D323","placental_abruption","L64","胎盤早期剥離: DIC(10-30%)",
    {"not_done":0.10,"normal":0.40,"pre_DIC":0.25,"overt_DIC":0.25})
add("D01","sepsis","L64","敗血症: DIC合併(30-40%)",
    {"not_done":0.10,"normal":0.30,"pre_DIC":0.30,"overt_DIC":0.30})
add("D192","APL","L64","APL: DIC(80%+)",
    {"not_done":0.05,"normal":0.05,"pre_DIC":0.10,"overt_DIC":0.80})
add("D78","heatstroke_severe","L64","熱中症: DIC合併(30-40%)",
    {"not_done":0.10,"normal":0.30,"pre_DIC":0.30,"overt_DIC":0.30})
add("D284","mamushi","L64","マムシ咬傷: DIC(10-20%)",
    {"not_done":0.15,"normal":0.45,"pre_DIC":0.25,"overt_DIC":0.15})
add("D156","TTP","L64","TTP: DICスコアは通常正常(PT/フィブリノゲン正常)",
    {"not_done":0.10,"normal":0.70,"pre_DIC":0.15,"overt_DIC":0.05})
add("D162","HUS","L64","HUS: DICスコアは通常正常~軽度",
    {"not_done":0.10,"normal":0.55,"pre_DIC":0.25,"overt_DIC":0.10})
add("D68","acute_leukemia","L64","急性白血病: DIC合併(15-20%)",
    {"not_done":0.10,"normal":0.45,"pre_DIC":0.25,"overt_DIC":0.20})

# ============================================================
# L65 心不全グレード (NYHA/Killip/臨床評価)
# 観測可能: BNP + 胸部X線 + 身体所見(ラ音/浮腫/JVD)から判定
# ============================================================
s1["variables"].append({
    "id": "L65", "name": "heart_failure_grade", "name_ja": "心不全グレード(臨床評価)",
    "category": "lab",
    "states": ["not_assessed", "absent", "mild_NYHA2", "severe_NYHA3_4"],
    "note": "臨床評価: BNP+CXR+ラ音+浮腫+JVDから総合判定。NYHA/Killip分類"
})
n["L65"] = {
    "description": "心不全グレード(臨床評価)",
    "leak": {"not_assessed": 0.40, "absent": 0.50, "mild_NYHA2": 0.06, "severe_NYHA3_4": 0.04},
    "parent_effects": {}
}

# 心不全を直接起こす疾患
add("D120","ADHF","L65","急性心不全: severe(定義的)",
    {"not_assessed":0.03,"absent":0.02,"mild_NYHA2":0.15,"severe_NYHA3_4":0.80})
add("D327","aortic_stenosis","L65","AS: 心不全(三徴の一つ, 50-60%)",
    {"not_assessed":0.05,"absent":0.20,"mild_NYHA2":0.35,"severe_NYHA3_4":0.40})
add("D340","mitral_stenosis","L65","MS: 心不全(肺うっ血, 60-70%)",
    {"not_assessed":0.05,"absent":0.15,"mild_NYHA2":0.35,"severe_NYHA3_4":0.45})
add("D346","HCM","L65","HCM: 心不全(拡張障害, 40-50%)",
    {"not_assessed":0.05,"absent":0.30,"mild_NYHA2":0.35,"severe_NYHA3_4":0.30})
add("D343","takotsubo","L65","たこつぼ: 心不全(EF低下, 50-60%)",
    {"not_assessed":0.05,"absent":0.20,"mild_NYHA2":0.30,"severe_NYHA3_4":0.45})
add("D344","constrictive_pericarditis","L65","収縮性心膜炎: 右心不全(定義的, 80%+)",
    {"not_assessed":0.05,"absent":0.05,"mild_NYHA2":0.25,"severe_NYHA3_4":0.65})
add("D116","acute_myocarditis","L65","急性心筋炎: 心不全(50-60%)",
    {"not_assessed":0.05,"absent":0.20,"mild_NYHA2":0.30,"severe_NYHA3_4":0.45})
add("D124","cardiac_tamponade","L65","心タンポナーデ: 心不全様(閉塞性, 80%+)",
    {"not_assessed":0.05,"absent":0.05,"mild_NYHA2":0.15,"severe_NYHA3_4":0.75})
add("D131","ACS","L65","ACS: 心不全(Killip II-IV, 30-40%)",
    {"not_assessed":0.05,"absent":0.40,"mild_NYHA2":0.25,"severe_NYHA3_4":0.30})
add("D318","CTEPH","L65","CTEPH: 右心不全(60-70%)",
    {"not_assessed":0.05,"absent":0.15,"mild_NYHA2":0.30,"severe_NYHA3_4":0.50})
add("D350","marfan","L65","マルファン: 心不全(大動脈弁逆流, 30-40%)",
    {"not_assessed":0.10,"absent":0.35,"mild_NYHA2":0.25,"severe_NYHA3_4":0.30})
# 心不全を起こさない疾患(鑑別用)
add("D134","acute_pericarditis","L65","急性心膜炎: 心不全は通常なし(心嚢液少量)",
    {"not_assessed":0.10,"absent":0.70,"mild_NYHA2":0.12,"severe_NYHA3_4":0.08})
add("D125","arrhythmia","L65","不整脈: 心不全(頻脈性で, 20-30%)",
    {"not_assessed":0.05,"absent":0.45,"mild_NYHA2":0.25,"severe_NYHA3_4":0.25})

# ============================================================
# Save + Trinity check
# ============================================================
s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

edges_set = {(e["from"],e["to"]) for e in s2["edges"]}
enc = sum(1 for e in s2["edges"] if e["to"] in n and e["from"] not in n[e["to"]].get("parent_effects",{}))
cne = sum(1 for vid,p in n.items() if isinstance(p,dict) for did in p.get("parent_effects",{}) if (did,vid) not in edges_set)
print(f"Added 2 variables + {added_edges} edges")
print(f"Total: {s2['total_edges']} edges")
print(f"Trinity: EDGE_NO_CPT={enc}, CPT_NO_EDGE={cne}")
