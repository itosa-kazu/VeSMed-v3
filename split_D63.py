#!/usr/bin/env python3
"""Split D63 (IBD) → D63 (Crohn's disease) + D353 (UC)

Existing case R130 is Crohn's disease (70M, bloody diarrhea + Sweet syndrome).

差別化:
- S26(血便): UC=0.90, CD=0.50
- S29(口腔潰瘍): CD=0.40, UC=0.05
- S12(腹痛部位): CD=RLQ, UC=LLQ
- 肛門病変: CD=30-50%, UC=rare
- 体重減少: CD>UC
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
        if v['id'] == 'D63':
            v['name'] = 'crohns_disease'
            v['name_ja'] = 'クローン病'
            v['icd10'] = 'K50'
            v['key_features'] = '非連続性病変(skip lesion)+肛門病変+口腔潰瘍+右下腹部痛。若年者。体重減少顕著。肉芽腫形成。'
            print(f"  Renamed D63 → クローン病")
            break

    uc = {
        "id": "D353",
        "name": "ulcerative_colitis",
        "name_ja": "潰瘍性大腸炎(UC)",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "K51",
        "category_sub": "autoimmune",
        "severity": "moderate",
        "key_features": "連続性直腸炎から口側進展+血性下痢+左下腹部痛+テネスムス。若年者。関節炎/壊疽性膿皮症/原発性硬化性胆管炎合併。"
    }

    last_disease_idx = 0
    for i, v in enumerate(data['variables']):
        if v.get('category') == 'disease':
            last_disease_idx = i
    data['variables'].insert(last_disease_idx + 1, uc)
    print(f"  Added D353 潰瘍性大腸炎(UC)")

    save_json(path, data)

def split_step2(path):
    data = load_json(path)

    old_edges = [e for e in data['edges'] if e['from'] == 'D63']
    data['edges'] = [e for e in data['edges'] if e['from'] != 'D63']

    # Crohn's (D63) edges
    cd_edges = [
        {"from": "D63", "to": "E01", "from_name": "crohns_disease", "to_name": "temperature",
         "reason": "CD: 発熱(40-50%)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D63", "to": "S14", "from_name": "crohns_disease", "to_name": "diarrhea",
         "reason": "CD: 慢性下痢(70-80%, 非血性が多い)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D63", "to": "S26", "from_name": "crohns_disease", "to_name": "bloody_stool",
         "reason": "CD: 血便(30-50%, UCより低頻度)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D63", "to": "S12", "from_name": "crohns_disease", "to_name": "abdominal_pain_location",
         "reason": "CD: 腹痛(80%+, 右下腹部が典型)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D63", "to": "S17", "from_name": "crohns_disease", "to_name": "weight_loss",
         "reason": "CD: 体重減少(60-70%, 吸収障害)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D63", "to": "S29", "from_name": "crohns_disease", "to_name": "oral_ulcer",
         "reason": "CD: 口腔潰瘍(20-40%, CDに特徴的)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D63", "to": "L02", "from_name": "crohns_disease", "to_name": "CRP",
         "reason": "CD: CRP上昇(80%+)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D63", "to": "L28", "from_name": "crohns_disease", "to_name": "ESR",
         "reason": "CD: ESR上昇(50-60%)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D63", "to": "S46", "from_name": "crohns_disease", "to_name": "anorexia",
         "reason": "CD: 食欲不振(50-60%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D63", "to": "T01", "from_name": "crohns_disease", "to_name": "fever_duration",
         "reason": "CD: 慢性経過(数週~数ヶ月)", "onset_day_range": {"earliest": 7, "typical": 21, "latest": 120}},
        {"from": "D63", "to": "S07", "from_name": "crohns_disease", "to_name": "fatigue",
         "reason": "CD: 全身倦怠感(60-70%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 60}},
        {"from": "D63", "to": "L01", "from_name": "crohns_disease", "to_name": "WBC",
         "reason": "CD: WBC上昇(炎症時)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D63", "to": "S86", "from_name": "crohns_disease", "to_name": "diarrhea_character",
         "reason": "CD: 下痢の性状(水様~粘液性が多い)", "onset_day_range": None},
        {"from": "D63", "to": "S89", "from_name": "crohns_disease", "to_name": "abdominal_pain_location_detail",
         "reason": "CD: 腹痛部位(右下腹部が典型)", "onset_day_range": None},
    ]

    # UC (D353) edges
    uc_edges = [
        {"from": "D353", "to": "E01", "from_name": "ulcerative_colitis", "to_name": "temperature",
         "reason": "UC: 発熱(30-40%, 重症時)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D353", "to": "S14", "from_name": "ulcerative_colitis", "to_name": "diarrhea",
         "reason": "UC: 血性下痢(90%+, 最多症状)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D353", "to": "S26", "from_name": "ulcerative_colitis", "to_name": "bloody_stool",
         "reason": "UC: 血便(90%+, CDより高頻度)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D353", "to": "S12", "from_name": "ulcerative_colitis", "to_name": "abdominal_pain_location",
         "reason": "UC: 腹痛(70-80%, 左下腹部が典型)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D353", "to": "S17", "from_name": "ulcerative_colitis", "to_name": "weight_loss",
         "reason": "UC: 体重減少(30-40%, CDより軽度)", "onset_day_range": {"earliest": 7, "typical": 30, "latest": 90}},
        {"from": "D353", "to": "L02", "from_name": "ulcerative_colitis", "to_name": "CRP",
         "reason": "UC: CRP上昇(70-80%)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D353", "to": "L28", "from_name": "ulcerative_colitis", "to_name": "ESR",
         "reason": "UC: ESR上昇(50-60%)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D353", "to": "S46", "from_name": "ulcerative_colitis", "to_name": "anorexia",
         "reason": "UC: 食欲不振(40-50%)", "onset_day_range": {"earliest": 0, "typical": 7, "latest": 30}},
        {"from": "D353", "to": "T01", "from_name": "ulcerative_colitis", "to_name": "fever_duration",
         "reason": "UC: 慢性経過(数週~数ヶ月)", "onset_day_range": {"earliest": 7, "typical": 21, "latest": 120}},
        {"from": "D353", "to": "S07", "from_name": "ulcerative_colitis", "to_name": "fatigue",
         "reason": "UC: 全身倦怠感(50-60%)", "onset_day_range": {"earliest": 7, "typical": 14, "latest": 60}},
        {"from": "D353", "to": "L01", "from_name": "ulcerative_colitis", "to_name": "WBC",
         "reason": "UC: WBC上昇(炎症時)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D353", "to": "E02", "from_name": "ulcerative_colitis", "to_name": "heart_rate",
         "reason": "UC: 頻脈(重症/脱水時)", "onset_day_range": {"earliest": 0, "typical": 3, "latest": 14}},
        {"from": "D353", "to": "S86", "from_name": "ulcerative_colitis", "to_name": "diarrhea_character",
         "reason": "UC: 下痢の性状(血性が典型)", "onset_day_range": None},
        {"from": "D353", "to": "S89", "from_name": "ulcerative_colitis", "to_name": "abdominal_pain_location_detail",
         "reason": "UC: 腹痛部位(左下腹部が典型)", "onset_day_range": None},
    ]

    data['edges'].extend(cd_edges)
    data['edges'].extend(uc_edges)

    print(f"  Removed {len(old_edges)} old D63 edges")
    print(f"  Added {len(cd_edges)} CD edges + {len(uc_edges)} UC edges")
    print(f"  Total edges: {len(data['edges'])}")

    save_json(path, data)

def split_step3(path):
    data = load_json(path)

    # Root priors: D63 was {18_39: 0.008, 40_64: 0.003, 65_plus: 0.002}
    # CD ≈ 40% of IBD in Japan, UC ≈ 60%
    # CD: {18_39: 0.004, 40_64: 0.001, 65_plus: 0.001}
    # UC: {18_39: 0.005, 40_64: 0.002, 65_plus: 0.001}
    if 'D63' in data['root_priors']:
        data['root_priors']['D63'] = {
            "parents": ["R01"],
            "description": "CD。若年に多い(20-30代ピーク)",
            "cpt": {"18_39": 0.004, "40_64": 0.001, "65_plus": 0.001}
        }
        data['root_priors']['D353'] = {
            "parents": ["R01"],
            "description": "UC。若年に多い(20-30代ピーク)",
            "cpt": {"18_39": 0.005, "40_64": 0.002, "65_plus": 0.001}
        }
        print(f"  Split root_priors")

    # Full CPTs: D63 was parents=["R35"], {"no": 0.005, "yes": 0.015}
    # R35 = IBD_history. Split both with R35.
    if 'D63' in data['full_cpts']:
        data['full_cpts']['D63'] = {
            "parents": ["R35"],
            "description": "クローン病",
            "cpt": {"no": 0.002, "yes": 0.010}
        }
        data['full_cpts']['D353'] = {
            "parents": ["R35"],
            "description": "潰瘍性大腸炎(UC)",
            "cpt": {"no": 0.003, "yes": 0.010}
        }
        print(f"  Split full_cpts")

    save_json(path, data)

def remap_cases(path):
    """R130 is Crohn's disease → stays with D63"""
    data = load_json(path)
    cases = [c for c in data['cases'] if c.get('expected_id') == 'D63']
    print(f"  D63 cases (Crohn's, no remapping): {[c['id'] for c in cases]}")
    save_json(path, data)

def main():
    print("=" * 60)
    print("Split D63 (IBD) → D63(Crohn) + D353(UC)")
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
