#!/usr/bin/env python3
"""
Fix missing edges round 2: 情報幾何分析 + 新18症例で検出された辺欠損

14辺追加:
  D16(デング熱) → T01, S07, S14, S26, L02  (5本)
  D28(腸チフス) → E02, L02                  (2本)
  D90(ベーチェット) → T03, L28              (2本)
  D19(薬剤熱) → L28                         (1本)
  D77(DVT/PE) → S13, S14, S12              (3本)
  D32(化膿性関節炎) → L28                   (1本)
"""

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── Step 2: Add edges ─────────────────────────────────────────
step2 = load_json(os.path.join(BASE, "step2_fever_edges_v4.json"))

new_edges = [
    # D16(デング熱) — 5本
    {"from": "D16", "to": "T01", "reason": "デング熱は3-7日の急性発熱", "onset_day_range": {"min": 3, "max": 7}},
    {"from": "D16", "to": "S07", "reason": "デング熱で強い倦怠感", "onset_day_range": {"min": 1, "max": 7}},
    {"from": "D16", "to": "S14", "reason": "デング熱で下痢(15-30%)", "onset_day_range": {"min": 2, "max": 7}},
    {"from": "D16", "to": "S26", "reason": "デング出血熱で消化管出血", "onset_day_range": {"min": 3, "max": 10}},
    {"from": "D16", "to": "L02", "reason": "デング熱でCRP軽度上昇", "onset_day_range": {"min": 1, "max": 7}},
    # D28(腸チフス) — 2本
    {"from": "D28", "to": "E02", "reason": "腸チフスで相対的徐脈もあるが重症で頻脈", "onset_day_range": {"min": 3, "max": 21}},
    {"from": "D28", "to": "L02", "reason": "腸チフスでCRP上昇", "onset_day_range": {"min": 3, "max": 21}},
    # D90(ベーチェット) — 2本
    {"from": "D90", "to": "T03", "reason": "ベーチェット病で周期的発熱", "onset_day_range": {"min": 1, "max": 365}},
    {"from": "D90", "to": "L28", "reason": "ベーチェット病でESR上昇", "onset_day_range": {"min": 1, "max": 365}},
    # D19(薬剤熱) — 1本
    {"from": "D19", "to": "L28", "reason": "薬剤熱でESR上昇(非特異的)", "onset_day_range": {"min": 1, "max": 30}},
    # D77(DVT/PE) — 3本
    {"from": "D77", "to": "S13", "reason": "PE関連の悪心・嘔吐", "onset_day_range": {"min": 0, "max": 7}},
    {"from": "D77", "to": "S14", "reason": "PE関連の消化器症状", "onset_day_range": {"min": 0, "max": 7}},
    {"from": "D77", "to": "S12", "reason": "PE関連の腹痛(横隔膜刺激)", "onset_day_range": {"min": 0, "max": 7}},
    # D32(化膿性関節炎) — 1本
    {"from": "D32", "to": "L28", "reason": "化膿性関節炎でESR上昇", "onset_day_range": {"min": 1, "max": 14}},
]

step2["edges"].extend(new_edges)
step2["total_edges"] = len(step2["edges"])
existing = step2.get("changelog", "")
step2["changelog"] = existing + "; v4.6: 新18症例分析で14辺追加: D16×5, D28×2, D90×2, D19×1, D77×3, D32×1"
save_json(os.path.join(BASE, "step2_fever_edges_v4.json"), step2)
print(f"Step2: {step2['total_edges']} edges (added 14)")

# ─── Step 3: Add CPTs ──────────────────────────────────────────
step3 = load_json(os.path.join(BASE, "step3_fever_cpts_v2.json"))
nop = step3["noisy_or_params"]

# D16(デング熱) → T01: 3-7日が典型、1w-3wもあり
nop["T01"]["parent_effects"]["D16"] = {
    "under_3d": 0.15, "3d_to_1w": 0.55, "1w_to_3w": 0.25, "over_3w": 0.05
}

# D16 → S07(全身倦怠感): デング熱は"breakbone fever"、強い倦怠感
nop["S07"]["parent_effects"]["D16"] = {
    "absent": 0.10, "mild": 0.30, "severe": 0.60
}

# D16 → S14(下痢): 15-30%で出現
nop["S14"]["parent_effects"]["D16"] = {
    "absent": 0.70, "watery": 0.25, "bloody": 0.05
}

# D16 → S26(血便): デング出血熱で消化管出血(重症例5-10%)
nop["S26"]["parent_effects"]["D16"] = {
    "absent": 0.90, "present": 0.10
}

# D16 → L02(CRP): デング熱はCRP軽度〜中等度(ウイルス性なので)
nop["L02"]["parent_effects"]["D16"] = {
    "normal_under_0.3": 0.20, "mild_0.3_3": 0.35, "moderate_3_10": 0.35, "high_over_10": 0.10
}

# D28(腸チフス) → E02(心拍数): 相対的徐脈が有名だが重症では頻脈
nop["E02"]["parent_effects"]["D28"] = {
    "under_100": 0.50, "100_120": 0.35, "over_120": 0.15
}

# D28 → L02(CRP): 腸チフスでCRP上昇
nop["L02"]["parent_effects"]["D28"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.15, "moderate_3_10": 0.35, "high_over_10": 0.45
}

# D90(ベーチェット) → T03(発熱パターン): 周期的発熱が典型
nop["T03"]["parent_effects"]["D90"] = {
    "continuous": 0.15, "intermittent": 0.30, "periodic": 0.50, "double_quotidian": 0.05
}

# D90 → L28(ESR): ベーチェット活動期でESR上昇
nop["L28"]["parent_effects"]["D90"] = {
    "normal": 0.10, "elevated": 0.40, "very_high_over_100": 0.50
}

# D19(薬剤熱) → L28(ESR): 薬剤熱でESR軽度上昇
nop["L28"]["parent_effects"]["D19"] = {
    "normal": 0.30, "elevated": 0.50, "very_high_over_100": 0.20
}

# D77(DVT/PE) → S13(悪心嘔吐): PEで10-20%
nop["S13"]["parent_effects"]["D77"] = {
    "absent": 0.80, "present": 0.20
}

# D77 → S14(下痢): PEで稀だがatypical presentationで
nop["S14"]["parent_effects"]["D77"] = {
    "absent": 0.90, "watery": 0.10, "bloody": 0.00
}

# D77 → S12(腹痛): PE関連腹痛(横隔膜刺激、肝うっ血)
nop["S12"]["parent_effects"]["D77"] = {
    "absent": 0.75, "epigastric": 0.10, "RUQ": 0.05, "RLQ": 0.02,
    "LLQ": 0.02, "suprapubic": 0.01, "diffuse": 0.04, "periumbilical": 0.01
}

# D32(化膿性関節炎) → L28(ESR): 化膿性関節炎でESR上昇
nop["L28"]["parent_effects"]["D32"] = {
    "normal": 0.10, "elevated": 0.55, "very_high_over_100": 0.35
}

save_json(os.path.join(BASE, "step3_fever_cpts_v2.json"), step3)
print("Step3: 14 parent_effects added")

# Verify
checks = [
    ("T01","D16"),("S07","D16"),("S14","D16"),("S26","D16"),("L02","D16"),
    ("E02","D28"),("L02","D28"),
    ("T03","D90"),("L28","D90"),
    ("L28","D19"),
    ("S13","D77"),("S14","D77"),("S12","D77"),
    ("L28","D32"),
]
print("\nVerification:")
for var_id, disease_id in checks:
    pe = nop[var_id]["parent_effects"].get(disease_id)
    print(f"  {disease_id}→{var_id}: {pe}")
