#!/usr/bin/env python3
"""
D23(リケッチア症)辺強化: 9辺追加
R61(地中海紅斑熱)がD16(デング)95.9%に吸収される問題を解決

追加辺:
  D23 → T01 (発熱持続期間): 3d-3w
  D23 → S05 (頭痛): 80-90%
  D23 → S07 (全身倦怠感): 高頻度
  D23 → S09 (悪寒戦慄): 典型症状
  D23 → E02 (心拍数): 重症で頻脈
  D23 → E16 (意識障害): 重症で意識混濁
  D23 → E18 (黄疸): 重症肝障害
  D23 → L11 (肝酵素): 60-80%で上昇
  D23 → L02 (CRP): 細菌感染として高値
"""

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── Step 2: Add edges ─────────────────────────────────────────
step2 = load_json("step2_fever_edges_v4.json")

new_edges = [
    {"from": "D23", "to": "T01", "reason": "リケッチア症の発熱は3日〜3週間", "onset_day_range": {"min": 3, "max": 21}},
    {"from": "D23", "to": "S05", "reason": "リケッチア症で激しい頭痛(80-90%)", "onset_day_range": {"min": 1, "max": 7}},
    {"from": "D23", "to": "S07", "reason": "リケッチア症で全身倦怠感", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D23", "to": "S09", "reason": "リケッチア症で悪寒戦慄", "onset_day_range": {"min": 0, "max": 7}},
    {"from": "D23", "to": "E02", "reason": "リケッチア症重症で頻脈", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D23", "to": "E16", "reason": "リケッチア症重症で意識障害", "onset_day_range": {"min": 3, "max": 14}},
    {"from": "D23", "to": "E18", "reason": "リケッチア症重症肝障害で黄疸", "onset_day_range": {"min": 3, "max": 14}},
    {"from": "D23", "to": "L11", "reason": "リケッチア症で肝酵素上昇(60-80%)", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D23", "to": "L02", "reason": "リケッチア症でCRP高値", "onset_day_range": {"min": 1, "max": 14}},
]

step2["edges"].extend(new_edges)
step2["total_edges"] = len(step2["edges"])
existing = step2.get("changelog", "")
step2["changelog"] = existing + "; v4.7: D23(リケッチア)9辺追加 T01/S05/S07/S09/E02/E16/E18/L11/L02"
save_json("step2_fever_edges_v4.json", step2)
print(f"Step2: {step2['total_edges']} edges (+9)")

# ─── Step 3: Add CPTs ──────────────────────────────────────────
step3 = load_json("step3_fever_cpts_v2.json")
nop = step3["noisy_or_params"]

# D23 → T01(発熱持続期間): 3d-1wが最多、1w-3wも多い
nop["T01"]["parent_effects"]["D23"] = {
    "under_3d": 0.10, "3d_to_1w": 0.45, "1w_to_3w": 0.35, "over_3w": 0.10
}

# D23 → S05(頭痛): 激しい頭痛は80-90%
nop["S05"]["parent_effects"]["D23"] = {
    "absent": 0.10, "mild": 0.25, "severe": 0.65
}

# D23 → S07(全身倦怠感): 高頻度
nop["S07"]["parent_effects"]["D23"] = {
    "absent": 0.10, "mild": 0.30, "severe": 0.60
}

# D23 → S09(悪寒戦慄): 典型的
nop["S09"]["parent_effects"]["D23"] = 0.70

# D23 → E02(心拍数): 重症で頻脈、軽症は正常範囲
nop["E02"]["parent_effects"]["D23"] = {
    "under_100": 0.40, "100_120": 0.40, "over_120": 0.20
}

# D23 → E16(意識障害): 重症例10-20%
nop["E16"]["parent_effects"]["D23"] = {
    "normal": 0.80, "confused": 0.15, "obtunded": 0.05
}

# D23 → E18(黄疸): 重症肝障害5-15%
nop["E18"]["parent_effects"]["D23"] = {
    "absent": 0.85, "present": 0.15
}

# D23 → L11(肝酵素): 60-80%で上昇、重症でmarkedly elevated
nop["L11"]["parent_effects"]["D23"] = {
    "normal": 0.20, "mild_elevated": 0.45, "very_high": 0.35
}

# D23 → L02(CRP): リケッチアはCRP高値(細菌性 intracellular pathogen)
# デング(ウイルス)との差別化ポイント: リケッチアのほうがCRP高い
nop["L02"]["parent_effects"]["D23"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.35, "high_over_10": 0.50
}

save_json("step3_fever_cpts_v2.json", step3)
print("Step3: 9 parent_effects added for D23")

# ─── Verify ────────────────────────────────────────────────────
checks = [
    ("T01","D23"),("S05","D23"),("S07","D23"),("S09","D23"),
    ("E02","D23"),("E16","D23"),("E18","D23"),("L11","D23"),("L02","D23"),
]
print("\nVerification:")
for var_id, disease_id in checks:
    pe = nop[var_id]["parent_effects"].get(disease_id)
    print(f"  D23→{var_id}: {pe}")
