#!/usr/bin/env python3
"""
統一推奨テスト — 確認推奨と反証推奨を単一ランキングに統合する実験

理論的背景:
  - 確認推奨 (IG): E[ΔH] = H_now - Σ P(s) × H_after(s)  → 期待値最適
  - 反証推奨: max_s(H_after(s))                           → 最悪ケース最適
  - 統一指標: 両方が高い検査 = 情報論的に最強

統一スコア案:
  1. IG単独 (既にEIG = 理論最適)
  2. rank fusion: rank_ig + rank_falsification の和で統合
  3. harmonic mean: 2 * IG_norm * h_increase_norm / (IG_norm + h_increase_norm)
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bn_inference import (load_json, build_model, infer, entropy,
                          next_best_test, next_best_falsification_test,
                          compute_idf_disc, IDF_DISC_POWER, CF_COVERAGE_ALPHA,
                          STEP1, STEP2, STEP3, CASES)


def unified_recommendation(evidence, risk, diseases, disease_children,
                           noisy_or, root_priors, disc, disc_power, cf_alpha,
                           top_n=10):
    """
    統一推奨: IG(確認)とmax(H_after)(反証)を一つのランキングに統合。

    Returns list of dicts with:
      - var_id, ig, h_increase, rank_ig, rank_fals, rank_sum
      - agreement: True if both ranks are in top-5
      - unified_score: harmonic mean of normalized IG and h_increase
    """
    # Get both rankings (full list)
    confirm = next_best_test(
        evidence, risk, diseases, disease_children, noisy_or, root_priors,
        disc=disc, disc_power=disc_power, cf_alpha=cf_alpha, top_n=9999)

    fals = next_best_falsification_test(
        evidence, risk, diseases, disease_children, noisy_or, root_priors,
        disc=disc, disc_power=disc_power, cf_alpha=cf_alpha, top_n=9999)

    if not confirm or not fals:
        return []

    h_now = confirm[0]["h_now"]

    # Build rank maps
    rank_ig = {item["var_id"]: i + 1 for i, item in enumerate(confirm)}
    rank_fals = {item["var_id"]: i + 1 for i, item in enumerate(fals)}

    # Build h_increase map from falsification results
    h_increase_map = {item["var_id"]: item["h_increase"] for item in fals}
    disruptive_map = {item["var_id"]: item for item in fals}

    # Normalize IG and h_increase for harmonic mean
    max_ig = max(item["ig"] for item in confirm) if confirm else 1.0
    max_h_inc = max(item["h_increase"] for item in fals) if fals else 1.0

    results = []
    for item in confirm:
        vid = item["var_id"]
        ig = item["ig"]
        h_inc = h_increase_map.get(vid, 0.0)
        r_ig = rank_ig.get(vid, 9999)
        r_fals = rank_fals.get(vid, 9999)

        # Normalized values (0-1)
        ig_norm = ig / max_ig if max_ig > 0 else 0
        h_inc_norm = h_inc / max_h_inc if max_h_inc > 0 else 0

        # Harmonic mean of normalized scores
        if ig_norm + h_inc_norm > 0:
            harmonic = 2 * ig_norm * h_inc_norm / (ig_norm + h_inc_norm)
        else:
            harmonic = 0.0

        # Rank fusion (lower = better)
        rank_sum = r_ig + r_fals

        # Agreement: both in top-5
        agreement = r_ig <= 5 and r_fals <= 5

        # Get falsification details
        fals_detail = disruptive_map.get(vid, {})

        results.append({
            "var_id": vid,
            "ig": ig,
            "h_increase": h_inc,
            "rank_ig": r_ig,
            "rank_fals": r_fals,
            "rank_sum": rank_sum,
            "harmonic": harmonic,
            "agreement": agreement,
            "h_now": h_now,
            "best_state": item["best_state"],
            "best_state_h": item["best_state_h"],
            "disruptive_state": fals_detail.get("disruptive_state", "?"),
            "disruptive_h": fals_detail.get("disruptive_h", 0),
            "state_details": item["state_details"],
        })

    # Sort by rank_sum (Borda count fusion)
    results.sort(key=lambda x: x["rank_sum"])
    return results[:top_n]


def run_case(case_id, var_lookup):
    """Run unified recommendation on a specific case."""
    step1 = load_json(STEP1)
    step2 = load_json(STEP2)
    step3 = load_json(STEP3)
    case_data = load_json(CASES)

    variables, diseases, disease_children, noisy_or, root_priors = \
        build_model(step1, step2, step3)
    disc = compute_idf_disc(step2, noisy_or, n_diseases=len(diseases))

    # Find case
    case = None
    for c in case_data["cases"]:
        if c["id"] == case_id:
            case = c
            break
    if not case:
        print(f"Case {case_id} not found")
        return

    evidence = case.get("evidence", {})
    risk = case.get("risk_factors", {})

    print("=" * 80)
    print(f"Case: {case['id']}  Source: {case.get('source', '?')}")
    print(f"Diagnosis: {case.get('final_diagnosis', '?')} ({case.get('expected_id', '?')})")
    print(f"Evidence: {len(evidence)} variables")
    print("=" * 80)

    # Current inference
    ranked = infer(evidence, risk, diseases, disease_children, noisy_or,
                   root_priors, disc=disc, disc_power=IDF_DISC_POWER,
                   cf_alpha=CF_COVERAGE_ALPHA)
    h_now = entropy(ranked)

    print(f"\nTop-5 differential (H={h_now:.2f} bits):")
    for i, (d, p) in enumerate(ranked[:5]):
        marker = " <<<" if d == case.get("expected_id") else ""
        d_name = var_lookup.get(d, {}).get("name_ja", d)
        print(f"  {i+1}. {d} {d_name}: {p*100:.1f}%{marker}")

    # Unified recommendation
    print(f"\n{'─' * 80}")
    print("統一推奨ランキング (Rank Fusion: 確認rank + 反証rank)")
    print(f"{'─' * 80}")
    print(f"{'#':>2} {'VarID':<6} {'IG':>6} {'ΔH':>6} {'R_ig':>5} {'R_fal':>5} "
          f"{'R_sum':>5} {'HM':>5} {'Agree':>5}  確認方向 → 反証方向")
    print(f"{'─' * 80}")

    unified = unified_recommendation(
        evidence, risk, diseases, disease_children, noisy_or, root_priors,
        disc=disc, disc_power=IDF_DISC_POWER, cf_alpha=CF_COVERAGE_ALPHA,
        top_n=15)

    for i, item in enumerate(unified):
        vid = item["var_id"]
        v_name = var_lookup.get(vid, {}).get("name_ja", vid)
        agree_mark = "★" if item["agreement"] else " "
        print(f"{i+1:>2} {vid:<6} {item['ig']:.3f} {item['h_increase']:+.3f} "
              f"{item['rank_ig']:>5} {item['rank_fals']:>5} "
              f"{item['rank_sum']:>5} {item['harmonic']:.3f} {agree_mark:>5}  "
              f"{item['best_state']}(H={item['best_state_h']:.2f}) → "
              f"{item['disruptive_state']}(H={item['disruptive_h']:.2f})  "
              f"{v_name}")

    # Analysis
    print(f"\n{'─' * 80}")
    print("分析:")
    n_agree = sum(1 for item in unified if item["agreement"])
    print(f"  Top-5両方一致: {n_agree}件")

    if unified:
        top1 = unified[0]
        print(f"\n  統一Top-1: {top1['var_id']} "
              f"(確認rank={top1['rank_ig']}, 反証rank={top1['rank_fals']})")
        v_name = var_lookup.get(top1['var_id'], {}).get("name_ja", top1['var_id'])
        print(f"    {v_name}")
        print(f"    IG={top1['ig']:.4f} bits (期待エントロピー削減)")
        print(f"    ΔH={top1['h_increase']:+.4f} bits (最大動揺ポテンシャル)")
        if top1["agreement"]:
            print(f"    ★ 確認・反証 両方Top-5一致 → 情報論的最強検査")


def main():
    step1 = load_json(STEP1)
    var_lookup = {v["id"]: v for v in step1["variables"]}

    if len(sys.argv) > 1:
        for case_id in sys.argv[1:]:
            run_case(case_id, var_lookup)
    else:
        # Run on a few interesting cases
        for case_id in ["R01", "R04", "R10"]:
            run_case(case_id, var_lookup)
            print("\n")


if __name__ == "__main__":
    main()
