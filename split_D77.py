#!/usr/bin/env python3
"""Split D77 (DVT/PE) → D77 (PE only) + D355 (DVT)

All 4 existing cases (R13, R71, R72, R210) are PE cases.
D77 becomes 肺塞栓症(PE), D355 becomes 深部静脈血栓症(DVT).

差別化:
- S39(下肢腫脹): DVT=0.90, PE=0.30
- S04(呼吸困難): PE=0.85, DVT=0.20
- E05(SpO2低下): PE高, DVT正常
- S21(胸痛): PE=0.60, DVT=0.05
- L20(D-dimer): both elevated but PE more so
"""

import json
import sys
import copy

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {path}")

def split_step1(path):
    """Rename D77 to PE, add D355 DVT"""
    data = load_json(path)

    for v in data['variables']:
        if v['id'] == 'D77':
            v['name'] = 'pulmonary_embolism'
            v['name_ja'] = '肺塞栓症(PE)'
            v['icd10'] = 'I26'
            v['key_features'] = '突然の呼吸困難+胸痛(胸膜性)+頻脈+低酸素血症。D-dimer上昇。造影CTで確定。発熱は低頻度。'
            print(f"  Renamed D77 → 肺塞栓症(PE)")
            break

    # Add D355 DVT after D77 (or at end of diseases)
    dvt = {
        "id": "D355",
        "name": "deep_vein_thrombosis",
        "name_ja": "深部静脈血栓症(DVT)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "I82",
        "category_sub": "vascular",
        "severity": "moderate",
        "key_features": "片側下肢腫脹+疼痛+発赤+Homans徴候。D-dimer上昇。PE移行リスク。発熱は低頻度(10-15%)。"
    }

    # Insert after D77
    for i, v in enumerate(data['variables']):
        if v['id'] == 'D77':
            # Find next disease after D77
            insert_idx = i + 1
            break

    # Actually, insert at end of disease list (before non-disease variables)
    # Find last disease
    last_disease_idx = 0
    for i, v in enumerate(data['variables']):
        if v.get('category') == 'disease':
            last_disease_idx = i

    data['variables'].insert(last_disease_idx + 1, dvt)
    print(f"  Added D355 深部静脈血栓症(DVT)")

    save_json(path, data)

def split_step2(path):
    """Split edges: PE-specific stay with D77, shared edges copied to D355, DVT-specific added"""
    data = load_json(path)

    # Current D77 edges and their PE/DVT applicability:
    # E01 (fever): PE low freq, DVT very low → both keep, different reason
    # S04 (dyspnea): PE=85%, DVT=20% → both but different
    # S21 (chest pain): PE=60%, DVT=5% → PE mainly
    # S39 (leg swelling): PE=30%, DVT=90% → both but DVT dominant
    # E02 (heart rate): PE=tachycardia, DVT=normal → PE mainly
    # E05 (SpO2): PE=low, DVT=normal → PE only
    # L20 (D-dimer): both elevated → both
    # L04 (chest xray): PE → PE only
    # T03 (fever pattern): PE → PE only

    # Remove old D77 edges
    old_edges = [e for e in data['edges'] if e['from'] == 'D77']
    data['edges'] = [e for e in data['edges'] if e['from'] != 'D77']

    # PE (D77) edges - refined
    pe_edges = [
        {"from": "D77", "to": "E01", "from_name": "pulmonary_embolism", "to_name": "temperature",
         "reason": "PE: 発熱(10-15%, 低頻度)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D77", "to": "S04", "from_name": "pulmonary_embolism", "to_name": "dyspnea",
         "reason": "PE: 突然の呼吸困難(85%+, 最多症状)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D77", "to": "S21", "from_name": "pulmonary_embolism", "to_name": "chest_pain",
         "reason": "PE: 胸膜性胸痛(60-70%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D77", "to": "S39", "from_name": "pulmonary_embolism", "to_name": "unilateral_leg_swelling",
         "reason": "PE: 片側下肢腫脹(DVT合併時, 30%)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 7}},
        {"from": "D77", "to": "E02", "from_name": "pulmonary_embolism", "to_name": "heart_rate",
         "reason": "PE: 頻脈(80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D77", "to": "E05", "from_name": "pulmonary_embolism", "to_name": "SpO2",
         "reason": "PE: 低酸素血症(80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D77", "to": "L20", "from_name": "pulmonary_embolism", "to_name": "D_dimer",
         "reason": "PE: D-dimer上昇(95%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D77", "to": "L04", "from_name": "pulmonary_embolism", "to_name": "chest_xray",
         "reason": "PE: CXR異常(無気肺/胸水, 50%)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 7}},
        {"from": "D77", "to": "T03", "from_name": "pulmonary_embolism", "to_name": "fever_pattern",
         "reason": "PE: 持続熱パターン", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 14}},
        {"from": "D77", "to": "T02", "from_name": "pulmonary_embolism", "to_name": "onset_pattern",
         "reason": "PE: 突然発症", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D77", "to": "T01", "from_name": "pulmonary_embolism", "to_name": "fever_duration",
         "reason": "PE: 急性(数時間~数日)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 3}},
        {"from": "D77", "to": "L51", "from_name": "pulmonary_embolism", "to_name": "BNP",
         "reason": "PE: BNP上昇(右心負荷, 50-60%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D77", "to": "S49", "from_name": "pulmonary_embolism", "to_name": "orthopnea",
         "reason": "PE: 起座呼吸(大量PE時, 20-30%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
    ]

    # DVT (D355) edges
    dvt_edges = [
        {"from": "D355", "to": "E01", "from_name": "deep_vein_thrombosis", "to_name": "temperature",
         "reason": "DVT: 発熱(10-15%, 低頻度)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 5}},
        {"from": "D355", "to": "S39", "from_name": "deep_vein_thrombosis", "to_name": "unilateral_leg_swelling",
         "reason": "DVT: 片側下肢腫脹(90%+, 最多症状)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 3}},
        {"from": "D355", "to": "L20", "from_name": "deep_vein_thrombosis", "to_name": "D_dimer",
         "reason": "DVT: D-dimer上昇(90%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D355", "to": "S04", "from_name": "deep_vein_thrombosis", "to_name": "dyspnea",
         "reason": "DVT: 呼吸困難(PE移行時のみ, 5-10%)", "onset_day_range": {"earliest": 1, "typical": 3, "latest": 14}},
        {"from": "D355", "to": "E02", "from_name": "deep_vein_thrombosis", "to_name": "heart_rate",
         "reason": "DVT: 頻脈(通常なし、PE移行時)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 7}},
        {"from": "D355", "to": "E05", "from_name": "deep_vein_thrombosis", "to_name": "SpO2",
         "reason": "DVT: SpO2通常正常", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 7}},
        {"from": "D355", "to": "T01", "from_name": "deep_vein_thrombosis", "to_name": "fever_duration",
         "reason": "DVT: 亜急性(数日~数週)", "onset_day_range": {"earliest": 1, "typical": 3, "latest": 14}},
        {"from": "D355", "to": "T02", "from_name": "deep_vein_thrombosis", "to_name": "onset_pattern",
         "reason": "DVT: 漸増性(急性だが突然ではない)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D355", "to": "E36", "from_name": "deep_vein_thrombosis", "to_name": "limb_edema",
         "reason": "DVT: 四肢浮腫(患肢, 80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 3}},
        {"from": "D355", "to": "L01", "from_name": "deep_vein_thrombosis", "to_name": "WBC",
         "reason": "DVT: WBC通常正常~軽度上昇", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D355", "to": "L02", "from_name": "deep_vein_thrombosis", "to_name": "CRP",
         "reason": "DVT: CRP軽度上昇(炎症反応)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
    ]

    data['edges'].extend(pe_edges)
    data['edges'].extend(dvt_edges)

    print(f"  Removed {len(old_edges)} old D77 edges")
    print(f"  Added {len(pe_edges)} PE edges + {len(dvt_edges)} DVT edges")
    print(f"  Total edges: {len(data['edges'])}")

    save_json(path, data)

def split_step3(path):
    """Split CPTs for D77 → PE + DVT"""
    data = load_json(path)

    # Root priors: D77 was age-dependent {18_39: 0.003, 40_64: 0.005, 65_plus: 0.010}
    # Split: PE ≈ 60% of VTE, DVT ≈ 40%
    # PE: {18_39: 0.002, 40_64: 0.003, 65_plus: 0.006}
    # DVT: {18_39: 0.002, 40_64: 0.003, 65_plus: 0.005}

    if 'D77' in data['root_priors']:
        data['root_priors']['D77'] = {
            "parents": ["R01"],
            "description": "PE。高齢に多い",
            "cpt": {
                "18_39": 0.002,
                "40_64": 0.003,
                "65_plus": 0.006
            }
        }
        data['root_priors']['D355'] = {
            "parents": ["R01"],
            "description": "DVT。高齢+不動+術後に多い",
            "cpt": {
                "18_39": 0.002,
                "40_64": 0.003,
                "65_plus": 0.005
            }
        }
        print(f"  Split root_priors D77 → D77(PE) + D355(DVT)")

    # Full CPTs: D77 was {"": 0.005}
    # Split: PE=0.003, DVT=0.003
    if 'D77' in data['full_cpts']:
        data['full_cpts']['D77'] = {
            "parents": [],
            "description": "肺塞栓症(PE)",
            "cpt": {"": 0.003}
        }
        data['full_cpts']['D355'] = {
            "parents": [],
            "description": "深部静脈血栓症(DVT)",
            "cpt": {"": 0.003}
        }
        print(f"  Split full_cpts D77 → D77(PE) + D355(DVT)")

    # noisy_or_params: D77 had none, so nothing to split

    save_json(path, data)

def remap_cases(path):
    """No remapping needed - all 4 cases (R13, R71, R72, R210) are PE cases"""
    data = load_json(path)

    pe_cases = [c for c in data['cases'] if c.get('expected_id') == 'D77']
    print(f"  D77 cases (all PE, no remapping needed): {[c['id'] for c in pe_cases]}")

    # No changes needed
    save_json(path, data)

def main():
    print("=" * 60)
    print("Split D77 (DVT/PE) → D77(PE) + D355(DVT)")
    print("=" * 60)

    print("\n[1/4] step1: Rename D77 + Add D355")
    split_step1('step1_fever_v2.7.json')

    print("\n[2/4] step2: Split edges")
    split_step2('step2_fever_edges_v4.json')

    print("\n[3/4] step3: Split CPTs")
    split_step3('step3_fever_cpts_v2.json')

    print("\n[4/4] Remap test cases")
    remap_cases('real_case_test_suite.json')

    print("\n" + "=" * 60)
    print("Done! Run: python bn_inference.py to verify")
    print("=" * 60)

if __name__ == '__main__':
    main()
