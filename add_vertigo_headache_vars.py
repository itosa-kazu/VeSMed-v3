#!/usr/bin/env python3
"""
Add S59 めまいの性状 + S60 頭痛のパターン.
全面的に設計：今後の疾患追加でも再利用可能なstate設計。
三位一体。
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
added = 0

def add(did, dname, to, reason, cpt):
    global added
    if (did,to) in existing: return
    if to not in n: return
    s2["edges"].append({"from":did,"to":to,"from_name":dname,"to_name":to,"reason":reason})
    existing.add((did,to))
    n[to]["parent_effects"][did] = cpt
    added += 1

# ============================================================
# S59 めまいの性状
# ============================================================
s1["variables"].append({
    "id": "S59", "name": "vertigo_pattern", "name_ja": "めまいの性状",
    "category": "symptom",
    "states": ["absent", "positional_brief", "continuous_rotatory",
               "episodic_with_hearing", "non_rotatory_disequilibrium"],
    "note": "positional_brief: BPPV(頭位変換で誘発, <1分)。"
            "continuous_rotatory: 前庭神経炎(持続性回転性, 数日)。"
            "episodic_with_hearing: メニエール(反復性回転性+聴力低下, 20分~数時間)。"
            "non_rotatory: ふらつき/不安定感(中枢性/薬剤性/起立性低血圧)"
})
n["S59"] = {
    "description": "めまいの性状",
    "leak": {"absent": 0.85, "positional_brief": 0.05,
             "continuous_rotatory": 0.03, "episodic_with_hearing": 0.02,
             "non_rotatory_disequilibrium": 0.05},
    "parent_effects": {}
}

# BPPV: positional_brief (定義的)
add("D293","BPPV","S59","BPPV: 頭位変換性めまい(定義的, <1分)",
    {"absent":0.03,"positional_brief":0.90,"continuous_rotatory":0.02,
     "episodic_with_hearing":0.02,"non_rotatory_disequilibrium":0.03})

# 前庭神経炎: continuous_rotatory
add("D292","vestibular_neuritis","S59","前庭神経炎: 持続性回転性めまい(定義的, 数日)",
    {"absent":0.03,"positional_brief":0.05,"continuous_rotatory":0.85,
     "episodic_with_hearing":0.02,"non_rotatory_disequilibrium":0.05})

# 脳梗塞/脳出血: non_rotatory or continuous
add("D138","stroke","S59","脳梗塞: めまい(後方循環で, 非回転性多い)",
    {"absent":0.40,"positional_brief":0.03,"continuous_rotatory":0.15,
     "episodic_with_hearing":0.02,"non_rotatory_disequilibrium":0.40})
add("D139","ICH","S59","脳出血: めまい(小脳出血で)",
    {"absent":0.40,"positional_brief":0.03,"continuous_rotatory":0.15,
     "episodic_with_hearing":0.02,"non_rotatory_disequilibrium":0.40})

# PSP: non_rotatory (姿勢反射障害)
add("D302","PSP","S59","PSP: ふらつき/不安定感(姿勢反射障害)",
    {"absent":0.15,"positional_brief":0.03,"continuous_rotatory":0.05,
     "episodic_with_hearing":0.02,"non_rotatory_disequilibrium":0.75})

# パーキンソン: non_rotatory
add("D303","PD","S59","PD: ふらつき(姿勢反射障害, 進行期)",
    {"absent":0.30,"positional_brief":0.03,"continuous_rotatory":0.05,
     "episodic_with_hearing":0.02,"non_rotatory_disequilibrium":0.60})

# DLB: non_rotatory
add("D304","DLB","S59","DLB: ふらつき/失神(自律神経障害)",
    {"absent":0.20,"positional_brief":0.05,"continuous_rotatory":0.05,
     "episodic_with_hearing":0.02,"non_rotatory_disequilibrium":0.68})

# ============================================================
# S60 頭痛のパターン
# ============================================================
s1["variables"].append({
    "id": "S60", "name": "headache_pattern", "name_ja": "頭痛のパターン",
    "category": "symptom",
    "states": ["absent", "bilateral_pressing", "unilateral_pulsating",
               "periorbital_stabbing", "thunderclap",
               "progressive_with_neuro", "electric_triggered"],
    "note": "bilateral_pressing: 緊張型頭痛。unilateral_pulsating: 片頭痛。"
            "periorbital_stabbing: 群発頭痛(激烈+自律神経症状)。"
            "thunderclap: SAH/CVST(突発worst-ever)。"
            "progressive_with_neuro: 脳腫瘍(進行性+局所神経症状)。"
            "electric_triggered: 三叉神経痛(電撃様+トリガー誘発)"
})
n["S60"] = {
    "description": "頭痛のパターン",
    "leak": {"absent": 0.70, "bilateral_pressing": 0.10,
             "unilateral_pulsating": 0.08, "periorbital_stabbing": 0.02,
             "thunderclap": 0.03, "progressive_with_neuro": 0.04,
             "electric_triggered": 0.03},
    "parent_effects": {}
}

# 緊張型頭痛: bilateral_pressing (定義的)
add("D296","TTH","S60","TTH: 両側圧迫感(定義的)",
    {"absent":0.03,"bilateral_pressing":0.90,"unilateral_pulsating":0.02,
     "periorbital_stabbing":0.01,"thunderclap":0.01,
     "progressive_with_neuro":0.01,"electric_triggered":0.02})

# 片頭痛: unilateral_pulsating (定義的)
add("D294","migraine","S60","片頭痛: 片側拍動性(定義的)",
    {"absent":0.03,"bilateral_pressing":0.10,"unilateral_pulsating":0.80,
     "periorbital_stabbing":0.02,"thunderclap":0.02,
     "progressive_with_neuro":0.01,"electric_triggered":0.02})

# 群発頭痛: periorbital_stabbing (定義的)
add("D295","cluster","S60","群発頭痛: 眼窩周囲激烈(定義的)",
    {"absent":0.02,"bilateral_pressing":0.03,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.85,"thunderclap":0.02,
     "progressive_with_neuro":0.01,"electric_triggered":0.02})

# 三叉神経痛: electric_triggered (定義的)
add("D297","TN","S60","三叉神経痛: 電撃様+トリガー(定義的)",
    {"absent":0.02,"bilateral_pressing":0.02,"unilateral_pulsating":0.03,
     "periorbital_stabbing":0.03,"thunderclap":0.02,
     "progressive_with_neuro":0.01,"electric_triggered":0.87})

# SAH: thunderclap (定義的)
add("D155","SAH","S60","SAH: thunderclap headache(定義的)",
    {"absent":0.05,"bilateral_pressing":0.03,"unilateral_pulsating":0.02,
     "periorbital_stabbing":0.02,"thunderclap":0.82,
     "progressive_with_neuro":0.03,"electric_triggered":0.03})

# CVST: thunderclap or progressive
add("D315","CVST","S60","CVST: thunderclap(30%)or進行性(60%)",
    {"absent":0.03,"bilateral_pressing":0.05,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.02,"thunderclap":0.30,
     "progressive_with_neuro":0.50,"electric_triggered":0.05})

# GBM: progressive_with_neuro
add("D311","GBM","S60","GBM: 進行性頭痛+局所神経症状(定義的)",
    {"absent":0.10,"bilateral_pressing":0.05,"unilateral_pulsating":0.03,
     "periorbital_stabbing":0.02,"thunderclap":0.02,
     "progressive_with_neuro":0.75,"electric_triggered":0.03})

# 髄膜腫: progressive_with_neuro
add("D312","meningioma","S60","髄膜腫: 進行性頭痛(40-60%)",
    {"absent":0.20,"bilateral_pressing":0.10,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.02,"thunderclap":0.02,
     "progressive_with_neuro":0.58,"electric_triggered":0.03})

# 転移性脳腫瘍: progressive_with_neuro
add("D313","brain_metastasis","S60","脳転移: 進行性頭痛(40-50%)",
    {"absent":0.20,"bilateral_pressing":0.08,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.02,"thunderclap":0.02,
     "progressive_with_neuro":0.60,"electric_triggered":0.03})

# 慢性SDH: progressive
add("D164","chronic_SDH","S60","慢性SDH: 進行性頭痛(90%)",
    {"absent":0.05,"bilateral_pressing":0.10,"unilateral_pulsating":0.03,
     "periorbital_stabbing":0.02,"thunderclap":0.02,
     "progressive_with_neuro":0.75,"electric_triggered":0.03})

# 高血圧緊急症: bilateral_pressing
add("D146","hypertensive_emergency","S60","高血圧緊急症: 両側圧迫性(60-70%)",
    {"absent":0.15,"bilateral_pressing":0.55,"unilateral_pulsating":0.10,
     "periorbital_stabbing":0.03,"thunderclap":0.10,
     "progressive_with_neuro":0.05,"electric_triggered":0.02})

# 髄膜炎: bilateral + progressive
add("D13","meningitis","S60","髄膜炎: びまん性頭痛(80%+)",
    {"absent":0.05,"bilateral_pressing":0.30,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.02,"thunderclap":0.15,
     "progressive_with_neuro":0.40,"electric_triggered":0.03})

# CO中毒: bilateral_pressing
add("D149","CO_poisoning","S60","CO中毒: 両側鈍痛(90%+)",
    {"absent":0.05,"bilateral_pressing":0.75,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.02,"thunderclap":0.03,
     "progressive_with_neuro":0.07,"electric_triggered":0.03})

# AVM出血: thunderclap
add("D309","AVM","S60","AVM出血: thunderclap(出血時)",
    {"absent":0.15,"bilateral_pressing":0.05,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.02,"thunderclap":0.60,
     "progressive_with_neuro":0.10,"electric_triggered":0.03})

# PRES: bilateral + progressive
add("D325","PRES","S60","PRES: 頭痛(50-60%, progressive)",
    {"absent":0.25,"bilateral_pressing":0.20,"unilateral_pulsating":0.05,
     "periorbital_stabbing":0.02,"thunderclap":0.08,
     "progressive_with_neuro":0.37,"electric_triggered":0.03})

# ============================================================
# Save + Trinity
# ============================================================
s2["total_edges"] = len(s2["edges"])
for fname, data in [("step1_fever_v2.7.json",s1),("step2_fever_edges_v4.json",s2),("step3_fever_cpts_v2.json",s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

edges_set = {(e["from"],e["to"]) for e in s2["edges"]}
enc = sum(1 for e in s2["edges"] if e["to"] in n and isinstance(n[e["to"]],dict) and e["from"] not in n[e["to"]].get("parent_effects",{}))
cne = sum(1 for vid,p in n.items() if isinstance(p,dict) for did in p.get("parent_effects",{}) if (did,vid) not in edges_set)
print(f"Added 2 variables + {added} edges. Total {s2['total_edges']}")
print(f"Trinity: EDGE_NO_CPT={enc}, CPT_NO_EDGE={cne}")
print(f"\nS59 parents: {len(n['S59']['parent_effects'])}")
print(f"S60 parents: {len(n['S60']['parent_effects'])}")
