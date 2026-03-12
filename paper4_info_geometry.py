#!/usr/bin/env python3
"""
Paper 4: 因果グラフ → 情報幾何
Causal BN posterior dynamics on the statistical manifold.

3つの実用機能:
  1. 疾患間の診断距離 (Fisher-Rao distance)
  2. 辺欠損の自動検出 (距離異常 → NO EDGE警告)
  3. Next Best Test 推奨 (幾何学的information gain)

Usage:
  python paper4_info_geometry.py                    # 全分析
  python paper4_info_geometry.py --trajectory IE    # IE scenario の診断軌跡
  python paper4_info_geometry.py --distance         # 疾患間距離行列
  python paper4_info_geometry.py --next-test E15=new S01=present  # 次の検査推奨
  python paper4_info_geometry.py --missing-edges    # 辺欠損検出
"""

import json
import math
import os
import argparse
from collections import defaultdict
from bn_inference import build_model, infer, entropy, load_json

BASE = os.path.dirname(os.path.abspath(__file__))
STEP1 = os.path.join(BASE, "step1_fever_v2.7.json")
STEP2 = os.path.join(BASE, "step2_fever_edges_v4.json")
STEP3 = os.path.join(BASE, "step3_fever_cpts_v2.json")

# ─── Load model ──────────────────────────────────────────────────────
step1 = load_json(STEP1)
step2 = load_json(STEP2)
step3 = load_json(STEP3)
variables, diseases, disease_children, noisy_or, root_priors = build_model(step1, step2, step3)
var_lookup = {v["id"]: v for v in step1["variables"]}

# Filter to actual diseases (exclude M01)
disease_ids = [d for d in diseases if d != "M01"]


# ═══════════════════════════════════════════════════════════════════════
# Core: Fisher-Rao geometry on the probability simplex
# ═══════════════════════════════════════════════════════════════════════

def ranked_to_dict(ranked):
    """Convert [(d_id, prob), ...] to {d_id: prob}."""
    return {d: p for d, p in ranked}


def fisher_rao_distance(p_dict, q_dict):
    """
    Fisher-Rao distance on the categorical simplex.
    d_FR(p, q) = 2 * arccos( Σ √(p_i * q_i) )

    This is the geodesic distance on the statistical manifold.
    Range: [0, π]. 0 = identical, π = orthogonal (no overlap).
    """
    keys = set(p_dict.keys()) | set(q_dict.keys())
    bc = 0.0  # Bhattacharyya coefficient
    for k in keys:
        pi = p_dict.get(k, 0.0)
        qi = q_dict.get(k, 0.0)
        if pi > 0 and qi > 0:
            bc += math.sqrt(pi * qi)
    # Clamp for numerical stability
    bc = min(bc, 1.0)
    return 2.0 * math.acos(bc)


def push_vector(p_dict, q_dict):
    """
    The "push" of an observation: log-ratio of posteriors.
    In natural parameter space: θ_after - θ_before = log(q/p).
    Returns dict of {disease: push_magnitude}.
    """
    push = {}
    for d in p_dict:
        pi = max(p_dict.get(d, 1e-15), 1e-15)
        qi = max(q_dict.get(d, 1e-15), 1e-15)
        push[d] = math.log(qi) - math.log(pi)
    return push


# ═══════════════════════════════════════════════════════════════════════
# 機能1: 診断軌跡 (Diagnostic Trajectory)
# ═══════════════════════════════════════════════════════════════════════

def diagnostic_trajectory(evidence_steps, risk=None):
    """
    Compute the posterior trajectory as evidence is added step by step.

    Args:
        evidence_steps: list of (var_id, state) tuples in order
        risk: risk factor evidence dict

    Returns:
        list of trajectory points, each containing:
        - step, evidence added, posterior dict, entropy, Fisher-Rao distance from previous
    """
    if risk is None:
        risk = {}

    trajectory = []
    cumulative_evidence = {}

    # Step 0: prior only
    ranked = infer({}, risk, disease_ids, disease_children, noisy_or, root_priors)
    p_dict = ranked_to_dict(ranked)
    h = entropy(ranked)
    trajectory.append({
        "step": 0,
        "added": ("prior", "—"),
        "evidence": {},
        "posterior": p_dict,
        "entropy": h,
        "fr_distance": 0.0,
        "top3": ranked[:3],
    })

    prev_dict = p_dict

    for i, (var_id, state) in enumerate(evidence_steps):
        cumulative_evidence[var_id] = state
        ranked = infer(cumulative_evidence, risk, disease_ids, disease_children, noisy_or, root_priors)
        p_dict = ranked_to_dict(ranked)
        h = entropy(ranked)
        fr_dist = fisher_rao_distance(prev_dict, p_dict)

        trajectory.append({
            "step": i + 1,
            "added": (var_id, state),
            "evidence": dict(cumulative_evidence),
            "posterior": p_dict,
            "entropy": h,
            "fr_distance": fr_dist,
            "top3": ranked[:3],
        })
        prev_dict = p_dict

    return trajectory


def print_trajectory(trajectory, title=""):
    """Pretty-print a diagnostic trajectory."""
    if title:
        print(f"\n{'='*90}")
        print(f"  診断軌跡: {title}")
        print(f"{'='*90}")

    print(f"{'Step':>4s}  {'Added':30s}  {'H':>5s}  {'d_FR':>6s}  {'Cumul':>6s}  Top-3")
    print("-" * 110)

    total_dist = 0.0
    for pt in trajectory:
        var_id, state = pt["added"]
        if var_id == "prior":
            added_str = "(事前確率)"
        else:
            name_ja = var_lookup.get(var_id, {}).get("name_ja", var_id)
            added_str = f"{name_ja}={state}"

        total_dist += pt["fr_distance"]

        top3_str = " | ".join(
            f"{var_lookup.get(d,{}).get('name_ja',d)[:10]} {p*100:5.1f}%"
            for d, p in pt["top3"]
        )

        print(f"{pt['step']:4d}  {added_str:30s}  {pt['entropy']:5.2f}  "
              f"{pt['fr_distance']:6.3f}  {total_dist:6.3f}  {top3_str}")


# ═══════════════════════════════════════════════════════════════════════
# 機能2: 疾患間の診断距離 (Disease Diagnostic Distance)
# ═══════════════════════════════════════════════════════════════════════

def compute_disease_distance_via_profile(d1, d2):
    """
    Compute diagnostic distance between two diseases.

    Method: For each observable variable with edges from both diseases,
    compute the CPT profile (probability distribution over states).
    The distance = average Fisher-Rao distance across their CPT profiles.

    Small distance → hard to differentiate → might need biopsy or specific test.
    """
    params_with_both = []

    for var_id, params in noisy_or.items():
        pe = params.get("parent_effects", {})
        if d1 in pe and d2 in pe:
            states = params["states"]
            p1 = pe[d1]
            q1 = pe[d2]
            # Normalize to probability distributions
            sum_p = sum(p1.get(s, 0.001) for s in states)
            sum_q = sum(q1.get(s, 0.001) for s in states)
            p_norm = {s: p1.get(s, 0.001) / sum_p for s in states}
            q_norm = {s: q1.get(s, 0.001) / sum_q for s in states}
            fr = fisher_rao_distance(p_norm, q_norm)
            params_with_both.append((var_id, fr))

    if not params_with_both:
        return None, []

    avg_dist = sum(d for _, d in params_with_both) / len(params_with_both)
    return avg_dist, params_with_both


def compute_posterior_distance(d1, d2):
    """
    Alternative: compute distance between the posteriors that each disease
    would produce if it were the true diagnosis.

    For disease d: generate "ideal evidence" = all children set to their
    most likely state under d. Then compute posterior. Compare posteriors.
    """
    # Get children of each disease
    ch1 = disease_children.get(d1, set())
    ch2 = disease_children.get(d2, set())

    # Generate ideal evidence for d1
    ev1 = {}
    for var_id in ch1:
        params = noisy_or.get(var_id)
        if params is None:
            continue
        pe = params.get("parent_effects", {})
        if d1 not in pe:
            continue
        # Most likely non-absent state
        d_probs = pe[d1]
        states = params["states"]
        best_state = max(states, key=lambda s: d_probs.get(s, 0))
        if best_state != states[0]:  # skip if most likely is "absent"
            ev1[var_id] = best_state

    # Generate ideal evidence for d2
    ev2 = {}
    for var_id in ch2:
        params = noisy_or.get(var_id)
        if params is None:
            continue
        pe = params.get("parent_effects", {})
        if d2 not in pe:
            continue
        d_probs = pe[d2]
        states = params["states"]
        best_state = max(states, key=lambda s: d_probs.get(s, 0))
        if best_state != states[0]:
            ev2[var_id] = best_state

    # Compute posteriors
    ranked1 = infer(ev1, {}, disease_ids, disease_children, noisy_or, root_priors)
    ranked2 = infer(ev2, {}, disease_ids, disease_children, noisy_or, root_priors)

    p1 = ranked_to_dict(ranked1)
    p2 = ranked_to_dict(ranked2)

    return fisher_rao_distance(p1, p2), ev1, ev2


# ═══════════════════════════════════════════════════════════════════════
# 機能3: Next Best Test (情報幾何的推奨)
# ═══════════════════════════════════════════════════════════════════════

def next_best_test(current_evidence, risk=None, top_n=15):
    """
    For each unobserved variable, compute:
    1. Expected entropy after observing it (averaging over possible states)
    2. Expected Fisher-Rao distance (how far posterior would move)

    Rank by expected information gain.

    Returns sorted list of (var_id, expected_ig, expected_fr_dist, detail).
    """
    if risk is None:
        risk = {}

    # Current posterior
    ranked_now = infer(current_evidence, risk, disease_ids, disease_children, noisy_or, root_priors)
    p_now = ranked_to_dict(ranked_now)
    h_now = entropy(ranked_now)

    results = []

    for var_id, params in noisy_or.items():
        if var_id in current_evidence:
            continue
        # Skip disease nodes
        if var_id.startswith("D") or var_id == "M01":
            continue
        # Skip risk factors (R-prefix) — they're background, not tests
        if var_id.startswith("R"):
            continue

        states = params["states"]
        leak = params["leak"]

        # For each possible state, compute what the posterior would be
        expected_h = 0.0
        expected_fr = 0.0
        state_details = []

        # Estimate P(state) under current posterior (marginal)
        # P(v=s) ≈ Σ_d P(d) * P(v=s|d) where P(v=s|d) comes from noisy-OR
        state_probs = {}
        pe = params.get("parent_effects", {})
        for s in states:
            p_s = 0.0
            for d_id in disease_ids:
                p_d = p_now.get(d_id, 0.0)
                if d_id in pe:
                    p_vs_d = pe[d_id].get(s, leak.get(s, 1.0 / len(states)))
                else:
                    p_vs_d = leak.get(s, 1.0 / len(states))
                p_s += p_d * p_vs_d
            state_probs[s] = max(p_s, 1e-10)

        # Normalize
        total = sum(state_probs.values())
        for s in state_probs:
            state_probs[s] /= total

        for s in states:
            trial_evidence = dict(current_evidence)
            trial_evidence[var_id] = s
            ranked_trial = infer(trial_evidence, risk, disease_ids, disease_children, noisy_or, root_priors)
            p_trial = ranked_to_dict(ranked_trial)
            h_trial = entropy(ranked_trial)
            fr_trial = fisher_rao_distance(p_now, p_trial)

            weight = state_probs[s]
            expected_h += weight * h_trial
            expected_fr += weight * fr_trial
            state_details.append((s, weight, h_trial, fr_trial))

        ig = h_now - expected_h
        results.append({
            "var_id": var_id,
            "name_ja": var_lookup.get(var_id, {}).get("name_ja", var_id),
            "category": var_lookup.get(var_id, {}).get("category", ""),
            "expected_ig": ig,
            "expected_fr": expected_fr,
            "state_details": state_details,
        })

    results.sort(key=lambda x: -x["expected_ig"])
    return results[:top_n], h_now


# ═══════════════════════════════════════════════════════════════════════
# 辺欠損検出 (Missing Edge Detection)
# ═══════════════════════════════════════════════════════════════════════

def detect_missing_edges():
    """
    Detect potential missing edges using real test cases (no model self-bias).

    Logic: For each real case where rank > 3, the model confused the correct
    disease with the top-ranked disease. Analyze WHY by comparing their edges
    and computing Fisher-Rao distance under that case's evidence.

    This uses external clinical data, not model-generated evidence.
    """
    CASES = os.path.join(BASE, "real_case_test_suite.json")
    case_data = load_json(CASES)

    confusions = []

    for case in case_data["cases"]:
        expected = case["expected_id"]
        if expected == "OOS" or not case["in_scope"]:
            continue

        ev = case.get("evidence", {})
        risk = case.get("risk_factors", {})
        ranked = infer(ev, risk, disease_ids, disease_children, noisy_or, root_priors)
        p_dict = ranked_to_dict(ranked)

        # Find rank of expected disease
        rank = None
        for i, (d, p) in enumerate(ranked):
            if d == expected:
                rank = i + 1
                break

        if rank is None or rank <= 3:
            continue  # Not a problem case

        top1_id, top1_prob = ranked[0]
        exp_prob = p_dict.get(expected, 0)
        h = entropy(ranked)

        # Analyze edge difference between expected and top1
        ch_expected = disease_children.get(expected, set())
        ch_top1 = disease_children.get(top1_id, set())
        only_expected = ch_expected - ch_top1
        only_top1 = ch_top1 - ch_expected
        shared = ch_expected & ch_top1

        # For evidence variables: which ones does expected lack edges to?
        missing_edges_for_expected = []
        for var_id in ev:
            if var_id.startswith("R") or var_id.startswith("D"):
                continue
            params = noisy_or.get(var_id)
            if params is None:
                continue
            pe = params.get("parent_effects", {})
            has_expected = expected in pe
            has_top1 = top1_id in pe

            if not has_expected and has_top1:
                # top1 has edge, expected doesn't → top1 gets LR boost, expected doesn't
                missing_edges_for_expected.append(var_id)
            elif not has_expected and not has_top1:
                # Neither has edge → neutral, but could be an opportunity
                pass

        # Compute LR breakdown for the evidence
        lr_breakdown = []
        for var_id, obs_state in ev.items():
            params = noisy_or.get(var_id)
            if params is None:
                continue
            pe = params.get("parent_effects", {})
            leak = params["leak"]
            states = params["states"]

            from bn_inference import resolve_state
            resolved = resolve_state(obs_state, states)
            if resolved is None:
                continue

            p_leak = leak.get(resolved, 1.0 / len(states))
            if p_leak <= 0:
                p_leak = 1e-10

            # LR for expected
            if expected in pe:
                p_exp = pe[expected].get(resolved, 0.001)
            else:
                p_exp = p_leak
            lr_exp = p_exp / p_leak

            # LR for top1
            if top1_id in pe:
                p_t1 = pe[top1_id].get(resolved, 0.001)
            else:
                p_t1 = p_leak
            lr_top1 = p_t1 / p_leak

            if abs(math.log(max(lr_exp, 1e-10)) - math.log(max(lr_top1, 1e-10))) > 0.1:
                lr_breakdown.append({
                    "var": var_id,
                    "name_ja": var_lookup.get(var_id, {}).get("name_ja", var_id),
                    "state": resolved,
                    "lr_expected": lr_exp,
                    "lr_top1": lr_top1,
                    "has_edge_expected": expected in pe,
                    "has_edge_top1": top1_id in pe,
                })

        confusions.append({
            "case_id": case["id"],
            "expected": expected,
            "expected_name": var_lookup.get(expected, {}).get("name_ja", expected),
            "top1": top1_id,
            "top1_name": var_lookup.get(top1_id, {}).get("name_ja", top1_id),
            "rank": rank,
            "entropy": h,
            "top1_prob": top1_prob,
            "exp_prob": exp_prob,
            "missing_edges": missing_edges_for_expected,
            "lr_breakdown": sorted(lr_breakdown,
                                   key=lambda x: x["lr_top1"] / max(x["lr_expected"], 1e-10),
                                   reverse=True),
            "n_shared": len(shared),
            "n_only_expected": len(only_expected),
            "n_only_top1": len(only_top1),
            "biopsy_dependent": case.get("biopsy_dependent", False),
        })

    confusions.sort(key=lambda x: x["rank"])
    return confusions


# ═══════════════════════════════════════════════════════════════════════
# Showcase Scenarios
# ═══════════════════════════════════════════════════════════════════════

SCENARIOS = {
    "IE": {
        "title": "感染性心内膜炎(IE) の6ステップ診断",
        "steps": [
            ("T01", "1w_to_3w"),          # 亜急性（1〜3週）
            ("T03", "intermittent"),       # 間欠熱
            ("E15", "new"),               # 新規心雑音
            ("L09", "gram_positive"),     # 血液培養 グラム陽性
            ("S05", "mild"),              # 頭痛
            ("E14", "present"),           # 脾腫
        ],
    },
    "Still": {
        "title": "成人Still病 — フェリチン一発診断",
        "steps": [
            ("T03", "intermittent"),       # 間欠熱
            ("S08", "present"),           # 関節痛
            ("E12", "maculopapular_rash"),  # 皮膚所見：斑丘疹
            ("L02", "high_over_10"),      # CRP高値
            ("L01", "leukocytosis_over_12000"),  # 白血球増加
            ("L15", "elevated"),          # フェリチン上昇
        ],
    },
    "PE": {
        "title": "肺塞栓症(PE) — D-dimer→下肢腫脹で確定",
        "steps": [
            ("S04", "at_rest"),           # 安静時呼吸困難
            ("T01", "under_3d"),          # 急性（3日以内）
            ("L20", "elevated"),          # D-dimer上昇
            ("S39", "present"),           # 片側下肢腫脹
        ],
    },
    "malaria": {
        "title": "マラリア — 渡航歴＋周期熱＋塗抹標本",
        "steps": [
            ("R01", "yes"),               # 海外渡航歴
            ("T03", "periodic"),          # 周期熱
            ("T01", "under_3d"),          # 急性（3日以内）
            ("L10", "positive"),          # マラリア塗抹陽性
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Paper 4: 情報幾何分析")
    parser.add_argument("--trajectory", nargs="?", const="all",
                        help="診断軌跡を表示 (scenario名 or 'all')")
    parser.add_argument("--distance", action="store_true",
                        help="疾患間の診断距離行列")
    parser.add_argument("--next-test", nargs="*",
                        help="Next Best Test推奨 (E15=new S01=present ...)")
    parser.add_argument("--missing-edges", action="store_true",
                        help="辺欠損の自動検出")
    parser.add_argument("--all", action="store_true",
                        help="全分析を実行")
    args = parser.parse_args()

    if not any([args.trajectory, args.distance, args.next_test is not None,
                args.missing_edges, args.all]):
        args.all = True

    # ─── 1. Diagnostic Trajectories ──────────────────────────────
    if args.trajectory or args.all:
        scenarios_to_run = SCENARIOS
        if args.trajectory and args.trajectory != "all":
            key = args.trajectory
            if key in SCENARIOS:
                scenarios_to_run = {key: SCENARIOS[key]}
            else:
                print(f"Unknown scenario: {key}. Available: {', '.join(SCENARIOS.keys())}")
                return

        for key, scenario in scenarios_to_run.items():
            traj = diagnostic_trajectory(scenario["steps"])
            print_trajectory(traj, scenario["title"])

            # Summary
            total_fr = sum(pt["fr_distance"] for pt in traj)
            final_h = traj[-1]["entropy"]
            biggest_push = max(traj[1:], key=lambda pt: pt["fr_distance"])
            bp_var, bp_state = biggest_push["added"]
            bp_name = var_lookup.get(bp_var, {}).get("name_ja", bp_var)
            print(f"\n  総移動距離: {total_fr:.3f} | 最終H: {final_h:.2f} | "
                  f"最大の推し: {bp_name}={bp_state} (d_FR={biggest_push['fr_distance']:.3f})")

    # ─── 2. Disease Distance Matrix ──────────────────────────────
    if args.distance or args.all:
        print(f"\n{'='*90}")
        print(f"  疾患間の診断距離（CPTプロファイル類似度）")
        print(f"  距離が小さい = 鑑別が難しい")
        print(f"{'='*90}")

        # Compute all pairwise distances, show the closest pairs
        pairs = []
        for i, d1 in enumerate(disease_ids):
            for d2 in disease_ids[i+1:]:
                avg_dist, var_dists = compute_disease_distance_via_profile(d1, d2)
                if avg_dist is not None and len(var_dists) >= 3:
                    pairs.append((d1, d2, avg_dist, len(var_dists)))

        pairs.sort(key=lambda x: x[2])

        print(f"\n最も鑑別困難な疾患ペア (Top 20):")
        print(f"{'D1':6s} {'Name1':20s}  {'D2':6s} {'Name2':20s}  {'距離':>6s}  {'共有辺':>4s}")
        print("-" * 85)
        for d1, d2, dist, n_shared in pairs[:20]:
            n1 = var_lookup.get(d1, {}).get("name_ja", d1)[:20]
            n2 = var_lookup.get(d2, {}).get("name_ja", d2)[:20]
            print(f"{d1:6s} {n1:20s}  {d2:6s} {n2:20s}  {dist:6.3f}  {n_shared:4d}")

        print(f"\n最も鑑別容易な疾患ペア (Top 10):")
        print(f"{'D1':6s} {'Name1':20s}  {'D2':6s} {'Name2':20s}  {'距離':>6s}  {'共有辺':>4s}")
        print("-" * 85)
        for d1, d2, dist, n_shared in pairs[-10:]:
            n1 = var_lookup.get(d1, {}).get("name_ja", d1)[:20]
            n2 = var_lookup.get(d2, {}).get("name_ja", d2)[:20]
            print(f"{d1:6s} {n1:20s}  {d2:6s} {n2:20s}  {dist:6.3f}  {n_shared:4d}")

    # ─── 3. Next Best Test ────────────────────────────────────────
    if args.next_test is not None or args.all:
        if args.next_test:
            evidence = {}
            for item in args.next_test:
                var_id, state = item.split("=")
                evidence[var_id] = state
        else:
            # Default: show for the IE scenario at step 2 (after subacute + intermittent fever)
            evidence = {"T01": "1w_to_3w", "T03": "intermittent"}

        results, h_now = next_best_test(evidence)

        ev_str = ", ".join(
            f"{var_lookup.get(v,{}).get('name_ja',v)}={s}"
            for v, s in evidence.items()
        )
        print(f"\n{'='*90}")
        print(f"  Next Best Test 推奨")
        print(f"  現在のエビデンス: {ev_str}")
        print(f"  現在のエントロピー: H = {h_now:.2f}")
        print(f"{'='*90}")

        print(f"\n{'Rank':>4s}  {'変数':25s}  {'カテゴリ':8s}  {'期待IG':>7s}  {'期待d_FR':>8s}  状態別効果")
        print("-" * 110)
        for i, r in enumerate(results):
            detail_str = " | ".join(
                f"{s}→H={h:.1f}" for s, w, h, fr in r["state_details"]
                if w > 0.05  # Only show states with >5% probability
            )
            print(f"{i+1:4d}  {r['name_ja']:25s}  {r['category']:8s}  "
                  f"{r['expected_ig']:7.3f}  {r['expected_fr']:8.3f}  {detail_str}")

    # ─── 4. Missing Edge Detection ────────────────────────────────
    if args.missing_edges or args.all:
        print(f"\n{'='*90}")
        print(f"  辺欠損検出 (Real Case Evidence)")
        print(f"  実症例でrank>3の誤診を分析 → 正解疾患に足りない辺を特定")
        print(f"{'='*90}")

        confusions = detect_missing_edges()

        if not confusions:
            print("\n  rank>3の誤診なし。全症例Top-3以内。")
        else:
            print(f"\n  {len(confusions)} 件の誤診を検出:\n")
            for c in confusions:
                biopsy = " [活検依存]" if c["biopsy_dependent"] else ""
                fatal = " ⚠FATAL" if c["entropy"] < 2.0 else ""
                print(f"  {c['case_id']:5s} rank={c['rank']:2d} H={c['entropy']:.2f}{fatal}{biopsy}")
                print(f"    正解: {c['expected_name']}({c['expected']}) {c['exp_prob']*100:.1f}%")
                print(f"    出力: {c['top1_name']}({c['top1']}) {c['top1_prob']*100:.1f}%")
                print(f"    辺構造: 共有{c['n_shared']} | 正解のみ{c['n_only_expected']} | Top1のみ{c['n_only_top1']}")

                if c["missing_edges"]:
                    me_names = [var_lookup.get(v, {}).get("name_ja", v) for v in c["missing_edges"]]
                    print(f"    ★正解に辺なし(Top1にはあり): {', '.join(me_names)}")

                # Show top LR imbalances
                lr = c["lr_breakdown"][:5]
                if lr:
                    print(f"    LR不均衡 (Top1有利な変数):")
                    for item in lr:
                        edge_exp = "○" if item["has_edge_expected"] else "×"
                        edge_t1 = "○" if item["has_edge_top1"] else "×"
                        print(f"      {item['name_ja']}={item['state']}: "
                              f"LR正解={item['lr_expected']:.2f}(辺{edge_exp}) "
                              f"LR_Top1={item['lr_top1']:.2f}(辺{edge_t1})")
                print()


if __name__ == "__main__":
    main()
