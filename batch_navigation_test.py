#!/usr/bin/env python3
"""Batch navigation test: falsification-guided step-by-step diagnosis for all cases.

Protocol:
  1. Split evidence: initial(S/E/T/R) vs pool(L-series lab tests)
  2. Follow falsification recommendation top-1 from pool
  3. Record steps to reach correct disease at Top-1
  4. Max 15 steps
"""
import json, sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bn_inference as bn

BASE = os.path.dirname(os.path.abspath(__file__))
MAX_STEPS = 15

def run_nav(case, diseases, disease_children, noisy_or, root_priors, disc, dp, ca):
    evidence = case.get("evidence", {})
    risk = case.get("risk_factors", {})
    expected = case.get("expected_id", "OOS")
    if expected == "OOS":
        return None

    # Split: initial (S/E/T/M) vs pool (L)
    initial = {}
    pool = {}
    for vid, state in evidence.items():
        if vid.startswith("L"):
            pool[vid] = state
        else:
            initial[vid] = state

    if not pool:
        return None

    ev = dict(initial)
    steps = []
    reached = False
    reached_step = None

    for step in range(MAX_STEPS):
        ranked = bn.infer(ev, risk, diseases, disease_children, noisy_or, root_priors, disc=disc)
        h = bn.entropy(ranked)
        exp_rank = next((i+1 for i, (d,p) in enumerate(ranked) if d == expected), 999)
        exp_prob = next((p for d,p in ranked if d == expected), 0) * 100
        top1_d = ranked[0][0]

        if exp_rank == 1 and not reached:
            reached = True
            reached_step = step

        # Get falsification recommendation from pool
        fals = bn.next_best_falsification_test(
            ev, risk, diseases, disease_children, noisy_or, root_priors,
            disc=disc, disc_power=dp, cf_alpha=ca, top_n=50
        )
        next_test = None
        for f in fals:
            vid = f["var_id"]
            if vid in pool and vid not in ev:
                next_test = vid
                break

        steps.append({
            "step": step, "H": round(h, 2),
            "exp_rank": exp_rank, "exp_prob": round(exp_prob, 1),
            "top1": top1_d, "test": next_test
        })

        if not next_test:
            break
        ev[next_test] = pool[next_test]

    return {
        "case_id": case["id"],
        "expected_id": expected,
        "n_initial": len(initial),
        "n_pool": len(pool),
        "reached": reached,
        "reached_step": reached_step,
        "final_rank": steps[-1]["exp_rank"] if steps else 999,
        "final_prob": steps[-1]["exp_prob"] if steps else 0,
        "n_steps": len(steps),
        "steps": steps,
    }


def main():
    s1 = bn.load_json(os.path.join(BASE, "step1_fever_v2.7.json"))
    s2 = bn.load_json(os.path.join(BASE, "step2_fever_edges_v4.json"))
    s3 = bn.load_json(os.path.join(BASE, "step3_fever_cpts_v2.json"))
    variables, diseases, disease_children, noisy_or, root_priors = bn.build_model(s1, s2, s3)
    disc = bn.compute_idf_disc(s2, noisy_or, n_diseases=len(diseases))
    dp, ca = 0.5, 0.3

    with open(os.path.join(BASE, "real_case_test_suite.json"), "r", encoding="utf-8") as f:
        suite = json.load(f)

    cases = [c for c in suite["cases"] if c.get("in_scope", True) and c.get("expected_id", "OOS") != "OOS"]

    results = []
    for c in cases:
        r = run_nav(c, diseases, disease_children, noisy_or, root_priors, disc, dp, ca)
        if r:
            results.append(r)

    # Summary
    n = len(results)
    reached = sum(1 for r in results if r["reached"])
    not_reached = [r for r in results if not r["reached"]]
    avg_steps = sum(r["reached_step"] for r in results if r["reached"]) / reached if reached else 0

    print(f"Navigation Test Results ({datetime.now().isoformat()})")
    print(f"Total cases with lab pool: {n}")
    print(f"Reached Top-1: {reached}/{n} ({100*reached/n:.1f}%)")
    print(f"Avg steps to Top-1: {avg_steps:.2f}")
    print()

    # Step distribution
    step_dist = {}
    for r in results:
        if r["reached"]:
            s = r["reached_step"]
            step_dist[s] = step_dist.get(s, 0) + 1
    print("Step distribution (reached cases):")
    for s in sorted(step_dist.keys()):
        print(f"  Step {s}: {step_dist[s]} cases")

    print(f"\nNot reached ({len(not_reached)} cases):")
    for r in sorted(not_reached, key=lambda x: x["final_rank"]):
        print(f"  {r['case_id']:>5s} exp={r['expected_id']:>5s} final_rank={r['final_rank']} pool={r['n_pool']}")

    # Save
    output = {
        "date": datetime.now().isoformat(),
        "protocol": "falsification-guided navigation (disc_power=0.5, cf_alpha=0.3)",
        "summary": {
            "total": n, "reached": reached, "not_reached": len(not_reached),
            "reach_rate": round(100*reached/n, 1), "avg_steps": round(avg_steps, 2)
        },
        "cases": results
    }
    out_path = os.path.join(BASE, "navigation_test_batch_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
