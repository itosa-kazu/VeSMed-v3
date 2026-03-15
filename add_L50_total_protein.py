#!/usr/bin/env python3
"""Add L50 total serum protein (血清総蛋白).

三位一体: step1 + step2 + step3 同時追加。
FUO精査の基本血液検査。骨髄腫ではM蛋白によりTP著明上昇(>10g/dL)。
10 parents → IDF≈0.51 (健全)

References:
  - Kyle RA et al. Mayo Clin Proc 2003: myeloma TP often >10 g/dL
  - Dispenzieri A et al. Blood 2009: serum protein as screening
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "step1_fever_v2.7.json"), "r", encoding="utf-8") as f:
    s1 = json.load(f)
with open(os.path.join(BASE, "step2_fever_edges_v4.json"), "r", encoding="utf-8") as f:
    s2 = json.load(f)
with open(os.path.join(BASE, "step3_fever_cpts_v2.json"), "r", encoding="utf-8") as f:
    s3 = json.load(f)

# ===== step1 =====
s1["variables"].append({
    "id": "L50",
    "name": "total_serum_protein",
    "name_ja": "血清総蛋白(TP)",
    "category": "lab",
    "states": ["normal", "mildly_elevated", "very_high"],
    "note": "基本血液検査(肝機能パネル含)。正常6.5-8.0g/dL。"
           "骨髄腫ではM蛋白により10g/dL超(very_high)が多い。"
           "ポリクローナル高γ(SLE/サルコイドーシス/HIV等)ではmild上昇。"
})
print("step1: Added L50 total_serum_protein")

# ===== step2 =====
edges = [
    ("D114", "L50", "骨髄腫: M蛋白によりTP著明上昇(>10g/dL, 75-80%)"),
    ("D97",  "L50", "キャッスルマン病: ポリクローナル高γでTP上昇(40%)"),
    ("D67",  "L50", "悪性リンパ腫: Waldenstrom等でM蛋白/高γ(10-15%)"),
    ("D94",  "L50", "IgG4関連疾患: IgG4高値によるTP上昇(40%)"),
    ("D59",  "L50", "SLE: ポリクローナル高γグロブリン血症(30-40%)"),
    ("D62",  "L50", "サルコイドーシス: ポリクローナル高γ(20-30%)"),
    ("D107", "L50", "HLH: 炎症性高γグロブリン血症(25-35%)"),
    ("D44",  "L50", "急性HIV: ポリクローナルB細胞活性化(20-30%)"),
    ("D17",  "L50", "肺結核: 慢性炎症による高γ(15-25%)"),
    ("D113", "L50", "播種性ヒストプラズマ: 慢性感染による高γ(15-25%)"),
]
for frm, to, reason in edges:
    s2["edges"].append({"from": frm, "to": to, "from_name": frm, "to_name": to, "reason": reason})
s2["total_edges"] = len(s2["edges"])
print(f"step2: Added {len(edges)} edges (total: {s2['total_edges']})")

# ===== step3 =====
n = s3["noisy_or_params"]
n["L50"] = {
    "description": "血清総蛋白。基本検査。骨髄腫ではM蛋白で著明上昇。",
    "leak": {"normal": 0.90, "mildly_elevated": 0.08, "very_high": 0.02},
    "parent_effects": {
        # D114 骨髄腫: M蛋白 → very_high 75%
        "D114": {"normal": 0.10, "mildly_elevated": 0.15, "very_high": 0.75},
        # D97 キャッスルマン: polyclonal → mildly elevated, sometimes high
        "D97":  {"normal": 0.40, "mildly_elevated": 0.40, "very_high": 0.20},
        # D67 リンパ腫: Waldenstrom/一部で上昇
        "D67":  {"normal": 0.70, "mildly_elevated": 0.20, "very_high": 0.10},
        # D94 IgG4: elevated IgG4
        "D94":  {"normal": 0.50, "mildly_elevated": 0.40, "very_high": 0.10},
        # D59 SLE: polyclonal
        "D59":  {"normal": 0.55, "mildly_elevated": 0.35, "very_high": 0.10},
        # D62 サルコイドーシス: polyclonal
        "D62":  {"normal": 0.65, "mildly_elevated": 0.30, "very_high": 0.05},
        # D107 HLH: inflammatory
        "D107": {"normal": 0.55, "mildly_elevated": 0.35, "very_high": 0.10},
        # D44 急性HIV: polyclonal
        "D44":  {"normal": 0.65, "mildly_elevated": 0.28, "very_high": 0.07},
        # D17 TB: chronic
        "D17":  {"normal": 0.70, "mildly_elevated": 0.25, "very_high": 0.05},
        # D113 ヒストプラズマ: chronic
        "D113": {"normal": 0.70, "mildly_elevated": 0.25, "very_high": 0.05},
    }
}
print(f"step3: Added L50 with leak + {len(edges)} parent_effects")

# ===== Save =====
for fname, data in [
    ("step1_fever_v2.7.json", s1),
    ("step2_fever_edges_v4.json", s2),
    ("step3_fever_cpts_v2.json", s3),
]:
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved. {s2['total_edges']} edges total.")
