#!/usr/bin/env python3
"""
VeSMed Variable Audit Script
Usage:
  python audit_variables.py                # Run all phases
  python audit_variables.py --phase 1      # Structural integrity only
  python audit_variables.py --phase 2      # Atomicity only
  python audit_variables.py --phase 3      # OPQRST completeness
  python audit_variables.py --phase 5      # Disease-driven (low-edge)
"""

import json, os, re, sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))

def load():
    s1 = json.load(open(os.path.join(BASE, 'step1_fever_v2.7.json')))
    s2 = json.load(open(os.path.join(BASE, 'step2_fever_edges_v4.json')))
    s3 = json.load(open(os.path.join(BASE, 'step3_fever_cpts_v2.json')))
    return s1, s2, s3

def phase1(s1, s2, s3):
    """Phase 1: Structural Integrity"""
    print("=" * 70)
    print("PHASE 1: 構造的整合性 (Structural Integrity)")
    print("=" * 70)
    issues = 0

    # 1.1 Duplicate IDs
    ids = [v['id'] for v in s1['variables']]
    dupes = set(x for x in ids if ids.count(x) > 1)
    if dupes:
        print(f"\n[1.1] FAIL: ID重複 {dupes}")
        issues += len(dupes)
    else:
        print(f"\n[1.1] OK: ID重複なし ({len(ids)} variables)")

    # 1.2 Main variables should be binary (with exceptions)
    severity_ok = ['mild','moderate','severe','low','normal','high','under','over',
                   'not_done','not_assessed','hypothermia','localized','generalized',
                   'presyncope','syncope','stress','urge','overflow','functional',
                   'unilateral','bilateral','on_exertion','at_rest',
                   'pre_existing','new','excessive','hyperactive','hypoactive','oliguria','anuria',
                   'S3','S4','both','transient','persistent',
                   'heat_intolerance','cold_intolerance',
                   'binocular','monocular','horizontal','vertical','rotatory',
                   'lung','bone','liver','brain','multiple',
                   'acute','subacute','chronic']
    
    mixed = []
    for v in s1['variables']:
        if v['id'].startswith('D') or v['id'].startswith('M'):
            continue
        # L(検査) and E(徴候) are exam results — always deterministic, skip
        if v['id'].startswith('L') or v['id'].startswith('E'):
            continue
        states = v['states']
        if 'absent' not in states and 'normal' not in states:
            continue
        non_base = [s for s in states if s not in ('absent','normal')]
        if len(non_base) <= 1:
            continue
        is_ok = all(any(p in s.lower() for p in severity_ok) for s in non_base)
        if not is_ok:
            # Check if it's a satellite (no absent allowed)
            mixed.append(v)

    if mixed:
        print(f"\n[1.2] WARN: {len(mixed)} variables with absent+descriptive states:")
        for v in mixed[:20]:
            print(f"      {v['id']:6s} {v.get('name_ja',''):35s} {v['states']}")
        issues += len(mixed)
    else:
        print(f"\n[1.2] OK: 全主変数がbinary or severity/laterality scale")

    # 1.3 Satellite variables should NOT have absent/not_applicable
    # Heuristic: variables that are NOT targets of edges from diseases are likely satellites
    edge_targets = set(e['to'] for e in s2['edges'])
    satellites_with_absent = []
    for v in s1['variables']:
        if v['id'].startswith('D') or v['id'].startswith('M'):
            continue
        if v['id'] not in edge_targets:
            # Likely a satellite (no disease points to it yet)
            if 'absent' in v['states'] or 'not_applicable' in v['states']:
                # Exception: if it's a new variable with no edges yet, skip
                pass  # Can't reliably detect satellites without edges
        if 'not_applicable' in v['states']:
            satellites_with_absent.append(v)

    if satellites_with_absent:
        print(f"\n[1.3] WARN: {len(satellites_with_absent)} variables with 'not_applicable':")
        for v in satellites_with_absent:
            print(f"      {v['id']:6s} {v.get('name_ja','')}")
        issues += len(satellites_with_absent)
    else:
        print(f"\n[1.3] OK: not_applicableなし")

    # 1.4 Lab variables should have not_done
    labs_without_not_done = []
    for v in s1['variables']:
        if not v['id'].startswith('L'):
            continue
        states = v['states']
        # Some labs are always done (CBC components, basic vitals) — skip these
        always_done = ['L01','L02','L11','L14','L15','L16','L17','L28','L36',
                       'L44','L54','L55','L84','L85','L86','L87','L93','L94']
        if v['id'] in always_done:
            continue
        if 'not_done' not in states and 'not_assessed' not in states:
            labs_without_not_done.append(v)

    if labs_without_not_done:
        print(f"\n[1.4] INFO: {len(labs_without_not_done)} lab variables without 'not_done':")
        for v in labs_without_not_done[:10]:
            print(f"      {v['id']:6s} {v.get('name_ja',''):35s} {v['states']}")
    else:
        print(f"\n[1.4] OK: 全検査変数にnot_done/not_assessedあり")

    print(f"\n>>> Phase 1 issues: {issues}")
    return issues


def phase2(s1, s2, s3):
    """Phase 2: Atomicity"""
    print("\n" + "=" * 70)
    print("PHASE 2: 原子性 (Atomicity)")
    print("=" * 70)
    issues = 0

    # 2.1 Names with / ・ AND
    separators = []
    for v in s1['variables']:
        if v['id'].startswith('D'):
            continue
        name = v.get('name_ja', v['name'])
        # Check for separators that might indicate merged concepts
        if any(sep in name for sep in ['/', '・', ' and ', '＋']):
            # Whitelist: known OK patterns
            ok_patterns = [
                # Lab test names (composite tests, abbreviations)
                '肋骨脊柱角', 'AST/ALT', 'Na/K', 'PT/INR', 'Fe/TIBC',
                'VMA/HVA', 'C3/C4', 'RPR/TPHA', 'PSA/AFP/CEA',
                'NT-proBNP', 'BNP/NT', 'sIL-2R', 'IL-6/sIL-2R',
                'β-D', 'IGF-1/GH', 'III音/IV音', 'dsDNA', 'CCP',
                'Trousseau/Chvostek', 'Cullen/Grey', 'Kernig/Brudzinski', 'ステント/人工', '焦燥・興奮',
                'Roth', 'ADAMTS13', 'ステロイド', 'ステント', '嚥下障害', 'CK', 'ACE', 'AFP', 'ESR', 'ABI', 'BUN', 'MCV', 'ぶどう膜', '直接/間接', 'RF', 'CDトキシン', 'アミラーゼ/リパーゼ',
                '蛋白電気泳動/免疫固定', 'トロポニン', '経腹/経膣',
                'CT/PET', '直接/間接', 'ICD', 'ペースメーカー',
                '血液ガス/乳酸',
                # Sign/symptom compound names (same clinical concept)
                '人工弁・人工関節', '感染流行・濃厚接触', '外傷・創傷',
                'タンポン・腟内', '側腹部痛・腰背部', '顔面痛・圧迫',
                '血便/粘血便', '股関節/鼠径', '発赤・熱感',
                '脈拍左右差/血管雑音', '手掌・足底', '拡張期雑音/opening',
                '増悪/緩和', '爪/指', '色/性状', '不安/焦燥',
                '小脳徴候', '臥床/不動', '筋痙攣/こむら返り',
                '経口避妊薬/HRT', '記憶/認知', '粘膜出血',
                '紫斑/点状', 'AIDS期', '治療中',
                # Risk factor descriptions
                '免疫不全', '動物接触', '誤嚥リスク',
                # Exam names
                '眼症状', '体内デバイス', 'ステント', '焦燥・興奮',
            ]
            if not any(p in name for p in ok_patterns):
                separators.append((v['id'], name))

    if separators:
        print(f"\n[2.1] REVIEW: {len(separators)} variables with separators in name:")
        for vid, name in separators:
            print(f"      {vid:6s} {name}")
        issues += len(separators)
    else:
        print(f"\n[2.1] OK: 分離候補なし")

    # 2.2 Names with parenthetical cause/mechanism
    cause_parens = []
    for v in s1['variables']:
        if v['id'].startswith('D'):
            continue
        name = v.get('name_ja', v['name'])
        # Find (cause) patterns
        m = re.search(r'[（(].+[）)]', name)
        if m:
            content = m.group()
            # Whitelist: measurement units, abbreviations, examples
            ok = ['JVD', 'CRT', 'OPQRST', 'BMI', 'ISTH', 'NYHA',
                  'Na/K', 'AST/ALT', 'Fe/TIBC', 'CT/PET', 'PSA',
                  'I/T', 'gallop', '片麻痺', '経腹', 'うっ血',
                  '紫斑', '歯肉', '痛み', '腫瘤', '立ちくらみ',
                  'しゃっくり', '暑がり', '寒がり', '記憶以外',
                  'しぶり腹', '病的反射',
                  # Abbreviation explanations
                  'CK', 'ACE', 'AFP', 'ESR', 'EBV', 'SAH',
                  'TP', 'RPR', 'MMR', 'Hb', 'MCV', 'BUN',
                  'C3', 'RF', 'ABI', 'hCG', 'IGF', 'VMA',
                  # Clarification parentheticals
                  '地域別', '30日以内', '化学療法後', '家畜',
                  '痂皮', '好中球数', '脊椎レベル', '骨溶解',
                  '収縮期', '腎機能', '妊娠検査', '臨床評価',
                  '検査所見', '相対的', '異常分泌', '指鼻',
                  '冷え不耐', '熱不耐', 'タール', 'CD4',
                  '化学療法/放射線', '寛解', 'trimester',
                  'ショック', 'ステロイド', 'ステント', '嚥下障害', 'ぶどう膜炎', '足関節', '直接/間接', '平均赤血球']
            if not any(p in content for p in ok):
                cause_parens.append((v['id'], name))

    if cause_parens:
        print(f"\n[2.2] REVIEW: {len(cause_parens)} variables with parenthetical content:")
        for vid, name in cause_parens:
            print(f"      {vid:6s} {name}")
    else:
        print(f"\n[2.2] OK: 原因名混入なし")

    print(f"\n>>> Phase 2 issues: {issues}")
    return issues


def phase3(s1, s2, s3):
    """Phase 3: OPQRST Completeness for major symptoms"""
    print("\n" + "=" * 70)
    print("PHASE 3: OPQRST完全性 (OPQRST Completeness)")
    print("=" * 70)

    edge_count = Counter(e['to'] for e in s2['edges'])
    name_map = {v['id']: v.get('name_ja', v['name']) for v in s1['variables']}

    # Major symptoms (15+ edges, S-prefix, binary)
    major_symptoms = []
    for v in s1['variables']:
        if not v['id'].startswith('S'):
            continue
        if edge_count.get(v['id'], 0) >= 15:
            major_symptoms.append((v['id'], name_map.get(v['id'], ''), edge_count[v['id']]))

    major_symptoms.sort(key=lambda x: -x[2])

    # Known satellite mappings
    satellite_map = {
        'S05': {'Q': 'S60', 'P': 'S68', 'T': 'S69'},
        'S12': {'Q': 'S61', 'P': 'S62', 'R': 'S89', 'S': 'S64', 'T': 'S65'},
        'S21': {'Q': 'S83', 'P': 'S50', 'R': 'S51', 'S': 'S181', 'T': 'S182'},
        'S01': {'Q': 'S84', 'P': 'S179', 'T': 'S47'},
        'S04': {'Q': 'S81', 'P': 'S178', 'T': 'S177'},
        'S14': {'Q': 'S86', 'P': 'S174', 'T': 'S173'},
        'S08': {'Q': 'S184', 'P': 'S185', 'R': 'S90'},
        'S42': {'Q': 'S170', 'P': 'S171', 'T': 'S172'},
        'S52': {'T': 'S175'},
        'S13': {'P': 'S176'},
        'S06': {'R': 'S180'},
        'S17': {'T': 'S183'},
        'S15': {'R': 'S186'},
        'S53': {'T': 'S187'},
    }

    print(f"\n{'ID':6s} {'Name':25s} {'Edges':>5s}  O  P  Q  R  S  T")
    print("-" * 70)
    for sid, name, cnt in major_symptoms:
        sats = satellite_map.get(sid, {})
        o = 'T02' if True else '-'
        p = sats.get('P', ' - ')
        q = sats.get('Q', ' - ')
        r = sats.get('R', ' - ')
        s = sats.get('S', ' - ')
        t = sats.get('T', ' - ')
        print(f"{sid:6s} {name[:25]:25s} {cnt:5d}  {o:3s} {p:3s} {q:3s} {r:3s} {s:3s} {t:3s}")

    print(f"\n(T02=global onset, '-'=missing satellite)")


def phase5(s1, s2, s3):
    """Phase 5: Disease-driven — show low-edge diseases"""
    print("\n" + "=" * 70)
    print("PHASE 5: 疾患逆引き — Edge不足疾患")
    print("=" * 70)

    name_map = {v['id']: v.get('name_ja', v['name']) for v in s1['variables']}
    edge_count = Counter(e['from'] for e in s2['edges'] if e['from'].startswith('D'))

    diseases = sorted(
        [(did, name_map.get(did, ''), edge_count.get(did, 0))
         for did in name_map if did.startswith('D')],
        key=lambda x: x[2]
    )

    print(f"\nBottom 30 diseases by edge count:")
    print(f"{'ID':6s} {'Name':40s} {'Edges':>5s}")
    print("-" * 55)
    for did, name, cnt in diseases[:30]:
        print(f"{did:6s} {name[:40]:40s} {cnt:5d}")

    # Stats
    vals = [x[2] for x in diseases]
    print(f"\nEdge statistics: min={min(vals)}, max={max(vals)}, "
          f"median={sorted(vals)[len(vals)//2]}, mean={sum(vals)/len(vals):.1f}")
    print(f"<5 edges: {sum(1 for v in vals if v < 5)}")
    print(f"<10 edges: {sum(1 for v in vals if v < 10)}")
    print(f"<15 edges: {sum(1 for v in vals if v < 15)}")


if __name__ == "__main__":
    s1, s2, s3 = load()

    phases = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not phases or '--phase' not in phases:
        # Run all
        phase1(s1, s2, s3)
        phase2(s1, s2, s3)
        phase3(s1, s2, s3)
        phase5(s1, s2, s3)
    else:
        idx = phases.index('--phase')
        if idx + 1 < len(phases):
            p = phases[idx + 1]
            if p == '1': phase1(s1, s2, s3)
            elif p == '2': phase2(s1, s2, s3)
            elif p == '3': phase3(s1, s2, s3)
            elif p == '5': phase5(s1, s2, s3)
