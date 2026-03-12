#!/usr/bin/env python3
"""
OOSケース処理:
1. R12(Murine typhus), R31(ツツガムシ) → D23(リケッチア)として in_scope化
2. R54(キャッスルマン) → D97として in_scope化
3. D103(急性リウマチ熱), D104(オウム病) を step1/step2/step3 に新規追加
4. R29→D103, R42→D104 として in_scope化
"""

import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_json(name):
    with open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ═══════════════════════════════════════════════════════════════
# 1. テストケース修正
# ═══════════════════════════════════════════════════════════════
cases = load_json("real_case_test_suite.json")

reclassify = {
    "R12": {"expected_id": "D23", "in_scope": True},   # Murine typhus → リケッチア
    "R31": {"expected_id": "D23", "in_scope": True},   # ツツガムシ → リケッチア
    "R54": {"expected_id": "D97", "in_scope": True},   # キャッスルマン → D97
    "R29": {"expected_id": "D103", "in_scope": True},  # リウマチ熱 → 新D103
    "R42": {"expected_id": "D104", "in_scope": True},  # オウム病 → 新D104
}

for c in cases["cases"]:
    if c["id"] in reclassify:
        for k, v in reclassify[c["id"]].items():
            c[k] = v
        print(f"  {c['id']}: → expected={c['expected_id']}, in_scope={c['in_scope']}")

# Update counts
cases["results_summary"]["total_cases"] = len(cases["cases"])
cases["results_summary"]["total_in_scope"] = sum(1 for c in cases["cases"] if c.get("in_scope", True) and c.get("expected_id") != "OOS")
cases["results_summary"]["total_oos"] = sum(1 for c in cases["cases"] if not c.get("in_scope", True) or c.get("expected_id") == "OOS")
save_json("real_case_test_suite.json", cases)
print(f"  In-scope: {cases['results_summary']['total_in_scope']}, OOS: {cases['results_summary']['total_oos']}")

# ═══════════════════════════════════════════════════════════════
# 2. Step1: 新ノード追加
# ═══════════════════════════════════════════════════════════════
step1 = load_json("step1_fever_v2.7.json")

new_diseases = [
    {
        "id": "D103",
        "name": "acute_rheumatic_fever",
        "name_ja": "急性リウマチ熱",
        "category": "disease",
        "states": ["no", "yes"],
        "note": "A群溶連菌感染後の自己免疫疾患。Jones基準: 心炎、多関節炎、舞踏病、輪状紅斑、皮下結節",
        "diagnostic_profile": {
            "name_ja": "急性リウマチ熱",
            "diagnostic_speed": "moderate",
            "expected_certainty_day": 7,
            "entropy_half_life_days": 3,
            "typical_total_duration_days": [7, 42],
            "key_timeline_note": "溶連菌感染2-4週後に発症。心炎が最も重要な合併症",
            "onset_pattern": "subacute（溶連菌感染後2-4週）",
            "resolution_pattern": "関節炎は数日-数週で自然軽快、心炎は数週-数ヶ月",
            "red_flags": ["心炎", "弁膜症", "心不全"]
        }
    },
    {
        "id": "D104",
        "name": "psittacosis",
        "name_ja": "オウム病（Chlamydia psittaci肺炎）",
        "category": "disease",
        "states": ["no", "yes"],
        "note": "鳥類との接触で感染。非定型肺炎の鑑別。高熱、乾性咳嗽、頭痛、肝脾腫",
        "diagnostic_profile": {
            "name_ja": "オウム病",
            "diagnostic_speed": "moderate",
            "expected_certainty_day": 7,
            "entropy_half_life_days": 3,
            "typical_total_duration_days": [7, 21],
            "key_timeline_note": "鳥との接触歴+高熱+乾性咳嗽+相対的徐脈が典型",
            "onset_pattern": "acute to subacute（潜伏期1-2週）",
            "resolution_pattern": "適切な抗菌薬で1-2週で改善",
            "red_flags": ["呼吸不全", "多臓器不全", "DIC"]
        }
    },
]

step1["variables"].extend(new_diseases)
save_json("step1_fever_v2.7.json", step1)
print(f"\nStep1: Added D103, D104. Total variables: {len(step1['variables'])}")

# ═══════════════════════════════════════════════════════════════
# 3. Step2: 新疾病の辺追加
# ═══════════════════════════════════════════════════════════════
step2 = load_json("step2_fever_edges_v4.json")

new_edges = [
    # ── D103(急性リウマチ熱) ──
    # Jones大基準: 心炎、多関節炎(遊走性)、舞踏病、輪状紅斑、皮下結節
    # Jones小基準: 発熱、関節痛、ESR/CRP上昇、PR延長
    {"from": "D103", "to": "T01", "reason": "リウマチ熱は1-3週の発熱", "onset_day_range": {"min": 7, "max": 21}},
    {"from": "D103", "to": "T02", "reason": "急性〜亜急性発症", "onset_day_range": {"min": 0, "max": 3}},
    {"from": "D103", "to": "S02", "reason": "先行する咽頭痛(溶連菌感染)", "onset_day_range": {"min": 0, "max": 7}},
    {"from": "D103", "to": "S05", "reason": "頭痛", "onset_day_range": {"min": 0, "max": 7}},
    {"from": "D103", "to": "S07", "reason": "全身倦怠感", "onset_day_range": {"min": 0, "max": 14}},
    {"from": "D103", "to": "S08", "reason": "関節痛/多関節炎(75%、遊走性)", "onset_day_range": {"min": 0, "max": 21}},
    {"from": "D103", "to": "S21", "reason": "胸痛(心膜炎)", "onset_day_range": {"min": 0, "max": 14}},
    {"from": "D103", "to": "S23", "reason": "関節腫脹", "onset_day_range": {"min": 0, "max": 14}},
    {"from": "D103", "to": "E01", "reason": "発熱38-39度", "onset_day_range": {"min": 0, "max": 21}},
    {"from": "D103", "to": "E02", "reason": "頻脈(心炎時)", "onset_day_range": {"min": 0, "max": 14}},
    {"from": "D103", "to": "E12", "reason": "輪状紅斑(5-10%)", "onset_day_range": {"min": 0, "max": 21}},
    {"from": "D103", "to": "E15", "reason": "新規心雑音(心炎、弁膜症)", "onset_day_range": {"min": 0, "max": 21}},
    {"from": "D103", "to": "L02", "reason": "CRP上昇(小基準)", "onset_day_range": {"min": 0, "max": 21}},
    {"from": "D103", "to": "L28", "reason": "ESR上昇(小基準)", "onset_day_range": {"min": 0, "max": 21}},

    # ── D104(オウム病) ──
    # 高熱、頭痛、乾性咳嗽、筋肉痛、相対的徐脈、肝脾腫
    {"from": "D104", "to": "T01", "reason": "オウム病は1-3週の発熱", "onset_day_range": {"min": 7, "max": 21}},
    {"from": "D104", "to": "T02", "reason": "急性発症", "onset_day_range": {"min": 0, "max": 3}},
    {"from": "D104", "to": "S01", "reason": "乾性咳嗽(50-80%)", "onset_day_range": {"min": 1, "max": 7}},
    {"from": "D104", "to": "S04", "reason": "呼吸困難(重症例)", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D104", "to": "S05", "reason": "激しい頭痛(70-90%)", "onset_day_range": {"min": 0, "max": 7}},
    {"from": "D104", "to": "S06", "reason": "筋肉痛(40-60%)", "onset_day_range": {"min": 0, "max": 7}},
    {"from": "D104", "to": "S07", "reason": "全身倦怠感", "onset_day_range": {"min": 0, "max": 14}},
    {"from": "D104", "to": "S09", "reason": "悪寒戦慄", "onset_day_range": {"min": 0, "max": 3}},
    {"from": "D104", "to": "E01", "reason": "高熱39-40度が典型", "onset_day_range": {"min": 0, "max": 21}},
    {"from": "D104", "to": "E02", "reason": "相対的徐脈が特徴的", "onset_day_range": {"min": 0, "max": 14}},
    {"from": "D104", "to": "E05", "reason": "低酸素(肺炎時)", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D104", "to": "E14", "reason": "脾腫(10-70%)", "onset_day_range": {"min": 3, "max": 14}},
    {"from": "D104", "to": "E34", "reason": "肝腫大", "onset_day_range": {"min": 3, "max": 14}},
    {"from": "D104", "to": "L01", "reason": "WBC正常〜軽度上昇", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D104", "to": "L02", "reason": "CRP上昇", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D104", "to": "L04", "reason": "胸部X線異常(肺炎)", "onset_day_range": {"min": 1, "max": 14}},
    {"from": "D104", "to": "L11", "reason": "肝酵素上昇(50%)", "onset_day_range": {"min": 3, "max": 14}},
]

step2["edges"].extend(new_edges)
step2["total_edges"] = len(step2["edges"])
existing = step2.get("changelog", "")
step2["changelog"] = existing + "; v4.8: D103(リウマチ熱)14辺, D104(オウム病)17辺追加"
save_json("step2_fever_edges_v4.json", step2)
print(f"Step2: {step2['total_edges']} edges (+{len(new_edges)})")

# ═══════════════════════════════════════════════════════════════
# 4. Step3: 新疾病のCPT追加
# ═══════════════════════════════════════════════════════════════
step3 = load_json("step3_fever_cpts_v2.json")
nop = step3["noisy_or_params"]

# ── D103(急性リウマチ熱) root prior ──
step3["root_priors"]["D103"] = 0.001  # 先進国では稀

# ── D104(オウム病) root prior ──
step3["root_priors"]["D104"] = 0.003  # 鳥接触歴で上がる

# ── D103 CPTs ──
# T01: 1-3週の発熱
nop["T01"]["parent_effects"]["D103"] = {
    "under_3d": 0.10, "3d_to_1w": 0.30, "1w_to_3w": 0.45, "over_3w": 0.15
}

# T02: 急性〜亜急性
nop["T02"]["parent_effects"]["D103"] = {
    "sudden_hours": 0.30, "gradual_days": 0.70
}

# S02: 咽頭痛(先行感染)
nop["S02"]["parent_effects"]["D103"] = 0.60

# S05: 頭痛
nop["S05"]["parent_effects"]["D103"] = {
    "absent": 0.50, "mild": 0.35, "severe": 0.15
}

# S07: 倦怠感
nop["S07"]["parent_effects"]["D103"] = {
    "absent": 0.20, "mild": 0.50, "severe": 0.30
}

# S08: 関節痛(75%、遊走性多関節炎が典型)
nop["S08"]["parent_effects"]["D103"] = {
    "absent": 0.25, "present": 0.75
}

# S21: 胸痛(心膜炎で胸膜様疼痛)
nop["S21"]["parent_effects"]["D103"] = {
    "absent": 0.70, "pleuritic": 0.25, "constant": 0.05
}

# S23: 関節腫脹(多関節)
nop["S23"]["parent_effects"]["D103"] = {
    "absent": 0.30, "monoarticular": 0.15, "polyarticular": 0.55
}

# E01: 38-39度が多い
nop["E01"]["parent_effects"]["D103"] = {
    "under_37.5": 0.05, "37.5_38.0": 0.10, "38.0_39.0": 0.50, "39.0_40.0": 0.30, "over_40.0": 0.05
}

# E02: 頻脈(心炎時)
nop["E02"]["parent_effects"]["D103"] = {
    "under_100": 0.50, "100_120": 0.35, "over_120": 0.15
}

# E12: 輪状紅斑(5-10%)
nop["E12"]["parent_effects"]["D103"] = {
    "normal": 0.90, "localized_erythema_warmth_swelling": 0.02,
    "petechiae_purpura": 0.0, "maculopapular_rash": 0.05,
    "vesicular_dermatomal": 0.0, "diffuse_erythroderma": 0.03,
    "skin_necrosis": 0.0, "purpura": 0.0, "vesicle_bulla": 0.0
}

# E15: 新規心雑音(心炎 50-70%)
nop["E15"]["parent_effects"]["D103"] = {
    "absent": 0.35, "pre_existing": 0.05, "new": 0.60
}

# L02: CRP上昇
nop["L02"]["parent_effects"]["D103"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.40, "high_over_10": 0.45
}

# L28: ESR上昇
nop["L28"]["parent_effects"]["D103"] = {
    "normal": 0.05, "elevated": 0.40, "very_high_over_100": 0.55
}

# ── D104(オウム病) CPTs ──
# T01: 1-3週
nop["T01"]["parent_effects"]["D104"] = {
    "under_3d": 0.05, "3d_to_1w": 0.30, "1w_to_3w": 0.50, "over_3w": 0.15
}

# T02: 急性発症
nop["T02"]["parent_effects"]["D104"] = {
    "sudden_hours": 0.60, "gradual_days": 0.40
}

# S01: 乾性咳嗽(50-80%)
nop["S01"]["parent_effects"]["D104"] = {
    "absent": 0.20, "dry": 0.55, "productive": 0.25
}

# S04: 呼吸困難(重症で)
nop["S04"]["parent_effects"]["D104"] = {
    "absent": 0.55, "on_exertion": 0.30, "at_rest": 0.15
}

# S05: 激しい頭痛
nop["S05"]["parent_effects"]["D104"] = {
    "absent": 0.10, "mild": 0.25, "severe": 0.65
}

# S06: 筋肉痛
nop["S06"]["parent_effects"]["D104"] = 0.50

# S07: 倦怠感
nop["S07"]["parent_effects"]["D104"] = {
    "absent": 0.10, "mild": 0.30, "severe": 0.60
}

# S09: 悪寒戦慄
nop["S09"]["parent_effects"]["D104"] = 0.65

# E01: 高熱 39-40度
nop["E01"]["parent_effects"]["D104"] = {
    "under_37.5": 0.02, "37.5_38.0": 0.05, "38.0_39.0": 0.25, "39.0_40.0": 0.50, "over_40.0": 0.18
}

# E02: 相対的徐脈が特徴
nop["E02"]["parent_effects"]["D104"] = {
    "under_100": 0.55, "100_120": 0.30, "over_120": 0.15
}

# E05: 低酸素(肺炎時)
nop["E05"]["parent_effects"]["D104"] = {
    "normal_over_96": 0.50, "mild_hypoxia_93_96": 0.30, "severe_hypoxia_under_93": 0.20
}

# E14: 脾腫
nop["E14"]["parent_effects"]["D104"] = {
    "absent": 0.60, "present": 0.40
}

# E34: 肝腫大
nop["E34"]["parent_effects"]["D104"] = {
    "absent": 0.65, "present": 0.35
}

# L01: WBC 正常〜軽度上昇
nop["L01"]["parent_effects"]["D104"] = {
    "low_under_4000": 0.10, "normal_4000_10000": 0.55, "high_10000_20000": 0.30, "very_high_over_20000": 0.05
}

# L02: CRP上昇
nop["L02"]["parent_effects"]["D104"] = {
    "normal_under_0.3": 0.05, "mild_0.3_3": 0.10, "moderate_3_10": 0.35, "high_over_10": 0.50
}

# L04: 胸部X線(非定型肺炎パターン)
nop["L04"]["parent_effects"]["D104"] = {
    "normal": 0.15, "lobar_consolidation": 0.15, "bilateral_infiltrate": 0.40,
    "interstitial_pattern": 0.20, "pleural_effusion": 0.10
}

# L11: 肝酵素上昇(50%)
nop["L11"]["parent_effects"]["D104"] = {
    "normal": 0.50, "mild_elevated": 0.40, "very_high": 0.10
}

save_json("step3_fever_cpts_v2.json", step3)
print("Step3: D103(14 CPTs), D104(17 CPTs) added")

# ═══════════════════════════════════════════════════════════════
# 5. Verification
# ═══════════════════════════════════════════════════════════════
print("\nVerification - D103 CPTs:")
for vid in ["T01","S08","S23","E15","L02","L28"]:
    pe = nop[vid]["parent_effects"].get("D103")
    print(f"  D103→{vid}: {pe}")

print("\nVerification - D104 CPTs:")
for vid in ["T01","S01","S05","E02","L04","L11"]:
    pe = nop[vid]["parent_effects"].get("D104")
    print(f"  D104→{vid}: {pe}")
