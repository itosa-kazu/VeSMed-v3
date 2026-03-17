#!/usr/bin/env python3
"""Split D37 (細菌性腸炎) → D37(Campylobacter) + D351(Salmonella) + D352(Shigella)

R133 (Campylobacter + pancreatitis) stays with D37.

差別化:
- S26(血便): Shigella>Campylobacter>Salmonella
- 菌血症: Salmonella高, Campylobacter/Shigella低
- 腹痛部位: Campylobacter=RLQ, Shigella=LLQ, Salmonella=diffuse
- GBS合併: Campylobacter特徴
- テネスムス: Shigella特徴
"""

import json
import copy

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
        if v['id'] == 'D37':
            v['name'] = 'campylobacter_enteritis'
            v['name_ja'] = 'カンピロバクター腸炎'
            v['icd10'] = 'A04.5'
            v['key_features'] = '鶏肉摂取後2-5日。高熱+血性下痢+右下腹部痛。WBC/CRP著明上昇。GBS合併リスク。'
            print(f"  Renamed D37 → カンピロバクター腸炎")
            break

    salm = {
        "id": "D351",
        "name": "salmonella_enteritis",
        "name_ja": "サルモネラ腸炎",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "A02.0",
        "category_sub": "gastrointestinal",
        "severity": "moderate",
        "key_features": "鶏卵/食肉摂取後6-48h。高熱+水様性下痢+腹痛。菌血症リスク高(5-10%)。高齢者/免疫不全で重症化。"
    }

    shig = {
        "id": "D352",
        "name": "shigellosis",
        "name_ja": "細菌性赤痢",
        "category": "disease",
        "states": ["no", "yes"],
        "icd10": "A03",
        "category_sub": "gastrointestinal",
        "severity": "moderate",
        "key_features": "少量接種で感染(感染力強)。高熱+粘血便+テネスムス+左下腹部痛。WBC著明上昇。渡航歴重要。"
    }

    last_disease_idx = 0
    for i, v in enumerate(data['variables']):
        if v.get('category') == 'disease':
            last_disease_idx = i
    data['variables'].insert(last_disease_idx + 1, salm)
    data['variables'].insert(last_disease_idx + 2, shig)
    print(f"  Added D351 サルモネラ腸炎, D352 細菌性赤痢")

    save_json(path, data)

def split_step2(path):
    data = load_json(path)

    old_edges = [e for e in data['edges'] if e['from'] == 'D37']
    data['edges'] = [e for e in data['edges'] if e['from'] != 'D37']

    # Campylobacter (D37) edges
    campy_edges = [
        {"from": "D37", "to": "E01", "from_name": "campylobacter_enteritis", "to_name": "temperature",
         "reason": "Campylobacter: 高熱(80%+)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D37", "to": "S14", "from_name": "campylobacter_enteritis", "to_name": "diarrhea",
         "reason": "Campylobacter: 下痢(90%+, 血性が多い)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D37", "to": "S26", "from_name": "campylobacter_enteritis", "to_name": "bloody_stool",
         "reason": "Campylobacter: 血便(50-70%)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D37", "to": "S12", "from_name": "campylobacter_enteritis", "to_name": "abdominal_pain_location",
         "reason": "Campylobacter: 腹痛(80%+, 右下腹部→虫垂炎様)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D37", "to": "S13", "from_name": "campylobacter_enteritis", "to_name": "nausea_vomiting",
         "reason": "Campylobacter: 嘔気嘔吐(50-60%)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D37", "to": "L02", "from_name": "campylobacter_enteritis", "to_name": "CRP",
         "reason": "Campylobacter: CRP上昇(80%+)", "onset_day_range": {"earliest": 1, "typical": 2, "latest": 3}},
        {"from": "D37", "to": "L01", "from_name": "campylobacter_enteritis", "to_name": "WBC",
         "reason": "Campylobacter: WBC上昇(70-80%)", "onset_day_range": {"earliest": 1, "typical": 2, "latest": 3}},
        {"from": "D37", "to": "L34", "from_name": "campylobacter_enteritis", "to_name": "stool_culture",
         "reason": "Campylobacter: 便培養陽性", "onset_day_range": {"earliest": 1, "typical": 3, "latest": 5}},
        {"from": "D37", "to": "T01", "from_name": "campylobacter_enteritis", "to_name": "fever_duration",
         "reason": "Campylobacter: 急性(2-5日の潜伏後)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 5}},
        {"from": "D37", "to": "S09", "from_name": "campylobacter_enteritis", "to_name": "chills",
         "reason": "Campylobacter: 悪寒(高熱時)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D37", "to": "E09", "from_name": "campylobacter_enteritis", "to_name": "abdomen_exam",
         "reason": "Campylobacter: 腹部圧痛(右下腹部)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D37", "to": "S86", "from_name": "campylobacter_enteritis", "to_name": "diarrhea_character",
         "reason": "Campylobacter: 血性下痢", "onset_day_range": None},
        {"from": "D37", "to": "S89", "from_name": "campylobacter_enteritis", "to_name": "abdominal_pain_location_detail",
         "reason": "Campylobacter: 右下腹部痛が典型", "onset_day_range": None},
        {"from": "D37", "to": "S15", "from_name": "campylobacter_enteritis", "to_name": "flank_pain",
         "reason": "Campylobacter: 側腹部痛(腸間膜リンパ節炎)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
    ]

    # Salmonella (D351) edges
    salm_edges = [
        {"from": "D351", "to": "E01", "from_name": "salmonella_enteritis", "to_name": "temperature",
         "reason": "Salmonella: 高熱(80-90%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 2}},
        {"from": "D351", "to": "S14", "from_name": "salmonella_enteritis", "to_name": "diarrhea",
         "reason": "Salmonella: 水様性下痢(90%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D351", "to": "S26", "from_name": "salmonella_enteritis", "to_name": "bloody_stool",
         "reason": "Salmonella: 血便(20-30%, Campyloより低頻度)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 3}},
        {"from": "D351", "to": "S12", "from_name": "salmonella_enteritis", "to_name": "abdominal_pain_location",
         "reason": "Salmonella: 腹痛(70-80%, びまん性)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D351", "to": "S13", "from_name": "salmonella_enteritis", "to_name": "nausea_vomiting",
         "reason": "Salmonella: 嘔気嘔吐(70-80%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D351", "to": "L02", "from_name": "salmonella_enteritis", "to_name": "CRP",
         "reason": "Salmonella: CRP上昇(70-80%)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D351", "to": "L01", "from_name": "salmonella_enteritis", "to_name": "WBC",
         "reason": "Salmonella: WBC上昇(60-70%)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D351", "to": "L34", "from_name": "salmonella_enteritis", "to_name": "stool_culture",
         "reason": "Salmonella: 便培養陽性", "onset_day_range": {"earliest": 1, "typical": 3, "latest": 5}},
        {"from": "D351", "to": "T01", "from_name": "salmonella_enteritis", "to_name": "fever_duration",
         "reason": "Salmonella: 急性(6-48h潜伏)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 2}},
        {"from": "D351", "to": "S09", "from_name": "salmonella_enteritis", "to_name": "chills",
         "reason": "Salmonella: 悪寒(菌血症時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D351", "to": "E09", "from_name": "salmonella_enteritis", "to_name": "abdomen_exam",
         "reason": "Salmonella: 腹部圧痛(びまん性)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D351", "to": "S86", "from_name": "salmonella_enteritis", "to_name": "diarrhea_character",
         "reason": "Salmonella: 水様性下痢が典型", "onset_day_range": None},
        {"from": "D351", "to": "S89", "from_name": "salmonella_enteritis", "to_name": "abdominal_pain_location_detail",
         "reason": "Salmonella: びまん性腹痛が典型", "onset_day_range": None},
    ]

    # Shigella (D352) edges
    shig_edges = [
        {"from": "D352", "to": "E01", "from_name": "shigellosis", "to_name": "temperature",
         "reason": "赤痢: 高熱(80-90%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 2}},
        {"from": "D352", "to": "S14", "from_name": "shigellosis", "to_name": "diarrhea",
         "reason": "赤痢: 粘血便(90%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D352", "to": "S26", "from_name": "shigellosis", "to_name": "bloody_stool",
         "reason": "赤痢: 血便(80-90%, 最多)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D352", "to": "S12", "from_name": "shigellosis", "to_name": "abdominal_pain_location",
         "reason": "赤痢: 腹痛(80%+, 左下腹部が典型)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D352", "to": "S13", "from_name": "shigellosis", "to_name": "nausea_vomiting",
         "reason": "赤痢: 嘔気(40-50%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D352", "to": "L02", "from_name": "shigellosis", "to_name": "CRP",
         "reason": "赤痢: CRP著明上昇(80%+)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D352", "to": "L01", "from_name": "shigellosis", "to_name": "WBC",
         "reason": "赤痢: WBC著明上昇(80%+)", "onset_day_range": {"earliest": 0, "typical": 1, "latest": 2}},
        {"from": "D352", "to": "L34", "from_name": "shigellosis", "to_name": "stool_culture",
         "reason": "赤痢: 便培養陽性", "onset_day_range": {"earliest": 1, "typical": 3, "latest": 5}},
        {"from": "D352", "to": "T01", "from_name": "shigellosis", "to_name": "fever_duration",
         "reason": "赤痢: 急性(1-3日潜伏)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 2}},
        {"from": "D352", "to": "S09", "from_name": "shigellosis", "to_name": "chills",
         "reason": "赤痢: 悪寒(高熱時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D352", "to": "E09", "from_name": "shigellosis", "to_name": "abdomen_exam",
         "reason": "赤痢: 左下腹部圧痛", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D352", "to": "S86", "from_name": "shigellosis", "to_name": "diarrhea_character",
         "reason": "赤痢: 粘血便が典型", "onset_day_range": None},
        {"from": "D352", "to": "S89", "from_name": "shigellosis", "to_name": "abdominal_pain_location_detail",
         "reason": "赤痢: 左下腹部痛が典型", "onset_day_range": None},
    ]

    data['edges'].extend(campy_edges)
    data['edges'].extend(salm_edges)
    data['edges'].extend(shig_edges)

    print(f"  Removed {len(old_edges)} old D37 edges")
    print(f"  Added {len(campy_edges)} Campy + {len(salm_edges)} Salm + {len(shig_edges)} Shig")
    print(f"  Total edges: {len(data['edges'])}")

    save_json(path, data)

def split_step3(path):
    data = load_json(path)

    # Full CPTs: D37 was {"": 0.005}
    # Campylobacter = most common, then Salmonella, then Shigella
    if 'D37' in data['full_cpts']:
        data['full_cpts']['D37'] = {"parents": [], "description": "カンピロバクター腸炎", "cpt": {"": 0.003}}
        data['full_cpts']['D351'] = {"parents": [], "description": "サルモネラ腸炎", "cpt": {"": 0.002}}
        data['full_cpts']['D352'] = {"parents": [], "description": "細菌性赤痢", "cpt": {"": 0.001}}
        print(f"  Split full_cpts")

    # Root priors: D37 had no root_prior
    # Add: Salmonella has higher risk in elderly, Shigella more in travelers
    data['root_priors']['D351'] = {
        "parents": ["R01"],
        "description": "Salmonella。高齢者で重症化リスク",
        "cpt": {"18_39": 0.002, "40_64": 0.002, "65_plus": 0.003}
    }
    print(f"  Added root_priors for D351")

    # noisy_or_params: copy D37's to D351 and D352, with adjustments
    nop = data.get('noisy_or_params', {})

    # D37 evidence variables
    d37_vars = [var for var, params in nop.items() if 'D37' in params.get('parent_effects', {})]

    for var in d37_vars:
        pe = nop[var]['parent_effects']
        d37_pe = pe['D37']

        # Copy for Salmonella with adjustments
        d351_pe = copy.deepcopy(d37_pe)
        # Copy for Shigella with adjustments
        d352_pe = copy.deepcopy(d37_pe)

        if var == 'S26':  # bloody stool
            # Campylobacter: moderate, Salmonella: low, Shigella: highest
            pe['D37'] = {"absent": 0.3, "present": 0.7}  # Campy (unchanged)
            d351_pe = {"absent": 0.65, "present": 0.35}   # Salm: less bloody
            d352_pe = {"absent": 0.10, "present": 0.90}   # Shig: very bloody

        elif var == 'S86':  # diarrhea character
            pe['D37'] = {"watery": 0.3, "bloody": 0.7}  # Campy: bloody common
            d351_pe = {"watery": 0.8, "bloody": 0.2}     # Salm: watery dominant
            d352_pe = {"watery": 0.1, "bloody": 0.9}     # Shig: bloody/mucus

        elif var == 'S89':  # abdominal pain location
            pe['D37'] = {"epigastric": 0.05, "RUQ": 0.05, "RLQ": 0.35, "LLQ": 0.10, "suprapubic": 0.05, "diffuse": 0.40}  # Campy: RLQ
            d351_pe = {"epigastric": 0.10, "RUQ": 0.05, "RLQ": 0.10, "LLQ": 0.10, "suprapubic": 0.05, "diffuse": 0.60}   # Salm: diffuse
            d352_pe = {"epigastric": 0.05, "RUQ": 0.05, "RLQ": 0.10, "LLQ": 0.40, "suprapubic": 0.10, "diffuse": 0.30}   # Shig: LLQ

        elif var == 'S14':  # diarrhea
            d351_pe = {"absent": 0.05, "present": 0.95}  # All have diarrhea
            d352_pe = {"absent": 0.05, "present": 0.95}

        elif var == 'S13':  # nausea/vomiting
            d351_pe = {"absent": 0.15, "present": 0.85}  # Salm: more vomiting
            d352_pe = {"absent": 0.45, "present": 0.55}  # Shig: less vomiting

        pe['D351'] = d351_pe
        pe['D352'] = d352_pe

    print(f"  Copied D37 noisy_or_params to D351/D352 for {len(d37_vars)} evidence vars")

    save_json(path, data)

def remap_cases(path):
    """R133 (Campylobacter) stays with D37"""
    data = load_json(path)
    cases = [c for c in data['cases'] if c.get('expected_id') == 'D37']
    print(f"  D37 cases (Campylobacter, no remapping): {[c['id'] for c in cases]}")
    save_json(path, data)

def main():
    print("=" * 60)
    print("Split D37 → D37(Campy) + D351(Salm) + D352(Shig)")
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
