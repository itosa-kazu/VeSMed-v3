#!/usr/bin/env python3
"""Split D67 (リンパ腫) → D67 (NHL) + D354 (HL)

R03(DLBCL), R14(PTCL), R15(splenic NHL) → stay D67
R04(Hodgkin) → move to D354

差別化:
- 年齢: HL=二峰性(20代+60代), NHL=高齢偏重
- 縦隔腫大: HL=60%, NHL=20%
- Pel-Ebstein熱: HL特徴, NHL稀
- B症状: both, but HL=30%, NHL=20%
"""

import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {path}")

def split_step1(path):
    data = load_json(path)

    for v in data['variables']:
        if v['id'] == 'D67':
            v['name'] = 'non_hodgkin_lymphoma'
            v['name_ja'] = '非ホジキンリンパ腫(NHL)'
            v['icd10'] = 'C85'
            v['key_features'] = 'FUOの主因。B症状(発熱+盗汗+体重減少)+リンパ節腫脹+肝脾腫。LDH/sIL-2R上昇。高齢に多い。'
            print(f"  Renamed D67 → 非ホジキンリンパ腫(NHL)")
            break

    hl = {
        "id": "D354",
        "name": "hodgkin_lymphoma",
        "name_ja": "ホジキンリンパ腫(HL)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "C81",
        "category_sub": "malignancy",
        "severity": "high",
        "key_features": "二峰性年齢分布(20代+60代)。B症状+頸部/縦隔リンパ節腫脹。Pel-Ebstein熱。Reed-Sternberg細胞。"
    }

    last_disease_idx = 0
    for i, v in enumerate(data['variables']):
        if v.get('category') == 'disease':
            last_disease_idx = i
    data['variables'].insert(last_disease_idx + 1, hl)
    print(f"  Added D354 ホジキンリンパ腫(HL)")

    save_json(path, data)

def split_step2(path):
    data = load_json(path)

    old_edges = [e for e in data['edges'] if e['from'] == 'D67']
    data['edges'] = [e for e in data['edges'] if e['from'] != 'D67']

    # NHL (D67) edges - similar to original but refined
    nhl_edges = [
        {"from": "D67", "to": "E01", "from_name": "non_hodgkin_lymphoma", "to_name": "temperature",
         "reason": "NHL: 発熱(B症状, 20-30%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D67", "to": "S16", "from_name": "non_hodgkin_lymphoma", "to_name": "night_sweats",
         "reason": "NHL: 盗汗(B症状, 15-25%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D67", "to": "S17", "from_name": "non_hodgkin_lymphoma", "to_name": "weight_loss",
         "reason": "NHL: 体重減少(B症状, 15-25%)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D67", "to": "E13", "from_name": "non_hodgkin_lymphoma", "to_name": "lymphadenopathy",
         "reason": "NHL: リンパ節腫脹(60-70%, 無痛性)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D67", "to": "E14", "from_name": "non_hodgkin_lymphoma", "to_name": "splenomegaly",
         "reason": "NHL: 脾腫(30-40%)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D67", "to": "E34", "from_name": "non_hodgkin_lymphoma", "to_name": "hepatomegaly",
         "reason": "NHL: 肝腫大(20-30%)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D67", "to": "L16", "from_name": "non_hodgkin_lymphoma", "to_name": "LDH",
         "reason": "NHL: LDH上昇(50-60%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D67", "to": "L41", "from_name": "non_hodgkin_lymphoma", "to_name": "IL6_sIL2R",
         "reason": "NHL: sIL-2R上昇(80%+, 特異度高い)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D67", "to": "L15", "from_name": "non_hodgkin_lymphoma", "to_name": "ferritin",
         "reason": "NHL: フェリチン上昇(30-40%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D67", "to": "S07", "from_name": "non_hodgkin_lymphoma", "to_name": "fatigue",
         "reason": "NHL: 全身倦怠感(40-50%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D67", "to": "L28", "from_name": "non_hodgkin_lymphoma", "to_name": "ESR",
         "reason": "NHL: ESR上昇(40-50%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D67", "to": "S46", "from_name": "non_hodgkin_lymphoma", "to_name": "anorexia",
         "reason": "NHL: 食欲不振(30-40%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D67", "to": "T01", "from_name": "non_hodgkin_lymphoma", "to_name": "fever_duration",
         "reason": "NHL: 慢性経過(数週~数ヶ月)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 180}},
        {"from": "D67", "to": "L04", "from_name": "non_hodgkin_lymphoma", "to_name": "chest_xray",
         "reason": "NHL: 縦隔腫大(20%, HLより低頻度)", "onset_day_range": {"earliest": 14, "typical": 30, "latest": 90}},
        {"from": "D67", "to": "S01", "from_name": "non_hodgkin_lymphoma", "to_name": "cough",
         "reason": "NHL: 咳嗽(縦隔病変時)", "onset_day_range": {"earliest": 14, "typical": 30, "latest": 90}},
    ]

    # HL (D354) edges
    hl_edges = [
        {"from": "D354", "to": "E01", "from_name": "hodgkin_lymphoma", "to_name": "temperature",
         "reason": "HL: 発熱(B症状, 30-40%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D354", "to": "S16", "from_name": "hodgkin_lymphoma", "to_name": "night_sweats",
         "reason": "HL: 盗汗(B症状, 25-35%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D354", "to": "S17", "from_name": "hodgkin_lymphoma", "to_name": "weight_loss",
         "reason": "HL: 体重減少(B症状, 25-35%)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D354", "to": "E13", "from_name": "hodgkin_lymphoma", "to_name": "lymphadenopathy",
         "reason": "HL: リンパ節腫脹(80%+, 頸部が最多)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D354", "to": "E14", "from_name": "hodgkin_lymphoma", "to_name": "splenomegaly",
         "reason": "HL: 脾腫(30-40%)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D354", "to": "L16", "from_name": "hodgkin_lymphoma", "to_name": "LDH",
         "reason": "HL: LDH上昇(30-40%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D354", "to": "L41", "from_name": "hodgkin_lymphoma", "to_name": "IL6_sIL2R",
         "reason": "HL: sIL-2R上昇(50-60%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D354", "to": "S07", "from_name": "hodgkin_lymphoma", "to_name": "fatigue",
         "reason": "HL: 全身倦怠感(40-50%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D354", "to": "L28", "from_name": "hodgkin_lymphoma", "to_name": "ESR",
         "reason": "HL: ESR上昇(60-70%, 予後因子)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D354", "to": "S46", "from_name": "hodgkin_lymphoma", "to_name": "anorexia",
         "reason": "HL: 食欲不振(20-30%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 30}},
        {"from": "D354", "to": "T01", "from_name": "hodgkin_lymphoma", "to_name": "fever_duration",
         "reason": "HL: 慢性経過(数週~数ヶ月)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 180}},
        {"from": "D354", "to": "T03", "from_name": "hodgkin_lymphoma", "to_name": "fever_pattern",
         "reason": "HL: Pel-Ebstein熱(1-2週の高熱と1-2週の解熱を繰り返す)", "onset_day_range": {"earliest": 14, "typical": 30, "latest": 90}},
        {"from": "D354", "to": "L04", "from_name": "hodgkin_lymphoma", "to_name": "chest_xray",
         "reason": "HL: 縦隔腫大(60%+, NHLより高頻度)", "onset_day_range": {"earliest": 14, "typical": 30, "latest": 90}},
        {"from": "D354", "to": "L22", "from_name": "hodgkin_lymphoma", "to_name": "anemia",
         "reason": "HL: 貧血(30-40%, 慢性疾患貧血)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D354", "to": "S01", "from_name": "hodgkin_lymphoma", "to_name": "cough",
         "reason": "HL: 咳嗽(縦隔腫大による, 20-30%)", "onset_day_range": {"earliest": 14, "typical": 30, "latest": 90}},
        {"from": "D354", "to": "E46", "from_name": "hodgkin_lymphoma", "to_name": "skin_finding_detail",
         "reason": "HL: 皮膚所見(掻痒, 10-20%)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
    ]

    data['edges'].extend(nhl_edges)
    data['edges'].extend(hl_edges)

    print(f"  Removed {len(old_edges)} old D67 edges")
    print(f"  Added {len(nhl_edges)} NHL edges + {len(hl_edges)} HL edges")
    print(f"  Total edges: {len(data['edges'])}")

    save_json(path, data)

def split_step3(path):
    data = load_json(path)

    # Root priors: D67 was bimodal with sex
    # {male|18_39: 0.004, male|40_64: 0.003, male|65_plus: 0.005,
    #  female|18_39: 0.003, female|40_64: 0.002, female|65_plus: 0.004}
    # NHL: 高齢偏重, HL: 二峰性(若年+高齢)
    if 'D67' in data['root_priors']:
        data['root_priors']['D67'] = {
            "parents": ["R02", "R01"],
            "description": "NHL。高齢に多い、やや男性優位",
            "cpt": {
                "male|18_39": 0.002, "male|40_64": 0.002, "male|65_plus": 0.004,
                "female|18_39": 0.001, "female|40_64": 0.001, "female|65_plus": 0.003
            }
        }
        data['root_priors']['D354'] = {
            "parents": ["R02", "R01"],
            "description": "HL。二峰性(20代+60代)、やや男性優位",
            "cpt": {
                "male|18_39": 0.003, "male|40_64": 0.001, "male|65_plus": 0.002,
                "female|18_39": 0.002, "female|40_64": 0.001, "female|65_plus": 0.001
            }
        }
        print(f"  Split root_priors")

    # Full CPTs: D67 was {"": 0.005}
    if 'D67' in data['full_cpts']:
        data['full_cpts']['D67'] = {
            "parents": [],
            "description": "非ホジキンリンパ腫(NHL)",
            "cpt": {"": 0.003}
        }
        data['full_cpts']['D354'] = {
            "parents": [],
            "description": "ホジキンリンパ腫(HL)",
            "cpt": {"": 0.002}
        }
        print(f"  Split full_cpts")

    save_json(path, data)

def remap_cases(path):
    """R04(Hodgkin) → D354, others stay D67"""
    data = load_json(path)

    for c in data['cases']:
        if c['id'] == 'R04' and c.get('expected_id') == 'D67':
            c['expected_id'] = 'D354'
            print(f"  Remapped R04 (Hodgkin) → D354")

    nhl_cases = [c['id'] for c in data['cases'] if c.get('expected_id') == 'D67']
    hl_cases = [c['id'] for c in data['cases'] if c.get('expected_id') == 'D354']
    print(f"  NHL cases: {nhl_cases}")
    print(f"  HL cases: {hl_cases}")

    save_json(path, data)

def main():
    print("=" * 60)
    print("Split D67 (Lymphoma) → D67(NHL) + D354(HL)")
    print("=" * 60)

    print("\n[1/4] step1")
    split_step1('step1_fever_v2.7.json')
    print("\n[2/4] step2")
    split_step2('step2_fever_edges_v4.json')
    print("\n[3/4] step3")
    split_step3('step3_fever_cpts_v2.json')
    print("\n[4/4] Remap cases")
    remap_cases('real_case_test_suite.json')

    print("\nDone! Run: python bn_inference.py")

if __name__ == '__main__':
    main()
