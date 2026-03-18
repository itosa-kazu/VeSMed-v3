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
import re
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


BASE_PRIOR = 0.01

# Japan 2024 population pyramid (Statistics Bureau of Japan)
# Source: stat.go.jp + UN World Population Prospects
# Used as FIXED reference distribution for demographic contrast.
JAPAN_POP = {
    "R01": {"0_1": 0.013, "1_5": 0.027, "6_12": 0.057, "13_17": 0.045,
            "18_39": 0.220, "40_64": 0.340, "65_plus": 0.298},
    "R02": {"male": 0.488, "female": 0.512},
    "R03": {"never": 0.75, "former": 0.10, "current": 0.15},
    "R04": {"no": 0.88, "yes": 0.12},
    "R05": {"no": 0.95, "yes": 0.05},
    "R06": {"no": 0.85, "tropical_endemic": 0.02, "developed": 0.03, "domestic": 0.10},
    "R07": {"no": 0.97, "yes": 0.03},
    "R08": {"no": 0.97, "yes": 0.03},
    "R09": {"no": 0.90, "yes": 0.10},
    "R10": {"no": 0.95, "yes": 0.05},
    "R11": {"no": 0.85, "yes": 0.15},
    "R12": {"no": 0.95, "yes": 0.05},
    "R13": {"no": 0.90, "yes": 0.10},
    "R14": {"no": 0.95, "yes": 0.05},
    "R15": {"no": 0.95, "yes": 0.05},
    "R16": {"no": 0.95, "yes": 0.05},
    "R17": {"no": 0.90, "yes": 0.10},
    "R18": {"no": 0.95, "yes": 0.05},
    "R19": {"spring": 0.25, "summer": 0.25, "autumn": 0.25, "winter": 0.25},
    "R20": {"no": 0.95, "yes": 0.05},
    "R21": {"no": 0.95, "yes": 0.05},
    "R22": {"no": 0.95, "yes": 0.05},
    "R23": {"no": 0.95, "yes": 0.05},
    "R24": {"no": 0.95, "yes": 0.05},
    "R25": {"no": 0.95, "yes": 0.05},
    "R26": {"no": 0.95, "yes": 0.05},
    "R29": {"no": 0.95, "yes": 0.05},
    "R30": {"none": 0.70, "livestock": 0.05, "pet_cat": 0.15, "wild_animal": 0.10},
    "R37": {"no": 0.95, "yes": 0.05},
    "R40": {"no": 0.95, "history_remission": 0.02,
            "active_on_treatment": 0.02, "active_untreated": 0.01},
    "R42": {"no": 0.95, "yes": 0.05},
    "R44": {"no": 0.85, "yes": 0.15},
    "R45": {"never": 0.75, "former": 0.10, "current": 0.15},
    "R46": {"no": 0.90, "yes": 0.10},
    "R35": {"no": 0.997, "yes": 0.003},
    "R48": {"no": 0.90, "yes": 0.10},
}


def _parse_cpt_entries(cpt, parents):
    """Parse joint CPT keys into per-parent state tuples.

    Handles three key formats:
      1. Pipe-delimited:  "state1|state2" → parts follow parent order
      2. Comma-delimited: "state1,state2" → parts follow parent order
      3. Standalone:      "state"         → single parent (typically R01 age)

    Returns: list of (state_dict, value) where state_dict maps parent_id → state.
    """
    import re
    entries = []

    # Build set of known states per parent for standalone key matching
    known = {}
    for pid in parents:
        dist = JAPAN_POP.get(pid)
        if dist:
            known[pid] = set(dist.keys())

    for key, val in cpt.items():
        val = _cpt_val_to_prior(val)
        parts = re.split(r'[|,]', key)

        if len(parts) == len(parents):
            # Full composite: parts[i] → parents[i]
            sd = {parents[i]: parts[i] for i in range(len(parents))}
            entries.append((sd, val))
        elif len(parts) == 1:
            # Standalone: find which parent it belongs to
            for pid in parents:
                if pid in known and parts[0] in known[pid]:
                    entries.append(({pid: parts[0]}, val))
                    break
        # else: part count mismatch — skip entry

    return entries


def _decompose_marginals(cpt, parents):
    """Decompose a joint CPT into per-parent individual marginals.

    For each parent R_i, computes:
      marginal[R_i][state] = Σ P(d | R_i=state, others) × pop(others) / Σ pop(others)

    This marginalizes out all other parents using JAPAN_POP weights.
    Returns: dict of {parent_id: {state: marginal_value}}
    """
    entries = _parse_cpt_entries(cpt, parents)
    if not entries:
        return {}

    from collections import defaultdict
    marginals = {}

    for target_pid in parents:
        # Accumulate weighted values for each state of target parent
        accum = defaultdict(lambda: [0.0, 0.0])  # state → [weighted_sum, weight_sum]

        for state_dict, val in entries:
            if target_pid not in state_dict:
                continue
            target_state = state_dict[target_pid]

            # Validate: target state must be a known state for this parent
            target_known = JAPAN_POP.get(target_pid)
            if target_known and target_state not in target_known:
                continue  # e.g. R01 encoded as binary "no"/"yes" — skip

            # Weight = product of other parents' population probabilities
            weight = 1.0
            for other_pid in parents:
                if other_pid == target_pid:
                    continue
                if other_pid in state_dict:
                    other_state = state_dict[other_pid]
                    pop = JAPAN_POP.get(other_pid, {})
                    weight *= pop.get(other_state, 0.5)
                # If other_pid not in state_dict (standalone entry), weight stays 1.0

            accum[target_state][0] += val * weight
            accum[target_state][1] += weight

        result = {}
        for state, (ws, wt) in accum.items():
            if wt > 0:
                result[state] = ws / wt
        if result:
            marginals[target_pid] = result

    return marginals


def _compute_single_r_lr(r_cpt, r_id, risk_evidence):
    """Compute log-LR for a single R variable given its individual CPT.

    r_cpt: dict of {state: prior_value}, e.g. {"18_39": 0.01, "65_plus": 0.03}
    Returns: log(P(d|R=obs) / P_marginal) or 0.0 if neutral.
    """
    obs = risk_evidence.get(r_id)
    if obs is None:
        pop = JAPAN_POP.get(r_id)
        obs = max(pop, key=pop.get) if pop else "no"

    p_obs = r_cpt.get(obs)
    if p_obs is None:
        p_obs = min(r_cpt.values()) if r_cpt else None
    if p_obs is None or p_obs <= 0:
        return 0.0

    pop = JAPAN_POP.get(r_id, {})
    if pop:
        p_marg = sum(r_cpt.get(s, 0) * w for s, w in pop.items())
    else:
        vals = list(r_cpt.values())
        p_marg = sum(vals) / len(vals) if vals else 0

    if p_marg <= 0:
        return 0.0

    return math.log(p_obs / p_marg)


def get_prior(disease_id, root_priors, risk_evidence, prior_power=0.0):
    """Get disease prior using independent multiplicative R-factor adjustment.

    DeepMind three-layer BN approach (Richens et al. 2020):
    Each R variable independently contributes a likelihood ratio (LR).

    Supports two data formats in full_cpts:

    Old format (joint CPT):
      {"parents": ["R01", "R11"], "cpt": {"18_39|no": 0.06, ...}}
      → Decomposed at runtime into per-R marginals

    New format (per-R individual CPTs, can coexist with old):
      {"parents": ["R11", "R19"], "cpt": {...},
       "R01": {"0_1": 0.001, ..., "65_plus": 0.03}}
      → R01 used directly, R11/R19 decomposed from joint CPT

    prior_power controls strength:
      0.0 = no demographic adjustment (all diseases equal)
      1.0 = full adjustment
    """
    rp = root_priors.get(disease_id)
    if rp is None or isinstance(rp, (int, float)) or not isinstance(rp, dict):
        return BASE_PRIOR
    if prior_power <= 0:
        return BASE_PRIOR

    # Collect all per-R individual CPTs (new format: top-level R keys)
    individual_r = {}
    for key, val in rp.items():
        if key.startswith("R") and isinstance(val, dict) and key != "cpt":
            # Verify it looks like a CPT (has string keys with numeric values)
            if any(isinstance(v, (int, float)) for v in val.values()):
                individual_r[key] = val

    # Collect R parents from joint CPT (old format)
    parents = rp.get("parents", [])
    cpt = rp.get("cpt", {})
    joint_rf_parents = [p for p in parents if p.startswith("R")]

    # Exclude R variables that already have individual CPTs from joint decomposition
    joint_rf_only = [p for p in joint_rf_parents if p not in individual_r]

    # If no R information at all, return base
    if not individual_r and not joint_rf_only:
        return BASE_PRIOR

    log_ratio_sum = 0.0

    # === Process individual per-R CPTs (new format) ===
    for r_id, r_cpt in individual_r.items():
        log_ratio_sum += _compute_single_r_lr(r_cpt, r_id, risk_evidence)

    # === Process joint CPT R parents (old format) ===
    if joint_rf_only and cpt:
        if len(joint_rf_only) == 1:
            # Single R parent in joint CPT: direct lookup
            pid = joint_rf_only[0]
            obs = risk_evidence.get(pid)
            if obs is None:
                pop = JAPAN_POP.get(pid)
                obs = max(pop, key=pop.get) if pop else "no"

            p_obs = cpt.get(obs)
            if p_obs is not None:
                p_obs = _cpt_val_to_prior(p_obs)
            else:
                vals = [_cpt_val_to_prior(v) for v in cpt.values()]
                p_obs = min(vals) if vals else None

            if p_obs is not None and p_obs > 0:
                pop = JAPAN_POP.get(pid, {})
                if pop:
                    p_marg = sum(_cpt_val_to_prior(cpt.get(s, 0)) * w
                                 for s, w in pop.items()
                                 if cpt.get(s) is not None)
                else:
                    vals = [_cpt_val_to_prior(v) for v in cpt.values()]
                    p_marg = sum(vals) / len(vals) if vals else 0

                if p_marg > 0:
                    log_ratio_sum += math.log(p_obs / p_marg)
        else:
            # Multiple R parents in joint CPT: decompose into marginals
            marginals = _decompose_marginals(cpt, joint_rf_only)
            for r_id in joint_rf_only:
                if r_id not in marginals:
                    continue
                log_ratio_sum += _compute_single_r_lr(
                    marginals[r_id], r_id, risk_evidence)

    if log_ratio_sum == 0.0:
        return BASE_PRIOR

    adjusted = BASE_PRIOR * math.exp(log_ratio_sum * prior_power)
    return max(min(adjusted, 0.5), 1e-6)


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
                   prior_power=0.0, top_n=10):
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
                       cf_alpha=cf_alpha, prior_power=prior_power)
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
                                disc_power=disc_power, cf_alpha=cf_alpha,
                                prior_power=prior_power)
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
                                  disc_power=0.0, cf_alpha=0.0,
                                  prior_power=0.0, top_n=5):
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
        prior_power=prior_power, top_n=9999
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
