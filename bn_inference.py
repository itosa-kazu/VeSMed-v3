#!/usr/bin/env python3
"""
VeSMed V3 — Noisy-OR Bayesian Network Inference Engine
発熱鑑別診断102疾患の因果ベイズネットワーク推論

Usage:
    python bn_inference.py                      # 全案例テスト
    python bn_inference.py --case R01           # 単一案例テスト
    python bn_inference.py --case R01 R04 R28   # 複数案例テスト
"""

import json
import math
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
STEP1 = os.path.join(BASE, "step1_fever_v2.7.json")
STEP2 = os.path.join(BASE, "step2_fever_edges_v4.json")
STEP3 = os.path.join(BASE, "step3_fever_cpts_v2.json")
CASES = os.path.join(BASE, "real_case_test_suite.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_state_map(step1_states, cpt_keys):
    """
    Build a mapping from step1 state names to CPT keys.
    Handles mismatches like 'sudden_hours' <-> 'sudden',
    'on_exertion' <-> 'exertional', etc.
    """
    mapping = {}

    # First: exact matches
    for s in step1_states:
        if s in cpt_keys:
            mapping[s] = s

    # Second: substring/prefix matching for unmatched
    unmatched_s1 = [s for s in step1_states if s not in mapping]
    unmatched_cpt = [k for k in cpt_keys if k not in mapping.values()]

    for s in unmatched_s1:
        best = None
        best_score = 0
        s_lower = s.lower().replace("_", "")
        for k in unmatched_cpt:
            k_lower = k.lower().replace("_", "")
            # Check if one contains the other
            if k_lower in s_lower or s_lower in k_lower:
                score = min(len(k_lower), len(s_lower))
                if score > best_score:
                    best = k
                    best_score = score
            # Check prefix match
            elif s_lower[:4] == k_lower[:4] and len(s_lower) >= 4:
                score = 4
                if score > best_score:
                    best = k
                    best_score = score
        if best:
            mapping[s] = best
            unmatched_cpt = [k for k in unmatched_cpt if k != best]

    return mapping


def expand_prob(val, states):
    """
    Expand a parent_effect or leak value into a full state->prob dict.
    - dict: return as-is
    - float: first state gets (1-val), rest share val equally
    - str: return None (formula/note)
    """
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        return None
    if isinstance(val, (int, float)):
        val = float(val)
        if not states:
            return None
        result = {}
        result[states[0]] = 1.0 - val
        rest = states[1:]
        if rest:
            each = val / len(rest)
            for s in rest:
                result[s] = each
        return result
    return None


def build_model(step1, step2, step3):
    """Build model from 3-file network definition."""
    # Variables
    variables = {}
    diseases = []
    for v in step1["variables"]:
        vid = v["id"]
        variables[vid] = {
            "name": v.get("name", ""),
            "name_ja": v.get("name_ja", ""),
            "states": v.get("states", []),
            "category": v.get("category", ""),
        }
        if v.get("category") == "disease":
            diseases.append(vid)

    # Edges
    disease_children = defaultdict(set)
    for e in step2["edges"]:
        frm = e["from"]
        if frm.startswith("D") or frm == "M01":
            disease_children[frm].add(e["to"])

    # Noisy-OR parameters — pre-expand and normalize state names
    raw_noisy = step3.get("noisy_or_params", {})
    noisy_or = {}

    for var_id, section in raw_noisy.items():
        if not isinstance(section, dict):
            continue
        cpt_states = section.get("states", [])

        # Infer states from leak keys if states list is missing
        if not cpt_states:
            leak_raw = section.get("leak")
            if isinstance(leak_raw, dict):
                cpt_states = list(leak_raw.keys())
            else:
                continue

        # Get step1 states (canonical)
        s1_states = variables.get(var_id, {}).get("states", cpt_states)

        # Expand leak
        leak_raw = section.get("leak")
        leak_expanded = expand_prob(leak_raw, cpt_states)
        if leak_expanded is None:
            continue

        # Build state mapping: step1_state -> cpt_key
        cpt_keys = set(leak_expanded.keys())
        # Also collect all keys from parent_effects
        for pe_val in section.get("parent_effects", {}).values():
            if isinstance(pe_val, dict):
                cpt_keys.update(pe_val.keys())

        state_map = build_state_map(s1_states, cpt_keys)

        # Also build reverse map: cpt_key -> step1_state
        reverse_map = {v: k for k, v in state_map.items()}

        # Normalize leak to use step1 state names
        norm_leak = {}
        for s1_state in s1_states:
            cpt_key = state_map.get(s1_state, s1_state)
            norm_leak[s1_state] = leak_expanded.get(cpt_key,
                                  leak_expanded.get(s1_state, 1.0 / len(s1_states)))

        # Normalize parent_effects
        norm_pe = {}
        for d, pe_raw in section.get("parent_effects", {}).items():
            pe = expand_prob(pe_raw, cpt_states)
            if pe is None:
                continue
            norm_d = {}
            for s1_state in s1_states:
                cpt_key = state_map.get(s1_state, s1_state)
                norm_d[s1_state] = pe.get(cpt_key, pe.get(s1_state, 0.001))
            norm_pe[d] = norm_d

        noisy_or[var_id] = {
            "states": s1_states,
            "leak": norm_leak,
            "parent_effects": norm_pe,
        }

    root_priors = step3.get("root_priors", {})
    return variables, diseases, dict(disease_children), noisy_or, root_priors


def get_prior(disease_id, root_priors, risk_evidence):
    """Get disease prior, modulated by risk factor evidence."""
    rp = root_priors.get(disease_id)
    if rp is None:
        return 0.01
    if isinstance(rp, (int, float)):
        return float(rp)
    if isinstance(rp, dict):
        parents = rp.get("parents", [])
        cpt = rp.get("cpt", {})
        if not cpt:
            return 0.01
        for pid in parents:
            if pid in risk_evidence:
                state = risk_evidence[pid]
                if state in cpt:
                    return float(cpt[state])
        for key in ("no", "none", "absent"):
            if key in cpt:
                return float(cpt[key])
        vals = [float(v) for v in cpt.values() if isinstance(v, (int, float))]
        return min(vals) if vals else 0.01
    return 0.01


def resolve_state(obs_state, states):
    """
    Resolve an observed state to a matching state in the CPT.
    Handles mismatches like 'moderate' -> 'mild', 'on_exertion' -> 'exertional'.
    """
    if obs_state in states:
        return obs_state

    # Known mappings
    MANUAL_MAP = {
        "moderate": "mild",
        "on_exertion": "exertional",
        "hypotension_under_90": "hypotension",
        "normal_over_90": "normal",
        "mild_elevated": "elevated",
        "very_high": "elevated",
    }
    if obs_state in MANUAL_MAP and MANUAL_MAP[obs_state] in states:
        return MANUAL_MAP[obs_state]

    # Substring match
    obs_lower = obs_state.lower().replace("_", "")
    for s in states:
        s_lower = s.lower().replace("_", "")
        if obs_lower in s_lower or s_lower in obs_lower:
            return s
    return None


def infer(evidence, risk, diseases, disease_children, noisy_or, root_priors):
    """
    Compute P(disease | evidence) for all diseases.

    For each disease d:
      log P(d|E) ∝ log prior(d) + Σ_v [log P(v=obs|d) - log P(v=obs|leak)]
    """
    log_posteriors = {}

    for d in diseases:
        if d == "M01":
            continue

        prior = get_prior(d, root_priors, risk)
        if prior <= 0:
            prior = 1e-10
        log_post = math.log(prior)

        for var_id, obs_state in evidence.items():
            params = noisy_or.get(var_id)
            if params is None:
                continue

            states = params["states"]
            leak = params["leak"]
            pe = params["parent_effects"]

            # Resolve evidence state to CPT state
            resolved = resolve_state(obs_state, states)
            if resolved is None:
                continue

            p_leak = leak.get(resolved, 1.0 / len(states))
            if p_leak <= 0:
                p_leak = 1e-10

            if d in pe:
                p_d = pe[d].get(resolved, 0.001)
            else:
                p_d = p_leak  # no edge → LR=1

            if p_d <= 0:
                p_d = 1e-10

            log_post += math.log(p_d) - math.log(p_leak)

        log_posteriors[d] = log_post

    if not log_posteriors:
        return []

    max_lp = max(log_posteriors.values())
    posteriors = {}
    total = 0.0
    for d, lp in log_posteriors.items():
        p = math.exp(lp - max_lp)
        posteriors[d] = p
        total += p
    if total > 0:
        for d in posteriors:
            posteriors[d] /= total

    return sorted(posteriors.items(), key=lambda x: -x[1])


def entropy(ranked):
    h = 0.0
    for _, p in ranked:
        if p > 1e-15:
            h -= p * math.log2(p)
    return h


def main():
    import argparse
    parser = argparse.ArgumentParser(description="VeSMed BN Inference")
    parser.add_argument("--case", nargs="*", help="Case IDs to test")
    args = parser.parse_args()

    step1 = load_json(STEP1)
    step2 = load_json(STEP2)
    step3 = load_json(STEP3)
    case_data = load_json(CASES)

    variables, diseases, disease_children, noisy_or, root_priors = \
        build_model(step1, step2, step3)

    var_lookup = {v["id"]: v for v in step1["variables"]}

    cases = case_data["cases"]
    if args.case:
        cases = [c for c in cases if c["id"] in args.case]

    print("=" * 120)
    print(f"VeSMed V3 BN Inference | {len(diseases)} diseases, {len(step2['edges'])} edges, {len(cases)} cases")
    print("=" * 120)

    # Run all cases and collect results
    all_results = []
    for case in cases:
        cid = case["id"]
        expected = case["expected_id"]
        is_in = case["in_scope"]
        ev = case.get("evidence", {})
        risk = case.get("risk_factors", {})

        ranked = infer(ev, risk, diseases, disease_children, noisy_or, root_priors)
        h = entropy(ranked)

        rank = None
        if expected != "OOS":
            for i, (d, p) in enumerate(ranked):
                if d == expected:
                    rank = i + 1
                    break

        result = {
            "id": cid, "expected": expected, "in_scope": is_in,
            "rank": rank, "entropy": h,
            "top1_d": ranked[0][0] if ranked else "?",
            "top1_p": ranked[0][1] if ranked else 0,
            "ranked": ranked,
        }
        all_results.append(result)

        # Classify
        if not is_in:
            icon = "  OOS"
        elif rank == 1:
            icon = " TOP1"
        elif rank is not None and rank <= 3:
            icon = " TOP3"
        elif h < 2.0 and rank is not None and rank > 3:
            icon = "FATAL"
        elif h < 2.0 and is_in and expected != "OOS" and rank is None:
            icon = "FATAL"
        else:
            icon = " MISS"

        top3_disp = []
        for d, p in ranked[:3]:
            nm = var_lookup.get(d, {}).get("name_ja", d)
            if len(nm) > 14:
                nm = nm[:14]
            top3_disp.append(f"{nm}({d}){p*100:.1f}%")

        exp_name = var_lookup.get(expected, {}).get("name_ja", expected) if expected != "OOS" else "OOS"
        rk = f"r{rank}" if rank else "---"
        print(f"[{icon}] {cid:4s} H={h:5.2f} {rk:>5s}  正解={exp_name}  | {' | '.join(top3_disp)}")

    # ─── Summary ────────────────────────────────────────────────────
    in_results = [r for r in all_results if r["in_scope"] and r["expected"] != "OOS"]
    oos_results = [r for r in all_results if not r["in_scope"] or r["expected"] == "OOS"]

    t1 = sum(1 for r in in_results if r["rank"] == 1)
    t3 = sum(1 for r in in_results if r["rank"] is not None and r["rank"] <= 3)
    conf = sum(1 for r in in_results if r["entropy"] < 2.0 and (r["rank"] is None or r["rank"] > 3))
    n = len(in_results)

    print("\n" + "=" * 120)
    print(f"SUMMARY: {n} in-scope | Top-1: {t1}/{n} ({t1/n*100:.0f}%) | "
          f"Top-3: {t3}/{n} ({t3/n*100:.0f}%) | "
          f"Confident misdiag: {conf} | OOS: {len(oos_results)}")
    print("=" * 120)

    # Per-disease
    disease_stats = defaultdict(lambda: {"n": 0, "t1": 0, "t3": 0})
    for r in in_results:
        ds = disease_stats[r["expected"]]
        ds["n"] += 1
        if r["rank"] == 1:
            ds["t1"] += 1
        if r["rank"] is not None and r["rank"] <= 3:
            ds["t3"] += 1

    print(f"\n{'Disease':8s} {'Name':25s} {'N':>3s} {'T1':>4s} {'T3':>4s}")
    print("-" * 55)
    for d in sorted(disease_stats.keys()):
        ds = disease_stats[d]
        nm = var_lookup.get(d, {}).get("name_ja", d)[:25]
        print(f"{d:8s} {nm:25s} {ds['n']:3d} {ds['t1']:4d} {ds['t3']:4d}")

    # Confident misdiagnosis detail
    conf_list = [r for r in in_results if r["entropy"] < 2.0 and (r["rank"] is None or r["rank"] > 3)]
    if conf_list:
        print(f"\n自信的誤診 (H<2 + rank>3): {len(conf_list)}件")
        for r in conf_list:
            t1n = var_lookup.get(r["top1_d"], {}).get("name_ja", r["top1_d"])
            en = var_lookup.get(r["expected"], {}).get("name_ja", r["expected"])
            print(f"  {r['id']}: H={r['entropy']:.2f} r{r['rank']} "
                  f"出力={t1n}({r['top1_d']}) {r['top1_p']*100:.1f}% ← 正解={en}({r['expected']})")

    # Miss detail (rank > 5)
    miss_list = [r for r in in_results if r["rank"] is not None and r["rank"] > 5]
    if miss_list:
        print(f"\nMiss (rank>5): {len(miss_list)}件")
        for r in miss_list:
            t1n = var_lookup.get(r["top1_d"], {}).get("name_ja", r["top1_d"])
            en = var_lookup.get(r["expected"], {}).get("name_ja", r["expected"])
            print(f"  {r['id']}: H={r['entropy']:.2f} r{r['rank']} "
                  f"出力={t1n}({r['top1_d']}) {r['top1_p']*100:.1f}% ← 正解={en}({r['expected']})")


if __name__ == "__main__":
    main()
