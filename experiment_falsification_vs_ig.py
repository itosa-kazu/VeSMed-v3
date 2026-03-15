#!/usr/bin/env python3
"""
Experiment: Falsification vs IG test recommendation strategy comparison.

Protocol:
  1. For each test case, split evidence into:
     - INITIAL: symptoms(S), signs(E), temporal(T), risk_factors(R) → known at presentation
     - POOL: lab tests(L) → available to be "ordered" by the system
  2. Run two strategies from the same initial state:
     A) Normal IG (entropy-decreasing): follow top-1 IG recommendation
     B) Falsification (entropy-increasing): follow top-1 falsification recommendation
  3. At each step, if the recommended test is in POOL → add it. Otherwise skip to next.
  4. Record: steps to reach correct disease at Top-1, final rank, final probability.
  5. Max 15 steps per strategy.

Output: JSON results file for reproducibility + summary statistics.

No bias: ALL in-scope cases are tested. No cherry-picking.
"""
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bn_inference as bn

BASE = os.path.dirname(os.path.abspath(__file__))
MAX_STEPS = 15


def load_all():
    s1 = bn.load_json(os.path.join(BASE, "step1_fever_v2.7.json"))
    s2 = bn.load_json(os.path.join(BASE, "step2_fever_edges_v4.json"))
    s3 = bn.load_json(os.path.join(BASE, "step3_fever_cpts_v2.json"))
    cases = bn.load_json(os.path.join(BASE, "real_case_test_suite.json"))
    return s1, s2, s3, cases


def split_evidence(case):
    """Split case evidence into initial (known at presentation) and pool (orderable tests)."""
    evidence = case.get("evidence", {})
    risk = case.get("risk_factors", {})

    initial = {}
    pool = {}
    for vid, state in evidence.items():
        if vid.startswith("L"):
            pool[vid] = state  # Lab tests go to pool
        else:
            initial[vid] = state  # S, E, T go to initial

    return initial, pool, risk


def run_strategy(strategy, initial_ev, pool, risk, expected_id,
                 diseases, disease_children, noisy_or, root_priors,
                 disc, disc_power, cf_alpha):
    """Run a test recommendation strategy and return step-by-step results."""
    ev = dict(initial_ev)
    steps = []
    reached_top1 = False
    reached_step = None

    for step in range(MAX_STEPS):
        # Current ranking
        ranked = bn.infer(ev, risk, diseases, disease_children,
                          noisy_or, root_priors, disc=disc,
                          disc_power=disc_power, cf_alpha=cf_alpha)
        h = bn.entropy(ranked)
        top1_d, top1_p = ranked[0]

        exp_rank = None
        exp_prob = 0
        for i, (d, p) in enumerate(ranked):
            if d == expected_id:
                exp_rank = i + 1
                exp_prob = p
                break

        # Check if reached Top-1
        if exp_rank == 1 and not reached_top1:
            reached_top1 = True
            reached_step = step

        # Get recommendations
        if strategy == "ig":
            recs = bn.next_best_test(
                ev, risk, diseases, disease_children, noisy_or, root_priors,
                disc=disc, disc_power=disc_power, cf_alpha=cf_alpha, top_n=9999
            )
            # Find first recommendation that's in pool and not yet observed
            next_test = None
            for rec in recs:
                vid = rec["var_id"]
                if vid in pool and vid not in ev:
                    next_test = vid
                    break
        else:  # falsification
            recs = bn.next_best_test(
                ev, risk, diseases, disease_children, noisy_or, root_priors,
                disc=disc, disc_power=disc_power, cf_alpha=cf_alpha, top_n=9999
            )
            h_now = recs[0]["h_now"] if recs else h
            # Find test with max entropy increase that's in pool
            best_vid = None
            best_h_inc = -999
            for rec in recs:
                vid = rec["var_id"]
                if vid not in pool or vid in ev:
                    continue
                max_h = max(sd["h_after"] for sd in rec["state_details"])
                h_inc = max_h - h_now
                if h_inc > best_h_inc:
                    best_h_inc = h_inc
                    best_vid = vid
            next_test = best_vid

        steps.append({
            "step": step,
            "h": round(h, 3),
            "top1": top1_d,
            "top1_prob": round(top1_p * 100, 1),
            "exp_rank": exp_rank,
            "exp_prob": round(exp_prob * 100, 2),
            "test_added": next_test,
        })

        if not next_test:
            break  # No more tests available

        ev[next_test] = pool[next_test]

    # Final state
    ranked_final = bn.infer(ev, risk, diseases, disease_children,
                            noisy_or, root_priors, disc=disc,
                            disc_power=disc_power, cf_alpha=cf_alpha)
    final_rank = None
    final_prob = 0
    for i, (d, p) in enumerate(ranked_final):
        if d == expected_id:
            final_rank = i + 1
            final_prob = p
            break

    return {
        "reached_top1": reached_top1,
        "reached_step": reached_step,
        "final_rank": final_rank,
        "final_prob": round(final_prob * 100, 2),
        "n_steps": len(steps),
        "steps": steps,
    }


def main():
    print("=" * 70)
    print("Experiment: Falsification vs IG Test Recommendation")
    print(f"Date: {datetime.now().isoformat()}")
    print("=" * 70)

    s1, s2, s3, case_data = load_all()
    variables, diseases, disease_children, noisy_or, root_priors = \
        bn.build_model(s1, s2, s3)
    disc = bn.compute_idf_disc(s2, noisy_or, n_diseases=len(diseases))

    IDF_DISC_POWER = 0.5
    CF_COVERAGE_ALPHA = 0.3

    results = []
    cases = [c for c in case_data["cases"]
             if c.get("in_scope", True) and c.get("expected_id", "OOS") != "OOS"]

    print(f"Total in-scope cases: {len(cases)}")
    print()

    for ci, case in enumerate(cases):
        cid = case["id"]
        expected = case["expected_id"]
        initial, pool, risk = split_evidence(case)

        # Skip cases with no lab tests in pool (nothing to recommend)
        if not pool:
            continue

        # Run both strategies
        ig_result = run_strategy(
            "ig", initial, pool, risk, expected,
            diseases, disease_children, noisy_or, root_priors,
            disc, IDF_DISC_POWER, CF_COVERAGE_ALPHA
        )
        fals_result = run_strategy(
            "falsification", initial, pool, risk, expected,
            diseases, disease_children, noisy_or, root_priors,
            disc, IDF_DISC_POWER, CF_COVERAGE_ALPHA
        )

        result = {
            "case_id": cid,
            "expected_id": expected,
            "n_initial": len(initial),
            "n_pool": len(pool),
            "ig": {
                "reached": ig_result["reached_top1"],
                "step": ig_result["reached_step"],
                "final_rank": ig_result["final_rank"],
                "final_prob": ig_result["final_prob"],
            },
            "fals": {
                "reached": fals_result["reached_top1"],
                "step": fals_result["reached_step"],
                "final_rank": fals_result["final_rank"],
                "final_prob": fals_result["final_prob"],
            },
        }
        results.append(result)

        # Progress indicator
        ig_mark = f"step{ig_result['reached_step']}" if ig_result["reached_top1"] else f"r{ig_result['final_rank']}"
        fals_mark = f"step{fals_result['reached_step']}" if fals_result["reached_top1"] else f"r{fals_result['final_rank']}"
        winner = ""
        if ig_result["reached_top1"] and not fals_result["reached_top1"]:
            winner = "IG"
        elif fals_result["reached_top1"] and not ig_result["reached_top1"]:
            winner = "FALS"
        elif ig_result["reached_top1"] and fals_result["reached_top1"]:
            if ig_result["reached_step"] < fals_result["reached_step"]:
                winner = "IG"
            elif fals_result["reached_step"] < ig_result["reached_step"]:
                winner = "FALS"
            else:
                winner = "TIE"

        if (ci + 1) % 10 == 0 or winner == "FALS" or winner == "IG":
            print(f"  {cid:5s} exp={expected:5s} | IG:{ig_mark:8s} FALS:{fals_mark:8s} | {winner}")

    # Summary statistics
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    n = len(results)
    ig_reached = sum(1 for r in results if r["ig"]["reached"])
    fals_reached = sum(1 for r in results if r["fals"]["reached"])
    both_reached = sum(1 for r in results if r["ig"]["reached"] and r["fals"]["reached"])
    ig_only = sum(1 for r in results if r["ig"]["reached"] and not r["fals"]["reached"])
    fals_only = sum(1 for r in results if r["fals"]["reached"] and not r["ig"]["reached"])
    neither = sum(1 for r in results if not r["ig"]["reached"] and not r["fals"]["reached"])

    print(f"Total cases with lab pool: {n}")
    print(f"IG reached Top-1:          {ig_reached}/{n} ({100*ig_reached/n:.1f}%)")
    print(f"FALS reached Top-1:        {fals_reached}/{n} ({100*fals_reached/n:.1f}%)")
    print(f"Both reached:              {both_reached}")
    print(f"IG only:                   {ig_only}")
    print(f"FALS only:                 {fals_only}")
    print(f"Neither:                   {neither}")

    # Among cases where both reached, compare speed
    both_cases = [r for r in results if r["ig"]["reached"] and r["fals"]["reached"]]
    if both_cases:
        ig_faster = sum(1 for r in both_cases if r["ig"]["step"] < r["fals"]["step"])
        fals_faster = sum(1 for r in both_cases if r["fals"]["step"] < r["ig"]["step"])
        tie = sum(1 for r in both_cases if r["ig"]["step"] == r["fals"]["step"])
        ig_avg = sum(r["ig"]["step"] for r in both_cases) / len(both_cases)
        fals_avg = sum(r["fals"]["step"] for r in both_cases) / len(both_cases)
        print(f"\nAmong {len(both_cases)} cases where both reached Top-1:")
        print(f"  IG faster:     {ig_faster}")
        print(f"  FALS faster:   {fals_faster}")
        print(f"  Tie:           {tie}")
        print(f"  IG avg steps:  {ig_avg:.2f}")
        print(f"  FALS avg steps:{fals_avg:.2f}")

    # Save full results
    output = {
        "experiment": "falsification_vs_ig",
        "date": datetime.now().isoformat(),
        "protocol": {
            "initial": "S+E+T+R (symptoms, signs, temporal, risk factors)",
            "pool": "L (lab tests) from case evidence",
            "max_steps": MAX_STEPS,
            "ig_strategy": "follow top-1 IG recommendation in pool",
            "fals_strategy": "follow top-1 max-entropy-increase recommendation in pool",
        },
        "summary": {
            "n_cases": n,
            "ig_reached": ig_reached,
            "fals_reached": fals_reached,
            "both": both_reached,
            "ig_only": ig_only,
            "fals_only": fals_only,
            "neither": neither,
        },
        "cases": results,
    }

    out_path = os.path.join(BASE, "experiment_results_fals_vs_ig.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    main()
