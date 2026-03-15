#!/usr/bin/env python3
"""Add L48 (SPEP) and L49 (bone lesions) for myeloma and related diseases.

三位一体: step1(変数定義) + step2(辺) + step3(CPT) を同時追加。
9項目監査チェック付き。

L48: 血清蛋白電気泳動/免疫固定 (SPEP/Immunofixation)
  - not_done, normal, monoclonal_gammopathy, polyclonal_gammopathy
  - D114(骨髄腫), D67(リンパ腫), D97(キャッスルマン), D62(サルコイドーシス),
    D59(SLE), D45(CMV) = 6 parents → IDF健全

L49: 骨X線・骨病変 (Skeletal survey)
  - not_done, normal, lytic_lesions, compression_fracture
  - D114(骨髄腫), D67(リンパ腫), D31(椎体骨髄炎), D68(急性白血病),
    D69(腎細胞癌) = 5 parents → IDF健全
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# ===== step1: 変数定義 =====
s1["variables"].append({
    "id": "L48",
    "name": "SPEP_immunofixation",
    "name_ja": "血清蛋白電気泳動/免疫固定",
    "category": "lab",
    "states": ["not_done", "normal", "monoclonal_gammopathy", "polyclonal_gammopathy"],
    "note": "M蛋白検出。骨髄腫(monoclonal 90%+), リンパ腫(5-10%), "
           "サルコイドーシス/SLE/感染症(polyclonal高γ)"
})
s1["variables"].append({
    "id": "L49",
    "name": "skeletal_survey",
    "name_ja": "骨X線（骨溶解性病変）",
    "category": "lab",
    "states": ["not_done", "normal", "lytic_lesions", "compression_fracture"],
    "note": "骨髄腫(打ち抜き像80%), リンパ腫(骨浸潤), 椎体骨髄炎(圧迫骨折), "
           "急性白血病(骨浸潤), 腎細胞癌(転移性骨病変)"
})
print("step1: Added L48 (SPEP) and L49 (skeletal_survey)")

# ===== step2: 辺追加 =====
new_edges = [
    # L48: SPEP edges (6 parents)
    ("D114", "L48", "骨髄腫: M蛋白(monoclonal IgG/IgA/light chain, 90%以上)"),
    ("D67",  "L48", "悪性リンパ腫: M蛋白(monoclonal, 5-10%)"),
    ("D97",  "L48", "キャッスルマン病: ポリクローナル高γグロブリン血症"),
    ("D62",  "L48", "サルコイドーシス: ポリクローナル高γグロブリン血症(20-30%)"),
    ("D59",  "L48", "SLE: ポリクローナル高γグロブリン血症(30-50%)"),
    ("D45",  "L48", "CMV: ポリクローナル高γグロブリン血症(急性期)"),
    # L49: skeletal survey edges (5 parents)
    ("D114", "L49", "骨髄腫: 打ち抜き像/溶骨性病変(80%), 圧迫骨折(30%)"),
    ("D67",  "L49", "悪性リンパ腫: 骨浸潤/溶骨性病変(10-20%)"),
    ("D31",  "L49", "椎体骨髄炎: 椎体破壊/圧迫骨折"),
    ("D68",  "L49", "急性白血病: 骨浸潤/溶骨性病変(稀)"),
    ("D69",  "L49", "腎細胞癌: 転移性溶骨性病変"),
]

for frm, to, reason in new_edges:
    s2["edges"].append({
        "from": frm, "to": to,
        "from_name": frm, "to_name": to,
        "reason": reason
    })
s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(new_edges)} edges (total: {s2['total_edges']})")

# ===== step3: CPT =====
n = s3["noisy_or_params"]

# --- L48 SPEP ---
n["L48"] = {
    "description": "血清蛋白電気泳動。FUO精査で施行。",
    "leak": {
        "not_done": 0.85, "normal": 0.13,
        "monoclonal_gammopathy": 0.01, "polyclonal_gammopathy": 0.01
    },
    "parent_effects": {
        # D114 骨髄腫: monoclonal 90%以上
        "D114": {
            "not_done": 0.15, "normal": 0.03,
            "monoclonal_gammopathy": 0.80, "polyclonal_gammopathy": 0.02
        },
        # D67 リンパ腫: monoclonal 5-10%
        "D67": {
            "not_done": 0.50, "normal": 0.35,
            "monoclonal_gammopathy": 0.08, "polyclonal_gammopathy": 0.07
        },
        # D97 キャッスルマン: polyclonal
        "D97": {
            "not_done": 0.40, "normal": 0.15,
            "monoclonal_gammopathy": 0.05, "polyclonal_gammopathy": 0.40
        },
        # D62 サルコイドーシス: polyclonal 20-30%
        "D62": {
            "not_done": 0.55, "normal": 0.25,
            "monoclonal_gammopathy": 0.02, "polyclonal_gammopathy": 0.18
        },
        # D59 SLE: polyclonal 30-50%
        "D59": {
            "not_done": 0.45, "normal": 0.20,
            "monoclonal_gammopathy": 0.02, "polyclonal_gammopathy": 0.33
        },
        # D45 CMV: polyclonal (急性期)
        "D45": {
            "not_done": 0.60, "normal": 0.25,
            "monoclonal_gammopathy": 0.02, "polyclonal_gammopathy": 0.13
        },
    }
}

# --- L49 骨X線 ---
n["L49"] = {
    "description": "骨X線/骨病変。骨痛・FUO精査で施行。",
    "leak": {
        "not_done": 0.85, "normal": 0.12,
        "lytic_lesions": 0.01, "compression_fracture": 0.02
    },
    "parent_effects": {
        # D114 骨髄腫: lytic 80%, compression fracture 30%
        "D114": {
            "not_done": 0.10, "normal": 0.10,
            "lytic_lesions": 0.55, "compression_fracture": 0.25
        },
        # D67 リンパ腫: lytic 10-20%
        "D67": {
            "not_done": 0.50, "normal": 0.30,
            "lytic_lesions": 0.12, "compression_fracture": 0.08
        },
        # D31 椎体骨髄炎: compression fracture/破壊
        "D31": {
            "not_done": 0.20, "normal": 0.15,
            "lytic_lesions": 0.15, "compression_fracture": 0.50
        },
        # D68 急性白血病: bone involvement rare
        "D68": {
            "not_done": 0.60, "normal": 0.25,
            "lytic_lesions": 0.10, "compression_fracture": 0.05
        },
        # D69 腎細胞癌: metastatic lytic
        "D69": {
            "not_done": 0.50, "normal": 0.25,
            "lytic_lesions": 0.20, "compression_fracture": 0.05
        },
    }
}
print("step3: Added L48 and L49 noisy_or_params with leak + parent_effects")

# ===== Save =====
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("\nAll saved.")
print("9-item audit TODO:")
print("  [x] 1. step1: L48, L49 defined")
print("  [x] 2. step2: 11 edges added")
print("  [x] 3. step3: CPTs with leak + parent_effects")
print("  [ ] 4. bn_inference.py: L-prefix handled normally (OK)")
print("  [ ] 5. test cases: update R190/R191/R192 with L48/L49 evidence")
print("  [ ] 6. WebUI STATE_JA: add monoclonal/polyclonal/lytic labels")
print("  [ ] 7. app.py: no changes needed for new L vars")
print("  [ ] 8. IDF: L48=6parents, L49=5parents (healthy)")
print("  [ ] 9. regression test")
