#!/usr/bin/env python3
"""
批量追加缺失辺+CPT — 三位一体同步
针对新追加案例(R140-R160)中MISS/FATAL的疾患
"""
import json

BASE = "."

# Load
with open(f"{BASE}/step2_fever_edges_v4.json", "r", encoding="utf-8") as f:
    step2 = json.load(f)
with open(f"{BASE}/step3_fever_cpts_v2.json", "r", encoding="utf-8") as f:
    step3 = json.load(f)

edges_list = step2["edges"]
cpts = step3["noisy_or_params"]

def add_edge(frm, to, frm_name, to_name, reason):
    """Add edge to step2 if not exists"""
    for e in edges_list:
        if e["from"] == frm and e["to"] == to:
            return False
    edges_list.append({
        "from": frm, "to": to,
        "from_name": frm_name, "to_name": to_name,
        "reason": reason
    })
    return True

def add_cpt_binary(var_id, disease_id, prob_present):
    """Add binary CPT (absent/present) to step3"""
    if var_id not in cpts:
        print(f"  WARNING: {var_id} not in CPTs")
        return
    pe = cpts[var_id].get("parent_effects", {})
    if disease_id in pe:
        return  # already exists
    pe[disease_id] = {
        "absent": round(1.0 - prob_present, 2),
        "present": prob_present
    }

def add_cpt_multi(var_id, disease_id, state_probs):
    """Add multi-state CPT to step3"""
    if var_id not in cpts:
        print(f"  WARNING: {var_id} not in CPTs")
        return
    pe = cpts[var_id].get("parent_effects", {})
    if disease_id in pe:
        return
    pe[disease_id] = state_probs

def add_cpt_scalar(var_id, disease_id, prob):
    """Add scalar CPT (for binary vars with simple probability)"""
    if var_id not in cpts:
        print(f"  WARNING: {var_id} not in CPTs")
        return
    pe = cpts[var_id].get("parent_effects", {})
    if disease_id in pe:
        return
    pe[disease_id] = prob

added = 0

# ============================================================
# D47 ムンプス (R151 FATAL) — 最優先
# ============================================================
print("=== D47 ムンプス ===")
# S40 顔面腫脹 — ムンプスの主症状
if add_edge("D47", "S40", "mumps", "facial_swelling", "耳下腺腫脹による顔面腫脹はムンプスの主症状"):
    add_cpt_binary("S40", "D47", 0.85)
    added += 1
# E23 頸部腫脹
if add_edge("D47", "E23", "mumps", "neck_swelling", "顎下腺腫脹による頸部腫脹"):
    add_cpt_binary("E23", "D47", 0.6)
    added += 1
# E13 リンパ節腫脹
if add_edge("D47", "E13", "mumps", "lymphadenopathy", "頸部リンパ節腫脹"):
    add_cpt_multi("E13", "D47", {"absent": 0.5, "cervical": 0.45, "generalized": 0.05})
    added += 1
# L02 CRP
if add_edge("D47", "L02", "mumps", "CRP", "ムンプスでCRP軽度上昇"):
    add_cpt_multi("L02", "D47", {"normal_under_0.3": 0.3, "mild_0.3_3": 0.4, "moderate_3_10": 0.25, "high_over_10": 0.05})
    added += 1
# S07 倦怠感
if add_edge("D47", "S07", "mumps", "fatigue", "ムンプスで倦怠感"):
    add_cpt_multi("S07", "D47", {"absent": 0.3, "mild": 0.5, "severe": 0.2})
    added += 1
# E02 心拍数
if add_edge("D47", "E02", "mumps", "heart_rate", "発熱に伴う頻脈"):
    add_cpt_multi("E02", "D47", {"under_100": 0.5, "100_120": 0.4, "over_120": 0.1})
    added += 1
# S24 開口障害
if add_edge("D47", "S24", "mumps", "trismus", "耳下腺腫脹による開口障害"):
    add_cpt_binary("S24", "D47", 0.4)
    added += 1
# T02 発症速さ
if add_edge("D47", "T02", "mumps", "onset_speed", "急性発症"):
    add_cpt_multi("T02", "D47", {"sudden_hours": 0.6, "gradual_days": 0.4})
    added += 1

# ============================================================
# D26 PID (R140 rank24)
# ============================================================
print("=== D26 PID ===")
if add_edge("D26", "L09", "PID", "blood_culture", "PIDで菌血症"):
    add_cpt_multi("L09", "D26", {"not_done_or_pending": 0.3, "negative": 0.5, "gram_positive": 0.1, "gram_negative": 0.1})
    added += 1
if add_edge("D26", "L28", "PID", "ESR", "PIDでESR上昇"):
    add_cpt_multi("L28", "D26", {"normal": 0.15, "elevated": 0.5, "very_high_over_100": 0.35})
    added += 1
if add_edge("D26", "S07", "PID", "fatigue", "PIDで倦怠感"):
    add_cpt_multi("S07", "D26", {"absent": 0.3, "mild": 0.5, "severe": 0.2})
    added += 1
if add_edge("D26", "E02", "PID", "heart_rate", "PIDで頻脈"):
    add_cpt_multi("E02", "D26", {"under_100": 0.4, "100_120": 0.4, "over_120": 0.2})
    added += 1
if add_edge("D26", "E03", "PID", "SBP", "重症PIDで低血圧"):
    add_cpt_multi("E03", "D26", {"normal_over_90": 0.75, "hypotension_under_90": 0.25})
    added += 1
if add_edge("D26", "S14", "PID", "diarrhea", "PIDで下痢（骨盤腹膜刺激）"):
    add_cpt_multi("S14", "D26", {"absent": 0.6, "watery": 0.35, "bloody": 0.05})
    added += 1
if add_edge("D26", "T02", "PID", "onset_speed", "PIDの発症速さ"):
    add_cpt_multi("T02", "D26", {"sudden_hours": 0.3, "gradual_days": 0.7})
    added += 1

# ============================================================
# D39 肛門周囲膿瘍 (R146 rank76)
# ============================================================
print("=== D39 肛門周囲膿瘍 ===")
if add_edge("D39", "S09", "perianal_abscess", "rigors", "膿瘍形成で悪寒戦慄"):
    add_cpt_binary("S09", "D39", 0.4)
    added += 1
if add_edge("D39", "L31", "perianal_abscess", "abd_CT", "CT膿瘍描出"):
    add_cpt_multi("L31", "D39", {"normal": 0.1, "abscess": 0.8, "mass": 0.0, "other_abnormal": 0.1})
    added += 1
if add_edge("D39", "E12", "perianal_abscess", "skin_exam", "肛門周囲の発赤腫脹"):
    add_cpt_multi("E12", "D39", {"normal": 0.15, "localized_erythema_warmth_swelling": 0.8, "petechiae_purpura": 0.0, "maculopapular_rash": 0.0, "vesicular_dermatomal": 0.0, "diffuse_erythroderma": 0.0, "purpura": 0.0, "vesicle_bulla": 0.0, "skin_necrosis": 0.05})
    added += 1
if add_edge("D39", "T02", "perianal_abscess", "onset_speed", "膿瘍は徐々に"):
    add_cpt_multi("T02", "D39", {"sudden_hours": 0.2, "gradual_days": 0.8})
    added += 1

# ============================================================
# D40 CRBSI (R147 rank14)
# ============================================================
print("=== D40 CRBSI ===")
if add_edge("D40", "E02", "CRBSI", "heart_rate", "敗血症で頻脈"):
    add_cpt_multi("E02", "D40", {"under_100": 0.2, "100_120": 0.5, "over_120": 0.3})
    added += 1
if add_edge("D40", "E03", "CRBSI", "SBP", "CRBSIで低血圧/敗血症性ショック"):
    add_cpt_multi("E03", "D40", {"normal_over_90": 0.55, "hypotension_under_90": 0.45})
    added += 1
if add_edge("D40", "E04", "CRBSI", "respiratory_rate", "敗血症で頻呼吸"):
    add_cpt_multi("E04", "D40", {"normal_under_20": 0.3, "tachypnea_20_30": 0.5, "severe_over_30": 0.2})
    added += 1
if add_edge("D40", "T02", "CRBSI", "onset_speed", "CRBSI急性発症"):
    add_cpt_multi("T02", "D40", {"sudden_hours": 0.8, "gradual_days": 0.2})
    added += 1

# ============================================================
# D41 SSI (R148 rank20)
# ============================================================
print("=== D41 SSI ===")
if add_edge("D41", "L28", "SSI", "ESR", "SSIでESR上昇"):
    add_cpt_multi("L28", "D41", {"normal": 0.2, "elevated": 0.6, "very_high_over_100": 0.2})
    added += 1
if add_edge("D41", "L03", "SSI", "procalcitonin", "局所SSIでPCT低値"):
    add_cpt_multi("L03", "D41", {"not_done": 0.3, "low_under_0.25": 0.4, "gray_0.25_0.5": 0.2, "high_over_0.5": 0.1})
    added += 1
if add_edge("D41", "T02", "SSI", "onset_speed", "SSIは術後徐々に"):
    add_cpt_multi("T02", "D41", {"sudden_hours": 0.1, "gradual_days": 0.9})
    added += 1

# ============================================================
# D42 複雑性UTI (R149 rank6)
# ============================================================
print("=== D42 複雑性UTI ===")
if add_edge("D42", "S33", "complicated_UTI", "hematuria", "複雑性UTIで血尿"):
    add_cpt_binary("S33", "D42", 0.4)
    added += 1
if add_edge("D42", "E16", "complicated_UTI", "consciousness", "高齢者UTIで意識変容"):
    add_cpt_multi("E16", "D42", {"normal": 0.6, "confused": 0.35, "obtunded": 0.05})
    added += 1
if add_edge("D42", "E02", "complicated_UTI", "heart_rate", "UTI敗血症で頻脈"):
    add_cpt_multi("E02", "D42", {"under_100": 0.5, "100_120": 0.35, "over_120": 0.15})
    added += 1
if add_edge("D42", "E11", "complicated_UTI", "CVA_tenderness", "上部UTI波及でCVA叩打痛"):
    add_cpt_binary("E11", "D42", 0.5)
    added += 1
if add_edge("D42", "S07", "complicated_UTI", "fatigue", "複雑性UTIで倦怠感"):
    add_cpt_multi("S07", "D42", {"absent": 0.3, "mild": 0.5, "severe": 0.2})
    added += 1
if add_edge("D42", "T02", "complicated_UTI", "onset_speed", "複雑性UTIは徐々に"):
    add_cpt_multi("T02", "D42", {"sudden_hours": 0.3, "gradual_days": 0.7})
    added += 1

# ============================================================
# D43 精巣上体炎 (R150 rank4)
# ============================================================
print("=== D43 精巣上体炎 ===")
if add_edge("D43", "S11", "epididymitis", "frequency", "精巣上体炎で頻尿"):
    add_cpt_binary("S11", "D43", 0.5)
    added += 1
if add_edge("D43", "S13", "epididymitis", "nausea", "精巣上体炎で嘔気"):
    add_cpt_binary("S13", "D43", 0.35)
    added += 1
if add_edge("D43", "L09", "epididymitis", "blood_culture", "精巣上体炎で菌血症は稀"):
    add_cpt_multi("L09", "D43", {"not_done_or_pending": 0.3, "negative": 0.55, "gram_positive": 0.05, "gram_negative": 0.1})
    added += 1
if add_edge("D43", "T01", "epididymitis", "fever_duration", "精巣上体炎の発熱期間"):
    add_cpt_multi("T01", "D43", {"under_3d": 0.3, "3d_to_1w": 0.5, "1w_to_3w": 0.15, "over_3w": 0.05})
    added += 1
if add_edge("D43", "T02", "epididymitis", "onset_speed", "精巣上体炎は徐々に"):
    add_cpt_multi("T02", "D43", {"sudden_hours": 0.3, "gradual_days": 0.7})
    added += 1

# ============================================================
# D48 風疹 (R152 rank22)
# ============================================================
print("=== D48 風疹 ===")
if add_edge("D48", "S06", "rubella", "myalgia", "風疹で筋肉痛"):
    add_cpt_binary("S06", "D48", 0.4)
    added += 1
if add_edge("D48", "S03", "rubella", "nasal", "風疹で鼻汁"):
    add_cpt_multi("S03", "D48", {"absent": 0.4, "clear_rhinorrhea": 0.55, "purulent_rhinorrhea": 0.05})
    added += 1
if add_edge("D48", "E25", "rubella", "conjunctival_injection", "風疹で結膜充血"):
    add_cpt_binary("E25", "D48", 0.5)
    added += 1
if add_edge("D48", "S02", "rubella", "sore_throat", "風疹で咽頭痛"):
    add_cpt_binary("S02", "D48", 0.4)
    added += 1
if add_edge("D48", "S05", "rubella", "headache", "風疹で頭痛"):
    add_cpt_multi("S05", "D48", {"absent": 0.5, "mild": 0.4, "severe": 0.1})
    added += 1
if add_edge("D48", "E35", "rubella", "eye_findings", "風疹で結膜炎"):
    add_cpt_multi("E35", "D48", {"absent": 0.5, "conjunctivitis": 0.45, "uveitis": 0.05})
    added += 1
if add_edge("D48", "T02", "rubella", "onset_speed", "風疹は前駆期から徐々に"):
    add_cpt_multi("T02", "D48", {"sudden_hours": 0.3, "gradual_days": 0.7})
    added += 1

# ============================================================
# D76 輸血関連発熱 (R156 rank29)
# ============================================================
print("=== D76 輸血関連発熱 ===")
if add_edge("D76", "L01", "FNHTR", "WBC", "輸血反応でWBCは通常正常"):
    add_cpt_multi("L01", "D76", {"low_under_4000": 0.1, "normal_4000_10000": 0.7, "high_10000_20000": 0.15, "very_high_over_20000": 0.05})
    added += 1
if add_edge("D76", "T02", "FNHTR", "onset_speed", "輸血反応は急性発症"):
    add_cpt_multi("T02", "D76", {"sudden_hours": 0.95, "gradual_days": 0.05})
    added += 1
# R33→D76 parent edge
if add_edge("R33", "D76", "recent_transfusion", "FNHTR", "輸血が必須リスク"):
    added += 1

# ============================================================
# D79 人工弁心内膜炎 (R157 rank25)
# ============================================================
print("=== D79 PVE ===")
if add_edge("D79", "E12", "PVE", "skin_exam", "PVEでOsler結節/Janeway/線状出血"):
    add_cpt_multi("E12", "D79", {"normal": 0.4, "localized_erythema_warmth_swelling": 0.05, "petechiae_purpura": 0.45, "maculopapular_rash": 0.05, "vesicular_dermatomal": 0.0, "diffuse_erythroderma": 0.0, "purpura": 0.05, "vesicle_bulla": 0.0, "skin_necrosis": 0.0})
    added += 1
if add_edge("D79", "E02", "PVE", "heart_rate", "心内膜炎で頻脈"):
    add_cpt_multi("E02", "D79", {"under_100": 0.4, "100_120": 0.4, "over_120": 0.2})
    added += 1
if add_edge("D79", "E03", "PVE", "SBP", "PVEで血行動態"):
    add_cpt_multi("E03", "D79", {"normal_over_90": 0.7, "hypotension_under_90": 0.3})
    added += 1
if add_edge("D79", "T02", "PVE", "onset_speed", "PVEの発症"):
    add_cpt_multi("T02", "D79", {"sudden_hours": 0.5, "gradual_days": 0.5})
    added += 1

# ============================================================
# Save
# ============================================================
with open(f"{BASE}/step2_fever_edges_v4.json", "w", encoding="utf-8") as f:
    json.dump(step2, f, ensure_ascii=False, indent=2)
with open(f"{BASE}/step3_fever_cpts_v2.json", "w", encoding="utf-8") as f:
    json.dump(step3, f, ensure_ascii=False, indent=2)

print(f"\n=== Added {added} new edges+CPTs ===")
print(f"Total edges: {len(edges_list)}")
