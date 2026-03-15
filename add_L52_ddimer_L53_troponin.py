#!/usr/bin/env python3
"""Add L52 D-dimer and L53 Troponin.

L52 D-dimer:
  大動脈解離で著高(>20が多い), PE/DVTで上昇, ACSでは通常正常~軽度
  DIC/敗血症でも上昇。非特異的だが陰性で除外に使える
  Parent: D132解離, D77 PE, D24 TSS, D57壊死性筋膜炎, D15マラリア(DIC)

L53 Troponin:
  ACSの核心マーカー。心筋壊死を反映。
  ACS: 著高(>1ng/mL), 心筋炎: 上昇, PE: 軽度上昇, 敗血症: 軽度上昇
  Parent: D131 ACS, D116心筋炎, D77 PE, D124タンポナーデ, D120心不全
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

# === step1: add variables ===
s1["variables"].append({
    "id": "L52", "name": "D_dimer", "name_ja": "Dダイマー",
    "category": "lab",
    "states": ["not_done", "normal", "mildly_elevated", "very_high"],
    "note": "凝固線溶マーカー。正常<0.5ug/mL。PE/DVT/解離/DICで上昇。"
           "解離では著高(>20)。陰性でPE/解離除外に有用"
})
s1["variables"].append({
    "id": "L53", "name": "troponin", "name_ja": "トロポニン(I/T)",
    "category": "lab",
    "states": ["not_done", "normal", "mildly_elevated", "very_high"],
    "note": "心筋壊死マーカー。正常<0.04ng/mL。ACS: 著高(>1)。"
           "心筋炎/PE/敗血症で軽度上昇。大動脈解離の冠動脈巻込みでも上昇"
})

# === step2+step3: edges + CPTs ===

# L52 D-dimer
l52_edges = {
    "D132": ("大動脈解離: D-dimer著高(>20ug/mLが多い, 感度97%)",
             {"not_done": 0.10, "normal": 0.03, "mildly_elevated": 0.17, "very_high": 0.70}),
    "D77":  ("PE/DVT: D-dimer上昇(感度95%+, 特異度低い)",
             {"not_done": 0.15, "normal": 0.05, "mildly_elevated": 0.40, "very_high": 0.40}),
    "D24":  ("TSS/敗血症: DICでD-dimer上昇",
             {"not_done": 0.20, "normal": 0.10, "mildly_elevated": 0.35, "very_high": 0.35}),
    "D57":  ("壊死性筋膜炎: DICでD-dimer上昇",
             {"not_done": 0.20, "normal": 0.10, "mildly_elevated": 0.35, "very_high": 0.35}),
    "D15":  ("マラリア: DICでD-dimer上昇",
             {"not_done": 0.25, "normal": 0.15, "mildly_elevated": 0.35, "very_high": 0.25}),
    "D131": ("ACS: D-dimer通常正常~軽度上昇",
             {"not_done": 0.25, "normal": 0.40, "mildly_elevated": 0.30, "very_high": 0.05}),
    "D107": ("HLH: DICでD-dimer上昇",
             {"not_done": 0.20, "normal": 0.10, "mildly_elevated": 0.30, "very_high": 0.40}),
}
n["L52"] = {
    "description": "Dダイマー。PE/解離/DICで上昇。陰性でPE/解離除外",
    "leak": {"not_done": 0.70, "normal": 0.25, "mildly_elevated": 0.04, "very_high": 0.01},
    "parent_effects": {}
}
for did, (reason, cpt) in l52_edges.items():
    s2["edges"].append({"from": did, "to": "L52", "from_name": did, "to_name": "L52", "reason": reason})
    n["L52"]["parent_effects"][did] = cpt

# L53 Troponin
l53_edges = {
    "D131": ("ACS: トロポニン著高(>1ng/mL, 心筋壊死の核心マーカー)",
             {"not_done": 0.05, "normal": 0.03, "mildly_elevated": 0.17, "very_high": 0.75}),
    "D116": ("心筋炎: トロポニン上昇(>90%, 心筋障害)",
             {"not_done": 0.10, "normal": 0.05, "mildly_elevated": 0.30, "very_high": 0.55}),
    "D77":  ("PE: トロポニン軽度上昇(右心負荷, 30-50%)",
             {"not_done": 0.20, "normal": 0.35, "mildly_elevated": 0.35, "very_high": 0.10}),
    "D124": ("心タンポナーデ: トロポニン軽度上昇(心筋圧迫)",
             {"not_done": 0.20, "normal": 0.30, "mildly_elevated": 0.40, "very_high": 0.10}),
    "D120": ("心不全: トロポニン軽度上昇(心筋ストレス, 40-60%)",
             {"not_done": 0.15, "normal": 0.30, "mildly_elevated": 0.40, "very_high": 0.15}),
    "D132": ("大動脈解離: トロポニン上昇(冠動脈巻込みなら著高, なければ正常~軽度)",
             {"not_done": 0.15, "normal": 0.35, "mildly_elevated": 0.30, "very_high": 0.20}),
    "D125": ("不整脈: トロポニン軽度上昇(頻脈性心筋障害)",
             {"not_done": 0.25, "normal": 0.35, "mildly_elevated": 0.30, "very_high": 0.10}),
}
n["L53"] = {
    "description": "トロポニン。ACS/心筋炎で著高。PE/タンポナーデで軽度上昇",
    "leak": {"not_done": 0.65, "normal": 0.30, "mildly_elevated": 0.04, "very_high": 0.01},
    "parent_effects": {}
}
for did, (reason, cpt) in l53_edges.items():
    s2["edges"].append({"from": did, "to": "L53", "from_name": did, "to_name": "L53", "reason": reason})
    n["L53"]["parent_effects"][did] = cpt

s2["total_edges"] = len(s2["edges"])

# === IDF check ===
import math
n_diseases = 132
for vid, parents in [("L52", l52_edges), ("L53", l53_edges)]:
    np = len(parents)
    idf = math.log(n_diseases / np) / math.log(n_diseases)
    print(f"{vid}: {np} parents, IDF={idf:.3f}")

# === Save ===
for fname, data in [("step1_fever_v2.7.json", s1), ("step2_fever_edges_v4.json", s2), ("step3_fever_cpts_v2.json", s3)]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal: {s2['total_edges']} edges")
