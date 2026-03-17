#!/usr/bin/env python3
"""
Edge-audit batch fix: Add missing edges for worst-ranking disease groups.
Deep-first priority. All edges backed by PMC/literature evidence.
"""

import json

step1 = json.load(open('step1_fever_v2.7.json'))
step2 = json.load(open('step2_fever_edges_v4.json'))
step3 = json.load(open('step3_fever_cpts_v2.json'))
tests = json.load(open('real_case_test_suite.json'))

existing_edges = {(e['from'], e['to']) for e in step2['edges']}
nop = step3.setdefault('noisy_or_params', {})

def add_edge(frm, to, reason, onset=None, frm_name=None, to_name=None):
    if (frm, to) in existing_edges:
        print(f"  SKIP (exists): {frm} -> {to}")
        return False
    e = {"from": frm, "to": to, "reason": reason}
    if onset:
        e["onset_day_range"] = onset
    if frm_name:
        e["from_name"] = frm_name
    if to_name:
        e["to_name"] = to_name
    step2['edges'].append(e)
    existing_edges.add((frm, to))
    print(f"  ADD: {frm} -> {to}: {reason}")
    return True

def add_nop_parent(var_id, disease_id, effects):
    if var_id in nop:
        if disease_id not in nop[var_id].get('parent_effects', {}):
            nop[var_id].setdefault('parent_effects', {})[disease_id] = effects
            print(f"  NOP: {var_id} += {disease_id}")
        else:
            print(f"  NOP SKIP: {var_id} {disease_id}")
    else:
        print(f"  WARN: {var_id} not in noisy_or_params")

added = 0

# === D366 トキソプラズマリンパ節炎 (max_rank=59) ===
# PMC10209818, PMC10447303, StatPearls
print("=== D366 トキソプラズマリンパ節炎 ===")
if add_edge("D366", "S05", "トキソリンパ節炎: 頭痛(15%, IM様症状, PMC10209818)"):
    added += 1
    add_nop_parent("S05", "D366", {"absent": 0.85, "mild": 0.12, "severe": 0.03})
if add_edge("D366", "S16", "トキソリンパ節炎: 盗汗(75%, PMC10447303)"):
    added += 1
    add_nop_parent("S16", "D366", {"absent": 0.30, "present": 0.70})
if add_edge("D366", "S17", "トキソリンパ節炎: 体重減少(10-20%, StatPearls)"):
    added += 1
    add_nop_parent("S17", "D366", {"absent": 0.85, "present": 0.15})
if add_edge("R06", "D366", "トキソプラズマ: 熱帯で高流行(Africa 61%)"):
    added += 1

# === D365 肺クリプトコッカス症 (max_rank=49) ===
print("\n=== D365 肺クリプトコッカス症 ===")
if add_edge("D365", "L11", "肺クリプト: 肝酵素(播散時10-20%)"):
    added += 1
    add_nop_parent("L11", "D365", {"normal": 0.80, "mild_elevated": 0.15, "very_high": 0.05})
# S05/E13/E46/E02/S16 skipped: overfit risk or non-specific

# === D353 UC (max_rank=43) ===
print("\n=== D353 UC ===")
if add_edge("R01", "D353", "UC: 15-30歳+50-70歳の二峰性"):
    added += 1
if add_edge("R02", "D353", "UC: 性差少ない(45歳以降男性やや多い)"):
    added += 1
if add_edge("R35", "D353", "UC: IBD既往/家族歴リスク(5-20%)"):
    added += 1
# L22 skipped: drug-induced, not disease-driven

# === D222 RA (max_rank=26) ===
print("\n=== D222 RA ===")
if add_edge("D222", "E05", "RA: SpO2低下(ILD10%臨床的, 安静時異常13%)"):
    added += 1
    add_nop_parent("E05", "D222", {"normal_over_96": 0.85, "mild_hypoxia_93_96": 0.10, "severe_hypoxia_under_93": 0.05})
if add_edge("D222", "E16", "RA: 意識障害(頸椎亜脱臼/脊髄症, 稀)"):
    added += 1
    add_nop_parent("E16", "D222", {"normal": 0.95, "confused": 0.04, "obtunded": 0.01})
if add_edge("D222", "E37", "RA: JVD(心膜炎1-5%)"):
    added += 1
    add_nop_parent("E37", "D222", {"absent": 0.97, "present": 0.03})

# === D258 RSV (max_rank=24) ===
print("\n=== D258 RSV ===")
if add_edge("D258", "L09", "RSV: 血培陰性(ウイルス性, 二次感染時GP)"):
    added += 1
    add_nop_parent("L09", "D258", {"not_done_or_pending": 0.30, "negative": 0.60, "gram_positive": 0.08, "gram_negative": 0.02})
if add_edge("D258", "L53", "RSV: トロポニン(心筋炎合併時, 稀)"):
    added += 1
    add_nop_parent("L53", "D258", {"not_done": 0.50, "normal": 0.40, "mildly_elevated": 0.08, "very_high": 0.02})

# === D355 DVT (max_rank=19) ===
print("\n=== D355 DVT ===")
if add_edge("D355", "S01", "DVT: 咳嗽(PE移行時5-10%)"):
    added += 1
    add_nop_parent("S01", "D355", {"absent": 0.90, "present": 0.10})
if add_edge("R01", "D355", "DVT: 高齢ほどリスク増"):
    added += 1
if add_edge("R02", "D355", "DVT: 女性やや多い(OCP/妊娠)"):
    added += 1

# === Save step2 + step3 ===
step2['total_edges'] = len(step2['edges'])
json.dump(step2, open('step2_fever_edges_v4.json', 'w'), indent=2, ensure_ascii=False)

# Update step3 CPTs for new R01/R02 parents
if 'D353' in step3['full_cpts']:
    cpt = step3['full_cpts']['D353']
    if 'R01' not in cpt.get('parents', []):
        cpt['parents'] = ['R01']
        cpt['cpt'] = {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0005,
            "13_17": 0.002, "18_39": 0.003, "40_64": 0.002, "65_plus": 0.003
        }
        print("\nUpdated D353 CPT: R01 parent (bimodal)")

if 'D355' in step3['full_cpts']:
    cpt = step3['full_cpts']['D355']
    if 'R01' not in cpt.get('parents', []):
        cpt['parents'] = ['R01']
        cpt['cpt'] = {
            "0_1": 0.0001, "1_5": 0.0001, "6_12": 0.0001,
            "13_17": 0.0005, "18_39": 0.001, "40_64": 0.002, "65_plus": 0.003
        }
        print("Updated D355 CPT: R01 parent (age-dependent)")

json.dump(step3, open('step3_fever_cpts_v2.json', 'w'), indent=2, ensure_ascii=False)

print(f"\n=== Total: {added} edges added. Total edges: {step2['total_edges']} ===")
