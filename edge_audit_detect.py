"""Edge Audit Step 1: 全rank>=2案例の漏れ辺検出"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bn_inference import load_json, build_model, infer, compute_idf_disc

STEP1 = "step1_fever_v2.7.json"
STEP2 = "step2_fever_edges_v4.json"
STEP3 = "step3_fever_cpts_v2.json"
CASES = "real_case_test_suite.json"

def main():
    step1 = load_json(STEP1)
    step2 = load_json(STEP2)
    step3 = load_json(STEP3)
    case_data = load_json(CASES)

    variables, diseases, disease_children, noisy_or, root_priors = \
        build_model(step1, step2, step3)

    var_lookup = {v["id"]: v for v in step1["variables"]}
    disease_lookup = {d["id"]: d.get("name_ja", d.get("name", d["id"])) for d in step1["variables"] if d["category"] == "disease"}

    idf_disc = compute_idf_disc(step2, noisy_or, n_diseases=len(diseases))

    # Build edge map: disease -> set of connected variable IDs
    edge_map = {}
    for e in step2["edges"]:
        f, t = e["from"], e["to"]
        # D->V edges (disease causes symptom/lab)
        if f.startswith("D"):
            edge_map.setdefault(f, set()).add(t)
        # R->D edges (risk factor to disease)
        if t.startswith("D"):
            edge_map.setdefault(t, set()).add(f)

    in_scope = [c for c in case_data["cases"]
                if c["in_scope"] and c.get("expected_id", "OOS") != "OOS"]

    # Run inference on all cases
    results = []
    for case in in_scope:
        ev = case.get("evidence", {})
        risk = case.get("risk_factors", {})
        expected = case["expected_id"]

        ranking = infer(ev, risk, diseases, disease_children, noisy_or,
                        root_priors, disc=idf_disc,
                        disc_power=0.3, cf_alpha=2.0, prior_power=0.5)

        rank = None
        for i, (did, prob) in enumerate(ranking):
            if did == expected:
                rank = i + 1
                break

        if rank is None or rank < 2:
            continue

        # Find missing edges
        disease_edges = edge_map.get(expected, set())
        all_ev_vars = set(ev.keys()) | set(risk.keys())
        missing = all_ev_vars - disease_edges

        # Filter: only vars that could have causal edges
        # Skip T01/T02 (temporal) since many diseases share them via onset pattern
        # Actually include all - let clinical judgment decide

        if missing:
            results.append({
                "case_id": case["id"],
                "expected_id": expected,
                "disease_name": disease_lookup.get(expected, expected),
                "rank": rank,
                "top1_id": ranking[0][0],
                "top1_name": disease_lookup.get(ranking[0][0], ranking[0][0]),
                "top1_prob": f"{ranking[0][1]*100:.1f}%",
                "expected_prob": f"{ranking[rank-1][1]*100:.1f}%" if rank <= len(ranking) else "?",
                "missing_edges": sorted(missing),
                "missing_details": [(v, var_lookup[v].get("name_ja", var_lookup[v].get("name", v)))
                                    for v in sorted(missing) if v in var_lookup],
                "existing_edges": sorted(disease_edges & all_ev_vars),
            })

    # Sort by rank (worst first), then by case count per disease
    results.sort(key=lambda x: (-x["rank"], x["expected_id"]))

    # Print summary by priority
    print("=" * 100)
    print(f"Edge Audit Step 1: 漏れ辺検出 — {len(results)}案例にrank>=2 & 漏れ辺あり")
    print("=" * 100)

    # Group by priority
    fatal = [r for r in results if r["rank"] >= 20]
    high_miss = [r for r in results if 6 <= r["rank"] < 20]
    mid = [r for r in results if 4 <= r["rank"] <= 5]
    top3 = [r for r in results if r["rank"] == 3]
    top2 = [r for r in results if r["rank"] == 2]

    for label, group in [("RANK 20+ (深刻)", fatal), ("RANK 6-19 (MISS)", high_miss),
                          ("RANK 4-5 (Top-3直結)", mid), ("RANK 3", top3), ("RANK 2 (Top-1直結)", top2)]:
        if not group:
            continue
        print(f"\n{'='*80}")
        print(f"  {label}: {len(group)}件")
        print(f"{'='*80}")
        for r in group:
            print(f"\n  {r['case_id']}: rank={r['rank']}  {r['disease_name']}({r['expected_id']}) {r['expected_prob']}")
            print(f"    Top-1: {r['top1_name']}({r['top1_id']}) {r['top1_prob']}")
            print(f"    漏れ辺({len(r['missing_edges'])}): ", end="")
            for vid, vname in r['missing_details']:
                print(f"{vid}({vname}) ", end="")
            print()

    # Aggregate: which (disease, variable) pairs appear most often
    print(f"\n{'='*100}")
    print("集計: 疾患×変量ペア別の出現回数（多い順）")
    print(f"{'='*100}")

    pair_count = {}
    pair_cases = {}
    pair_ranks = {}
    for r in results:
        for vid in r['missing_edges']:
            key = (r['expected_id'], vid)
            pair_count[key] = pair_count.get(key, 0) + 1
            pair_cases.setdefault(key, []).append(r['case_id'])
            pair_ranks.setdefault(key, []).append(r['rank'])

    # Sort by: worst average rank * count
    sorted_pairs = sorted(pair_count.items(), key=lambda x: -max(pair_ranks[x[0]]) * x[1])

    for (did, vid), count in sorted_pairs[:80]:
        dname = disease_lookup.get(did, did)
        vname = var_lookup[vid].get("name_ja", var_lookup[vid].get("name", vid)) if vid in var_lookup else vid
        ranks = pair_ranks[(did, vid)]
        cases = pair_cases[(did, vid)]
        print(f"  {did}({dname}) → {vid}({vname}): {count}件 ranks={ranks} cases={cases}")

if __name__ == "__main__":
    main()
