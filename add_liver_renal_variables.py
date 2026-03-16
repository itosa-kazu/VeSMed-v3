#!/usr/bin/env python3
"""
Add L66 肝障害パターン + L67 AKI原因分類 as observable lab variables.
L63方式: 観測可能な検査所見として実装。三位一体。
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
# L66 肝障害パターン
# 観測可能: AST/ALT/ALP/GGT/Bil/Albのパターンから判定
# ============================================================
s1["variables"].append({
    "id": "L66", "name": "liver_injury_pattern", "name_ja": "肝障害パターン",
    "category": "lab",
    "states": ["not_assessed", "normal", "hepatocellular", "cholestatic", "congestive"],
    "note": "肝細胞型:AST/ALT優位(肝炎/薬剤性/ショック肝)。胆汁うっ滞型:ALP/GGT/Bil優位(胆石/胆管癌/PBC)。うっ血型:軽度AST+Bil+低Alb(心不全/肝硬変)"
})
n["L66"] = {
    "description": "肝障害パターン",
    "leak": {"not_assessed": 0.40, "normal": 0.50, "hepatocellular": 0.04, "cholestatic": 0.03, "congestive": 0.03},
    "parent_effects": {}
}

# 肝細胞型
add("D100","acute_hep_A","L66","A型肝炎: 肝細胞型(AST/ALT著明上昇)",
    {"not_assessed":0.05,"normal":0.03,"hepatocellular":0.85,"cholestatic":0.05,"congestive":0.02})
add("D108","hep_B","L66","B型肝炎: 肝細胞型",
    {"not_assessed":0.05,"normal":0.03,"hepatocellular":0.82,"cholestatic":0.08,"congestive":0.02})
add("D169","AIH","L66","自己免疫性肝炎: 肝細胞型",
    {"not_assessed":0.05,"normal":0.03,"hepatocellular":0.80,"cholestatic":0.10,"congestive":0.02})
add("D170","alcoholic_hepatitis","L66","アルコール性肝炎: 肝細胞型(AST/ALT比>2)",
    {"not_assessed":0.05,"normal":0.05,"hepatocellular":0.78,"cholestatic":0.08,"congestive":0.04})
add("D166","APAP","L66","アセトアミノフェン中毒: 肝細胞型(AST著明上昇)",
    {"not_assessed":0.05,"normal":0.03,"hepatocellular":0.85,"cholestatic":0.05,"congestive":0.02})
add("D151","acute_liver_failure","L66","急性肝不全: 肝細胞型",
    {"not_assessed":0.03,"normal":0.02,"hepatocellular":0.85,"cholestatic":0.07,"congestive":0.03})
add("D322","HELLP","L66","HELLP: 肝細胞型(AST/ALT/LDH上昇)",
    {"not_assessed":0.05,"normal":0.05,"hepatocellular":0.75,"cholestatic":0.10,"congestive":0.05})
add("D282","mushroom_poison","L66","キノコ中毒: 肝細胞型(遅発性肝障害)",
    {"not_assessed":0.05,"normal":0.10,"hepatocellular":0.75,"cholestatic":0.05,"congestive":0.05})

# 胆汁うっ滞型
add("D273","CBD_stone","L66","総胆管結石: 胆汁うっ滞型(ALP/GGT/Bil上昇)",
    {"not_assessed":0.05,"normal":0.03,"hepatocellular":0.10,"cholestatic":0.80,"congestive":0.02})
add("D287","gallbladder_cancer","L66","胆嚢癌: 胆汁うっ滞型",
    {"not_assessed":0.05,"normal":0.05,"hepatocellular":0.10,"cholestatic":0.75,"congestive":0.05})
add("D231","cholangiocarcinoma","L66","胆管癌: 胆汁うっ滞型",
    {"not_assessed":0.05,"normal":0.03,"hepatocellular":0.07,"cholestatic":0.82,"congestive":0.03})
add("D230","pancreatic_cancer","L66","膵癌: 胆汁うっ滞型(閉塞性黄疸)",
    {"not_assessed":0.05,"normal":0.10,"hepatocellular":0.05,"cholestatic":0.75,"congestive":0.05})
add("D250","PBC","L66","PBC: 胆汁うっ滞型(ALP/GGT優位)",
    {"not_assessed":0.05,"normal":0.03,"hepatocellular":0.08,"cholestatic":0.82,"congestive":0.02})
add("D94","IgG4_RD","L66","IgG4: 胆汁うっ滞型(硬化性胆管炎)",
    {"not_assessed":0.05,"normal":0.15,"hepatocellular":0.10,"cholestatic":0.65,"congestive":0.05})

# うっ血型
add("D251","decompensated_cirrhosis","L66","非代償性肝硬変: うっ血型(低Alb+Bil上昇)",
    {"not_assessed":0.05,"normal":0.05,"hepatocellular":0.15,"cholestatic":0.10,"congestive":0.65})
add("D344","constrictive_pericarditis","L66","収縮性心膜炎: うっ血肝(右心不全→肝うっ血)",
    {"not_assessed":0.05,"normal":0.15,"hepatocellular":0.10,"cholestatic":0.10,"congestive":0.60})
add("D120","ADHF","L66","急性心不全: うっ血肝(30-40%)",
    {"not_assessed":0.10,"normal":0.30,"hepatocellular":0.10,"cholestatic":0.05,"congestive":0.45})
add("D345","sheehan","L66","Sheehan: ショック肝(肝細胞型寄り)",
    {"not_assessed":0.10,"normal":0.30,"hepatocellular":0.40,"cholestatic":0.05,"congestive":0.15})

# ============================================================
# L67 AKI原因分類
# 観測可能: BUN/Cr比 + 尿検査 + 尿Na + FENaから判定
# ============================================================
s1["variables"].append({
    "id": "L67", "name": "AKI_etiology", "name_ja": "AKI原因分類(検査所見)",
    "category": "lab",
    "states": ["not_assessed", "no_AKI", "prerenal", "renal", "postrenal"],
    "note": "腎前性:BUN/Cr比>20+FENa<1%+尿Na<20。腎性:FENa>2%+尿沈渣異常。腎後性:水腎症+尿閉"
})
n["L67"] = {
    "description": "AKI原因分類",
    "leak": {"not_assessed": 0.50, "no_AKI": 0.40, "prerenal": 0.04, "renal": 0.03, "postrenal": 0.03},
    "parent_effects": {}
}

# 腎前性AKI
add("D140","DKA","L67","DKA: 腎前性AKI(脱水, 30-40%)",
    {"not_assessed":0.10,"no_AKI":0.30,"prerenal":0.45,"renal":0.10,"postrenal":0.05})
add("D141","HHS","L67","HHS: 腎前性AKI(重度脱水, 50-60%)",
    {"not_assessed":0.10,"no_AKI":0.15,"prerenal":0.60,"renal":0.10,"postrenal":0.05})
add("D174","AAA_rupture","L67","AAA破裂: 腎前性AKI(出血性ショック, 30-40%)",
    {"not_assessed":0.10,"no_AKI":0.30,"prerenal":0.45,"renal":0.10,"postrenal":0.05})
add("D332","hypopituitarism","L67","下垂体機能低下: 腎前性AKI(副腎不全→低血圧, 15-20%)",
    {"not_assessed":0.15,"no_AKI":0.50,"prerenal":0.25,"renal":0.05,"postrenal":0.05})
add("D345","sheehan","L67","Sheehan: 腎前性AKI(副腎クリーゼ, 20-30%)",
    {"not_assessed":0.10,"no_AKI":0.40,"prerenal":0.35,"renal":0.10,"postrenal":0.05})
add("D78","heatstroke_severe","L67","熱中症: 腎前性→腎性AKI(横紋筋融解合併)",
    {"not_assessed":0.10,"no_AKI":0.20,"prerenal":0.30,"renal":0.35,"postrenal":0.05})

# 腎性AKI
add("D153","rhabdomyolysis","L67","横紋筋融解: 腎性AKI(ミオグロビン腎症, 30-50%)",
    {"not_assessed":0.10,"no_AKI":0.25,"prerenal":0.10,"renal":0.50,"postrenal":0.05})
add("D168","RPGN","L67","RPGN: 腎性AKI(定義的)",
    {"not_assessed":0.05,"no_AKI":0.03,"prerenal":0.05,"renal":0.85,"postrenal":0.02})
add("D326","TLS","L67","TLS: 腎性AKI(尿酸結晶, 50-60%)",
    {"not_assessed":0.10,"no_AKI":0.15,"prerenal":0.10,"renal":0.60,"postrenal":0.05})
add("D162","HUS","L67","HUS: 腎性AKI(TMA, 70-80%)",
    {"not_assessed":0.05,"no_AKI":0.05,"prerenal":0.05,"renal":0.80,"postrenal":0.05})

# 腎後性AKI
add("D290","bladder_cancer","L67","膀胱癌: 腎後性AKI(尿路閉塞, 20-30%)",
    {"not_assessed":0.10,"no_AKI":0.40,"prerenal":0.05,"renal":0.05,"postrenal":0.40})
add("D289","prostate_cancer","L67","前立腺癌: 腎後性AKI(尿路閉塞, 20-30%)",
    {"not_assessed":0.10,"no_AKI":0.35,"prerenal":0.05,"renal":0.05,"postrenal":0.45})
add("D336","ADPKD","L67","ADPKD: 腎性AKI(嚢胞→腎実質破壊)",
    {"not_assessed":0.10,"no_AKI":0.15,"prerenal":0.05,"renal":0.65,"postrenal":0.05})

# ============================================================
# Save + Trinity check
# ============================================================
s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

edges_set = {(e["from"],e["to"]) for e in s2["edges"]}
enc = sum(1 for e in s2["edges"] if e["to"] in n and isinstance(n[e["to"]],dict) and e["from"] not in n[e["to"]].get("parent_effects",{}))
cne = sum(1 for vid,p in n.items() if isinstance(p,dict) for did in p.get("parent_effects",{}) if (did,vid) not in edges_set)
print(f"Added 2 variables + {added_edges} edges")
print(f"Total: {s2['total_edges']} edges")
print(f"Trinity: EDGE_NO_CPT={enc}, CPT_NO_EDGE={cne}")
