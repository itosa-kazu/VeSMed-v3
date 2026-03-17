"""
Edge Audit Fix 2026-03-17 Round 2: 9条临床辺追加

文献根据:
1. D146(高血圧緊急症)→L16(LDH): 恶性HTN→TMA→LDH↑ (PMC5535052, r=0.76)
2. D171(APS)→L53(トロポニン): APS→MI→troponin↑ (MI 1-4%, PMC6522847)
3. D171(APS)→E05(SpO2): APS→PE→低酸素 (PE 11-20%, PMC9309373)
4. D183(クリオグロブリン)→E36(下腿浮腫): Cryo→MPGN→浮腫 (GN ~30%)
5. D183(クリオグロブリン)→E50(浮腫側性): GN→両側性浮腫
6. D219(GPA)→S21(胸痛): GPA肺病変→胸膜炎 (肺95%, 胸水15-20%, PMC10224739)
7. D42(複雑性UTI)→E09(腹部触診): 腎盂腎炎→CVA圧痛 (~66%)
8. D324(TB髄膜炎)→S22(背部痛): 脊髄蜘蛛膜炎 (~50%合併)
9. R10(体内デバイス)→D55(Q熱): 人工弁→慢性Q熱 (39%リスク, PMC5048103)
"""

import json

STEP2 = "step2_fever_edges_v4.json"
STEP3 = "step3_fever_cpts_v2.json"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_edge(step2, from_id, to_id, from_name, to_name, reason, onset=None):
    for e in step2["edges"]:
        if e["from"] == from_id and e["to"] == to_id:
            print(f"  SKIP (exists): {from_id}→{to_id}")
            return False
    step2["edges"].append({
        "from": from_id, "to": to_id,
        "from_name": from_name, "to_name": to_name,
        "reason": reason, "onset_day_range": onset,
    })
    print(f"  ADD: {from_id}→{to_id}: {reason[:50]}")
    return True


def add_cpt(step3, var_id, disease_id, cpt_dict):
    nop = step3["noisy_or_params"]
    if var_id not in nop:
        print(f"  WARNING: {var_id} not in noisy_or_params!")
        return False
    pe = nop[var_id].setdefault("parent_effects", {})
    if disease_id in pe:
        print(f"  SKIP (CPT exists): {disease_id} in {var_id}")
        return False
    pe[disease_id] = cpt_dict
    print(f"  CPT: {disease_id}→{var_id}")
    return True


def main():
    step2 = load(STEP2)
    step3 = load(STEP3)
    n_before = len(step2["edges"])

    print("=" * 60)
    print("Edge Audit 2026-03-17 Round 2: 9 clinical edges")
    print("=" * 60)

    # 1. D146(高血圧緊急症)→L16(LDH)
    # 悪性高血圧→TMA→微小血管症性溶血→LDH上昇
    # PMC5535052: LDH correlates with PRA (r=0.76) in malignant HTN
    add_edge(step2, "D146", "L16", "hypertensive_emergency", "LDH",
             "悪性高血圧→TMA→微小血管症性溶血→LDH上昇(PMC5535052)", [0, 3])
    add_cpt(step3, "L16", "D146", {
        "normal": 0.4,
        "elevated": 0.6
    })

    # 2. D171(APS)→L53(トロポニン)
    # APS→冠動脈血栓→MI→トロポニン上昇 (MI ~1-4%, PMC6522847)
    add_edge(step2, "D171", "L53", "APS", "troponin",
             "APS→冠動脈血栓/心筋微小血栓→トロポニン上昇(PMC6522847)", [0, 7])
    add_cpt(step3, "L53", "D171", {
        "not_done": 0.60,
        "normal": 0.25,
        "mildly_elevated": 0.12,
        "very_high": 0.03
    })

    # 3. D171(APS)→E05(SpO2)
    # APS→PE(11-20%)→低酸素血症 (PMC9309373)
    add_edge(step2, "D171", "E05", "APS", "SpO2",
             "APS→PE(11-20%)/DAH→低酸素血症(PMC9309373)", [0, 7])
    add_cpt(step3, "E05", "D171", {
        "normal_over_96": 0.65,
        "mild_hypoxia_93_96": 0.20,
        "severe_hypoxia_under_93": 0.15
    })

    # 4. D183(クリオグロブリン血症)→E36(下腿浮腫)
    # Cryo→MPGN(~30%)→ネフローゼ→下腿浮腫
    add_edge(step2, "D183", "E36", "cryoglobulinemia", "lower_leg_edema",
             "クリオグロブリン→MPGN(~30%)→ネフローゼ→下腿浮腫", [14, 90])
    add_cpt(step3, "E36", "D183", {
        "absent": 0.7,
        "present": 0.3
    })

    # 5. D183(クリオグロブリン血症)→E50(下腿浮腫の側性)
    # GN由来の浮腫→両側性
    add_edge(step2, "D183", "E50", "cryoglobulinemia", "edema_laterality",
             "クリオグロブリンGN→両側性浮腫", [14, 90])
    add_cpt(step3, "E50", "D183", {
        "unilateral": 0.1,
        "bilateral": 0.9
    })

    # 6. D219(GPA)→S21(胸痛)
    # GPA肺病変(95%)→胸膜炎→胸痛 (胸水15-20%, PMC10224739)
    add_edge(step2, "D219", "S21", "GPA", "chest_pain",
             "GPA肺病変→胸膜炎→胸痛(PMC10224739)", [7, 60])
    add_cpt(step3, "S21", "D219", {
        "absent": 0.8,
        "present": 0.2
    })

    # 7. D42(複雑性UTI)→E09(腹部触診)
    # 腎盂腎炎→CVA圧痛/腹部圧痛(~66%)
    add_edge(step2, "D42", "E09", "complicated_UTI", "abdominal_exam",
             "腎盂腎炎→CVA/腹部圧痛(~66%)", [0, 7])
    add_cpt(step3, "E09", "D42", {
        "soft_nontender": 0.35,
        "localized_tenderness": 0.60,
        "peritoneal_signs": 0.05
    })

    # 8. D324(結核性髄膜炎)→S22(背部痛)
    # TB meningitis→脊髄蜘蛛膜炎→背部痛(~50%合併, ~25%有症状)
    add_edge(step2, "D324", "S22", "TB_meningitis", "back_pain",
             "結核性髄膜炎→脊髄蜘蛛膜炎→背部痛(~50%合併)", [7, 60])
    add_cpt(step3, "S22", "D324", {
        "absent": 0.75,
        "present": 0.25
    })

    # 9. R10(体内デバイス)→D55(Q熱)
    # 人工弁→慢性Q熱リスク(39%, PMC5048103)
    add_edge(step2, "R10", "D55", "prosthetic_device", "Q_fever",
             "人工弁→慢性Q熱リスク(39%, PMC5048103)", None)
    # R→D edge: add full_cpt entry for D55
    fc = step3["full_cpts"]
    if not fc.get("D55") or fc.get("D55") == {}:
        fc["D55"] = {
            "parents": ["R10"],
            "description": "Q熱。人工弁で慢性Q熱リスク上昇",
            "cpt": {"no": 0.005, "yes": 0.015}
        }
        print("  CPT: D55 full_cpt with R10 parent")
    else:
        print(f"  WARNING: D55 already has full_cpt: {fc['D55']}")

    # Save
    n_after = len(step2["edges"])
    print(f"\nEdges: {n_before} → {n_after} (+{n_after - n_before})")
    save(STEP2, step2)
    save(STEP3, step3)
    print("Done!")


if __name__ == "__main__":
    main()
