#!/usr/bin/env python3
"""validate_edges.py - Pre-commit validation for step2/step3 consistency

Checks:
1. No disease ID has edges with conflicting disease names (wrong ID reuse)
2. All step3 parent_effects have corresponding step2 edges (orphan CPTs)
3. No duplicate edges in step2
4. step2 total_edges count matches actual edge count

Run: python3 validate_edges.py
Exit code 0 = pass, 1 = errors found
"""
import json, sys, re
from collections import defaultdict


def main():
    with open('step2_fever_edges_v4.json', encoding='utf-8') as f:
        s2 = json.load(f)
    with open('step3_fever_cpts_v2.json', encoding='utf-8') as f:
        s3 = json.load(f)

    nop = s3['noisy_or_params']
    errors = []
    warnings = []

    # === CHECK 1: Disease name consistency in step2 ===
    did_names = defaultdict(lambda: defaultdict(list))
    for e in s2['edges']:
        did = e['from']
        if did.startswith('R'):
            continue
        fname = e.get('from_name', '')
        reason = e.get('reason', '')
        if fname and fname != did and fname != '?' and 'FIXED' not in fname:
            did_names[did][fname].append((e['to'], reason))

    for did, name_dict in did_names.items():
        if len(name_dict) <= 1:
            continue
        main_name = max(name_dict, key=lambda n: len(name_dict[n]))
        for name, edges in name_dict.items():
            if name == main_name:
                continue
            mn = set(re.split(r'[\s_/()（）・]', main_name.lower())) - {'', 'acute', 'syndrome', 'disease', 'd'}
            nn = set(re.split(r'[\s_/()（）・]', name.lower())) - {'', 'acute', 'syndrome', 'disease', 'd'}
            if mn and nn and len(mn & nn) == 0:
                for vid, reason in edges:
                    errors.append(
                        f"NAME CONFLICT: {did} main='{main_name}' but edge to {vid} "
                        f"has from_name='{name}' reason: {reason[:60]}"
                    )

    # === CHECK 2: Orphan CPTs (step3 parent without step2 edge) ===
    edge_set = set()
    for e in s2['edges']:
        edge_set.add((e['from'], e['to']))

    for vid, data in nop.items():
        for did in data.get('parent_effects', {}):
            if (did, vid) not in edge_set:
                warnings.append(f"ORPHAN CPT: {did} → {vid} (step3 has CPT, step2 has no edge)")

    # === CHECK 3: Duplicate edges ===
    edge_counts = defaultdict(int)
    for e in s2['edges']:
        key = (e['from'], e['to'])
        edge_counts[key] += 1
    for (did, vid), count in edge_counts.items():
        if count > 1:
            errors.append(f"DUPLICATE EDGE: {did}→{vid} appears {count} times")

    # === CHECK 4: Edge count consistency ===
    actual = len(s2['edges'])
    declared = s2.get('total_edges', actual)
    if actual != declared:
        errors.append(f"EDGE COUNT MISMATCH: declared={declared}, actual={actual}")

    # === Report ===
    if errors:
        print(f"\n❌ {len(errors)} ERRORS:")
        for e in sorted(set(errors))[:50]:
            print(f"  {e}")

    if warnings:
        print(f"\n⚠ {len(warnings)} WARNINGS:")
        for w in sorted(set(warnings))[:50]:
            print(f"  {w}")

    if not errors and not warnings:
        print("✓ All checks passed")

    print(f"\nSummary: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
