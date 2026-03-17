#!/usr/bin/env python3
"""Split D125 (不整脈) → D125(AF) + D356(SVT) + D357(VT)

R208(AVNRT) → D356, R209(VT from cardiac sarcoidosis) → D357.
D125 has no existing AF cases → needs PMC search.

Also adds SVT and VT states to E40 (ECG).

差別化:
- E40(ECG): AF state vs SVT state vs VT state (定義的)
- E02(HR): SVT>AF>VT in typical ranges
- E16(意識): VT=失神/意識障害高, AF/SVT=低
- L53(troponin): VT>AF>SVT
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

    # Add SVT and VT states to E40
    for v in data['variables']:
        if v['id'] == 'E40':
            if 'SVT' not in v['states']:
                v['states'].append('SVT')
            if 'VT' not in v['states']:
                v['states'].append('VT')
            v['note'] = 'ECG: ST変化/AF/SVT/VT/QT延長/Brugada/右室負荷/左室肥大'
            print(f"  Added SVT/VT states to E40")
            break

    # Rename D125
    for v in data['variables']:
        if v['id'] == 'D125':
            v['name'] = 'acute_atrial_fibrillation'
            v['name_ja'] = '急性心房細動(AF)'
            v['note'] = '新規発症/発作性AF。動悸+不整脈+呼吸困難。HR irregularly irregular。ECGでAF。BNP軽度上昇。塞栓リスク。'
            print(f"  Renamed D125 → 急性心房細動(AF)")
            break

    svt = {
        "id": "D356",
        "name": "paroxysmal_SVT",
        "name_ja": "発作性上室性頻拍(SVT)",
        "category": "disease",
        "states": ["no", "yes"],
        "severity": "moderate",
        "note": "AVNRT/AVRT/AT。突然発症の規則的頻脈(HR 150-250)。動悸+呼吸困難。迷走神経刺激で停止。若年者に多い。"
    }

    vt = {
        "id": "D357",
        "name": "ventricular_tachycardia",
        "name_ja": "心室頻拍(VT)",
        "category": "disease",
        "states": ["no", "yes"],
        "severity": "critical",
        "note": "器質的心疾患(虚血/サルコイドーシス/心筋症)に伴う。wide QRS頻拍。失神/低血圧リスク高。緊急電気的除細動。"
    }

    last_disease_idx = 0
    for i, v in enumerate(data['variables']):
        if v.get('category') == 'disease':
            last_disease_idx = i
    data['variables'].insert(last_disease_idx + 1, svt)
    data['variables'].insert(last_disease_idx + 2, vt)
    print(f"  Added D356 SVT, D357 VT")

    save_json(path, data)

def split_step2(path):
    data = load_json(path)

    old_edges = [e for e in data['edges'] if e['from'] == 'D125']
    data['edges'] = [e for e in data['edges'] if e['from'] != 'D125']

    # AF (D125) edges
    af_edges = [
        {"from": "D125", "to": "S35", "from_name": "acute_atrial_fibrillation", "to_name": "palpitations",
         "reason": "AF: 動悸(80%+)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "S04", "from_name": "acute_atrial_fibrillation", "to_name": "dyspnea",
         "reason": "AF: 呼吸困難(50-70%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "S21", "from_name": "acute_atrial_fibrillation", "to_name": "chest_pain",
         "reason": "AF: 胸痛(30-40%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "E02", "from_name": "acute_atrial_fibrillation", "to_name": "heart_rate",
         "reason": "AF: 頻脈(HR 100-180, irregularly irregular)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D125", "to": "E01", "from_name": "acute_atrial_fibrillation", "to_name": "temperature",
         "reason": "AF: 通常無熱", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D125", "to": "E40", "from_name": "acute_atrial_fibrillation", "to_name": "ECG",
         "reason": "AF: ECGでAF(定義的)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D125", "to": "L51", "from_name": "acute_atrial_fibrillation", "to_name": "BNP",
         "reason": "AF: BNP上昇(頻脈性心筋障害)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "L01", "from_name": "acute_atrial_fibrillation", "to_name": "WBC",
         "reason": "AF: WBC通常正常", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D125", "to": "L02", "from_name": "acute_atrial_fibrillation", "to_name": "CRP",
         "reason": "AF: CRP通常正常", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D125", "to": "T01", "from_name": "acute_atrial_fibrillation", "to_name": "fever_duration",
         "reason": "AF: 急性(数時間~数日)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 3}},
        {"from": "D125", "to": "T02", "from_name": "acute_atrial_fibrillation", "to_name": "onset_pattern",
         "reason": "AF: 突然発症", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D125", "to": "S07", "from_name": "acute_atrial_fibrillation", "to_name": "fatigue",
         "reason": "AF: 倦怠感(30-40%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "S59", "from_name": "acute_atrial_fibrillation", "to_name": "dizziness",
         "reason": "AF: めまい(30-40%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "L04", "from_name": "acute_atrial_fibrillation", "to_name": "chest_xray",
         "reason": "AF: CXR通常正常(心不全合併なら肺うっ血)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "L53", "from_name": "acute_atrial_fibrillation", "to_name": "troponin",
         "reason": "AF: トロポニン軽度上昇(需要虚血)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "S83", "from_name": "acute_atrial_fibrillation", "to_name": "chest_pain_character",
         "reason": "AF: 胸痛性状(圧迫感)", "onset_day_range": None},
        {"from": "D125", "to": "S92", "from_name": "acute_atrial_fibrillation", "to_name": "dizziness_character",
         "reason": "AF: めまい性状", "onset_day_range": None},
        {"from": "D125", "to": "L65", "from_name": "acute_atrial_fibrillation", "to_name": "heart_failure",
         "reason": "AF: 心不全(頻脈性, 20-30%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 3}},
        {"from": "D125", "to": "S49", "from_name": "acute_atrial_fibrillation", "to_name": "orthopnea",
         "reason": "AF: 起座呼吸(心不全合併時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 3}},
        {"from": "D125", "to": "E03", "from_name": "acute_atrial_fibrillation", "to_name": "blood_pressure",
         "reason": "AF: 低血圧(fast AF時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D125", "to": "S50", "from_name": "acute_atrial_fibrillation", "to_name": "chest_pain_trigger",
         "reason": "AF: 胸痛誘発", "onset_day_range": None},
        {"from": "D125", "to": "S51", "from_name": "acute_atrial_fibrillation", "to_name": "chest_pain_radiation",
         "reason": "AF: 胸痛放散", "onset_day_range": None},
    ]

    # SVT (D356) edges
    svt_edges = [
        {"from": "D356", "to": "S35", "from_name": "paroxysmal_SVT", "to_name": "palpitations",
         "reason": "SVT: 動悸(95%+, 規則的・突然発症)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "S04", "from_name": "paroxysmal_SVT", "to_name": "dyspnea",
         "reason": "SVT: 呼吸困難(50-60%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "E02", "from_name": "paroxysmal_SVT", "to_name": "heart_rate",
         "reason": "SVT: 頻脈(HR 150-250, 規則的)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "E01", "from_name": "paroxysmal_SVT", "to_name": "temperature",
         "reason": "SVT: 通常無熱", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "E40", "from_name": "paroxysmal_SVT", "to_name": "ECG",
         "reason": "SVT: ECGでnarrow QRS頻拍", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "L01", "from_name": "paroxysmal_SVT", "to_name": "WBC",
         "reason": "SVT: WBC通常正常", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "L02", "from_name": "paroxysmal_SVT", "to_name": "CRP",
         "reason": "SVT: CRP通常正常", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "T01", "from_name": "paroxysmal_SVT", "to_name": "fever_duration",
         "reason": "SVT: 急性(数分~数時間)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "T02", "from_name": "paroxysmal_SVT", "to_name": "onset_pattern",
         "reason": "SVT: 突然発症(on/offスイッチ様)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "S59", "from_name": "paroxysmal_SVT", "to_name": "dizziness",
         "reason": "SVT: めまい(30-40%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "S21", "from_name": "paroxysmal_SVT", "to_name": "chest_pain",
         "reason": "SVT: 胸痛(20-30%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D356", "to": "L51", "from_name": "paroxysmal_SVT", "to_name": "BNP",
         "reason": "SVT: BNP軽度上昇(持続時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
    ]

    # VT (D357) edges
    vt_edges = [
        {"from": "D357", "to": "S35", "from_name": "ventricular_tachycardia", "to_name": "palpitations",
         "reason": "VT: 動悸(70-80%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "S04", "from_name": "ventricular_tachycardia", "to_name": "dyspnea",
         "reason": "VT: 呼吸困難(60-70%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "E02", "from_name": "ventricular_tachycardia", "to_name": "heart_rate",
         "reason": "VT: 頻脈(HR 150-250)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "E01", "from_name": "ventricular_tachycardia", "to_name": "temperature",
         "reason": "VT: 通常無熱", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "E40", "from_name": "ventricular_tachycardia", "to_name": "ECG",
         "reason": "VT: ECGでwide QRS頻拍", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "E16", "from_name": "ventricular_tachycardia", "to_name": "consciousness",
         "reason": "VT: 意識障害/失神(30-50%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "E03", "from_name": "ventricular_tachycardia", "to_name": "blood_pressure",
         "reason": "VT: 低血圧(50-70%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "L53", "from_name": "ventricular_tachycardia", "to_name": "troponin",
         "reason": "VT: トロポニン上昇(心筋障害)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D357", "to": "L01", "from_name": "ventricular_tachycardia", "to_name": "WBC",
         "reason": "VT: WBC通常正常", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "L02", "from_name": "ventricular_tachycardia", "to_name": "CRP",
         "reason": "VT: CRP通常正常(基礎疾患あれば上昇)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "T01", "from_name": "ventricular_tachycardia", "to_name": "fever_duration",
         "reason": "VT: 急性(数分~数時間)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "T02", "from_name": "ventricular_tachycardia", "to_name": "onset_pattern",
         "reason": "VT: 突然発症", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
        {"from": "D357", "to": "L51", "from_name": "ventricular_tachycardia", "to_name": "BNP",
         "reason": "VT: BNP上昇(心不全合併)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D357", "to": "L04", "from_name": "ventricular_tachycardia", "to_name": "chest_xray",
         "reason": "VT: CXR(心拡大/肺うっ血あり得る)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D357", "to": "S49", "from_name": "ventricular_tachycardia", "to_name": "orthopnea",
         "reason": "VT: 起座呼吸(心不全時)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 1}},
        {"from": "D357", "to": "S59", "from_name": "ventricular_tachycardia", "to_name": "dizziness",
         "reason": "VT: めまい/前失神(50-60%)", "onset_day_range": {"earliest": 0, "typical": 0, "latest": 0}},
    ]

    data['edges'].extend(af_edges)
    data['edges'].extend(svt_edges)
    data['edges'].extend(vt_edges)

    print(f"  Removed {len(old_edges)} old D125 edges")
    print(f"  Added {len(af_edges)} AF + {len(svt_edges)} SVT + {len(vt_edges)} VT edges")
    print(f"  Total edges: {len(data['edges'])}")

    save_json(path, data)

def split_step3(path):
    data = load_json(path)

    # Root priors: D125 was {male|40_64: 0.004, male|65_plus: 0.008, female|40_64: 0.003, female|65_plus: 0.006}
    # AF: dominant in elderly, SVT: younger adults, VT: all ages with cardiac disease
    if 'D125' in data['root_priors']:
        data['root_priors']['D125'] = {
            "parents": ["R02", "R01"],
            "description": "AF。高齢+男性に多い",
            "cpt": {
                "male|40_64": 0.002, "male|65_plus": 0.006,
                "female|40_64": 0.001, "female|65_plus": 0.004
            }
        }
        data['root_priors']['D356'] = {
            "parents": ["R02", "R01"],
            "description": "SVT。若年女性に多い",
            "cpt": {
                "male|18_39": 0.001, "male|40_64": 0.001, "male|65_plus": 0.001,
                "female|18_39": 0.002, "female|40_64": 0.002, "female|65_plus": 0.001
            }
        }
        data['root_priors']['D357'] = {
            "parents": ["R02", "R01"],
            "description": "VT。器質的心疾患に伴う",
            "cpt": {
                "male|18_39": 0.0005, "male|40_64": 0.001, "male|65_plus": 0.002,
                "female|18_39": 0.0003, "female|40_64": 0.0005, "female|65_plus": 0.001
            }
        }
        print(f"  Split root_priors")

    # Full CPTs: D125 was parents=["R44"], {"no": 0.003, "yes": 0.015}
    # R44 = heart failure history
    if 'D125' in data['full_cpts']:
        data['full_cpts']['D125'] = {"parents": ["R44"], "description": "急性心房細動", "cpt": {"no": 0.002, "yes": 0.010}}
        data['full_cpts']['D356'] = {"parents": [], "description": "発作性上室性頻拍(SVT)", "cpt": {"": 0.002}}
        data['full_cpts']['D357'] = {"parents": ["R44"], "description": "心室頻拍(VT)", "cpt": {"no": 0.001, "yes": 0.008}}
        print(f"  Split full_cpts")

    # noisy_or_params: Update E40 for all diseases + add SVT/VT parent effects
    nop = data.get('noisy_or_params', {})

    if 'E40' in nop:
        pe = nop['E40']['parent_effects']

        # For ALL existing E40 parents, add SVT=0 and VT=0 (they don't cause SVT/VT)
        for d_id in list(pe.keys()):
            if d_id not in ['D125']:  # D125 will be handled separately
                pe[d_id]['SVT'] = 0.0
                pe[d_id]['VT'] = 0.0

        # D125 (AF): ECG shows AF
        pe['D125'] = {
            "not_done": 0.03, "normal": 0.02, "ST_elevation": 0.02, "ST_depression": 0.08,
            "AF": 0.75, "QT_prolongation": 0.02, "Brugada_pattern": 0.01, "RVH_strain": 0.02,
            "LVH_pattern": 0.05, "SVT": 0.0, "VT": 0.0
        }

        # D356 (SVT): ECG shows SVT
        pe['D356'] = {
            "not_done": 0.03, "normal": 0.02, "ST_elevation": 0.01, "ST_depression": 0.05,
            "AF": 0.0, "QT_prolongation": 0.02, "Brugada_pattern": 0.01, "RVH_strain": 0.01,
            "LVH_pattern": 0.02, "SVT": 0.83, "VT": 0.0
        }

        # D357 (VT): ECG shows VT
        pe['D357'] = {
            "not_done": 0.03, "normal": 0.02, "ST_elevation": 0.03, "ST_depression": 0.05,
            "AF": 0.0, "QT_prolongation": 0.03, "Brugada_pattern": 0.02, "RVH_strain": 0.02,
            "LVH_pattern": 0.02, "SVT": 0.0, "VT": 0.78
        }

        print(f"  Updated E40 noisy_or_params (added SVT/VT states)")

    # Add D356/D357 parent effects for other evidence variables
    d125_vars = [var for var, params in nop.items() if 'D125' in params.get('parent_effects', {})]

    for var in d125_vars:
        if var == 'E40':
            continue  # Already handled above

        pe = nop[var]['parent_effects']
        d125_pe = pe['D125']

        # SVT: similar to AF for most things
        d356_pe = copy.deepcopy(d125_pe)
        # VT: different
        d357_pe = copy.deepcopy(d125_pe)

        if var == 'E02':  # Heart rate
            # SVT: very fast, regular
            d356_pe = {"under_100": 0.02, "100_120": 0.08, "over_120": 0.90}
            # VT: fast
            d357_pe = {"under_100": 0.05, "100_120": 0.15, "over_120": 0.80}

        elif var == 'E16':  # Consciousness
            # SVT: usually preserved
            d356_pe = {"normal": 0.90, "confused": 0.07, "obtunded": 0.03}
            # VT: syncope/LOC more common
            d357_pe = {"normal": 0.50, "confused": 0.25, "obtunded": 0.25}

        elif var == 'E03':  # Blood pressure
            # SVT: usually maintained
            d356_pe = {"normal_over_90": 0.85, "hypotension_under_90": 0.15}
            # VT: hypotension common
            d357_pe = {"normal_over_90": 0.40, "hypotension_under_90": 0.60}

        elif var == 'L53':  # Troponin
            # SVT: usually normal
            d356_pe = {"not_done": 0.25, "normal": 0.55, "mildly_elevated": 0.15, "very_high": 0.05}
            # VT: often elevated
            d357_pe = {"not_done": 0.20, "normal": 0.20, "mildly_elevated": 0.40, "very_high": 0.20}

        elif var == 'L51':  # BNP
            # SVT: mild elevation
            d356_pe = {"not_done": 0.30, "normal": 0.35, "mildly_elevated": 0.25, "very_high": 0.10}
            # VT: often elevated
            d357_pe = {"not_done": 0.25, "normal": 0.15, "mildly_elevated": 0.35, "very_high": 0.25}

        elif var == 'S04':  # Dyspnea
            d356_pe = {"absent": 0.35, "on_exertion": 0.25, "at_rest": 0.40}
            d357_pe = {"absent": 0.20, "on_exertion": 0.20, "at_rest": 0.60}

        elif var == 'S35':  # Palpitations
            d356_pe = {"absent": 0.03, "present": 0.97}
            d357_pe = {"absent": 0.15, "present": 0.85}

        pe['D356'] = d356_pe
        pe['D357'] = d357_pe

    print(f"  Added D356/D357 parent_effects for {len(d125_vars)} evidence vars")

    save_json(path, data)

def remap_cases(path):
    """R208(AVNRT) → D356, R209(VT) → D357"""
    data = load_json(path)

    for c in data['cases']:
        if c['id'] == 'R208' and c.get('expected_id') == 'D125':
            c['expected_id'] = 'D356'
            print(f"  Remapped R208 (AVNRT) → D356")
        elif c['id'] == 'R209' and c.get('expected_id') == 'D125':
            c['expected_id'] = 'D357'
            print(f"  Remapped R209 (VT) → D357")

    # Update E40 values in test cases for SVT/VT
    for c in data['cases']:
        if c['id'] == 'R208':
            # AVNRT is SVT
            if c['evidence'].get('E40') == 'AF':
                c['evidence']['E40'] = 'SVT'
                print(f"  R208: E40 AF → SVT")
        elif c['id'] == 'R209':
            # VT
            if c['evidence'].get('E40') == 'AF':
                c['evidence']['E40'] = 'VT'
                print(f"  R209: E40 AF → VT")

    save_json(path, data)

def main():
    print("=" * 60)
    print("Split D125 → D125(AF) + D356(SVT) + D357(VT)")
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
