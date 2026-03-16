#!/usr/bin/env python3
"""
Add L63 転移巣(CT/PET) as observable lab variable.
三位一体: step1 + step2 + step3.
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
# L63 転移巣(CT/PET所見)
# ============================================================
s1["variables"].append({
    "id": "L63", "name": "metastasis_imaging", "name_ja": "転移巣(CT/PET所見)",
    "category": "lab",
    "states": ["not_done", "absent", "lung", "bone", "liver", "brain", "multiple"],
    "note": "CT/PET等で確認された転移巣。肺転移→咳嗽/呼吸困難、骨転移→骨痛/高Ca、肝転移→肝酵素上昇、脳転移→神経症状"
})

n["L63"] = {
    "description": "転移巣(CT/PET所見)",
    "leak": {
        "not_done": 0.50, "absent": 0.45, "lung": 0.01, "bone": 0.01,
        "liver": 0.01, "brain": 0.005, "multiple": 0.005
    },
    "parent_effects": {}
}

# === 癌 → L63 (どの癌がどこに転移しやすいか) ===

# D289 前立腺癌: 骨転移(70-80%), 肺転移(15-20%), 肝(5-10%)
add("D289","prostate_cancer","L63","前立腺癌: 骨転移優位(70-80%)",
    {"not_done":0.10,"absent":0.10,"lung":0.05,"bone":0.45,"liver":0.03,"brain":0.02,"multiple":0.25})

# D277 肺腺癌: 脳(30-40%), 骨(30%), 肝(20%), 肺内(20%)
add("D277","lung_adenocarcinoma","L63","肺腺癌: 脳/骨/肝に多発転移(50-60%)",
    {"not_done":0.10,"absent":0.20,"lung":0.10,"bone":0.15,"liver":0.10,"brain":0.15,"multiple":0.20})

# D313 脳転移(定義的に脳転移あり)
add("D313","brain_metastasis","L63","脳転移: 脳転移(定義的)+原発巣",
    {"not_done":0.05,"absent":0.02,"lung":0.08,"bone":0.05,"liver":0.05,"brain":0.45,"multiple":0.30})

# D287 胆嚢癌: 肝転移(60-70%), 腹膜播種
add("D287","gallbladder_cancer","L63","胆嚢癌: 肝転移優位(60-70%)",
    {"not_done":0.10,"absent":0.15,"lung":0.05,"bone":0.03,"liver":0.45,"brain":0.02,"multiple":0.20})

# D288 精巣腫瘍: 肺転移(40-50%), 後腹膜リンパ節
add("D288","testicular_tumor","L63","精巣腫瘍: 肺転移(40-50%)",
    {"not_done":0.10,"absent":0.25,"lung":0.35,"bone":0.05,"liver":0.05,"brain":0.05,"multiple":0.15})

# D290 膀胱癌: 骨/肺/肝転移
add("D290","bladder_cancer","L63","膀胱癌: 骨/肺/肝転移(進行期30-40%)",
    {"not_done":0.10,"absent":0.35,"lung":0.10,"bone":0.15,"liver":0.10,"brain":0.03,"multiple":0.17})

# D278 悪性胸膜中皮腫: 局所進展優位、遠隔転移は晩期
add("D278","mesothelioma","L63","悪性中皮腫: 局所進展優位、遠隔転移は晩期(20-30%)",
    {"not_done":0.10,"absent":0.45,"lung":0.15,"bone":0.08,"liver":0.08,"brain":0.02,"multiple":0.12})

# D320 喉頭癌: 肺転移(10-15%), 頸部リンパ節転移が主
add("D320","laryngeal_cancer","L63","喉頭癌: 遠隔転移は稀(肺10-15%)",
    {"not_done":0.10,"absent":0.55,"lung":0.15,"bone":0.05,"liver":0.05,"brain":0.02,"multiple":0.08})

# D347 神経芽腫: 骨/骨髄/肝/皮膚
add("D347","neuroblastoma","L63","神経芽腫: 骨/骨髄/肝転移(Stage IV, 50-60%)",
    {"not_done":0.10,"absent":0.20,"lung":0.03,"bone":0.25,"liver":0.15,"brain":0.02,"multiple":0.25})

# D348 ウィルムス: 肺転移(15-20%)
add("D348","wilms_tumor","L63","ウィルムス: 肺転移(15-20%)",
    {"not_done":0.10,"absent":0.55,"lung":0.20,"bone":0.02,"liver":0.03,"brain":0.02,"multiple":0.08})

# ============================================================
# Save (三位一体)
# ============================================================
s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Trinity check
edges_set = {(e["from"],e["to"]) for e in s2["edges"]}
enc = sum(1 for e in s2["edges"] if e["to"] in n and e["from"] not in n[e["to"]].get("parent_effects",{}))
cne = sum(1 for vid,p in n.items() if isinstance(p,dict) for did in p.get("parent_effects",{}) if (did,vid) not in edges_set)

print(f"Added L63 variable + {added_edges} edges")
print(f"Total: {s2['total_edges']} edges")
print(f"Trinity: EDGE_NO_CPT={enc}, CPT_NO_EDGE={cne}")
