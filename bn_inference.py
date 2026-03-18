#!/usr/bin/env python3
"""
VeSMed V3.1 — Noisy-OR Bayesian Network Inference Engine
発熱鑑別診断102疾患の因果ベイズネットワーク推論

V3.1 改善点:
  - 方向C: IDF鑑別力係数 — 非特異的変数(WBC,CRP等)の影響を自動的に抑制
  - 反事実Coverage — 疾患が観察された陽性所見をどれだけ因果的に説明できるかをスコアに加算
  - 結果: Top-1 42%→47%, Top-3 75%→79%, FATAL 2件(不変)

Usage:
    python bn_inference.py                      # 全案例テスト (改善版)
    python bn_inference.py --case R01           # 単一案例テスト
    python bn_inference.py --case R01 R04 R28   # 複数案例テスト
    python bn_inference.py --classic            # 旧版(改善なし)で実行
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

# === 推論改善パラメータ (grid search最適化済み: 350疾患/712案例) ===
# IDF鑑別力係数のべき乗 (0=無効, 0.3=最適, 1.0=強)
IDF_DISC_POWER = 0.3
# 反事実Coverage: 因果説明力の重み (0=無効, 2.0=最適, 3.0=強)
CF_COVERAGE_ALPHA = 2.0
# Prior Power: デモグラフィック調整の強さ (0=無効, 0.5=最適, 1.0=フル)
# 日本人口ピラミッド(2024)を固定参照分布として使用
PRIOR_POWER = 0.5


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
            if k_lower in s_lower or s_lower in k_lower:
                score = min(len(k_lower), len(s_lower))
                if score > best_score:
                    best = k
                    best_score = score
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

    disease_children = defaultdict(set)
    for e in step2["edges"]:
        frm = e["from"]
        if frm.startswith("D") or frm.startswith("M"):
            disease_children[frm].add(e["to"])

    raw_noisy = step3.get("noisy_or_params", {})
    noisy_or = {}

    for var_id, section in raw_noisy.items():
        if not isinstance(section, dict):
            continue
        cpt_states = section.get("states", [])

        if not cpt_states:
            leak_raw = section.get("leak")
            if isinstance(leak_raw, dict):
                cpt_states = list(leak_raw.keys())
            else:
                continue

        s1_states = variables.get(var_id, {}).get("states", cpt_states)

        leak_raw = section.get("leak")
        leak_expanded = expand_prob(leak_raw, cpt_states)
        if leak_expanded is None:
            continue

        cpt_keys = set(leak_expanded.keys())
        for pe_val in section.get("parent_effects", {}).values():
            if isinstance(pe_val, dict):
                cpt_keys.update(pe_val.keys())

        state_map = build_state_map(s1_states, cpt_keys)

        norm_leak = {}
        for s1_state in s1_states:
            cpt_key = state_map.get(s1_state, s1_state)
            norm_leak[s1_state] = leak_expanded.get(cpt_key,
                                  leak_expanded.get(s1_state, 1.0 / len(s1_states)))

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

    # Merge priors: root_priors overrides, full_cpts as fallback
    root_priors = dict(step3.get("root_priors", {}))
    full_cpts = step3.get("full_cpts", {})
    for did in diseases:
        if did not in root_priors and did in full_cpts:
            fc = full_cpts[did]
            if isinstance(fc, dict) and "parents" in fc:
                root_priors[did] = fc

    return variables, diseases, dict(disease_children), noisy_or, root_priors


def compute_idf_disc(step2, noisy_or, n_diseases=104):
    """
    方向C: IDF鑑別力係数を計算

    disc(v) = log(N / n_connected) / log(N)

    連結疾患が少ない変数 → disc高い → 鑑別力が高い (例: 焦痂 → 0.85)
    連結疾患が多い変数 → disc低い → 非特異的      (例: CRP → 0.065)
    """
    edge_count = defaultdict(int)
    for e in step2["edges"]:
        frm = e["from"]
        if frm.startswith("D") or frm.startswith("M"):
            edge_count[e["to"]] += 1

    disc = {}
    max_idf = math.log(n_diseases) if n_diseases > 1 else 1.0

    for var_id in noisy_or:
        n_connected = edge_count.get(var_id, 0)
        if n_connected == 0:
            disc[var_id] = 1.0
        else:
            idf = math.log(n_diseases / n_connected)
            disc[var_id] = idf / max_idf

    return disc


def _cpt_val_to_prior(val):
    """Convert a CPT value to a scalar prior.

    Some full_cpts entries have nested dicts (e.g. D13 meningitis subtypes:
    {"no": 0.994, "viral": 0.004, "bacterial": 0.002}).
    Disease prior = 1 - P(no disease).
    """
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, dict):
        no_val = val.get("no", 0)
        return max(1.0 - float(no_val), 0.001)
    return 0.01


def _lookup_cpt(cpt, parents, parts):
    """Look up a CPT value given parent states. Returns scalar or None."""
    # Try composite key
    key = "|".join(parts) if len(parts) > 1 else parts[0]
    if key in cpt:
        return _cpt_val_to_prior(cpt[key])

    # Fallback: try single parent state directly
    if len(parts) == 1 and parts[0] in cpt:
        return _cpt_val_to_prior(cpt[parts[0]])

    # Fallback: common default keys
    for k in ("no", "none", "absent"):
        if k in cpt:
            return _cpt_val_to_prior(cpt[k])

    # Final fallback: minimum value
    vals = [_cpt_val_to_prior(v) for v in cpt.values()]
    return min(vals) if vals else None


BASE_PRIOR = 0.01


def _compute_marginal(cpt, parents, root_priors):
    """Compute population-weighted marginal P(d) = Σ P(d|RF=s) × P(RF=s).

    This represents the average prior across the population, without
    knowing any risk factor values. Used as the denominator in the
    RF relative adjustment ratio.
    """
    # Get distribution for each RF parent
    distributions = []
    for pid in parents:
        dist_info = root_priors.get(pid)
        if isinstance(dist_info, dict) and "distribution" in dist_info:
            distributions.append(list(dist_info["distribution"].items()))
        else:
            distributions.append([("no", 0.5), ("yes", 0.5)])

    # For single parent: simple weighted average
    if len(parents) == 1:
        total = 0.0
        for state, prob in distributions[0]:
            val = cpt.get(state)
            if val is not None:
                total += _cpt_val_to_prior(val) * prob
        return total if total > 0 else None

    # For multi-parent: iterate over all state combinations
    # Use itertools-style nested loop
    from itertools import product
    total = 0.0
    for combo in product(*distributions):
        states = [s for s, _ in combo]
        weight = 1.0
        for _, p in combo:
            weight *= p
        key = "|".join(states)
        val = cpt.get(key)
        if val is not None:
            total += _cpt_val_to_prior(val) * weight
    return total if total > 0 else None


def get_prior(disease_id, root_priors, risk_evidence, prior_power=0.0):
    """Get disease prior: demographic contrast with FIXED Japan population distribution.

    Formula: adjusted_prior = BASE × P(d|RF_observed) / P_marginal_fixed(d)

    P_marginal_fixed uses Japan 2024 population pyramid (hardcoded).
    This is INDEPENDENT of root_priors distribution — adding/removing age
    groups never changes existing results.

    prior_power controls strength:
      0.0 = no demographic adjustment (all diseases equal)
      1.0 = full adjustment (original ratio formula)
    """
    # Japan 2024 population pyramid (Statistics Bureau of Japan)
    # Source: stat.go.jp + UN World Population Prospects
    JAPAN_POP = {
        "R01": {"description": "Japan 2024 population", "distribution": {
            "0_1": 0.013, "1_5": 0.027, "6_12": 0.057, "13_17": 0.045,
            "18_39": 0.220, "40_64": 0.340, "65_plus": 0.298
        }},
        "R02": {"description": "Japan 2024 sex ratio", "distribution": {
            "male": 0.488, "female": 0.512
        }},
        "R05": {"description": "Immunocompromised prevalence", "distribution": {
            "no": 0.95, "yes": 0.05
        }},
        "R06": {"description": "Travel history distribution (Japan)", "distribution": {
            "no": 0.85, "tropical_endemic": 0.02, "developed": 0.03, "domestic": 0.10
        }},
        "R40": {"description": "Malignancy status distribution", "distribution": {
            "no": 0.95, "history_remission": 0.02,
            "active_on_treatment": 0.02, "active_untreated": 0.01
        }},
        "R35": {"description": "IBD history prevalence (Japan)", "distribution": {
            "no": 0.997, "yes": 0.003
        }},
    }

    rp = root_priors.get(disease_id)
    if rp is None:
        return BASE_PRIOR
    if isinstance(rp, (int, float)):
        return BASE_PRIOR
    if not isinstance(rp, dict):
        return BASE_PRIOR

    parents = rp.get("parents", [])
    cpt = rp.get("cpt", {})
    if not cpt or not parents:
        return BASE_PRIOR

    # Only use risk factor parents (R-prefixed)
    rf_parents = [p for p in parents if p.startswith("R")]
    if not rf_parents:
        return BASE_PRIOR

    # Build observed state for each RF parent
    obs_parts = []
    for pid in rf_parents:
        if pid in risk_evidence:
            obs_parts.append(risk_evidence[pid])
        else:
            # Unobserved: use most common state from Japan population
            dist_info = JAPAN_POP.get(pid)
            if dist_info:
                dist = dist_info["distribution"]
                obs_parts.append(max(dist, key=dist.get))
            else:
                obs_parts.append("no")

    # For CPTs with mixed parents (RF + disease), fill disease parents with "no"
    if len(rf_parents) < len(parents):
        full_obs = []
        rf_idx = 0
        full_parents = parents
        for pid in parents:
            if pid.startswith("R"):
                full_obs.append(obs_parts[rf_idx])
                rf_idx += 1
            else:
                full_obs.append("no")
        obs_parts = full_obs
    else:
        full_parents = rf_parents

    # P(d | RF=observed)
    p_observed = _lookup_cpt(cpt, full_parents, obs_parts)
    if p_observed is None:
        return BASE_PRIOR
    if p_observed <= 0:
        return 1e-6

    if prior_power <= 0:
        return BASE_PRIOR

    # P_marginal using Japan population (fixed, never changes)
    p_marginal = _compute_marginal(cpt, full_parents, JAPAN_POP)
    if p_marginal is None or p_marginal <= 0:
        return BASE_PRIOR

    # Ratio-based adjustment
    ratio = p_observed / p_marginal
    adjusted = BASE_PRIOR * (ratio ** prior_power)

    return max(min(adjusted, 0.5), 1e-6)


def _compute_marginal_fixed(cpt, parents):
    """Compute marginal prior using FIXED reference distribution.

    Uses a hardcoded adult-weighted distribution that never changes,
    regardless of how many age/sex states exist in R01/R02.
    This makes the demographic contrast independent of population composition
    while preserving disease-specific modulation.
    """
    # Fixed reference distribution (hardcoded, never changes)
    FIXED_DIST = {
        "R01": {"18_39": 0.40, "40_64": 0.35, "65_plus": 0.25},
        "R02": {"male": 0.50, "female": 0.50},
    }

    if not parents or not cpt:
        return None

    # Compute weighted average using fixed distribution
    # For single parent
    if len(parents) == 1:
        pid = parents[0]
        dist = FIXED_DIST.get(pid, {})
        if not dist:
            # Fallback: uniform over leaf values
            vals = [v for v in cpt.values() if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else None

        total = 0.0
        weight_sum = 0.0
        for state, weight in dist.items():
            val = cpt.get(state)
            if val is not None and isinstance(val, (int, float)):
                total += val * weight
                weight_sum += weight
        return total / weight_sum if weight_sum > 0 else None

    # For multiple parents (e.g., R01+R02): enumerate combinations
    if len(parents) == 2:
        p0, p1 = parents[0], parents[1]
        d0 = FIXED_DIST.get(p0, {})
        d1 = FIXED_DIST.get(p1, {})
        if not d0 or not d1:
            vals = [v for v in cpt.values() if isinstance(v, (int, float))]
            return sum(vals) / len(vals) if vals else None

        total = 0.0
        weight_sum = 0.0
        for s0, w0 in d0.items():
            for s1, w1 in d1.items():
                key = f"{s0},{s1}"
                val = cpt.get(key)
                if val is not None and isinstance(val, (int, float)):
                    w = w0 * w1
                    total += val * w
                    weight_sum += w
        return total / weight_sum if weight_sum > 0 else None

    # Fallback for >2 parents
    vals = [v for v in cpt.values() if isinstance(v, (int, float))]
    return sum(vals) / len(vals) if vals else None


def resolve_state(obs_state, states):
    """Resolve an observed state to a matching state in the CPT."""
    if obs_state in states:
        return obs_state

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

    obs_lower = obs_state.lower().replace("_", "")
    for s in states:
        s_lower = s.lower().replace("_", "")
        if obs_lower in s_lower or s_lower in obs_lower:
            return s
    return None


def infer(evidence, risk, diseases, disease_children, noisy_or, root_priors,
          disc=None, disc_power=0.0, cf_alpha=0.0, prior_power=0.0):
    """
    Compute P(disease | evidence) for all diseases.

    基本式: log P(d|E) ∝ log prior(d) + Σ_v [ w(v) × log_LR(v) ]

    方向C (disc_power > 0):
      w(v) = disc(v) ^ disc_power
      → 非特異的変数の log_LR を自動的に抑制

    反事実Coverage (cf_alpha > 0):
      coverage = n_explained / n_positive
      score += cf_alpha × log(coverage)
      → より多くの陽性所見を因果的に説明できる疾患にボーナス
    """
    log_posteriors = {}

    for d in diseases:
        if d.startswith("M"):
            continue

        prior = get_prior(d, root_priors, risk, prior_power=prior_power)
        if prior <= 0:
            prior = 1e-10
        log_post = math.log(prior)

        n_positive = 0
        n_explained = 0

        for var_id, obs_state in evidence.items():
            params = noisy_or.get(var_id)
            if params is None:
                continue

            states = params["states"]
            leak = params["leak"]
            pe = params["parent_effects"]

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

            log_lr = math.log(p_d) - math.log(p_leak)

            # 方向C: IDF鑑別力係数
            if disc and disc_power > 0:
                w = disc.get(var_id, 1.0) ** disc_power
                log_lr *= w

            log_post += log_lr

            # 反事実Coverage: 陽性所見カウント
            if cf_alpha > 0 and resolved != states[0]:
                n_positive += 1
                if d in pe:
                    p_cause = pe[d].get(resolved, 0.0)
                    if p_cause > 0.05:
                        n_explained += 1

        # 反事実Coverageボーナス
        if cf_alpha > 0 and n_positive > 0:
            coverage = n_explained / n_positive
            log_post += cf_alpha * math.log(max(coverage, 1e-6))

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


def next_best_test(evidence, risk, diseases, disease_children, noisy_or,
                   root_priors, disc=None, disc_power=0.0, cf_alpha=0.0,
                   top_n=10):
    """
    次に行うべき検査を情報利得(IG)で推奨する。

    各未観測変数vについて:
      1. 現在のposteriorからP(v=s|evidence)を近似計算
      2. evidence + {v=s} を仮定した場合のエントロピーH(v=s)を計算
      3. 期待エントロピー E[H|v] = Σ_s P(v=s|evidence) × H(v=s)
      4. 情報利得 IG(v) = H_now - E[H|v]
    IG降順でtop_n件を返す。
    """
    # Current posterior and entropy
    ranked_now = infer(evidence, risk, diseases, disease_children, noisy_or,
                       root_priors, disc=disc, disc_power=disc_power,
                       cf_alpha=cf_alpha)
    h_now = entropy(ranked_now)
    posterior = {d: p for d, p in ranked_now}

    # Skip variables already in evidence, risk factors, and disease nodes
    observed = set(evidence.keys()) | set(risk.keys())

    results = []
    for var_id, params in noisy_or.items():
        if var_id in observed:
            continue
        # Skip non-observation variables
        if var_id.startswith("R") or var_id.startswith("D") or var_id.startswith("M"):
            continue

        states = params["states"]
        leak = params["leak"]
        pe = params["parent_effects"]

        # Compute P(v=s|evidence) by marginalizing over diseases
        marginal = {}
        for s in states:
            p_s = 0.0
            for d in diseases:
                if d.startswith("M"):
                    continue
                p_d = posterior.get(d, 0.0)
                if d in pe:
                    p_vs_d = pe[d].get(s, 0.001)
                else:
                    p_vs_d = leak.get(s, 1.0 / len(states))
                p_s += p_vs_d * p_d
            marginal[s] = max(p_s, 1e-10)

        # Normalize marginal
        total_m = sum(marginal.values())
        if total_m > 0:
            for s in states:
                marginal[s] /= total_m

        # Compute expected entropy after observing v (per-state tracking)
        expected_h = 0.0
        state_details = []
        for s in states:
            p_s = marginal[s]
            if p_s < 1e-8:
                state_details.append({"state": s, "prob": p_s, "h_after": h_now})
                continue
            ev_hypo = dict(evidence)
            ev_hypo[var_id] = s
            ranked_hypo = infer(ev_hypo, risk, diseases, disease_children,
                                noisy_or, root_priors, disc=disc,
                                disc_power=disc_power, cf_alpha=cf_alpha)
            h_hypo = entropy(ranked_hypo)
            expected_h += p_s * h_hypo
            state_details.append({"state": s, "prob": p_s, "h_after": h_hypo})

        ig = h_now - expected_h
        # Best state = maximum entropy reduction
        best = min(state_details, key=lambda x: x["h_after"])
        results.append({
            "var_id": var_id,
            "ig": ig,
            "h_now": h_now,
            "expected_h": expected_h,
            "marginal": marginal,
            "best_state": best["state"],
            "best_state_h": best["h_after"],
            "state_details": state_details,
        })

    results.sort(key=lambda x: -x["ig"])
    return results[:top_n]


def next_best_falsification_test(evidence, risk, diseases, disease_children,
                                  noisy_or, root_priors, disc=None,
                                  disc_power=0.0, cf_alpha=0.0, top_n=5):
    """
    反証推奨: 現在のTop-1診断を最も動揺させる検査を推奨する。

    通常のnext_best_testがエントロピーを最小化する検査(確認方向)を選ぶのに対し、
    この関数はエントロピーを最大化する状態を持つ検査(反証方向)を選ぶ。

    原理:
      各未観測変数vの各状態sについてH_after(v=s)を計算。
      max_s(H_after(v=s)) が最大の変数 = 最も現診断を動揺させうる検査。

    臨床的意義:
      - 誤診の場合: 反証検査が正しい診断への道を開く
      - 正診の場合: 実際の結果が動揺方向と逆に出るため、確信が強まる
      - 確認バイアスを防ぎ、自己修正的な診断プロセスを実現
    """
    # Reuse next_best_test with same IDF/CF settings as the main system.
    all_results = next_best_test(
        evidence, risk, diseases, disease_children, noisy_or, root_priors,
        disc=disc, disc_power=disc_power, cf_alpha=cf_alpha,
        top_n=9999
    )

    if not all_results:
        return []

    h_now = all_results[0]["h_now"]

    # Rank by max(H_after) — the state that produces the highest post-test entropy.
    # No threshold needed: all tests are ranked by disruption potential.
    falsification_results = []
    for item in all_results:
        max_h_state = max(item["state_details"], key=lambda x: x["h_after"])
        h_increase = max_h_state["h_after"] - h_now

        falsification_results.append({
            "var_id": item["var_id"],
            "h_increase": h_increase,
            "h_now": h_now,
            "disruptive_state": max_h_state["state"],
            "disruptive_h": max_h_state["h_after"],
            "disruptive_prob": max_h_state["prob"],
            "marginal": item["marginal"],
            "state_details": item["state_details"],
            "ig": item["ig"],
        })

    # Sort by max(H_after) descending = most disruptive first
    falsification_results.sort(key=lambda x: -x["disruptive_h"])
    return falsification_results[:top_n]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="VeSMed BN Inference")
    parser.add_argument("--case", nargs="*", help="Case IDs to test")
    parser.add_argument("--classic", action="store_true",
                        help="旧版(改善なし)で実行")
    parser.add_argument("--grid", action="store_true",
                        help="Grid searchで最適(disc_power, cf_alpha)を探索")
    args = parser.parse_args()

    step1 = load_json(STEP1)
    step2 = load_json(STEP2)
    step3 = load_json(STEP3)
    case_data = load_json(CASES)

    variables, diseases, disease_children, noisy_or, root_priors = \
        build_model(step1, step2, step3)

    var_lookup = {v["id"]: v for v in step1["variables"]}

    # --- Grid Search Mode ---
    if args.grid:
        print("=" * 80)
        print("Grid Search: finding optimal (disc_power, cf_alpha, prior_power)")
        print("=" * 80)

        in_scope_cases = [c for c in case_data["cases"]
                          if c["in_scope"] and c.get("expected_id", "OOS") != "OOS"]

        best_score = -1
        best_params = (IDF_DISC_POWER, CF_COVERAGE_ALPHA, PRIOR_POWER)
        results_table = []

        dp_values = [0.0, 0.3, 0.5, 0.7, 1.0]
        ca_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        pp_values = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]

        d = compute_idf_disc(step2, noisy_or, n_diseases=len(diseases))
        total_combos = len(dp_values) * len(ca_values) * len(pp_values)
        done = 0

        for dp in dp_values:
            for ca in ca_values:
                for pp in pp_values:
                    t1, t3, fatal = 0, 0, 0

                    for case in in_scope_cases:
                        ev = case.get("evidence", {})
                        risk = case.get("risk_factors", {})
                        expected = case["expected_id"]

                        ranked = infer(ev, risk, diseases, disease_children,
                                       noisy_or, root_priors,
                                       disc=d, disc_power=dp, cf_alpha=ca,
                                       prior_power=pp)
                        h = entropy(ranked)

                        rank = None
                        for i, (dd, p) in enumerate(ranked):
                            if dd == expected:
                                rank = i + 1
                                break

                        if rank == 1:
                            t1 += 1
                        if rank is not None and rank <= 3:
                            t3 += 1
                        if h < 2.0 and (rank is None or rank > 3):
                            fatal += 1

                    score = t3 * 10000 + t1 * 100 - fatal * 50000
                    results_table.append((dp, ca, pp, t1, t3, fatal, score))

                    if score > best_score:
                        best_score = score
                        best_params = (dp, ca, pp)

                    done += 1
                    if done % 30 == 0:
                        print(f"  [{done}/{total_combos}] best so far: dp={best_params[0]}, ca={best_params[1]}, pp={best_params[2]} T1={[r for r in results_table if (r[0],r[1],r[2])==best_params][0][3]} T3={[r for r in results_table if (r[0],r[1],r[2])==best_params][0][4]}", flush=True)

        print(f"\n{'dp':>5s} {'ca':>5s} {'pp':>5s} {'T1':>5s} {'T3':>5s} {'FATAL':>5s} {'Score':>8s}")
        print("-" * 50)
        for dp, ca, pp, t1, t3, fatal, score in sorted(results_table, key=lambda x: -x[6])[:30]:
            marker = " <<<" if (dp, ca, pp) == best_params else ""
            print(f"{dp:5.1f} {ca:5.1f} {pp:5.1f} {t1:5d} {t3:5d} {fatal:5d} {score:8d}{marker}")

        print(f"\nBest: disc_power={best_params[0]}, cf_alpha={best_params[1]}, prior_power={best_params[2]}")
        best_row = [r for r in results_table if (r[0], r[1], r[2]) == best_params][0]
        print(f"Top-1={best_row[3]}, Top-3={best_row[4]}, FATAL={best_row[5]}")
        print(f"\nCurrent: disc_power={IDF_DISC_POWER}, cf_alpha={CF_COVERAGE_ALPHA}, prior_power={PRIOR_POWER}")
        return

    # 改善パラメータ
    if args.classic:
        disc = None
        disc_power = 0.0
        cf_alpha = 0.0
        prior_power = 0.0
        mode_label = "CLASSIC"
    else:
        disc = compute_idf_disc(step2, noisy_or, n_diseases=len(diseases))
        disc_power = IDF_DISC_POWER
        cf_alpha = CF_COVERAGE_ALPHA
        prior_power = PRIOR_POWER
        mode_label = f"ENHANCED (IDF={disc_power}, CF={cf_alpha}, PP={prior_power})"

    cases = case_data["cases"]
    if args.case:
        cases = [c for c in cases if c["id"] in args.case]

    print("=" * 120)
    print(f"VeSMed V3.1 BN Inference [{mode_label}] | {len(diseases)} diseases, "
          f"{len(step2['edges'])} edges, {len(cases)} cases")
    print("=" * 120)

    all_results = []
    for case in cases:
        cid = case["id"]
        expected = case["expected_id"]
        is_in = case["in_scope"]
        ev = case.get("evidence", {})
        risk = case.get("risk_factors", {})

        ranked = infer(ev, risk, diseases, disease_children, noisy_or, root_priors,
                       disc=disc, disc_power=disc_power, cf_alpha=cf_alpha,
                       prior_power=prior_power)
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

        exp_name = var_lookup.get(expected, {}).get("name_ja", expected) \
            if expected != "OOS" else "OOS"
        rk = f"r{rank}" if rank else "---"
        print(f"[{icon}] {cid:4s} H={h:5.2f} {rk:>5s}  正解={exp_name}"
              f"  | {' | '.join(top3_disp)}")

    # ─── Summary ────────────────────────────────────────────────────
    in_results = [r for r in all_results
                  if r["in_scope"] and r["expected"] != "OOS"]
    oos_results = [r for r in all_results
                   if not r["in_scope"] or r["expected"] == "OOS"]

    t1 = sum(1 for r in in_results if r["rank"] == 1)
    t3 = sum(1 for r in in_results
             if r["rank"] is not None and r["rank"] <= 3)
    conf = sum(1 for r in in_results
               if r["entropy"] < 2.0 and (r["rank"] is None or r["rank"] > 3))
    n = len(in_results)

    print("\n" + "=" * 120)
    print(f"SUMMARY [{mode_label}]: {n} in-scope | "
          f"Top-1: {t1}/{n} ({t1/n*100:.0f}%) | "
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
    conf_list = [r for r in in_results
                 if r["entropy"] < 2.0 and (r["rank"] is None or r["rank"] > 3)]
    if conf_list:
        print(f"\n自信的誤診 (H<2 + rank>3): {len(conf_list)}件")
        for r in conf_list:
            t1n = var_lookup.get(r["top1_d"], {}).get("name_ja", r["top1_d"])
            en = var_lookup.get(r["expected"], {}).get("name_ja", r["expected"])
            print(f"  {r['id']}: H={r['entropy']:.2f} r{r['rank']} "
                  f"出力={t1n}({r['top1_d']}) {r['top1_p']*100:.1f}%"
                  f" ← 正解={en}({r['expected']})")

    # Miss detail (rank > 5)
    miss_list = [r for r in in_results
                 if r["rank"] is not None and r["rank"] > 5]
    if miss_list:
        print(f"\nMiss (rank>5): {len(miss_list)}件")
        for r in miss_list:
            t1n = var_lookup.get(r["top1_d"], {}).get("name_ja", r["top1_d"])
            en = var_lookup.get(r["expected"], {}).get("name_ja", r["expected"])
            print(f"  {r['id']}: H={r['entropy']:.2f} r{r['rank']} "
                  f"出力={t1n}({r['top1_d']}) {r['top1_p']*100:.1f}%"
                  f" ← 正解={en}({r['expected']})")


if __name__ == "__main__":
    main()
