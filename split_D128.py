#!/usr/bin/env python3
"""Split D128 (上気道閉塞) → D128(急性喉頭蓋炎) + D358(気道異物)
Remap R226(HAE) → D185, R227(foreign body) → D358, R225(epiglottitis) stays D128

差別化:
- E01(発熱): epiglottitis=50-70%, FB=0%
- L01/L02: epiglottitis=elevated, FB=normal
- S02(咽頭痛): epiglottitis=80%+, FB=0%
- T02(発症): epiglottitis=acute, FB=sudden
- S25(嚥下困難): epiglottitis=90%, FB=variable
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
        if v['id'] == 'D128':
            v['name'] = 'acute_epiglottitis'
            v['name_ja'] = '急性喉頭蓋炎'
            v['severity'] = 'critical'
            v['note'] = '高熱+咽頭痛+嚥下困難+流涎+嗄声。WBC/CRP著明上昇。吸気性喘鳴。緊急気道確保。'
            print(f"  Renamed D128 → 急性喉頭蓋炎")
            break

    fb = {
        "id": "D358",
        "name": "airway_foreign_body",
        "name_ja": "気道異物",
        "category": "disease",
        "states": ["no", "yes"],
        "severity": "critical",
        "note": "食物/異物の気道閉塞。突然発症の呼吸困難+窒息+チアノーゼ。無熱。cafe coronary(高齢者)。"
    }

    last_disease_idx = 0
    for i, v in enumerate(data['variables']):
        if v.get('category') == 'disease':
            last_disease_idx = i
    data['variables'].insert(last_disease_idx + 1, fb)
    print(f"  Added D358 気道異物")

    save_json(path, data)

def split_step2(path):
    data = load_json(path)

    old_edges = [e for e in data['edges'] if e['from'] == 'D128']
    data['edges'] = [e for e in data['edges'] if e['from'] != 'D128']

    # Epiglottitis (D128) edges
    epi_edges = [
        {"from": "D128", "to": "E01", "from_name": "acute_epiglottitis", "to_name": "temperature",
         "reason": "喉頭蓋炎: 高熱(50-70%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 2}},
        {"from": "D128", "to": "S04", "from_name": "acute_epiglottitis", "to_name": "dyspnea",
         "reason": "喉頭蓋炎: 呼吸困難(80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "S02", "from_name": "acute_epiglottitis", "to_name": "sore_throat",
         "reason": "喉頭蓋炎: 咽頭痛(80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "E02", "from_name": "acute_epiglottitis", "to_name": "heart_rate",
         "reason": "喉頭蓋炎: 頻脈(70-80%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "E04", "from_name": "acute_epiglottitis", "to_name": "respiratory_rate",
         "reason": "喉頭蓋炎: 頻呼吸(60-70%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "E05", "from_name": "acute_epiglottitis", "to_name": "SpO2",
         "reason": "喉頭蓋炎: 低酸素(50-60%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "L01", "from_name": "acute_epiglottitis", "to_name": "WBC",
         "reason": "喉頭蓋炎: WBC著明上昇(80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "L02", "from_name": "acute_epiglottitis", "to_name": "CRP",
         "reason": "喉頭蓋炎: CRP著明上昇(80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "T01", "from_name": "acute_epiglottitis", "to_name": "fever_duration",
         "reason": "喉頭蓋炎: 超急性(数時間~1日)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "T02", "from_name": "acute_epiglottitis", "to_name": "onset_pattern",
         "reason": "喉頭蓋炎: 急性発症", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "E16", "from_name": "acute_epiglottitis", "to_name": "consciousness",
         "reason": "喉頭蓋炎: 意識障害(窒息時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "S09", "from_name": "acute_epiglottitis", "to_name": "chills",
         "reason": "喉頭蓋炎: 悪寒(細菌感染)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "E03", "from_name": "acute_epiglottitis", "to_name": "blood_pressure",
         "reason": "喉頭蓋炎: 低血圧(窒息→循環不全)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "E07", "from_name": "acute_epiglottitis", "to_name": "auscultation",
         "reason": "喉頭蓋炎: 吸気性喘鳴(stridor)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "S13", "from_name": "acute_epiglottitis", "to_name": "nausea_vomiting",
         "reason": "喉頭蓋炎: 嘔気(嚥下困難)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "S55", "from_name": "acute_epiglottitis", "to_name": "hoarseness",
         "reason": "喉頭蓋炎: 嗄声(muffled voice, 50-60%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D128", "to": "S25", "from_name": "acute_epiglottitis", "to_name": "dysphagia",
         "reason": "喉頭蓋炎: 嚥下困難(90%+)", "onset_day_range": None},
        {"from": "D128", "to": "E31", "from_name": "acute_epiglottitis", "to_name": "drooling",
         "reason": "喉頭蓋炎: 流涎(嚥下不能)", "onset_day_range": None},
    ]

    # Foreign body (D358) edges
    fb_edges = [
        {"from": "D358", "to": "S04", "from_name": "airway_foreign_body", "to_name": "dyspnea",
         "reason": "気道異物: 呼吸困難(90%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "E01", "from_name": "airway_foreign_body", "to_name": "temperature",
         "reason": "気道異物: 通常無熱", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "E02", "from_name": "airway_foreign_body", "to_name": "heart_rate",
         "reason": "気道異物: 頻脈(窒息時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "E05", "from_name": "airway_foreign_body", "to_name": "SpO2",
         "reason": "気道異物: 低酸素(窒息時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "E16", "from_name": "airway_foreign_body", "to_name": "consciousness",
         "reason": "気道異物: 意識障害(窒息→低酸素脳症)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "E03", "from_name": "airway_foreign_body", "to_name": "blood_pressure",
         "reason": "気道異物: 低血圧(窒息→循環不全)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "T01", "from_name": "airway_foreign_body", "to_name": "fever_duration",
         "reason": "気道異物: 超急性(数分)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "T02", "from_name": "airway_foreign_body", "to_name": "onset_pattern",
         "reason": "気道異物: 突然発症(食事中)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "E07", "from_name": "airway_foreign_body", "to_name": "auscultation",
         "reason": "気道異物: 喘鳴/呼吸音減弱", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "S13", "from_name": "airway_foreign_body", "to_name": "nausea_vomiting",
         "reason": "気道異物: 嘔吐(反射)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D358", "to": "L01", "from_name": "airway_foreign_body", "to_name": "WBC",
         "reason": "気道異物: WBC通常正常", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
    ]

    data['edges'].extend(epi_edges)
    data['edges'].extend(fb_edges)

    print(f"  Removed {len(old_edges)} old D128 edges")
    print(f"  Added {len(epi_edges)} epiglottitis edges + {len(fb_edges)} FB edges")
    print(f"  Total edges: {len(data['edges'])}")

    save_json(path, data)

def split_step3(path):
    data = load_json(path)

    # Full CPTs: D128 was {"": 0.003}
    if 'D128' in data['full_cpts']:
        data['full_cpts']['D128'] = {
            "parents": [],
            "description": "急性喉頭蓋炎",
            "cpt": {"": 0.002}
        }
        data['full_cpts']['D358'] = {
            "parents": [],
            "description": "気道異物",
            "cpt": {"": 0.001}
        }
        print(f"  Split full_cpts")

    # Root priors: D128 had no root_prior (just flat)
    # Add age-based priors
    data['root_priors']['D358'] = {
        "parents": ["R01"],
        "description": "気道異物。高齢者(cafe coronary)に多い",
        "cpt": {"18_39": 0.0005, "40_64": 0.001, "65_plus": 0.002}
    }
    print(f"  Added D358 root_prior")

    # noisy_or_params: Add D358 entries for its edge targets
    nop = data.get('noisy_or_params', {})
    d358_evidence = {
        'E01': {"under_37.5": 0.85, "37.5_38.0": 0.10, "38.0_39.0": 0.04, "39.0_40.0": 0.01, "over_40.0": 0.0, "hypothermia_under_35": 0.0},
        'S04': {"absent": 0.02, "on_exertion": 0.08, "at_rest": 0.90},
        'E02': {"under_100": 0.3, "100_120": 0.5, "over_120": 0.2},
        'E05': {"normal_over_96": 0.2, "mild_hypoxia_93_96": 0.3, "severe_hypoxia_under_93": 0.5},
        'E16': {"normal": 0.5, "confused": 0.25, "obtunded": 0.25},
        'E03': {"normal_over_90": 0.6, "hypotension_under_90": 0.4},
        'T01': {"under_3d": 0.95, "3d_to_1w": 0.04, "1w_to_3w": 0.01, "over_3w": 0.0},
        'T02': {"sudden": 0.85, "acute": 0.14, "subacute": 0.01, "chronic": 0.0},
        'E07': {"clear": 0.05, "crackles": 0.05, "wheezes": 0.60, "decreased_absent": 0.30},
        'S13': {"absent": 0.5, "present": 0.5},
        'L01': {"low_under_4000": 0.05, "normal_4000_10000": 0.70, "high_10000_20000": 0.20, "very_high_over_20000": 0.05},
    }

    for var, effects in d358_evidence.items():
        if var in nop:
            nop[var]['parent_effects']['D358'] = effects
        # If var not in nop, that's ok - the edge alone handles it

    print(f"  Added D358 noisy_or_params for {len(d358_evidence)} evidence vars")

    save_json(path, data)

def remap_cases(path):
    """R225(epiglottitis) stays D128, R226(HAE)→D185, R227(FB)→D358"""
    data = load_json(path)

    for c in data['cases']:
        if c['id'] == 'R226' and c.get('expected_id') == 'D128':
            c['expected_id'] = 'D185'
            print(f"  Remapped R226 (HAE) → D185")
        elif c['id'] == 'R227' and c.get('expected_id') == 'D128':
            c['expected_id'] = 'D358'
            print(f"  Remapped R227 (foreign body) → D358")

    print(f"  R225 stays D128 (epiglottitis)")

    save_json(path, data)

def main():
    print("=" * 60)
    print("Split D128 → D128(epiglottitis) + D358(FB) + R226→D185")
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
