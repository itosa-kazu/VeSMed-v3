#!/usr/bin/env python3
"""
VeSMed 疾患完全性監査スクリプト
大清洗pipeline用 — 全疾患の欠陥を一括検出してJSONレポートを生成

Usage:
  python3 audit_disease_completeness.py              # 全疾患レポート
  python3 audit_disease_completeness.py --top 20     # ワースト20のみ
  python3 audit_disease_completeness.py --disease D58 D65  # 特定疾患
  python3 audit_disease_completeness.py --summary    # サマリーのみ
"""

import json
import sys
import argparse
from collections import Counter, defaultdict

def load_data():
    s1 = json.load(open("step1_fever_v2.7.json"))
    s2 = json.load(open("step2_fever_edges_v4.json"))
    s3 = json.load(open("step3_fever_cpts_v2.json"))
    cases = json.load(open("real_case_test_suite.json"))
    if isinstance(cases, dict):
        cases = cases.get("cases", [])
    return s1, s2, s3, cases


def build_edge_map(s2):
    """disease_id -> set of target variable IDs"""
    edge_map = defaultdict(set)
    edge_reasons = defaultdict(dict)
    for e in s2["edges"]:
        edge_map[e["from"]].add(e["to"])
        edge_reasons[e["from"]][e["to"]] = e.get("reason", "")
    return edge_map, edge_reasons


def build_cpt_map(s3):
    """variable_id -> set of parent disease IDs in noisy_or_params"""
    cpt_parents = defaultdict(set)
    for var_id, params in s3.get("noisy_or_params", {}).items():
        for parent_id in params.get("parent_effects", {}):
            if parent_id.startswith("D"):
                cpt_parents[var_id].add(parent_id)
    return cpt_parents


def audit_one_disease(d_id, d_info, s1, s2, s3, cases, edge_map, cpt_parents,
                      case_ranks, in_scope_cases):
    """Audit a single disease and return a deficiency dict."""
    issues = []
    scores = {}

    # --- 1. Edge count ---
    n_edges = len(edge_map.get(d_id, set()))
    scores["edge_count"] = n_edges
    if n_edges < 10:
        issues.append(f"SPARSE_EDGES: only {n_edges} edges (want ≥10)")
    if n_edges < 5:
        issues.append(f"CRITICAL_SPARSE: only {n_edges} edges (want ≥5)")

    # --- 2. Case count ---
    d_cases = [c for c in in_scope_cases if c["expected_id"] == d_id]
    n_cases = len(d_cases)
    scores["case_count"] = n_cases
    if n_cases == 0:
        issues.append("NO_CASES: 0 test cases (want ≥3)")
    elif n_cases < 3:
        issues.append(f"FEW_CASES: only {n_cases} cases (want ≥3)")

    # --- 3. R01/R02 priors ---
    full_cpts = s3.get("full_cpts", {})
    has_r01 = False
    has_r02 = False
    if d_id in full_cpts:
        parents = full_cpts[d_id].get("parents", [])
        has_r01 = "R01" in parents
        has_r02 = "R02" in parents
    scores["has_r01"] = has_r01
    scores["has_r02"] = has_r02
    if not has_r01:
        issues.append("NO_R01: missing age prior")
    if not has_r02:
        issues.append("NO_R02: missing sex prior")

    # --- 4. Case ranks ---
    ranks = []
    for c in d_cases:
        r = case_ranks.get(c["id"])
        if r is not None:
            ranks.append(r)
    scores["ranks"] = ranks
    worst_rank = max(ranks) if ranks else None
    scores["worst_rank"] = worst_rank
    top1_count = sum(1 for r in ranks if r == 1)
    top3_count = sum(1 for r in ranks if r <= 3)
    scores["top1_rate"] = top1_count / len(ranks) if ranks else None
    scores["top3_rate"] = top3_count / len(ranks) if ranks else None

    miss_cases = [c["id"] for c, r in zip(d_cases, ranks) if r is not None and r > 3]
    if miss_cases:
        issues.append(f"MISS_CASES: {len(miss_cases)} cases rank>3: {miss_cases}")

    fatal_cases = [c["id"] for c, r in zip(d_cases, ranks) if r is not None and r > 10]
    if fatal_cases:
        issues.append(f"DEEP_MISS: {len(fatal_cases)} cases rank>10: {fatal_cases}")

    # --- 5. Edge↔CPT sync ---
    edges_no_cpt = []
    cpt_no_edge = []
    for var_id in edge_map.get(d_id, set()):
        if var_id.startswith("R"):
            continue
        nop = s3.get("noisy_or_params", {}).get(var_id, {})
        pe = nop.get("parent_effects", {})
        if d_id not in pe:
            edges_no_cpt.append(var_id)
    if edges_no_cpt:
        issues.append(f"EDGE_NO_CPT: {len(edges_no_cpt)} edges without CPT: {edges_no_cpt}")

    # CPTs without edges
    for var_id, params in s3.get("noisy_or_params", {}).items():
        pe = params.get("parent_effects", {})
        if d_id in pe and var_id not in edge_map.get(d_id, set()):
            cpt_no_edge.append(var_id)
    if cpt_no_edge:
        issues.append(f"CPT_NO_EDGE: {len(cpt_no_edge)} CPTs without edge: {cpt_no_edge}")

    # --- 6. Name conflict check ---
    names_used = set()
    for e in s2["edges"]:
        if e["from"] == d_id:
            names_used.add(e.get("from_name", ""))
    if len(names_used) > 1:
        issues.append(f"NAME_CONFLICT: multiple from_names: {names_used}")

    # --- 7. Missing evidence edges (for cases that have evidence but no edge) ---
    missing_ev_edges = set()
    for c in d_cases:
        ev = c.get("evidence", {})
        for v_id in ev:
            if not v_id.startswith("R") and v_id not in edge_map.get(d_id, set()):
                missing_ev_edges.add(v_id)
    if missing_ev_edges:
        issues.append(f"MISSING_EV_EDGES: case evidence has {len(missing_ev_edges)} vars without edges: {sorted(missing_ev_edges)}")

    # --- Compute priority score ---
    # Higher = needs more work
    priority = 0
    if n_cases == 0:
        priority += 50
    elif n_cases < 3:
        priority += 20
    if not has_r01:
        priority += 5
    if not has_r02:
        priority += 3
    if worst_rank and worst_rank > 10:
        priority += 30
    elif worst_rank and worst_rank > 3:
        priority += 15
    if edges_no_cpt:
        priority += 10 * len(edges_no_cpt)
    if cpt_no_edge:
        priority += 10 * len(cpt_no_edge)
    if missing_ev_edges:
        priority += 5 * len(missing_ev_edges)
    if len(names_used) > 1:
        priority += 20
    if n_edges < 10:
        priority += 10

    return {
        "id": d_id,
        "name": d_info.get("name", ""),
        "name_ja": d_info.get("name_ja", ""),
        "issues": issues,
        "scores": scores,
        "priority": priority,
        "is_complete": len(issues) == 0,
    }


def run_inference_ranks():
    """Run bn_inference.py and parse ranks per case."""
    import subprocess, re
    result = subprocess.run(
        ["python3", "bn_inference.py"],
        capture_output=True, text=True, timeout=300
    )
    output = result.stdout + result.stderr
    ranks = {}
    for line in output.split("\n"):
        # Format: "[ TOP1] R01  H= 1.64    r1  正解=..."
        #         "[ MISS] R123  H=6.23 r19 出力=..."
        #         "[  OOS] R02  H= 4.18   ---  正解=OOS"
        m = re.match(r"\[\s*(?:TOP1|TOP3|MISS|OOS)\]\s+(R\d+)\s+H=\s*[\d.]+\s+r(\d+)", line)
        if m:
            ranks[m.group(1)] = int(m.group(2))
        elif re.match(r"\[\s*TOP1\]\s+(R\d+)", line):
            # TOP1 always rank 1
            m2 = re.match(r"\[\s*TOP1\]\s+(R\d+)", line)
            if m2 and m2.group(1) not in ranks:
                ranks[m2.group(1)] = 1
    return ranks


def main():
    parser = argparse.ArgumentParser(description="VeSMed Disease Completeness Audit")
    parser.add_argument("--top", type=int, help="Show top N worst diseases")
    parser.add_argument("--disease", nargs="+", help="Audit specific disease IDs")
    parser.add_argument("--summary", action="store_true", help="Summary only")
    parser.add_argument("--no-inference", action="store_true",
                        help="Skip inference (faster, no rank data)")
    parser.add_argument("--output", default="disease_audit_report.json",
                        help="Output JSON file")
    args = parser.parse_args()

    print("Loading model data...")
    s1, s2, s3, cases = load_data()
    edge_map, _ = build_edge_map(s2)
    cpt_parents = build_cpt_map(s3)

    in_scope_cases = [c for c in cases
                      if c.get("in_scope", True) and c.get("expected_id", "") != "OOS"]

    diseases = {v["id"]: v for v in s1["variables"] if v["category"] == "disease"}

    # Run inference for ranks
    if args.no_inference:
        print("Skipping inference (--no-inference)")
        case_ranks = {}
    else:
        print("Running inference for case ranks...")
        case_ranks = run_inference_ranks()
        print(f"  Got ranks for {len(case_ranks)} cases")

    # Filter diseases
    if args.disease:
        target_ids = set(args.disease)
    else:
        target_ids = set(diseases.keys())

    # Audit each disease
    results = []
    for d_id in sorted(target_ids):
        if d_id not in diseases:
            print(f"WARNING: {d_id} not found in step1")
            continue
        r = audit_one_disease(d_id, diseases[d_id], s1, s2, s3, cases,
                              edge_map, cpt_parents, case_ranks, in_scope_cases)
        results.append(r)

    # Sort by priority (highest first)
    results.sort(key=lambda x: -x["priority"])

    # Filter top N
    if args.top:
        results = results[:args.top]

    # Summary stats
    complete = sum(1 for r in results if r["is_complete"])
    total = len(results)
    issue_counts = Counter()
    for r in results:
        for issue in r["issues"]:
            tag = issue.split(":")[0]
            issue_counts[tag] += 1

    summary = {
        "total_diseases": total,
        "complete": complete,
        "incomplete": total - complete,
        "completion_rate": f"{complete}/{total} ({100*complete/total:.1f}%)" if total else "N/A",
        "issue_breakdown": dict(issue_counts.most_common()),
    }

    # Print summary
    print(f"\n{'='*60}")
    print(f"VeSMed 疾患完全性監査レポート")
    print(f"{'='*60}")
    print(f"Total: {total} | Complete: {complete} | Incomplete: {total-complete}")
    print(f"Completion rate: {summary['completion_rate']}")
    print(f"\nIssue breakdown:")
    for tag, count in issue_counts.most_common():
        print(f"  {tag}: {count}")

    if not args.summary:
        print(f"\n{'='*60}")
        print(f"Top issues by priority:")
        print(f"{'='*60}")
        for r in results[:50]:
            if r["is_complete"]:
                continue
            s = r["scores"]
            rank_str = f"worst_r{s['worst_rank']}" if s['worst_rank'] else "no_cases"
            print(f"\n[P={r['priority']:3d}] {r['id']} {r['name_ja']} "
                  f"({s['edge_count']}edges, {s['case_count']}cases, {rank_str})")
            for issue in r["issues"]:
                print(f"  - {issue}")

    # Save full report
    report = {"summary": summary, "diseases": results}
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nFull report saved to {args.output}")


if __name__ == "__main__":
    main()
