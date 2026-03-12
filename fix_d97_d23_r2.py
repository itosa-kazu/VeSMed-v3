#!/usr/bin/env python3
"""
D97(キャッスルマン)辺追加 + D23(リケッチア)辺追加Round2
- R54 FATAL解消: D97→T03/S17/L22 追加
- R12 FATAL解消: D23→S14/S12/E34/E14 追加 + D23にR30(動物接触)を親として追加
"""

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ═══ Step 2: edges ═══════════════════════════════════════════
step2 = load_json("step2_fever_edges_v4.json")

new_edges = [
    # ── D97(キャッスルマン) 追加辺 ──
    {"from": "D97", "to": "T03", "reason": "iMCDで周期的発熱が典型", "onset_day_range": {"min": 7, "max": 120}},
    {"from": "D97", "to": "S17", "reason": "iMCDで体重減少(消耗症状)", "onset_day_range": {"min": 14, "max": 120}},
    {"from": "D97", "to": "L22", "reason": "iMCDで貧血(慢性炎症性貧血)", "onset_day_range": {"min": 14, "max": 120}},
    {"from": "D97", "to": "L01", "reason": "iMCDでWBC上昇", "onset_day_range": {"min": 7, "max": 60}},
    {"from": "D97", "to": "L16", "reason": "iMCDでLDH上昇", "onset_day_range": {"min": 7, "max": 60}},

    # ── D23(リケッチア) 追加辺 ──
    {"from": "D23", "to": "S14", "reason": "リケッチアで消化器症状(下痢10-30%)", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D23", "to": "S12", "reason": "リケッチアで腹痛", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D23", "to": "E34", "reason": "リケッチアで肝腫大", "onset_day_range": {"min": 3, "max": 14}},
    {"from": "D23", "to": "E14", "reason": "リケッチアで脾腫", "onset_day_range": {"min": 3, "max": 14}},
    {"from": "D23", "to": "L01", "reason": "リケッチアでWBC正常〜低下", "onset_day_range": {"min": 1, "max": 14}},
]

step2["edges"].extend(new_edges)
step2["total_edges"] = len(step2["edges"])
existing = step2.get("changelog", "")
step2["changelog"] = existing + "; v4.9: D97+5辺(T03/S17/L22/L01/L16), D23+5辺(S14/S12/E34/E14/L01)"
save_json("step2_fever_edges_v4.json", step2)
print(f"Step2: {step2['total_edges']} edges (+10)")

# ═══ Step 3: CPTs ════════════════════════════════════════════
step3 = load_json("step3_fever_cpts_v2.json")
nop = step3["noisy_or_params"]

# ── D97 CPTs ──

# D97 → T03(発熱パターン): iMCDは周期的発熱が典型
nop["T03"]["parent_effects"]["D97"] = {
    "continuous": 0.15, "intermittent": 0.25, "periodic": 0.55, "double_quotidian": 0.05
}

# D97 → S17(体重減少): iMCDで消耗症状60-80%
nop["S17"]["parent_effects"]["D97"] = 0.70

# D97 → L22(貧血): iMCDで慢性炎症性貧血70-80%
nop["L22"]["parent_effects"]["D97"] = 0.75

# D97 → L01(WBC): iMCDでWBC上昇
nop["L01"]["parent_effects"]["D97"] = {
    "low_under_4000": 0.05, "normal_4000_10000": 0.30,
    "high_10000_20000": 0.45, "very_high_over_20000": 0.20
}

# D97 → L16(LDH): iMCDでLDH上昇
nop["L16"]["parent_effects"]["D97"] = {
    "normal": 0.30, "elevated": 0.70
}

# ── D23 CPTs (追加分) ──

# D23 → S14(下痢): Murine typhus/RMSF で10-30%
nop["S14"]["parent_effects"]["D23"] = {
    "absent": 0.70, "watery": 0.25, "bloody": 0.05
}

# D23 → S12(腹痛): リケッチアで腹痛15-25%
nop["S12"]["parent_effects"]["D23"] = {
    "absent": 0.75, "epigastric": 0.05, "RUQ": 0.05, "RLQ": 0.05,
    "LLQ": 0.02, "suprapubic": 0.01, "diffuse": 0.07
}

# D23 → E34(肝腫大): リケッチアで肝腫大20-40%
nop["E34"]["parent_effects"]["D23"] = {
    "absent": 0.65, "present": 0.35
}

# D23 → E14(脾腫): リケッチアで脾腫15-30%
nop["E14"]["parent_effects"]["D23"] = {
    "absent": 0.70, "present": 0.30
}

# D23 → L01(WBC): リケッチアで正常〜白血球減少
nop["L01"]["parent_effects"]["D23"] = {
    "low_under_4000": 0.25, "normal_4000_10000": 0.50,
    "high_10000_20000": 0.20, "very_high_over_20000": 0.05
}

# ── D23にR30(動物接触)を親として追加 ──
# full_cptsでD23の親にR30を追加
d23_cpt = step3["full_cpts"]["D23"]
if "R30" not in d23_cpt.get("parents", []):
    d23_cpt["parents"].append("R30")
    # 既存のCPT keyにR30状態を追加
    # R30: none/livestock/pet_cat/wild_animal
    # R06: no/tropical_endemic/developed/domestic
    # R19: spring/summer/autumn/winter
    old_cpt = d23_cpt["cpt"].copy()
    new_cpt = {}
    # R30=noneの場合は既存確率を維持、pet_cat/livestock/wild_animalで確率上昇
    r30_multiplier = {"none": 1.0, "livestock": 2.0, "pet_cat": 3.0, "wild_animal": 5.0}
    for old_key, old_p in old_cpt.items():
        for r30_state, mult in r30_multiplier.items():
            new_key = f"{old_key}|{r30_state}" if old_key else r30_state
            new_cpt[new_key] = min(old_p * mult, 0.5)  # cap at 0.5
    d23_cpt["cpt"] = new_cpt
    print(f"  D23: Added R30 as parent. CPT keys: {len(new_cpt)}")

save_json("step3_fever_cpts_v2.json", step3)
print("Step3: D97(5 CPTs) + D23(5 CPTs + R30 parent) added")

# ═══ Verify ══════════════════════════════════════════════════
print("\nD97 new CPTs:")
for vid in ["T03","S17","L22","L01","L16"]:
    pe = nop[vid]["parent_effects"].get("D97")
    print(f"  D97→{vid}: {pe}")

print("\nD23 new CPTs:")
for vid in ["S14","S12","E34","E14","L01"]:
    pe = nop[vid]["parent_effects"].get("D23")
    print(f"  D23→{vid}: {pe}")
